#!/usr/bin/env python3
"""Static endgame NPC designs; no database, backend registration or APK writes."""
import argparse
import copy
import hashlib
import itertools
import json
import random
import sys
from collections import Counter
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools import build_npc_catalog as b
from network_redirect import fate_rebuild as fr, activity_home as home, combat_loadout

OUT = ROOT / 'analysis/npc_design/extreme'
NOW = 1793548800  # 2026-11-02 00:00 Asia/Shanghai, deterministic settlement only.
ROSTERS = {
    'attack': [5022, 5034, 5027, 5046, 5052, 5048, 5021, 5013],
    'magic': [5024, 5051, 5046, 5025, 5021, 5053, 5013, 5023],
    'endurance': [5044, 5053, 5023, 5036, 5051, 5034, 5048, 5025],
}
# P is progression, E is measured power. Never assume they are interchangeable.
PROFILES = [
    dict(stage='P1', level=400, evolve=249, home=30, active=0, soul=0, body=0, stone=10),
    dict(stage='P2', level=450, evolve=299, home=35, active=2, soul=30, body=10, stone=11),
    dict(stage='P3', level=500, evolve=349, home=40, active=4, soul=50, body=30, stone=12),
    dict(stage='P4', level=550, evolve=399, home=45, active=6, soul=70, body=50, stone=12),
    dict(stage='P5', level=600, evolve=449, home=50, active=8, soul=85, body=75, stone=13),
    dict(stage='P6', level=600, evolve=499, home=50, active=8, soul=100, body=100, stone=14),
]
NAMES = {
    'attack': ['破岳长风', '逐日赤霄', '凌霄问剑', '诛邪天衡', '无极照夜', '太初劫锋'],
    'magic': ['听潮玄月', '烛天流火', '星河渡厄', '九曜归墟', '天衍无相', '混元万法'],
    'endurance': ['镇岳青岚', '不动禅心', '玄武守真', '万劫莲生', '长生照海', '永劫太玄'],
}
LABELS = {'E6':'极高入门', 'E5':'极高精锐', 'E4':'极高宗师',
          'E3':'极高霸主', 'E2':'极高至尊', 'E1':'极高绝巅'}


