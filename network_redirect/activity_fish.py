"""Permanent East Sea fishing; offline daily shop and Monday weekly progress."""
import copy
from datetime import datetime, timezone, timedelta
from secrets import randbelow
from . import activity as a, summon, formation
from . import activity_seasonal as se


def validate(r):
    a.require(r.get('timezone_offset_hours') == 8, '东海刷新使用北京时间')
    for key, minimum in (('fish_daily_nets', 0), ('fish_gold_per_net', 1), ('fish_recycle_peaches_per_koi', 1)):
        a.require(type(r.get(key)) is int and minimum <= r[key] <= 1000, '东海价格或赠网配置无效')
    pool, weights = r.get('fish_pool'), r.get('fish_pool_weights')
    a.require(isinstance(pool, list) and len(pool) == 8, '东海道具池须含八种奖励')
    a.require(isinstance(weights, list) and len(weights) == len(pool) and
              all(type(w) is int and 0 < w <= 10000 for w in weights), '东海概率权重无效')
    def valid(p):
        return (isinstance(p, list) and len(p) == 4 and all(type(v) is int for v in p)
                and 0 < p[2] <= 1000000 and p[3] == 1 and
                (p[0] == 5 and p[1] in formation.ITEMS or p[0] == 10 and p[1] in summon.BASES
                 or p[0] == 12 and p[1] == 0))
    a.require(all(valid(p) for p in pool) and {(p[0],p[1]) for p in pool} ==
              {(5,t) for t in (1020,1022,1023,1001,1006,1034,1033)} | {(12,0)}, '东海道具奖励无效')
    koi = r.get('fish_koi_pool')
    a.require(isinstance(koi,list) and len(koi)==3 and all(isinstance(x,dict) for x in koi), '锦鲤池无效')
    a.require([x.get('count') for x in koi] == [2,3,5] and all(type(x.get('weight')) is int for x in koi)
              and 10000 >= koi[0]['weight'] > koi[1]['weight'] > koi[2]['weight'] > 0, '锦鲤概率须随数量递减')
    a.require(isinstance(r.get('fish_shop_revision'),str) and bool(r['fish_shop_revision']), '东海商店版本缺失')
    shop = r.get('fish_shop')
    a.require(isinstance(shop,list) and len(shop)==12 and all(isinstance(x,dict) for x in shop), '东海商店池无效')
    for row in shop:
        a.require(valid(row.get('reward')) and row.get('tier') in ('low','high'), '东海商品无效')
        a.require(type(row.get('cost')) is int and 0 < row['cost'] <= 1000000 and
                  type(row.get('limit')) is int and 0 < row['limit'] <= 100, '东海商品价格或限购无效')
        if row['tier']=='high':a.require(row['reward'][2]==5 and row['limit']==1, '高级商品固定五个、每日限兑一次')
    a.require(len({x['reward'][1] for x in shop})==12, '东海商品编号不得重复')
    a.require({tuple(x['reward'][:2]) for x in shop if x['tier']=='low'} ==
              {(5,t) for t in (1007,1343,1024,1042,1032,1031)}, '低级兑换池不完整')
    a.require({tuple(x['reward'][:2]) for x in shop if x['tier']=='high'} ==
              {(10,t) for t in (5039,5041,5032)} | {(5,t) for t in (6002,6003,6004)}, '高级兑换池不完整')


def draw(values, weights):
    ticket = randbelow(sum(weights))
    for value, weight in zip(values, weights):
        if ticket < weight:return copy.deepcopy(value)
        ticket -= weight
    raise AssertionError('Invalid weighted pool')


def is_open(r):
    # The seasonal time window no longer expires this permanent activity.
    return r['seasonal_games']['fish']['enabled']


