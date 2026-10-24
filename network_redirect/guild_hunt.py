"""Guild beast quests and wilderness: persistent inferred local progression."""
from . import guild as u,daily,journey
from .guild_instances import state
from .guild_combat import simulate


def prepare(s):
    a=state(s)
    for k,v in dict(tasks=[],wander=0,field=None,shop_bought={},rank_claimed=False).items():a.setdefault(k,v)
    return a


def task(r,index):
    reward=dict(add_reputation=10,prize_list=[daily.spec(p) for p in r['hunt_rewards']])
    return dict(task_info={1:[101],2:[201],3:[]},prize_info=[reward,reward],boss_info=dict(cur_hp=10000,max_hp=10000,cost_gold=10,fight_count=0),index=index)


def main(a,now,r):
    return dict(result=1,free_task_times=max(0,r['hunt_daily']-len(a['tasks'])),pay_task_times=0,pay_task_gold=10,
        union_task=[task(r,i) for i in range(1,4)],has_prize=False,pet_info={1:len(a['pets']),2:0,3:0},task_last_time=now+3600,
        drop_baoxiang_item=daily.spec([5,1001,1,1]),week_reputation=a['reputation'],wander_times=max(0,r['wander_daily']-a['wander']))


def shop(a,r):
    return dict(result=1,two_type=1,cur_reputation=a['reputation'],total_reputation=a.get('total_reputation',a['reputation']),
        item_list=[dict(item=daily.spec(p),consume_gold=0,buy_reputation=20,total_reputation=0,left_times=max(0,3-a['shop_bought'].get(str(i),0))) for i,p in enumerate(r['hunt_rewards'],1)])


def settle(role,s,g,op,d,now,r):
    a=prepare(s)
    if op==83:return [u.reply(op,main(a,now,r))]
    if op in (84,85):
        u.authorize(role,r,28);idx=u.positive(d,'task_index',3)
        u.require(idx not in a['tasks'] and len(a['tasks'])<r['hunt_daily'],'任务已完成或今日次数不足')
        typ=d.get('task_type',2 if op==85 else None);u.require(typ in (1,2),'任务类型无效')
        u.require(d.get('pay_type',1) in (1,2),'任务支付方式无效')
        if d.get('pay_type')==2:u.pay(role,'gold_coin',r['hunt_gold'])
        else:u.pay(role,'silver_coin',r['hunt_silver'])
        won=True;out=[]
        if typ==2:
            result,packets,replay=simulate(role,s,r,journey.load_rules(),28,'仙盟任务守卫');won=1<=result<=3
            out.append(u.reply(85,dict(result=1,fight_result_list=[replay],free_times=1,fight_count=1,task_index=idx)))
        prizes=[]
        if won:
            a['tasks'].append(idx);a['reputation']+=10;a['total_reputation']=a.get('total_reputation',0)+10;g['money']+=100
            prizes=[journey.grant(role,p) for p in r['hunt_rewards']]
        out.append(u.reply(84,dict(result=1,task_type=typ,task_index=idx,fight_result=won,boss_info=task(r,idx)['boss_info'],prize_reputation=10 if won else 0,prize_union_gold=100 if won else 0,prize_list=prizes,animal_info=[])))
        return out
    if op==86:
        typ=d.get('two_type');u.require(typ in (1,2),'野外操作无效')
        if typ==2:
            u.require(a['wander']<r['wander_daily'],'今日游历次数已用完');a['wander']+=1
            a['field']=dict(type_id=101+(a['wander']-1)%6,tries=3)
            return [u.reply(op,dict(result=1,two_type=2,wander_times=r['wander_daily']-a['wander'],boss_info=dict(type_id=a['field']['type_id']),left_times=3))]
        return [u.reply(op,dict(result=1,two_type=1,wander_times=r['wander_daily']-a['wander'],pet_info={1:len(a['pets']),2:0,3:0},wander_broad=[]))]
    if op==87:
        typ=d.get('two_type');u.require(typ in (1,2),'捕捉操作无效');f=a['field'];u.require(f is not None,'请先游历寻找灵兽')
        if typ==1:return [u.reply(op,dict(result=1,two_type=1,boss_info=dict(type_id=f['type_id']),left_times=f['tries']))]
        u.require(f['tries']>0 and len(a['pets'])<240,'捕捉次数不足或灵兽已满');u.pay(role,'gold_coin',r['catch_gold']);f['tries']-=1
        tid=f['type_id'];a['pets'].append(tid);a['field']=None
        return [u.reply(op,dict(result=1,two_type=2,flag=1,left_times=0,animal_list=[dict(type_id=tid,name='灵兽',flag=1)]))]
    if op==91:
        typ=d.get('two_type');u.require(typ in (1,2),'灵兽商店操作无效')
        if typ==1:return [u.reply(op,shop(a,r))]
        idx=u.positive(d,'index',len(r['hunt_rewards']));n=u.positive(d,'buy_count',3)
        u.require(a['shop_bought'].get(str(idx),0)+n<=3,'购买次数不足');u.require(a['reputation']>=20*n,'声望不足')
        a['reputation']-=20*n;a['shop_bought'][str(idx)]=a['shop_bought'].get(str(idx),0)+n
        p=list(r['hunt_rewards'][idx-1]);p[2]*=n;journey.grant(role,p)
        return [u.reply(op,dict(result=1,two_type=2,index=idx,cur_reputation=a['reputation'],total_reputation=a.get('total_reputation',0),buy_item=shop(a,r)['item_list'][idx-1]))]
    if op==92:
        typ=d.get('two_type');u.require(typ in (1,2),'灵兽排行操作无效');q=d.get('query_type',1)
        if typ==2:
            u.require(a.get('total_reputation',0)>0 and not a['rank_claimed'],'尚无排行奖励或已领取');a['rank_claimed']=True
            prizes=[journey.grant(role,p) for p in r['hunt_rewards']]
            return [u.reply(op,dict(result=1,two_type=2,query_type=q,prize_info=dict(prize_list=prizes,add_reputation=0)))]
        me=dict(order=1,name=role['role_name'],union_name=g['name'],week_reputation=a.get('total_reputation',0))
        return [u.reply(op,dict(result=1,two_type=1,query_type=q,my_order_data=me,rank_data=[me],can_take_prize=a.get('total_reputation',0)>0 and not a['rank_claimed'],prize_info=dict(prize_list=[daily.spec(p) for p in r['hunt_rewards']],add_reputation=0)))]
    u.require(False,'灵兽任务操作无效')
