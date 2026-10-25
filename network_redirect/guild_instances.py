"""Offline guild team dungeon and spirit-beast training, original callback shapes."""
from . import guild as u,journey,daily,summon
from .guild_combat import simulate
from . import guild_offline as offline


def state(s):
    a=s.setdefault('instances',{})
    if a.get('day')!=s['day']:
        a.update(train_claimed_stage=0,paid_tasks=0,train_hp=None,train_end=0,train_damage={},train_support=0,layer=0,search_tiles=[],search_order=[],search_bought={},tasks=[],wander=0,field=None,shop_bought={},rank_claimed=False,day=s['day'],team=None,team_fights=0,search=0,points=0,board=[],train_open=False,train_done=False,train_claimed=False,train_record=[],catch=0,reputation=a.get('reputation',0),pets=a.get('pets',[]))
    week=(s['day']+3)//7
    if a.get('week')!=week:
        a['previous_week_score']=0 if a.get('week_claimed') else a.get('week_score',0);a['week_score']=0;a['week']=week;a['week_claimed']=False
    for k,v in dict(train_claimed_stage=4 if a.get('train_claimed') else 0,train_end=0,train_damage={},train_support=0,layer=0,paid_tasks=0).items():a.setdefault(k,v)
    offline.pets(a)
    return a


def team_applications(team):
    # showJoinTeamPage overwrites each row.id with its table key.
    return {int(key):dict(row) for key,row in (team or {}).get('applications',{}).items()}


def team_info(role,a,g,r):
    t=a['team'];members=[]
    if t:
        members=[dict(g['members'][rid],head_type=next((c['type'] for c in role['corteges'] if c.get('order')),5004),cortege_layer=a.get('layer',0),finish_fam_data=a.get('layer',0)) for rid in t['members'] if rid in g['members']]
    return dict(teams=members,captain=t.get('captain',role['role_id']) if t else 0,max_count=r['team_size'],free_times=r['team_daily'],fight_count=a['team_fights'],
        apply_list=team_applications(t),last_search_time=0,max_layer=max(1,a.get('layer',0)),fam_id=1,fam_count=max(1,len(members)),can_support_fight=True)


def team_list(role,a,g,r):
    rows=[]
    if a['team']:
        captain=a['team'].get('captain',int(role['role_id']))
        rows.append(dict(name=g['members'][str(captain)]['name'],captain=captain,count=len(a['team']['members']),avg_level=role['level'],had_fight=a['team_fights']>0))
    else:
        rows=[dict(name=m['name'],captain=m['id'],count=1,avg_level=m['level'],had_fight=False) for key,m in g['members'].items() if key!=str(int(role['role_id']))]
    return dict(teams=rows,max_count=r['team_size'],free_times=r['team_daily'],fight_count=a['team_fights'])


def train_info(role,a,g,now,r):
    return dict(result=54 if a['train_done'] else 1 if a['train_open'] else 61,last_time=a.get('train_end',0),rest_time=a.get('train_end',0),
        pet_info={1:len(a['pets']),2:0},train_prize={i:dict(add_union_gold=i*100,add_reputation=i*10,prize_list=[daily.spec(p[:2]+[p[2]*i,p[3]]) for p in r['train_rewards']]) for i in range(1,5)},
        boss_type=r['battle_npc'],boss_layer=1,has_record=bool(a['train_record']),boss_info=dict(type_id=r['battle_npc'],boss_hp=a.get('train_hp') if a.get('train_hp') is not None else r['train_hp'],boss_full_hp=r['train_hp']),
        name=g['members'].get(str(a.get('appoint',role['role_id'])),{}).get('name',role['role_name']),support=a.get('train_support',0),can_support=a.get('train_support',0)<r['train_support_limit'],damage_rank=sorted(a.get('train_damage',{}).values(),key=lambda v:-v['damage']))


