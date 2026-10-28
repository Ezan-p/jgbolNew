"""Export current seven-gift rules with exact probabilities and original evidence."""
import csv
from fractions import Fraction
import hashlib
import io
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import item_rewards as rewards

IDS = (1247, 1084, 1085, 1086, 1098, 1099, 1205)
OUT = ROOT / 'analysis/evidence/seven_gifts'


def main():
    rules = rewards.load_rules()
    index = dict(line.split('====')[:2] for line in
                 (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    encodings = {row['logical']: row['encoding'] for row in json.loads(
        (ROOT/'analysis/evidence/config_inventory.json').read_text())}
    inputs = []
    for name in ('item_name', 'item_base', 'item_buy_config', 'item_receive_config',
                 'gift_config', 'exchange_zone', 'stone_cost_worth'):
        logical = f'csv_config/{name}.csv'
        raw = (ROOT/'jgbol3.87/assets/release_'/index[logical]).read_bytes()
        original = list(csv.reader(io.StringIO(raw.decode(encodings[logical]))))
        with (ROOT/'analysis/configs'/f'{name}.csv').open(encoding='utf-8-sig') as stream:
            assert original == list(csv.reader(stream)), name
        inputs.append(dict(logical=logical, asset=index[logical],
                           sha256=hashlib.sha256(raw).hexdigest(), csv_matches=True))
    items = {}
    for tid in IDS:
        rule = rules['items'][str(tid)]
        assert rule['mode'] == 'fixed_random'
        groups = rules['pools'][rule['pool']]
        total = sum(g['weight'] for g in groups)
        candidates = []
        for group in groups:
            probability = Fraction(group['weight'], total * len(group['candidates']))
            for p in group['candidates']:
                rewards.valid_prize(p, tid)
                k, t, n, lv = p
                candidates.append(dict(reward=p, name=rewards.NAMES[t]['name'] if k == 5
                                       else {11: '元宝', 12: '银币'}[k],
                                       probability=str(probability),
                                       expected_quantity_per_100=str(100*n*probability)))
        assert sum(Fraction(p['probability']) for p in candidates) == 1
        items[str(tid)] = dict(name=rule['name'], rule=rule,
                               fixed_probability='1', bonus=candidates, bonus_probability_sum='1')
    OUT.mkdir(exist_ok=True)
    # Preserve the earlier audit as historical evidence, never call it current.
    old = OUT/'audit.json'
    if old.exists() and 'current_real_wire_checks' in json.loads(old.read_text()):
        history = OUT/'initial_fixed_rules_audit.json'
        if not history.exists():
            history.write_bytes(old.read_bytes())
    report = dict(date='2026-10-28', revision=rules['revision'], status='implemented_in_workspace',
                  source='User images: contents and stone rates; local design: silver and other rates',
                  original_server_probabilities_verified=False, visible_ui_verified=False,
                  original_inputs=inputs, items=items,
                  verification='tests/test_item_rewards.py; tests.log records executed regression suite')
    old.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(f'PASS: 7 original CSVs; {len(items)} fixed-plus-one pools; '
          f'{sum(len(x["bonus"]) for x in items.values())} concrete bonus outcomes; exact sums = 1.')


if __name__ == '__main__':
    main()
