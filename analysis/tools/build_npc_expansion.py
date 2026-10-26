#!/usr/bin/env python3
"""Seeded five-star-heavy expansion; leaves V1 artifacts and live accounts intact."""
import argparse
from collections import Counter
import copy
import csv
import hashlib
import json
import math
from pathlib import Path
import random
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools import build_npc_catalog as base

CONFIG_PATH = ROOT / 'server_config/npc_expansion_rules.json'
CONFIG = json.loads(CONFIG_PATH.read_text())
V1 = ROOT / 'analysis/npc_design/v1'
POOLS = {q: sorted(t for t, r in base.f.BASES.items() if base.quality(t) == q
                   and 3000 <= t < 6000 and int(r['base_type_id']) == t) for q in (3, 4, 5)}
RANGES = {(int(r['role_level']), r['tier']): {k: int(v) if v else None for k, v in r.items()
           if k in ('minimum', 'maximum', 'sample_min', 'sample_max')}
          for r in csv.DictReader((ROOT / CONFIG['tier_ranges']).open())}
FATE_PARTNERS = {}
for row in base.f.FATES:
    if row['tartege_type[4-cortege/5-equip/6-skill]'] == '4':
        FATE_PARTNERS.setdefault(int(row['cortege_type[effected_cortege]']), set()).update(
            map(int, row['target_object_type[1/2/3]'].split('/')))


def seed_for(level, tier, variant, attempt):
    value = f"{CONFIG['base_seed']}:{level}:{tier}:{variant}:{attempt}"
    return int.from_bytes(hashlib.sha256(value.encode()).digest()[:8], 'big')


def draw(rng, quality, used, style, *, eligible=False):
    candidates = [t for t in POOLS[quality] if t not in used and (not eligible or t in base.reborn.CORTS)]
    if not candidates:
        raise ValueError('No legal unique candidate')
    column = {'attack': 'base_gongji_plus', 'magic': 'base_maxmagic_plus', 'endurance': 'base_fangyu_plus'}[style]
    peak = max(float(base.f.BASES[t][column]) for t in candidates)
    preferred = set(base.pool(style, quality))
    weights = []
    for t in candidates:
        linked = any(t in FATE_PARTNERS.get(u, set()) or u in FATE_PARTNERS.get(t, set()) for u in used)
        weights.append(1 + CONFIG['growth_weight_factor'] * float(base.f.BASES[t][column]) / peak
                       + CONFIG['preferred_candidate_weight'] * (t in preferred)
                       + CONFIG['fate_candidate_weight'] * linked)
    return rng.choices(candidates, weights=weights, k=1)[0]


def signature(npc):
    return tuple(sorted(c['type'] for c in npc['role']['corteges'] if c['order']))


def random_equipment(role, rng):
    for item in role['attachments']:
        cfg = base.f.ITEMS.get(item['type_id'], {})
        if item['attach_type'] != 5 or int(cfg.get('main_type', 0)) not in (1, 2, 3):
            continue
        c = next(c for c in role['corteges'] if c['order'] == item['equip_order'])
        fates = {int(t) for r in base.f.FATES if int(r['cortege_type[effected_cortege]']) == c['type']
                 and r['tartege_type[4-cortege/5-equip/6-skill]'] == '5'
                 for t in r['target_object_type[1/2/3]'].split('/')}
        candidates = sorted(t for t, r in base.f.ITEMS.items()
                            if r['quality'] == cfg['quality'] and r['main_type'] == cfg['main_type'])
        item['type_id'] = rng.choices(candidates, weights=[CONFIG['equipment_fate_weight'] if t in fates else 1
                                                        for t in candidates], k=1)[0]
        item['level'] = min(item['level'], int(base.f.ITEMS[item['type_id']]['top_level']))