def inside(a,now,r):
    return dict(result=1,week_reputation=a['reputation'],total_catch_times=a['catch'],left_catch_times=max(0,r['catch_daily']-a['catch']),task_last_time=now+3600,
                pet_category_info={i:{p:a['pets'].count(p) for p in a['pets'] if p//100==i} for i in range(1,5)},pet_entities=[dict(p,power=offline.pet_power(p)) for p in offline.pets(a)])


def settle(role,s,g,op,d,now,r):
    a=state(s);rid=str(int(role['role_id']))
    if op in (26,27,28,29,30,31,32,33,44,50,73,74,75):
        if op==26:
            u.require(a['team'] is None,'已经在队伍中');a['team']=dict(members=[rid],captain=int(role['role_id']),applications={key:dict(m,apply_time=now) for key,m in g['members'].items() if key!=rid and m.get('npc')})
            return [u.notice(op),u.reply(44,dict(result=1,team=team_info(role,a,g,r)))]
        if op==27:
            u.require(a['team'] is None,'已经在队伍中');target=str(u.positive(d,'leader_id'));u.require(target in g['members'] and target!=rid,'队伍不存在')
            a['team']=dict(members=[target,rid],captain=int(target),applications={},application_log=[dict(role_id=int(rid),time=now,status='npc_accepted')])
            return [u.notice(28),u.reply(44,dict(result=1,team=team_info(role,a,g,r)))]
        if op in (31,32):
            u.require(a['team'] is not None,'尚未组队')
            if op==32:u.require(a['team'].get('captain')==int(role['role_id']),'只有队长可以解散')
            a['team']=None
            return [u.notice(op),u.reply(32,dict(result=1)),u.reply(44,dict(result=21,team=team_list(role,a,g,r)))]
        if op==33:
            u.require(a['team'] is not None and a['team'].get('captain')==int(role['role_id']),'只有队长可以移除成员');target=str(u.positive(d,'role_id'));u.require(target in a['team']['members'] and target!=rid,'成员无效');a['team']['members'].remove(target)
        if op in (28,29,30):
            u.require(a['team'] is not None and a['team']['captain']==int(rid),'只有队长可以审核')
            pending=a['team'].setdefault('applications',{})
            if op==30:pending.clear()
            else:
                selected=d.get('role_list',[d.get('role_id')])
                if isinstance(selected,dict):selected=list(selected.values())
                u.require(isinstance(selected,list) and selected and all(type(v)is int and v>0 for v in selected) and len(set(selected))==len(selected),'申请成员列表无效')
                u.require(all(str(v) in pending and str(v) in g['members'] for v in selected),'申请不存在')
                if op==28:u.require(len(a['team']['members'])+len(selected)<=r['team_size'],'队伍已满')
                for ident in selected:
                    target=str(ident)
                    if op==28:a['team']['members'].append(target)
                    del pending[target]
            return [u.notice(op),u.reply(op,dict(result=1,team=team_info(role,a,g,r)))]
        if op==50:
            u.require(a['team'] is not None,'请先创建队伍')
            return [u.reply(50,team_applications(a['team']))]
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
                a['layer']=a.get('layer',0)+1
                a['member_contributions']={key:a['layer'] for key in a['team']['members']}
                for p in r['team_rewards']:journey.grant(role,p)
        return [u.reply(op,dict(result=1,free_times=r['team_daily'],fight_count=a['team_fights'],fight_result_list=a.get('team_record',[])))]
    if op==43:
        from . import activity
        flag=d.get('flag');u.require(type(flag)is int and flag in range(1,8),'寻宝操作无效')
        bought=a.setdefault('search_bought',{})
        def stock():return [dict(daily.spec(p),cost_score=20,buy_times=max(0,5-bought.get(str(i),0))) for i,p in enumerate(r['train_rewards'],1)]
        if not a.get('search_tiles'):
            a['search_tiles']=[dict(item=daily.spec(r['search_rewards'][offline.roll(s,len(r['search_rewards']))]),had_token=i<a['search']) for i in range(25)]
            positions=list(range(1,26));a['search_order']=[]
            while positions:a['search_order'].append(positions.pop(offline.roll(s,len(positions))))
        prizes=[];sweep_prizes={};new_broadcast=[]
        if flag in (2,6):
            n=1 if flag==2 else r['search_daily']-a['search']
            u.require(n>0 and a['search']+n<=r['search_daily'],'今日寻宝次数已用完')
            if flag==6:u.pay(role,'gold_coin',r['search_sweep_gold'])
            for _ in range(n):
                a['search']+=1;a['points']+=10
                tile=a['search_tiles'][a['search']-1];tile['had_token']=True;item=tile['item']
                prize=[item['object_type'],item['attach_type'],item['attach_count'],item['attach_level']]
                index=a['search_order'][a['search']-1]
                row=dict(index=index,server_index=a['search'],object_type=prize[0],attach_type=prize[1],attach_count=prize[2],attach_level=prize[3],point=10,random_sort=index,name=role['role_name'],tips='寻宝获得10积分')
                a['board'].append(row);new_broadcast.append(row)
                granted=journey.grant(role,prize);prizes.append(granted);sweep_prizes[a['search']]=granted
        if flag==4:
            idx=u.positive(d,'index',len(r['train_rewards']))
            u.require(a['points']>=20 and bought.get(str(idx),0)<5,'积分或购买次数不足')
            a['points']-=20;bought[str(idx)]=bought.get(str(idx),0)+1;prizes=[journey.grant(role,r['train_rewards'][idx-1])]
        if flag==5:
            n=u.positive(d,'index',100);activity.consume(role,1035,n);a['points']+=n*r['search_card_points']
        if flag==7:
            u.require(a['team'] is not None,'请先加入队伍')
            return [u.reply(op,dict(result=1,flag=7,fam_info=team_info(role,a,g,r)))]
        return [u.reply(op,dict(result=1,flag=flag,index=d.get('index',0),attach_list=prizes,free_times=r['search_daily']-a['search'],fight_count=a['team_fights'],sweep_gold_cost=r['search_sweep_gold'],token_index=min(a['search']+1,25),my_broad_data=a['board'][-1] if flag==2 else new_broadcast,gold_cost=10,all_point=a['points'],get_point=10,prize_list=sweep_prizes if flag==6 else prizes,prize_items=a['search_tiles'],search_order=a['search_order'],max_free_times=r['search_daily'],broad_data=a['board'],store_items=stock(),board_size=25,flush_time=(s['day']+1)*86400-r['timezone_offset_hours']*3600))]
    if op==79:return [u.reply(op,train_info(role,a,g,now,r))]
    if op in (80,78):
        u.authorize(role,r,27);u.require(not a['train_done'],'今日试炼已完成')
        u.require(role['level']>=r['join_level'],'人物等级不足')
        if op==80:
            u.require(not a['train_open'],'已开启试炼');a.update(train_open=True,train_hp=r['train_hp'],train_end=now+r['train_seconds'],train_damage={},train_support=0)
        else:
            u.require(a['train_open'] and now<a['train_end'],'试炼未开启或已过期')
            u.require(a['train_support']<r['train_support_limit'],'援助次数已用完');a['train_support']+=1
        result,packets,replay=simulate(role,s,r,journey.load_rules(),27,'仙盟灵兽试炼',a['train_hp'])
        damage=min(a['train_hp'],sum(sum(max(0,v) for v in row['damage_list']) for row in replay['fight_result_msg']['fight_result'] if row['is_src']))
        a['train_hp']-=damage;a['train_done']=a['train_hp']==0;a['train_record'].append(replay)
        row=a['train_damage'].setdefault(rid,dict(id=int(rid),name=role['role_name'],damage=0));row['damage']+=damage
        return [u.reply(op,dict(result=1,support=a['train_support'],free_times=1,fight_count=len(a['train_record']),fight_result_list=a['train_record'])),u.reply(79,train_info(role,a,g,now,r))]
    if op==95:return [u.reply(op,dict(result=1,free_times=1,fight_count=1 if a['train_record'] else 0,fight_result_list=a['train_record']))]
    if op==81:
        u.authorize(role,r,27);target=d.get('appoint_role');u.require(str(target) in g['members'],'指定成员不存在');a['appoint']=target
        return [u.reply(op,dict(result=1,name=g['members'][str(target)]['name']))]
    if op==82:
        hp=a.get('train_hp');stage=4 if a['train_done'] else 0 if hp is None else (r['train_hp']-hp)*4//r['train_hp']
        last=a.get('train_claimed_stage',0);u.require(stage>last,'尚未达到下一阶段或奖励已领取')
        count=stage-last
        prizes=[journey.grant(role,p[:2]+[p[2]*count,p[3]]) for p in r['train_rewards']]
        a['train_claimed_stage']=stage;a['train_claimed']=stage==4;a['reputation']+=10*count
        a['week_score']=a.get('week_score',0)+10*count;a['total_reputation']=a.get('total_reputation',0)+10*count
        money=offline.funds(g,100*count,r)
        return [u.reply(op,dict(result=1,prize_list=prizes,add_reputation=10*count,add_union_gold=money,add_catch_count=0))]
    if op==88:return [u.reply(op,inside(a,now,r))]
    if op==89:
        u.require(a['catch']<r['catch_daily'],'今日捕获次数已用完');u.pay(role,'gold_coin',r['catch_gold']);a['catch']+=1;offline.add_pet(a,101+offline.roll(s,5),s,r)
        return [u.reply(op,dict(result=1,index=a['pets'][-1]-100)),catch_update(a,role,a['pets'][-1],now)]
    u.require(False,'仙盟副本操作无效')


def catch_update(a,role,tid,now):
    if tid is not None:
        a['catch_history']=(a.get('catch_history',[])+[dict(name=role['role_name'],type_id=tid,time=now)])[-30:]
    return u.reply(94,dict(result=1,catch_list=a.get('catch_history',[])))
