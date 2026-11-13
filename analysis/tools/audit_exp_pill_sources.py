"""Trace every experience pill in active tables, without opening player saves."""
from collections import defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import (formation, summon, activity_abyss as abyss,
                              abyss_balance, activity_babel as babel,
                              activity_pavilion as pavilion,
                              activity_save_monkey as monkey,
                              activity_moon, activity_treasure, qiankun_bags)
from analysis.tools.send_launch_gift import build as launch_gift


def audit():
    names = {int(x['Ftype_id']): x['name'] for x in summon.rows('item_name.csv')}
    items = {tid: dict(id=tid, name=names[tid], subtype=int(row['sub_type']),
                       display_tier=int(row['show_level']), xp=int(row['experience_plus']),
                       sources=[])
             for tid, row in formation.ITEMS.items()
             if row['main_type'] == '5' and row['sub_type'] in ('100', '101')
             and int(row['experience_plus']) > 0}
    assert len(items) == 40

    def add(tid, kind, **details):
        items[tid]['sources'].append(dict(kind=kind, **details))

    idle = defaultdict(list)
    bosses = defaultdict(list)
    for floor, groups in abyss.DROPS.items():
        for outer, entries in groups:
            for typ, tid, level, count, weight in entries:
                if typ == 5 and tid in items:
                    probability = Fraction(outer, sum(g[0] for g in groups)) * Fraction(weight, sum(e[4] for e in entries))
                    idle[tid].append(dict(floor=floor, count=count, probability=str(probability),
                                          expected_daily=str(288 * count * probability)))
        for typ, tid, count, level in abyss_balance.victory_rewards(floor):
            if typ == 5 and tid in items:
                bosses[tid].append(dict(floor=floor, count=count))
    for tid, rows in idle.items():
        add(tid, 'abyss_idle', status='active', floors=rows)
    for tid, rows in bosses.items():
        add(tid, 'abyss_first_win', status='active_once', floors=rows,
            total_count=sum(r['count'] for r in rows))
    for secret, table in ((False, babel.FLOORS), (True, babel.SECRET_FLOORS)):
        for row in table:
            specs = [list(map(int, token.split('|'))) for token in row['daoju'].split('/')]
            weighted = not secret and any(s[:2] == [5, 1246] for s in specs)
            weights = [babel.floor_reward_weight(s, secret) if weighted else 1 for s in specs]
            for index, spec in enumerate(specs):
                if spec[0] == 5 and spec[1] in items:
                    add(spec[1], 'babel_secret' if secret else 'babel_normal', status='active',
                        min_floor=int(row['floor_l']), max_floor=int(row['floor_r']), count=spec[2],
                        probability_per_reward_point=str(Fraction(weights[index], sum(weights))))
    prules = pavilion.load_rules()
    for index, row in pavilion.SHOP.items():
        for typ, tid, count, level in pavilion.specs(row['attach_list']):
            if typ == 5 and tid in items:
                add(tid, 'pavilion', status='active' if prules['enabled'] else 'disabled', index=index,
                    count=count, bricks=int(row['goldon_count']), limit_per_period=int(row['max_buy_count']),
                    period_days=prules['period_days'])
    for typ, tid, count, level in abyss_balance.rules()['starter_rewards']:
        if typ == 5 and tid in items:
            add(tid, 'abyss_starter', status='active_once', count=count)
    for index, row in monkey.ASSIST.items():
        for typ, tid, count, level in row['prizes']:
            if typ == 5 and tid in items:
                add(tid, 'save_monkey_assist', status='active' if monkey.load_rules()['enabled'] else 'disabled',
                    index=index, count=count, consume=row['consume'])
    for row in summon.rows('cross_server/camp_top_prize.csv'):
        for token in row['prize_list'].split('/'):
            typ, tid, level, count = map(int, token.split('|'))
            if typ == 5 and tid in items:
                add(tid, 'original_camp_rank', status='table_only_no_current_consumer',
                    original_rank_fields={k: v for k, v in row.items() if k != 'prize_list'}, count=count)
    for typ, tid, count, level in launch_gift()[0]:
        if typ == 5 and tid in items:
            add(tid, 'operator_launch_mail', status='manual_optional_once', count=count)
    excluded = {}
    rules = json.loads((ROOT / 'server_config/activity_rules.json').read_text())
    for tier in range(1, 11):
        for index, spec in enumerate(activity_treasure.pool(1430 + tier, rules)):
            if spec['object_type'] == 5 and spec['attach_type'] in items:
                add(spec['attach_type'], 'abyss_map', status='active', revision=rules['abyss_map_revision'],
                    map_tier=tier, count=spec['attach_count'],
                    first_probability=str(Fraction(rules['abyss_map_weights'][index],
                                                   sum(rules['abyss_map_weights']))))
    moon = activity_moon.load_rules()
    for label, specs in (
        ('current_abyss_shop', [p['reward'] for p in rules['abyss_shop']]),
        ('current_abyss_events', rules['abyss_event_rewards']),
        ('current_moon', [p for pool in moon['pools'].values() for g in pool['groups'] for p in g['candidates']]),
    ):
        found = sorted({p[1] for p in specs if p[0] == 5 and p[1] in items})
        assert not found, (label, found)
        excluded[label] = found
    bag_found = sorted({tid for pool in qiankun_bags.CATALOG.values() for typ, tid in pool if typ == 5 and tid in items})
    assert not bag_found
    excluded['current_qiankun_bags'] = bag_found
    gaps = [tid for tid, item in items.items() if item['subtype'] == 100 and
            not any(s['status'] in ('active', 'active_once') for s in item['sources'])]
    assert gaps == []  # All 30 immortal XP pills now have a matching map tier.
    sources = [
        'analysis/configs/item_base.csv', 'analysis/configs/item_name.csv',
        'analysis/configs/specter_hang_ouput.csv', 'analysis/configs/specter_boss_config.csv',
        'analysis/configs/babel_hotupdate/babel_tower_floor_prize.csv',
        'analysis/configs/babel_hotupdate/babel_secret_tower_floor_prize.csv',
        'analysis/configs/pavilion/exchange_zone.csv', 'analysis/configs/save_monkey/assist_shop_config.csv',
        'analysis/configs/cross_server/camp_top_prize.csv',
        'server_config/abyss_rules.json', 'server_config/activity_rules.json',
        'server_config/moon_rules.json', 'server_config/qiankun_bag_rules.json',
        'server_config/pavilion_rules.json', 'server_config/save_monkey_rules.json',
        'network_redirect/summon.py', 'network_redirect/formation.py',
        'network_redirect/activity_abyss.py', 'network_redirect/activity_treasure.py', 'network_redirect/activity_babel.py',
        'network_redirect/activity_pavilion.py', 'network_redirect/activity_save_monkey.py',
        'network_redirect/activity_drug.py', 'network_redirect/activity_moon.py',
        'network_redirect/qiankun_bags.py', 'analysis/tools/send_launch_gift.py',
    ]
    return dict(date='2026-11-13', scope='current working-tree item catalog and reward consumers',
                pills=list(items.values()), current_source_gap_ids=gaps, excluded_current_pools=excluded,
                source_sha256={s: hashlib.sha256((ROOT / s).read_bytes()).hexdigest() for s in sources})


if __name__ == '__main__':
    data = audit()
    out = ROOT / 'analysis/evidence/exp_pill_sources_20261113.json'
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(f'Audited {len(data["pills"])} pills; {len(data["current_source_gap_ids"])} immortal pill IDs have no current normal source; wrote {out.relative_to(ROOT)}')
