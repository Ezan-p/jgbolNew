"""逐鹿 1302/event149 [A]; local opponents, schedules and soul economy [B]."""
import copy
import secrets
from . import activity as a, journey, summon
from . import activity_land_npc as npc
from .activity_land_rewards import gain, news, weekly
from .protocol import encode, decode


def table(name,key):return {int(x[key]):x for x in summon.rows(name+'.csv')}
MAPS=table('prey_map_config','map_level')
GRIDS=table('prey_open_grid','cortege_index')
CHARMS=table('prey_open_charm','index')
CONVERT=table('prey_charm_convert','charm')


def status(now,r):
    begin=a.day(now,r)*86400-r['timezone_offset_hours']*3600
    attack=begin+r['land_tower_start_hour']*3600
    return dict(is_open=True,cur_status=1 if now<attack else 3,next_status=3 if now<attack else 1,
                begin_time=begin,end_time=attack if now<attack else begin+86400)


def state(role,now,r):
    s=role['activity'].setdefault('land',dict(map_level=1,soul_count=0,grid_count=2,boss_layer=0,
        inv_boss_layer=0,total_score=0,tower_id=0,charms={},bag={},travel=None,day=-1,boss=None,hell=None,
        history={},inv_history={},auto_tower=0,unlocked=[]))
    a.require(a.day(now,r)>=s['day'] and now>=s.get('clock',0),'猎魂之地时间已回退，请恢复本地时间')
    s['clock']=now
    s.setdefault('team', None)
    npc.migrate(role,s)
    s.setdefault('week',(a.day(now,r)-4)//7)
    if s['tower_id']:
        t=s['towers'][str(s['tower_id'])]
        end=min(now,t['expire'],(s['day']+1)*86400-r['timezone_offset_hours']*3600);n=max(0,end-t['last_tick'])//r['land_tower_tick']
        gained=min(t['left_soul'],n*r['land_tower_soul'])
        gain(s,gained);t['left_soul']-=gained;t['last_tick']+=n*r['land_tower_tick']
        if gained:news(s,now,f'占塔获得{gained}魂力。')
        if now>=t['expire'] or not t['left_soul']:t['owner_type']=2;t['owner_name']=npc.catalog()[t['npc_id']]['role']['name'];s['tower_id']=0
    weekly(role,s,now,r)
    if s['day']!=a.day(now,r):
        s.update(day=a.day(now,r),travel_count=0,attack_count=0,hell_counts={},swept=False,tower_id=0,towers={},travel=None)
    if s['auto_tower'] and not s['tower_id'] and status(now,r)['cur_status']==3 and s['attack_count']<r['land_daily_attack']:
        towers(s,now,r);tid=s['map_level']*10+4;t=s['towers'][str(tid)]
        if t['left_soul']>0:
            s['tower_id']=tid;s['attack_count']+=1
            t.update(owner_type=1,owner_name=role['role_name'],last_tick=now,expire=now+r['land_tower_duration'])
    for kind,count in (('boss',5),('hell',3)):
        pending=s[kind]
        if pending:
            while len(pending['rewards'])<count:pending['rewards'].append(copy.deepcopy(secrets.choice(r['land_card_rewards'])))
    for i,row in CHARMS.items():
        if str(i) in s['charms'] and s['boss_layer']>=int(row['need_boss']):s['charms'][str(i)]['unlock']=True
        if int(row['auto_open']) and s['boss_layer']>=int(row['need_boss']):
            s['charms'].setdefault(str(i),dict(unlock=True,is_open=True,key=0,value=0))
    from .activity_land_boss import migrate_scores
    migrate_scores(s)
    from .activity_land_rewards import titles
    titles(role,s,now)
    return s


def charm_show(s):return {i:dict(s['charms'].get(str(i),dict(unlock=s['boss_layer']>=int(row['need_boss']),is_open=False,key=0,value=0))) for i,row in CHARMS.items()}

def bag(s):return {int(k):{int(v):n for v,n in values.items() if n} for k,values in s['bag'].items()}

def charm(s,kind,value,n):
    values=s['bag'].setdefault(str(kind),{});count=values.get(str(value),0)
    a.require(count+n>=0,'符咒不足');values[str(value)]=count+n


def info(s,r):
    plus={k:sum(c['value'] for c in s['charms'].values() if c['key']==k) for k in range(1,5)}
    return dict(map_level=s['map_level'],soul_count=s['soul_count'],grid_count=s['grid_count'],boss_layer=s['boss_layer'],
        inv_boss_layer=s['inv_boss_layer'],total_score=s['total_score'],tower_id=s['tower_id'],had_news=s.get('had_news',False),
        left_travel_count=r['land_daily_travel']-s['travel_count'],max_travel_count=r['land_daily_travel'],
        left_attack_count=r['land_daily_attack']-s['attack_count'],max_attack_count=r['land_daily_attack'],
        charm_plus=plus,max_level_score=3000,auto_tower=s['auto_tower'],is_clear=s['boss_layer']>=r['land_boss_layers'],is_inv_clear=s['inv_boss_layer']>=r['land_boss_layers'])


def response(op,s,r,**data):return summon.event(149,dict(flag=op,prey_info=info(s,r),**data))

def opponent(r,level=1,ident=1,count=1):
    return dict(id=ident,object_type=2,type_id=r['battle_npc'],name='逐鹿守卫',union_name='',cortege_layer=0,
        cortege_count=count,fight_power=level*100,expect_soul=r['land_travel_soul'],level=level)


def travel(s,r,role):
    a.require(s['travel_count']<r['land_daily_travel'],'今日游历次数已用完')
    s['travel_count']+=1
    # Native showChallengeLayer has exactly four portrait slots (L1751).
    n=min(4,secrets.choice(list(map(int,MAPS[s['map_level']]['count_list'].split('|')))))
    keys=[]
    for i in range(n):keys.append(npc.choose(role,s,i,excluded=keys))
    s['travel']=[npc.view(key,s['grid_count'],942001+i,r['land_travel_soul']) for i,key in enumerate(keys)]


def simulate(role,s,r,jrules,level,count=1,cur_num=None,target=None,team=False,encounter=None):
    a.require(any(1<=c.get('order',0)<=8 for c in role['corteges']),'请先上阵神仙')
    ours,enemies=journey.fighters(role,dict(cortege_list='/'.join([f"{r['battle_npc']}|{level}"]*count)))
    ours=ours[:cur_num or s['grid_count']]
    if target:
        enemies=npc.units(target,cur_num or s['grid_count'])
    if encounter is not None:
        enemies=copy.deepcopy(encounter['units'])
    if team and s.get('team'):
        members=s['team']['members'];limit=min(s['grid_count'],8//len(members))
        player_units=ours[:limit];ours=[]
        for m in members:
            group=player_units if m['id']==role['role_id'] else npc.units(m['npc_id'],limit)
            for u in group:
                # Snapshot companion IDs overlap accounts; keep NPC traits from
                # being overwritten by the player's essence/star attachment pass.
                if m['id']!=role['role_id']:u['companion_id']=-(len(ours)+1)
                u['order']=len(ours)+1;ours.append(u)
    for u in ours:
        for i,key in enumerate(('gongji','fangyu','hp','magic'),1):u[key]=u[key]*(100+info(s,r)['charm_plus'][i])//100
        u['max_hp']=u['hp']
    replay_rules=copy.deepcopy(jrules);replay_rules['battle']['max_actions']=min(r['land_max_actions'],jrules['battle']['max_actions'])
    # Rulai shields can exceed 1 KB before either army is defeated. Allow
    # those events while reserving room for 80 actions in the nested Lua replay.
    replay_rules['battle']['mechanics']['event_budget_bytes']=min(4000,jrules['battle']['mechanics']['event_budget_bytes'])
    result,lineup,actions=journey.battle(role,{},replay_rules,units=(ours,enemies))
    role['activity']['fight_id']+=1;fid=role['activity']['fight_id']
    # [A] landUI consumes nested Lua replay messages, not independent 1027 packets.
    name=encounter['name'] if encounter is not None else npc.catalog()[target]['role']['name'] if target else '逐鹿守卫'
    return result,dict(fight_events=journey.combat_engine.event_data(actions,fid),line_up_msg=decode(encode(1028,dict(fight_id=fid,first_hand=1,des_name=name,lineup_count=len(lineup),lineup=lineup)))[2],
        fight_result_msg=decode(encode(1027,dict(fight_id=fid,fight_type=21,final_result=result,fight_round=len(actions),fight_result=actions)))[2])


def towers(s,now,r):
    for i in range(1,5):
        ident=s['map_level']*10+i
        key=npc.choose(None,s,(i-1)%3,fixed=True)
        s['towers'].setdefault(str(ident),dict(id=ident,position=i,tower_type=i,create_time=now-1,
            all_soul=r['land_tower_total'],left_soul=r['land_tower_total'],owner_type=2,owner_name=npc.catalog()[key]['role']['name'],npc_id=key,
            last_tick=now,expire=now+r['land_tower_duration']))
    return [copy.deepcopy(s['towers'][str(s['map_level']*10+i)]) for i in range(1,5)]


def tower_view(role,s,t,now,r):
    from .activity_land_team import member
    owned=s['tower_id']==t['id']
    t.setdefault('npc_id',npc.choose(role,s,(t['position']-1)%3,fixed=True))
    defender=npc.view(t['npc_id'],s['grid_count'],940100+t['id'])
    if not owned:t['owner_name']=defender['name']
    if owned and s.get('team') and t['tower_type']==1:
        count=min(s['grid_count'],8//len(s['team']['members']))
        players=[dict(member(role,dict(s,grid_count=count)) if m['id']==role['role_id'] else npc.view(m['npc_id'],count,m['id']),had_soulcount=0) for m in s['team']['members']]
    else:players=([dict(member(role,s),had_soulcount=0)] if owned else [defender])
    head=players[0]
    return dict(t,player_list=players,is_owner=owned,end_time=t['expire'],role_list=[],
        owner_id=role['role_id'] if owned else defender['id'],fps_count=r['land_tower_soul'],
        soul_speed=r['land_tower_soul'],expect_soul=t['left_soul'],fight_power=sum(m.get('power',0) for m in players),
        cortege_count=sum(m['cortege_count'] for m in players),type_id=head['type_id'],cortege_layer=head['cortege_layer'])


def settle(role,req,now,r,jrules,parse):
    a.require(role['level']>=38,'逐鹿需38级');d=parse(req['data']) if req['data'] else {}
    a.require(isinstance(d,dict),'逐鹿参数无效');op=req['id'];s=state(role,now,r)
    from .activity_land_team import summary
    if op==1:return [response(1,s,r,status_info=status(now,r),team_info=summary(role,s,now,r),
        charm_show=charm_show(s),tower_info=towers(s,now,r))]
    if op==2:
        dest=d.get('des_level');a.require(type(dest)is int and dest in MAPS and dest!=s['map_level'],'地图无效')
        a.require(not s.get('team') and not s['tower_id'] and s['boss_layer']>=int(MAPS[dest]['need_boss_layer']),'尚未解锁地图或正在占塔')
        a.spend(s,'soul_count',int(MAPS[dest]['soul_count']));s['map_level']=dest;s['travel']=None
        return [response(2,s,r,tower_info=towers(s,now,r))]
    if op==3:
        a.require(status(now,r)['cur_status']==1,'当前是占塔时段')
        fresh=not s['travel']
        if fresh:travel(s,r,role)
        s['travel']=s['travel'][:4]
        # Native checkLineup reads role_id; keep scene IDs for the activity's
        # limited formation inspection, including encounters saved by old builds.
        return [response(3,s,r,enemy_list=[dict(x,role_id=x['id']) for x in s['travel']],is_new=fresh)]
    if op==17:
        a.require(s['travel'] is not None,'没有进行中的游历');s['travel']=None
        return [response(17,s,r)]
    if op==4 and d.get('des_type')==1:
        ident=d.get('des_id');candidates=(s['travel'] or [])[:4]
        a.require(type(ident)is int,'游历目标无效')
        # [A] landUI L1767 tags portraits with their 1-based array position;
        # sendChallengeRequest forwards that tag as des_id (L1807).
        target=candidates[ident-1] if 1<=ident<=len(candidates) else next((x for x in candidates if x['id']==ident),None)
        a.require(target is not None and d.get('flag')==1,'游历目标无效')
        a.require(status(now,r)['cur_status']==1,'当前是占塔时段')
        result,replay=simulate(role,s,r,jrules,target['level'],target=target.get('npc_id'));win=1<=result<=3
        reward=r['land_travel_soul'] if win else 0;drop=None
        if win:
            gain(s,reward);kind=secrets.randbelow(4)+1;charm(s,kind,5,1);drop=dict(key=kind,value=5)
        news(s,now,f"游历挑战{target['name']}：{'胜利' if win else '未获胜'}，获得{reward}魂力。")
        s['travel']=None
        return [summon.event(121,replay['fight_events']),response(4,s,r,fight_type=1,is_win=win,soul_count=reward,charm_data=drop,final_result_list=[replay])]
    if op==6:return [response(6,s,r,charm_get=bag(s),exchange_consume=r['land_charm_exchange'])]
    if op==7:
        idx=d.get('index');a.require(type(idx)is int and idx in CHARMS,'符咒位置无效');row=CHARMS[idx]
        c=s['charms'].setdefault(str(idx),dict(unlock=s['boss_layer']>=int(row['need_boss']),is_open=False,key=0,value=0))
        unlock=d.get('is_unlock',False)
        a.require(type(unlock)is bool,'解锁参数无效')
        if unlock:
            a.require(not c['unlock'] and int(row['can_force_open']),'该位置不能提前解锁')
            a.spend(s,'soul_count',int(row['force_open_soul']));c['unlock']=True
        else:
            a.require(c['unlock'] and not c['is_open'],'位置未解锁或已经开启')
            a.spend(s,'soul_count',int(row['consume_soul']));c['is_open']=True
        return [response(7,s,r,index=idx,is_unlock=unlock)]
    if op==8:
        idx,kind,value=d.get('index'),d.get('key'),d.get('value');c=s['charms'].get(str(idx))
        a.require(type(idx)is int and c is not None and c['is_open'] and type(kind)is int and type(value)is int,'符咒装备参数无效')
        a.require((kind==0 and value==0) or (kind in (1,2,3,4) and value in CONVERT),'符咒类型无效')
        a.require((kind,value)!=(c['key'],c['value']),'符咒没有变化')
        if kind:charm(s,kind,value,-1)
        if c['key']:a.spend(s,'soul_count',r['land_charm_exchange']);charm(s,c['key'],c['value'],1)
        c.update(key=kind,value=value)
        return [response(8,s,r,index=idx,key=kind,value=value)]
    if op==9:
        n=d.get('grid_count');row=GRIDS.get(n)
        a.require(type(n)is int and n==s['grid_count']+1 and row and s['boss_layer']>=int(row['boss_layer']),'阵位解锁条件不足')
        a.spend(s,'soul_count',int(row['consume_soul']));s['grid_count']=n
        return [response(9,s,r)]
    if op==10:
        s['had_news']=False
        return [response(10,s,r,news_list=list(reversed(s.get('news',[]))))]
    if op==21:
        auto=d.get('auto_tower');a.require(type(auto)is int and auto in (0,1),'占塔设置无效');s['auto_tower']=auto
        state(role,now,r)
        return [response(21,s,r)]
    if op in (18,27):
        flag=d.get('flag',1);a.require(type(flag)is int and flag in (1,2),'榜单参数无效')
        rows,mine=npc.ranking(role,s,op==27,flag,now,r)
        return [response(op,s,r,top_flag=flag,top_data=rows,my_top_data=mine)]
    if op in (5,11,16) or op==4 and d.get('des_type')==2:
        a.require(status(now,r)['cur_status']==3,'尚未到占塔时段');towers(s,now,r)
        tid=d.get('des_id') if op==4 else d.get('tower_id')
        a.require(type(tid)is int and tid in [s['map_level']*10+i for i in range(1,5)],'塔不存在');t=s['towers'][str(tid)]
        if op==11:return [response(11,s,r,tower_info=tower_view(role,s,t,now,r))]
        if op==5:
            a.require(s['tower_id']==tid,'尚未占领此塔');s['tower_id']=0;t['owner_type']=2;t['owner_name']=npc.catalog()[t['npc_id']]['role']['name']
            return [response(5,s,r,tower_id=tid)]
        a.require(not s['tower_id'] and t['left_soul']>0,'已占塔或塔内魂力耗尽')
        a.require(s['attack_count']<r['land_daily_attack'],'今日攻塔次数已用完')
        if op==16:
            a.require(t['tower_type']==4,'该塔需要战斗占领');s['attack_count']+=1;s['tower_id']=tid
            t.update(owner_type=1,owner_name=role['role_name'],last_tick=now,expire=now+r['land_tower_duration'])
            return [response(16,s,r,tower_id=tid)]
        a.require(d.get('flag')==1,'攻塔参数无效')
        tower_view(role,s,t,now,r)
        a.require(t['tower_type']!=1 or bool(s.get('team')),'铁脊塔需要先组队')
        result,replay=simulate(role,s,r,jrules,s['map_level']*5,count=s['map_level'],target=t['npc_id'],team=t['tower_type']==1);s['attack_count']+=1;win=1<=result<=3
        news(s,now,f"攻打{tid}号塔：{'胜利' if win else '未获胜'}。")
        if win:s['tower_id']=tid;t.update(owner_type=1,owner_name=role['role_name'],last_tick=now,expire=now+r['land_tower_duration'])
        return [summon.event(121,replay['fight_events']),response(4,s,r,fight_type=2,des_id=tid,is_win=win,final_result_list=[replay])]
    from .activity_land_boss import settle as boss_settle
    return boss_settle(role,s,op,d,now,r,jrules)
