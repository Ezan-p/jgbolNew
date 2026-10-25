"""Journey: original 3.87 tables/protocol [A], explicit server inference [B].

See docs/旅途模块规则与调试.md. Settlement runs on a detached role; the
backend encodes all replies before committing resources and progress together.
"""
import copy
import json
import math
from pathlib import Path
import secrets

from . import formation, summon, combat, combat_engine
from .protocol import encode

ROOT = Path(__file__).resolve().parents[1]
require = formation.require

def table(name, key):
    return {int(r[key]): {k.split('(')[0]: v for k, v in r.items()} for r in summon.rows(name)}

GATES = {1: table('tollgate_config.csv', 'id'), 2: table('elite/elite_tollgate_config.csv', 'tollgate_id')}
MAPS = {1: table('map_config.csv', 'id'), 2: table('elite/elite_map_config.csv', 'id')}
NPCS = {}
for path in sorted((ROOT / 'analysis/configs/cortege').glob('cortege_base_*.csv')):
    NPCS.update(table('cortege/' + path.name, 'type_id'))
NPCS.update(table('elite/elite_cortege_base.csv', 'type_id'))
FLUSH = table('tollgate_flush_cost.csv', 'flush_count')
SWEEP_FLUSH = table('tollgate_sweep_flush.csv', 'count')
ITEM_PRICE = table('item_buy_price.csv', 'count')
HANDLED = {1018, 1026, 1050, 1058, 1061, 1062, 1201}


def load_rules(path=ROOT / 'server_config/journey_rules.json'):
    r = json.loads(Path(path).read_text())
    require(r.get('schema_version') == 1 and r.get('mode') == 'inferred', '旅途配置须标注 inferred')
    for key, lo, hi in [('timezone_offset_hours', -12, 14), ('strength_recovery_seconds', 1, 86400),
                        ('energy_recovery_seconds', 1, 86400), ('resource_item_daily_limit', 1, 255),
                        ('normal_flush_daily_limit', 0, 10), ('defeat_companion_exp_percent', 0, 100),
                        ('defeat_silver_percent', 0, 100)]:
        require(type(r.get(key)) is int and lo <= r[key] <= hi, '旅途配置无效：' + key)
    b = r.get('battle', {})
    for key, lo, hi in [('max_actions', 16, 255), ('minimum_damage_percent', 1, 100),
                        ('multi_target_limit', 1, 8)]:
        require(type(b.get(key)) is int and lo <= b[key] <= hi, '战斗配置无效：' + key)
    combat.validate_rules(b)
    require(b.get('first_hand') == 'challenger' and b.get('timeout') == 'unresolved'
            and r.get('drop_policy') == 'independent_percent'
            and r.get('sweep_result') == 'historical_best_star'
            and r.get('first_win_extra_exp') == 'all_active_companions', '不支持的旅途结算策略')
    return r


def prepare(role, now, rules):
    from . import vip
    old = json.dumps(role, sort_keys=True)
    state = role.setdefault('journey', dict(gates={}, claimed_maps=[], fight_id=0))
    day = (now + rules['timezone_offset_hours'] * 3600) // 86400
    if state.get('day') != day:
        state['day'] = day
        for g in state['gates'].values():
            g.update(day_count=0, flush_count=0)
        for key in ('elite_fight_count', 'elite_tollgate_flush_count', 'tollgate_flush_count',
                    'sweep_flush_count', 'strength_item_count', 'energy_item_count'):
            role[key] = 0
    role['tollgate_flush_limit'] = vip.limit(role, vip.REFRESH, rules['normal_flush_daily_limit'])
    role['sweep_flush_limit'] = 30  # [A] common_def.const_def
    role['strength_item_limit'] = role['energy_item_limit'] = vip.limit(role, vip.RESOURCE, rules['resource_item_daily_limit'])
    for key in ('last_sweep_time', 'tollgate_flush_time', 'elite_tollgate_flush_time',
                'elite_fight_time', 'strength_item_time', 'energy_item_time'):
        role.setdefault(key, 0)
    role.setdefault('cur_exp', 0)
    role['next_exp'] = int(formation.LEVELS[role['level']]['upgrade_exp'])
    for key, cap in (('strength', 30), ('energy', 15)):
        role.setdefault(key, 0)
        clock = key + '_recovery_at'
        last = state.setdefault(clock, now)
        if role[key] >= cap:
            state[clock] = now
        elif now > last:
            units = (now - last) // rules[key + '_recovery_seconds']
            role[key] = min(cap, role[key] + units)
            state[clock] = now if role[key] >= cap else last + units * rules[key + '_recovery_seconds']
    return old != json.dumps(role, sort_keys=True)


