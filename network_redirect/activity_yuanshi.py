"""两周年 / 元始祈愿: 3.87 contracts [A], missing server economy [B]."""
import json
import secrets
from pathlib import Path

from . import activity as a, formation as f, summon

ROOT = Path(__file__).resolve().parents[1]


def load_rules(path=ROOT / 'server_config/yuanshi_rules.json'):
    r = json.loads(Path(path).read_text())
    f.require(r.get('schema_version') == 1 and r.get('mode') == 'inferred'
              and isinstance(r.get('revision'), str) and bool(r['revision']), '两周年配置来源无效')
    f.require(type(r.get('enabled')) is bool, '两周年开放开关无效')
    f.require(type(r.get('timezone_offset_hours')) is int and
              -12 <= r['timezone_offset_hours'] <= 14, '两周年时区无效')
    for key, upper in [('period_days', 365), ('daily_free', 100),
                       ('progress_per_wish', 100), ('souls_per_wish', 100),
                       ('offering_gold', 1000000), ('bag_gold', 1000000),
                       ('bag_daily_limit', 100), ('gold_per_rmb', 1000)]:
        f.require(type(r.get(key)) is int and 1 <= r[key] <= upper, '两周年数值无效：' + key)
    f.require(r.get('activation_rmb') == [0, 30, 30, 50, 50], '原版五礼包门槛须为任意/30/30/50/50元')
    pool = r.get('wish_pool')
    f.require(isinstance(pool, list) and len(pool) == 5, '祈愿需要五类奖励')
    identities = set()
    for row in pool:
        f.require(isinstance(row, dict) and type(row.get('weight')) is int
                  and 1 <= row['weight'] <= 1000000, '祈愿奖励权重无效')
        p = row.get('reward')
        f.require(isinstance(p, list) and len(p) == 4 and all(type(v) is int for v in p), '祈愿奖励格式无效')
        typ, tid, n, lv = p
        f.require((typ, tid) in {(12, 0), (5, 1022), (5, 1023), (5, 1032), (5, 1031)}
                  and 1 <= n <= 100000 and lv == 1, '祈愿奖励无效')
        identities.add((typ, tid))
    f.require(len(identities) == 5, '祈愿奖励种类重复或缺失')
    gifts = r.get('gifts')
    f.require(isinstance(gifts, list) and len(gifts) == 5, '原版需要五个礼包')
    for rows in gifts:
        f.require(isinstance(rows, list) and 1 <= len(rows) <= 10, '礼包奖励缺失')
        for p in rows:
            f.require(isinstance(p, list) and len(p) == 4 and all(type(v) is int for v in p), '礼包格式无效')
            typ, tid, n, lv = p
            f.require(1 <= n <= 100000 and lv == 1 and
                      (typ in (11, 12) and tid == 0 or typ == 5 and tid in f.ITEMS
                       or typ == 10 and tid in f.BASES), '礼包奖励无效')
    return r


def period(now, r):
    duration = r['period_days'] * 86400
    anchor = 4 * 86400 - r['timezone_offset_hours'] * 3600
    start = (now - anchor) // duration * duration + anchor
    return start, start + duration


def client_config(now, r=None):
    r = r or load_rules()
    start, end = period(now, r)
    # end_time remains a wire-compatible cycle deadline, never an activity expiry.
    return dict(begin_time=start if r['enabled'] else 0, end_time=end if r['enabled'] else 0,
                permanent=r['enabled'], refresh_time=end if r['enabled'] else 0)


def clear_offerings(role):
    """Extra wishes expire with the cycle, including locked stacks/pending mail."""
    role['attachments'] = [i for i in role.get('attachments', [])
                           if not (i['attach_type'] == 5 and i['type_id'] == 1807)]
    for mail in role.get('welfare', {}).get('mails', {}).values():
        if mail['claimed']:
            continue
        prizes = mail['prizes']
        mail['prizes'] = [p for p in prizes if not (p[0] == 5 and p[1] == 1807)]
        if len(prizes) != len(mail['prizes']):
            mail['claimed'] = not mail['prizes']
            mail['mail_body'] += '\n元始祈愿本期已刷新，未领取的祈愿供品已清空。'


def state(role, now, r):
    start, end = period(now, r)
    day = a.day(now, r)
    activity = role.setdefault('activity', {})
    s = activity.get('yuanshi')
    if s is None or now >= s['clock'] and start > s['start']:
        if s is not None:
            clear_offerings(role)
        s = dict(start=start, end=end, clock=now, day=day, free=r['daily_free'],
                 progress=0, claimed=False, wishes=0, wish_days=0, wished_today=False,
                 offering_stock=0, bag_bought=0, charge_gold=0, activated=[],
                 gift_counts=[], entitlement_day=-1, activation_day=-1)
        activity['yuanshi'] = s
    if now >= s['clock'] and start == s['start']:
        # Shorten legacy 28-day saves in the same fortnight without wiping
        # current progress. The next boundary performs the normal full reset.
        s['end'] = end
    if now >= s['clock'] and day > s['day']:
        # Only enrolled days count; no gifts or free attempts accrue while absent.
        s['offering_stock'] += day - s['day'] - int(s['wished_today'])
        s.update(day=day, free=r['daily_free'], wished_today=False, bag_bought=0, charge_gold=0)
    s['clock'] = max(now, s['clock'])
    return s


def guard(s, now, r):
    f.require(r['enabled'] and s['start'] <= now < s['end'], '两周年活动尚未开放或已经结束')
    f.require(now >= s['clock'], '两周年时钟已回退，请恢复本地时间')


