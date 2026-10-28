"""Inventory-backed offline payments; every benefit uses the same paid principal.

Original catalog/month card values are from order_config and monthCardUI [A].
Small cards are 5 RMB by the user's explicit offline rule, not the old 10 RMB text.
The caller holds the SQLite write lock, encodes replies, then commits once.
"""
import json
import re
from pathlib import Path

from . import formation as f, summon, vip, welfare, xianling
from .protocol import encode

RULES = Path(__file__).resolve().parents[1] / 'server_config/recharge_rules.json'
ORDER = re.compile(r'[A-Za-z0-9-]{8,80}')


def load_rules(path=RULES):
    r = json.loads(Path(path).read_text())
    f.require(r['schema_version'] == 1 and r['mode'] == 'offline_cards', '金卡充值配置无效')
    f.require((r['large_item_id'], r['small_item_id'], r['large_rmb'], r['small_rmb'], r['gold_per_rmb']) ==
              (1152, 1156, 50, 5, 10), '金卡面值配置无效')
    for k in ('max_cards_per_order', 'month_days', 'month_daily_gold', 'month_renew_below_days'):
        f.require(type(r[k]) is int and 0 < r[k] <= 10000, '金卡配置数值无效')
    seen = set()
    for p in r['products']:
        f.require(type(p['id']) is int and p['id'] not in seen and p['kind'] in ('gold', 'month', 'fund'), '充值商品无效')
        seen.add(p['id'])
        f.require(all(type(p[k]) is int and 0 <= p[k] <= 1000000 for k in ('rmb', 'gold', 'bonus')) and
                  p['rmb'] > 0 and p['rmb'] % r['small_rmb'] == 0, '充值商品金额无效')
    return r


def available(item, tid):
    return (item.get('attach_type') == 5 and item.get('type_id') == tid and
            not any(item.get(k) for k in ('is_lock', 'owner_id', 'equip_pos')))


def count(role, tid):
    return sum(i['count'] for i in role['attachments'] if available(i, tid))


def consume(role, tid, n, selected=None):
    items = [i for i in role['attachments'] if available(i, tid) and (selected is None or i['id'] == selected)]
    f.require(sum(i['count'] for i in items) >= n, '可用金卡不足，请检查背包数量或锁定状态')
    for i in items:
        take = min(n, i['count']); i['count'] -= take; n -= take
    # Skill count is failure compensation, not an inventory stack size.
    consumed = {i['id'] for i in items if i['count'] == 0}
    role['attachments'] = [i for i in role['attachments'] if i['id'] not in consumed]


def handles(mid, req):
    return (mid in (1111, 1112) or mid == 1201 and req['flag'] == 9 or
            mid == 1051 and req['item_type'] in (1150, 1151, 1152, 1156))


def record(role, principal, now, vr, wr, *, double=True):
    """Single authoritative fan-out; bonuses and daily rewards never call this."""
    from . import activity_pavilion, activity_yuanshi, activity_rulai
    role['charge_gold'] = role.get('charge_gold', 0) + principal
    f.require(role['charge_gold'] <= 2147483647, '累计充值额度超出协议上限')
    role['vip_level'] = max(vip.level(role), max(i for i, n in enumerate(vr['thresholds']) if role['charge_gold'] >= n))
    vip.prepare(role, vr)
    welfare.record_charge(role, principal, now, wr, fund=not double)
    xianling.record_charge(role, principal, now)
    activity_pavilion.record_charge(role, principal, now)
    activity_yuanshi.record_charge(role, principal, now)
    activity_rulai.record_charge(role, principal, now)


