"""VIP wire/UI rules [A]; missing economy is explicit inferred configuration [B]."""
import json
import re
from pathlib import Path
from . import formation as f, summon, journey
from .protocol import encode

ROOT = Path(__file__).resolve().parents[1]
# Original vip_pri_config.csv: unspecified levels inherit the previous tier.
RESOURCE = [0,5,8,10,12,14,16,18,18,22,26]
REFRESH = [0,1,2,3,3,4,5,6,6,6,6]
RANK = [0,6,7,8,10,12,12,12,12,12,12]
RAPE = [0,4,5,6,7,8,9,10,11,12,12]
# Total includes the original first free challenge plus CSV token attempts.
CONVERT = [1,2,2,3,3,4,5,6,7,8,9]
DIVINATION = [0,10,10,20,20,30,30,40,40,50,50]
GIFTS = {int(x['vip_level']): x for x in summon.rows('item_receive_config.csv')}


def load_rules(path=ROOT / 'server_config/vip_rules.json'):
    r = json.loads(Path(path).read_text())
    f.require(r['schema_version'] == 1 and r['mode'] == 'inferred', 'VIP配置来源无效')
    for key in ('thresholds','daily_gold','daily_jade'):
        f.require(len(r[key]) == 11 and all(type(n) is int and 0 <= n <= 100000000 for n in r[key]), 'VIP配置数值无效')
    f.require(r['thresholds'][0] == 0 and all(a < b for a,b in zip(r['thresholds'],r['thresholds'][1:])), 'VIP门槛无效')
    f.require(r['daily_gold'][:4] == [0]*4 and r['daily_jade'][0] == 0 and all(r['daily_jade'][1:]), 'VIP福利与原版不符')
    for row in r['bag_pool']:
        f.require(type(row['weight']) is int and row['weight'] > 0, '乾坤袋概率无效')
        typ,tid,n,lv = row['prize']
        f.require(typ in (5,11,12) and n > 0 and lv == 1 and (typ != 5 or tid in f.ITEMS), '乾坤袋奖励无效')
    f.require(len({p['id'] for p in r['products']}) == len(r['products']) and all(type(p['gold']) is int and 0 < p['gold'] <= 1000000 for p in r['products']), '模拟充值商品无效')
    f.require(all(type(p.get('bonus', 0)) is int and 0 <= p.get('bonus', 0) <= 1000000 for p in r['products']), '模拟充值赠送数量无效')
    return r


def level(role):
    return max(0, min(10, int(role.get('vip_level', 0))))


def limit(role, table, fallback):
    return table[level(role)] if level(role) else fallback


def prepare(role, r):
    role.setdefault('vip_level', 0)
    for k in ('vip_gift','take_vip_gold_time','charge_gold'):
        role.setdefault(k, 0)
    v = level(role)
    role['next_charge_gold'] = r['thresholds'][min(10,v+1)]
    role['day_take_gold_limit'] = r['daily_gold'][v]
    role['enhance_inbatch_limit'] = int(v >= 3)


def client_config(r):
    return {v:dict(charge_gold=r['thresholds'][v],lingyu_count=r['daily_jade'][v],day_take_gold_limit=r['daily_gold'][v],
                  day_pick_cortege_limit={grade:int(summon.load_rules()['grades'][str(grade)]['paid_daily_limit']) for grade in (1,2,3)}) for v in range(11)}


def handles(mid, req):
    return (mid == 1201 and req['flag'] in (5,7) or
            mid == 1051 and (req['item_type'] == 1031 or 1101 <= req['item_type'] <= 1110) or
            mid == 1111 and req['event_id'] == 250)


def attrs(role):
    pairs = [(7,'silver_coin'),(8,'gold_coin'),(15,'take_vip_gold_time'),(51,'vip_level'),(52,'vip_gift'),(70,'next_charge_gold')]
    return encode(1032,dict(id=role['role_id'],unit_type=1,attr_count=len(pairs),attr_list=[dict(type=t,value=role[k]) for t,k in pairs]))


def settle(role, mid, req, now, r, parse):
    prepare(role,r); v = level(role)
    if mid == 1111:
        data = parse(req['data'])
        product = next((p for p in r['products'] if p['id'] == data.get('item_id')), None)
        f.require(product is not None, '模拟充值商品不存在')
        order = data.get('order_id')
        f.require(isinstance(order,str) and re.fullmatch(r'[A-Za-z0-9-]{8,80}',order), '模拟充值订单编号无效')
        orders = role.setdefault('vip_orders', {})
        if order in orders:
            f.require(orders[order] == product['id'], '模拟充值订单内容冲突')
            return [summon.event(55,dict(op_string='该模拟充值订单已到账'))]
        orders[order] = product['id']
        role['charge_gold'] += product['gold']; role['gold_coin'] += product['gold'] + product.get('bonus', 0)
        role['vip_level'] = max(v, max(i for i,n in enumerate(r['thresholds']) if role['charge_gold'] >= n))
        prepare(role,r)
        return [summon.event(55,dict(op_string='本地模拟充值成功，不发生真实扣款'))]
    if mid == 1201 and req['flag'] == 5:
        day = lambda t: (t+r['timezone_offset_hours']*3600)//86400
        f.require(v > 0, 'VIP1开放每日福利')
        f.require(not role['take_vip_gold_time'] or day(role['take_vip_gold_time']) != day(now), '今日VIP福利已领取')
        gold,jade=r['daily_gold'][v],r['daily_jade'][v]
        role['gold_coin'] += gold; summon.add_item(role,1140,jade)
        role['take_vip_gold_time'] = now
        return [summon.event(58,dict(gold_count=gold,lingyu_count=jade))]
    if mid == 1201:
        target=req['id']
        f.require(target in GIFTS and 1 <= target <= v, 'VIP等级不足或礼包编号无效')
        f.require(not role['vip_gift'] & (1 << target), 'VIP礼包已领取')
        tid=int(GIFTS[target]['type_id']); summon.add_item(role,tid,1)
        role['vip_gift'] |= 1 << target
        return [summon.event(59,dict(type_id=tid,count=1))]
    tid,n=req['item_type'],req['item_count']
    f.require(1 <= n <= 15 and req['des_type'] == 1 and req['des_id'] in (0,role['role_id']), '开包参数无效')
    f.require(v >= (1 if tid == 1031 else tid-1100), 'VIP等级不足')
    item=f.lookup(role,'attachments',req['item_id'])
    f.require(item['type_id']==tid and item['attach_type']==5 and item['count']>=n and not item.get('is_lock'), '礼包不足或已锁定')
    specs=[]
    if tid == 1031:
        weights={i:x['weight'] for i,x in enumerate(r['bag_pool'])}
        specs=[r['bag_pool'][summon.weighted_choice(weights)]['prize'] for _ in range(n)]
    else:
        for token in GIFTS[tid-1100]['attach_data'].split('/'):
            typ,t,lv,count=map(int,token.split('|'))
            specs.append([typ,t,count*n,lv])
    item['count']-=n
    if not item['count']:role['attachments'].remove(item)
    prizes=[journey.grant(role,p) for p in specs]
    return [summon.event(21,dict(result=1,type_id=tid,count=n,attach_list=prizes))]


def client_state(role):
    keys = ('charge_gold','vip_level','vip_gift','next_charge_gold','day_take_gold_limit','enhance_inbatch_limit',
            'strength_item_limit','energy_item_limit','top_fight_limit','rape_flush_limit','convert_fight_limit','tollgate_flush_limit')
    return {k:role[k] for k in keys if k in role}