def progress(role, kind, gid):
    return role['journey']['gates'].get(f'{kind}:{gid}', dict(day_count=0, flush_count=0, pass_star=0))


def completed(role, kind, mid, stars=1):
    return all(progress(role, kind, gid)['pass_star'] >= stars
               for gid, g in GATES[kind].items() if int(g['map_id']) == mid)


def unlocked(role, kind, gid):
    cfg = GATES.get(kind, {}).get(gid)
    if cfg is None:
        return False
    mid, pre = int(cfg['map_id']), int(cfg['pre_tollgate'])
    if kind == 2 and not completed(role, 1, mid):
        return False
    if pre:
        return progress(role, kind, pre)['pass_star'] > 0
    previous = int(MAPS[kind][mid]['pre_map'])
    return not previous or completed(role, kind, previous)


def gate_row(role, kind, gid):
    return dict(tollgate_type=kind, map_id=int(GATES[kind][gid]['map_id']), tollgate_id=gid,
                **progress(role, kind, gid))


def snapshots(role):
    rows = [gate_row(role, kind, gid) for kind in (1, 2) for gid in GATES[kind] if unlocked(role, kind, gid)]
    replies = [encode(1020, dict(first_send=i == 0, tollgate_count=len(rows[i:i+128]), tollgate_list=rows[i:i+128]))
               for i in range(0, len(rows), 128)]
    maps = [dict(tollgate_type=1, map_id=mid, pass_map=int(mid in role['journey']['claimed_maps']))
            for mid in MAPS[1]]
    return replies + [encode(1023, dict(map_count=len(maps), map_list=maps))]


def updates(role, old):
    packets, opened = [], []
    for kind in (1, 2):
        for gid in GATES[kind]:
            if unlocked(role, kind, gid) and not unlocked(old, kind, gid):
                opened.append(gate_row(role, kind, gid))
            if unlocked(role, kind, gid) and progress(role, kind, gid) != progress(old, kind, gid):
                row = gate_row(role, kind, gid)
                row['pass_map'] = int(row['map_id'] in role['journey']['claimed_maps'])
                packets.append(encode(1019, row))
    # 1019 also sets last_fight_npc and advances the next gate itself. Sending
    # 1019 for a newly opened zero-star gate makes the victory UI show that
    # next gate's money and skips the actual gate's post-fight dialogue.
    return [encode(1020, dict(first_send=False, tollgate_count=len(opened[i:i+128]),
                             tollgate_list=opened[i:i+128])) for i in range(0, len(opened), 128)] + packets


def get_gate(role, kind, gid):
    require(type(gid) in (int, float) and math.isfinite(gid) and gid == int(gid), '关卡编号无效')
    gid = int(gid)
    require(unlocked(role, kind, gid), '请先通过前置关卡及对应普通地图')
    cfg = GATES[kind][gid]
    require(kind != 2 or role['level'] >= 10, '精英旅途需要角色10级')
    require(role['level'] >= int(cfg.get('require_level', 0)), '角色等级不足')
    return gid, cfg


