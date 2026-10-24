"""East Sea fishing: original request/response contract, configured economy [B]."""
import copy
import secrets
from . import activity as a, summon
from . import activity_seasonal as se


def state(role,now,r):
    s=se.state(role).setdefault('fish',dict(day=-1,purchases={},news=[],gift_day=-1))
    if s['day']!=a.day(now,r):s.update(day=a.day(now,r),purchases={})
    return s


def status(role,now,r):
    s=state(role,now,r);cfg=r['seasonal_games']['fish']
    if se.is_open(r,'fish',now) and s['gift_day']!=a.day(now,r):
        a.prizes(role,[[5,1026,r['fish_daily_nets'],1]]);s['gift_day']=a.day(now,r)
    goods=[dict(a.prize_spec(row['reward']),type_id=row['reward'][1],cost_fish_count=row['cost'],
        count=row['limit']-s['purchases'].get(str(row['reward'][1]),0)) for row in r['fish_shop']]
    return dict(search_gold_data=dict(begin_time=cfg['start_time'] if cfg['enabled'] else 0,
        end_time=cfg['end_time'] if cfg['enabled'] else 0,exchange_data=goods,
        cost_gold_count=r['fish_gold_per_net'],random_get_item=[a.prize_spec(p) for p in r['fish_pool']],broad_data=copy.deepcopy(s['news'])))


def settle(role,req,now,r):
    a.require(se.is_open(r,'fish',now),'东海寻宝尚未开放或已经结束')
    s=state(role,now,r);tid,n=req['type_id'],req['count']
    a.require(type(n)is int and 1<=n<=100,'捕鱼或兑换数量无效')
    if tid==0:
        a.require(n in (1,10),'捕鱼仅支持单次或十连')
        nets=sum(i['count'] for i in role['attachments'] if i['attach_type']==5 and i['type_id']==1026 and not i.get('is_lock') and not i.get('owner_id') and not i.get('equip_pos'))
        # The ten-draw button checks the full gold cost even when nets exist.
        if n==1 and nets:a.consume(role,1026,1)
        else:a.spend(role,'gold_coin',r['fish_gold_per_net']*n)
        rewards=[]
        for _ in range(n):
            rewards.append([5,1027,r['fish_per_catch'],1])
            rewards.append(copy.deepcopy(secrets.choice(r['fish_pool'])))
        return [summon.event(85,dict(result=1,item_list=a.prizes(role,rewards)))]
    row=next((x for x in r['fish_shop'] if x['reward'][1]==tid),None)
    a.require(row is not None,'不存在此东海兑换物品')
    used=s['purchases'].get(str(tid),0);a.require(used+n<=row['limit'],'今日东海兑换次数不足')
    a.consume(role,1027,row['cost']*n);p=copy.deepcopy(row['reward']);p[2]*=n
    s['purchases'][str(tid)]=used+n
    news=dict(name=role['role_name'],object_type=p[0],type_id=tid)
    s['news'].append(news);s['news']=s['news'][-3:]
    return [summon.event(85,dict(result=1,count=n,item_data=a.prizes(role,[p]))),summon.event(86,[news])]
