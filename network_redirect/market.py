"""Original market wire/UI contract [A], explicit local server policy [B]."""
import json
import math
from datetime import datetime, timezone
from pathlib import Path

from . import formation, summon

RULES_PATH = Path(__file__).resolve().parents[1] / 'server_config/market_rules.json'
CATALOG = summon.rows('item_buy_config.csv')
NAMES = {int(r['Ftype_id']): r['name'] for r in summon.rows('item_name.csv')}
LISTS = {1: 'cheap_item_list', 2: 'rich_item_list', 3: 'limit_item_list'}


class Rejected(ValueError):
    def __init__(self, result):
        self.result = result
        super().__init__('market result %d' % result)


def load_rules(path=RULES_PATH):
    rules = json.loads(Path(path).read_text(encoding='utf-8'))
    def integer(value, low, high):
        return type(value) is int and low <= value <= high
    def require(ok):
        if not ok:
            raise ValueError('集市配置无效：请检查 market_rules.json')
    require(rules.get('schema_version') == 1 and rules.get('mode') == 'inferred_server')
    require(integer(rules.get('reset_utc_offset_hours'), -12, 14))
    require(rules.get('money_type') in (11, 12))
    require(integer(rules.get('cheap_daily_limit'), 1, 1000))
    require(integer(rules.get('max_batch_count'), 1, 999))
    p = rules['panic']
    # [A] String.plist sales1 explicitly promises Tue/Thu 12:00 and 18:00.
    require(p.get('weekdays') == [1, 3] and p.get('hours') == [12, 18])
    require(integer(p['stock'], 1, 100000))
    for key in ('first', 'second'):
        item = p[key]
        require(item['type_id'] in NAMES and item['type_id'] in formation.ITEMS
                and formation.ITEMS[item['type_id']]['can_stack'] == '1')
        require(integer(item['count'], 1, 10000) and integer(item['price'], 1, 1000000))
    discounts = p['first']['discounts']
    require(isinstance(discounts, list) and len(discounts) == 6
            and all(type(d) in (float, int) and math.isfinite(d) and 0 < d <= 1
                    and math.floor(p['first']['price'] * d) >= 1 for d in discounts)
            and discounts == sorted(discounts, reverse=True))
    require(integer(p['second']['panic_price'], 1, p['second']['price']))
    require(integer(p['second']['per_buy_limit'], 1, 10000))
    return rules


def day_start(now, rules):
    offset = rules['reset_utc_offset_hours'] * 3600
    return (now + offset) // 86400 * 86400 - offset


def sale_time(now, rules):
    start = day_start(now, rules)
    # Preserve the original inclusive end (start < now <= start + 3600).
    weekday = datetime.fromtimestamp(start + rules['reset_utc_offset_hours'] * 3600, timezone.utc).weekday()
    candidates = [start + day * 86400 + hour * 3600
                  for day in range(-1, 8) if (weekday + day) % 7 in rules['panic']['weekdays']
                  for hour in rules['panic']['hours']]
    active = [t for t in candidates if t < now <= t + 3600]
    return max(active) if active else min(t for t in candidates if t >= now)


def prepare(role, now, rules):
    state = role.setdefault('market', {})
    day = day_start(now, rules)
    if state.get('day') != day:
        state.update(day=day, purchases={})
    start = sale_time(now, rules)
    if state.get('panic', {}).get('sale_time') != start:
        state['panic'] = dict(sale_time=start, sold=0, last_buy_item1=0,
                              has_buy_item2=0, item1_sale_price=rules['panic']['first']['price'])
    return state


def attachment(type_id, count):
    return dict(object_type=5, attach_type=type_id, attach_count=count, attach_level=1)


