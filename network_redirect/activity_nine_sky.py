"""九重天: original 1309/164 and route CSV [A]; event economy [B]."""
import copy
import json
import secrets
from datetime import datetime, timedelta, timezone
from pathlib import Path

from . import activity as a, formation as f, summon

ROOT = Path(__file__).resolve().parents[1]
LEVELS = [int(row['need_steps']) for row in summon.rows('tower_level.csv')]
ROADS = {(int(row['old']), int(row['new'])): row['road'] for row in summon.rows('tower_road.csv')}
DIRECTIONS = {'1': (0, 1), '2': (-1, 0), '3': (1, 0)}


def load_rules(path=ROOT / 'server_config/nine_sky_rules.json'):
    r = json.loads(Path(path).read_text())
    f.require(r.get('schema_version') == 1 and r.get('mode') == 'inferred'
              and isinstance(r.get('revision'), str) and r['revision'], '九重天配置来源无效')
    f.require(type(r.get('enabled')) is bool, '九重天开关无效')
    for key, low, high in [('timezone_offset_hours', -12, 14), ('period_days', 1, 365),
                           ('min_level', 1, 200), ('bag_gold', 1, 1000000), ('bag_peaches', 1, 100000), ('daily_free', 1, 100), ('palace_every', 1, 100),
                           ('double_basis_points', 0, 10000), ('treasure_basis_points', 0, 10000),
                           ('battle_basis_points', 0, 10000)]:
        f.require(type(r.get(key)) is int and low <= r[key] <= high, '九重天配置无效：' + key)
    f.require(type(r.get('one_rock_money')) is int and r['one_rock_money'] == 100, '原版单次100元宝')
    vals = r.get('card_values')
    f.require(isinstance(vals, list) and bool(vals) and len(vals) <= 10 and
              all(type(v) is int and 1 <= v <= 9999 for v in vals) and len(set(vals)) == len(vals), '天星卡面额无效')
    f.require(r['timezone_offset_hours'] == 8 and r['period_days'] == 7, '九重天每周一北京时间刷新')
    f.require(type(r.get('recycle_stars_per_peach')) is int and r['recycle_stars_per_peach'] == 2, '天星回收比例须为2:1')
    power = r.get('battle_floor_power')
    f.require(isinstance(power, list) and len(power) == 9 and
              all(type(v) is int and 1 <= v <= 10000000 for v in power) and
              all(x < y for x, y in zip(power, power[1:])), '九重天敌方战力须逐层递增')
    for name in ('star_shop', 'credit_shop', 'palace_cards', 'treasure_pool', 'battle_pool'):
        f.require(isinstance(r.get(name), list) and 1 <= len(r[name]) <= 20, '九重天商品缺失')
    f.require(len(r['palace_cards']) >= 2 and isinstance(r.get('palace_special'), dict), '天宫商品缺失')
    for row in r['star_shop'] + r['credit_shop'] + r['palace_cards'] + [r['palace_special']] + r['treasure_pool'] + r['battle_pool']:
        f.require(isinstance(row, dict), '九重天奖励行无效')
        p = row.get('reward')
        f.require(isinstance(p, list) and len(p) == 4 and all(type(v) is int for v in p), '九重天奖励格式无效')
        typ, tid, n, lv = p
        f.require(1 <= n <= 100000 and ((typ == 1 and (tid == -1 and lv in vals or tid == -2 and lv == 1))
                  or lv == 1 and (typ == 5 and tid in f.ITEMS or typ == 10 and tid in f.BASES
                  or typ in (11, 12) and tid == 0)), '九重天奖励无效')
        if row in r['treasure_pool'] + r['battle_pool']:
            f.require(type(row.get('weight')) is int and 1 <= row['weight'] <= 10000, '九重天权重无效')
        else:
            f.require('weight' not in row and type(row.get('cost')) is int and 1 <= row['cost'] <= 1000000 and
                      type(row.get('limit')) is int and 1 <= row['limit'] <= 1000, '九重天价格/限购无效')
    f.require(all(row['reward'][0] != 1 for row in r['star_shop'] + r['credit_shop'] + [r['palace_special']]), '常规商店需实体奖励')
    for row in r['palace_cards'] + [r['palace_special']]:
        f.require(type(row.get('money_type')) is int and row['money_type'] in (11, 12), '天宫货币无效')
    for name in ('treasure_pool', 'battle_pool'):
        f.require(all(type(row.get('weight')) is int and 1 <= row['weight'] <= 10000 for row in r[name]), '九重天奖励权重缺失')
    low = [x for x in r['star_shop'] if x.get('tier') == 'low']
    high = [x for x in r['star_shop'] if x.get('tier') == 'high']
    f.require(len(low) == 9 and len(high) == 5 and
              [x['reward'] for x in low] == [[5, t, 1, 1] for t in (1022,1023,1041,1033,1006,1032,1024,1042,1007)] and
              {tuple(x['reward']) for x in high} == {(10,5027,5,1),(10,5036,5,1),(5,1031,5,1),(5,1249,50,1),(5,1243,1,1)}, '九重商会奖励池不完整')
    f.require(all(x['cost'] < y['cost'] for x,y in zip(low,low[1:])) and
              all(x['limit'] == 1 for x in r['star_shop']), '九重商会定价须递增、每种每日限兑一份')
    return r