def day_limit(role, kind, cfg):
    return int(cfg['day_fight_count']) + (2 if kind == 2 and role.get('vip_level', 0) >= 1 else 0)


def check_attempt(role, kind, gid, cfg, count):
    require(role['strength'] >= int(cfg['strenth_consume']) * count, '体力不足，请使用包子或等待恢复')
    require(progress(role, kind, gid)['day_count'] + count <= day_limit(role, kind, cfg), '今日挑战次数不足，请先刷新')
    require(kind != 2 or role['elite_fight_count'] + count <= 30, '今日精英挑战已达30次')
    require(any(1 <= c.get('order', 0) <= 8 for c in role['corteges']), '请先布置出战神仙')


def stars(hp, maximum):
    return 3 if hp * 10 >= maximum * 7 else 2 if hp * 10 >= maximum * 4 else 1


def fighters(role, cfg):
    ours = []
    for c in sorted(role['corteges'], key=lambda c: c.get('order', 0)):
        if not 1 <= c.get('order', 0) <= 8:
            continue
        unit = dict(companion_id=c['id'], type=c['type'], order=c['order'], level=c['level'], evolve=c.get('evolve_level', 0),
                    reborn=c.get('reborn_layer', 0), **{s: max(1, int(c[s])) for s in formation.STATS})
        unit['skills'] = [(i['type_id'], i['level']) for i in role['attachments'] if i['attach_type'] == 6
                          and i.get('equip_order') == c['order'] and i.get('equip_pos', 0) > 0]
        ours.append(unit)
    enemies = []
    for order, token in enumerate(cfg['cortege_list'].split('/'), 1):
        parts = token.split('|')
        tid, level = int(parts[0]), int(parts[1])
        base = NPCS[tid]
        unit = dict(type=tid, order=order, level=level, evolve=0, reborn=0)
        for stat, col, growth in zip(formation.STATS, formation.BASE_COLUMNS, formation.GROWTH_COLUMNS):
            unit[stat] = max(1, int(float(base[col]) + float(base[growth]) * (level - 1)))
        sk = [int(s) for s in parts[2].split('+')] if len(parts) > 2 and parts[2] else [int(base['chushijineng'])]
        unit['skills'] = [(s, int(cfg.get('skill_level', 1))) for s in sk if s in formation.SKILLS]
        enemies.append(unit)
    for u in ours + enemies:
        u['max_hp'] = u['hp']
    return ours, enemies


def battle(role, cfg, rules, *, units=None, slots=8):
    """[B] Server turn simulation; no client-supplied victory or damage trusted."""
    from . import role_profile
    prepared, talent = role_profile.talent_units(role, units if units is not None else fighters(role, cfg),
                                                 int(cfg.get('genius_prob') or 0))
    result, lineup, actions = combat_engine.Battle(role, prepared, rules, slots).run()
    actions.talent = talent
    return result, lineup, actions


def grant(role, spec):
    typ, tid, count, level = spec
    require(count > 0, '奖励数量无效')
    if typ in (11, 12):
        role['gold_coin' if typ == 11 else 'silver_coin'] += count
    elif typ == 5:
        require(tid in formation.ITEMS, '未知奖励物品')
        if level == 1:
            summon.add_item(role, tid, count)
        else:
            role['attachments'].append(dict(id=formation.new_id(role), attach_type=5, type_id=tid, level=level, count=count))
    elif typ == 6:
        require(tid in formation.SKILLS, '未知奖励法术')
        for _ in range(count):
            role['attachments'].append(dict(id=formation.new_id(role), attach_type=6, type_id=tid, level=level,
                                           count=0, equip_order=0, equip_pos=0, effect_value=formation.skill_effect(dict(type_id=tid, level=level))))
    elif typ == 4:
        require(tid in summon.BASES, '未知奖励神仙')
        if any(c['type'] == tid for c in role['corteges']):
            role.setdefault('souls', {})[str(tid)] = role.get('souls', {}).get(str(tid), 0) + summon.CONVERT[int(summon.BASES[tid]['quality'])] * count
        else:
            for _ in range(count):
                role['corteges'].append(summon.companion(role, tid))
    elif typ in (7, 10):
        role.setdefault('souls', {})[str(tid)] = role.get('souls', {}).get(str(tid), 0) + count
    elif typ == 15:
        # Original object_type.animal; attachment level denotes pet quality.
        from . import activity, activity_home, activity_home_pets
        import time
        require(tid in activity_home_pets.BASE and level in (1, 2, 3, 4), '未知灵兽或品质')
        role.setdefault('activity', {})
        home = activity_home.state(role, int(time.time()), activity.load_rules())
        from . import pets
        for _ in range(count):
            pets.add(home, tid, level)
    else:
        raise formation.Rejected('未知奖励类型：' + str(typ))
    return dict(object_type=typ, attach_type=tid, attach_count=count, attach_level=level)


