"""天命之战: 3.87 client contracts with user-authorized offline balance. Round
in the save is the NEXT stage; cur_round on the original wire is stages CLEARED.
Ranking contains actual local-account results, never fabricated NPC scores.
"""
import copy
import hashlib
from . import formation, journey, summon, achievements, role_profile, cheer, duty_balance
from . import battle_replay
from .protocol import encode

require = formation.require
FIELDS = (174, 175, 176, 177)  # hp, magic, attack, defence
STATS = ('hp', 'magic', 'gongji', 'fangyu')
PRIZES = summon.rows('duty_topprize_config.csv')
COLUMNS = {4: 'lineup_four', 5: 'lineup_five', 6: 'lineup_six',
           7: 'lineup_seven', 8: 'lineup_eight'}


def day(now, r):
    return (int(now) + r['timezone_offset_hours'] * 3600) // 86400


def identity(role):
    return role.get('register_account', str(role['role_id']))


def alias(role):
    # Existing local saves share role_id=1. Read-only ranking aliases avoid
    # changing their IDs or allowing a peer lookup to resolve to the viewer.
    return 2**40 + int.from_bytes(hashlib.sha256(identity(role).encode()).digest()[:5], 'big')


def group(role):
    return min(8, max(4, int(role['cortege_count'])))


def meta(role):
    return role['activity']['duty_meta']


def checkpoint(d):
    out = {k: copy.deepcopy(d[k]) for k in ('round', 'stars', 'used', 'bonus', 'initial_bonus', 'phase', 'group', 'offers', 'guard_reward') if k in d}
    # A half-run skips already earned rewards, but keeps its saved offers.
    if out['phase'] == 'prize':
        out['phase'] = d.get('after_prize', 'exchange')
    return out


def remember(d):
    ensure_guard_reward(d)
    d.setdefault('checkpoints', {})[str(d['round'])] = checkpoint(d)


def ensure_guard_reward(d):
    # Roll once before displaying the layer, including a legacy in-progress save.
    if d['phase'] == 'fight' and d.get('guard_reward', {}).get('round') != d['round']:
        d['guard_reward'] = duty_balance.guard_reward(d['round'])