def panic_snapshot(role, now, rules):
    state = prepare(role, now, rules)['panic']
    first, second = rules['panic']['first'], rules['panic']['second']
    return dict(activity_data=dict(
        sale_time=state['sale_time'],
        sale_index=rules['panic']['hours'].index((state['sale_time'] - day_start(state['sale_time'], rules)) // 3600) + 1,
        item1_sale_count=max(0, rules['panic']['stock'] - state['sold']),
        item1_sale_price=state['item1_sale_price'],
        sale_item=[dict(item=attachment(first['type_id'], first['count']), price=first['price'],
                        panic_discount=first['discounts']),
                   dict(item=attachment(second['type_id'], second['count']), price=second['price'],
                        panic_price=second['panic_price'], per_buy_limit=second['per_buy_limit'])]),
        role_data=dict(last_buy_item1=state['last_buy_item1'], has_buy_item2=state['has_buy_item2']))


def catalog(role, now, rules):
    state = prepare(role, now, rules)
    result = {key: {} for key in LISTS.values()}
    normal_prices = {int(r['type_id'].split('|')[1]): int(r['buy_price'])
                     for r in CATALOG if r['page_id'] == '2' and r['begin_time'] == '0'}
    for raw in CATALOG:
        # Only permanent entries: the dated 2013 events are not a 2026 schedule.
        if raw['begin_time'] != '0' or raw['end_time'] != '0':
            continue
        object_type, type_id, count = map(int, raw['type_id'].split('|'))
        index, page = int(raw['index']), int(raw['page_id'])
        price = int(raw['buy_price'])
        result[LISTS[page]][index] = dict(
            index=index, object_type=object_type, type_id=type_id, count=count,
            name=NAMES[type_id], buy_price=price, money_type=rules['money_type'],
            vip_level=int(raw['vip_level']), order=int(raw['order']),
            # [B] missing original-price fields: use matching normal unit price,
            # or the actual price when no normal listing survives.
            origin_price=normal_prices[type_id] * count if type_id in normal_prices else price,
            begin_time=state['day'], end_time=state['day'] + 86400 - 1,
            buy_limit_times=max(0, rules['cheap_daily_limit'] - state['purchases'].get(str(index), 0))
                            if page == 1 else 0, is_day_limit=1)
    from . import cheer
    result['rich_item_list'].update(cheer.market_goods(role))
    from . import activity_nine_sky
    result['rich_item_list'].update(activity_nine_sky.market_goods(now))
    result.update(panic_buy_list=panic_snapshot(role, now, rules),
                  item_begin_time=0, item_end_time=0, server_time=now)
    return result


def grant(role, type_id, count):
    item = next((i for i in role['attachments'] if i['attach_type'] == 5 and i['type_id'] == type_id), None)
    if item:
        if item['count'] + count > 2147483647:
            raise ValueError('物品数量超限')
        item['count'] += count
    else:
        role['attachments'].append(dict(id=formation.new_id(role), attach_type=5,
            type_id=type_id, count=count, level=1, equip_order=0, equip_pos=0))


def buy(role, request, now, rules):
    page, index, count = request['page_id'], request['index'], request['count']
    goods = catalog(role, now, rules)
    row = goods.get(LISTS.get(page), {}).get(index)
    if not row or row['type_id'] != request['type_id'] or not 1 <= count <= rules['max_batch_count']:
        raise Rejected(2)
    if role.get('vip_level', 0) < row['vip_level']:
        raise Rejected(5)
    if page == 1 and count > row['buy_limit_times']:
        raise Rejected(7)
    # Single-click limited purchases decrement one in the original callback.
    if page != 2 and count != 1:
        raise Rejected(2)
    currency = {11: 'gold_coin', 12: 'silver_coin'}[row['money_type']]
    price = row['buy_price'] * count
    if role.get(currency, 0) < price:
        raise Rejected(6)
    grant(role, row['type_id'], row['count'] * count)
    role[currency] -= price
    state = role['market']['purchases']
    state[str(index)] = state.get(str(index), 0) + count
    return dict(first_send=0, result=1, type_id=row['type_id'], count=count,
                index=index, page_id=page)


def current_price(now, start, first):
    # [A] Lua math.floor(price * discounts[ceil(elapsed / 600)]).
    if start < now <= start + 3600:
        return math.floor(first['price'] * first['discounts'][(now - start - 1) // 600])
    return first['price']


def panic_buy(role, request, now, rules, expected_sale_time):
    state = prepare(role, now, rules)['panic']
    start = state['sale_time']
    # [B] 1241 has no event identity: bind it to the last catalog/query on this
    # connection so an old queued click cannot buy the next session's item.
    if expected_sale_time != start or not start < now <= start + 3600:
        raise Rejected(4)
    index = request['buy_index']
    if index == 1:
        if state['sold'] >= rules['panic']['stock']:
            raise Rejected(5)
        if state['last_buy_item1'] and now < state['last_buy_item1'] + 10:
            raise Rejected(1)
        item = rules['panic']['first']
        price = current_price(now, start, item)
    elif index == 2:
        if state['sold'] < rules['panic']['stock']:
            raise Rejected(4)
        item = rules['panic']['second']
        if state['has_buy_item2'] >= item['per_buy_limit']:
            raise Rejected(3)
        price = item['panic_price']
    else:
        raise Rejected(1)
    if role.get('gold_coin', 0) < price:
        raise Rejected(2)
    grant(role, item['type_id'], item['count'])
    role['gold_coin'] -= price
    if index == 1:
        state['sold'] += 1
        state['last_buy_item1'] = now
        state['item1_sale_price'] = price
    else:
        state['has_buy_item2'] += 1
    return dict(panic_snapshot(role, now, rules), result=0,
                attach_list=[attachment(item['type_id'], item['count'])])