def drops(role, value, map_prize=False):
    result = []
    for token in filter(None, value.split('/')):
        p = list(map(int, token.split('|')))
        typ, tid, count = p[:3]
        level, rate = (1, p[3]) if map_prize else p[3:5]
        if secrets.randbelow(100) < rate:
            result.append(grant(role, (typ, tid, count, level)))
    return result


def experience(role, cfg, win, rules, formation_rules, bonus_exp=0):
    level = role['level']
    gain = int(formation.LEVELS[level]['win_exp' if win else 'lose_exp']) * int(cfg['strenth_consume'])
    role['cur_exp'] += gain
    while role['level'] < max(formation.LEVELS) and role['cur_exp'] >= int(formation.LEVELS[role['level']]['upgrade_exp']):
        role['cur_exp'] -= int(formation.LEVELS[role['level']]['upgrade_exp'])
        role['level'] += 1
    role['next_exp'] = int(formation.LEVELS[role['level']]['upgrade_exp'])
    if role['level'] == max(formation.LEVELS):
        role['cur_exp'] = min(role['cur_exp'], role['next_exp'])
    exp = int(cfg['exp']) * (100 if win else rules['defeat_companion_exp_percent']) // 100 + bonus_exp
    exp_list = {}
    for c in role['corteges']:
        if not c.get('order'):
            continue
        quality = int(summon.BASES[c['type']]['quality'])
        top = min(200, role['level'] * 3) if role['level'] < 80 else 200
        applied = exp if c['level'] < top else 0
        c['cur_exp'] += applied
        while c['level'] < top and c['cur_exp'] >= formation.EXPERIENCE[quality, c['level']]:
            c['cur_exp'] -= formation.EXPERIENCE[quality, c['level']]
            c['level'] += 1
            c['culture_point'] += formation_rules['culture_per_level']
        if c['level'] >= top:
            c['cur_exp'] = 0
        c['next_exp'] = formation.EXPERIENCE.get((quality, c['level']), 0)
        exp_list[c['order']] = applied
    money = int(cfg['money']) * (100 if win else rules['defeat_silver_percent']) // 100
    role['silver_coin'] += money
    return gain, exp_list, money


