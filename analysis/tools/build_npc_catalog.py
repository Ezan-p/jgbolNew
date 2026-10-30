#!/usr/bin/env python3
"""Reproducible NPC design snapshots. Never opens the live role database.

Run from the repository root with .runtime/venv/bin/python. The exported role
is a combat snapshot, not a login-ready account. All power comes from production
settlement; this tool has no score multipliers or manually assigned panel stats.
"""
import argparse
import copy
import csv
import hashlib
import io
import json
from pathlib import Path
import random
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import formation as f, summon, combat_power as cp, cheer, reborn
from network_redirect import reborn_stars, combat, combat_engine, journey

RULE_PATH = ROOT / 'server_config/npc_design_rules.json'
DESIGN = json.loads(RULE_PATH.read_text())
RULES = f.load_rules()
CHEER = cheer.load_rules()
REBORN = reborn.load_rules()
NAMES = {int(r['type_id']): r['name'].strip() for r in summon.rows('cortege/cortege_name_0.csv')}
ITEM_NAMES = {int(next(iter(r.values()))): r['name'] for r in summon.rows('item_name.csv')}
SKILL_NAMES = {int(r['type_id']): r['name'] for r in summon.rows('skill_name.csv')}
TIERS = DESIGN['tier_order_weak_to_strong']
ARCHES = list(DESIGN['archetypes'])
NOW = 1792857600  # Fixed settlement clock; no temporary title is granted.


def band(level):
    starts = DESIGN['band_starts']
    lo = max(n for n in starts if n <= level)
    hi = min([n - 1 for n in starts if n > level] or [99])
    return lo, hi


def caps(level):
    realm = sum(level >= r['level'] for r in REBORN['realms'])
    count = int(f.LEVELS[level]['cortege_count'])
    return dict(role_level=level, formation_slots=count, starters=min(4, count), battle_reserves=max(0, count - 4),
                idle_reserve_cap=None, positive_support_cap=8 if level >= 60 else 0,
                reverse_support_cap=8 if level >= 80 else 0,
                free_support_slots=2 if level >= 60 else 0,
                companion_level_cap=min(200, level * 3) if level < 80 else 200,
                companion_level_cap_with_home=min(300, level * 3) if level < 80 else 300,
                experience_slow_at=level * 5 // 2 if level < 80 else None,
                equipment_level_cap=level * 2,
                cultivation_open=level >= 5, evolution_table_cap=max(f.EVOLVE_COST),
                role_realm_cap=realm,
                rebirth_layer_cap=REBORN['realms'][realm - 1]['max_layer'] if realm else 0,
                equipment_advance_cap=10 if level >= RULES['equipment_advance']['min_role_level'] else 0,
                stone_open=level >= 10, essence_slots_cap=4, essence_level_cap=5,
                skill_cap_note='逐法术读取skill_base.top_level；本候选池均为10级',
                cap_note='境界、助威、装备门槛依当前本地配置；人数上限不等于已付材料开启')


def quality(t):
    return int(f.BASES[t]['quality'])


def pool(arch, q):
    return DESIGN['archetypes'][arch]['pools'][str(q)]


def choose(arch, q, used):
    # Ordered authored candidates, then other authored flows, then real base forms.
    candidates = pool(arch, q) + [t for a in ARCHES for t in pool(a, q)]
    candidates += sorted(t for t, b in f.BASES.items()
                         if quality(t) == q and 3000 <= t < 6000 and int(b['base_type_id']) == t)
    return next(t for t in candidates if t not in used)


def attach(role, kind, tid, **values):
    obj = dict(id=f.new_id(role), attach_type=kind, type_id=tid, count=1, level=1)
    obj.update(values)
    role['attachments'].append(obj)
    return obj