def period(now, r):
    duration = r['period_days'] * 86400
    anchor = 4 * 86400 - r['timezone_offset_hours'] * 3600
    start = (now - anchor) // duration * duration + anchor
    return start, start + duration


def status(now, r=None):
    r = r or load_rules()
    start, end = period(now, r)
    return dict(begin_time=start-1 if r['enabled'] else 0, end_time=end if r['enabled'] else 0,
                local_permanent=True, local_enabled=r['enabled'], next_weekly_refresh=end)


def recycle(role, s, now, r):
    """Deliver a permanent, idempotent attachment before discarding an old week."""
    stars = s['stars']
    if not stars:
        return s.get('last_recycle')
    from . import system_mail, welfare
    peaches = (stars + r['recycle_stars_per_peach'] - 1) // r['recycle_stars_per_peach']
    date = datetime.fromtimestamp(s['start'], timezone(timedelta(hours=8))).strftime('%Y-%m-%d')
    delivery = copy.deepcopy(role)
    _, mail = system_mail.deliver(delivery, key=f'nine-sky-recycle-{s["start"]}',
        title='九重天周刷新·天星返还',
        body=f'九重天常驻开放，每周一北京时间0点刷新。{date}开始的一周已结束。'
             f'剩余天星{stars}颗已全部回收，按2天星兑换1蟠桃，共返还蟠桃{peaches}个。'
             '奇数尾星不足2颗时补足1个蟠桃，请领取附件。天星不结转；残星、天星卡及活动内骰子随周进度清空。'
             '已入背包的道具及魂魄保留。', prizes=[[5,1001,peaches,1]], now=now, rules=welfare.load_rules())
    # deliver replaces its role object; copy just welfare to retain this state reference.
    role['welfare'] = delivery['welfare']
    return dict(start=s['start'], stars=stars, peaches=peaches, mail_id=mail['mail_id'])


def refresh_shop(s, r, today):
    old = s.get('shop')
    if today > s.get('shop_day', -1) or old is None:
        low = [x for x in r['star_shop'] if x['tier'] == 'low']
        high = [x for x in r['star_shop'] if x['tier'] == 'high']
        chosen = [low.pop(secrets.randbelow(len(low))) for _ in range(5)]
        chosen.sort(key=lambda row: row['cost'])
        chosen.append(secrets.choice(high))
        # Preserve matching quotas when upgrading the legacy fixed shop on the same day.
        legacy = {}
        if old is None and today == s['day']:
            for spec, used in zip([(10,5027),(5,1001),(5,1024),(5,1249)], s.get('purchases',{}).get('1',[])):
                legacy[spec] = used
        s['shop'] = copy.deepcopy(chosen)
        s['purchases'] = {'1': [min(x['limit'], legacy.get(tuple(x['reward'][:2]), 0)) for x in chosen],
                          '2': list(s.get('purchases',{}).get('2',[])) if legacy else [0]*len(r['credit_shop'])}
        s['shop_day'] = today
    if s.get('shop_revision') != r['revision']:
        # Configuration updates retain today's selection and purchases.
        configured = {tuple(x['reward'][:2]): x for x in r['star_shop']}
        s['shop'] = [copy.deepcopy(configured[tuple(x['reward'][:2])]) for x in s['shop']]
        s['shop_revision'] = r['revision']


