"""Server-authoritative guild battles, original fixed-width replay format."""
import copy
from . import guild as u, journey, summon, npc_players, combat, reborn_stars, spirit_array
from .protocol import encode,decode


def replay_damage(replay):
    return replay.get('damage_total', journey.combat_engine.total_damage(replay['fight_result_msg']['fight_result']))


def record_events(records):
    # Rehydrate numeric Lua array keys after JSON persistence.
    packets = []
    for replay in records:
        data = replay.get('fight_events')
        if data:
            packets.append(summon.event(121, {int(k) if str(k).isdigit() else k: v for k, v in data.items()}))
    return packets


def client_records(records):
    """JSON object keys become strings; preserve native numeric event indexes."""
    records=copy.deepcopy(records)
    for replay in records:
        if replay.get('fight_events'):
            replay['fight_events']={int(k) if str(k).isdigit() else k:v for k,v in replay['fight_events'].items()}
    return records


def recent_records(records):
    """Keep complete newest replays within the native Lua event packet budget."""
    selected = []
    for replay in reversed(records):
        if len(summon.lua([replay] + selected).encode('utf-8')) > 28000:
            break
        selected.insert(0, replay)
    return client_records(selected)


def player_units(role):
    """Take an immutable player's actual formation, including attached effects."""
    units=journey.fighters(role,dict(cortege_list='1001|1'))[0]
    combat.attach_essences(role,units)
    reborn_stars.attach_combat_traits(role,units)
    # Joint formation has no shared owner. Attach each owner's bonuses before
    # moving slots, then use a neutral combat owner to avoid double attachment.
    home=role.get('activity',{}).get('home',{}).get('train',{})
    if home:
        from fractions import Fraction
        from .activity_home import TRAIN
        bonuses=[tuple(map(Fraction,TRAIN[i,home.get(str(i),{}).get('level',0)]['worth'].split('|')))
                 if home.get(str(i),{}).get('level',0) else (0,0) for i in range(1,5)]
        for unit in units:unit['training_bonuses']=bonuses
    spirit_array.attach_combat(role,units)
    return units


def joint_units(roles):
    """[B] Round-robin eight slots: every 3–5 participant fields real units."""
    armies=[player_units(actor) for actor in roles]
    u.require(all(armies),'队员尚未配置出战神仙')
    selected=[];sources=[];power=0
    for index in range(max(map(len,armies))):
        for actor,army in zip(roles,armies):
            if index>=len(army):continue
            unit=army[index];original=unit['order'];unit['order']=len(selected)+1
            source=next(c for c in actor['corteges'] if c.get('order')==original)
            power+=source.get('combat_power',0)
            # IDs are scoped to their source account and can collide. A negative
            # local marker prevents the engine matching a different owner.
            unit['companion_id']=-len(selected)-1
            selected.append(unit)
            sources.append(dict(role_id=actor['role_id'],name=actor['role_name'],
                                npc_id=npc_players.resolve(actor['role_id']) or '',
                                source_order=original,order=unit['order'],type=unit['type']))
            if len(selected)==8:return selected,sources,power
    return selected,sources,power