def snapshot(s, r):
    return dict(flag=0, cur_progress=s['progress'], free_times=s['free'],
                wish_times=s['wish_days'], gift_list=list(s['gift_counts']),
                gift_config=[dict(prize_list=[a.prize_spec(p) for p in rows]) for rows in r['gifts']],
                is_today_charge=s['activation_day'] == s['day'], claimed=s['claimed'],
                begin_time=s['start'], end_time=s['end'], permanent=True, refresh_time=s['end'])


def shop(s, r):
    return [dict(a.prize_spec([5, 1807, 1, 1]), need_gold=r['offering_gold'], buy_times=s['offering_stock']),
            dict(a.prize_spec([5, 1808, 1, 1]), need_gold=r['bag_gold'],
                 buy_times=r['bag_daily_limit'] - s['bag_bought'])]


def update(role, now):
    r = load_rules()
    if not r['enabled']:
        return summon.event(80, {})
    return summon.event(80, dict(local_yuanshi=snapshot(state(role, now, r), r)))


def record_charge(role, amount, now):
    r = load_rules()
    if not r['enabled'] or amount <= 0:
        return
    s = state(role, now, r)
    guard(s, now, r)
    s['charge_gold'] += amount
    if s['entitlement_day'] != s['day']:
        s['gift_counts'] = [n + 1 for n in s['gift_counts']]
        s['entitlement_day'] = s['day']
    index = len(s['activated'])
    if index < 5 and s['activation_day'] != s['day'] and s['charge_gold'] >= r['activation_rmb'][index] * r['gold_per_rmb']:
        s['activated'].append(s['day'])
        s['gift_counts'].append(1)
        s['activation_day'] = s['day']


def grant_yuanshi(role, count=1):
    """Honor the box's 2x level, including stats/innate spell via formation.prepare."""
    rewards = []
    for _ in range(count):
        if any(c['type'] == 5046 for c in role['corteges']):
            # [B] Duplicate converts to a full synthesis cost, never another copy.
            rewards.extend(a.prizes(role, [[10, 5046, 40, 1]]))
        else:
            level = min(role['level'] * 2, max(lv for q, lv in f.EXPERIENCE if q == 5))
            c = summon.companion(role, 5046)
            c.update(level=level, cur_exp=0)
            role['corteges'].append(c)
            rewards.append(a.prize_spec([4, 5046, 1, level]))
    return rewards


def use_bag(role, req):
    n = req['item_count']
    f.require(req['item_type'] == 1808 and type(n) is int and 1 <= n <= 100, '元始福袋数量无效')
    f.require(req['des_type'] == 1 and req['des_id'] in (0, role['role_id']), '元始福袋目标无效')
    item = f.lookup(role, 'attachments', req['item_id'])
    f.require(item['attach_type'] == 5 and item['type_id'] == 1808 and item['count'] >= n
              and not item.get('is_lock') and not item.get('owner_id') and not item.get('equip_pos'), '福袋不足或不可使用')
    # Debit the selected stack, not a different same-type stack.
    item['count'] -= n
    role['attachments'] = [i for i in role['attachments'] if i is not item or i['count'] > 0]
    return [summon.event(21, dict(result=1, type_id=1808, count=n, attach_list=grant_yuanshi(role, n)))]


def draw_wish(r):
    """One server-side reward per unfinished wish; weights are inferred [B]."""
    pick = secrets.randbelow(sum(row['weight'] for row in r['wish_pool']))
    for row in r['wish_pool']:
        if pick < row['weight']:
            return row['reward']
        pick -= row['weight']
    raise AssertionError('unreachable weighted wish')


def settle(role, req, now):
    r = load_rules()
    s = state(role, now, r)
    guard(s, now, r)
    flag, index = req['flag'], req['index']
    f.require(type(flag) is int and flag in range(5) and type(index) is int, '两周年操作无效')
    f.require(index == 0 if flag in (0, 2, 3) else 1 <= index <= (5 if flag == 1 else 2), '两周年编号无效')
    gain = []
    if flag == 2:
        if s['progress'] == 100 and not s['claimed']:
            # Native getChar sends the same flag/index as pray. Claim is free.
            gain = grant_yuanshi(role)
            s['claimed'] = True
        else:
            if s['free']:
                s['free'] -= 1
            else:
                a.consume(role, 1807, 1)
            if not s['wished_today']:
                s['wish_days'] += 1
            s['wished_today'] = True
            s['wishes'] += 1
            if s['claimed']:
                gain = a.prizes(role, [[10, 5046, r['souls_per_wish'], 1]])
            else:
                # Includes the wish that reaches 100%; claiming is a separate free action.
                gain = a.prizes(role, [draw_wish(r)])
                s['progress'] = min(100, s['progress'] + r['progress_per_wish'])
    elif flag == 1:
        f.require(index <= len(s['gift_counts']) and s['gift_counts'][index - 1] > 0, '礼包未激活或已领取')
        # One click settles all accumulated entitlements for this gift.
        n = s['gift_counts'][index - 1]
        gain = a.prizes(role, [[typ, tid, count * n, lv] for typ, tid, count, lv in r['gifts'][index - 1]])
        s['gift_counts'][index - 1] = 0
    elif flag == 4:
        goods = shop(s, r)[index - 1]
        f.require(goods['buy_times'] > 0, '可购买数量不足')
        a.spend(role, 'gold_coin', goods['need_gold'])
        gain = a.prizes(role, [[5, goods['attach_type'], 1, 1]])
        if index == 1:
            s['offering_stock'] -= 1
        else:
            s['bag_bought'] += 1
    data = snapshot(s, r)
    data.update(flag=flag, prize_list=gain)
    if flag in (3, 4):
        data.update(shop_config=shop(s, r), shop_list=gain)
    return [summon.event(179, data)]