def budget(c):
    # Minimal reproducible history: level to each rebirth minimum, reset, relevel.
    q = quality(c['type'])
    if c.get('level_culture_version', 0) >= 2:
        earned = f.level_culture_points(q, 1, c['level'])
        earned += sum(f.level_culture_points(q, int(reborn.LAYERS[n]['reset_level']),
                                           int(reborn.LAYERS[n]['min_level']))
                      for n in range(1, c.get('reborn_layer', 0) + 1))
    elif c.get('level_culture_version') == 1:
        # Preserve snapshots generated under the previous evolve-table rule.
        earned = sum(f.EVOLVE_POINTS[q, n] for n in range(2, c['level'] + 1))
        earned += sum(f.EVOLVE_POINTS[q, level]
                      for n in range(1, c.get('reborn_layer', 0) + 1)
                      for level in range(int(reborn.LAYERS[n]['reset_level']) + 1,
                                         int(reborn.LAYERS[n]['min_level']) + 1))
    else:
        # Frozen NPC snapshots keep their original budget and combat balance.
        # Newly generated NPCs carry the version marker from summon.companion.
        cycles = sum(int(reborn.LAYERS[n]['min_level']) - int(reborn.LAYERS[n]['reset_level'])
                     for n in range(1, c.get('reborn_layer', 0) + 1))
        earned = (c['level'] - 1 + cycles) * 5
    earned += sum(int(reborn.LAYERS[n]['ret_culture']) for n in range(1, c.get('reborn_layer', 0) + 1))
    earned += sum(f.EVOLVE_POINTS[quality(c['type']), n] for n in range(1, c.get('evolve_level', 0) + 1))
    return earned