def choose_enemy(role,s,*,power=None,layer=0,excluded=()):
    """[B] Pick among nearby-power immutable players, growing 8% per layer."""
    from .guild_offline import roll
    own=power if power is not None else sum(c.get('combat_power',0) for c in role['corteges'] if 1<=c.get('order',0)<=8)
    target=max(1,own)*(75+min(100,layer*8))//100
    excluded=set(excluded)
    candidates=[]
    for key,entry in npc_players.catalog().items():
        if entry['profile']['role_id'] in excluded:continue
        raw=npc_players.source_file(entry['source_file'])[key]
        if raw.get('battle_validation',{}).get('status')=='replay_limit_observed':continue
        candidates.append(entry)
    u.require(candidates,'没有可用的仙盟NPC阵容')
    candidates.sort(key=lambda row:(abs(row['profile']['role_combat_power']-target),
                                    abs(row['profile']['level']-role['level']),row['npc_id']))
    distance=abs(candidates[0]['profile']['role_combat_power']-target)
    close=[row for row in candidates[:8] if abs(row['profile']['role_combat_power']-target)<=distance+max(1,target//5)]
    return close[roll(s,len(close))]['npc_id']


def simulate(role,s,r,jrules,ft,name,hp=None,*,enemy_npc=None,ally_roles=None,actor_role=None):
    actor=actor_role or role
    u.require(any(1<=c.get('order',0)<=8 for c in actor['corteges']),'请先上阵神仙')
    units=journey.fighters(actor,dict(cortege_list=f"{r['battle_npc']}|{r['battle_level']}"))
    if ft==27:
        boost=s.get('instances',{}).get('train_support',0)*r['train_support_percent']
        for unit in units[0]:
            for key in ('hp','max_hp','gongji','fangyu','magic'):unit[key]=unit[key]*(100+boost)//100
    sources=[];battle_owner=actor
    if ally_roles:
        allies,sources,power=joint_units(ally_roles)
        units=(allies,units[1])
        battle_owner=dict(role_id=role['role_id'],level=role['level'],corteges=[],attachments=[])
        if enemy_npc is None:
            a=s.setdefault('instances',{});floor=str(a.get('layer',0))
            opponents=a.setdefault('team_opponents',{})
            if floor not in opponents:
                opponents[floor]=choose_enemy(role,s,power=power,layer=a.get('layer',0),excluded=[v['role_id'] for v in ally_roles])
            enemy_npc=opponents[floor]
    if enemy_npc is not None:
        enemy=npc_players.get(enemy_npc);u.require(enemy is not None,'仙盟NPC阵容不存在')
        units=(units[0],player_units(enemy['role']))
        name=enemy['role']['role_name']
    if ft==15 and s.get('feast_fam_rate',0):
        for unit in units[0]:
            for key in ('hp','max_hp','gongji','fangyu','magic'):unit[key]=unit[key]*(100+s['feast_fam_rate'])//100
    if ft in (15,27,28):
        from .guild_offline import pets,pet_power
        a=s.get('instances',{})
        bonus=min(100,sum(pet_power(p) for p in pets(a))//100)
        for unit in units[0]:
            for key in ('hp','max_hp','gongji','fangyu','magic'):unit[key]=unit[key]*(100+bonus)//100
    if hp is not None:units[1][0].update(hp=hp,max_hp=hp)
    rules=copy.deepcopy(jrules);rules['battle']['max_actions']=min(60,rules['battle']['max_actions'])
    rules['battle']['mechanics']['event_budget_bytes']=1000
    result,lineup,actions=journey.battle(battle_owner,{},rules,units=units,slots=8)
    s['fight_id']=s.get('fight_id',0)+1;fid=s['fight_id']
    packets=[encode(1028,dict(fight_id=fid,first_hand=1,des_name=name,lineup_count=len(lineup),lineup=lineup)),
             encode(1027,dict(fight_id=fid,fight_type=ft,final_result=result,fight_round=len(actions),fight_result=actions))]
    replay=dict(line_up_msg=decode(packets[0])[2],fight_result_msg=decode(packets[1])[2],
        fight_events=journey.combat_engine.event_data(actions,fid),damage_total=journey.combat_engine.total_damage(actions))
    if sources:replay['participants']=sources
    if enemy_npc is not None:replay['enemy_npc']=enemy['npc_id']
    if actor_role is not None:replay['actor_role_id']=actor['role_id']
    return result,journey.combat_engine.event_packets(actions,fid)+packets,replay


def fight(role,req,now,r,jrules):
    s,g=u.prepare(role,now,r);u.require(g is not None,'请先加入仙盟');ft=req['fight_type']
    if ft==13:
        u.authorize(role,r,15);t=g['tree'];u.require(t['state']==3,'神树尚未进入守护阶段')
        u.require(req['des_type'] in (1,2),'守护方式无效')
        if req['des_type']==2:u.pay(role,'gold_coin',r['tree_flush_gold'])
        else:u.require(now>=t.get('cooltime',0),'守护冷却中')
        full=r['tree_boss_hp']*(100+(t['level']-1)*10)//100
        old=t.get('hp',full);result,packets,replay=simulate(role,s,r,jrules,ft,'神树守护',old)
        damage=replay_damage(replay)
        # Damage is read from the authoritative replay, including unsuccessful attempts.
        damage=min(old,damage);t['hp']=old-damage;t['cooltime']=now+r['tree_fight_cooldown']
        rank=next((x for x in t['ranks'] if x['id']==role['role_id']),None)
        if rank is None:rank=dict(id=role['role_id'],name=role['role_name'],order=1,challenge_count=0,damage=0);t['ranks'].append(rank)
        rank['damage']+=damage;rank['challenge_count']+=1
        used=s.get('tree_reward_count',0)
        if used<r['tree_challenge_limit']:
            u.contribution(role,r['tree_challenge_contrib']);s['tree_reward_count']=used+1
        if req['des_type']==2:journey.grant(role,[5,1001,r['tree_paid_peaches'],1])
        t['ranks'].sort(key=lambda x:-x['damage'])
        for i,x in enumerate(t['ranks'],1):x['order']=i
        if not t['hp']:
            for p in r['tree_rewards']:journey.grant(role,p)
            bonus=max(1,4-rank['order']);u.contribution(role,bonus*r['tree_challenge_contrib'])
            t.update(state=1,planted=0);t.pop('hp',None)
        return packets+[u.reply(16,u.tree_data(role,s,g,now,r)),summon.event(44,dict(fight_id=s['fight_id'],fight_type=ft))]
    if ft==19:
        from . import guild_escort
        return guild_escort.rob(role,s,g,guild_escort.state(s),dict(des_id=req['des_id'],flush_cd=req['des_type']==2),now,r)
    if ft in (14,16,17):
        from . import guild_match
        return guild_match.fight(role,s,g,req,now,r,jrules)
    u.require(False,'该仙盟战斗尚未完成接入')
