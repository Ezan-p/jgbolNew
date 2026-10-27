"""Permanent Caishen worship, persisted daily offers and weekly coin recycling."""
import copy
from datetime import datetime, timedelta, timezone
from secrets import randbelow
from . import activity as a, activity_seasonal as se, formation, summon


def validate(r):
    a.require(r.get('timezone_offset_hours') == 8, '财神刷新使用北京时间')
    a.require(r.get('spring_recycle_coins_per_peach') == 2, '财神钱币回收比例须为2:1')
    a.require(isinstance(r.get('spring_shop_revision'), str) and bool(r['spring_shop_revision']), '财神商店版本缺失')
    pool, weights = r.get('spring_pool'), r.get('spring_pool_weights')
    def valid(p):
        return (isinstance(p, list) and len(p) == 4 and all(type(v) is int for v in p)
                and 0 < p[2] <= 1000000 and p[3] == 1 and
                (p[0] == 5 and p[1] in formation.ITEMS or p[0] == 10 and p[1] in summon.BASES
                 or p[0] == 12 and p[1] == 0))
    a.require(isinstance(pool, list) and len(pool) == 7 and all(valid(p) for p in pool) and
              {tuple(p[:2]) for p in pool} == {(5,t) for t in (1020,1022,1023,1001,1034,1033)} | {(12,0)}, '财神道具池无效')
    a.require(isinstance(weights, list) and len(weights) == len(pool) and
              all(type(w) is int and 0 < w <= 10000 for w in weights), '财神道具权重无效')
    coins = r.get('spring_coin_pool')
    a.require(isinstance(coins,list) and len(coins)==3 and all(isinstance(x,dict) for x in coins), '财神钱币池无效')
    a.require([x.get('count') for x in coins] == [100,200,300] and
              all(type(x.get('weight')) is int for x in coins) and
              10000 >= coins[0]['weight'] > coins[1]['weight'] > coins[2]['weight'] > 0, '钱币概率须随数量递减')
    shop = r.get('spring_shop')
    a.require(isinstance(shop,list) and len(shop)==13 and all(isinstance(x,dict) for x in shop), '财神商店池无效')
    for row in shop:
        a.require(valid(row.get('reward')) and row.get('tier') in ('low','high'), '财神商品无效')
        a.require(type(row.get('cost')) is int and 0 < row['cost'] <= 1000000 and
                  type(row.get('limit')) is int and row['limit']==1, '财神商品须每日限兑一次')
    low = [x for x in shop if x['tier']=='low']
    high = [x for x in shop if x['tier']=='high']
    a.require([x['reward'][1] for x in low]==[1022,1023,1041,1033,1006,1042,1007,1032] and
              all(x['reward'][0]==5 and x['reward'][2]==1 for x in low), '财神低级池须按贵重程度排列')
    a.require(all(x['cost'] < y['cost'] for x,y in zip(low,low[1:])) and low[-1]['cost']==50, '低级价格须递增且金丝定价50')
    a.require({tuple(x['reward'][:2]) for x in high}=={(10,5044),(5,1031),(5,6002),(5,6003),(5,6004)}, '财神高级池不完整')
    for row in high:
        vip = row['reward'][1] == 1031
        a.require(row['cost']==(100 if vip else 200) and row['reward'][2]==(1 if vip else 5), '财神高级价格或数量不符')


def draw(values, weights):
    ticket = randbelow(sum(weights))
    for value, weight in zip(values, weights):
        if ticket < weight:return copy.deepcopy(value)
        ticket -= weight
    raise AssertionError('Invalid weighted pool')


def is_open(r):return r['seasonal_games']['spring_money']['enabled']