def settle(role, mid, req, now, r, vr, wr, parse):
    bag_order = None
    if mid == 1111 and req['event_id'] == 253:
        data = parse(req['data'])
        f.require(set(data) == {'order_id', 'item_id', 'item_type', 'item_count', 'des_type', 'des_id'}, '金卡使用订单参数无效')
        bag_order = data.pop('order_id')
        f.require(isinstance(bag_order, str) and ORDER.fullmatch(bag_order) and not bag_order.startswith('bag-'), '充值订单编号无效')
        f.require(all(type(data[k]) is int for k in ('item_type', 'item_count', 'des_type')) and
                  type(data['item_id']) in (int, float) and type(data['des_id']) in (int, float), '金卡使用参数无效')
        mid, req = 1051, dict(data, serial_num=req['serial_num'])
    if mid == 1201:
        f.require(now >= role.get('recharge', {}).get('last_time', 0), '充值时钟已回退，请恢复本地时间')
        f.require(req['id'] == 0, '月卡领取参数无效')
        f.require(now < role.get('month_card_time', 0), '月卡未开通或已到期')
        day = lambda t: (t + r['timezone_offset_hours'] * 3600) // 86400
        last = role.get('month_card_record', 0)
        f.require(not last or day(now) > day(last), '今日月卡奖励已领取或时钟已回退')
        role['gold_coin'] += r['month_daily_gold']
        role['month_card_record'] = now
        role.pop('month_card_rewards_remaining', None)
        return [summon.event(74, dict(result=1, gold_count=r['month_daily_gold']))]
    if mid == 1111 and req['event_id'] == 252:
        f.require(now >= role.get('recharge', {}).get('last_time', 0), '充值时钟已回退，请恢复本地时间')
        data = parse(req['data'])
        f.require(set(data) == {'index'} and type(data['index']) is int, '单充领奖参数无效')
        return welfare.claim_single(role, data['index'], now, wr)
    state = role.setdefault('recharge', dict(orders={}, last_order_id='', last_time=0))
    if mid == 1051:
        tid, n = req['item_type'], req['item_count']
        f.require(tid in (1152, 1156), '该金卡面值尚未确认，请使用大传世金卡或小传世金卡')
        f.require(type(n) is int and 1 <= n <= 15 and req['des_type'] == 1 and req['des_id'] in (0, role['role_id']), '金卡使用参数无效')
        # Native item-use packets have no order ID. Persist their full fingerprint
        # to prevent reconnect/restart replay from charging a second time.
        order = bag_order or 'bag-' + str(req['serial_num'])
        fingerprint = {k: req[k] for k in ('item_id', 'item_type', 'item_count', 'des_type', 'des_id')}
        large, small = (n, 0) if tid == 1152 else (0, n)
        p = dict(id=0, kind='card', rmb=large * r['large_rmb'] + small * r['small_rmb'], bonus=0)
        p['gold'] = p['rmb'] * r['gold_per_rmb']
    else:
        f.require(mid == 1111 and req['event_id'] == 251, '免费模拟充值已移除，请从充值入口选择金卡支付')
        data = parse(req['data'])
        f.require(set(data) == {'item_id', 'order_id', 'large_count', 'small_count'}, '金卡订单参数无效')
        f.require(type(data['item_id']) is int, '充值商品编号无效')
        p = next((p for p in r['products'] if p['id'] == data['item_id']), None)
        f.require(p is not None, '充值商品不存在')
        order, large, small = data['order_id'], data['large_count'], data['small_count']
        f.require(isinstance(order, str) and ORDER.fullmatch(order) and not order.startswith('bag-'), '充值订单编号无效')
        f.require(all(type(n) is int and 0 <= n <= r['max_cards_per_order'] for n in (large, small)) and
                  0 < large + small <= r['max_cards_per_order'], '金卡数量无效')
        f.require(large * r['large_rmb'] + small * r['small_rmb'] >= p['rmb'], '金卡面值合计不足商品金额')
        fingerprint = dict(item_id=p['id'], large_count=large, small_count=small)
    previous = state['orders'].get(order)
    if previous:
        f.require(previous['request'] == fingerprint, '充值订单内容冲突，请刷新')
        state['last_order_id'] = order
        return [summon.event(55, dict(op_string='该金卡订单已结算，无需再次支付'))]
    f.require(now >= state['last_time'], '充值时钟已回退，请恢复本地时间')
    if p['kind'] == 'fund':
        f.require(not role.get('buy_growup'), '成长基金已购买')
    if p['kind'] == 'month':
        f.require(role.get('month_card_time', 0) - now < r['month_renew_below_days'] * 86400, '月卡剩余时间较长，请稍后续期')
    # Validate both pools before either is consumed.
    f.require(count(role, 1152) >= large and count(role, 1156) >= small, '可用金卡不足，请检查背包数量或锁定状态')
    consume(role, 1152, large, req['item_id'] if mid == 1051 else None)
    consume(role, 1156, small, req['item_id'] if mid == 1051 else None)
    role['gold_coin'] += p['gold'] + p['bonus']
    if p['kind'] == 'month':
        role.pop('month_card_rewards_remaining', None)
        role['month_card_time'] = max(now, role.get('month_card_time', 0)) + r['month_days'] * 86400
    if p['kind'] == 'fund':
        role['buy_growup'] = 1
    # Excess card value is not returned or credited; benefits use the product price.
    principal = p['rmb'] * r['gold_per_rmb']
    was_first = not role.get('first_charge') and p['kind'] in ('gold', 'card')
    record(role, principal, now, vr, wr, double=p['kind'] in ('gold', 'card'))
    # The pavilion mail hook replaces nested dictionaries: reacquire after fan-out.
    state = role['recharge']
    state['orders'][order] = dict(request=fingerprint, product_id=p['id'], kind=p['kind'], rmb=p['rmb'],
                                principal=principal, gold=p['gold'], bonus=p['bonus'], first_bonus=principal if was_first else 0,
                                large_count=large, small_count=small, settled_at=now)
    state.update(last_order_id=order, last_time=now)
    events = [summon.event(55, dict(op_string=f"金卡充值成功，计入充值{p['rmb']}元"))]
    if mid == 1051:
        events = [summon.event(21, dict(result=1, type_id=tid, count=n, attach_list=[dict(
            object_type=11, attach_type=0, attach_count=p['gold'] + (principal if was_first else 0), attach_level=1)]))]
    return events


def client_state(role, now, r, wr):
    return dict(products=r['products'], large_count=count(role, 1152), small_count=count(role, 1156),
                large_rmb=r['large_rmb'], small_rmb=r['small_rmb'],
                last_order_id=role.get('recharge', {}).get('last_order_id', ''),
                month=dict(rmb=50, daily_gold=r['month_daily_gold'], expires_at=role.get('month_card_time', 0),
                           last_claim_at=role.get('month_card_record', 0)),
                single=welfare.single_catalog(role, now, wr))


def attrs(role):
    pairs = [(21, 'month_card_time'), (22, 'month_card_record')]
    return encode(1032, dict(id=role['role_id'], unit_type=1, attr_count=len(pairs),
                            attr_list=[dict(type=t, value=role.get(k, 0)) for t, k in pairs]))
