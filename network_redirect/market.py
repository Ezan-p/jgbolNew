"""Original market wire/UI contract [A], explicit local server policy [B]."""
import json
import math
import hashlib
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
    # User schedule: Tue/Thu/Sat, retaining native 12:00 and 18:00 sessions.
    require(p.get('weekdays') == [1, 3, 5] and p.get('hours') == [12, 18])
    require(integer(p['stock'], 1, 100000))
    require(p['stock'] == 3 and p['per_buy_limit'] == 1 and p['discount_percent'] == 70)
    require(isinstance(p.get('pairs'), list) and 1 <= len(p['pairs']) <= 1000)
    for pair in p['pairs']:
        require(integer(pair.get('weight'), 1, 1000000))
        for key in ('first', 'second'):
            item = pair[key]
            require(item['type_id'] in NAMES and item['type_id'] in formation.ITEMS)
            require(formation.ITEMS[item['type_id']]['can_stack'] == '1' or item['count'] == 1)
            require(integer(item['count'], 1, 10000) and integer(item['price'], 2, 1000000))
    for type_id, override in rules.get('cheap_overrides', {}).items():
        require(int(type_id) in NAMES)
        for key, value in override.items():
            require(key in ('count', 'origin_price') and integer(value, 1, 1000000))
    indices = {int(row['index']) for row in CATALOG}
    for section in ('cheap_additions', 'rich_additions'):
        for row in rules.get(section, []):
            require(integer(row['index'], 1, 255) and row['index'] not in indices)
            indices.add(row['index'])
            require(row['type_id'] in NAMES and row['type_id'] in formation.ITEMS)
            for key in ('count', 'origin_price', 'buy_price', 'order'):
                require(integer(row[key], 1, 1000000))
            require(integer(row['vip_level'], 0, 10))
            if section == 'cheap_additions':
                require(integer(row['daily_limit'], 1, 1000))
            require(formation.ITEMS[row['type_id']]['can_stack'] == '1' or row['count'] == 1)
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


def rotation_start(now, rules):
    start = day_start(now, rules)
    weekday = datetime.fromtimestamp(start + rules['reset_utc_offset_hours'] * 3600, timezone.utc).weekday()
    return start - next(d for d in range(7) if (weekday - d) % 7 in rules['panic']['weekdays']) * 86400


