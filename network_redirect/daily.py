"""3.87 checkinUI wire contract [A]; isolated, configurable reward policy [B]."""
import json
from pathlib import Path
from . import formation, journey, summon
from .protocol import decode

ROOT = Path(__file__).resolve().parents[1]
require = formation.require
HANDLED = {1206, 1347}


def load_rules(path=ROOT / 'server_config/daily_rules.json'):
    r = json.loads(Path(path).read_text())
    require(r.get('schema_version') == 1 and r.get('mode') == 'inferred', '日常配置必须标注 inferred')
    require(isinstance(r.get('revision'), str) and bool(r['revision']), '日常配置版本缺失')
    require(type(r.get('timezone_offset_hours')) is int and -12 <= r['timezone_offset_hours'] <= 14, '日常时区无效')
    tasks = r.get('tasks', [])
    require(isinstance(tasks, list) and [t.get('id') for t in tasks] == list(range(1, 12)), '日常任务必须包含原版九类及封神榜、吃包子来源')
    for t in tasks:
        require(isinstance(t.get('desc'), str) and 0 < len(t['desc']) <= 20, '日常描述无效')
        require(all(type(t.get(k)) is int and 0 < t[k] <= 10000 for k in ('points', 'limit')), '日常积分配置无效')
    boxes = r.get('point_prizes', [])
    require(isinstance(boxes, list) and 1 <= len(boxes) <= 6, '日常宝箱数量无效')
    last = 0
    for b in boxes:
        require(type(b.get('point')) is int and last < b['point'] <= sum(t['limit'] for t in tasks), '日常宝箱门槛无效')
        last = b['point']
        require(isinstance(b.get('prizes'), list) and 1 <= len(b['prizes']) <= 12, '日常奖励列表无效')
        for p in b['prizes']: validate_prize(p)
    require(isinstance(r.get('checkin'), list) and len(r['checkin']) == 7, '原版签到需要七档金额')
    for c in r['checkin']:
        require(all(type(c.get(k)) is int and 0 < c[k] <= 1000000 for k in ('gold_count', 'silver_count')), '签到金额无效')
    bonuses = r.get('checkin_bonus', [])
    require(isinstance(bonuses, list) and 3 <= len(bonuses) <= 30, '累计签到奖励缺失')
    last = 0
    for b in bonuses:
        require(type(b.get('day_index')) is int and last < b['day_index'] <= 10000, '累计签到天数无效')
        last = b['day_index']; validate_prize(b.get('prize'))
    return r


def validate_prize(p):
    require(isinstance(p, list) and len(p) == 4 and all(type(x) is int for x in p), '日常奖励格式无效')
    typ, tid, count, level = p
    require(0 < count <= 1000000 and level == 1 and
            (typ in (11, 12) and tid == 0 or typ == 5 and tid in formation.ITEMS), '日常奖励物品无效')


def day(now, r):
    return (int(now) + r['timezone_offset_hours'] * 3600) // 86400


def week(now, r):
    # Shared by weekly guild/wealth features; daily activity no longer uses this.
    # Unix epoch Thursday; shifting three days aligns week buckets to Monday.
    return (day(now, r) + 3) // 7


def prepare(role, now, r):
    s = role.setdefault('daily', dict(day=day(now, r), points={}, claimed=[], checkin_count=0, bonus_claimed=[]))
    if s['day'] != day(now, r):
        s.update(day=day(now, r), points={}, claimed=[])
    # Migrate weekly saves using only today's earned points. Keep same-day
    # claims to prevent a rules deployment from issuing a second set of prizes.
    s.pop('week', None)
    s['total'] = sum(s['points'].values())
    role.setdefault('checkin_time', 0)
    return s


def record(role, kind, count, now, r):
    """Only called by authoritative settlements, never from a client progress field."""
    require(type(count) is int and count >= 0 and type(kind) is int and 1 <= kind <= len(r['tasks']), '日常累计参数无效')
    s = prepare(role, now, r); t = r['tasks'][kind - 1]; key = str(kind)
    previous = s['points'].get(key, 0)
    s['points'][key] = min(t['limit'], previous + count * t['points'])
    s['total'] += s['points'][key] - previous


def spec(p):
    return dict(object_type=p[0], attach_type=p[1], attach_count=p[2], attach_level=p[3])


def snapshot(role, now, r):
    s = prepare(role, now, r)
    rows = [dict(desc=t['desc'], cur_point=s['points'].get(str(t['id']), 0), point_limit=t['limit']) for t in r['tasks']]
    total = s['total']
    boxes = [dict(point=b['point'], status=3 if i in s['claimed'] else 2 if total >= b['point'] else 1,
                  prize_list=[spec(p) for p in b['prizes']]) for i, b in enumerate(r['point_prizes'], 1)]
    return dict(id=1, point=total, point_data=rows, point_prize=boxes, local_day=s['day'])