def make_companion(role, arch, tier, tid, order=0, support=0, reserve=False):
    p, a, cap = DESIGN['profiles'][tier], DESIGN['archetypes'][arch], caps(role['level'])
    c = summon.companion(role, tid)
    c.update(order=order, cheer_order=support, cur_exp=0, reborn_layer=0, reborn_vein_level=0,
             reborn_plus_type={'attack': 1, 'endurance': 2, 'magic': 3}[arch])
    c['level'] = max(1, cap['companion_level_cap'] * p['level_percent'] // 100)
    if support:
        c['level'] = max(1, c['level'] * 3 // 4)
    if reserve:
        c['level'] = max(1, c['level'] // 2)
    if order and role['reborn_layer'] and tid in reborn.CORTS:
        c['reborn_layer'] = p['reborn_layers'][role['reborn_layer'] - 1]
        if c['reborn_layer']:
            c['level'] = max(c['level'], int(reborn.LAYERS[c['reborn_layer']]['reset_level']))
    c['evolve_level'] = (role['level'] * p['evolve_percent'] // 100
                         if role['level'] >= DESIGN['gates']['evolution_design_min_level'] and not reserve else 0)
    if support:
        c['evolve_level'] //= 2
    total = budget(c)
    spent = total * p['culture_percent'] // 100 if role['level'] >= 5 and c['level'] > 1 and not reserve else 0
    weights = [35, 15, 45, 5] if order in (2, 6) else a['culture_weights']
    allocated = [spent * w // 100 for w in weights]
    allocated[weights.index(max(weights))] += spent - sum(allocated)
    c.update({s + '_plus': v for s, v in zip(f.STATS, allocated)})
    c['culture_point'] = total - spent
    c['equiped_ext_skill_limit'] = 1
    role['corteges'].append(c)
    return c


def outfit(role, c, arch, tier):
    p, a, level = DESIGN['profiles'][tier], DESIGN['archetypes'][arch], role['level']
    order = c['order']
    q = p.get('equipment_quality_at_50', p['equipment_quality']) if level >= 50 else p['equipment_quality']
    # Same cost tier per equipment category; prefer real equipment fate when available.
    fate_ids = {int(t) for r in f.FATES if int(r['cortege_type[effected_cortege]']) == c['type']
                and r['tartege_type[4-cortege/5-equip/6-skill]'] == '5'
                for t in r['target_object_type[1/2/3]'].split('/')}
    for main in (1, 2, 3):
        candidates = [t for t, r in f.ITEMS.items() if int(r['quality']) == q and int(r['main_type']) == main]
        tid = min(candidates, key=lambda t: (t not in fate_ids, t))
        item = attach(role, 5, tid, equip_order=order, equip_pos=int(f.ITEMS[tid]['equip_pos']),
                      level=min(int(f.ITEMS[tid]['top_level']), max(1, level * 2 * p['enhance_percent'] // 100)),
                      advance_level=p['advance'] if level >= 60 else 0, star_count=0,
                      cur_spirit_count=0, reborn_bit=0, cast_level=0, star_level=0, drill_count=0)
        if tier == 'T1' and role['reborn_layer'] >= 3:
            item.update(reborn_bit=1, cast_level=4)
            if role['reborn_layer'] == 4:
                item['star_level'] = 1
        if p['stone_level'] and level >= 10:
            item['drill_count'] = 1  # Deliberately one stone per item, not maximal sockets.
            stone_level = min(p['stone_level'], max(1, level // 10))
            item['stone1_level'] = stone_level
            attach(role, 5, 1089 + main, level=stone_level, owner_id=item['id'], equip_pos=1, equip_order=0)
    innate = next(i for i in role['attachments'] if i.get('innate_owner_id') == c['id'])
    sl = min(10, 1 + level // p['skill_divisor'])
    innate['level'] = min(sl, int(f.SKILLS[innate['type_id']]['top_level']))
    sq = min(5, max(3, q))
    # Preserve a usable active skill even when the native skill is passive.
    desired = list(a['passives'][str(sq)])
    if f.SKILLS[innate['type_id']]['use_mode(1-active，2-passive)'] == '2':
        desired.insert(0, a['active_fallback'][str(sq)])
    used = {innate['type_id']}
    pos = 2
    for tid in desired + a['passives']['3']:
        if tid in used:
            continue
        if pos > 1 + p['extra_skills']:
            break
        attach(role, 6, tid, count=0, level=sl, protogenic=0, equip_order=order, equip_pos=pos)
        used.add(tid)
        pos += 1
    if c['reborn_layer'] and innate['level'] == 10:
        innate['awaken'] = 2 if order in (2, 6) else a['awaken']
        # One legal LINEUP star; leave other slots empty to keep samples interpretable.
        star_id = {1: 10302, 2: 10304, 3: 10308}[innate['awaken']]
        attach(role, 5, star_id, level=5 if tier == 'T1' else 3, owner_id=c['id'], ext_awaken_pos=1)
    if level >= DESIGN['gates']['essence_design_min_level']:
        count = p['essence_slots']
        c['equiped_ext_skill_limit'] = max(1, count)
        base = 10200 if tier == 'T1' and level >= 80 else 10100
        el = min(p['essence_level'], max(1, level // 20))
        families = [10, 14, 6, 3] if order in (2, 6) else a['essence_families']
        for slot, family in enumerate(families[:count], 1):
            attach(role, 5, base + family, level=el, owner_id=c['id'], ext_skill_pos=slot)


def generate(level, tier, arch):
    p, cap = DESIGN['profiles'][tier], caps(level)
    index = (level * 100 + TIERS.index(tier) * 10 + ARCHES.index(arch))
    role = dict(role_id=900000000 + index, name=f"离线·{level:02d}·{tier}·{DESIGN['archetypes'][arch]['name']}",
                level=level, corteges=[], attachments=[], summon={'next_id': 1},
                reborn_layer=cap['role_realm_cap'] if tier in ('T1', 'T2') else 0,
                cortege_limit_plus=0, max_combat_power=0)
    used = set()
    for pos in range(1, cap['formation_slots'] + 1):
        q = p['quality_pattern'][(pos - 1) % len(p['quality_pattern'])]
        tid = choose(arch, q, used)
        used.add(tid)
        # Original combat position 2 is the front; position 1 is the back/core.
        make_companion(role, arch, tier, tid, order={1: 2, 2: 1}.get(pos, pos))
    support_count = min(p['support_count'], cap['positive_support_cap'] + cap['reverse_support_cap'])
    for pos in range(1, support_count + 1):
        tid = choose(arch, 4 if tier in ('T1', 'T2') else 3, used)
        used.add(tid)
        make_companion(role, arch, tier, tid, support=pos)
        name = cheer.NAMES[pos - 1]
        role['cheer_' + name + '_level'] = p['cheer_level']
        role['cheer_' + name + '_effect'] = (pos - 1) % cap['formation_slots'] + 1
    for _ in range(2):
        tid = choose(arch, 3, used)
        used.add(tid)
        make_companion(role, arch, tier, tid, reserve=True)
    cheer.prepare(role, CHEER)
    f.prepare(role, RULES)
    for c in role['corteges']:
        if c['order']:
            outfit(role, c, arch, tier)
    cp.recalculate(role, RULES, now=NOW)
    return dict(npc_id=f'npc_v1_l{level:02d}_{tier.lower()}_{arch}', tier=tier,
                archetype=arch, band=list(band(level)), role=role)


def validate(npc):
    role, level = npc['role'], npc['role']['level']
    cap = caps(level)
    members = role['corteges']
    assert sorted(c['order'] for c in members if c['order']) == list(range(1, cap['formation_slots'] + 1))
    assert len({c['type'] for c in members}) == len(members)
    ids = [i['id'] for i in members + role['attachments']]
    assert len(ids) == len(set(ids))
    assert role.get('combat_sources', {}) == {}
    for c in members:
        assert not (c['order'] and c['cheer_order'])
        assert 1 <= c['level'] <= cap['companion_level_cap']
        assert 0 <= c['evolve_level'] <= max(f.EVOLVE_COST)
        assert c['culture_point'] + sum(c[s + '_plus'] for s in f.STATS) == budget(c)
        assert all(c[s + '_plus'] >= 0 for s in f.STATS)
        if level < 5 or c['level'] == 1:
            assert sum(c[s + '_plus'] for s in f.STATS) == 0
        assert c.get('combat_sources', {}) == {}
        if c['reborn_layer']:
            assert c['type'] in reborn.CORTS
            assert c['reborn_layer'] <= cap['rebirth_layer_cap']
            assert c['level'] >= int(reborn.LAYERS[c['reborn_layer']]['reset_level'])
            assert all(int(reborn.LAYERS[n]['min_level']) <= cap['companion_level_cap']
                       for n in range(1, c['reborn_layer'] + 1))
        if c['cheer_order']:
            pos = c['cheer_order']
            assert level >= CHEER['cheer_level_limit'][pos - 1]
            assert role['cheer_' + cheer.NAMES[pos - 1] + '_level'] > 0
            assert role['cheer_' + cheer.NAMES[pos - 1] + '_effect'] in range(1, cap['formation_slots'] + 1)
            if pos > 8:
                assert role['cheer_' + cheer.NAMES[pos - 9] + '_level'] > 0
        innates = [i for i in role['attachments'] if i.get('innate_owner_id') == c['id']]
        assert len(innates) == 1 and innates[0]['type_id'] == int(f.BASES[c['type']]['chushijineng'])
        essences = [i for i in role['attachments'] if i['type_id'] in cp.ESSENCE_SCORES and i.get('owner_id') == c['id']]
        assert len({i['ext_skill_pos'] for i in essences}) == len(essences)
        assert len({i['type_id'] % 100 for i in essences}) == len(essences)
        assert all(1 <= i['ext_skill_pos'] <= c['equiped_ext_skill_limit'] and 1 <= i['level'] <= 5 for i in essences)
    for n in range(role['reborn_layer']):
        r = REBORN['realms'][n]
        assert level >= r['level']
        assert sum(c['reborn_layer'] >= r['required_layer'] for c in members) >= r['count']
    for i in role['attachments']:
        if i['attach_type'] == 6:
            assert int(f.SKILLS[i['type_id']]['begin_level']) <= i['level'] <= int(f.SKILLS[i['type_id']]['top_level'])
            if i.get('awaken'):
                owner = next(c for c in members if c['id'] == i['innate_owner_id'])
                assert owner['reborn_layer'] > 0 and i['level'] == 10
        elif i['type_id'] in reborn_stars.STARS:
            owner = next(c for c in members if c['id'] == i['owner_id'])
            assert owner['reborn_layer'] >= reborn_stars.OPEN[i['ext_awaken_pos']]
            assert any(x.get('innate_owner_id') == owner['id'] and x.get('awaken') for x in role['attachments'])
            assert 1 <= i['level'] <= 10
        elif int(f.ITEMS[i['type_id']]['main_type']) in (1, 2, 3):
            cfg = f.ITEMS[i['type_id']]
            assert i['level'] <= min(level * 2, int(cfg['top_level']))
            assert i['equip_pos'] == int(cfg['equip_pos'])
            assert not i['advance_level'] or (level >= 60 and int(cfg['quality']) in (4, 5))
            assert 0 <= i['advance_level'] <= 10
            assert not i['reborn_bit'] or (role['reborn_layer'] >= 3 and i['advance_level'] == 10 and int(cfg['quality']) == 5)
            assert not i['star_level'] or role['reborn_layer'] == 4
            stones = [s for s in role['attachments'] if s.get('owner_id') == i['id']]
            assert len(stones) == i['drill_count']
            for stone in stones:
                assert level >= 10 and stone['type_id'] == 1089 + int(cfg['main_type'])
                assert i['stone%d_level' % stone['equip_pos']] == stone['level']
    for pos in range(1, cap['formation_slots'] + 1):
        skills = [i for i in role['attachments'] if i['attach_type'] == 6 and i.get('equip_order') == pos]
        assert len({i['type_id'] for i in skills}) == len(skills)
        assert len({i['equip_pos'] for i in skills}) == len(skills) <= 3
    expected = sum(c['combat_power'] for c in members if c['order'])
    assert expected == role['role_combat_power'] < cp.LIMIT
    for c in members:
        assert c['combat_power'] == cp.score_panel(c, RULES['combat_weights'], cp.essence_score(role, c)['total'])
    before = copy.deepcopy(role)
    cp.recalculate(role, RULES, now=NOW)
    assert role == before, 'settlement must be idempotent'


def csv_text(rows):
    out = io.StringIO(newline='')
    w = csv.DictWriter(out, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
    return out.getvalue()


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def source_manifest():
    paths = list((ROOT / 'analysis/configs').rglob('*.csv'))
    paths += list((ROOT / 'server_config').glob('*.json'))
    paths += [ROOT / 'network_redirect' / (m + '.py') for m in
              ('formation', 'summon', 'combat_power', 'immortal', 'cheer', 'equipment',
               'reborn', 'reborn_stars', 'skill_insight', 'combat', 'combat_engine', 'journey')]
    paths += [Path(__file__)]
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}


def battle_units(role):
    units = []
    for c in role['corteges']:
        if not c['order']:
            continue
        u = dict(companion_id=c['id'], type=c['type'], order=c['order'], level=c['level'],
                 evolve=c['evolve_level'], reborn=c['reborn_layer'], max_hp=c['hp'],
                 **{s: c[s] for s in f.STATS})
        u['skills'] = [(i['type_id'], i['level']) for i in role['attachments']
                       if i['attach_type'] == 6 and i.get('equip_order') == c['order']]
        units.append(u)
    combat.attach_essences(role, units)
    reborn_stars.attach_combat_traits(role, units)
    return units


def battle_checks(samples):
    lookup = {(x['role']['level'], x['tier'], x['archetype']): x for x in samples}
    rules = journey.load_rules()
    rows = []
    for level in (7, 36, 60, 80, 99):
        pairs = []
        for tier in TIERS:
            for idx, arch in enumerate(ARCHES):
                pairs.append(('same_tier', lookup[level, tier, arch], lookup[level, tier, ARCHES[(idx + 1) % 3]]))
        for weak, strong in zip(TIERS, TIERS[1:]):
            for arch in ARCHES:
                pairs.append(('adjacent_tier', lookup[level, strong, arch], lookup[level, weak, arch]))
        for kind, left, right in pairs:
            for seed in (17, 83):
                for swap in (False, True):
                    a, b = (right, left) if swap else (left, right)
                    ar, br = a['role'], b['role']
                    rng = random.Random(seed)
                    with patch('network_redirect.combat.secrets.randbelow', side_effect=rng.randrange):
                        engine = combat_engine.Battle(ar, (battle_units(ar), battle_units(br)), rules, slots=8)
                        assert len(engine.fielded(1)) == caps(level)['starters']
                        assert all(u['order'] <= 4 for side in (1, 2) for u in engine.fielded(side))
                        result, _, actions = engine.run()
                    assert actions and all(hp >= 0 for side in actions.final_hp.values() for hp in side.values())
                    rows.append(dict(kind=kind, level=level, left=a['npc_id'], right=b['npc_id'], seed=seed,
                                     result=result, action_count=len(actions), stop_reason=actions.stop_reason,
                                     left_power=ar['role_combat_power'], right_power=br['role_combat_power']))
    return rows


def build():
    samples, ranges = [], []
    # Calibrate at every actual role level; never apply a band's upper end to its lower end.
    for level in range(1, 100):
        groups = {tier: [generate(level, tier, a) for a in ARCHES] for tier in TIERS}
        spans = {t: (min(n['role']['role_combat_power'] for n in ns), max(n['role']['role_combat_power'] for n in ns))
                 for t, ns in groups.items()}
        for low, high in zip(TIERS, TIERS[1:]):
            assert spans[low][1] < spans[high][0], (level, low, spans[low], high, spans[high])
        cuts = [(spans[a][1] + spans[b][0]) // 2 for a, b in zip(TIERS, TIERS[1:])]
        for idx, tier in enumerate(TIERS):
            lower = 0 if idx == 0 else cuts[idx - 1] + 1
            upper = cuts[idx] if idx < 4 else None
            ranges.append(dict(role_level=level, band_start=band(level)[0], band_end=band(level)[1], tier=tier,
                               minimum=lower, maximum=upper, sample_min=spans[tier][0], sample_max=spans[tier][1]))
            for npc in groups[tier]:
                validate(npc)
                npc['power_range'] = dict(minimum=lower, maximum=upper)
                if level in DESIGN['band_starts']:
                    samples.append(npc)
    results = battle_checks(samples)
    return samples, ranges, results


def export(samples, ranges, battles):
    overview, units = [], []
    for npc in samples:
        role = npc['role']
        checked = [b for b in battles if npc['npc_id'] in (b['left'], b['right'])]
        limited = [b for b in checked if b['stop_reason'] != 'elimination']
        npc['battle_validation'] = dict(
            status='replay_limit_observed' if limited else 'smoke_passed' if checked else 'not_sampled',
            checked_battles=len(checked), replay_limited_battles=len(limited),
            note='事件容量触顶对局须按未决处理；无对战记录仅表示完成数据与战力校验')
        team = sorted((c for c in role['corteges'] if c['order']), key=lambda c: c['order'])
        overview.append(dict(npc_id=npc['npc_id'], name=role['name'], role_level=role['level'], tier=npc['tier'],
                             archetype=DESIGN['archetypes'][npc['archetype']]['name'], power=role['role_combat_power'],
                             starters=min(4, len(team)), battle_reserves=max(0, len(team) - 4),
                             supports=sum(bool(c['cheer_order']) for c in role['corteges']),
                             idle_reserves=2, battle_validation=npc['battle_validation']['status'],
                             lineup=' / '.join(f"{c['order']}:{NAMES[c['type']]}({c['type']})" for c in team)))
        for c in role['corteges']:
            items = [i for i in role['attachments'] if (i.get('innate_owner_id') == c['id'] or
                     (c['order'] and i.get('equip_order') == c['order']) or i.get('owner_id') == c['id'])]
            view = lambda i: f"{SKILL_NAMES.get(i['type_id'], '') if i['attach_type'] == 6 else ITEM_NAMES.get(i['type_id'], '')}({i['type_id']})Lv{i['level']}"
            units.append(dict(npc_id=npc['npc_id'], id=c['id'], type_id=c['type'], name=NAMES[c['type']], quality=quality(c['type']),
                              duty={1: '后位核心', 2: '前位承伤', 3: '上路', 4: '下路', 5: '后位替补', 6: '前位替补', 7: '上路替补', 8: '下路替补'}.get(c['order'], '助威' if c['cheer_order'] else '背包候补'),
                              order=c['order'], cheer_order=c['cheer_order'], level=c['level'], evolve=c['evolve_level'],
                              rebirth=c['reborn_layer'], hp=c['hp'], attack=c['gongji'], defense=c['fangyu'], magic=c['magic'],
                              power=c['combat_power'], essence_power=cp.essence_score(role, c)['total'],
                              culture_spent=sum(c[s + '_plus'] for s in f.STATS), culture_left=c['culture_point'],
                              culture_hp=c['hp_plus'], culture_attack=c['gongji_plus'], culture_defense=c['fangyu_plus'], culture_magic=c['magic_plus'],
                              equipment=' / '.join(view(i) + f"进阶{i.get('advance_level', 0)}铸造{i.get('cast_level', 0)}六星{i.get('star_level', 0)}" for i in items if i['attach_type'] == 5 and int(f.ITEMS[i['type_id']]['main_type']) in (1, 2, 3)),
                              stones=' / '.join(f"装备{i['type_id']}:孔1 Lv{i['stone1_level']}" for i in items if i.get('stone1_level')),
                              skills=' / '.join(view(i) for i in items if i['attach_type'] == 6),
                              awakening=next((i.get('awaken', 0) for i in items if i.get('innate_owner_id') == c['id']), 0),
                              stars=' / '.join(view(i) for i in items if i['type_id'] in reborn_stars.STARS),
                              essences=' / '.join(view(i) for i in items if i['type_id'] in cp.ESSENCE_SCORES)))
        npc['settlement'] = dict(scoring_version=cp.SCORE_VERSION, attribute_revision=RULES['attribute_policy']['revision'],
                                 total=role['role_combat_power'], member_ids=role['combat_power_breakdown']['member_ids'])
        role.pop('combat_power_breakdown')  # Rebuild full trace with cp.explain; avoid redundant megabytes.
    candidates = [dict(type_id=t, name=NAMES[t], quality=quality(t), innate_skill=int(b['chushijineng']),
                       innate_name=SKILL_NAMES[int(b['chushijineng'])], rebirth_eligible=t in reborn.CORTS,
                       archetypes=[a for a in ARCHES if t in pool(a, quality(t))],
                       growth={s: b[g] for s, g in zip(f.STATS, f.GROWTH_COLUMNS)})
                  for t, b in sorted(f.BASES.items()) if any(t == c['type'] for n in samples for c in n['role']['corteges'])]
    adjacent = [b for b in battles if b['kind'] == 'adjacent_tier']
    strong_wins = sum((b['left_power'] > b['right_power'] and 1 <= b['result'] <= 3) or
                      (b['right_power'] > b['left_power'] and 4 <= b['result'] <= 6) for b in adjacent)
    unresolved = sum(b['result'] == 0 for b in adjacent)
    summary = dict(revision=DESIGN['revision'], mode='inferred', scoring_version=cp.SCORE_VERSION,
                   representative_npcs=len(samples), calibrated_levels=99, validated_calibration_npcs=99 * 15,
                   level_tier_ranges=len(ranges), battle_count=len(battles),
                   battle_stop_reasons={reason: sum(b['stop_reason'] == reason for b in battles) for reason in sorted({b['stop_reason'] for b in battles})},
                   adjacent_tier_battles=dict(count=len(adjacent), higher_power_wins=strong_wins,
                                              lower_power_wins=len(adjacent) - strong_wins - unresolved, unresolved=unresolved),
                   sample_battle_status={s: sum(n['battle_validation']['status'] == s for n in samples)
                                         for s in ('smoke_passed', 'replay_limit_observed', 'not_sampled')},
                   checks=['unique_ids_and_types', 'slots_and_ownership', 'four_starters_four_battle_reserves', 'growth_and_rebirth_caps', 'realm_prerequisites',
                           'potential_conservation', 'equipment_and_stone_links', 'skill_and_essence_limits',
                           'awakening_prerequisites', 'score_sum', 'idempotence', 'non_overlapping_tiers_at_all_99_levels'],
                   battle_scope='5个等级、3流派同档对局及同流派相邻档对局，每组2种子、交换先后手；不等于胜率校准',
                   official_power_verified=False, production_accounts_modified=False, online_routes_replaced=False)
    files = {'catalog.json': json_text(dict(schema_version=1, revision=DESIGN['revision'], mode='inferred', npcs=samples)),
             'overview.csv': csv_text(overview), 'companions.csv': csv_text(units),
             'level_rules.csv': csv_text([caps(l) for l in range(1, 100)]), 'power_ranges.csv': csv_text(ranges),
             'candidate_pool.json': json_text(candidates), 'battle_checks.csv': csv_text(battles),
             'validation.json': json_text(summary), 'source_manifest.json': json_text(source_manifest())}
    rows = ['# 首批代表等级战力样本范围', '',
            '本表是各代表等级三种流派的实际结算最小值～最大值，不是整个等级段的统一界限，也不是理论养成上限。',
            '逐级闭区间分类见 [power_ranges.csv](power_ranges.csv)。T1最高，T5最低。', '',
            '| 等级段 | 代表等级 | T5 | T4 | T3 | T2 | T1 |', '|---|---:|---:|---:|---:|---:|---:|']
    for level in DESIGN['band_starts']:
        columns = [f'{band(level)[0]}–{band(level)[1]}', str(level)]
        for tier in TIERS:
            r = next(r for r in ranges if r['role_level'] == level and r['tier'] == tier)
            columns.append(f"{r['sample_min']:,}～{r['sample_max']:,}")
        rows.append('| ' + ' | '.join(columns) + ' |')
    files['sample_ranges.md'] = '\n'.join(rows) + '\n'
    rows = ['# 首批 NPC 阵容清单', '',
            '1后位、2前位、3上路、4下路为首发；5～8分别接替1～4。助威不进入此出战列表。',
            '每个样本另有2名背包候补。完整逐仙养成见 [companions.csv](companions.csv)，机器快照见 [catalog.json](catalog.json)。',
            '数据校验覆盖全部样本；对战状态为“通过抽样”“回放限制”或“未抽样”，不能互相替代。', '']
    for level in DESIGN['band_starts']:
        rows += [f'## 角色 {level} 级', '', '| NPC ID | 流派 | 战力 | 首发/替补/助威 | 阵容（阵位:神仙ID） | 对战验证 |',
                 '|---|---|---:|---|---|---|']
        for r in overview:
            if r['role_level'] == level:
                status = {'smoke_passed': '通过抽样', 'replay_limit_observed': '回放限制', 'not_sampled': '未抽样'}[r['battle_validation']]
                rows.append(f"| {r['npc_id']} | {r['archetype']} | {r['power']:,} | {r['starters']}/{r['battle_reserves']}/{r['supports']} | {r['lineup']} | {status} |")
        rows.append('')
    files['rosters.md'] = '\n'.join(rows) + '\n'
    return files, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'analysis/npc_design/v1')
    parser.add_argument('--check', action='store_true', help='Rebuild and compare without modifying artifacts')
    args = parser.parse_args()
    files, summary = export(*build())
    if args.check:
        changed = [name for name, value in files.items()
                   if not (args.output / name).exists() or (args.output / name).read_bytes() != value.encode()]
        if changed:
            raise SystemExit('NPC artifacts are stale: ' + ', '.join(changed))
    else:
        args.output.mkdir(parents=True, exist_ok=True)
        for name, value in files.items():
            (args.output / name).write_bytes(value.encode())
    print(json_text(summary))


if __name__ == '__main__':
    main()
