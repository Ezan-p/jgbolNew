"""Server-authoritative guild battles, original fixed-width replay format."""
import copy
from . import guild as u, journey, summon
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


def recent_records(records):
    """Keep complete newest replays within the native Lua event packet budget."""
    selected = []
    for replay in reversed(records):
        if len(summon.lua([replay] + selected).encode('utf-8')) > 28000:
            break
        selected.insert(0, replay)
    return selected


def simulate(role,s,r,jrules,ft,name,hp=None):
    u.require(any(c.get('order') for c in role['corteges']),'请先上阵神仙')
    units=journey.fighters(role,dict(cortege_list=f"{r['battle_npc']}|{r['battle_level']}"))
    if ft==15 and s.get('feast_fam_rate',0):
        for unit in units[0]:
            for key in ('hp','max_hp','gongji','fangyu','magic'):unit[key]=unit[key]*(100+s['feast_fam_rate'])//100
    if ft in (15,27,28):
        from .guild_offline import pets,pet_power
        a=s.get('instances',{})
        bonus=min(100,sum(pet_power(p) for p in pets(a))//100)
        team=a.get('team') or {}
        bonus+=max(0,len(team.get('members',[]))-1)*10 if ft==15 else 0
        for unit in units[0]:
            for key in ('hp','max_hp','gongji','fangyu','magic'):unit[key]=unit[key]*(100+bonus)//100
    if hp is not None:units[1][0].update(hp=hp,max_hp=hp)
    rules=copy.deepcopy(jrules);rules['battle']['max_actions']=min(60,rules['battle']['max_actions'])
    rules['battle']['mechanics']['event_budget_bytes']=1000
    result,lineup,actions=journey.battle(role,{},rules,units=units,slots=8)
    s['fight_id']=s.get('fight_id',0)+1;fid=s['fight_id']
    packets=[encode(1028,dict(fight_id=fid,first_hand=1,des_name=name,lineup_count=len(lineup),lineup=lineup)),
             encode(1027,dict(fight_id=fid,fight_type=ft,final_result=result,fight_round=len(actions),fight_result=actions))]
    return result,journey.combat_engine.event_packets(actions,fid)+packets,dict(
        line_up_msg=decode(packets[0])[2],fight_result_msg=decode(packets[1])[2],
        fight_events=journey.combat_engine.event_data(actions,fid),damage_total=journey.combat_engine.total_damage(actions))


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