def attempt(role, kind, gid, cfg, result, now, rules, formation_rules, activity_rules=None):
    state = role['journey']['gates'].setdefault(f'{kind}:{gid}', dict(day_count=0, flush_count=0, pass_star=0))
    role['strength'] -= int(cfg['strenth_consume'])
    state['day_count'] += 1
    if kind == 2:
        role['elite_fight_count'] += 1
        role['elite_fight_time'] = now
    win = 1 <= result <= 3
    prize_events, prize_list = [], []
    bonus_exp = 0
    if win:
        if not state['pass_star'] and cfg['first_win_prize']:
            count, rate = map(int, cfg['first_win_prize'].split('|'))
            if secrets.randbelow(100) < rate:
                bonus_exp = count
        random = drops(role, cfg['first_random_prize'] if not state['pass_star'] and cfg['first_random_prize'] else cfg['random_prize'])
        if activity_rules:
            from .activity_seasonal import travel_drop
            random += travel_drop(role,now,activity_rules)
        if random:
            prize_events.append(summon.event(22, dict(prize_type=1, prize_list=random)))
            prize_list.extend(random)
        if result == 3 and state['pass_star'] < 3:
            bonus = drops(role, cfg['com_win_prize'])
            if bonus:
                prize_events.append(summon.event(22, dict(prize_type=2, prize_list=bonus)))
                prize_list.extend(bonus)
        state['pass_star'] = max(state['pass_star'], result)
    gain, exp_list, money = experience(role, cfg, win, rules, formation_rules, bonus_exp)
    return dict(role_add_exp=gain, exp_list=exp_list, silver_coin=money, send_prize_list=prize_list), prize_events


def resource_item(role, req, now, rules, buy=False):
    tid = req['type_id'] if buy else req['item_type']
    require(tid in (1022, 1023), '仅支持包子、仙丹')
    key = 'strength' if tid == 1022 else 'energy'
    count_key, time_key = key + '_item_count', key + '_item_time'
    require(role[count_key] < role[key + '_item_limit'], '今日使用次数已达上限')
    if buy:
        index = role[count_key] + 1
        price = int(ITEM_PRICE[index]['price'])
        require(role['gold_coin'] >= price, '元宝不足')
        role['gold_coin'] -= price
    else:
        require(req['des_type'] == 1 and req['des_id'] in (0, role['role_id']) and req['item_count'] in (0, 1), '包子使用参数无效')
        item = formation.lookup(role, 'attachments', req['item_id'])
        require(item['attach_type'] == 5 and item['type_id'] == tid and item['count'] >= 1 and not item.get('is_lock'), '物品不足或已锁定')
        item['count'] -= 1
        if not item['count']:
            role['attachments'].remove(item)
    role[key] += int(formation.ITEMS[tid][key + '_plus'])
    role[count_key] += 1
    role[time_key] = now
    return [summon.event(21, dict(result=1, type_id=tid, count=1))]