def state(role, now, r):
    start, end = period(now, r)
    store = role.setdefault('activity', {})
    s = store.get('nine_sky')
    if s is None or now >= s['clock'] and start > s['start']:
        last_recycle = recycle(role, s, now, r) if s else None
        s = dict(start=start, end=end, clock=now, day=a.day(now, r), steps=0, floor=1,
                 cur_map=0, cur_point=dict(x=0, y=0), stars=0, credits=0,
                 free_times=r['daily_free'], cards={}, rolls=0, reached_at=now,
                 purchases={'1': [], '2': [0] * len(r['credit_shop'])},
                 palaces={}, palace_count=0)
        if last_recycle:
            s['last_recycle'] = last_recycle
        store['nine_sky'] = s
    today = max(a.day(now, r), s['day'])
    refresh_shop(s, r, today)
    if now >= s['clock'] and a.day(now, r) > s['day']:
        # Daily allowance expires; earned dice remain separately spendable.
        s['free_times'] = r['daily_free'] + s.get('bonus_dice', 0)
        s['day'] = a.day(now, r)
    s['clock'] = max(now, s['clock'])
    s['enabled'] = r['enabled']
    return s


def snapshot(s):
    return {k: copy.deepcopy(s[k]) for k in ('steps', 'cur_map', 'cur_point', 'stars', 'credits', 'free_times')} | dict(
        end_time=s['end'], local_permanent=True, local_enabled=s['enabled'],
        next_weekly_refresh=s['end'], next_daily_refresh=(s['shop_day']+1)*86400-8*3600,
        shop_day=s['shop_day'], shop_revision=s['shop_revision'])


def cards(s):
    return {int(k): v for k, v in s['cards'].items() if v > 0}


def grant(role, s, spec):
    typ, tid, n, lv = spec
    if typ == 1:
        if tid == -1:
            s['cards'][str(lv)] = s['cards'].get(str(lv), 0) + n
        else:
            s['free_times'] += n
            s['bonus_dice'] = s.get('bonus_dice', 0) + n
        return [a.prize_spec(spec)]
    return a.prizes(role, [spec])


def goods(row):
    return dict(attach_data=a.prize_spec(row['reward']), buy_limit=row['limit'],
                need_stars=row['cost'], need_credits=row['cost'],
                money_type=row.get('money_type', 11), need_count=row['cost'])


def palace_rows(index, r):
    pool = r['palace_cards']
    return [pool[(index - 1) % len(pool)], pool[index % len(pool)]]


def palace_data(s, index, r):
    p = s['palaces'][str(index)]
    return dict(shop_index=index, left_shop=[goods(r['palace_special'])],
                right_shop=[goods(row) for row in palace_rows(index, r)],
                predit_shop=[goods(row) for row in palace_rows(index + 1, r)],
                role_buy_list=copy.deepcopy(p))


def top(role, s, peers):
    candidates = [(s['steps'], s['reached_at'], role['role_id'], role)]
    for peer in (peers or []):
        ps = peer.get('activity', {}).get('nine_sky', {})
        if peer['role_id'] != role['role_id'] and ps.get('start') == s['start']:
            candidates.append((ps['steps'], ps['reached_at'], peer['role_id'], peer))
    winner = min(candidates, key=lambda c: (-c[0], c[1], c[2]))
    return dict(name=winner[3]['role_name'] if winner[0] else '', steps=winner[0])


def choose_map(s):
    remaining = LEVELS[s['floor'] - 1] - s['cur_point']['y']
    choices = []
    for new in range(1, 7):
        advance = ROADS[s['cur_map'], new].count('1')
        # Land exactly on the portal, retaining the original complete route.
        if advance <= remaining and (advance == remaining or
                any(ROADS[new, following].count('1') <= remaining - advance for following in range(1, 7))):
            choices.append(new)
    f.require(bool(choices), '九重天路径无效，请重新进入')
    return secrets.choice(choices)


def treasure(r):
    pick = secrets.randbelow(sum(row['weight'] for row in r['treasure_pool']))
    for row in r['treasure_pool']:
        if pick < row['weight']:
            return row['reward']
        pick -= row['weight']


