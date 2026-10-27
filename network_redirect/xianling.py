"""Original xianlingShopUI protocol [A], configurable offline catalog [B]."""
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from . import formation as f, summon, journey
from .protocol import encode

ROOT = Path(__file__).resolve().parents[1]

def load_rules(path=ROOT/'server_config/xianling_rules.json'):
    r=json.loads(Path(path).read_text())
    f.require(r['schema_version']==1 and r['mode']=='inferred','仙灵配置来源无效')
    f.require(r['monthly_thresholds']==[1,500,1500,3000],'仙灵月礼包门槛须与原版文案一致')
    f.require(len(r['monthly_prizes'])==4 and 1<=len(r['exchange'])<=255,'仙灵商品配置无效')
    f.require(len(r['daily_limits'])==11 and all(type(n)is int and 0<=n<=1000 for n in r['daily_limits']),'仙灵限购配置无效')
    f.require(r['daily_price']==10 and r['box_cost']==30 and r['box_targets']==[5001,5004,5005], '仙灵原版价格检查或界魂箱规则不符')
    for p in [r['daily_prize']]+[p for row in r['monthly_prizes'] for p in row]+[row['prize'] for row in r['exchange']]:
        f.require(isinstance(p,list) and len(p)==4 and all(type(n)is int for n in p),'仙灵奖励格式无效')
        typ,tid,n,lv=p
        f.require(typ==5 and tid in f.ITEMS and 0<n<=100000 and lv==1,'仙灵奖励物品无效')
    for row in r['exchange']:
        f.require(type(row['price'])is int and 0<row['price']<=100000,'灵玉价格无效')
    return r


def prepare(role, now):
    dt=datetime.fromtimestamp(now,timezone(timedelta(hours=8)))
    month=dt.strftime('%Y-%m');day=dt.strftime('%Y-%m-%d')
    s=role.setdefault('xianling',dict(month=month,day=day,charge=0,claimed=[],bought=0))
    if s['month']!=month:s.update(month=month,charge=0,claimed=[])
    if s['day']!=day:s.update(day=day,bought=0)
    return s


def record_charge(role,gold,now):
    f.require(type(gold)is int and gold>0,'充值统计无效')
    prepare(role,now)['charge']+=gold


def statuses(role,now,r):
    s=prepare(role,now)
    return [3 if i in s['claimed'] else 2 if s['charge']>=threshold else 1
            for i,threshold in enumerate(r['monthly_thresholds'],1)]


def hint(role,now,r):
    return dict(had_gift=2 in statuses(role,now,r))


def tip(role,now,r):
    return encode(2995,dict(tip_type=10,tip_info=summon.lua(hint(role,now,r))))


def spec(p):
    return dict(object_type=p[0],attach_type=p[1],attach_count=p[2],attach_level=p[3])


def remaining(role,now,r):
    return max(0,r['daily_limits'][max(0,min(10,role.get('vip_level',0)))]-prepare(role,now)['bought'])


def snapshot(role,now,r):
    s=prepare(role,now)
    return dict(flag=4,index=0,exchange_list=[dict(spec(row['prize']),price=row['price']) for row in r['exchange']],
                shop_data=dict(attach_list=[spec(r['daily_prize'])],need_gold=r['daily_price']),
                month_charge=s['charge'],canbuy_count=remaining(role,now,r),
                charge_shop=[dict(attach_list=[spec(p) for p in row]) for row in r['monthly_prizes']],
                take_list=statuses(role,now,r))


def consume(role,tid,n):
    # Only unlocked, unowned stacks can be currency/materials.
    items=[a for a in role['attachments'] if a['attach_type']==5 and a['type_id']==tid and not a.get('is_lock') and not a.get('owner_id') and not a.get('equip_pos')]
    f.require(sum(a['count'] for a in items)>=n,'灵玉不足' if tid==1140 else '界魂箱不足')
    for a in items:
        take=min(n,a['count']);a['count']-=take;n-=take
    role['attachments']=[a for a in role['attachments'] if a not in items or a['count']>0]


def settle(role,mid,req,now,r):
    s=prepare(role,now)
    if mid==1051:
        f.require(req['item_type']==1249 and req['item_count']==r['box_cost'] and req['des_type']==5 and req['des_id'] in r['box_targets'],'界魂箱兑换目标或数量无效')
        item=f.lookup(role,'attachments',req['item_id'])
        f.require(item['type_id']==1249 and item['attach_type']==5 and item.get('count',0)>=r['box_cost']
                  and not any(item.get(k) for k in ('is_lock','owner_id','equip_pos','equip_order')),'界魂箱实例无效或该叠数量不足')
        item['count']-=r['box_cost']
        if not item['count']:role['attachments'].remove(item)
        prize=journey.grant(role,[5,int(req['des_id']),1,1])
        return [summon.event(21,dict(result=1,type_id=1249,count=r['box_cost'],attach_list=[prize]))]
    op,index,n=req['flag'],req['index'],req['count']
    f.require(op in (1,2,3,4),'仙灵操作无效')
    if op==4:return [summon.event(185,snapshot(role,now,r))]
    f.require(1<=n<=999,'仙灵数量无效')
    if op==1:
        f.require(1<=index<=len(r['exchange']),'仙灵商品不存在')
        row=r['exchange'][index-1];consume(role,1140,row['price']*n)
        typ,tid,count,lv=row['prize'];prizes=[journey.grant(role,[typ,tid,count*n,lv])]
    elif op==3:
        f.require(index==1 and n==1,'限购商品每次仅能购买一个')
        f.require(remaining(role,now,r)>0,'今日购买数量已达限购上限')
        f.debit_money(role,'gold_coin',r['daily_price'])
        prizes=[journey.grant(role,r['daily_prize'])];s['bought']+=1
    else:
        f.require(1<=index<=4 and n==1,'月度礼包编号无效')
        f.require(statuses(role,now,r)[index-1]==2,'月度充值不足或礼包已领取')
        prizes=[journey.grant(role,p) for p in r['monthly_prizes'][index-1]];s['claimed'].append(index)
    # Full state first: original exchange/buy callbacks only repaint their old tables.
    return [summon.event(185,snapshot(role,now,r)),summon.event(185,dict(flag=op,index=index,
            canbuy_count=remaining(role,now,r),take_list=statuses(role,now,r),attach_list=prizes))]
