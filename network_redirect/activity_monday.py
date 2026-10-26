"""天工制物阁 (menu32/mondayUI), distinct from 天机阁 (1227)."""
import copy
import json
import secrets
from pathlib import Path

from . import formation as f, summon, journey

ROOT = Path(__file__).resolve().parents[1]


def load_rules(path=ROOT / 'server_config/monday_rules.json'):
    r = json.loads(Path(path).read_text())
    f.require(r.get('schema_version') == 1 and r.get('mode') == 'inferred'
              and bool(r.get('revision')), '天工规则来源无效')
    f.require(type(r.get('enabled')) is bool, '天工开关无效')
    for key, low, high in [('timezone_offset_hours', -12, 14), ('daily_jade', 1, 10000),
                           ('monday_jade', 1, 10000), ('recycle_silver', 1, 100000)]:
        f.require(type(r.get(key)) is int and low <= r[key] <= high, '天工数值无效：' + key)
    f.require(sorted(r.get('task_rotation', [])) == list(range(1, 10))
              and all(type(x) is int for x in r['task_rotation']), '天工九类任务缺失')
    f.require(isinstance(r.get('slots'), list) and len(r['slots']) == 4, '天工须为原版四格商品')
    for row in r['slots']:
        f.require(type(row.get('cost')) is int and 1 <= row['cost'] <= 100000, '天工价格无效')
        pool = row.get('pool')
        f.require(isinstance(pool, list) and len(pool) >= 2, '天工换货池不足')
        for p in pool:
            f.require(isinstance(p, list) and len(p) == 4 and all(type(v) is int for v in p), '天工奖励格式无效')
            typ, tid, n, lv = p
            f.require(1 <= n <= 100000 and lv == 1 and
                      (typ == 5 and tid in f.ITEMS or typ in (11, 12) and tid == 0), '天工奖励无效')
        f.require(len({tuple(p) for p in pool}) == len(pool), '天工候选商品重复')
    return r


def calendar(now, r):
    day = (now + r['timezone_offset_hours'] * 3600) // 86400
    weekday = (day + 3) % 7 + 1
    # A season starts on Tuesday and ends after the following Monday sale.
    start = day - (weekday - 2) % 7
    return day, weekday, start


def state(role, now, r):
    day, weekday, start = calendar(now, r)
    store = role.setdefault('activity', {})
    s = store.get('monday')
    if s and now < s['clock']:
        return s
    if s is None or start > s['start']:
        if s and s['jade']:
            # Cash-out is a permanent, idempotent mail so offline closure does
            # not silently change currency after response attributes are built.
            from . import system_mail, welfare
            system_mail.deliver(role, key='monday-recycle-' + str(s['start']),
                title='天工制物阁玉圭回收', body='本期开业结束，剩余玉圭已折算为银两。',
                prizes=[[12, 0, s['jade'] * r['recycle_silver'], 1]],
                now=now, rules=welfare.load_rules())
            store = role['activity']
        s = dict(start=start, day=day, clock=now, jade=0, pending=0,
                 goods=[copy.deepcopy(secrets.choice(row['pool'])) for row in r['slots']],
                 random_time=[0]*4, task={})
        store['monday'] = s
    elif day > s['day']:
        task = s['task']
        if task.get('finish_time') and not task.get('recv_time'):
            s['pending'] += task['gain']
        s.update(day=day, task={})
    if not s['task']:
        gain = r['monday_jade'] * (2 if role.get('vip_level', 0) > 0 else 1) if weekday == 1 else r['daily_jade']
        s['task'] = dict(cur_task=r['task_rotation'][day % 9], finish_time=now if weekday == 1 else 0,
                         recv_time=0, gain=gain)
    elif weekday == 1 and not s['task']['recv_time']:
        s['task']['gain'] = r['monday_jade'] * (2 if role.get('vip_level', 0) > 0 else 1)
    s['clock'] = max(now, s['clock'])
    return s


def available(s):
    t = s['task']
    return s['pending'] + (t['gain'] if t['finish_time'] and not t['recv_time'] else 0)


def hint(role, now, r=None):
    r = r or load_rules()
    s = state(role, now, r)
    return int(r['enabled'] and now >= s['clock'] and available(s) > 0)


def snapshot(role, now, r):
    from . import activity as a
    s = state(role, now, r)
    day, weekday, _ = calendar(now, r)
    goods = {i+1: dict(attach_data=a.prize_spec(p), random_time=s['random_time'][i])
             for i, p in enumerate(s['goods'])}
    prices = {i+1: row['cost'] for i, row in enumerate(r['slots'])}
    if weekday == 1:
        prices = {i: dict(consume_count=prices[i], attach_data=g['attach_data']) for i, g in goods.items()}
    return dict(result=1, flag=1, can_rece=hint(role, now, r),
                week_prize_config={weekday: s['task']['gain']},
                exchange_item=a.prize_spec([12, 0, r['recycle_silver'], 1]),
                end_time=(day+1)*86400-r['timezone_offset_hours']*3600-1,
                activity_data=dict(prize_count=s['jade'], can_take_count=available(s),
                                   today_task=copy.deepcopy(s['task']), prize_list=prices, show_list=goods))