def rollover(role, now, r):
    """Recycle expired koi once, including locked stacks, before new-week actions."""
    role.setdefault('activity', {})
    s = se.state(role).setdefault('fish', dict(day=-1, purchases={}, news=[], gift_day=-1))
    today = max(a.day(now,r), s['day'])
    week = (today + 3) // 7
    previous = s.get('week', (s['day']+3)//7 if s['day'] >= 0 else week)
    if week > previous:
        koi = sum(i['count'] for i in role['attachments'] if i['attach_type']==5 and i['type_id']==1027)
        if koi:
            from . import system_mail, welfare
            rate = r['fish_recycle_peaches_per_koi']
            peaches = koi * rate
            start = (previous*7-3)*86400-r['timezone_offset_hours']*3600
            date = datetime.fromtimestamp(start, timezone(timedelta(hours=8))).strftime('%Y-%m-%d')
            delivery = copy.deepcopy(role)
            _, mail = system_mail.deliver(delivery, key=f'fish-recycle-{previous}',
                title='东海寻宝周刷新·锦鲤返还',
                body=f'东海寻宝每周一北京时间0点刷新。{date}开始的活动周已结束，'
                     f'剩余锦鲤{koi}条已全部回收，按1条锦鲤兑换{rate}个蟠桃，'
                     f'共返还蟠桃{peaches}个，请领取邮件附件。锦鲤不结转至新一周；'
                     '仙网及此前已获得的其它奖励保留。',
                prizes=[[5,1001,peaches,1]], now=now, rules=welfare.load_rules())
            role['welfare'] = delivery['welfare']
            role['attachments'] = [i for i in role['attachments'] if not (i['attach_type']==5 and i['type_id']==1027)]
            s['last_recycle'] = dict(week=previous,koi=koi,peaches=peaches,mail_id=mail['mail_id'])
    if week > s.get('week', -1):
        s.update(week=week, weekly_casts=0, weekly_koi=0, weekly_exchanges=0, news=[])
    return s


def state(role, now, r):
    s = rollover(role, now, r)
    today = max(a.day(now,r), s['day'])  # Clock rollback cannot reopen old quotas.
    if today > s['day'] or 'shop' not in s:
        low = [x for x in r['fish_shop'] if x['tier']=='low']
        high = [x for x in r['fish_shop'] if x['tier']=='high']
        selected=[]
        for _ in range(4):selected.append(low.pop(randbelow(len(low))))
        selected.append(high[randbelow(len(high))])
        s.update(day=today, purchases={}, shop=copy.deepcopy(selected))
    if s.get('shop_revision') != r['fish_shop_revision']:
        # Update offers in place: retain today's selection and already-used quotas.
        configured = {x['reward'][1]: x for x in r['fish_shop']}
        s['shop'] = [copy.deepcopy(configured[x['reward'][1]]) for x in s['shop']]
        s['shop_revision'] = r['fish_shop_revision']
    return s


def payload(s, r):
    goods = [dict(a.prize_spec(x['reward']), type_id=x['reward'][1], cost_fish_count=x['cost'],
                  count=max(0,x['limit']-s['purchases'].get(str(x['reward'][1]),0)), tier=x['tier']) for x in s['shop']]
    offset=r['timezone_offset_hours']*3600
    week_start=(s['week']*7-3)*86400-offset
    preview=[dict(a.prize_spec(p), probability=w/sum(r['fish_pool_weights']))
             for p,w in zip(r['fish_pool'],r['fish_pool_weights'])]
    return dict(begin_time=week_start-1, end_time=week_start+7*86400,
                local_permanent=True, local_enabled=is_open(r),
                next_daily_refresh=(s['day']+1)*86400-offset, next_weekly_refresh=week_start+7*86400,
                shop_day=s['day'], shop_revision=s['shop_revision'], week=s['week'], weekly_casts=s['weekly_casts'],
                weekly_koi=s['weekly_koi'], weekly_exchanges=s['weekly_exchanges'],
                exchange_data=goods, cost_gold_count=r['fish_gold_per_net'], random_get_item=preview,
                recycle_peaches_per_koi=r['fish_recycle_peaches_per_koi'],
                koi_pool=copy.deepcopy(r['fish_koi_pool']), broad_data=copy.deepcopy(s['news']))


def status(role, now, r):
    from . import feature_levels
    s=state(role,now,r)
    if (is_open(r) and role.get('level', 1) >= feature_levels.LEVELS['fishrush']
            and s['gift_day'] < s['day']):
        if r['fish_daily_nets']:a.prizes(role,[[5,1026,r['fish_daily_nets'],1]])
        s['gift_day']=s['day']
    return dict(search_gold_data=payload(s,r))


def settle(role, req, now, r):
    a.require(is_open(r), '东海寻宝尚未开放')
    tid,n=req['type_id'],req['count']
    a.require(type(tid) is int and type(n) is int and 1<=n<=100, '捕鱼或兑换数量无效')
    old_day=se.state(role).get('fish',{}).get('day',-1)
    s=state(role,now,r)
    if tid==0:
        a.require(n in (1,10), '捕鱼仅支持单次或十连')
        nets=sum(i['count'] for i in role['attachments'] if i['attach_type']==5 and i['type_id']==1026
                 and not i.get('is_lock') and not i.get('owner_id') and not i.get('equip_pos'))
        if n==1 and nets:a.consume(role,1026,1)
        else:a.spend(role,'gold_coin',r['fish_gold_per_net']*n)
        rewards=[]
        for _ in range(n):
            koi=draw([x['count'] for x in r['fish_koi_pool']], [x['weight'] for x in r['fish_koi_pool']])
            rewards.extend([[5,1027,koi,1], draw(r['fish_pool'],r['fish_pool_weights'])])
            s['weekly_koi']+=koi
        s['weekly_casts']+=n
        return [summon.event(85,dict(result=1,item_list=a.prizes(role,rewards),local_fish=payload(s,r)))]
    a.require(old_day==s['day'], '东海商店已刷新，请重新打开商店后兑换')
    row=next((x for x in s['shop'] if x['reward'][1]==tid),None)
    a.require(row is not None, '此物品今日未上架')
    used=s['purchases'].get(str(tid),0)
    a.require(used+n<=row['limit'], '今日东海兑换次数不足')
    a.consume(role,1027,row['cost']*n)
    p=copy.deepcopy(row['reward']);p[2]*=n
    s['purchases'][str(tid)]=used+n;s['weekly_exchanges']+=n
    news=dict(name=role['role_name'],object_type=p[0],type_id=tid)
    s['news'].append(news);s['news']=s['news'][-3:]
    return [summon.event(85,dict(result=1,count=n,item_data=a.prizes(role,[p]),local_fish=payload(s,r))),
            summon.event(86,[news])]
