"""Guild beast quests and wilderness: persistent inferred local progression."""
from . import guild as u,daily,journey
from .guild_instances import state, weekend, resident_info, residents
from .guild_combat import simulate, record_events, choose_enemy
from . import guild_offline as offline


def prepare(s):
    a=state(s)
    for k,v in dict(tasks=[],wander=0,field=None,shop_bought={},rank_claimed=False).items():a.setdefault(k,v)
    return a


def task(r,index,day=0):
    reward=dict(add_reputation=10*index,prize_list=[daily.spec(p[:2]+[p[2]*index,p[3]]) for p in r['hunt_rewards']])
    return dict(task_info={1:[101+(day+index)%5],2:[201+(day+index)%6],3:[]},prize_info=[reward,reward],boss_info=dict(cur_hp=10000,max_hp=10000,cost_gold=10,fight_count=0),index=index)


def main(a,now,r,g):
    return dict(result=1,cur_reputation=a['reputation'],free_task_times=max(0,r['hunt_daily']-len(a['tasks'])) if r['hunt_weekend_open'] or not weekend(a) else 0,pay_task_times=max(0,r['hunt_paid_limit']-a.get('paid_tasks',0)) if r['hunt_weekend_open'] or not weekend(a) else 0,pay_task_gold=r['hunt_gold'],
        union_task=[task(r,i,a['day']) for i in range(1,4)] if r['hunt_weekend_open'] or not weekend(a) else [],has_prize=False,pet_info=resident_info(g,r),task_last_time=(a['day']+1)*86400-r['timezone_offset_hours']*3600,
        drop_baoxiang_item=daily.spec([5,1001,1,1]),week_reputation=a['reputation'],wander_times=max(0,r['wander_daily']+len(a['tasks'])-a['wander']))