def rollover(role, now, r):
    role.setdefault('activity', {})
    s=se.state(role).setdefault('spring',dict(day=-1,last_visit_time=0,purchases={},cards_given=[]))
    s.setdefault('cards_given', [])
    # Older saves have a calendar day and last visit but no weekly marker.
    visit_day=a.day(s['last_visit_time'],r) if s.get('last_visit_time') else -1
    today=max(a.day(now,r),s['day'],visit_day,s.get('observed_day',-1))
    s['observed_day']=today
    week=(today+3)//7
    previous=s.get('week',(max(s['day'],visit_day)+3)//7 if max(s['day'],visit_day)>=0 else week)
    if week>previous:
        coins=sum(i['count'] for i in role['attachments'] if i['attach_type']==5 and i['type_id']==1028)
        if coins:
            from . import system_mail, welfare
            rate=r['spring_recycle_coins_per_peach']
            peaches=(coins+rate-1)//rate  # An odd tail coin gets one courtesy peach.
            start=(previous*7-3)*86400-8*3600
            date=datetime.fromtimestamp(start,timezone(timedelta(hours=8))).strftime('%Y-%m-%d')
            delivery=copy.deepcopy(role)
            _,mail=system_mail.deliver(delivery,key=f'caishen-recycle-{previous}',
                title='财神贺岁周刷新·钱币返还',
                body=f'财神贺岁常驻开放，每周一北京时间0点刷新。{date}开始的活动周已结束，'
                     f'剩余上古钱币{coins}枚已全部回收，按2枚钱币兑换1个蟠桃，'
                     f'共返还蟠桃{peaches}个。奇数尾币不足2枚时补足1个蟠桃。'
                     '请领取邮件附件；上古钱币不保留到新一周，已获得的其它奖励保留。',
                prizes=[[5,1001,peaches,1]],now=now,rules=welfare.load_rules())
            role['welfare']=delivery['welfare']
            role['attachments']=[i for i in role['attachments'] if not (i['attach_type']==5 and i['type_id']==1028)]
            s['last_recycle']=dict(week=previous,coins=coins,peaches=peaches,mail_id=mail['mail_id'])
    if week>s.get('week',-1):
        s.update(week=week,weekly_visits=0,weekly_coins=0,weekly_exchanges=0)
    s.setdefault('last_visit_day',visit_day)
    return s


def state(role,now,r):
    s=rollover(role,now,r)
    today=s['observed_day']
    if today>s['day'] or 'shop' not in s:
        # Preserve relevant purchases from the old fixed shop on same-day upgrade.
        legacy={str(t):s['purchases'].get(str(i),0) for i,t in ((2,1023),(4,1006),(5,1007))}
        purchases=legacy if today==s['day'] and 'shop' not in s else {}
        low=[x for x in r['spring_shop'] if x['tier']=='low']
        high=[x for x in r['spring_shop'] if x['tier']=='high']
        selected=[]
        for _ in range(4):selected.append(low.pop(randbelow(len(low))))
        selected.append(high[randbelow(len(high))])
        s.update(day=today,purchases=purchases,shop=copy.deepcopy(selected))
    if s.get('shop_revision')!=r['spring_shop_revision']:
        configured={x['reward'][1]:x for x in r['spring_shop']}
        s['shop']=[copy.deepcopy(configured[x['reward'][1]]) for x in s['shop']]
        s['shop_revision']=r['spring_shop_revision']
    return s


def offer_id(s,row,r):
    # Original protocol uses uint32; embedding the day rejects an old screen even
    # after another query/heartbeat has already advanced the saved shop.
    return s['day']*100+next(i for i,x in enumerate(r['spring_shop'],1) if x['reward'][1]==row['reward'][1])


def payload(s,r):
    start=(s['week']*7-3)*86400-8*3600
    goods=[dict(a.prize_spec(x['reward']),prize_id=offer_id(s,x,r),qianbi_count=x['cost'],
                count=max(0,1-s['purchases'].get(str(x['reward'][1]),0)),tier=x['tier']) for x in s['shop']]
    return dict(start_time=start-1,end_time=start+7*86400,local_permanent=True,local_enabled=is_open(r),
                last_visit_time=s['last_visit_time'],visited_today=s['last_visit_day']>=s['day'],
                prize_list=goods,shop_day=s['day'],shop_revision=s['shop_revision'],week=s['week'],
                next_daily_refresh=(s['day']+1)*86400-8*3600,next_weekly_refresh=start+7*86400,
                weekly_visits=s['weekly_visits'],weekly_coins=s['weekly_coins'],weekly_exchanges=s['weekly_exchanges'],
                coin_pool=copy.deepcopy(r['spring_coin_pool']),recycle_coins_per_peach=2,
                random_get_item=[dict(a.prize_spec(p),probability=w/sum(r['spring_pool_weights']))
                                 for p,w in zip(r['spring_pool'],r['spring_pool_weights'])])


def settle(role,mid,req,now,r):
    a.require(is_open(r),'财神贺岁尚未开放')
    s=state(role,now,r)
    if mid==1210:
        a.require(type(req['flag']) is int and req['flag']==1,'拜财神操作无效')
        a.require(s['last_visit_day']<s['day'],'今日已经拜访财神')
        coins=draw([x['count'] for x in r['spring_coin_pool']],[x['weight'] for x in r['spring_coin_pool']])
        item=draw(r['spring_pool'],r['spring_pool_weights'])
        s.update(last_visit_time=now,last_visit_day=s['day'])
        s['weekly_visits']+=1;s['weekly_coins']+=coins
        return [summon.event(88,dict(last_visit_time=now,prize_list=a.prizes(role,[[5,1028,coins,1],item]),local_caishen=payload(s,r)))]
    idx,n=req['prize_id'],req['count']
    a.require(type(idx) is int and type(n) is int and n==1,'财神商品每种每日仅可兑换一次')
    row=next((x for x in s['shop'] if offer_id(s,x,r)==idx),None)
    a.require(row is not None,'财神商店已刷新或商品未上架，请重新打开商店')
    key=str(row['reward'][1]);a.require(s['purchases'].get(key,0)<1,'今日兑换次数不足')
    a.consume(role,1028,row['cost'])
    s['purchases'][key]=1;s['weekly_exchanges']+=1
    prize=a.prizes(role,[row['reward']])[0]
    prize['local_caishen']=payload(s,r)
    return [summon.event(87,prize)]
