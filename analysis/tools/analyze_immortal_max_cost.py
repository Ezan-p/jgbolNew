"""Audit one immortal's five requested progression systems from active tables.

No player database is opened. Run from the repository root; results are written
only to analysis/evidence/immortal_max_cost_20261113.json.
"""
from collections import Counter
from decimal import Decimal, ROUND_CEILING
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import formation as f, immortal as im, reborn as rb
from network_redirect import reborn_stars as stars, fate_rebuild as fate, summon


def ceil_div(a, b):
    return (a + b - 1) // b


def materials(raw):
    result = Counter()
    for part in raw.split('/'):
        kind, tid, level, count = map(int, part.split('|'))
        assert kind == 5 and level == 1
        result[tid] += count
    return result


def skill_plan(quality):
    """100% route: feed level-1/2 quality-5 spells, <=500 per request.

    One level-2 quality-5 feeder costs three level-1 books in total (one
    retained target plus two feeders), and is worth 3. No silver is charged.
    This is a feasible deterministic route, not a global cost optimum.
    """
    assert Decimal(f.SKILL_WORTH[1]['quality_worth5']) == 1
    assert Decimal(f.SKILL_WORTH[2]['quality_worth5']) == 3
    assert Decimal(f.SKILL_COST[1]['quality5_cost']) == 2
    rows = []
    for lv in range(1, 10):
        need = Decimal(f.SKILL_COST[lv][f'quality{quality}_cost'])
        for n2 in range(501):
            n1 = int(max(Decimal(0), need - 3 * n2).to_integral_value(rounding=ROUND_CEILING))
            if n1 + n2 <= 500:
                break
        assert n1 + n2 <= 500 and n1 + 3 * n2 >= need
        rows.append(dict(from_level=lv, need=str(need), level1=n1,
                         level2=n2, raw_level1=n1 + 3 * n2))
    return dict(quality=quality, steps=rows, raw_level1=sum(x['raw_level1'] for x in rows))