def selected_pair(state, rules):
    pair = rules['panic']['pairs'][state['pair_index']]
    return (dict(pair['first'], discounts=[0.7] * 6, panic_price=pair['first']['price'] * 70 // 100),
            dict(pair['second'], panic_price=pair['second']['price'] * 70 // 100,
                 per_buy_limit=rules['panic']['per_buy_limit']))


def prepare(role, now, rules):
    state = role.setdefault('market', {})
    day = day_start(now, rules)
    if state.get('day') != day:
        state.update(day=day, purchases={})
    cycle = rotation_start(now, rules)
    if state.get('panic', {}).get('rotation_start') != cycle:
        # Stable independent draw per role/cycle: queries, failures and restarts
        # cannot reroll the candidate. Consecutive identical draws are allowed.
        seed = f"market-pairs:{role.get('role_id', 0)}:{cycle}".encode()
        pairs = rules['panic']['pairs']
        ticket = int.from_bytes(hashlib.sha256(seed).digest(), 'big') % sum(p['weight'] for p in pairs)
        for index, pair in enumerate(pairs):
            if ticket < pair['weight']:
                break
            ticket -= pair['weight']
        state['panic'] = dict(rotation_start=cycle, pair_index=index, sold=0,
                              last_buy_item1=0, has_buy_item2=0,
                              item1_sale_price=rules['panic']['pairs'][index]['first']['price'] * 70 // 100)
    state['panic']['sale_time'] = sale_time(now, rules)
    return state


def attachment(type_id, count):
    return dict(object_type=5, attach_type=type_id, attach_count=count, attach_level=1)


def panic_snapshot(role, now, rules):
    state = prepare(role, now, rules)['panic']
    first, second = selected_pair(state, rules)
    return dict(activity_data=dict(
        sale_time=state['sale_time'],
        sale_index=rules['panic']['hours'].index((state['sale_time'] - day_start(state['sale_time'], rules)) // 3600) + 1,
        item1_sale_count=max(0, rules['panic']['stock'] - state['sold']),
        item1_sale_price=state['item1_sale_price'],
        sale_item=[dict(item=attachment(first['type_id'], first['count']), price=first['price'],
                        panic_discount=first['discounts'], panic_price=first['panic_price']),
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
        override = rules.get('cheap_overrides', {}).get(str(type_id), {}) if page == 1 else {}
        count = override.get('count', count)
        # [A] Native monthCardUI promises one extra discounted Soul Fate Pill
        # per day. The same remaining quantity is enforced by buy(), so expiry
        # or renewal changes eligibility without resetting today's purchases.
        daily_limit = rules['cheap_daily_limit'] + int(
            page == 1 and type_id == 1024 and role.get('month_card_time', 0) > now)
        result[LISTS[page]][index] = dict(
            index=index, object_type=object_type, type_id=type_id, count=count,
            name=NAMES[type_id], buy_price=price, money_type=rules['money_type'],
            vip_level=int(raw['vip_level']), order=int(raw['order']),
            # [B] missing original-price fields: use matching normal unit price,
            # or the actual price when no normal listing survives.
            origin_price=override.get('origin_price', normal_prices[type_id] * count if type_id in normal_prices else price),
            begin_time=state['day'], end_time=state['day'] + 86400 - 1,
            buy_limit_times=max(0, daily_limit - state['purchases'].get(str(index), 0))
                            if page == 1 else 0, is_day_limit=1)
    for page, section in ((1, 'cheap_additions'), (2, 'rich_additions')):
        for extra in rules.get(section, []):
            index = extra['index']
            result[LISTS[page]][index] = dict(
                index=index, object_type=5, type_id=extra['type_id'], count=extra['count'],
                name=NAMES[extra['type_id']], buy_price=extra['buy_price'],
                origin_price=extra['origin_price'], money_type=rules['money_type'],
                vip_level=extra['vip_level'], order=extra['order'],
                begin_time=state['day'] if page == 1 else 0,
                end_time=state['day'] + 86400 - 1 if page == 1 else 0,
                buy_limit_times=max(0, extra['daily_limit'] - state['purchases'].get(str(index), 0))
                                if page == 1 else 0, is_day_limit=int(page == 1))
    from . import cheer
    result['rich_item_list'].update(cheer.market_goods(role))
    from . import equipment_crafting
    forge_goods = equipment_crafting.market_goods()
    for row in forge_goods.values():
        row['name'] = NAMES[row['type_id']]
    result['rich_item_list'].update(forge_goods)
    result.update(panic_buy_list=panic_snapshot(role, now, rules),
                  item_begin_time=0, item_end_time=0, server_time=now)
    return result


def grant(role, type_id, count):
    # Some original seasonal gifts cannot stack; preserve each inventory ID.
    if formation.ITEMS[type_id]['can_stack'] == '0':
        for _ in range(count):
            role['attachments'].append(dict(id=formation.new_id(role), attach_type=5,
                type_id=type_id, count=1, level=1, equip_order=0, equip_pos=0))
        return
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
                index=index, page_id=page, attach_list=[attachment(row['type_id'], row['count'] * count)])


def current_price(now, start, first):
    # Fixed-price pools use the same integer quote for preview and settlement.
    if 'panic_price' in first:
        return first['panic_price']
    # Legacy stepped-price contract. [A] Lua floor(price * discount).
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
        item = selected_pair(state, rules)[0]
        price = current_price(now, start, item)
    elif index == 2:
        if state['sold'] < rules['panic']['stock']:
            raise Rejected(4)
        item = selected_pair(state, rules)[1]
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