def roll(role, s, data, now, r):
    before_snapshot = snapshot(s)
    n, payment = data.get('count'), data.get('index')
    f.require(type(n) is int and n in (1, 10) and type(payment) is int and payment in (0, 1), '九重天掷骰参数无效')
    if payment == 0:
        f.require(n == 1 and s['free_times'] > 0, '免费骰子不足')
        # Spend expiring daily allowance before earned dice.
        if s['free_times'] <= s.get('bonus_dice', 0):
            s['bonus_dice'] -= 1
        s['free_times'] -= 1
    else:
        a.spend(role, 'gold_coin', n * r['one_rock_money'])
    s['palaces'] = {}  # All encounters from the previous batch expire on a new roll.
    events, battles = [], []
    for _ in range(n):
        encounter_floor = s['floor']
        new = choose_map(s)
        road = ROADS[s['cur_map'], new]
        forward = road.count('1')
        double = secrets.randbelow(10000) < r['double_basis_points']
        s['stars'] += forward * 5 + (5 if double else 0)
        s['steps'] += forward
        s['reached_at'] = now
        for direction in road:
            dx, dy = DIRECTIONS[direction]
            s['cur_point']['x'] += dx
            s['cur_point']['y'] += dy
        entered = s['cur_point']['y'] == LEVELS[s['floor'] - 1]
        if entered:
            # [B] The final sentinel reuses the native portal animation in sky9.
            s['floor'] = min(9, s['floor'] + 1)
            s['cur_point'] = dict(x=0, y=0)
            s['cur_map'] = 0
        else:
            s['cur_map'] = new
        s['rolls'] += 1
        rewards = []
        if secrets.randbelow(10000) < r['treasure_basis_points']:
            rewards = grant(role, s, treasure(r))
        if secrets.randbelow(10000) < r['battle_basis_points']:
            from . import nine_sky_battle
            record, reward = nine_sky_battle.encounter(role, s, r, floor=encounter_floor)
            record['rewards'] = grant(role, s, reward) if reward else []
            record['roll'] = s['rolls']
            battles.append(record)
        event = dict(rand_map=new, forward=forward, is_star_double=double,
                     is_enter_next=entered, meet_rand_list=rewards)
        if s['rolls'] % r['palace_every'] == 0:
            s['palace_count'] += 1
            index = s['palace_count']
            s['palaces'][str(index)] = [[0], [0, 0]]
            event['tina_shop'] = palace_data(s, index, r)
        events.append(event)
    return dict(flag=2, free_times=s['free_times'], map_event_list=events,
                local_battles=battles, local_before_snapshot=before_snapshot)


def buy(role, s, data, r, op):
    page, index, n = data.get('buy_type'), data.get('index'), data.get('count')
    f.require(type(page) is int and page in (1, 2) and type(index) is int and
              type(n) is int and 1 <= n <= 1000, '九重天购买参数无效')
    if op == 4:
        f.require(type(data.get('shop_day')) is int and data['shop_day'] == s['shop_day'] and
                  data.get('shop_revision') == s['shop_revision'], '九重商会已刷新，请重新打开商店后兑换')
        rows = s['shop'] if page == 1 else r['credit_shop']
        bought = s['purchases'][str(page)]
    else:
        shop_index = data.get('shop_index')
        f.require(type(shop_index) is int and str(shop_index) in s['palaces'], '天宫已离开或尚未遇见')
        rows = [r['palace_special']] if page == 1 else palace_rows(shop_index, r)
        bought = s['palaces'][str(shop_index)][page - 1]
    f.require(1 <= index <= len(rows), '九重天商品编号无效')
    row = rows[index - 1]
    f.require(bought[index - 1] + n <= row['limit'], '九重天商品限购数量不足')
    credit = 0
    if op == 4 and page == 1:
        selected = data.get('card_list', {})
        f.require(isinstance(selected, dict) and len(selected) <= len(r['card_values']), '天星卡格式无效')
        total = 0
        for value, count in selected.items():
            f.require(type(value) is int and value in r['card_values'] and type(count) is int and
                      1 <= count <= s['cards'].get(str(value), 0), '天星卡不足或面额无效')
            total += value * count
        cost = row['cost'] * n
        f.require(s['stars'] >= max(0, cost - total), '天星不足')
        s['stars'] -= max(0, cost - total)
        # [B] 1:1 residual value, never mint stars from overpayment.
        credit = max(0, total - cost)
        s['credits'] += credit
        for value, count in selected.items():
            s['cards'][str(value)] -= count
    elif op == 4:
        f.require(n == 1 and s['credits'] >= row['cost'], '残星不足或兑换数量无效')
        s['credits'] -= row['cost']
    else:
        f.require(n == 1, '天宫每次购买一份')
        a.spend(role, 'gold_coin' if row['money_type'] == 11 else 'silver_coin', row['cost'])
    bought[index - 1] += n
    typ, tid, count, lv = row['reward']
    rewards = grant(role, s, [typ, tid, count * n, lv])
    return dict(flag=op, shop_type=page, stars=s['stars'], credits=s['credits'],
                return_credits=credit, role_card_list=cards(s),
                buy_data=dict(index=index, count=n, item_list=rewards))


