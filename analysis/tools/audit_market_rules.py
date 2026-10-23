"""Reproduce market evidence and verify extracted CSVs against original assets."""
import csv
import hashlib
import io
import json
import plistlib
from pathlib import Path

from luajit_static import parse, listing

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'analysis/evidence'


def main():
    index = {p[0]: p[1] for line in (OUT / 'resource_index.decoded.txt').read_text().splitlines()
             if len(p := line.split('====')) == 3}
    encodings = {r['logical']: r['encoding'] for r in json.loads((OUT / 'config_inventory.json').read_text())}
    names = ['lua/ui/shopUI.lua', 'lua/ui/salesUI.lua', 'lua/data.lua',
             'lua/common/common_def.lua', 'lua/common/msg_def.lua', 'lua/event_mgr.lua']
    names += ['csv_config/' + name + '.csv' for name in ('item_buy_config', 'item_base', 'item_name')]
    names += ['v2/String.plist', 'v2/String2.plist']
    inputs, excerpts = [], []
    for name in names:
        path = ROOT / 'jgbol3.87/assets/release_' / index[name]
        record = dict(logical=name, physical=str(path.relative_to(ROOT)),
                      sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        inputs.append(record)
        if name.endswith('.plist'):
            strings = plistlib.loads(path.read_bytes())
            record['sales_strings'] = {k: v for k, v in strings.items() if k.startswith('sales')}
        if name.endswith('.csv'):
            extracted = ROOT / 'analysis/configs' / Path(name).name
            assert list(csv.reader(io.StringIO(path.read_bytes().decode(encodings[name])))) == list(
                csv.reader(io.StringIO(extracted.read_text(encoding='utf-8-sig')))), name
            record.update(csv_values_match=True, extracted_sha256=hashlib.sha256(extracted.read_bytes()).hexdigest())
        if name in ('lua/ui/shopUI.lua', 'lua/ui/salesUI.lua'):
            chunk = parse(path.read_bytes())
            for proto in chunk['protos']:
                excerpts.append('%s proto%d NUMERIC CONSTANTS: %s' % (name, proto['id'], proto['numbers']))
                excerpts.append(listing(dict(source=chunk['source'], root=proto['id'], protos=[proto])))
    (OUT / 'market_official_bytecode.txt').write_text('\n'.join(excerpts), encoding='utf-8')
    report = dict(date='2026-10-24', client='3.87', inputs=inputs,
                  implemented_requests=[1057, 1241, 1242], response_events=[24, 80, 138, 139],
                  official_server_available=False,
                  source_classes={'A': 'Original client bytecode and packaged CSV values',
                                  'B': 'Explicit inferred server policy; not recovered official operations'},
                  rules='server_config/market_rules.json',
                  rules_sha256=hashlib.sha256((ROOT / 'server_config/market_rules.json').read_bytes()).hexdigest())
    (OUT / 'market_official_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Original market CSV values verified; audit and bytecode written.')


if __name__ == '__main__':
    main()
