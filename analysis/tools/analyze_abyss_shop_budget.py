"""Enumerate all current daily shelves and compare idle/first-win budgets."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import permutations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import abyss_balance as balance


def main():
    rules = json.loads((ROOT / 'server_config/activity_rules.json').read_text())
    fixed = [p for p in rules['abyss_shop'] if p['guaranteed']]
    pool = [p for p in rules['abyss_shop'] if not p['guaranteed']]
    draws = rules['abyss_shop_daily_count'] - len(fixed)
    probabilities = defaultdict(F)
    for order in permutations(range(len(pool)), draws):
        chance = F(1); remaining = sum(p['weight'] for p in pool)
        for i in order:
            chance *= F(pool[i]['weight'], remaining)
            remaining -= pool[i]['weight']
        probabilities[tuple(sorted(order))] += chance
    assert sum(probabilities.values()) == 1
    shelves = []
    for selected, chance in probabilities.items():
        products = fixed + [pool[i] for i in selected]
        shelves.append(dict(products=products, probability=chance,
                            full_cost=sum(p['cost'] * p['limit'] for p in products)))
    low = min(s['full_cost'] for s in shelves)
    high = max(s['full_cost'] for s in shelves)

    def assess(budget):
        types, portions = [], []
        clear_chance = F(0)
        for shelf in shelves:
            # Maximizing fully exhausted types: buy cheapest full quotas first.
            spent = count = 0
            for price in sorted(p['cost'] * p['limit'] for p in shelf['products']):
                if spent + price > budget: break
                spent += price; count += 1
            types.append(count)
            # Maximal portions is a different objective, buying cheap units first.
            money = budget; bought = 0
            for p in sorted(shelf['products'], key=lambda p: p['cost']):
                n = min(p['limit'], money // p['cost'])
                bought += n; money -= n * p['cost']
            portions.append(bought)
            if budget >= shelf['full_cost']: clear_chance += shelf['probability']
        return dict(budget=budget, cost_coverage_percent=[min(100,budget/high*100),min(100,budget/low*100)],
                    max_cleared_types_range=[min(types),max(types)],
                    max_portions_range=[min(portions),max(portions)],
                    full_clear_probability=float(clear_chance), full_clear_exact=str(clear_chance))

    regions=[]
    for region in range(9):
        floor=region*9+1
        daily=86400//rules['abyss_tick_seconds']*balance.crystal_tick(
            dict(role_combat_power=10**9),dict(layer=floor),rules)
        rewards=[sum(p[2] for p in balance.victory_rewards(f) if p[:2]==[5,1441])
                 for f in range(floor,floor+9)]
        five=[sum(rewards[i:i+5]) for i in range(5)]
        regions.append(dict(region=region+1,normal=assess(daily),double=assess(daily*2),
            five_wins_crystals=[min(five),max(five)],
            normal_with_five_wins=[assess(daily+min(five)),assess(daily+max(five))],
            double_with_five_wins=[assess(daily*2+min(five)),assess(daily*2+max(five))]))
    result=dict(shop_revision=rules['abyss_shop_revision'],balance_revision=balance.rules()['revision'],
        shelf_count=len(shelves),full_cost_range=[low,high],
        expected_full_cost=float(sum(s['full_cost']*s['probability'] for s in shelves)),
        assumptions='zero starting balance; 24h at region cap; no other income/spending; '
                    '5 first wins within same region are conditional, not recurring',regions=regions)
    path=ROOT/'analysis/evidence/abyss/shop_budget_20261113.json'
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    def span(v):return str(v[0]) if v[0]==v[1] else f'{v[0]}—{v[1]}'
    lines=['| 狱 | 普通魂晶 | 普通预算覆盖 | 普通最多清空种类 | 双倍魂晶 | 双倍预算覆盖 | 双倍最多清空种类 |',
           '|---|---:|---:|---:|---:|---:|---:|']
    for row in regions:
        n,d=row['normal'],row['double']
        def coverage(s):return '100%' if s['cost_coverage_percent']==[100,100] else '—'.join(f'{x:.1f}%' for x in s['cost_coverage_percent'])
        lines.append(f"| 第{row['region']}狱 | {n['budget']:,} | {coverage(n)} | {span(n['max_cleared_types_range'])} | {d['budget']:,} | {coverage(d)} | {span(d['max_cleared_types_range'])} |")
    print('\n'.join(lines))
    print('First-win stage budgets:')
    for row in regions:
        stages=row['normal_with_five_wins']
        print(row['region'],row['five_wins_crystals'],[s['budget'] for s in stages],
              [s['max_cleared_types_range'] for s in stages],
              [s['full_clear_probability'] for s in stages])
    print('Double region 6 full clear:',regions[5]['double']['full_clear_probability'])


if __name__ == '__main__':
    main()