def half(d):
    # Retain the former offline half-round formula. Actual snapshots replace
    # the former invented zero-bonus/history-best shortcut.
    target = max(1, (d['round'] - 1) // 2)
    candidates = [int(k) for k in d.get('checkpoints', {}) if int(k) <= target]
    return copy.deepcopy(d['checkpoints'][str(max(candidates))]) if candidates else None


def prepare(role, now, r, peers=None):
    s = role['activity']; today = day(now, r)
    m = s.setdefault('duty_meta', dict(version=1, day=s.get('day', today),
        clock=0, records={}, settled={}, yesterday=None, streak_day=-1, streak=0))
    if today < m['day'] or now < m['clock']:
        return
    d = s.get('duty')
    if d is not None:
        ensure_guard_reward(d)
        d.setdefault('initial_bonus', [0]*4)
        d.setdefault('checkpoints', {})
        d.setdefault('group', group(role))
        if d['phase'] == 'exchange' and 'offers' not in d:
            exchange_or_fight(d)
        # Old saves contain no trustworthy earlier snapshots or victory grades.
        # Preserve their actual totals and pending reward; don't invent history.
        if not d['checkpoints'] and d['phase'] in ('initial', 'fight', 'exchange'):
            remember(d)
        record(role)
    if today > m['day']:
        previous = m['records'].get(str(today-1))
        m['yesterday'] = copy.deepcopy(previous) if previous else None
        # Earned, unclaimed silver and random drops survive exactly once.
        if d:
            grant_pending(role, d)
        s.update(duty=None, duty_runs=0)
        m['day'] = today
    m['clock'] = now
    if peers is not None:
        settle_ranks(role, peers, now, r)


def guard(role, now, r):
    require(role['level'] >= 12, '天命之战需12级')
    m = meta(role)
    require(day(now, r) == m['day'] and now >= m['clock'], '天命时钟已回退，请恢复本地时间')


def record(role):
    s = role['activity']; d = s.get('duty')
    if not d or d['round'] <= 1:
        return
    m = meta(role); key = str(m['day'])
    row = m['records'].get(key)
    # Best single run, not the sum of three attempts or rounds * 3.
    if row is None or (d['stars'], d['round']-1) >= (row['stars'], row['rounds']):
        m['records'][key] = dict(stars=d['stars'], rounds=d['round']-1,
            group=d['group'], half=half(d), bonus=copy.deepcopy(d['bonus']))
    s['duty_best'] = max(s.get('duty_best', 0), d['round']-1)


def boards(role, peers, date):
    people = {identity(p): p for p in (peers or [])}
    people[identity(role)] = role
    result = {g: [] for g in COLUMNS}
    for key, p in people.items():
        m = p.get('activity', {}).get('duty_meta', {})
        rec = m.get('records', {}).get(str(date))
        if not rec or not rec['stars']:
            continue
        result[rec['group']].append(dict(id=alias(p), name=p['role_name'], level=p['level'],
            rounds=rec['rounds'], stars=rec['stars'],
            keep_days=m.get('streak', 0) if m.get('streak_day') == date-1 else 0, _key=key))
    for rows in result.values():
        rows.sort(key=lambda row: (-row['stars'], -row['rounds'], row['_key']))
    return result


def rank(role, peers, date):
    for g, rows in boards(role, peers, date).items():
        for pos, row in enumerate(rows, 1):
            if row['_key'] == identity(role):
                return g, pos
    return group(role), 0


def rank_reward(g, position):
    if not 1 <= position <= len(PRIZES):
        return 0
    raw = PRIZES[position-1][COLUMNS[g]]
    return int(raw.split('|')[2]) if raw else 0


def settle_ranks(role, peers, now, r):
    m = meta(role)
    for date in sorted(map(int, m['records'])):
        if date >= m['day'] or str(date) in m['settled']:
            continue
        g, pos = rank(role, peers, date); amount = rank_reward(g, pos)
        m['settled'][str(date)] = dict(group=g, rank=pos, gold=amount)
        m['streak'] = ((m['streak']+1 if date == m['streak_day']+1 else 1) if amount else 0)
        m['streak_day'] = date
        if amount:
            journey.grant(role, [11, 1, amount, 1])
            achievements.observe(role, 216, 1)
            achievements.observe(role, 217, int(pos == 1))
            for ident in range(431, 440):
                achievements.observe(role, ident, m['streak'])
            if pos <= 10:
                tid = 110 + (3 if pos == 1 else 2 if pos <= 3 else 1 if pos <= 6 else 0)
                # Award period is the settlement date, not the eventual login.
                role_profile.grant_title(role, tid, (date+1)*86400-r['timezone_offset_hours']*3600)


def rank_data(role, peers=None):
    m = meta(role); g, pos = rank(role, peers, m['day'])
    rec = m['records'].get(str(m['day']), {})
    out = {}
    for k, rows in boards(role, peers, m['day']).items():
        out[k] = [{a:b for a,b in row.items() if not a.startswith('_')}
                  for row in rows[:50 if k == 8 else 20]]
    return dict(all_top_list=out, duty_group=g, expect_order=pos,
                max_get_star=rec.get('stars', 0), max_fight_round=rec.get('rounds', 0))


def exchange_or_fight(d):
    available = d['stars']-d['used']
    if available < duty_balance.rules()['bonus_tiers'][0]['star']:
        d.pop('offers', None)
        d['phase'] = 'fight'
    else:
        if 'offers' not in d:
            d['offers'] = duty_balance.offers(available)
        d['phase'] = 'exchange'


def pending(d):
    # Legacy unclaimed silver is not discarded when upgrading a save.
    return ([[12, 0, d['pending_silver'], 1]] if d.get('pending_silver') else []) + d.get('pending_rewards', [])


def grant_pending(role, d):
    for reward in pending(d):
        journey.grant(role, reward)
    d.pop('pending_silver', None)
    d.pop('pending_rewards', None)


def data(role, r, result=None, peers=None):
    s = role['activity']; m = meta(role)
    d = s.get('duty')
    if result is None:
        result = {'initial':1, 'fight':3, 'prize':6, 'exchange':5, 'finished':11}.get((d or {}).get('phase'), 2)
        if not d and m['yesterday'] and m['yesterday'].get('half'):
            result = 12
        if (not d or d['phase'] == 'finished') and s['duty_runs'] >= r['duty_daily_runs']:
            result = 7
    current = d or dict(round=1, stars=0, used=0, bonus=[0]*4, initial_bonus=[0]*4)
    if d:
        ensure_guard_reward(d)
    score = m['records'].get(str(m['day']), {})
    _, pos = rank(role, peers, m['day'])
    ours = sum(1 <= c.get('order', 0) <= 8 for c in role['corteges'])
    plan = duty_balance.stage(current.get('group', group(role)), current['round'])
    out = dict(result=result, cur_round=current['round']-1,
        max_fight_round=score.get('rounds', 0), max_get_star=score.get('stars', 0),
        fight_count=max(0, r['duty_daily_runs']-s['duty_runs']),
        cur_get_star=current['stars'], cur_used_star=current['used'], expect_order=pos,
        last_exchange_rate=r['duty_initial_bonus'],
        plus_list=[dict(zip(FIELDS, current['initial_bonus'])), dict(zip(FIELDS, current['bonus']))],
        lineup_list=[dict(type=plan['guard_types'][i-1], stars=i, vs=[ours, plan['group']]) for i in (1, 2, 3)])
    saved_reward = current.get('guard_reward', {})
    if saved_reward.get('round') == current['round']:
        p = saved_reward['reward']
        out['lineup_list'][saved_reward['difficulty']-1]['reward'] = dict(
            object_type=p[0], attach_type=p[1], attach_count=p[2], attach_level=p[3])
    if d and d['phase'] == 'exchange':
        out['star_exchange'] = copy.deepcopy(d['offers'])
    if d and pending(d):
        out['silver_prize'] = [dict(object_type=p[0], attach_type=p[1], attach_count=p[2], attach_level=p[3]) for p in pending(d)]
    restored = half(d) if d else None
    out.update(revert_begin_round=restored['round'] if restored else 1,
        revert_plus_list=dict(zip(FIELDS, [a+b for a,b in zip(restored['bonus'], restored['initial_bonus'])])) if restored else dict.fromkeys(FIELDS, 0))
    last = m['yesterday'] or {}; h = last.get('half')
    out.update(last_get_star=last.get('stars', 0), last_max_fight_round=last.get('rounds', 0),
        last_half_begin_round=h['round'] if h else 1,
        last_plus_list=dict(zip(FIELDS, [a+b for a,b in zip(h['bonus'], h['initial_bonus'])])) if h else dict.fromkeys(FIELDS, 0))
    return out


def event(role, r, result=None, peers=None):
    return summon.event(19, data(role, r, result, peers))


def start(role, r, restored=None):
    s = role['activity']
    require(s['duty_runs'] < r['duty_daily_runs'], '今日天命之战次数已用完')
    s['duty_runs'] += 1
    d = dict(round=1, stars=0, used=0, bonus=[0]*4, initial_bonus=[0]*4,
             phase='initial', group=group(role), checkpoints={})
    if restored:
        d.update(copy.deepcopy(restored))
        # Skipped-stage rewards were already earned; never grant them twice.
        if d['phase'] == 'prize':
            d['phase'] = 'exchange'
        if d['phase'] == 'exchange':
            exchange_or_fight(d)
    s['duty'] = d
    remember(d)


def update(role, req, now, r, peers=None):
    guard(role, now, r)
    op, idx = req['plus_type'], req['plus_index']; s = role['activity']; d = s.get('duty')
    require(req['flag'] in (0, 1) and op in range(6), '天命操作无效')
    require(req['flag'] == 0 or op == 0, '查询不能携带天命操作')
    if op == 0:
        if req['flag'] == 0 and (d is None or d['phase'] == 'finished'):
            if d is None and meta(role)['yesterday'] and meta(role)['yesterday'].get('half'):
                return [event(role, r, 12, peers)]
            if d and s['duty_runs'] < r['duty_daily_runs']:
                return [event(role, r, 11, peers)]
            if s['duty_runs'] < r['duty_daily_runs']:
                start(role, r)
        return [event(role, r, peers=peers)]
    if op == 5:
        last = meta(role)['yesterday'] or {}
        require(d is None and s['duty_runs'] == 0 and last.get('half') and idx in (0, 1), '昨日半程记录不可用')
        start(role, r, last['half'] if idx else None)
        return [event(role, r, peers=peers)]
    require(d is not None, '请先开始天命之战')
    if op == 4:
        require(d['phase'] == 'finished' and idx in (0, 1), '本轮尚未结束或重开选项无效')
        saved = half(d) if idx else None
        require(not idx or saved is not None, '旧存档缺少半程快照，请重新挑战')
        start(role, r, saved)
    elif op == 1:
        require(d['phase'] == 'initial' and 1 <= idx <= 4, '初始祝福已选择或选项无效')
        d['initial_bonus'][idx-1] += r['duty_initial_bonus']
        d['phase'] = 'fight'; remember(d)
    elif op == 2:
        require(d['phase'] == 'exchange' and 1 <= idx <= len(d['offers']), '尚未到祭魂阶段或选项无效')
        offer = d['offers'][idx-1]
        require(d['stars']-d['used'] >= offer['star'], '战魂不足')
        d['used'] += offer['star']; d['bonus'][FIELDS.index(offer['field'])] += offer['value']
        d.pop('offers'); d['phase'] = 'fight'; remember(d); record(role)
    elif op == 3:
        require(d['phase'] == 'prize' and bool(pending(d)), '暂无可领取奖励')
        grant_pending(role, d)
        d['phase'] = d.pop('after_prize', 'exchange')
        if d['phase'] == 'exchange':
            exchange_or_fight(d)
        remember(d); record(role)
    return [event(role, r, peers=peers)]


def battle(role, req, now, r, jrules, peers=None):
    guard(role, now, r)
    s = role['activity']; d = s.get('duty')
    require(d is not None and d['phase'] == 'fight', '请先完成祝福、领奖或重开')
    require(req['des_type'] in (1, 2, 3) and req['des_id'] == 0 and req['des_value'] == d['round'], '天命关卡已变化，请刷新后重试')
    ensure_guard_reward(d)
    cfg = dict(cortege_list=f"{r['battle_npc']}|{r['battle_level']}")
    plan = duty_balance.stage(d['group'], d['round'])
    units = (journey.fighters(role, cfg)[0], duty_balance.enemies(d['group'], d['round'], req['des_type']))
    require(bool(units[0]), '请先上阵神仙')
    for u in units[0]:
        for stat, bonus, initial in zip(STATS, d['bonus'], d['initial_bonus']):
            u[stat] = u[stat]*(100+bonus+initial)//100
        u['max_hp'] = u['hp']
    result, lineup, actions = journey.battle(role, cfg, jrules, units=units)
    win = 1 <= result <= 3
    s['fight_id'] += 1; fid = s['fight_id']
    material_events = []
    if win:
        from . import activity_seasonal
        materials = [journey.grant(role, p) for p in activity_seasonal.material_specs(r)]
        if materials:
            material_events.append(summon.event(22, dict(prize_type=1, prize_list=materials)))
        d['stars'] += req['des_type']*result
        d['round'] += 1
        rewards = []
        if (d['round']-1) % 3 == 0:
            rewards.append([12, 0, 3*r['duty_silver_per_round'], 1])
            exchange_or_fight(d)
        saved_reward = d.pop('guard_reward')
        if req['des_type'] == saved_reward['difficulty']:
            rewards.append(copy.deepcopy(saved_reward['reward']))
        if rewards:
            d['pending_rewards'] = rewards
            d['after_prize'] = d['phase']; d['phase'] = 'prize'
        remember(d); record(role)
    else:
        d['phase'] = 'finished'; record(role)
    outcome = 8 if win else 11 if half(d) and s['duty_runs'] < r['duty_daily_runs'] else 9
    return journey.combat_engine.event_packets(actions, fid) + [
        encode(1028, dict(fight_id=fid, first_hand=1, des_name=plan['name'], lineup_count=len(lineup), lineup=lineup)),
        *battle_replay.result_packets(1027, dict(fight_id=fid, fight_type=5, final_result=result, fight_round=len(actions), fight_result=actions)),
        event(role, r, outcome, peers), *material_events, summon.event(44, dict(fight_id=fid, fight_type=5))]


def inspection(role, req, peers):
    require(req['des_type'] == 1, '天命榜阵容类型无效')
    target = next((p for p in [role]+list(peers or []) if alias(p) == req['des_id']), None)
    require(target is not None, '天命榜角色不存在')
    chars = [dict(copy.deepcopy(c), type_id=c['type'], max_hp_show=c['hp'], max_magic_show=c['magic'],
                  wuligongji_show=c['gongji'], wulifangyu_show=c['fangyu'])
             for c in target['corteges'] if 1 <= c.get('order', 0) <= 8]
    out = dict(role_id=alias(target), role_name=target['role_name'], level=target['level'],
        vip_level=target.get('vip_level', 0), head_type=target.get('head_type', 1), rank=0,
        title_info={}, animal_info={}, hole_train={}, cortege_list=chars, equip_list=[],
        ext_skill_list={}, ext_star_list={})
    out.update(cheer.inspection(target))
    for i in target['attachments']:
        if not i.get('equip_order') or not i.get('equip_pos'):
            continue
        row = dict(copy.deepcopy(i), order=i['equip_order'])
        if i['attach_type'] == 6 and i['equip_order'] <= 8:
            out['skill_list'].append(row)
        elif i['attach_type'] == 5:
            out['equip_list'].append(row)
    return [summon.event(11, out)]