def candidate(level, tier, variant, attempt):
    seed = seed_for(level, tier, variant, attempt)
    rng = random.Random(seed)
    cap, p = base.caps(level), base.DESIGN['profiles'][tier]
    ordinal = (level - 1) * 15 + base.TIERS.index(tier) * 3 + base.ARCHES.index(variant)
    alphabet = '清风明月云海松竹星河山川青岚霜雪长空归鹤'
    name = '游仙' + ''.join(alphabet[(ordinal // (20 ** i)) % 20] for i in (2, 1, 0))
    role = dict(role_id=910000000 + ordinal, name=name, level=level, corteges=[], attachments=[], summon={'next_id': 1},
                reborn_layer=cap['role_realm_cap'] if tier in ('T1', 'T2') else 0,
                cortege_limit_plus=0, max_combat_power=0)
    n = cap['formation_slots']
    required = math.ceil(n * CONFIG['five_star_min_ratio'][tier])
    qlist = [5] * required + [5 if rng.random() < CONFIG['additional_five_star_probability']
                              else (3 if tier == 'T5' else 4) for _ in range(n - required)]
    rng.shuffle(qlist)
    used, styles, chosen = set(), {}, []
    eligible_needed = 3 if role['reborn_layer'] >= 2 else 0
    for q in sorted(qlist, reverse=True):
        style = variant if rng.random() < CONFIG['dominant_style_probability'] else rng.choice(base.ARCHES)
        tid = draw(rng, q, used, style, eligible=eligible_needed > 0)
        used.add(tid)
        eligible_needed -= int(tid in base.reborn.CORTS and eligible_needed > 0)
        chosen.append((tid, style))
    # Assign the front using defensive growth with randomness; all other positions shuffle.
    front = rng.choices(chosen, weights=[float(base.f.BASES[t]['base_fangyu_plus']) for t, _ in chosen], k=1)[0]
    chosen.remove(front)
    rng.shuffle(chosen)
    chosen.insert(1, front)
    for order, (tid, style) in enumerate(chosen, 1):
        c = base.make_companion(role, style, tier, tid, order=order)
        styles[int(c['id'])] = style
    support_count = min(p['support_count'], cap['positive_support_cap'] + cap['reverse_support_cap'])
    for pos in range(1, support_count + 1):
        q = 5 if rng.random() < 0.65 else 4
        tid = draw(rng, q, used, variant)
        used.add(tid)
        c = base.make_companion(role, variant, tier, tid, support=pos)
        styles[int(c['id'])] = variant
        name = base.cheer.NAMES[pos - 1]
        role['cheer_' + name + '_level'] = p['cheer_level']
        role['cheer_' + name + '_effect'] = rng.randint(1, n)
    for _ in range(2):
        tid = draw(rng, 5 if rng.random() < 0.65 else 4, used, variant)
        used.add(tid)
        c = base.make_companion(role, variant, tier, tid, reserve=True)
        styles[int(c['id'])] = variant
    base.cheer.prepare(role, base.CHEER)
    base.f.prepare(role, base.RULES)
    for c in role['corteges']:
        if c['order']:
            base.outfit(role, c, styles[int(c['id'])], tier)
        # Vary actual cultivation allocation per immortal, conserving the budget.
        spent = sum(c[s + '_plus'] for s in base.f.STATS)
        weights = [max(1, c[s + '_plus'] + rng.randint(-max(1, spent // 12), max(1, spent // 12)))
                   for s in base.f.STATS]
        points = [spent * w // sum(weights) for w in weights]
        points[weights.index(max(weights))] += spent - sum(points)
        c.update({s + '_plus': v for s, v in zip(base.f.STATS, points)})
    random_equipment(role, rng)
    return dict(npc_id=f'npc_v2_l{level:02d}_{tier.lower()}_{variant}', tier=tier, archetype=variant,
                band=list(base.band(level)), seed=seed, roster_attempt=attempt,
                unit_styles={str(k): v for k, v in styles.items()}, role=role,
                target_fraction=rng.uniform(*CONFIG['target_inner_fraction']))


def scaled(npc, percent):
    """Reduce attainable progress only, preserving rebirth history and prerequisites."""
    result = copy.deepcopy(npc)
    role = result['role']
    for c in role['corteges']:
        floor_level = int(base.reborn.LAYERS[c['reborn_layer']]['reset_level']) if c['reborn_layer'] else 1
        c['level'] = max(floor_level, 1 + (c['level'] - 1) * percent // 100)
        c['next_exp'] = base.f.EXPERIENCE.get((base.quality(c['type']), c['level']), 0)
        c['evolve_level'] = c['evolve_level'] * percent // 100
        total = base.budget(c)
        points = [c[s + '_plus'] * percent // 100 for s in base.f.STATS]
        if sum(points) > total:
            points = [v * total // sum(points) for v in points]
        if c['level'] == 1 or role['level'] < 5:
            points = [0] * 4
        c.update({s + '_plus': v for s, v in zip(base.f.STATS, points)})
        c['culture_point'] = total - sum(points)
    for item in role['attachments']:
        cfg = base.f.ITEMS.get(item['type_id'], {})
        if item['attach_type'] == 6 and not item.get('awaken'):
            item['level'] = max(int(base.f.SKILLS[item['type_id']]['begin_level']), 1 + (item['level'] - 1) * percent // 100)
        elif item['attach_type'] == 5 and int(cfg.get('main_type', 0)) in (1, 2, 3):
            item['level'] = 1 + (item['level'] - 1) * percent // 100
    # Lowest tiers can own five-star immortals without enough gear investment.
    # Unequip at most one progression step; retain inventory and bound stones.
    if result['tier'] == 'T5' and percent < 15:
        for item in role['attachments']:
            if item['attach_type'] == 5 and int(base.f.ITEMS.get(item['type_id'], {}).get('main_type', 0)) in (1, 2, 3):
                item.update(equip_order=0)
    role['max_combat_power'] = 0
    base.cp.recalculate(role, base.RULES, now=base.NOW)
    result['development_percent'] = percent
    return result


def generate(level, tier, variant, seen):
    limits = RANGES[level, tier]
    lower = limits['minimum']
    upper = limits['maximum'] or math.ceil(limits['sample_max'] * CONFIG['t1_sample_ceiling_multiplier'])
    for attempt in range(CONFIG['max_roster_attempts']):
        raw = candidate(level, tier, variant, attempt)
        if signature(raw) in seen:
            continue
        target = lower + (upper - lower) * raw['target_fraction']
        low, high, choices = 0, 100, []
        # Progress is monotone: positive base/growth and fixed legal effects only.
        while low <= high:
            mid = (low + high) // 2
            n = scaled(raw, mid)
            score = n['role']['role_combat_power']
            if lower <= score <= upper:
                choices.append(n)
            if score < target:
                low = mid + 1
            else:
                high = mid - 1
        if not choices:
            continue
        npc = min(choices, key=lambda n: abs(n['role']['role_combat_power'] - target))
        npc['power_range'] = dict(minimum=lower, maximum=limits['maximum'])
        npc['generation_ceiling'] = upper
        base.validate(npc)
        assert sum(base.quality(c['type']) == 5 for c in npc['role']['corteges'] if c['order']) >= math.ceil(
            base.caps(level)['formation_slots'] * CONFIG['five_star_min_ratio'][tier])
        seen.add(signature(npc))
        return npc
    raise RuntimeError(f'No in-range unique roster: {level} {tier} {variant}')


def battle_checks(samples):
    lookup = {(n['role']['level'], n['tier'], n['archetype']): n for n in samples}
    rules, results = base.journey.load_rules(), []
    for level in CONFIG['battle_levels']:
        pairs = []
        for tier in base.TIERS:
            for i, style in enumerate(CONFIG['variants']):
                pairs.append(('same_tier', lookup[level, tier, style],
                              lookup[level, tier, CONFIG['variants'][(i + 1) % 3]]))
        for weak, strong in zip(base.TIERS, base.TIERS[1:]):
            for style in CONFIG['variants']:
                pairs.append(('adjacent_tier', lookup[level, strong, style], lookup[level, weak, style]))
        for kind, left, right in pairs:
            for seed in CONFIG['battle_seeds']:
                for swap in (False, True):
                    a, b = (right, left) if swap else (left, right)
                    ar, br = a['role'], b['role']
                    rng = random.Random(seed)
                    with patch('network_redirect.combat.secrets.randbelow', side_effect=rng.randrange):
                        engine = base.combat_engine.Battle(ar, (base.battle_units(ar), base.battle_units(br)), rules, slots=8)
                        assert len(engine.fielded(1)) == base.caps(level)['starters']
                        assert all(u['order'] <= 4 for side in (1, 2) for u in engine.fielded(side))
                        result, _, actions = engine.run()
                    assert actions and all(hp >= 0 for side in actions.final_hp.values() for hp in side.values())
                    results.append(dict(kind=kind, level=level, left=a['npc_id'], right=b['npc_id'], seed=seed,
                                        result=result, action_count=len(actions), stop_reason=actions.stop_reason,
                                        left_power=ar['role_combat_power'], right_power=br['role_combat_power']))
    return results


def source_manifest():
    # Track the actual generation/settlement dependencies, not unrelated live
    # activity handlers which may be edited concurrently in this shared repo.
    paths = list((ROOT / 'analysis/configs').rglob('*.csv'))
    paths += [ROOT / 'network_redirect' / (name + '.py') for name in (
        'cheer', 'combat', 'combat_engine', 'combat_power', 'cortege_recycle',
        'equipment', 'formation', 'immortal', 'journey', 'protocol', 'reborn',
        'reborn_stars', 'skill_insight', 'spirit_array', 'summon')]
    paths += [ROOT / 'server_config' / name for name in (
        'npc_design_rules.json', 'npc_expansion_rules.json', 'formation_rules.json',
        'cheer_rules.json', 'reborn_rules.json', 'journey_rules.json',
        'essence_power_v1_1.json', 'stone_rules.json', 'immortal_rules.json',
        'skill_insight_rules.json', 'spirit_array_rules.json', 'cortege_recycle_rules.json')]
    paths += [Path(__file__), Path(base.__file__), V1 / 'catalog.json', V1 / 'power_ranges.csv',
              ROOT / 'analysis/evidence/cheer/role_attributes.json',
              ROOT / 'analysis/evidence/protocol_tables.json']
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}


def build(output, check=False):
    old = json.loads((V1 / 'catalog.json').read_text())['npcs']
    old_hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in V1.iterdir() if p.is_file()}
    for n in old:
        assert base.cp.explain(n['role'], base.RULES)['total'] == n['settlement']['total'], 'V1 calibration needs review'
    seen = {signature(n) for n in old}
    samples = []
    for level in range(CONFIG['levels'][0], CONFIG['levels'][1] + 1):
        for tier in base.TIERS:
            for variant in CONFIG['variants']:
                samples.append(generate(level, tier, variant, seen))
        if level % 10 == 0 or level == 99:
            print(f'Generated and validated level {level}: {len(samples)} NPCs', flush=True)
    battles = battle_checks(samples)
    files, overview, companions, pool_counts = {}, [], [], Counter()
    for n in samples:
        role = n['role']
        team = sorted((c for c in role['corteges'] if c['order']), key=lambda c: c['order'])
        checked = [b for b in battles if n['npc_id'] in (b['left'], b['right'])]
        limited = sum(b['stop_reason'] != 'elimination' for b in checked)
        n['battle_validation'] = dict(status='replay_limit_observed' if limited else 'smoke_passed' if checked else 'not_sampled',
                                      checked_battles=len(checked), replay_limited_battles=limited)
        n['settlement'] = dict(scoring_version=base.cp.SCORE_VERSION, attribute_revision=base.RULES['attribute_policy']['revision'],
                              total=role['role_combat_power'], member_ids=role['combat_power_breakdown']['member_ids'])
        role.pop('combat_power_breakdown')
        pool_counts.update(c['type'] for c in team)
        overview.append(dict(npc_id=n['npc_id'], name=role['name'], role_level=role['level'], tier=n['tier'],
                             archetype=base.DESIGN['archetypes'][n['archetype']]['name'], power=role['role_combat_power'],
                             minimum=n['power_range']['minimum'], maximum=n['power_range']['maximum'],
                             five_star_count=sum(base.quality(c['type']) == 5 for c in team),
                             starters=min(4, len(team)), battle_reserves=max(0, len(team)-4),
                             supports=sum(bool(c['cheer_order']) for c in role['corteges']), idle_reserves=2,
                             seed=n['seed'], roster_attempt=n['roster_attempt'], development_percent=n['development_percent'],
                             battle_validation=n['battle_validation']['status'],
                             lineup=' / '.join(f"{c['order']}:{base.NAMES[c['type']]}({c['type']})" for c in team)))
        for c in role['corteges']:
            items = [i for i in role['attachments'] if i.get('innate_owner_id') == c['id'] or
                     (c['order'] and i.get('equip_order') == c['order']) or i.get('owner_id') == c['id']]
            equipment = [i for i in items if i['attach_type'] == 5 and
                         int(base.f.ITEMS.get(i['type_id'], {}).get('main_type', 0)) in (1, 2, 3)]
            def label(item):
                names = base.SKILL_NAMES if item['attach_type'] == 6 else base.ITEM_NAMES
                return f"{names.get(item['type_id'], '')}({item['type_id']})Lv{item['level']}"
            companions.append(dict(npc_id=n['npc_id'], id=c['id'], type_id=c['type'], name=base.NAMES[c['type']],
                                   quality=base.quality(c['type']), order=c['order'], cheer_order=c['cheer_order'],
                                   style=n['unit_styles'][str(int(c['id']))], level=c['level'], evolve=c['evolve_level'], rebirth=c['reborn_layer'],
                                   culture_hp=c['hp_plus'], culture_attack=c['gongji_plus'], culture_defense=c['fangyu_plus'], culture_magic=c['magic_plus'],
                                   culture_left=c['culture_point'], hp=c['hp'], attack=c['gongji'], defense=c['fangyu'], magic=c['magic'],
                                   essence_score=base.cp.essence_score(role,c)['total'], power=c['combat_power'],
                                   equipment=' / '.join(label(i)+f"进阶{i['advance_level']}铸造{i['cast_level']}六星{i['star_level']}" for i in equipment),
                                   stones=' / '.join(f"装备{i['type_id']}:孔1 Lv{i['stone1_level']}" for i in equipment if i.get('stone1_level')),
                                   skills=' / '.join(label(i) for i in items if i['attach_type']==6),
                                   essences=' / '.join(label(i) for i in items if i['type_id'] in base.cp.ESSENCE_SCORES),
                                   stars=' / '.join(label(i) for i in items if i['type_id'] in base.reborn_stars.STARS),
                                   awakening=next((i.get('awaken',0) for i in items if i.get('innate_owner_id')==c['id']),0)))
    for level in range(1,100):
        files[f'levels/level_{level:02d}.json'] = base.json_text(dict(schema_version=1, revision=CONFIG['revision'],
                                              npcs=[n for n in samples if n['role']['level']==level]))
    groups = []
    for level in range(1,100):
        for tier in base.TIERS:
            ns = [n for n in overview if n['role_level']==level and n['tier']==tier]
            assert len(ns)==3
            groups.append(dict(role_level=level,tier=tier,count=len(ns),minimum=RANGES[level,tier]['minimum'],
                               maximum=RANGES[level,tier]['maximum'],sample_min=min(n['power'] for n in ns),
                               sample_max=max(n['power'] for n in ns),five_star_count=sum(n['five_star_count'] for n in ns),
                               formation_count=sum(n['starters']+n['battle_reserves'] for n in ns)))
    tier_stats={}
    for tier in base.TIERS:
        rows=[r for r in overview if r['tier']==tier]
        five=sum(r['five_star_count'] for r in rows)
        total=sum(r['starters']+r['battle_reserves'] for r in rows)
        tier_stats[tier]=dict(npcs=len(rows),five_star_count=five,formation_count=total,ratio=round(five/total,6))
    adjacent = [b for b in battles if b['kind'] == 'adjacent_tier']
    wins = sum((b['left_power'] > b['right_power'] and 1 <= b['result'] <= 3) or
               (b['right_power'] > b['left_power'] and 4 <= b['result'] <= 6) for b in adjacent)
    unresolved = sum(b['result'] == 0 for b in adjacent)
    summary=dict(revision=CONFIG['revision'],npc_count=len(samples),level_count=99,level_tier_cells=len(groups),
                 variants_per_cell=3,old_npc_count=len(old),combined_npc_count=len(samples)+len(old),
                 tier_stats=tier_stats,available_five_star_types=len(POOLS[5]),
                 used_five_star_types=sum(t in POOLS[5] for t in pool_counts),
                 unique_compositions=len({signature(n) for n in samples}),
                 composition_overlap_with_v1=len({signature(n) for n in samples}&{signature(n) for n in old}),
                 max_roster_attempt=max(n['roster_attempt'] for n in samples),
                 battle_count=len(battles),battle_stop_reasons=dict(Counter(b['stop_reason'] for b in battles)),
                 adjacent_tier_results=dict(count=len(adjacent),higher_power_wins=wins,
                                             lower_power_wins=len(adjacent)-wins-unresolved,unresolved=unresolved),
                 battle_sample_status=dict(Counter(n['battle_validation']['status'] for n in samples)),
                 old_power_recalculation_unchanged=True,old_artifacts_unchanged=True,online_routes_replaced=False,
                 checks=['all_495_level_tier_cells', 'in_original_power_range', 'five_star_quota',
                         'unique_composition_not_just_position_shuffle', 'no_duplicate_units_or_ids',
                         'v1_growth_ownership_rebirth_and_score_validation', 'idempotent_recalculation'])
    files['catalog.json']=base.json_text(dict(schema_version=1,revision=CONFIG['revision'],mode='inferred',
                           base_catalog='../v1/catalog.json',npc_count=len(samples),
                           files=[f'levels/level_{l:02d}.json' for l in range(1,100)],
                           index=[dict(npc_id=n['npc_id'],level=n['role']['level'],tier=n['tier'],
                                       file=f"levels/level_{n['role']['level']:02d}.json") for n in samples]))
    files['overview.csv']=base.csv_text(overview)
    files['companions.csv']=base.csv_text(companions)
    files['coverage.csv']=base.csv_text(groups)
    files['battle_checks.csv']=base.csv_text(battles)
    files['validation.json']=base.json_text(summary)
    files['candidate_pool.csv']=base.csv_text([dict(type_id=t,name=base.NAMES[t],quality=base.quality(t),
                  rebirth_eligible=t in base.reborn.CORTS,formation_appearances=pool_counts[t]) for q in (3,4,5) for t in POOLS[q]])
    files['source_manifest.json']=base.json_text(source_manifest())
    lines=['# 五星随机阵容扩充批次 V2','', '1～99每级、每档3个NPC；T1最高、T5最低。1～4首发，5～8为对应战斗替补。',
           '战力按V1原区间校验；完整状态保存在各等级JSON，含装备、法术、精魄、灵石及助威。','']
    for level in range(1,100):
        lines += [f'## {level}级','',f'[完整配置](levels/level_{level:02d}.json)','',
                  '| ID／姓名 | 档位／主流派 | 战力 | 五星／出战 | 阵位与神仙 | 对战状态 |','|---|---|---:|---|---|---|']
        for r in overview:
            if r['role_level']==level:
                lines.append(f"| {r['npc_id']}／{r['name']} | {r['tier']}／{r['archetype']} | {r['power']:,} | {r['five_star_count']}/{r['starters']+r['battle_reserves']} | {r['lineup']} | {r['battle_validation']} |")
        lines.append('')
    files['rosters.md']='\n'.join(lines)+'\n'
    assert len({n['npc_id'] for n in samples})==len(samples)
    assert len({n['role']['name'] for n in samples})==len(samples)
    assert len({n['role']['role_id'] for n in samples})==len(samples)
    assert {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in V1.iterdir() if p.is_file()}==old_hashes
    if check:
        stale=[name for name,value in files.items() if not (output/name).exists() or (output/name).read_bytes()!=value.encode()]
        if stale:
            raise SystemExit('Stale expansion artifacts: '+', '.join(stale))
    else:
        for name,value in files.items():
            path=output/name
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(value.encode())
    print(base.json_text(summary))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'analysis/npc_design/v2')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    build(args.output,args.check)
