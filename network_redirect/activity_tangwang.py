"""Permanent Tangwang cards: local weighted draws and Monday settlement."""
import copy
import json
from datetime import datetime, timezone, timedelta
from secrets import randbelow
from . import activity as a, formation, summon
from . import activity_seasonal as se

COMBINATIONS = [[1, 2, 3, 4], [1, 2, 5, 6], [7, 8, 1, 2]]
LEGACY_LEVELS = {1: 1, 2: 2, 3: 7, 4: 8, 5: 3, 6: 4, 7: 5, 8: 6, 9: 1, 10: 2}


def load_rules(path=a.ROOT/'server_config/tangwang_rules.json'):
    r = json.loads(path.read_text())
    a.require(r.get('mode') == 'inferred' and r.get('schema_version') == 1, '集卡配置必须标注 inferred')
    a.require(isinstance(r.get('revision'), str) and bool(r['revision']), '集卡版本缺失')
    a.require(r.get('timezone_offset_hours') == 8, '集卡使用北京时间')
    a.require(type(r.get('daily_cards')) is int and 0 <= r['daily_cards'] <= 20, '每日金牌数无效')
    a.require(type(r.get('travel_drop_percent')) is int and 0 <= r['travel_drop_percent'] <= 100, '金牌掉落率无效')
    a.require(r.get('letters') == list('国庆快乐有礼欢度'), '集卡字库无效')
    weights = r.get('letter_weights')
    a.require(isinstance(weights, list) and len(weights) == 8 and
              all(type(w) is int and 0 < w <= 10000 for w in weights), '字牌权重无效')
    pools = r.get('pools')
    a.require(isinstance(pools, list) and [p.get('name') for p in pools] ==
              ['国庆快乐', '国庆有礼', '欢度国庆', '未构成组合'], '集卡奖励池缺失')
    for pool in pools:
        rows = pool.get('rewards')
        a.require(isinstance(rows, list) and 1 <= len(rows) <= 30, '集卡奖励池无效')
        for row in rows:
            p, w = row.get('reward'), row.get('weight')
            a.require(type(w) is int and 0 < w <= 10000, '集卡奖励权重无效')
            a.require(isinstance(p, list) and len(p) == 4 and all(type(v) is int for v in p)
                      and 0 < p[2] <= 1000000 and p[3] == 1 and
                      (p[0] == 5 and p[1] in formation.ITEMS and p[1] != 1094 or
                       p[0] in (11, 12) and p[1] == 0), '集卡奖励无效')
    return r


def draw(values, weights):
    ticket = randbelow(sum(weights))
    for value, weight in zip(values, weights):
        if ticket < weight:
            return copy.deepcopy(value)
        ticket -= weight
    raise AssertionError('Invalid Tangwang weighted pool')


def card(role, level):
    # Native cards are distinct instances, including multiple copies of one letter.
    a.require(type(level) is int and 1 <= level <= 8, '金牌文字无效')
    item = dict(id=formation.new_id(role), attach_type=5, type_id=1094, level=level,
                count=1, equip_order=0, equip_pos=0, is_lock=0)
    role['attachments'].append(item)
    return item


def is_card(item):
    return item['attach_type'] == 5 and item['type_id'] == 1094


