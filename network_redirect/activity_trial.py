"""诸神试炼: native 3.87 contracts [A], daily five-star boss [user/B]."""
import copy
import json
import secrets
from pathlib import Path

from . import formation, journey, summon
from .protocol import encode

ROOT = Path(__file__).resolve().parents[1]
POOL = tuple(sorted(t for t, b in summon.BASES.items()
                    if 5000 <= t < 6000 and int(b['quality']) == 5))
NAMES = {int(r['type_id']): r['name'] for r in summon.rows('cortege/cortege_name_0.csv')}
require = formation.require


def load_rules(path=ROOT / 'server_config/trial_rules.json'):
    r = json.loads(Path(path).read_text())
    require(r.get('schema_version') == 1 and r.get('mode') == 'inferred'
            and isinstance(r.get('revision'), str) and bool(r['revision']), '试炼配置来源无效')
    for key, low, high in (('daily_attempts', 1, 100), ('cooldown_seconds', 1, 3600),
                           ('boss_hp_multiplier', 1, 100), ('boss_hp_initial_multiplier', 1, 100),
                           ('boss_hp_multiplier_level_step', 1, 100), ('boss_level_cap', 1, 200),
                           ('boss_growth_percent', 100, 200),
                           ('skill_level', 1, 10), ('journey_encounter_percent', 0, 100)):
        require(type(r.get(key)) is int and low <= r[key] <= high, '试炼配置无效：' + key)
    require(r['boss_hp_initial_multiplier'] <= r['boss_hp_multiplier'], '试炼初始血量倍率超过上限')
    require(POOL and all(t in journey.NPCS and t in NAMES for t in POOL), '试炼五星神仙池无效')
    rewards = r.get('rewards')
    require(isinstance(rewards, list) and 1 <= len(rewards) <= 5, '试炼奖励缺失')
    for p in rewards:
        require(isinstance(p, list) and len(p) == 4 and all(type(v) is int for v in p)
                and p[0] == 5 and p[1] in formation.ITEMS and 1 <= p[2] <= 1000
                and p[3] == 1, '试炼奖励无效')
    return r


def prepare(role, now, rules, r=None):
    """Own daily clock: keep earned prizes across the shared activity reset."""
    from .activity import day
    r = r or load_rules()
    s = role.setdefault('activity', {})
    current_day = day(now, rules)
    meta = s.get('trial_meta')
    if meta is None:
        old = s.get('trial')
        old_day = s.get('day') if type(s.get('day')) is int else current_day
        meta = s['trial_meta'] = dict(day=current_day, clock=now,
            type_id=secrets.choice(POOL), spawned=False)
        # Preserve already earned legacy rewards, but retire the generic live NPC.
        if old and old.get('is_dead'):
            old.setdefault('day', old_day)
            old.setdefault('rewards', [[p['object_type'], p['attach_type'], p['attach_count'],
                                       p.get('attach_level', 1)] for p in old.get('prize_list', [])])
            meta['spawned'] = old_day == current_day
        else:
            s['trial'] = None
        if old_day < current_day:
            s.update(trial_count=0, trial_next=0)
    elif current_day > meta['day']:
        boss = s.get('trial')
        if not boss or not boss['is_dead']:
            s['trial'] = None
        meta.update(day=current_day, clock=now, type_id=secrets.choice(POOL), spawned=False)
        s.update(trial_count=0, trial_next=0)
    meta['clock'] = max(now, meta['clock'])
    s.setdefault('trial', None)
    s.setdefault('trial_count', 0)
    s.setdefault('trial_next', 0)
    return s


def checked(role, now, rules, r):
    from .activity import day
    s = prepare(role, now, rules, r)
    require(day(now, rules) == s['trial_meta']['day'] and now >= s['trial_meta']['clock'],
            '试炼时钟已回退，请恢复本地时间')
    return s


