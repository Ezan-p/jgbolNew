"""User-authorized offline balance; original NPC snapshots remain immutable."""
import copy
import json
import math
import secrets
from functools import lru_cache
from pathlib import Path
from . import formation, npc_players, activity_rank

ROOT = Path(__file__).resolve().parents[1]
FIELDS = (174, 175, 176, 177)


@lru_cache(maxsize=1)
def rules():
    r = json.loads((ROOT/'server_config/duty_rules.json').read_text())
    require = formation.require
    require(r['schema_version'] == 1 and r['mode'] == 'inferred', '天命平衡配置版本无效')
    require(set(r['power_by_group']) == set(map(str, range(4, 9))), '天命人数分组不全')
    require(2 <= r['reference_stage'] <= 1000 and 1 < r['after_reference_growth'] <= 1.1, '天命成长曲线无效')
    require(0 < r['power_ceiling'] <= 1000000000, '天命战力上限无效')
    for lo, hi in r['power_by_group'].values():
        require(0 < lo < hi < r['power_ceiling'], '天命分组战力无效')
    require(r['difficulty_percent'] == sorted(set(r['difficulty_percent'])) and len(r['difficulty_percent']) == 3
            and 1 <= min(r['difficulty_percent']) < max(r['difficulty_percent']) <= 200, '天命难度倍率无效')
    require([(v['id'], v['candidate_offset']) for v in r['enemy_sets']] == [(0, 0), (1, 1), (2, 2)],
            '天命敌阵须配置三套互异候选偏移')
    tiers = r['bonus_tiers']
    require([t['value'] for t in tiers] == [5, 10, 15, 20] and tiers[0]['star'] >= 9, '天命祭魂档位无效')
    require(all(a['star'] < b['star'] and a['weight'] > b['weight'] > 0 for a, b in zip(tiers, tiers[1:])), '天命祭魂费用或概率无效')
    require(sum(t['weight'] for t in tiers) == 100, '天命祭魂概率和须为100')
    require(sum(t['weight'] for t in r['drops']) == 1000, '天命守卫奖励权重和须为1000')
    for row in r['drops']:
        p = row['reward']
        require(type(row['weight']) is int and row['weight'] > 0, '天命掉落权重无效')
        require(isinstance(p, list) and len(p) == 4 and all(type(v) is int for v in p) and p[2] > 0 and p[3] == 1
                and (p[0] in (11, 12) and p[1] == 0 or p[0] == 5 and p[1] in (1031, 1032, 1033, 1034)
                     and p[1] in formation.ITEMS and p[2] == 1), '天命掉落物品无效')
    return r


def weighted(rows):
    ticket = secrets.randbelow(sum(r['weight'] for r in rows))
    for row in rows:
        ticket -= row['weight']
        if ticket < 0:
            return row


def offers(available):
    tiers = rules()['bonus_tiers']
    result = [dict(field=f, **{k: v for k, v in weighted(tiers).items() if k != 'weight'}) for f in FIELDS]
    # The native page has no skip button. Keep a random attribute affordable;
    # no extra souls are granted and queries never reroll the saved options.
    if available >= tiers[0]['star'] and all(o['star'] > available for o in result):
        result[secrets.randbelow(4)].update(value=tiers[0]['value'], star=tiers[0]['star'])
    return result


def drop():
    return copy.deepcopy(weighted(rules()['drops'])['reward'])


def guard_reward(number):
    return dict(round=number, difficulty=secrets.randbelow(3)+1, reward=drop())


@lru_cache(maxsize=1)
def pool():
    groups = {g: [] for g in range(4, 9)}
    entries = npc_players.catalog()
    # Read each source once; retain only metadata, not all 1,725 full roles.
    for path in sorted({e['source_file'] for e in entries.values()}):
        for key, npc in npc_players.source_file(path).items():
            if key not in entries or npc.get('battle_validation', {}).get('status') == 'replay_limit_observed':
                continue
            active = sorted((c for c in npc['role']['corteges'] if 1 <= c.get('order', 0) <= 8), key=lambda c: c['order'])
            g = len(active)
            if g not in groups:
                continue
            # Use three members of this exact formation as its difficulty
            # portraits. Different type IDs/qualities can depict the same
            # immortal, so deduplicate by character artwork resource.
            guard_types = []
            resources = set()
            for c in active:
                resource = int(formation.BASES[c['type']]['resource'])
                if resource not in resources:
                    guard_types.append(c['type'])
                    resources.add(resource)
            formation.require(len(guard_types) >= 3, '天命NPC阵容缺少三种守卫立绘')
            p = entries[key]['profile']
            groups[g].append(dict(npc_id=key, power=p['role_combat_power'], name=p['role_name'],
                                  type=active[0]['type'], guard_types=tuple(guard_types[:3]),
                                  archetype=p['preferred_archetype'], level=p['level'],
                                  lineup_types=tuple(c['type'] for c in active)))
    for rows in groups.values():
        rows.sort(key=lambda row: (row['power'], row['npc_id']))
        formation.require(bool(rows), '天命NPC分组为空')
    return groups


@lru_cache(maxsize=2048)
def stage(group, number, enemy_set=0):
    formation.require(group in range(4, 9) and number >= 1, '天命关卡分组无效')
    r = rules()
    formation.require(enemy_set in (0, 1, 2), '天命敌阵套号无效')
    lo, hi = r['power_by_group'][str(group)]; end = r['reference_stage']
    exponent = min(number, end)-1
    base = lo * (hi/lo)**(exponent/(end-1))
    # Log-space ceiling avoids overflow even for malformed legacy round values.
    base = round(math.exp(min(math.log(r['power_ceiling']), math.log(base) + max(0, number-end)*math.log(r['after_reference_growth']))))
    rows = pool()[group]
    styles = sorted({row['archetype'] for row in rows})
    style = styles[(number-1) % len(styles)]
    candidates = [row for row in rows if row['archetype'] == style]
    # Set zero preserves the original schedule. Other sets take the next
    # nearest complete formation; all share the same power curve and archetype.
    candidates.sort(key=lambda row: (abs(math.log(row['power']/base)), row['npc_id']))
    formation.require(len(candidates) >= 3, '天命同流派敌阵不足三套')
    offset = r['enemy_sets'][enemy_set]['candidate_offset']
    first = ((number-1)//len(styles)) % 3
    ordered = [candidates[(first+i) % 3] for i in range(3)] + candidates[3:]
    distinct = []
    signatures = set()
    for row in ordered:
        if row['lineup_types'] not in signatures:
            distinct.append(row)
            signatures.add(row['lineup_types'])
        if len(distinct) == 3:
            break
    formation.require(len(distinct) == 3, '天命同流派互异阵容不足三套')
    chosen = distinct[offset]
    return dict(chosen, group=group, stage=number, enemy_set=enemy_set, base_power=base,
                targets=[base*p//100 for p in r['difficulty_percent']])


def choose_enemy_set(previous=None):
    choices = [row['id'] for row in rules()['enemy_sets'] if row['id'] != previous]
    return choices[secrets.randbelow(len(choices))]


@lru_cache(maxsize=128)
def template(key):
    return activity_rank.units(npc_players.get(key)['role'])


def enemies(group, number, difficulty, enemy_set=0):
    formation.require(difficulty in (1, 2, 3), '天命难度无效')
    plan = stage(group, number, enemy_set)
    units = copy.deepcopy(template(plan['npc_id']))
    target = plan['targets'][difficulty-1]
    for unit in units:
        for stat in formation.STATS:
            unit[stat] = max(1, min(2000000000, unit[stat]*target//plan['power']))
        unit['max_hp'] = unit['hp']
    return units