def state(role, now, r):
    activity = role.setdefault('activity', {})
    seasonal = se.state(role)
    s = seasonal.get('tangwang')
    today = a.day(now, r)
    if s is None:
        # Record the old last-observed day before other activity migrations advance it.
        legacy_day = max(activity.get('day', -1), seasonal.get('spring', {}).get('day', -1))
        previous = (legacy_day + 3)//7 if legacy_day >= 0 else (today + 3)//7
        s = seasonal['tangwang'] = dict(week=previous, observed_day=legacy_day,
            gift_day=-1, weekly_cards=0, weekly_travel_wins=0, weekly_travel_cards=0,
            exchanges=[0, 0, 0, 0])
        for item in role['attachments']:
            if is_card(item):
                item['level'] = LEGACY_LEVELS.get(item['level'], 1)
        s['migrated'] = True
    today = max(today, s['observed_day'])
    week = (today + 3)//7
    previous = s['week']
    if week > previous:
        count = sum(i['count'] for i in role['attachments'] if is_card(i))
        if count:
            from . import system_mail, welfare
            date = datetime.fromtimestamp((previous*7-3)*86400-8*3600,
                       timezone(timedelta(hours=8))).strftime('%Y-%m-%d')
            delivery = copy.deepcopy(role)
            _, mail = system_mail.deliver(delivery, key=f'tangwang-recycle-{previous}',
                title='唐王集卡诏周刷新·金牌返还',
                body=f'唐王集卡诏常驻开放，每周一北京时间0点刷新。{date}开始的活动周已结束，'
                     f'剩余御制金牌{count}枚（含所有文字及锁定金牌）已全部回收，'
                     f'按1枚金牌兑换1个蟠桃，共返还蟠桃{count}个。请领取附件。'
                     '旧金牌不保留到新一周，本周集卡与兑换进度已重置；此前获得的奖励保留。',
                prizes=[[5, 1001, count, 1]], now=now, rules=welfare.load_rules())
            role['welfare'] = delivery['welfare']
            role['attachments'] = [i for i in role['attachments'] if not is_card(i)]
            s['last_recycle'] = dict(week=previous, cards=count, peaches=count, mail_id=mail['mail_id'])
        s.update(week=week, weekly_cards=0, weekly_travel_wins=0,
                 weekly_travel_cards=0, exchanges=[0, 0, 0, 0])
    s['observed_day'] = today
    return s


def give_random(role, s, r):
    level = draw(list(range(1, 9)), r['letter_weights'])
    card(role, level)
    s['weekly_cards'] += 1
    return a.prize_spec([5, 1094, 1, level])


def travel_drop(role, now, shared):
    if not se.is_open(shared, 'spring_cards', now):
        return []
    r = shared['tangwang_rules']
    s = state(role, now, r)
    s['weekly_travel_wins'] += 1
    if randbelow(100) >= r['travel_drop_percent']:
        return []
    s['weekly_travel_cards'] += 1
    return [give_random(role, s, r)]


def payload(s, r, enabled):
    start = (s['week']*7-3)*86400-8*3600
    return dict(start_time=start-1, end_time=start+7*86400, local_permanent=True,
        local_enabled=enabled, next_weekly_refresh=start+7*86400,
        next_daily_refresh=(s['observed_day']+1)*86400-8*3600,
        daily_gift_pending=enabled and s['gift_day'] < s['observed_day'],
        card_combination=copy.deepcopy(COMBINATIONS), letters=r['letters'],
        letter_weights=r['letter_weights'], daily_cards=r['daily_cards'],
        travel_drop_percent=r['travel_drop_percent'], pools=r['pools'],
        week=s['week'], weekly_cards=s['weekly_cards'], exchanges=copy.deepcopy(s['exchanges']))


def status(role, now, shared):
    r = shared['tangwang_rules']
    s = state(role, now, r)
    enabled = se.is_open(shared, 'spring_cards', now)
    if enabled and s['gift_day'] < s['observed_day']:
        for _ in range(r['daily_cards']):
            give_random(role, s, r)
        s['gift_day'] = s['observed_day']
    return dict(tangwang_info=payload(s, r, enabled))


def settle(role, req, now, shared):
    a.require(se.is_open(shared, 'spring_cards', now), '唐王集卡诏暂未开放')
    r = shared['tangwang_rules']
    s = state(role, now, r)
    ids = [x['id'] for x in req['card_list']]
    a.require(req['count'] == len(ids) == 4 and len(set(ids)) == 4, '请选择四枚不同的金牌')
    cards = [formation.lookup(role, 'attachments', i) for i in ids]
    a.require(all(is_card(c) and c['count'] > 0 and 1 <= c['level'] <= 8 and
                  not c.get('is_lock') and not c.get('owner_id') and not c.get('equip_pos')
                  and not c.get('equip_order') for c in cards), '金牌无效、已锁定或被占用')
    letters = [c['level'] for c in cards]
    index = COMBINATIONS.index(letters) if letters in COMBINATIONS else 3
    rows = r['pools'][index]['rewards']
    reward = draw([x['reward'] for x in rows], [x['weight'] for x in rows])
    for c in cards:
        c['count'] -= 1
        if not c['count']:
            role['attachments'].remove(c)
    s['exchanges'][index] += 1
    return [summon.event(90, dict(prize_list=a.prizes(role, [reward]),
        local_tangwang=payload(s, r, True), pool_index=index+1))]
