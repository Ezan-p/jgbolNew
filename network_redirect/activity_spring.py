"""Spring fortune worship/exchange and original four-character card recipes."""
import copy
from . import activity as a, formation, summon
from . import activity_seasonal as se

COMBINATIONS=[[1,2,3,4],[1,2,5,6],[3,4,3,7],[4,8,9,10]]


def state(role,now,r):
    s=se.state(role).setdefault('spring',dict(day=-1,last_visit_time=0,purchases={},cards_given=[]))
    if s['day']!=a.day(now,r):s.update(day=a.day(now,r),purchases={})
    return s


def card(role,level):
    role['attachments'].append(dict(id=formation.new_id(role),attach_type=5,type_id=1094,level=level,count=1,
        equip_order=0,equip_pos=0,is_lock=0))


def status(role,now,r):
    s=state(role,now,r);money=r['seasonal_games']['spring_money'];cards=r['seasonal_games']['spring_cards']
    season=cards['start_time']
    if se.is_open(r,'spring_cards',now) and season not in s['cards_given']:
        for row in COMBINATIONS:
            for level in row:card(role,level)
        s['cards_given'].append(season)
    goods=[]
    for i,row in enumerate(r['spring_shop'],1):
        goods.append(dict(a.prize_spec(row['reward']),prize_id=i,qianbi_count=row['cost'],count=row['limit']-s['purchases'].get(str(i),0)))
    return dict(visit_caishen=dict(start_time=money['start_time'] if money['enabled'] else 0,
        end_time=money['end_time'] if money['enabled'] else 0,last_visit_time=s['last_visit_time'],prize_list=goods),
        tangwang_info=dict(start_time=cards['start_time'] if cards['enabled'] else 0,
        end_time=cards['end_time'] if cards['enabled'] else 0,card_combination=COMBINATIONS))


def settle(role,mid,req,now,r):
    name='spring_cards' if mid==1213 else 'spring_money'
    a.require(se.is_open(r,name,now),'春节活动尚未开放或已经结束');s=state(role,now,r)
    if mid==1210:
        a.require(req['flag']==1,'拜财神操作无效')
        a.require(not s['last_visit_time'] or a.day(s['last_visit_time'],r)!=a.day(now,r),'今日已经拜访财神')
        s['last_visit_time']=now
        return [summon.event(88,dict(last_visit_time=now,prize_list=a.prizes(role,[[5,1028,r['spring_daily_coins'],1]])))]
    if mid==1211:
        idx,n=req['prize_id'],req['count']
        a.require(type(idx)is int and 1<=idx<=len(r['spring_shop']) and type(n)is int and 1<=n<=100,'财神兑换参数无效')
        row=r['spring_shop'][idx-1];used=s['purchases'].get(str(idx),0)
        a.require(used+n<=row['limit'],'今日兑换数量不足');a.consume(role,1028,row['cost']*n)
        p=copy.deepcopy(row['reward']);p[2]*=n;s['purchases'][str(idx)]=used+n
        return [summon.event(87,a.prizes(role,[p])[0])]
    ids=[x['id'] for x in req['card_list']]
    a.require(req['count']==len(ids)==4 and len(set(ids))==4,'请选择四张不同的字牌')
    cards=[formation.lookup(role,'attachments',i) for i in ids]
    a.require(all(c['attach_type']==5 and c['type_id']==1094 and c['count']>0 and not c.get('is_lock') for c in cards),'字牌无效或已锁定')
    letters=[c['level'] for c in cards];a.require(letters in COMBINATIONS,'字牌顺序不符合原版组合')
    for c in cards:
        c['count']-=1
        if not c['count']:role['attachments'].remove(c)
    reward=r['spring_card_rewards'][COMBINATIONS.index(letters)]
    return [summon.event(90,dict(prize_list=a.prizes(role,[reward])))]
