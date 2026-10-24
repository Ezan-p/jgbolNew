"""Audit original 3.87 combat-power evidence without executing client code."""
import ast
import csv
import hashlib
import io
import json
import re
from pathlib import Path

from luajit_static import listing, parse

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'analysis/evidence'


def main():
    index = dict(line.split('====')[:2] for line in
                 (OUT / 'resource_index.decoded.txt').read_text().splitlines()
                 if len(line.split('====')) == 3)
    report = {'client': '3.87', 'date': '2026-10-24', 'scripts_scanned': 0,
              'power_references': [], 'inputs': [], 'enums': {}}
    excerpts = []
    for logical, physical in index.items():
        if not logical.endswith('.lua'):
            continue
        path = ROOT / 'jgbol3.87/assets/release_' / physical
        raw = path.read_bytes()
        chunk = parse(raw)
        report['scripts_scanned'] += 1
        text = listing(chunk)
        if re.search(r'combat_power|combatPower|CombatPower', text):
            report['power_references'].append(logical)
        if logical == 'lua/common/common_def.lua':
            lines = text.splitlines()
            for i, line in enumerate(lines[:-1]):
                if 'TDUP' not in line or "'value':" not in line:
                    continue
                nxt = lines[i + 1]
                for name in ('role_property', 'cortege_property', 'client_config_type'):
                    if 'GSET' in nxt and repr(name) in nxt:
                        report['enums'][name] = ast.literal_eval(
                            line[line.index("{'kind'"):])['value']
        if logical in ('lua/common/common_def.lua', 'lua/common/msg_def.lua',
                       'lua/ui/charPositionUI.lua', 'lua/ui/mainUI.lua',
                       'lua/ui/equipmentUpgradeUI.lua'):
            report['inputs'].append({'logical': logical, 'physical': str(path.relative_to(ROOT)),
                                     'sha256': hashlib.sha256(raw).hexdigest()})
            for proto in chunk['protos']:
                part = listing(dict(source=chunk['source'], root=proto['id'], protos=[proto]))
                if re.search(r'combat_power|base_gongji_plus', part):
                    excerpts.append(f"\n{logical} proto{proto['id']} NUMBERS={proto['numbers']}\n{part}")
    encodings = {r['logical']: r['encoding'] for r in
                 json.loads((OUT / 'config_inventory.json').read_text())}
    report['configs'] = []
    for logical, physical in index.items():
        if not logical.startswith('csv_config/') or not logical.endswith('.csv'):
            continue
        if not re.search(r'cortege|equip|skill|animal|star|ling_|stone|fate|title|hole_train|cheer', logical):
            continue
        raw = (ROOT / 'jgbol3.87/assets/release_' / physical).read_bytes()
        original = list(csv.reader(io.StringIO(raw.decode(encodings[logical]))))
        extracted = ROOT / 'analysis/configs' / logical.removeprefix('csv_config/')
        rows = list(csv.reader(io.StringIO(extracted.read_text(encoding='utf-8-sig'))))
        assert original == rows, logical
        report['configs'].append({'logical': logical, 'rows': len(rows) - 1,
                                  'sha256': hashlib.sha256(raw).hexdigest(),
                                  'csv_values_match': True})
    (OUT / 'combat_power_audit.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    (OUT / 'combat_power_bytecode.txt').write_text('\n'.join(excerpts))
    print(json.dumps({'scripts_scanned': report['scripts_scanned'],
                      'power_references': report['power_references'],
                      'cortege_fields': len(report['enums']['cortege_property'])}, ensure_ascii=False))


if __name__ == '__main__':
    main()