def hint(role, now, r):
    return summon.event(198, dict(id=3, local_day=day(now, r),
                                has_prize=any(b['status'] == 2 for b in snapshot(role, now, r)['point_prize'])))


def client_config(r):
    return {3: r['checkin'], 9: [dict(day_index=b['day_index'], prize_content=spec(b['prize'])) for b in r['checkin_bonus']]}


def checkin_data(role, now, r):
    s = prepare(role, now, r)
    # Original showItems indexes this table by day_index, displaying unclaimed bonuses.
    return dict(checkin_day_count=s['checkin_count'], checkin_take_prize=role['checkin_time'],
                checkin_take_bonus={b['day_index']: True for b in r['checkin_bonus']
                                    if b['day_index'] <= s['checkin_count'] and b['day_index'] not in s['bonus_claimed']})


def settle(role, mid, req, now, r, parse):
    s = prepare(role, now, r)
    if mid == 1347:
        op = req['id']; require(op in (1, 2), '日常操作无效')
        if op == 1:
            return [summon.event(198, snapshot(role, now, r))]
        data = parse(req['data']); ident = data.get('prize_id')
        require(type(ident) is int and 1 <= ident <= len(r['point_prizes']), '日常宝箱编号无效')
        box = snapshot(role, now, r)['point_prize'][ident - 1]
        require(box['status'] == 2, '日常积分不足或奖励已领取')
        prizes = [journey.grant(role, p) for p in r['point_prizes'][ident - 1]['prizes']]
        s['claimed'].append(ident)
        return [summon.event(198, dict(id=2, prize_id=ident, status=3, prize_list=prizes,
                point_prize_flag=any(b['status'] == 2 for b in snapshot(role, now, r)['point_prize'])))]
    require(mid == 1206 and req['checkin_type'] in (1, 2, 3), '签到操作无效')
    op = req['checkin_type']; result = 1; prizes = []
    if op == 3:
        if role['checkin_time'] and day(role['checkin_time'], r) == day(now, r):
            result = 2
        else:
            c = r['checkin'][min(s['checkin_count'], 6)]
            prizes = [journey.grant(role, [typ, 0, c[key], 1]) for typ, key in ((11, 'gold_count'), (12, 'silver_count'))]
            s['checkin_count'] += 1; role['checkin_time'] = int(now)
            record(role, 1, 1, now, r)
    elif op == 2:
        ident = req['day_index']
        b = next((b for b in r['checkin_bonus'] if b['day_index'] == ident), None)
        if b is None or ident > s['checkin_count']: result = 3
        elif ident in s['bonus_claimed']: result = 2
        else:
            prizes = [journey.grant(role, b['prize'])]; s['bonus_claimed'].append(ident)
    return [summon.event(54, dict(checkin_type=op, checkin_result=result, checkin_data=checkin_data(role, now, r), prize_list=prizes))]


def track(role, before, mid, req, events, now, r, parse):
    """Compare committed operation outcomes; a query, replay or failed action earns zero."""
    prepare(role, now, r)
    a = role.get('activity', {}); old = before.get('activity', {})
    if old.get('day') != a.get('day'): old = {}
    gains = {}
    if mid == 1026 and req['fight_type'] in (1, 20): gains[2] = 1
    if mid == 1061: gains[2] = req['sweep_count']
    if mid == 1029:
        gains[3] = max(0, a.get('rape_total_refreshes', a.get('rape_refreshes', 0)) - old.get('rape_total_refreshes', old.get('rape_refreshes', 0)))
    if mid in (1026, 1043):
        d, prev = a.get('duty') or {}, old.get('duty') or {}
        if d.get('phase') == 'finished' and prev.get('phase') != 'finished': gains[4] = 1
    if mid == 1026 and req['fight_type'] == 6:
        gains[5] = max(0, sum(a.get(k, 0) - old.get(k, 0) for k in ('party_count', 'party_paid')))
    if mid == 1337 and req['event_type'] in (2, 3):
        for packet in events:
            m, _, d = decode(packet)
            if m == 2998 and d['id'] == 190: gains[6] = len(parse(d['data']).get('prize_list', {}))
    if mid == 1302:
        land, prev = a.get('land', {}), old.get('land', {})
        gains[7] = max(0, land.get('travel_count', 0) - (prev.get('travel_count', 0) if prev.get('day') == land.get('day') else 0))
    if mid == 1030:
        gains[8] = sum(bool(v.get('claimed')) and not old.get('visits', {}).get(k, {}).get('claimed') for k, v in a.get('visits', {}).items())
    if mid == 1026 and req['fight_type'] == 2:
        gains[10] = max(0, a.get('rank_count', 0) - old.get('rank_count', 0))
    if mid == 1040:
        gains[11] = len(set(a.get('feed', {})) - set(old.get('feed', {})))
    for kind, count in gains.items():
        if count: record(role, kind, count, now, r)
    return [hint(role, now, r)] if any(gains.values()) else []
