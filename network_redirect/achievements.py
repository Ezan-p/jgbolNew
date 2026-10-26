"""Original 3.87 achievement catalogue [A]; authoritative local settlement [B]."""
import csv
import json
from pathlib import Path
from .protocol import encode

ROOT = Path(__file__).resolve().parents[1]
with (ROOT / 'analysis/configs/achievements_config.csv').open(encoding='utf-8-sig', newline='') as source:
    CATALOG = {int(r['id']): r for r in csv.DictReader(source)}
OPEN = {i: r for i, r in CATALOG.items() if r['is_open(Y/N)'] == 'Y'}


def load_rules(path=ROOT / 'server_config/achievement_rules.json'):
    r = json.loads(Path(path).read_text())
    if (r.get('schema_version') != 1 or r.get('mode') != 'inferred'
            or r.get('timezone_offset_hours') != 8 or r.get('point_formula') != 'additive_percent_floor'
            or r.get('first_category') != 'open_only' or r.get('wire_limit') != 65535):
        raise ValueError('成就服务端配置无效')
    if type(r.get('simulated_board_size')) is not int or r['simulated_board_size'] < 1:
        raise ValueError('模拟榜单容量无效')
    limits = r.get('simulated_array_max_levels')
    if not isinstance(limits, list) or len(limits) != 6 or any(type(v) is not int or v < 1 for v in limits):
        raise ValueError('模拟灵阵等级上限无效')
    return r


def state(role):
    return role.setdefault('achievements', dict(version=1, totals={}, observed={}, receipts={}, days=[], daily={}))


def add(role, ident, amount=1):
    """Internal settlement only. Closed catalogue entries never award points."""
    if type(ident) is not int or ident not in CATALOG or type(amount) is not int or amount < 0:
        raise ValueError('成就编号或进度无效')
    if ident not in OPEN:
        return
    row = OPEN[ident]
    cap = (int(row['max_repeatable_times']) or 65535) if row['repeatable(Y/N)'] == 'Y' else 1
    totals = state(role)['totals']
    totals[str(ident)] = min(cap * int(row['full_progress']), totals.get(str(ident), 0) + amount)


def observe(role, ident, value, source='value'):
    """Lifetime high-water mark, independently keyed by item/companion identity."""
    if value < 0:
        return
    seen = state(role)['observed']; key = f'{ident}:{source}'
    old = seen.get(key, 0)
    if value > old:
        add(role, ident, value - old)
        seen[key] = value


