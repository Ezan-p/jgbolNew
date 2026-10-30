"""诸神试炼: native 3.87 contracts [A], journey encounters and three-tier bosses [user/B]."""
import copy
import json
import secrets
from pathlib import Path

from . import formation, journey, summon
from . import battle_replay
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
    for key, low, high in (('daily_attempts', 1, 100), ('journey_pity_wins', 1, 1000), ('cooldown_seconds', 1, 3600),
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
    require(type(r.get('max_alive_bosses')) is int and r['max_alive_bosses'] == 3, '试炼留存上限必须为3')
    tiers = r.get('tiers')
    require(isinstance(tiers, list) and len(tiers) == 3 and all(isinstance(x, dict) for x in tiers), '试炼档位无效')
    require([x.get('key') for x in tiers] == ['low', 'medium', 'high'], '试炼档位顺序无效')
    for x in tiers:
        require(isinstance(x.get('name'), str) and bool(x['name']), '试炼档位名称无效')
        for key, cap in [('weight', 100), ('stat_percent', 1000), ('reward_multiplier', 100)]:
            require(type(x.get(key)) is int and 1 <= x[key] <= cap, '试炼档位数值无效')
    require(sum(x['weight'] for x in tiers) == 100 and tiers[0]['weight'] > tiers[1]['weight'] > tiers[2]['weight'], '试炼档位概率无效')
    require(tiers[0]['stat_percent'] >= 100 and tiers[0]['reward_multiplier'] == 1
            and tiers[0]['stat_percent'] < tiers[1]['stat_percent'] < tiers[2]['stat_percent']
            and tiers[0]['reward_multiplier'] < tiers[1]['reward_multiplier'] < tiers[2]['reward_multiplier'], '试炼档位成长无效')
    require(type(r.get('manual_level_step')) is int and 1 <= r['manual_level_step'] <= 100, '密卷等级步长无效')
    require(r.get('manual_pairs') == [[1041 + i * 2, 1042 + i * 2] for i in range(20)], '密卷等级物品表无效')
    require(all(int(formation.ITEMS[t]['sub_type']) == 99 and int(formation.ITEMS[t]['experience_plus']) > 0
                for pair in r['manual_pairs'] for t in pair), '密卷物品无效')
    require([p[1] for p in rewards] == [1041, 1042], '试炼基础密卷奖励无效')
    return r


def prepare(role, now, rules, r=None):
    """UTC+8 rollover expires all bosses/prizes and pity, retaining unique IDs."""
    from .activity import day
    s = role.setdefault('activity', {})
    current_day = day(now, rules)
    old_day = s.get('day') if type(s.get('day')) is int else current_day
    meta = s.setdefault('trial_meta', dict(day=old_day, clock=now))
    if 'trial_bosses' not in s:
        old = s.pop('trial', None)
        s['trial_bosses'] = []
        # Preserve v1/v2 snapshots, including damage and already earned legacy prizes.
        if old and (old.get('unit') or old.get('is_dead')):
            old.setdefault('day', meta['day'])
            old.setdefault('rewards', [[p['object_type'], p['attach_type'], p['attach_count'],
                                       p.get('attach_level', 1)] for p in old.get('prize_list', [])])
            old.update(boss_id=1)
            old.setdefault('tier', 'low')
            old.setdefault('tier_name', '低档')
            s['trial_bosses'].append(old)
        meta['next_id'] = 2 if s['trial_bosses'] else 1
        meta.pop('spawned', None)
        meta.pop('type_id', None)
    if current_day > meta['day']:
        meta['day'] = current_day
        s.update(trial_bosses=[], trial_next=0)
        meta['pity_misses'] = 0
        s.pop('trial_last_battle', None)
        s.pop('trial_last_claim', None)
    # v3 may have carried yesterday's boss into an already-current daily clock.
    s['trial_bosses'] = [b for b in s['trial_bosses'] if b.get('day', meta['day']) >= meta['day']]
    meta['clock'] = max(now, meta.get('clock', now))
    # v3 used one shared counter; initialize per-boss attempts once on migration.
    for boss in s['trial_bosses']:
        boss.setdefault('train_times', 0)
    s.pop('trial_count', None)
    meta.setdefault('pity_misses', 0)
    s.setdefault('trial_next', 0)
    return s


def checked(role, now, rules, r):
    from .activity import day
    s = prepare(role, now, rules, r)
    require(day(now, rules) == s['trial_meta']['day'] and now >= s['trial_meta']['clock'],
            '试炼时钟已回退，请恢复本地时间')
    return s


def spawn(role, s, r):
    """Called only after a successful journey encounter roll."""
    from .activity import prize_spec
    alive = [b for b in s['trial_bosses'] if not b['is_dead']]
    if len(alive) >= r['max_alive_bosses']:
        return None
    tid = secrets.choice([t for t in POOL if t not in {b['type_id'] for b in alive}])
    roll = secrets.randbelow(100)
    for tier in r['tiers']:
        roll -= tier['weight']
        if roll < 0:
            break
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
    for stat in formation.STATS:
        unit[stat] = max(1, unit[stat] * tier['stat_percent'] // 100)
    unit['max_hp'] = unit['hp']
    grade = min(len(r['manual_pairs']) - 1, (max(1, role['level']) - 1) // r['manual_level_step'])
    rewards = [[p[0], r['manual_pairs'][grade][i], p[2] * tier['reward_multiplier'], p[3]]
               for i, p in enumerate(r['rewards'])]
    boss = dict(boss_id=s['trial_meta']['next_id'], type_id=tid, name=NAMES[tid], show_level=level,
        tier=tier['key'], tier_name=tier['name'], reward_role_level=role['level'], manual_grade=grade + 1,
        day=s['trial_meta']['day'], hp=unit['hp'], max_hp=unit['hp'],
        is_dead=False, damage=0, train_times=0, unit=unit, config=cfg,
        rewards=rewards, prize_list=[prize_spec(p) for p in rewards], revision=r['revision'])
    s['trial_meta']['next_id'] += 1
    s['trial_bosses'].append(boss)
    s['trial_meta']['pity_misses'] = 0
    return boss


def damage_list(role, boss):
    return [dict(name=role['role_name'], damage=boss['damage'])] if boss and boss['damage'] else []


def query(role, req, now, rules):
    from .activity import prizes
    r = load_rules()
    s = checked(role, now, rules, r)
    flag = req['flag']
    require(flag in (1, 2, 3, 4, 6, 7, 9), '试炼操作无效')
    if flag in (3, 4, 7):
        require(False, '诸神试炼好友助战暂未开放，请独自挑战试炼首领')
    if flag == 6:
        return [summon.event(75, dict(flag=6, result=1, train_data=dict(friend_list=[])))]
    if flag == 1:
        return [summon.event(75, dict(flag=1, result=5, train_data={}))]
    if flag == 9:
        candidates = [b for b in s['trial_bosses'] if b['boss_id'] == req.get('id')]
        # Unpatched single-boss clients use id=0. Never guess among several bosses.
        if req.get('id', 0) == 0 and len(s['trial_bosses']) == 1:
            candidates = s['trial_bosses']
        require(len(candidates) == 1 and candidates[0]['is_dead'], '首领尚未击败或已领奖')
        boss = candidates[0]
        gain = prizes(role, boss['rewards'])
        s['trial_last_claim'] = dict(day=boss['day'], time=now, boss_id=boss['boss_id'],
                                    type_id=boss['type_id'], rewards=boss['rewards'])
        s['trial_bosses'].remove(boss)
        return [summon.event(75, dict(flag=9, result=1, train_data=dict(prize=gain, boss_id=boss['boss_id'])))]
    require(req.get('id', 0) == 0, '试炼目标无效')
    bosses = sorted(s['trial_bosses'], key=lambda b: (not b['is_dead'], b['boss_id']))
    public = [{k: v for k, v in boss.items() if k in
               ('boss_id', 'type_id', 'name', 'show_level', 'hp', 'max_hp', 'is_dead', 'prize_list',
                'tier', 'tier_name', 'manual_grade', 'train_times')} | {'friend_damage_list': damage_list(role, boss)} for boss in bosses]
    return [summon.event(75, dict(flag=2, result=1 if bosses else 2, train_data=dict(
        boss_list=public, friend_damage_list=damage_list(role, bosses[0] if bosses else None),
        have_broad=0, last_train_time=s['trial_next'], train_times=bosses[0]['train_times'] if bosses else 0,
        day_max_train_num=r['daily_attempts'], no_boss=not bosses,
        expires_at=(s['trial_meta']['day'] + 1) * 86400 - rules['timezone_offset_hours'] * 3600,
        pity_misses=s['trial_meta']['pity_misses'], pity_wins=r['journey_pity_wins'],
        alive_count=sum(not b['is_dead'] for b in bosses), max_alive_bosses=r['max_alive_bosses'])))]


def encounter(role, now, rules):
    """Native random_boss event is a server push, never a client reroll."""
    r = load_rules()
    s = prepare(role, now, rules, r)
    if sum(not b['is_dead'] for b in s['trial_bosses']) >= r['max_alive_bosses'] or now < s['trial_meta']['clock']:
        return []
    if s['trial_meta']['pity_misses'] < r['journey_pity_wins'] - 1:
        if secrets.randbelow(100) >= r['journey_encounter_percent']:
            s['trial_meta']['pity_misses'] += 1
            return []
    boss = spawn(role, s, r)
    return [summon.event(75, dict(flag=5, result=1, train_data=dict(type_id=boss['type_id'],
        boss_id=boss['boss_id'], tier=boss['tier'], tier_name=boss['tier_name'])))]


def battle(role, req, now, rules, jrules):
    r = load_rules()
    s = checked(role, now, rules, r)
    candidates = [b for b in s['trial_bosses'] if not b['is_dead'] and b['type_id'] == req.get('des_id')
                  and (not req.get('des_value', 0) or b['boss_id'] == req['des_value'])]
    boss = candidates[0] if len(candidates) == 1 else None
    require(boss is not None, '试炼首领不存在或已击败，请刷新活动')
    require(req.get('des_type') == 8, '试炼挑战目标已失效，请刷新活动')
    require(boss['train_times'] < r['daily_attempts'], '这只首领的今日挑战次数已用完')
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
    boss['train_times'] += 1
    s['trial_next'] = now + r['cooldown_seconds']
    s['fight_id'] = s['fight_id'] % 0x7ffffffe + 1
    fid = s['fight_id']
    s['trial_last_battle'] = dict(fight_id=fid, time=now, type_id=boss['type_id'],
        boss_id=boss['boss_id'], damage=damage, hp=boss['hp'], result=result, attempts=boss['train_times'])
    return journey.combat_engine.event_packets(actions, fid) + [
        encode(1028, dict(fight_id=fid, first_hand=1, des_name=boss['name'],
                         lineup_count=len(lineup), lineup=lineup)),
        *battle_replay.result_packets(1027, dict(fight_id=fid, fight_type=11, final_result=result,
                         fight_round=len(actions), fight_result=actions)),
        summon.event(75, dict(flag=8, result=7 if boss['is_dead'] else 1, train_data=dict(
            prize=[], boss_id=boss['boss_id'], hp=boss['hp'], train_times=boss['train_times'], last_train_time=s['trial_next'],
            friend_damage_list=damage_list(role, boss)))),
        summon.event(44, dict(fight_id=fid, fight_type=11, **getattr(actions, 'talent', {})))]