def settle(role, req, now, parse, peers=None):
    r = load_rules()
    s = state(role, now, r)
    f.require(r['enabled'], '九重天尚未开放')
    f.require(role['level'] >= r['min_level'], '九重天等级不足')
    f.require(now >= s['clock'], '九重天时钟已回退，请恢复本地时间')
    op = req['id']
    text = req['data']
    f.require(isinstance(text, str) and len(text) <= 4096 and text.strip().startswith('{')
              and text.strip().endswith('}'), '九重天请求格式无效')
    data = parse(text)
    f.require(type(op) is int and op in range(1, 6) and isinstance(data, dict), '九重天操作无效')
    allowed = {1: set(), 2: {'count', 'index'}, 3: {'buy_type', 'first_send'},
               4: {'buy_type', 'index', 'count', 'card_list', 'shop_day', 'shop_revision'},
               5: {'buy_type', 'index', 'count', 'shop_index'}}[op]
    f.require(set(data) <= allowed, '九重天请求包含无效字段')
    if op == 1:
        f.require(not data and text.replace(' ', '').replace('\n', '').replace('\t', '') == '{}', '九重天进入参数无效')
        result = dict(flag=1, role_sky_data=snapshot(s), const_data=dict(one_rock_money=r['one_rock_money']), top_data=top(role, s, peers))
        # Entry is a state query, not a new encounter. Native flag=1 with
        # tina_shop reopens the previous palace on every visit, even sold out.
        # Keep its purchase ledger; only roll events may open a palace.
    elif op == 2:
        result = roll(role, s, data, now, r)
    elif op == 3:
        page = data.get('buy_type')
        f.require(type(page) is int and page in (1, 2) and type(data.get('first_send', True)) is bool, '九重天商店无效')
        rows = s['shop'] if page == 1 else r['credit_shop']
        result = dict(flag=3, shop_type=page, shop_data=[goods(row) for row in rows],
                      role_buy_list=list(s['purchases'][str(page)]), role_card_list=cards(s))
    else:
        result = buy(role, s, data, r, op)
    result['local_snapshot'] = snapshot(s)
    result['local_cards'] = cards(s)
    result['local_top'] = top(role, s, peers)
    return [summon.event(164, result)]


def market_goods(now):
    """1243 original source is the market during the event, not a tower drop."""
    r = load_rules()
    start, end = period(now, r)
    if not r['enabled']:
        return {}
    return {9137: dict(index=9137, object_type=5, type_id=1243, count=1,
                      name='九重天礼包', buy_price=r['bag_gold'], money_type=11,
                      vip_level=0, order=9137, origin_price=r['bag_gold'],
                      begin_time=start-1, end_time=end, buy_limit_times=0, is_day_limit=0)}


def use_bag(role, req):
    r = load_rules()
    count = req['item_count']
    f.require(req['item_type'] == 1243 and type(count) is int and 1 <= count <= 100,
              '九重天礼包数量无效')
    f.require(req['des_type'] == 1 and req['des_id'] in (0, role['role_id']), '九重天礼包目标无效')
    item = f.lookup(role, 'attachments', req['item_id'])
    f.require(item['attach_type'] == 5 and item['type_id'] == 1243 and item['count'] >= count
              and not item.get('is_lock') and not item.get('owner_id') and not item.get('equip_pos'),
              '九重天礼包不足或不可使用')
    item['count'] -= count
    role['attachments'] = [i for i in role['attachments'] if i is not item or i['count'] > 0]
    # Soul amount [A] from item_name; unspecified peach amount [B].
    gain = a.prizes(role, [[10, 5027, 5 * count, 1], [5, 1001, r['bag_peaches'] * count, 1]])
    return [summon.event(21, dict(result=1, type_id=1243, count=count, attach_list=gain))]