def rows(role):
    totals = state(role)['totals']; result = []
    for ident, cfg in OPEN.items():
        full = int(cfg['full_progress']); total = totals.get(str(ident), 0)
        repeat = cfg['repeatable(Y/N)'] == 'Y'
        cap = (int(cfg['max_repeatable_times']) or 65535) if repeat else 1
        times = min(cap, total // full)
        progress = full if times == cap else total % full
        result.append(dict(id=ident, times=times, progress=min(65535, progress)))
    return result


def finalize(role):
    current = {r['id']: r for r in rows(role)}
    if all(current[i]['times'] for i, r in OPEN.items() if r['category'] == '1'):
        observe(role, 401, 1)
        current = {r['id']: r for r in rows(role)}
    base = rate = 0
    for i, v in current.items():
        points = v['times'] * int(OPEN[i]['plus_point'])
        if OPEN[i]['plus_type(A/R)'] == 'A': base += points
        else: rate += points
    role['tao_point'] = min(2147483647, base * (100 + rate) // 100)


def packets(role, new=0, previous=None):
    entries = rows(role)
    if previous is not None:
        old = {r['id']: r for r in rows(previous)}
        entries = [r for r in entries if r != old.get(r['id'])]
        if not entries and role.get('tao_point', 0) == previous.get('tao_point', 0):
            return []
    # All open entries fit one packet; unlike self updates, the native other-role
    # handler REPLACES its list on every 1066, so never split that list.
    if len(entries) > 255:
        raise ValueError('原版成就列表超过单包255条限制')
    attribute = encode(1032, dict(id=role['role_id'], unit_type=1, attr_count=1,
        attr_list=[dict(type=27, value=role.get('tao_point', 0))]))
    return [attribute, encode(1066, dict(new=new, role_id=role['role_id'], tao_point=role.get('tao_point', 0),
                              achievement_count=len(entries), achievements=entries))]


def login(role, now):
    s = state(role); day = (int(now) + 28800) // 86400
    if day not in s['days']:
        s['days'].append(day)
    for ident in range(402, 410): observe(role, ident, len(s['days']))
    finalize(role)


def daily_add(role, ident, amount, now, source='all'):
    s = state(role); day = (int(now) + 28800) // 86400
    if s['daily'].get('day') != day: s['daily'] = dict(day=day, counts={})
    counts = s['daily']['counts']; key = f'{ident}:{source}'
    counts[key] = counts.get(key, 0) + amount
    # Progress may reset at midnight until earned; completion remains permanent.
    if not any(r['id'] == ident and r['times'] for r in rows(role)):
        s['totals'][str(ident)] = min(int(OPEN[ident]['full_progress']), max(
            (v for k, v in counts.items() if k.startswith(f'{ident}:')), default=0))


def refresh(role, now):
    """Recover only facts still provable from the saved role; no invented history."""
    from . import formation as f, equipment, journey, reborn_stars
    s = state(role)
    day = (int(now) + 28800) // 86400
    if s['daily'].get('day') != day:
        for ident in (422, 423, 446, 447):
            if s['totals'].get(str(ident), 0) < int(OPEN[ident]['full_progress']):
                s['totals'].pop(str(ident), None)
        s['daily'] = dict(day=day, counts={})
    for ident in range(201, 211): observe(role, ident, int(role.get('vip_level', 0) >= ident - 200))
    for ident, lv in ((244, 1), (245, 2), (246, 3), (253, 4)):
        observe(role, ident, int(role.get('reborn_layer', 0) >= lv))
    activity = role.get('activity', {})
    rank = activity.get('rank_order', role.get('top_order', 0))
    for ident, limit in ((102, 5000), (211, 1000), (212, 500), (213, 100), (214, 10), (215, 1)):
        observe(role, ident, int(0 < rank <= limit))
    for ident, limit in ((424, 10), (425, 1)):
        clocks = s.setdefault('rank_since', {})
        key = str(ident)
        if 0 < rank <= limit:
            start = clocks.setdefault(key, int(now))
            observe(role, ident, int(now - start >= 86400))
        else:
            clocks.pop(key, None)
    for ident, limit in zip(range(426, 431), (20, 40, 60, 80, 100)):
        observe(role, ident, int(activity.get('duty_best', 0) >= limit))
    for c in role.get('corteges', []):
        key = str(c['id']); quality = int(f.BASES.get(c['type'], {}).get('quality', 0))
        evolve = c.get('evolve_level', 0); reborn = c.get('reborn_layer', 0)
        if evolve: observe(role, 118, 1)
        if quality == 5:
            observe(role, 319, 1, key)
            for ident, limit in ((240, 20), (241, 30), (242, 40), (243, 50)):
                observe(role, ident, int(evolve >= limit), key)
            for ident in (440, 441): observe(role, ident, int(evolve > 0), key)
        observe(role, 239, int(evolve >= 10), key)
        for ident, limit in ((247, 3), (248, 6), (249, 9)):
            observe(role, ident, int(reborn >= limit), key)
    for item in role.get('attachments', []):
        key = str(item['id']); tid = item['type_id']; lv = item.get('level', 1)
        if tid in reborn_stars.STARS:
            if int(f.ITEMS.get(tid, {}).get('quality', 0)) == 5: observe(role, 484, 1, key)
            observe(role, 485, int(lv >= 10), key)
        if item.get('attach_type', 5) == 6:
            if int(f.SKILLS.get(tid, {}).get('quality', 0)) == 5: observe(role, 318, 1, key)
            for ident, limit in ((414, 5), (415, 7), (416, 10)):
                observe(role, ident, int(lv >= limit), key)
        elif item.get('attach_type', 5) == 5:
            cfg = f.ITEMS.get(tid, {}); kind = int(cfg.get('main_type', 0))
            if tid in equipment.STONES:
                observe(role, 127, 1)
                observe(role, 228 + equipment.STONES[tid], item.get('count', 1) if lv >= 10 else 0, key)
                observe(role, 480 + equipment.STONES[tid], int(lv >= 11), key)
                observe(role, 562 + equipment.STONES[tid], int(lv >= 12), key)
            if kind in (1, 2, 3):
                if int(cfg.get('quality', 0)) == 5: observe(role, 317, item.get('count', 1), key)
                advance = item.get('advance_level', 0)
                observe(role, 122, int(advance >= 1))
                observe(role, 449 + kind, int(advance >= 10), key)
                observe(role, 467 + kind, int(item.get('reborn_bit', 0) > 0 and item.get('cast_level', 0) >= 4), key)
    gates = role.get('journey', {}).get('gates', {})
    elite = sum(g.get('pass_star', 0) > 0 for k, g in gates.items() if k.startswith('2:'))
    for ident in (226, 227, 228): observe(role, ident, elite)
    observe(role, 124, int(gates.get('2:'+str(min(journey.GATES[2])), {}).get('pass_star', 0) > 0))
    for k, g in gates.items():
        if k.startswith('2:'): observe(role, 225, int(g.get('pass_star', 0) >= 3), k)
    if 'journey' in role:
        for mid in journey.MAPS[1]:
            for ident, stars in ((443, 1), (444, 3)):
                observe(role, ident, int(journey.completed(role, 1, mid, stars)), str(mid))
    abyss = max(0, activity.get('abyss', {}).get('boss', 1) - 1)
    observe(role, 471, abyss)
    for ident in range(472, 476): observe(role, ident, abyss)
    home = activity.get('home', {})
    for kind in range(1, 6):
        value = home.get('build', {}).get(str(kind), 0)
        for ident in range(490 + (kind-1)*5, 495 + (kind-1)*5): observe(role, ident, value)
    for kind in range(1, 5):
        value = home.get('train', {}).get(str(kind), {}).get('level', 0)
        for ident in range(515 + (kind-1)*9, 524 + (kind-1)*9): observe(role, ident, value)
        observe(role, 551, value, str(kind))
    if home.get('build'):
        from .activity_home import point
        for ident in range(552, 559): observe(role, ident, point(home))
    for pet in home.get('pets', []):
        observe(role, 476, 1, str(pet['id']))
        for ident, quality in ((250, 2), (251, 3), (252, 4)):
            observe(role, ident, int(pet.get('quality', 0) >= quality))
    finalize(role)


def track(role, before, mid, req, now):
    """Runs inside the role/resource save transaction, after successful settlement.

    Requests alone do not count: each trigger requires a persistent outcome delta.
    Per-object high-water marks prevent recycling/unequipping from farming awards.
    """
    from . import formation as f
    if not before: refresh(role, now); return
    old_items = {x['id']: x for x in before.get('attachments', [])}
    old_corts = {x['id']: x for x in before.get('corteges', [])}
    for x in role.get('attachments', []):
        old = old_items.get(x['id'])
        if not old: continue
        if x.get('attach_type', 5) == 6:
            if x.get('level', 1) > old.get('level', 1) and mid == 1071: add(role, 101)
            if x.get('upgrade_level', 0) > old.get('upgrade_level', 0) and mid == 1076: add(role, 459)
            if x.get('awaken', 0) and not old.get('awaken', 0): observe(role, 479, 1, str(x['id']))
        elif x.get('attach_type', 5) == 5:
            kind = int(f.ITEMS.get(x['type_id'], {}).get('main_type', 0))
            if kind in (1, 2, 3):
                if x.get('star_level', 0) > old.get('star_level', 0): add(role, 254, x['star_level']-old.get('star_level', 0))
                if x.get('reborn_bit', 0) > old.get('reborn_bit', 0): add(role, 467)
    for c in role.get('corteges', []):
        old = old_corts.get(c['id'])
        if old and mid == 1084 and req.get('flag') == 0:
            add(role, 460, max(0, c.get('evolve_level', 0) - old.get('evolve_level', 0)))
        if old and c.get('reborn_layer', 0) > old.get('reborn_layer', 0):
            add(role, 466, c['reborn_layer'] - old.get('reborn_layer', 0))
    def amount(r, tid):
        return sum(i.get('count', 0) for i in r.get('attachments', []) if i.get('attach_type', 5) == 5 and i['type_id'] == tid)
    if mid == 1081:
        peaches = max(0, amount(before, 1001) - amount(role, 1001))
        for ident in range(410, 414): add(role, ident, peaches)
    if mid == 1082 and req.get('confirm') and any(
            c.get('pending_training') and not next((v for v in role['corteges'] if v['id'] == c['id']), {}).get('pending_training')
            for c in before.get('corteges', [])): add(role, 116)
    if mid == 1025 and role.get('corteges') != before.get('corteges'): add(role, 115)
    if mid == 1051:
        tid = req.get('item_type'); used = max(0, amount(before, tid) - amount(role, tid))
        if used:
            # Item identities are recovered from item_config; explicit map below.
            if tid in range(1041, 1049): add(role, 117, used)
            for ident, item in USE_ITEMS.items():
                if tid == item: add(role, ident, used)
    a, b = role.get('activity', {}), before.get('activity', {})
    if mid == 1301:
        donation = role.get('guild', {}).get('donations', 0) - before.get('guild', {}).get('donations', 0)
        if donation >= 100: add(role, 137)
    escort, oldescort = role.get('guild', {}).get('escort', {}), before.get('guild', {}).get('escort', {})
    active, oldactive = escort.get('active'), oldescort.get('active')
    if active and not oldactive and active['book']['book_level'] >= 4: add(role, 128)
    if oldactive and not active and oldactive['book']['book_level'] >= 4 and now >= oldactive['book']['end_time']:
        add(role, 232)
    match, oldmatch = role.get('guild', {}).get('match', {}), before.get('guild', {}).get('match', {})
    if match.get('fights', 0) > oldmatch.get('fights', 0): add(role, 126)
    for key, visit in a.get('visits', {}).items():
        if key == '1' and visit.get('claimed') and not b.get('visits', {}).get(key, {}).get('claimed'):
            reward = visit.get('reward', [])
            if len(reward) >= 2 and reward[0] == 5 and int(f.ITEMS.get(reward[1], {}).get('main_type', 0)) in (1, 2, 3): add(role, 322)
    if mid == 1029 and a.get('rape_refreshes', 0) > b.get('rape_refreshes', 0):
        if any(int(f.SKILLS.get(board['skill_type'], {}).get('quality', 0)) == 5 for board in a.get('rape_boards', [])):
            add(role, 321)
    if role.get('pray_spirit_times', 0) > before.get('pray_spirit_times', 0): add(role, 109)
    if (a.get('duty') or {}).get('phase') == 'finished' and (b.get('duty') or {}).get('phase') != 'finished': add(role, 104)
    if mid == 1026 and req.get('fight_type') == 6 and a.get('fight_id') != b.get('fight_id'): add(role, 105)
    if mid in (1026, 1061):
        oldg = before.get('journey', {}).get('gates', {})
        for key, g in role.get('journey', {}).get('gates', {}).items():
            if key.startswith('1:'):
                delta = g.get('day_count', 0) - (oldg.get(key, {}).get('day_count', 0) if before.get('journey', {}).get('day') == role['journey'].get('day') else 0)
                if delta > 0: daily_add(role, 446, delta, now, key)
    for field, ident in (('energy_item_count', 423), ('strength_item_count', 447)):
        if mid == 1051:
            previous = before.get(field, 0) if before.get('journey', {}).get('day') == role.get('journey', {}).get('day') else 0
            delta = role.get(field, 0) - previous
            if delta > 0: daily_add(role, ident, delta, now)
    refresh(role, now)


# Filled from original item descriptions, rather than guessing network operation IDs.
USE_ITEMS = {111: 1034, 112: 1033, 113: 1032, 114: 1031}


def simulate(role, ident, amount, receipt, now):
    """Explicit administrator simulation for unavailable upstream settlements.

    Same receipt is idempotent across restart; changed payload is rejected. This
    function is deliberately not reachable from any game-client message.
    """
    if ident not in OPEN or type(amount) is not int or amount <= 0 or not isinstance(receipt, str) or not receipt.strip():
        raise ValueError('模拟需要开放成就、正整数进度和唯一结算凭据')
    refresh(role, now)
    s = state(role); payload = [ident, amount]
    if receipt in s['receipts']:
        if s['receipts'][receipt] != payload: raise ValueError('模拟凭据已用于其他结算')
        return False
    if ident in (422, 423, 446, 447): daily_add(role, ident, amount, now)
    else: add(role, ident, amount)
    s['receipts'][receipt] = payload
    s.setdefault('simulation_log', []).append(dict(receipt=receipt, id=ident, amount=amount, time=int(now), source='B'))
    finalize(role)
    return True


def record_events(role, events, now, parse):
    """Consume already validated server results, never client-supplied award claims."""
    from .protocol import decode
    from . import formation as f
    for packet in events:
        mid, _, data = decode(packet)
        if mid == 1027 and data.get('fight_type') == 20:
            if 1 <= data.get('final_result', 0) <= 3: add(role, 456)
            else:
                totals = state(role)['totals']; totals['456'] = totals.get('456', 0) // 5 * 5
        if mid not in (2998, 1301): continue
        event = data['id']; d = parse(data['data'])
        if not isinstance(d, dict): continue
        if mid == 1301:
            if d.get('result', 1) != 1: continue
            if event == 40: add(role, 138)
            if event == 69:
                flag = d.get('flag')
                if flag == 2: add(role, 131, d.get('ten_pick', 1))
                if flag == 10:
                    for ident in (130, 453, 454, 455): add(role, ident)
            continue
        if event == 114:
            from . import summon
            nested = [summon.event(41, v) for k, v in d.items() if isinstance(k, int) and isinstance(v, dict)]
            record_events(role, nested, now, parse)
        if event == 41:
            daily_add(role, 422, 1, now)
            if d.get('pass_one_form'): add(role, 103)
            count = d.get('skill_count', 0)
            if count:
                for ident in (121, 417, 418, 419, 420, 421): add(role, ident, count)
        if event == 77:
            daily_add(role, 422, 1, now)
            if d.get('result') == 0:
                for ident in (121, 417, 418, 419, 420, 421): add(role, ident)
        if event == 43 and d.get('feed_result') == 2: add(role, 108)
        if event == 116 and d.get('flag') == 1 and d.get('result') == 1: add(role, 123)
        if event == 23:
            results = d.get('event_data', {1: d})
            if isinstance(results, dict): results = results.values()
            for result in results:
                tid = result.get('cortege_type')
                if tid and int(f.BASES.get(tid, {}).get('quality', 0)) == 5: add(role, 107)
    finalize(role)


FACT_EVENTS = {
    'tian_yuan': [106], 'revive': [119], 'book_stolen': [120], 'craft_exchange': [125],
    'cross_participation': [134], 'treasure_trip': [139], 'party_lucky': [320],
}


def simulate_fact(role, event, value, receipt, now, rules=None):
    """[B] Substitute missing upstream services with validated semantic facts.

    Rank 0 means unranked; array is {stage, level}; follow/follower are unique
    positive target IDs. Daily duty placements are recorded once per UTC+8 day.
    """
    rules = rules or load_rules()
    if not isinstance(receipt, str) or not receipt.strip(): raise ValueError('模拟凭据缺失')
    if event not in set(FACT_EVENTS) | {'duty_rank', 'party_daily_rank', 'party_week_rank', 'cross_rank',
                                      'follow', 'follower', 'fortune', 'feed_rank', 'spirit_array'}:
        raise ValueError('未知上游模拟事件')
    if event == 'spirit_array':
        if not isinstance(value, dict) or set(value) != {'stage', 'level'} or type(value['stage']) is not int or not 1 <= value['stage'] <= 6:
            raise ValueError('灵阵必须提供1至6阶及等级')
        stage, level = value['stage'], value['level']
        if type(level) is not int or not 1 <= level <= rules['simulated_array_max_levels'][stage-1]: raise ValueError('灵阵模拟等级无效')
    elif type(value) is not int or value < 0 or (event in FACT_EVENTS or event in ('follow', 'follower')) and value == 0:
        raise ValueError('模拟计数/名次/角色编号无效')
    if event == 'fortune' and value not in (323, 324, 325, 326): raise ValueError('禄星结果无效')
    # Validate before modifying a detached role; caller commits the whole batch.
    refresh(role, now); s = state(role); payload = dict(event=event, value=value)
    if receipt in s['receipts']:
        if s['receipts'][receipt] != payload: raise ValueError('模拟凭据已用于其他结算')
        return False
    if event in FACT_EVENTS:
        for ident in FACT_EVENTS[event]: add(role, ident, value)
    elif event == 'fortune': add(role, value)
    elif event in ('follow', 'follower'):
        targets = s.setdefault('simulation_'+event, [])
        if value not in targets: targets.append(value)
        for ident in ((302,303) if event == 'follow' else (304,305)): observe(role, ident, len(targets))
    elif event == 'spirit_array':
        for i, ident in enumerate((461,462,463,464,560,561), 1): observe(role, ident, int(stage >= i))
        if stage == 4: observe(role, 465, int(level == rules['simulated_array_max_levels'][3]))
        if stage == 6: observe(role, 562, int(level == rules['simulated_array_max_levels'][5]))
    else:
        if event == 'cross_rank':
            for ident, limit in ((236,3),(237,20),(238,50)): observe(role, ident, int(0 < value <= limit))
        elif event == 'feed_rank': observe(role, 445, int(0 < value <= rules['simulated_board_size']))
        else:
            base = {'duty_rank':216, 'party_daily_rank':218, 'party_week_rank':220}[event]
            ranked = 0 < value <= rules['simulated_board_size']
            observe(role, base, int(ranked)); observe(role, base+1, int(value == 1))
            if event == 'duty_rank':
                day = (int(now)+28800)//86400
                streak = s.setdefault('simulation_duty_streak', dict(day=-1, count=0))
                if day < streak['day']: raise ValueError('天命结榜时间不能倒退')
                if day == streak['day']:
                    if streak.get('rank') != value: raise ValueError('同一天的天命结榜结果不能重复改写')
                else:
                    streak.update(count=(streak['count']+1 if day==streak['day']+1 else 1) if ranked else 0, day=day, rank=value)
                    for ident in range(431,440):
                        full = int(OPEN[ident]['full_progress'])
                        if s['totals'].get(str(ident),0) < full: s['totals'][str(ident)] = min(full,streak['count'])
    s['receipts'][receipt] = payload
    s.setdefault('simulation_log', []).append(dict(receipt=receipt, **payload, time=int(now), source='B'))
    finalize(role)
    return True
