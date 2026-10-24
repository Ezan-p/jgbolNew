"""Offline guild team dungeon and spirit-beast training, original callback shapes."""
from . import guild as u,journey,daily,summon
from .guild_combat import simulate


def state(s):
    a=s.setdefault('instances',{})
    if a.get('day')!=s['day']:
        a.update(search_bought={},tasks=[],wander=0,field=None,shop_bought={},rank_claimed=False,day=s['day'],team=None,team_fights=0,search=0,points=0,board=[],train_open=False,train_done=False,train_claimed=False,train_record=[],catch=0,reputation=a.get('reputation',0),pets=a.get('pets',[]))
    return a


def team_info(role,a,g,r):
    t=a['team'];members=[]
    if t:
        members=[dict(g['members'][rid],head_type=next((c['type'] for c in role['corteges'] if c.get('order')),5004),cortege_layer=0,finish_fam_data=0) for rid in t['members'] if rid in g['members']]
    return dict(teams=members,captain=t.get('captain',role['role_id']) if t else 0,max_count=r['team_size'],free_times=r['team_daily'],fight_count=a['team_fights'],
        apply_list={},last_search_time=0,max_layer=max(1,a['team_fights']),fam_id=1,fam_count=1,can_support_fight=True)


def team_list(role,a,g,r):
    rows=[]
    if a['team']:
        captain=a['team'].get('captain',int(role['role_id']))
        rows.append(dict(name=g['members'][str(captain)]['name'],captain=captain,count=len(a['team']['members']),avg_level=role['level'],had_fight=a['team_fights']>0))
    else:
        rows=[dict(name=m['name'],captain=m['id'],count=1,avg_level=m['level'],had_fight=False) for key,m in g['members'].items() if key!=str(int(role['role_id']))]
    return dict(teams=rows,max_count=r['team_size'],free_times=r['team_daily'],fight_count=a['team_fights'])


def train_info(role,a,g,now,r):
    return dict(result=54 if a['train_done'] else 1 if a['train_open'] else 61,last_time=now+3600,rest_time=now+3600,
        pet_info={1:len(a['pets']),2:0},train_prize={i:dict(add_union_gold=i*100,add_reputation=i*10,prize_list=[daily.spec(p) for p in r['train_rewards']]) for i in range(1,5)},
        boss_type=r['battle_npc'],boss_layer=1,has_record=bool(a['train_record']),boss_info=dict(type_id=r['battle_npc'],boss_hp=10000,boss_full_hp=10000),
        name=g['members'].get(str(a.get('appoint',role['role_id'])),{}).get('name',role['role_name']),support=0,can_support=True)


def inside(a,now,r):
    return dict(result=1,week_reputation=a['reputation'],total_catch_times=a['catch'],left_catch_times=max(0,r['catch_daily']-a['catch']),task_last_time=now+3600,
                pet_category_info={i:{p:1 for p in a['pets'] if (p-1)%4+1==i} for i in range(1,5)})