def allocate(c, arch, percent):
    fr.refresh(c)
    total = b.budget(c) + int(c.get('fate_rebuilding_culture_point', 0))
    spent = total * percent // 100
    weights = [35, 15, 45, 5] if c['order'] in (2, 6) else b.DESIGN['archetypes'][arch]['culture_weights']
    amounts = [spent * w // 100 for w in weights]
    amounts[weights.index(max(weights))] += spent - sum(amounts)
    c.update({s + '_plus': v for s, v in zip(b.f.STATS, amounts)})
    c['culture_point'] = total - spent


def fate_plan(c, profile, arch):
    """Cost-derived synthetic design ledger, NOT a record of player transactions."""
    c['fate_rebullding_state'] = 1
    ledgers, passive = {}, Counter()
    for part, stem in fr.PARTS.items():
        target = min(profile['soul'] if part <= 3 else profile['body'], fr.MAX_LEVEL[part])
        c[stem + '_level'], c[stem + '_stars'] = target, 0
        ledger = Counter()
        for level in range(target):
            for star in range(1, fr.star_count(part) + 1):
                tokens = list(map(int, fr.COSTS[part, level, star].split('|')))
                mode = tokens[0]
                if mode == 3:
                    selected = dict(zip(tokens[1::2], tokens[2::2]))
                else:
                    candidates = tokens[1:-1]
                    if mode == 2:
                        attr = 377 if c['order'] in (2, 6) or arch == 'endurance' else 375 if arch == 'magic' else 376
                        tid = next(t for t in candidates if fr.PASSIVES[t][0] == attr)
                    else:
                        tid = candidates[0]
                    selected = {tid: tokens[-1]}
                ledger.update(selected)
                if mode == 2:
                    for tid, n in selected.items():
                        attr, value = fr.PASSIVES[tid]
                        passive[str(attr)] += value * n
        ledgers[str(part)] = {str(t): n for t, n in sorted(ledger.items())}
    c['fate_materials'] = ledgers
    c['fate_passive_bonuses'] = {k: float(v) for k, v in passive.items()}
    tank = c['order'] in (2, 6) or arch == 'endurance'
    c['fate_choices'] = {'1': 379 if tank else 378,
                         '2': 369 if c['order'] in (2, 6) else 366 if arch in ('magic', 'endurance') else 368}
    fr.refresh(c)


def generate(index, arch):
    p = PROFILES[index]
    role = dict(role_id=960000001 + index * 3 + b.ARCHES.index(arch), name=NAMES[arch][index],
                level=99, corteges=[], attachments=[], summon={'next_id': 1},
                reborn_layer=4, max_combat_power=0)
    hs = home.storage(role)
    hs.update(level=2, build={'1':p['home'], '2':p['home'], '3':p['home'], '4':0, '5':0})
    role['cortege_limit_plus'] = int(home.BUILD[1][p['home']]['coretege_limit_plus'])
    role['hole_hp_plus'] = home.point(hs)
    for order, tid in enumerate(ROSTERS[arch], 1):
        c = b.make_companion(role, arch, 'T1', tid, order=order)
        c.update(level=p['level'], evolve_level=p['evolve'], reborn_layer=9, level_culture_version=3)
        if order <= p['active']:
            fate_plan(c, p, arch)
        allocate(c, arch, 95)
    used = set(ROSTERS[arch])
    for pos in range(1, 17):
        tid = b.choose(arch, 4, used)
        used.add(tid)
        c = b.make_companion(role, arch, 'T1', tid, support=pos)
        c.update(level=200, evolve_level=49, level_culture_version=3)
        allocate(c, arch, 75)
        name = b.cheer.NAMES[pos - 1]
        role['cheer_' + name + '_level'] = 10
        role['cheer_' + name + '_effect'] = pos if pos <= 8 else 0
    for _ in range(2):
        tid = b.choose(arch, 3, used)
        used.add(tid)
        c = b.make_companion(role, arch, 'T1', tid, reserve=True)
        c.update(level=100, evolve_level=0, level_culture_version=3)
        allocate(c, arch, 0)
    b.cheer.prepare(role, b.CHEER)
    b.f.prepare(role, b.RULES)
    for c in role['corteges']:
        if not c['order']:
            continue
        b.outfit(role, c, arch, 'T1')
        essences = [i for i in role['attachments'] if i.get('owner_id') == c['id'] and i['type_id'] in b.cp.ESSENCE_SCORES]
        for item in essences:
            item['level'] = 5
        if c.get('fate_rebullding_state'):
            family = fr.ESSENCE_FAMILY[c['type']]
            families = {i['type_id'] % 100 for i in essences}
            if family not in families:
                if 5 in fr.essence_slots(c):
                    b.attach(role, 5, 10200 + family, level=5, owner_id=c['id'], ext_skill_pos=5)
                else:
                    essences[-1]['type_id'] = 10200 + family
            elif 5 in fr.essence_slots(c):
                extra = next(x for x in (14, 10, 6, 8, 18) if x not in families)
                b.attach(role, 5, 10200 + extra, level=5, owner_id=c['id'], ext_skill_pos=5)
    for item in role['attachments']:
        if item['attach_type'] == 5 and item['type_id'] in (1090, 1091, 1092):
            item['level'] = p['stone']
            owner = next(i for i in role['attachments'] if i['id'] == item['owner_id'])
            owner['stone1_level'] = p['stone']
    b.cp.recalculate(role, b.RULES, now=NOW)
    return dict(npc_id=f"npc_extreme_{p['stage'].lower()}_{arch}", stage=p['stage'], archetype=arch,
                status='design_only', role=role)


def validate(npc, *, expected_roster=26):
    role = npc['role']
    members, items = role['corteges'], role['attachments']
    assert len(members) == expected_roster and len({c['type'] for c in members}) == expected_roster
    ids = [x['id'] for x in members + items]
    assert len(ids) == len(set(ids))
    assert sorted(c['order'] for c in members if c['order']) == list(range(1, 9))
    assert sorted(c['cheer_order'] for c in members if c['cheer_order']) == list(range(1, 17))
    assert not role.get('combat_sources')
    assert role['hole_hp_plus'] == home.point(role['activity']['home'])
    for c in members:
        assert not c.get('combat_sources') and not (c['order'] and c['cheer_order'])
        assert 1 <= c['level'] <= b.f.companion_level_cap(role, b.quality(c['type']))
        assert 0 <= c['evolve_level'] <= 499
        assert c['culture_point'] + sum(c[s + '_plus'] for s in b.f.STATS) == b.budget(c) + int(c.get('fate_rebuilding_culture_point', 0))
        assert min(c['culture_point'], *(c[s + '_plus'] for s in b.f.STATS)) >= 0
        if c['reborn_layer']:
            assert c['type'] in b.reborn.CORTS and c['reborn_layer'] == 9
        if c.get('fate_rebullding_state'):
            assert c['type'] in fr.ACTIVE and c['reborn_layer'] == 9 and role['reborn_layer'] == 4
            assert all(0 <= fr.progress(c, part)[0] <= fr.MAX_LEVEL[part] and fr.progress(c, part)[1] == 0 for part in fr.PARTS)
            # Construct a round-robin path satisfying the seven-soul gates.
            reached = {part:0 for part in range(4, 11)}
            while any(reached[p] < fr.progress(c, p)[0] for p in reached):
                advanced = False
                for part in reached:
                    level = reached[part]
                    if level < fr.progress(c, part)[0] and (level <= 30 or sum(reached.values()) + 7 >= (100 if level <= 60 else 200)):
                        reached[part] += 1
                        advanced = True
                assert advanced, 'unreachable seven-soul progression'
        innate = [i for i in items if i.get('innate_owner_id') == c['id']]
        assert len(innate) == 1 and innate[0]['type_id'] == int(b.f.BASES[c['type']]['chushijineng'])
        ess = [i for i in items if i.get('owner_id') == c['id'] and i['type_id'] in b.cp.ESSENCE_SCORES]
        assert len({i['ext_skill_pos'] for i in ess}) == len(ess) == len({i['type_id'] % 100 for i in ess})
        assert all(i['ext_skill_pos'] in fr.essence_slots(c) and 1 <= i['level'] <= 5 for i in ess)
        assert not ({7, 15} <= {i['type_id'] % 100 for i in ess})
        if c.get('fate_rebullding_state'):
            assert fr.ESSENCE_FAMILY[c['type']] in {i['type_id'] % 100 for i in ess}
        assert c['combat_power'] == b.cp.score_panel(c, b.RULES['combat_weights'], b.cp.essence_score(role, c)['total'])
        assert all(0 <= c[s] < b.cp.LIMIT for s in b.f.STATS)
    for rule in b.REBORN['realms']:
        assert role['level'] >= rule['level']
        assert sum(c['reborn_layer'] >= rule['required_layer'] for c in members) >= rule['count']
    for pos in range(1, 9):
        skills = [i for i in items if i['attach_type'] == 6 and i.get('equip_order') == pos]
        assert len(skills) == len({i['type_id'] for i in skills}) == len({i['equip_pos'] for i in skills}) == 3
    for i in items:
        if i['attach_type'] == 6:
            assert int(b.f.SKILLS[i['type_id']]['begin_level']) <= i['level'] <= int(b.f.SKILLS[i['type_id']]['top_level'])
            if i.get('awaken'):
                assert i['level'] == 10 and any(c['id'] == i['innate_owner_id'] and c['reborn_layer'] == 9 for c in members)
        elif i['type_id'] in b.reborn_stars.STARS:
            c = next(c for c in members if c['id'] == i['owner_id'])
            assert c['reborn_layer'] >= b.reborn_stars.OPEN[i['ext_awaken_pos']] and 1 <= i['level'] <= 10
        elif i['type_id'] in b.f.ITEMS and int(b.f.ITEMS[i['type_id']]['main_type']) in (1, 2, 3):
            cfg = b.f.ITEMS[i['type_id']]
            assert i['level'] <= min(role['level'] * 2, int(cfg['top_level']))
            assert int(cfg['quality']) == 5 and i['advance_level'] == 10 and i['cast_level'] == 4 and i['reborn_bit'] == i['star_level'] == 1
            stones = [s for s in items if s.get('owner_id') == i['id']]
            assert len(stones) == i['drill_count'] == 1
            assert stones[0]['type_id'] == 1089 + int(cfg['main_type']) and 1 <= stones[0]['level'] == i['stone1_level'] <= 14
    assert role['role_combat_power'] == sum(c['combat_power'] for c in members if c['order']) < b.cp.LIMIT
    before = copy.deepcopy(role)
    b.cp.recalculate(role, b.RULES, now=NOW)
    assert role == before


def battles(npcs):
    pairs = [('same_tier', a, z) for tier in LABELS for a, z in itertools.combinations([n for n in npcs if n['tier'] == tier], 2)]
    ordered = sorted(npcs, key=lambda n:n['role']['role_combat_power'])
    pairs += [('tier_boundary', ordered[i-1], ordered[i]) for i in range(3, 18, 3)]
    pairs += [('same_roster_progression', a, z) for arch in b.ARCHES for a, z in zip(
        [n for n in npcs if n['archetype'] == arch][:-1], [n for n in npcs if n['archetype'] == arch][1:])]
    rows = []
    for kind, a, z in pairs:
        for seed in (17, 83):
            for left, right in ((a,z),(z,a)):
                rng = random.Random(seed)
                ar, br = copy.deepcopy(left['role']), copy.deepcopy(right['role'])
                with patch('network_redirect.combat.secrets.randbelow', side_effect=rng.randrange):
                    engine = b.combat_engine.Battle(ar, (combat_loadout.player_units(ar), combat_loadout.player_units(br)), b.journey.load_rules(), slots=8)
                    assert all(u['order'] <= 4 for side in (1,2) for u in engine.fielded(side))
                    error = ''
                    try:
                        result, _, actions = engine.run()
                    except TypeError as exc:
                        # Expose the existing float/Fraction fate-combo failure.
                        # Do not patch production combat or silently drop the god.
                        if str(exc) != 'both arguments should be Rational instances':
                            raise
                        rows.append(dict(kind=kind, left=left['npc_id'], right=right['npc_id'], seed=seed,
                                         left_power=ar['role_combat_power'], right_power=br['role_combat_power'],
                                         result='', action_count=len(engine.actions), stop_reason='runtime_error', error=str(exc)))
                        continue
                assert actions and all(hp >= 0 for side in actions.final_hp.values() for hp in side.values())
                rows.append(dict(kind=kind, left=left['npc_id'], right=right['npc_id'], seed=seed,
                                 left_power=ar['role_combat_power'], right_power=br['role_combat_power'],
                                 result=result, action_count=len(actions), stop_reason=actions.stop_reason, error=error))
    return rows


def export(npcs, ranges, checks):
    overview, companions, lines = [], [], ['# 极高战力 NPC 逐名配置', '',
        '后续扩充：[新增100名多样阵容](../extreme_expansion/逐名配置.md)。本页保留原18名模板，合计118名设计NPC；新增批次另按原E档边界归档。', '',
        '生成日期：2026-11-02。设计库未接入游戏；数字角色 ID 为设计预留，不是现有玩家查询 ID。', '',
        '所有角色99级、四重境界；4首发＋4替补＋16助威＋2背包候补。E1最强、E6最弱；P只表示养成阶段。', '',
        '同流派的六个阶段共用阵容，作为可比较的成长版本，不计作六种不同组合。具体分档、用途及边界见[设计说明](../../../docs/极高战力NPC设计说明_600级499飞升与逆天改命.md)。', '']
    def view(i):
        names = b.SKILL_NAMES if i['attach_type'] == 6 else b.ITEM_NAMES
        return f"{names.get(i['type_id'], str(i['type_id']))}({i['type_id']}) Lv{i['level']}"
    for npc in sorted(npcs, key=lambda n:-n['role']['role_combat_power']):
        r = npc['role']; p = next(p for p in PROFILES if p['stage'] == npc['stage'])
        overview.append(dict(npc_id=npc['npc_id'], reserved_role_id=r['role_id'], name=r['name'], tier=npc['tier'],
                             stage=npc['stage'], archetype=npc['archetype'], power=r['role_combat_power'],
                             level=p['level'], evolve=p['evolve'], fate_count=p['active'], status='design_only'))
        lines += [f"## {r['name']}｜{npc['tier']} {LABELS[npc['tier']]}｜{r['role_combat_power']:,}", '',
                  f"设计ID：`{npc['npc_id']}`；预留角色ID：`{r['role_id']}`；{npc['stage']}，{b.DESIGN['archetypes'][npc['archetype']]['name']}。", '',
                  f"主殿／药园／佛堂均{p['home']}级，洞府生命加成{r['hole_hp_plus']:,}；逆天激活{p['active']}名，顺序为阵位1→8。", '',
                  '| 阵位 | 神仙 | 等级／飞升／转生 | 三魂层数 | 七魄层数 | 生命 | 攻击 | 防御 | 法力 | 战力 |',
                  '|---|---|---|---|---|---:|---:|---:|---:|---:|']
        for c in r['corteges']:
            if not c['order']: continue
            soul = '/'.join(str(fr.progress(c,k)[0]) for k in range(1,4))
            body = '/'.join(str(fr.progress(c,k)[0]) for k in range(4,11))
            lines.append(f"| {c['order']} | {b.NAMES[c['type']]} {c['type']} | {c['level']}/{c['evolve_level']}/{c['reborn_layer']} | {soul} | {body} | " + ' | '.join(f"{c[s]:,}" for s in (*b.f.STATS,'combat_power')) + ' |')
        lines += ['', '### 逐仙装备、法术与培养', '', '四维培养顺序：生命／攻击／防御／法力。装备统一强化198、进阶10、封神、铸造4、六星，每件1孔；命星仅1号槽。', '']
        for c in r['corteges']:
            owned = [i for i in r['attachments'] if i.get('owner_id') == c['id']]
            equipped = [i for i in r['attachments'] if c['order'] and i.get('equip_order') == c['order']]
            ess = [i for i in owned if i['type_id'] in b.cp.ESSENCE_SCORES]
            stars = [i for i in owned if i['type_id'] in b.reborn_stars.STARS]
            gear = [i for i in equipped if i['attach_type'] == 5]
            skills = [i for i in equipped if i['attach_type'] == 6]
            row = dict(npc_id=npc['npc_id'], order=c['order'], cheer_order=c['cheer_order'], type=c['type'], name=b.NAMES[c['type']],
                       level=c['level'], evolve=c['evolve_level'], reborn=c['reborn_layer'], power=c['combat_power'],
                       culture_budget=b.budget(c)+int(c.get('fate_rebuilding_culture_point',0)), culture_remaining=c['culture_point'],
                       culture='/'.join(str(c[s+'_plus']) for s in b.f.STATS),
                       souls='/'.join(str(fr.progress(c,k)[0]) for k in range(1,4)),
                       bodies='/'.join(str(fr.progress(c,k)[0]) for k in range(4,11)),
                       equipment=' / '.join(view(i) for i in gear), skills=' / '.join(view(i) for i in skills),
                       essences=' / '.join(view(i) for i in ess), stars=' / '.join(view(i) for i in stars))
            companions.append(row)
            if not c['order']: continue
            choice = c.get('fate_choices',{})
            lines += [f"**{c['order']}号 {b.NAMES[c['type']]}**", '',
                      f"- 装备：{row['equipment']}；各镶1枚{p['stone']}级对应部位灵石。",
                      '- 法术：' + ' / '.join(view(i) + f"，觉醒方向{i.get('awaken',0)}" for i in skills) + '。',
                      f"- 精魄：{row['essences']}；命星：{row['stars']}。",
                      f"- 培养：{row['culture']}；总潜力{row['culture_budget']:,}，剩余{c['culture_point']:,}。",
                      f"- 逆天：{'已激活' if c.get('fate_rebullding_state') else '未激活'}；天魂选择{choice.get('1',0)}，命魂选择{choice.get('2',0)}；中枢被动加成{json.dumps(c.get('fate_passive_bonuses',{}),ensure_ascii=False)}。", '']
        lines += ['### 助威与背包', '', '| 助威位 | 神仙 | 等级／飞升 | 八卦等级 | 受益阵位 |', '|---|---|---|---|---|']
        for c in r['corteges']:
            if c['cheer_order']:
                lines.append(f"| {c['cheer_order']} | {b.NAMES[c['type']]} {c['type']} | 200/49 | 10 | {(c['cheer_order']-1)%8+1} |")
        lines += ['', '助威使用75%潜力，不转生、不逆天、不穿普通装备；其自带法术保持1级。背包候补：' + '、'.join(b.NAMES[c['type']] for c in r['corteges'] if not c['order'] and not c['cheer_order']) + '，均100级、0飞升、0转生、未培养。', '']
    summary = dict(npc_count=len(npcs), active_companions=144, support_companions=288, idle_companions=36,
                   unique_rosters=3, data_validation='passed', battle_validation='failed' if any(c['stop_reason']=='runtime_error' for c in checks) else 'completed', battle_count=len(checks),
                   battle_stop_reasons=dict(Counter(c['stop_reason'] for c in checks)),
                   battle_scope='in-memory production engine; no protocol replay or native UI validation',
                   backend_registered=False, live_database_touched=False,
                   checks=['level_and_home_cap','499_evolution_cap','rebirth_and_fate_eligibility','seven_soul_reachable_path',
                           'potential_conservation_current_v3_plus_fate','essence_slots_and_families','equipment_and_stone_links',
                           'skill_and_star_prerequisites','unique_ids','power_sum','idempotence','no_int32_saturation'])
    manifest = b.source_manifest()
    paths = [Path(__file__), ROOT/'network_redirect/fate_rebuild.py', ROOT/'network_redirect/combat_loadout.py', ROOT/'network_redirect/activity_home.py', ROOT/'network_redirect/summon.py']
    paths += list((ROOT/'analysis/configs/immortal_hotupdate').glob('*.csv')) + list((ROOT/'analysis/configs/fate_rebuild').glob('*.csv'))
    paths += [ROOT/'server_config/fate_rebuild_attributes.json']
    paths += [Path(module.__file__) for name,module in tuple(sys.modules.items())
              if name.startswith('network_redirect.') and getattr(module, '__file__', '').endswith('.py')]
    for p in paths: manifest[str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return {'catalog.json':b.json_text(dict(schema_version=1,status='design_only',profiles=PROFILES,npcs=npcs)),
            'overview.csv':b.csv_text(overview), 'companions.csv':b.csv_text(companions),
            'power_ranges.csv':b.csv_text(ranges), 'battle_checks.csv':b.csv_text(checks),
            'validation.json':b.json_text(summary), 'source_manifest.json':b.json_text(manifest),
            '逐名配置.md':'\n'.join(lines)+'\n'}, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    npcs = [generate(i,a) for i in range(6) for a in b.ARCHES]
    for n in npcs: validate(n)
    ordered = sorted(npcs, key=lambda n:n['role']['role_combat_power'])
    # Three calibration samples per measured tier, midpoint integer boundaries.
    powers = [n['role']['role_combat_power'] for n in ordered]
    baseline = 5174415  # Frozen rank_elite/details.md, not a universal T1 ceiling.
    assert powers[0] > baseline
    edges = [baseline] + [(powers[i-1]+powers[i])//2 for i in range(3,18,3)]
    ranges = []
    for group in range(6):
        tier = f'E{6-group}'
        for n in ordered[group*3:group*3+3]: n['tier'] = tier
        ranges.append(dict(tier=tier,label=LABELS[tier],lower=edges[group]+1,
                           upper=edges[group+1] if group<5 else '',
                           sample_min=powers[group*3],sample_max=powers[group*3+2],count=3))
    checks = battles(npcs)
    for n in npcs:
        n['battle_status'] = 'runtime_error_observed' if any(
            r['stop_reason'] == 'runtime_error' and n['npc_id'] in (r['left'],r['right']) for r in checks) else 'sampled_engine_only'
        n['fate_combo_risk'] = any(c['type'] == 5021 and c.get('fate_rebullding_state') for c in n['role']['corteges'] if c['order'])
    files, summary = export(npcs,ranges,checks)
    if args.check:
        different = [name for name,content in files.items() if not (OUT/name).exists() or (OUT/name).read_bytes() != content.encode('utf-8')]
        assert not different, f'generated artifacts differ: {different}'
    else:
        OUT.mkdir(parents=True,exist_ok=True)
        for name,content in files.items(): (OUT/name).write_text(content)
    print(json.dumps(summary,ensure_ascii=False))
    print(b.csv_text(ranges))


if __name__ == '__main__': main()