def spawn(role, s, r):
    from .activity import prize_spec
    if s['trial'] is None and not s['trial_meta']['spawned']:
        tid = s['trial_meta']['type_id']
        level = max(1, min(role['level'], r['boss_level_cap']))
        cfg = dict(cortege_list=f'{tid}|{level}', skill_level=r['skill_level'])
        _, enemies = journey.fighters(role, cfg)
        unit = enemies[0]
        base = journey.NPCS[tid]
        for stat, column, growth in zip(formation.STATS, formation.BASE_COLUMNS, formation.GROWTH_COLUMNS):
            unit[stat] = max(1, int(float(base[column]) + float(base[growth])
                                   * (level - 1) * r['boss_growth_percent'] / 100))
        multiplier = min(r['boss_hp_multiplier'], r['boss_hp_initial_multiplier']
                         + (level - 1) // r['boss_hp_multiplier_level_step'])
        unit['hp'] *= multiplier
        unit['max_hp'] = unit['hp']
        s['trial'] = dict(type_id=tid, name=NAMES[tid], show_level=level,
            day=s['trial_meta']['day'], hp=unit['hp'], max_hp=unit['hp'],
            is_dead=False, damage=0, unit=unit, config=cfg,
            rewards=copy.deepcopy(r['rewards']), prize_list=[prize_spec(p) for p in r['rewards']],
            revision=r['revision'])
        s['trial_meta']['spawned'] = True
    return s['trial']


def damage_list(role, boss):
    return [dict(name=role['role_name'], damage=boss['damage'])] if boss and boss['damage'] else []


def query(role, req, now, rules):
    from .activity import prizes
    r = load_rules()
    s = checked(role, now, rules, r)
    flag = req['flag']
    require(flag in (1, 2, 3, 4, 6, 7, 9), '试炼操作无效')
    if flag in (3, 4, 7):
        require(False, '诸神试炼好友助战暂未开放，请独自挑战今日首领')
    if flag == 6:
        return [summon.event(75, dict(flag=6, result=1, train_data=dict(friend_list=[])))]
    if flag == 1:
        return [summon.event(75, dict(flag=1, result=5, train_data={}))]
    require(req.get('id', 0) == 0, '试炼目标无效')
    if flag == 9:
        boss = s['trial']
        require(boss is not None and boss['is_dead'], '首领尚未击败或已领奖')
        gain = prizes(role, boss['rewards'])
        s['trial_last_claim'] = dict(day=boss['day'], time=now, type_id=boss['type_id'], rewards=boss['rewards'])
        s['trial'] = None
        return [summon.event(75, dict(flag=9, result=1, train_data=dict(prize=gain)))]
    boss = spawn(role, s, r)
    public = {k: v for k, v in boss.items() if k in
              ('type_id', 'name', 'show_level', 'hp', 'max_hp', 'is_dead', 'prize_list')} if boss else None
    return [summon.event(75, dict(flag=2, result=1 if boss else 2, train_data=dict(
        boss_list=[public] if boss else [], friend_damage_list=damage_list(role, boss),
        have_broad=0, last_train_time=s['trial_next'], train_times=s['trial_count'],
        day_max_train_num=r['daily_attempts'], daily_complete=boss is None)))]


def encounter(role, now, rules):
    """Native random_boss event is a server push, never a client reroll."""
    r = load_rules()
    s = prepare(role, now, rules, r)
    if s['trial'] or s['trial_meta']['spawned'] or now < s['trial_meta']['clock']:
        return []
    if secrets.randbelow(100) >= r['journey_encounter_percent']:
        return []
    boss = spawn(role, s, r)
    return [summon.event(75, dict(flag=5, result=1, train_data=dict(type_id=boss['type_id'])))]


def battle(role, req, now, rules, jrules):
    r = load_rules()
    s = checked(role, now, rules, r)
    boss = s['trial']
    require(boss is not None and not boss['is_dead'], '试炼首领不存在或已击败，请刷新活动')
    require(req.get('des_type') == 8 and req.get('des_id') == boss['type_id']
            and req.get('des_value', 0) == 0, '试炼挑战目标已失效，请刷新活动')
    require(s['trial_count'] < r['daily_attempts'], '今日试炼挑战次数已用完')
    require(now >= s['trial_next'], '试炼挑战正在冷却')
    require(any(1 <= c.get('order', 0) <= 8 for c in role['corteges']), '请先上阵神仙')
    allies, _ = journey.fighters(role, boss['config'])
    enemy = copy.deepcopy(boss['unit'])
    enemy.update(hp=boss['hp'], max_hp=boss['max_hp'])
    result, lineup, actions = journey.battle(role, boss['config'], jrules, units=(allies, [enemy]))
    damage = journey.combat_engine.total_damage(actions)
    remaining = getattr(actions, 'final_hp', {}).get(2, {}).get(1)
    if remaining is None:  # Legacy replay fixtures have no final-HP metadata.
        remaining = max(0, boss['hp'] - damage)
    boss['hp'] = max(0, min(boss['max_hp'], remaining))
    boss['is_dead'] = boss['hp'] == 0
    boss['damage'] += damage
    s['trial_count'] += 1
    s['trial_next'] = now + r['cooldown_seconds']
    s['fight_id'] = s['fight_id'] % 0x7ffffffe + 1
    fid = s['fight_id']
    s['trial_last_battle'] = dict(fight_id=fid, time=now, type_id=boss['type_id'],
        damage=damage, hp=boss['hp'], result=result, attempts=s['trial_count'])
    return journey.combat_engine.event_packets(actions, fid) + [
        encode(1028, dict(fight_id=fid, first_hand=1, des_name=boss['name'],
                         lineup_count=len(lineup), lineup=lineup)),
        encode(1027, dict(fight_id=fid, fight_type=11, final_result=result,
                         fight_round=len(actions), fight_result=actions)),
        summon.event(75, dict(flag=8, result=7 if boss['is_dead'] else 1, train_data=dict(
            prize=[], hp=boss['hp'], train_times=s['trial_count'], last_train_time=s['trial_next'],
            friend_damage_list=damage_list(role, boss)))),
        summon.event(44, dict(fight_id=fid, fight_type=11, **getattr(actions, 'talent', {})))]