def settle(role,s,g,op,d,now,r):
    a=state(s);rid=str(int(role['role_id']))
    if op in (26,27,28,29,30,31,32,33,44,50,73,74,75):
        if op==26:
            u.require(a['team'] is None,'已经在队伍中');a['team']=dict(members=[rid],captain=int(role['role_id']))
            return [u.notice(op),u.reply(44,dict(result=1,team=team_info(role,a,g,r)))]
        if op==27:
            u.require(a['team'] is None,'已经在队伍中');target=str(u.positive(d,'leader_id'));u.require(target in g['members'] and target!=rid,'队伍不存在')
            a['team']=dict(members=[target,rid],captain=int(target))
            return [u.notice(28),u.reply(44,dict(result=1,team=team_info(role,a,g,r)))]
        if op in (31,32):
            u.require(a['team'] is not None,'尚未组队')
            if op==32:u.require(a['team'].get('captain')==int(role['role_id']),'只有队长可以解散')
            a['team']=None
            return [u.notice(op),u.reply(32,dict(result=1)),u.reply(44,dict(result=21,team=team_list(role,a,g,r)))]
        if op==33:
            u.require(a['team'] is not None and a['team'].get('captain')==int(role['role_id']),'只有队长可以移除成员');target=str(u.positive(d,'role_id'));u.require(target in a['team']['members'] and target!=rid,'成员无效');a['team']['members'].remove(target)
        if op in (28,29):u.require(False,'没有待处理的组队申请')
        if op==73:return [u.reply(op,dict(result=1,team=team_list(role,a,g,r)))]
        if op==74:u.require(a['team'] is not None,'队伍不存在')
        return [u.reply(op if op in (44,50,74,75) else 44,dict(result=1 if a['team'] else 21,team=team_info(role,a,g,r) if a['team'] else team_list(role,a,g,r)))]
    if op in (41,42):
        u.require(a['team'] is not None,'请先创建队伍')
        if op==41:
            u.require(a['team_fights']<r['team_daily'],'秘境挑战次数已用完')
            result,packets,replay=simulate(role,s,r,journey.load_rules(),15,'仙盟秘境')
            a['team_fights']+=1;a['team_record']=[replay]
            if 1<=result<=3:
                for p in r['team_rewards']:journey.grant(role,p)
        return [u.reply(op,dict(result=1,free_times=r['team_daily'],fight_count=a['team_fights'],fight_result_list=a.get('team_record',[])))]
    if op==43:
        from . import activity
        flag=d.get('flag');u.require(type(flag)is int and flag in range(1,8),'寻宝操作无效')
        bought=a.setdefault('search_bought',{})
        def stock():return [dict(daily.spec(p),cost_score=20,buy_times=max(0,5-bought.get(str(i),0))) for i,p in enumerate(r['train_rewards'],1)]
        prizes=[]
        if flag in (2,6):
            n=1 if flag==2 else r['search_daily']-a['search']
            u.require(n>0 and a['search']+n<=r['search_daily'],'今日寻宝次数已用完')
            for _ in range(n):
                a['search']+=1;a['points']+=10
                a['board'].append(dict(index=a['search'],server_index=a['search'],object_type=12,attach_type=0,attach_count=1000,attach_level=1,point=10,random_sort=a['search']))
                prizes.append(journey.grant(role,[12,0,1000,1]))
        if flag==4:
            idx=u.positive(d,'index',len(r['train_rewards']))
            u.require(a['points']>=20 and bought.get(str(idx),0)<5,'积分或购买次数不足')
            a['points']-=20;bought[str(idx)]=bought.get(str(idx),0)+1;prizes=[journey.grant(role,r['train_rewards'][idx-1])]
        if flag==5:
            n=u.positive(d,'index',100);activity.consume(role,1035,n);a['points']+=n*r['search_card_points']
        if flag==7:
            u.require(a['team'] is not None,'请先加入队伍')
            return [u.reply(op,dict(result=1,flag=7,fam_info=team_info(role,a,g,r)))]
        return [u.reply(op,dict(result=1,flag=flag,index=d.get('index',0),attach_list=prizes,free_times=r['search_daily']-a['search'],fight_count=a['team_fights'],sweep_gold_cost=10,token_index=min(a['search']+1,25),my_broad_data=a['board'][-1] if flag==2 else a['board'],gold_cost=10,all_point=a['points'],get_point=10,prize_list=prizes,store_items=stock(),flush_time=now+86400))]
    if op==79:return [u.reply(op,train_info(role,a,g,now,r))]
    if op in (80,78):
        u.authorize(role,r,27);u.require(not a['train_done'],'今日试炼已完成')
        if op==80:u.require(not a['train_open'],'已开启试炼');a['train_open']=True
        else:u.require(a['train_open'],'请先开启试炼')
        result,packets,replay=simulate(role,s,r,journey.load_rules(),27,'仙盟灵兽试炼');a['train_record']=[replay];a['train_done']=1<=result<=3
        return [u.reply(op,dict(result=1,support=op==78,free_times=1,fight_count=1,fight_result_list=a['train_record']))]
    if op==95:return [u.reply(op,dict(result=1,free_times=1,fight_count=1 if a['train_record'] else 0,fight_result_list=a['train_record']))]
    if op==81:
        u.authorize(role,r,27);target=d.get('appoint_role');u.require(str(target) in g['members'],'指定成员不存在');a['appoint']=target
        return [u.reply(op,dict(result=1,name=g['members'][str(target)]['name']))]
    if op==82:
        u.require(a['train_done'] and not a['train_claimed'],'试炼未完成或奖励已领取')
        prizes=[journey.grant(role,p) for p in r['train_rewards']];a['train_claimed']=True;a['reputation']+=10
        return [u.reply(op,dict(result=1,prize_list=prizes,add_reputation=10,add_catch_count=0))]
    if op==88:return [u.reply(op,inside(a,now,r))]
    if op==89:
        u.require(a['catch']<r['catch_daily'],'今日捕获次数已用完');u.pay(role,'gold_coin',r['catch_gold']);a['catch']+=1;a['pets'].append((a['catch']-1)%6+1)
        return [u.reply(op,dict(result=1,index=a['pets'][-1])),u.reply(94,inside(a,now,r))]
    u.require(False,'仙盟副本操作无效')