def main():
    names = {int(x['Ftype_id']): x['name'] for x in summon.rows('item_name.csv')}
    xp = lambda q, a, b: sum(f.EXPERIENCE[q, lv] for lv in range(a, b))
    assert f.EXPERIENCE_CAPS == dict.fromkeys(range(1, 6), 600)
    assert set(f.EVOLVE_COST) == set(range(1, 500))
    assert len(rb.VEINS) == 81 and len(rb.LAYERS) == 9
    assert len(stars.OPEN) == 6
    layers, vein_choices, fixed = [], [], Counter()
    for layer, row in sorted(rb.LAYERS.items()):
        direct = materials(row['consum_list'])
        vein_fixed = Counter()
        grouped = Counter()
        for pulse in range(1, 10):
            vein = rb.VEINS[layer, pulse]
            allowed = materials(vein['consume_list'])
            n = int(vein['fixed_count(fix>0|unfix=0)'])
            if n:
                qs = {int(f.ITEMS[t]['quality']) for t in allowed}
                assert len(qs) == 1
                quality = qs.pop()
                grouped[quality] += n
                vein_choices.append(dict(layer=layer, pulse=pulse, count=n,
                                         quality=quality, allowed=dict(allowed),
                                         names={t: names[t] for t in allowed}))
            else:
                vein_fixed.update(allowed)
        fixed.update(direct + vein_fixed)
        layers.append(dict(layer=layer, min_level=int(row['min_level']),
                           reset_level=int(row['reset_level']), direct=dict(direct),
                           vein_fixed=dict(vein_fixed), essence_by_quality=dict(grouped),
                           lost_xp=xp(5, int(row['reset_level']), int(row['min_level']))))
    total_xp = xp(5, 1, 600) + sum(x['lost_xp'] for x in layers)
    evolve_bands = []
    for lo, hi in [(1, 8), (9, 25), (26, 30), (31, 35), (36, 40),
                   (41, 199), (200, 299), (300, 399), (400, 499)]:
        evolve_bands.append(dict(first=lo, last=hi, count=hi-lo+1,
                                 per_step=[f.EVOLVE_COST[n] for n in range(lo, hi+1)]
                                 if lo == 1 else f.EVOLVE_COST[lo],
                                 souls=sum(f.EVOLVE_COST[n] for n in range(lo, hi+1))))
    fifth = Counter({1371: 20})
    for lv in range(50):
        for step in range(1, 10):
            raw = list(map(int, fate.COSTS[3, lv, step].split('|')))
            assert raw[0] == 3
            fifth.update(dict(zip(raw[1::2], raw[2::2])))
    essence_xp = sum(im.UPGRADE_COST.values())
    eligible = sorted(rb.CORTS)
    assert all(int(f.BASES[t]['quality']) == 5 for t in eligible)
    result = dict(
        date='2026-11-13', scope='active workspace; owned level-1 quality-5 immortal; account prerequisites separate',
        example_type=5022, eligible_rebirth=eligible, eligible_fifth=sorted(fate.ACTIVE),
        levels={q: {top: xp(q, 1, top) for top in (165, 200, 300, 400, 500, 600)} for q in range(1, 6)},
        total_xp_with_nine_rebirths=total_xp, lost_xp=sum(x['lost_xp'] for x in layers),
        experience_items=[dict(id=t, name=names[t], xp=int(v['experience_plus']),
                               count_to_600=ceil_div(total_xp, int(v['experience_plus'])))
                          for t,v in f.ITEMS.items() if int(v['main_type']) == 5
                          and int(v['sub_type']) in (99,100) and int(v['experience_plus']) > 0],
        evolution=dict(souls=sum(f.EVOLVE_COST.values()), bands=evolve_bands,
                       silver_if_all_exchanged=sum(f.EVOLVE_COST.values())*im.load_rules()['exchange_silver_per_soul']['5'],
                       exchange_rates={t: im.EXCHANGE.get(t) for t in eligible}),
        rebirth=dict(layers=layers, fixed=dict(fixed), choices=vein_choices,
                     essence_totals=dict(sum((Counter(x['essence_by_quality']) for x in layers), Counter()))),
        essence=dict(per_item=essence_xp, stages=im.UPGRADE_COST,
                     four=4*essence_xp, five=5*essence_xp, fifth_unlock=dict(fifth),
                     with_veins_four=fixed[10000]+4*essence_xp,
                     with_veins_five=fixed[10000]+5*essence_xp, lock_gold=im.LOCK_COST),
        stars=dict(per_quality={q:sum(vals) for q,vals in stars.EXP.items()},
                   steps=stars.EXP, six_purple=6*sum(stars.EXP[5]), open=stars.OPEN,
                   divination_silver={p:int(row['consume_silver']) for p,row in stars.POSITIONS.items()}),
        skill_prerequisite={q:skill_plan(q) for q in range(1,6)},
        shared_realm=rb.load_rules()['realms'],
        material_names={t:names[t] for t in sorted(set(fixed) | set(fifth) | {10000,10300,1378})},
    )

    # Exercise real feed/rebirth settlement on a detached in-memory character.
    # Keep overage between turns; compare nine actual experience losses and
    # the final number of books against the closed-form budget.
    c = dict(id=1, type=5022, level=1, cur_exp=0, culture_point=0,
             reborn_layer=0, reborn_vein_level=0, reborn_plus_type=1)
    role = dict(level=99, reborn_layer=4, cortege_limit_plus=400,
                corteges=[c], attachments=[])
    book = 1080
    inventory = dict(id=1, type_id=book, attach_type=5, count=100000, level=1)
    role['attachments'].append(inventory)
    rules = f.load_rules()
    fed = 0
    observed_losses = []
    for layer in layers:
        need = xp(5, c['level'], layer['min_level']) - c['cur_exp']
        n = ceil_div(int(need), int(f.ITEMS[book]['experience_plus']))
        f.feed(role, dict(flag=1, first_send=True, cortege_id=1, roll_count=1,
                         roll_list=[dict(type_id=book,count=n)]), rules)
        fed += n
        before = xp(5, 1, c['level']) + c['cur_exp']
        for tid,n in layer['direct'].items():
            role['attachments'].append(dict(id=f.new_id(role), type_id=tid, attach_type=5, count=n, level=1))
        c['reborn_vein_level'] = 9  # Vein materials independently summed above.
        rb.settle(role, dict(id=2, reborn_type=2, data={'cortege_id':1}), rb.load_rules(), lambda v:v)
        after = xp(5, 1, c['level']) + c['cur_exp']
        assert before - after == layer['lost_xp']
        observed_losses.append(int(before-after))
    n = ceil_div(int(xp(5, c['level'], 600) - c['cur_exp']), int(f.ITEMS[book]['experience_plus']))
    f.feed(role, dict(flag=1, first_send=True, cortege_id=1, roll_count=1,
                     roll_list=[dict(type_id=book,count=n)]), rules)
    fed += n
    assert c['level'] == 600 and c['reborn_layer'] == 9
    assert fed == ceil_div(total_xp, int(f.ITEMS[book]['experience_plus']))
    assert fixed[10000] == 53400 and sum(f.EVOLVE_COST.values()) == 390910
    result['verification'] = dict(real_feed_and_rebirth=True, observed_losses=observed_losses,
                                  final_level=c['level'], final_rebirth=c['reborn_layer'],
                                  book_1080_consumed=fed)
    helper_fixed = Counter()
    helper_essences = Counter()
    for layer in layers[:8]:
        helper_fixed.update({t: 2*n for t,n in layer['direct'].items()})
        helper_fixed.update({t: 2*n for t,n in layer['vein_fixed'].items()})
        helper_essences.update({q: 2*n for q,n in layer['essence_by_quality'].items()})
    result['two_eight_rebirth_helpers'] = dict(
        fixed=dict(helper_fixed), essence_by_quality=dict(helper_essences),
        xp=2*(xp(5,1,180)+sum(x['lost_xp'] for x in layers[:8])),
        final_level_each=180, account_realm_sarira_extra=sum(x['cost'] for x in result['shared_realm']))
    paths = [ROOT/'network_redirect'/f'{n}.py' for n in ('formation','immortal','reborn','reborn_stars','fate_rebuild','summon')]
    paths += [ROOT/'server_config'/f'{n}_rules.json' for n in ('formation','immortal','reborn')]
    paths += [ROOT/'analysis/configs'/p for p in (
        'immortal_hotupdate/cortege_experience.csv', 'immortal_hotupdate/cortege_evolution.csv',
        'immortal_hotupdate/cortege_reborn_config.csv', 'cortege_reborn_layer.csv',
        'cortege_reborn_vein.csv', 'star_level_exp.csv', 'essence_hotupdate/ext_skill_lock_cost.csv',
        'fate_rebuild/rebuild_material_costs.csv', 'babel_hotupdate/star_config.csv',
        'item_base.csv', 'fate_rebuild/item_base.csv', 'babel_hotupdate/item_base.csv',
        'local_items/item_base.csv', 'adaptive_spirit_convert.csv',
        'skill_enhance_cost.csv', 'skill_enhance_worth.csv', 'star_decompose_config.csv',
        'awaken_skill_conf.csv', 'material_transform.csv', 'babel_hotupdate/material_transform.csv')]
    result['sha256'] = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    dest = ROOT/'analysis/evidence/immortal_max_cost_20261113.json'
    dest.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(report=str(dest.relative_to(ROOT)), xp=total_xp,
                          souls=result['evolution']['souls'], rebirth_fixed=dict(fixed),
                          essence=result['essence'], star_dust=result['stars']['six_purple'],
                          verification=result['verification']), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
