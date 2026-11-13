"""Recalculate equipment budgets from active tables; never open a player save."""
from collections import Counter
from decimal import Decimal, ROUND_CEILING
from functools import lru_cache
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import equipment as e, formation as f, reborn, summon


def enhance_budget(top):
    costs = {lv: int(f.EQUIP_COST[lv]['star5_money']) for lv in range(1, top)}
    expected = {top: Decimal(0)}
    minimum = {top: 0}
    maximum = {top: 0}
    attempts = {top: Decimal(0)}
    weight_sum = sum(f.EQUIP_WEIGHTS.values())
    for lv in range(top - 1, 0, -1):
        next_levels = [(min(top, lv + step), weight) for step, weight in f.EQUIP_WEIGHTS.items()]
        expected[lv] = costs[lv] + sum(expected[n] * w / weight_sum for n, w in next_levels)
        attempts[lv] = 1 + sum(attempts[n] * w / weight_sum for n, w in next_levels)
        minimum[lv] = costs[lv] + min(minimum[n] for n, _ in next_levels)
        maximum[lv] = costs[lv] + max(maximum[n] for n, _ in next_levels)
    assert maximum[1] == sum(costs.values())
    return dict(top=top, minimum=minimum[1], maximum=maximum[1],
                expectation=str(expected[1]), expected_attempts=str(attempts[1]))


def normal_stone_plan(kind):
    # A reproducible 100%-success plan, using level-1/2 fodder only.
    # Respect the original UI's 250-material limit, below the protocol's 255.
    one = Decimal(e.STONE_VALUES[kind, 1]['worth'])
    two = Decimal(e.STONE_VALUES[kind, 2]['worth'])
    make_two = int((Decimal(e.STONE_VALUES[kind, 1]['cost']) / one).to_integral_value(rounding=ROUND_CEILING))
    rows, raw, silver = [], 1, 0  # Includes the retained target stone.
    for lv in range(1, 10):
        row = e.STONE_VALUES[kind, lv]
        cost = Decimal(row['cost'])
        for n2 in range(251):
            n1 = max(0, int(((cost - n2 * two) / one).to_integral_value(rounding=ROUND_CEILING)))
            if n1 + n2 <= 250:
                break
        assert n1 + n2 <= 250 and n1 * one + n2 * two >= cost
        direct_silver = int(row['silver_cost'])
        raw += n1 + n2 * (make_two + 1)
        silver += direct_silver + n2 * int(e.STONE_VALUES[kind, 1]['silver_cost'])
        rows.append(dict(from_level=lv, level1_fodder=n1, level2_fodder=n2,
                         value=str(n1 * one + n2 * two), required=str(cost), silver=direct_silver))
    return dict(steps=rows, level1_stones=raw, silver=silver,
                direct_upgrade_silver=sum(r['silver'] for r in rows),
                level2_fodder=sum(r['level2_fodder'] for r in rows))


@lru_cache(None)
def stone_tree(kind, level):
    """Count all inputs, including the retained target, down to level 10."""
    if level == 10:
        return Counter({1089 + kind: 1}), Counter()
    materials, operations = (c.copy() for c in stone_tree(kind, level - 1))
    operations[level] += 1
    for part in list(e.STONE_REBORN[kind, level].values())[2].split('/'):
        typ, tid, count, mat_level = map(int, part.split('|'))
        assert typ == 5
        if tid in e.STONES:
            sub, ops = stone_tree(e.STONES[tid], mat_level)
            materials.update({t: n * count for t, n in sub.items()})
            operations.update({lv: n * count for lv, n in ops.items()})
        else:
            assert mat_level == 1
            materials[tid] += count
    return materials, operations


def equipment_budget(kind):
    materials, advance_rows, cast_rows = Counter(), [], []
    essence = 1309 + kind
    for advance in range(10):
        n = sum(int(f.STAR_COST[5, star][advance].split('|')[kind - 1]) for star in range(1, 8))
        stage = Counter({essence: n})
        for part in f.ADVANCE_COST[5, advance + 1][{1: 'wuqi_cost', 2: 'fangyu_cost', 3: 'fabao_cost'}[kind]].split('/'):
            tid, count = map(int, part.split('|'))
            stage[tid] += count
        materials.update(stage)
        advance_rows.append(dict(to_advance=advance + 1, materials=dict(stage)))
    for part in list(reborn.EQUIP[kind].values())[1].split('/'):
        typ, tid, level, count = map(int, part.split('|'))
        assert typ == 5 and level == 1
        materials[tid] += count
    for level in range(2, max(lv for k, lv in reborn.CAST if k == kind) + 1):
        stage = Counter()
        for part in list(reborn.CAST[kind, level].values())[2].split('/'):
            typ, tid, mat_level, count = map(int, part.split('|'))
            assert typ == 5 and mat_level == 1
            stage[tid] += count
        materials.update(stage)
        cast_rows.append(dict(to_level=level, materials=dict(stage)))
    materials[1369] += 20  # equipment_crafting.six_star
    body = materials.copy()
    materials[1093] += 4  # six-star quality-five equipment, initially zero holes
    stone, operations = stone_tree(kind, e.STONE_MAX_LEVEL[kind])
    materials.update({t: n * 4 for t, n in stone.items()})
    normal = normal_stone_plan(kind)
    return dict(kind=kind, advance=advance_rows, cast=cast_rows, body_materials=dict(body),
                complete_materials_with_level10_stones=dict(materials),
                single_max_stone=dict(stone), single_max_stone_operations=dict(operations),
                normal_stone_plan=normal,
                four_holes_level1_stones=normal['level1_stones'] * stone[1089 + kind] * 4,
                four_holes_normal_silver=normal['silver'] * stone[1089 + kind] * 4)


def conversion_budget():
    recipes = {}
    for row in summon.rows('material_transform.csv'):
        if row['category'] not in ('4', '5'):
            continue
        src = list(map(int, list(row.values())[1].split('|')))
        cost = list(map(int, list(row.values())[2].split('|')))
        dst = list(map(int, list(row.values())[4].split('|')))
        assert dst[3] == 1 and cost[0] == 12
        recipes[dst[1]] = (src[1], src[3], cost[3])
    # Replace only the spiritual-tool/crystal component of the direct ledger.
    demand = Counter({t: n for t, n in equipment_budget(1)['body_materials'].items()
                      if t in (1313, 1314, 1320, 1321, 1322, 1323, 1334, 1335)})
    operations, silver = Counter(), 0
    for tid in (1334, 1314, 1335, 1323, 1322, 1321):
        n = demand.pop(tid)
        src, count, price = recipes[tid]
        demand[src] += count * n
        operations[tid] = n
        silver += n * price
    return dict(raw_materials=dict(demand), output_counts=dict(operations), silver=silver)


def main():
    caps = {int(r['top_level']) for r in f.ITEMS.values()
            if int(r['main_type']) in (1, 2, 3) and int(r['quality']) == 5}
    assert len(caps) == 1
    template_cap = caps.pop()
    cap = min(template_cap, max(f.LEVELS) * 2)
    report = dict(date='2026-11-13', role_cap=max(f.LEVELS), template_cap=template_cap,
                  reachable_enhancement=enhance_budget(cap),
                  template_only_enhancement=enhance_budget(template_cap),
                  equipment=[equipment_budget(k) for k in (1, 2, 3)],
                  basic_material_conversion=conversion_budget())
    out = ROOT / 'analysis/evidence/equipment/max_cost_20261113.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