def settle(role, mid, req, now, rules, formation_rules, activity_rules=None):
    if mid == 1018:
        require(req['flag'] in (0, 1, 2), '地图查询参数无效')
        return snapshots(role)
    if mid in (1051, 1058):
        return resource_item(role, req, now, rules, mid == 1058)
    if mid == 2998:
        require(req['id'] == 3, '旅途事件无效')
        return []  # [A] fightUI sends this only after the replay has finished.
    if mid == 1201:
        mapid = req['id']
        require(req['flag'] == 3 and mapid in MAPS[1], '地图奖励参数无效')
        require(completed(role, 1, mapid, 3), '本地图尚未全部三星')
        require(mapid not in role['journey']['claimed_maps'], '地图奖励已领取')
        prizes = drops(role, MAPS[1][mapid]['pass_map_prize'], True)
        role['journey']['claimed_maps'].append(mapid)
        return [encode(1023, dict(map_count=1, map_list=[dict(tollgate_type=1, map_id=mapid, pass_map=1)])),
                summon.event(22, dict(prize_type=3, prize_list=prizes))]
    if mid == 1062:
        index = role['sweep_flush_count'] + 1
        require(index <= role['sweep_flush_limit'], '今日清除冷却次数已达上限')
        require(role['last_sweep_time'] + 1800 > now, '当前没有扫荡冷却')
        cost = int(SWEEP_FLUSH[index]['gold_cost'])
        require(req['cost_gold'] == cost and role['gold_coin'] >= cost, '扫荡刷新价格无效或元宝不足')
        role['gold_coin'] -= cost
        role['sweep_flush_count'] += 1
        role['last_sweep_time'] = 0
        return [encode(1063, dict(error_code=0, **{k: role[k] for k in ('sweep_flush_limit', 'sweep_flush_count', 'last_sweep_time')}))]
    kind = (1 if req['fight_type'] == 1 else 2 if req['fight_type'] == 20 else 0) if mid == 1026 else req['tollgate_type']
    gid, cfg = get_gate(role, kind, req['des_id'] if mid == 1026 else req['tollgate_id'])
    if mid == 1050:
        state = role['journey']['gates'].setdefault(f'{kind}:{gid}', dict(day_count=0, flush_count=0, pass_star=0))
        require(state['day_count'] > 0, '挑战次数未消耗')
        require(state['flush_count'] < int(cfg['day_flush_count']), '本关今日刷新次数已用完')
        require(kind == 2 or role.get('vip_level', 0) >= 1, '普通关卡刷新需要VIP1')
        if kind == 1:
            require(role['tollgate_flush_count'] < role['tollgate_flush_limit'], '今日刷新总次数已用完')
        cost = 30 if kind == 2 else int(FLUSH[state['flush_count'] + 1]['gold_cost'])
        require(role['gold_coin'] >= cost, '元宝不足')
        role['gold_coin'] -= cost
        state['day_count'] = max(0, state['day_count'] - (day_limit(role, kind, cfg) if kind == 2 else 10))
        state['flush_count'] += 1
        prefix = 'elite_tollgate' if kind == 2 else 'tollgate'
        role[prefix + '_flush_count'] += 1
        role[prefix + '_flush_time'] = now
        # Callback names differ from 1019: these are USED counts, despite the
        # day_fight_count name. The original callback also touches the normal
        # map while in elite mode; restore that cache with a non-resetting list.
        replies = [summon.event(56, dict(tollgate_id=gid, day_fight_count=state['day_count'],
                                        day_flush_count=state['flush_count']))]
        if kind == 2:
            replies.append(encode(1020, dict(first_send=False, tollgate_count=1,
                                             tollgate_list=[gate_row(role, 1, gid)])))
        return replies
    count = req['sweep_count'] if mid == 1061 else 1
    require(1 <= count <= 10, '扫荡次数必须为1至10')
    check_attempt(role, kind, gid, cfg, count)
    if mid == 1061:
        require(role['level'] >= 30 or role.get('vip_level', 0) >= 3, '扫荡需要30级或VIP3')
        require(progress(role, kind, gid)['pass_star'] >= 1, '尚未通关，不能扫荡')
        require(now >= role['last_sweep_time'] + 1800, '扫荡冷却中')
        result = progress(role, kind, gid)['pass_star']
        results = [attempt(role, kind, gid, cfg, result, now, rules, formation_rules, activity_rules)[0] for _ in range(count)]
        role['last_sweep_time'] = now
        return [summon.event(63, results)]
    require(req['des_type'] == 1 and req['des_value'] == 0, '挑战目标参数无效')
    result, lineup, actions = battle(role, cfg, rules)
    outcome, prizes = attempt(role, kind, gid, cfg, result, now, rules, formation_rules, activity_rules)
    role['journey']['fight_id'] = role['journey']['fight_id'] % 0x7ffffffe + 1
    fid, ft = role['journey']['fight_id'], req['fight_type']
    return combat_engine.event_packets(actions, fid) + [encode(1028, dict(fight_id=fid, first_hand=1, des_name='旅途', lineup_count=len(lineup), lineup=lineup)),
            encode(1027, dict(fight_id=fid, fight_type=ft, final_result=result, fight_round=len(actions), fight_result=actions)),
            summon.event(45, dict(fight_id=fid, obj_type=1, exp_plus=outcome['role_add_exp'])),
            summon.event(45, dict(fight_id=fid, obj_type=4, exp_list=outcome['exp_list']))] + prizes + [
            summon.event(44, dict(fight_id=fid, fight_type=ft, **getattr(actions, 'talent', {})))]
