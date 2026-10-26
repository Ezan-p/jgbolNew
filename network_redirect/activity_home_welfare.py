"""Original 1348/24 UI shapes; permanent goals and local weekly competition [B]."""
import copy
import json
from functools import lru_cache
from . import activity as a, activity_home as h, activity_home_friends as friends


@lru_cache(maxsize=1)
def rules():
    r = json.loads((a.ROOT/'server_config/home_rules.json').read_text())
    a.require(r['schema_version']==1 and r['mode']=='inferred', '洞府福利配置版本无效')
    for key, maximum in (('target_build_levels',20),('target_train_levels',40)):
        v=r[key]
        a.require(isinstance(v,list) and v==sorted(set(v)) and all(type(n)is int and 1<=n<=maximum for n in v), '洞府目标配置无效')
    for key, width, count in (('plan',2,3),('community',3,4)):
        a.require(len(r[key])==count and all(len(row)==width and all(type(n)is int and 0<n<=100000 for n in row) for row in r[key]), '洞府福利阶梯无效')
        a.require([row[0] for row in r[key]]==sorted(set(row[0] for row in r[key])), '洞府福利阶梯重复或乱序')
    a.require(len(r['race_gold'])==11 and all(type(n)is int and 0<n<=10000 for n in r['race_gold']), '洞府排名奖励无效')
    a.require(all(type(r[k])is int and 0<r[k]<=10000 for k in ('target_coins_per_level','race_npc_daily_exp')), '洞府奖励数值无效')
    return r


def week(now,r):
    return (a.day(now,r)+3)//7  # 1970-01-01 was Thursday; week starts Monday.


def rank(role,s,now,r,final=False):
    cfg=rules(); w=s['welfare']; start=(w['week']*7-3)*86400-r['timezone_offset_hours']*3600
    elapsed=604800 if final else max(0,min(604800,now-start))
    rows=[]
    for e in friends.roster(role,s):
        p=e['profile']
        daily=cfg['race_npc_daily_exp']+(p['level']-50)*20+p['role_id']%5*100
        rows.append(dict(id=p['role_id'], name=p['role_name'], exp=daily*elapsed//86400, is_npc=True))
    rows.append(dict(id=role['role_id'],name=role['role_name'],exp=w['race_exp'],is_npc=False))
    rows.sort(key=lambda row:(-row['exp'],row['id']))
    for i,row in enumerate(rows,1):
        row.update(order=i,prize_list=[a.prize_spec([11,0,cfg['race_gold'][i-1],1])])
    return rows


def prepare(role,s,now,r):
    current=week(now,r)
    w=s.setdefault('welfare',dict(week=current,race_exp=0,claims=[],plan_claimed=0))
    friends.roster(role,s)
    if current>w['week']:
        if w['race_exp']>0:
            board=rank(role,s,now,r,final=True)
            place=next(row['order'] for row in board if not row['is_npc'])
            from . import system_mail, welfare
            delivery=copy.deepcopy(role)
            system_mail.deliver(delivery, f"home-race-{w['week']}", '洞府修炼周榜奖励',
                f"本地修炼竞赛已结束，你获得第{place}名，累计修炼经验{w['race_exp']}。对手均为离线NPC。",
                [[11,0,rules()['race_gold'][place-1],1]], now, welfare.load_rules())
            role['welfare']=delivery['welfare']
            w['last_race']=dict(week=w['week'],order=place,exp=w['race_exp'])
        w.update(week=current,race_exp=0)
    return s


def status(w,key,ready):
    return 3 if key in w['claims'] else 2 if ready else 1


def goals(s):
    cfg=rules(); w=s['welfare']; out={1:dict(target_list={}),2:dict(target_list={})}
    for main,types,levels in ((1,range(1,5),cfg['target_train_levels']), (2,h.KEYS,cfg['target_build_levels'])):
        rows=out[main]['target_list']
        for typ in types:
            for lv in levels:
                i=len(rows)+1; key=f'target:{main}:{i}'
                current=s['train'][str(typ)]['level'] if main==1 else s['build'][str(typ)]
                name=({1:'攻击',2:'防御',3:'法伤',4:'法抗'} if main==1 else {1:'主殿',2:'药园',3:'佛堂',4:'修炼房',5:'灵兽殿'})[typ]
                rows[i]=dict(target=typ,need_level=lv,target_desc=f'{name}{"修炼" if main==1 else ""}达到{lv}级',
                    status=status(w,key,current>=lv),prize_list=[a.prize_spec([5,1361,lv*cfg['target_coins_per_level'],1])])
    return out


def community(role,s):
    w=s['welfare']; points=[h.point(friends.layout(e)) for e in friends.roster(role,s)]+[h.point(s)]
    data,build={},{}
    for i,(point,count,coins) in enumerate(rules()['community']):
        cur=sum(p>=point for p in points)
        data[i]=dict(point=point,status=status(w,f'community:{i}',cur>=count and h.point(s)>=point),
                     prize_list=[a.prize_spec([5,1361,coins,1])])
        build[i]=dict(cur_count=min(cur,count),min_count=count)
    return dict(act_data=data,build_info=build)


def plan(s):
    w=s['welfare']; eligible=sum(gold for point,gold in rules()['plan'] if h.point(s)>=point)
    return dict(hole_point=h.point(s),total_gold=max(0,eligible-w['plan_claimed']),
                can_take=2 if eligible>w['plan_claimed'] else 3 if w['plan_claimed'] else 1,
                hole_grow_plan_prize=[dict(point=p,prize_gold=g) for p,g in rules()['plan']])


def view(role,s,now,r):
    board=rank(role,s,now,r)
    end=(s['welfare']['week']*7+4)*86400-r['timezone_offset_hours']*3600
    return {72:goals(s),69:plan(s),70:community(role,s),68:dict(
        role_order=next(row['order'] for row in board if not row['is_npc']),role_exp=s['welfare']['race_exp'],
        rank_data=board,end_time=end)}


def settle(role,s,d,now,r):
    flag=d.get('flag',1)
    a.require(type(flag)is int and flag in (1,2),'洞府福利操作无效')
    if flag==1:
        return [h.response(24,dict(flag=1,all_activity=view(role,s,now,r)))]
    typ=d.get('act_type'); w=s['welfare']; key=None; extra={}
    a.require(type(typ)is int and typ in (69,70,72),'修炼周榜在周一结算后通过邮件发奖')
    if typ==69:
        amount=plan(s)['total_gold']; a.require(amount>0,'暂无可领取的养成奖励')
        rewards=[[11,0,amount,1]]; w['plan_claimed']+=amount
    else:
        i=d.get('index'); a.require(type(i)is int,'奖励编号无效')
        if typ==72:
            main=d.get('main_type'); a.require(type(main)is int and main in (1,2),'洞府目标类型无效')
            row=goals(s)[main]['target_list'].get(i);key=f'target:{main}:{i}';extra['main_type']=main
        else:
            row=community(role,s)['act_data'].get(i);key=f'community:{i}'
        a.require(row is not None and row['status']==2,'奖励条件未达成或已经领取')
        p=row['prize_list'][0]; rewards=[[p['object_type'],p['attach_type'],p['attach_count'],p['attach_level']]]
        w['claims'].append(key);extra['index']=i
    prizes=a.prizes(role,rewards)
    return [h.response(24,dict(flag=2,act_type=typ,prize_list=prizes,all_activity=view(role,s,now,r),**extra))]