def settle(role, mid, req, now):
    r = load_rules(); s = state(role, now, r)
    f.require(r['enabled'] and now >= s['clock'], '天工制物阁未开放或时钟回退')
    day, weekday, _ = calendar(now, r)
    if mid == 1243:
        index = req['index']
        f.require(type(index) is int and 1 <= index <= 4, '天工商品编号无效')
        f.require(weekday != 1, '开业当天不能更换商品')
        old_time = s['random_time'][index-1]
        f.require(not old_time or calendar(old_time, r)[0] < day, '这件物品今日已更换')
        choices = [p for p in r['slots'][index-1]['pool'] if p != s['goods'][index-1]]
        s['goods'][index-1] = copy.deepcopy(secrets.choice(choices))
        s['random_time'][index-1] = now
        from . import activity as a
        # 142 uses common_op_result.success=0; 112 instead checks result=1.
        return [summon.event(142, dict(result=0, index=index, attach_data=dict(
            attach_data=a.prize_spec(s['goods'][index-1]), random_time=now)))]
    flag, level, op = (req[k] for k in ('flag', 'level', 'op_type'))
    f.require(all(type(x) is int for x in (flag, level, op)) and op == 0 and flag in (1, 2, 3), '天工请求无效')
    if flag == 1:
        f.require(level == 0, '天工查询参数无效')
        return [summon.event(112, snapshot(role, now, r))]
    if flag == 2:
        f.require(level == 0 and available(s) > 0, '尚无可领取的玉圭')
        # VIP purchased during Monday takes effect before the free gift is claimed.
        if weekday == 1 and not s['task']['recv_time']:
            s['task']['gain'] = r['monday_jade'] * (2 if role.get('vip_level', 0) > 0 else 1)
        amount = available(s)
        s['jade'] += amount; s['pending'] = 0
        if s['task']['finish_time']:
            s['task']['recv_time'] = now
        data = snapshot(role, now, r); data.update(flag=2, add_count=amount)
        return [summon.event(112, data)]
    f.require(weekday == 1, '天工制物阁仅周一开放兑换')
    f.require(1 <= level <= 4, '天工商品编号无效')
    cost = r['slots'][level-1]['cost']
    f.require(s['jade'] >= cost, '玉圭不足')
    s['jade'] -= cost
    prize = journey.grant(role, s['goods'][level-1])
    return [summon.event(112, dict(result=1, flag=3, can_rece=hint(role, now, r),
                                   left_count=s['jade'], attach_data=prize))]


def track(role, before, mid, req, now):
    """Only committed gameplay deltas complete tasks, never arbitrary queries."""
    if not before or not mid:
        return []
    r = load_rules()
    if not r['enabled']:
        return []
    s = state(role, now, r)
    if now < s['clock']:
        return []
    t = s['task']
    if calendar(now, r)[1] != 1 and not t['finish_time']:
        a, b = role.get('activity', {}), before.get('activity', {})
        kind = t['cur_task']; done = False
        if kind in (1, 2):
            key = 'strength' if kind == 1 else 'energy'
            done = role.get(key, 0) < before.get(key, 0)
            # Recovery or a level-up can offset the same request's expenditure.
            # Confirm the consuming operation via its committed fight record.
            if kind == 1:
                j, oldj = role.get('journey', {}), before.get('journey', {})
                done |= (mid == 1026 and req.get('fight_type') in (1, 20)
                         and j.get('fight_id', 0) > oldj.get('fight_id', 0))
                done |= mid == 1061 and j.get('gates') != oldj.get('gates')
                u, oldu = a.get('undergo', {}), b.get('undergo', {})
                done |= (mid == 1349 and req.get('id') == 4 and u.get('count', 0) > 0
                         and u.get('count') != oldu.get('count')
                         and a.get('fight_id', 0) > b.get('fight_id', 0))
            else:
                done |= ((mid == 1026 and req.get('fight_type') in (2, 3, 12) or mid == 1072)
                         and a.get('fight_id', 0) > b.get('fight_id', 0))
        elif kind == 3:
            done = mid == 1026 and req.get('fight_type') == 5 and a.get('duty') != b.get('duty')
        elif kind == 4:
            done = (mid == 1072 or mid == 1026 and req.get('fight_type') in (3, 12)) and a.get('fight_id') != b.get('fight_id')
        elif kind == 5:
            done = mid == 1029 and a.get('rape_total_refreshes', 0) > b.get('rape_total_refreshes', 0)
        elif kind == 6:
            done = mid == 1081 and any(c.get('pending_training') and not next(
                (v for v in before.get('corteges', []) if v['id'] == c['id']), {}).get('pending_training')
                for c in role.get('corteges', []))
        elif kind == 7:
            done = mid == 1030 and req.get('op_type') == 1 and a.get('visits') != b.get('visits')
        elif kind == 8:
            done = a.get('convert_total', 0) > b.get('convert_total', 0)
        elif kind == 9:
            done = mid in (1026, 1061) and role.get('journey') != before.get('journey') and (
                mid == 1061 or req.get('fight_type') in (1, 20))
        if done:
            t['finish_time'] = now
    # Native event112 refreshes flag21 when opening the activity; bootstrap also
    # publishes it. Keep unrelated gameplay's response/event ordering intact.
    return []