def shop(a,r):
    return dict(result=1,two_type=1,cur_reputation=a['reputation'],total_reputation=a.get('total_reputation',a['reputation']),
        item_list=[dict(item=daily.spec(p),consume_gold=0,buy_reputation=20,total_reputation=r['hunt_shop_unlock'][i-1],left_times=max(0,3+a.get('total_reputation',0)//100-a['shop_bought'].get(str(i),0))) for i,p in enumerate(r['hunt_rewards'],1)])


def settle(role,s,g,op,d,now,r):
    a=prepare(s)
    if op==83:return [u.reply(op,main(a,now,r,g))]
    if op in (84,85):
        u.authorize(role,r,28);idx=u.positive(d,'task_index',3)
        paid=d.get('pay_type')==2
        u.require((a.get('paid_tasks',0)<r['hunt_paid_limit'] if paid else idx not in a['tasks'] and len(a['tasks'])<r['hunt_daily']),'任务已完成或今日次数不足')
        u.require(r['hunt_weekend_open'] or (s['day']+3)%7<5,'周末任务休息，可领取排行奖励')
        typ=d.get('task_type',2 if op==85 else None);u.require(typ in (1,2),'任务类型无效')
        u.require(d.get('pay_type',1) in (1,2),'任务支付方式无效')
        if d.get('pay_type')==2:u.pay(role,'gold_coin',r['hunt_gold'])
        else:u.pay(role,'silver_coin',r['hunt_silver'])
        # [A] APK checks checkDeviceFit/checkPuzzleFit locally before sending
        # task_type=1, pay_type and task_index. No move/answer proof is sent.
        won=True;out=[]
        if typ==2:
            opponents=a.setdefault('task_opponents',{})
            key=str(idx)
            if key not in opponents:
                opponents[key]=choose_enemy(role,s,layer=idx-1,excluded=[m['id'] for m in g['members'].values()])
            result,packets,replay=simulate(role,s,r,journey.load_rules(),28,'仙盟任务守卫',enemy_npc=opponents[key]);won=1<=result<=3
            out.extend(record_events([replay]))
            out.append(u.reply(85,dict(result=1,fight_result_list=[replay],free_times=1,fight_count=1,task_index=idx)))
        prizes=[]
        if won:
            if paid:a['paid_tasks']=a.get('paid_tasks',0)+1
            elif idx not in a['tasks']:a['tasks'].append(idx)
            a['reputation']+=10*idx;a['week_score']=a.get('week_score',0)+10*idx;a['total_reputation']=a.get('total_reputation',0)+10*idx;offline.funds(g,100*idx,r)
            prizes=[journey.grant(role,p[:2]+[p[2]*idx,p[3]]) for p in r['hunt_rewards']]
            from . import pets
            prizes.append(journey.grant(role,[5,1346,pets.load_rules()['task_training_boxes'],1]))
        out.append(u.reply(84,dict(result=1,task_type=typ,task_index=idx,fight_result=won,boss_info=task(r,idx)['boss_info'],prize_reputation=10*idx if won else 0,prize_union_gold=100*idx if won else 0,prize_list=prizes,animal_info=[])))
        return out
    if op==86:
        typ=d.get('two_type');u.require(typ in (1,2),'野外操作无效')
        if typ==2:
            u.require(a['field'] is None,'请先处理当前灵兽');u.require(a['wander']<r['wander_daily']+len(a['tasks']),'今日游历次数已用完');a['wander']+=1
            a['field']=dict(type_id=r['pet_types'][offline.roll(s,len(r['pet_types']))],tries=3)
            return [u.reply(op,dict(result=1,two_type=2,wander_times=r['wander_daily']+len(a['tasks'])-a['wander'],boss_info=dict(type_id=a['field']['type_id']),left_times=3)),u.reply(93,dict(result=1,update_list=[]))]
        return [u.reply(op,dict(result=1,two_type=1,wander_times=r['wander_daily']+len(a['tasks'])-a['wander'],pet_info=resident_info(g,r),wander_broad=a.get('broadcasts',[])))]
    if op==87:
        typ=d.get('two_type');u.require(typ in (1,2),'捕捉操作无效');f=a['field'];u.require(f is not None,'请先游历寻找灵兽')
        if typ==1:
            a['field']=None
            return [u.reply(op,dict(result=1,two_type=1)),broadcast(a,role,f['type_id'],4)]
        u.require(f['tries']>0 and len(a['pets'])<r['pet_limit'],'捕捉次数不足或灵兽已满')
        # [A] The native picker sends the selected catch-prop type, not an
        # arbitrary inventory ID. Never consume a different prop on its behalf.
        selected=d.get('catch_type',r['catch_item'])
        u.require(type(selected)is int and selected in (1338,1339,1340,1341),'捕捉道具无效')
        has_item=any(i['attach_type']==5 and i['type_id']==selected and i['count']>0 and not any(i.get(k) for k in ('owner_id','equip_pos','is_lock')) for i in role['attachments'])
        if has_item:
            from .activity import consume
            consume(role,selected,1)
        else:
            u.require('catch_type' not in d,'捕捉道具不足')
            # Compatibility for old offline scripted requests without a picker.
            u.pay(role,'gold_coin',r['catch_gold'])
        f['tries']-=1
        tid=f['type_id'];caught=offline.roll(s,100)<min(100,r['catch_success_percent']+(r['catch_item_bonus'] if has_item else 0))
        if caught:
            captured=offline.add_pet(a,tid,s,r)
            from .journey import grant
            grant(role,[15,tid,1,captured['quality']])
        flag=1 if caught else 2
        if not caught and not f['tries']:
            resting=offline.roll(s,100)<r['catch_resident_percent']
            if resting:
                population=residents(g,r);population[str(tid)]=population.get(str(tid),0)+1
            flag=3 if resting else 4
        left=f['tries']
        if caught or not left:a['field']=None
        from .guild_instances import catch_update
        return [u.reply(op,dict(result=1,two_type=2,flag=flag,left_times=0 if caught else left,animal_list=[dict(type_id=tid,name='灵兽',flag=flag)])),broadcast(a,role,tid,flag),catch_update(a,role,tid if caught else None,now)]
    if op==91:
        typ=d.get('two_type');u.require(typ in (1,2),'灵兽商店操作无效')
        if typ==1:return [u.reply(op,shop(a,r))]
        idx=u.positive(d,'index',len(r['hunt_rewards']));n=u.positive(d,'buy_count',3)
        u.require(a.get('total_reputation',0)>=r['hunt_shop_unlock'][idx-1],'累计声望尚未解锁商品')
        u.require(a['shop_bought'].get(str(idx),0)+n<=3+a.get('total_reputation',0)//100,'购买次数不足');u.require(a['reputation']>=20*n,'声望不足')
        a['reputation']-=20*n;a['shop_bought'][str(idx)]=a['shop_bought'].get(str(idx),0)+n
        p=list(r['hunt_rewards'][idx-1]);p[2]*=n;journey.grant(role,p)
        return [u.reply(op,dict(result=1,two_type=2,index=idx,cur_reputation=a['reputation'],total_reputation=a.get('total_reputation',0),buy_item=shop(a,r)['item_list'][idx-1]))]
    if op==92:
        typ=d.get('two_type');u.require(type(typ)is int and typ in (1,2),'灵兽排行操作无效');q=d.get('query_type',1);u.require(type(q)is int and q in (1,2),'灵兽排行范围无效')
        score=max(a.get('previous_week_score',0),a.get('week_score',0))
        all_ranks=ranking(role,s,g,score,2)
        my_rank=next(row['order'] for row in all_ranks if row['id']==role['role_id'])
        eligible=(r['hunt_weekend_open'] or weekend(s)) and score>0 and my_rank<=r['hunt_rank_limit'] and not a.get('week_claimed',False)
        if typ==2:
            u.require(r['hunt_weekend_open'] or weekend(s),'灵兽周排行奖励仅周末领取')
            u.require(eligible,'尚未上榜、尚无排行奖励或已领取');a['rank_claimed']=True;a['week_claimed']=True
            prizes=[journey.grant(role,p) for p in r['hunt_rewards']]
            return [u.reply(op,dict(result=1,two_type=2,query_type=q,prize_info=dict(prize_list=prizes,add_reputation=0)))]
        rows=all_ranks if q==2 else ranking(role,s,g,score,1)
        me=next(row for row in rows if row['id']==role['role_id'])
        return [u.reply(op,dict(result=1,two_type=1,query_type=q,my_order_data=me,rank_data=rows[:r['hunt_rank_limit']],can_take_prize=eligible,prize_info=dict(prize_list=[daily.spec(p) for p in r['hunt_rewards']],add_reputation=0)))]
    u.require(False,'灵兽任务操作无效')


def ranking(role,s,g,score,scope):
    rows=[dict(id=role['role_id'],order=0,name=role['role_name'],union_name=g['name'],week_reputation=score)]
    unions=[g] if scope==1 else list(s['unions'].values())
    for union in unions:
        rows.extend(dict(id=m['id'],order=0,name=m['name'],union_name=union['name'],week_reputation=(m['id']%5+1)*10)
                    for m in union['members'].values() if m.get('npc'))
    rows.sort(key=lambda v:(-v['week_reputation'],v['id']))
    for i,row in enumerate(rows,1):row['order']=i
    return rows


def broadcast(a,role,tid,flag):
    row=dict(name=role['role_name'],type_id=tid,flag=flag)
    a['broadcasts']=(a.get('broadcasts',[])+[row])[-30:]
    return u.reply(93,dict(result=1,update_list=[row]))
