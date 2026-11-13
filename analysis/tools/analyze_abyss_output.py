"""Audit current Abyss yields with exact probabilities; never open player saves."""
from collections import Counter, defaultdict
import csv
from fractions import Fraction as F
import hashlib
from itertools import permutations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import abyss_balance, activity_abyss, activity_treasure


def read_csv(name):
    with (ROOT / 'analysis/configs' / name).open(encoding='utf-8-sig', newline='') as src:
        return list(csv.DictReader(src))


def pack(n):
    n = F(n)
    return dict(exact=str(n), value=float(n))


def inclusion(weights, draws):
    states = {0: F(1)}
    for _ in range(draws):
        nxt = defaultdict(F)
        for mask, probability in states.items():
            total = sum(w for i, w in enumerate(weights) if not mask & (1 << i))
            for i, w in enumerate(weights):
                if not mask & (1 << i):
                    nxt[mask | (1 << i)] += probability * F(w, total)
        states = nxt
    assert sum(states.values()) == 1
    result = [sum(p for mask, p in states.items() if mask & (1 << i)) for i in range(len(weights))]
    assert sum(result) == draws
    return result


def analyze():
    rules = json.loads((ROOT / 'server_config/activity_rules.json').read_text())
    balance = abyss_balance.load_rules()
    names = {int(x['Ftype_id']): x['name'] for x in read_csv('item_name.csv')}
    items = {int(x['type_id']): x for x in read_csv('item_base.csv')}
    ticks = 86400 // rules['abyss_tick_seconds']
    assert ticks == 288 and rules['timezone_offset_hours'] == 8
    floors = []
    for floor in range(1, 82):
        groups = activity_abyss.DROPS[floor]
        assert [g[0] for g in groups] == [50, 30, 50, 2]
        region = (floor - 1) // 9 + 1
        local = (floor - 1) % 9 + 1
        weights = [0, 0, 0, 2, 5, 5, 10, 10, 20]
        drops = defaultdict(F)
        for index, (outer, entries) in enumerate(groups):
            if index < 3:
                base = (1400, 1441, 1430)[index] + region
                expected = [[5, base, 1, 1, 10]]
                if weights[local - 1]:
                    expected.append([5, base + 1, 1, 1, weights[local - 1]])
                assert entries == expected
            else:
                assert entries == [[5, 1330, 1, 1, 10]]
            total = sum(e[4] for e in entries)
            for typ, tid, lv, n, weight in entries:
                assert typ == 5 and lv == n == 1
                drops[tid] += ticks * F(outer, 132) * F(weight, total) * n
        assert sum(drops.values()) == ticks
        maps = {tid: n for tid, n in drops.items() if 1431 <= tid <= 1440}
        assert sum(maps.values()) == F(1200, 11)
        tier_units = sum((tid - 1430) * n for tid, n in maps.items())
        cap = min(rules['abyss_crystal_tick_cap'], balance['region_crystal_caps'][region - 1])
        crystals = ticks * balance['idle_crystal_multiplier'] * cap
        assert crystals == ticks * abyss_balance.crystal_tick({'role_combat_power': cap * 1000}, {'layer': floor}, rules)
        rewards = abyss_balance.victory_rewards(floor)
        raw = [list(map(int, t.split('|'))) for t in activity_abyss.BOSSES[floor]['prirze_list'].split('/')]
        expected_rewards = [[typ, tid, max(1, n // balance['boss_crystal_divisor']) * balance['boss_crystal_multiplier']
                             if tid == 1441 else n, lv] for typ, tid, lv, n in raw]
        expected_rewards.append([12, 0, balance['boss_silver_base'] + balance['boss_silver_per_floor'] * floor, 1])
        assert rewards == expected_rewards
        boss_items = Counter({})
        boss_crystals = silver = 0
        for typ, tid, n, lv in rewards:
            if tid == 1441:
                boss_crystals += n
            elif typ == 12:
                silver += n
            else:
                boss_items[tid] += n
        floors.append(dict(floor=floor, region=region, local_floor=local,
                           title=activity_abyss.HANG[floor]['title'], power_for_cap=cap * 1000,
                           idle_crystals_daily=crystals,
                           idle_items_daily={str(t): pack(n) for t, n in sorted(drops.items())},
                           map_tier_units_daily=pack(tier_units),
                           drug_xp_daily=pack(sum(n * int(items[t]['experience_plus']) for t, n in drops.items() if 1442 <= t <= 1451)),
                           boss_crystals=boss_crystals, boss_silver=silver, boss_items=dict(boss_items),
                           boss_course_xp=abyss_balance.course_total(floor) - abyss_balance.course_total(floor - 1)))
    probs = inclusion(rules['abyss_map_weights'], 5)
    maps = []
    for i, prize in enumerate(rules['abyss_map_rewards']):
        goods = [activity_treasure.pool(tid, rules)[i] for tid in range(1431, 1441)]
        maps.append(dict(id=prize[1], name=names[prize[1]],
                         ids_by_tier=[p['attach_type'] for p in goods],
                         quantity_by_tier=[p['attach_count'] for p in goods],
                         first_probability=pack(F(rules['abyss_map_weights'][i], sum(rules['abyss_map_weights']))),
                         five_probability=pack(probs[i])))
    random_shop = [p for p in rules['abyss_shop'] if not p['guaranteed']]
    fixed = [p for p in rules['abyss_shop'] if p['guaranteed']]
    slots = rules['abyss_shop_daily_count'] - len(fixed)
    assert slots == 6 and not fixed and len(random_shop) == 8
    total_weight = sum(p['weight'] for p in random_shop)
    shop_probs = defaultdict(F)
    costs = []
    fixed_cost = sum(p['cost'] * p['limit'] for p in fixed)
    for selected in permutations(random_shop, slots):
        probability = F(1)
        remaining = total_weight
        for p in selected:
            probability *= F(p['weight'], remaining)
            remaining -= p['weight']
        for p in selected:
            shop_probs[p['reward'][1]] += probability
        costs.append((fixed_cost + sum(p['cost'] * p['limit'] for p in selected), probability))
    assert sum(p for _, p in costs) == 1 and sum(shop_probs.values()) == slots
    shop = []
    for p in rules['abyss_shop']:
        tid = p['reward'][1]
        probability = F(1) if p['guaranteed'] else shop_probs[tid]
        shop.append(dict(id=tid, name=names[tid], count=p['reward'][2], cost=p['cost'], limit=p['limit'],
                         probability=pack(probability), max_quantity=p['reward'][2] * p['limit'],
                         funded_daily_expectation=pack(probability * p['reward'][2] * p['limit'])))
    boss_total = sum(f['boss_crystals'] for f in floors)
    assert boss_total == 180010
    assert sum(f['boss_silver'] for f in floors) == 74520000
    sources = ['server_config/abyss_rules.json', 'server_config/activity_rules.json',
               'analysis/configs/specter_hang_ouput.csv', 'analysis/configs/specter_boss_config.csv',
               'analysis/configs/item_name.csv', 'analysis/configs/item_base.csv',
               'analysis/configs/specter_druggist_config.csv', 'analysis/configs/specter_top_prize.csv',
               'network_redirect/activity_abyss.py', 'network_redirect/abyss_balance.py',
               'network_redirect/activity_abyss_random.py', 'network_redirect/activity_abyss_npc.py',
               'network_redirect/activity_treasure.py']
    return dict(date='2026-11-13', basis='current working tree; full 24 hours at one floor; no bag losses',
                revisions={k: rules[k] for k in ('abyss_shop_revision', 'abyss_map_revision')},
                balance_revision=balance['revision'], ticks_daily=ticks, floors=floors,
                map_rewards=maps, shop=shop,
                shop_full_cost=dict(min=min(n for n, _ in costs), max=max(n for n, _ in costs),
                                    expectation=pack(sum(n * p for n, p in costs))),
                source_sha256={s: hashlib.sha256((ROOT / s).read_bytes()).hexdigest() for s in sources})


if __name__ == '__main__':
    result = analyze()
    output = ROOT / 'analysis/evidence/abyss/output_20261113.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f"Validated {len(result['floors'])} floors, {len(result['map_rewards'])} map rewards, "
          f"{len(result['shop'])} shop items; wrote {output.relative_to(ROOT)}")
