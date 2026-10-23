"""Reproduce immortal evidence from original 3.87 assets, without execution."""
import csv
import hashlib
import io
import json
from pathlib import Path
from luajit_static import parse, listing

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'analysis/evidence'
MODULES = ['ui/lineupUI', 'ui/handbookUI', 'ui/other_functionUI', 'ui/runeUI',
           'ui/jpUI', 'ui/jpmkUI', 'ui/jpChangeUI', 'ui/soulExchangeUI',
           'ui/cortCollectUI', 'ui/allLineupUI', 'ui/commonLayerUI', 'ui/smithUI',
           'data', 'event_mgr', 'common/common_def', 'common/msg_def']
TABLES = ['item_base', 'ext_skill', 'ext_skill_lock_cost', 'jingpo_transform', 'material_transform',
          'adaptive_spirit_convert', 'collector_cortege', 'cortege_evolution', 'cortege_quality']


def main():
    index = dict(line.split('====')[:2] for line in (OUT / 'resource_index.decoded.txt').read_text().splitlines())
    encodings = {r['logical']: r['encoding'] for r in json.loads((OUT / 'config_inventory.json').read_text())}
    evidence, listings = [], []
    for name in ['lua/' + m + '.lua' for m in MODULES] + [next(k for k in index if k.startswith('csv_config/') and Path(k).stem == t) for t in TABLES]:
        path = ROOT / 'jgbol3.87/assets/release_' / index[name]
        row = dict(logical=name, physical=str(path.relative_to(ROOT)), sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        if name.endswith('.csv'):
            original = list(csv.reader(io.StringIO(path.read_bytes().decode(encodings[name]))))
            extracted = ROOT / 'analysis/configs' / name.removeprefix('csv_config/')
            assert original == list(csv.reader(io.StringIO(extracted.read_text(encoding='utf-8-sig')))), name
            row['csv_values_match'] = True
        else:
            chunk = parse(path.read_bytes())
            # Complete modules retain nested menu callbacks and their constants.
            listings.append(name)
            for p in chunk['protos']:
                listings.append('NUMERIC CONSTANTS proto%d: %r' % (p['id'], p['numbers']))
            listings.append(listing(chunk))
        evidence.append(row)
    (OUT / 'immortal_official_bytecode.txt').write_text('\n'.join(listings))
    report = dict(date='2026-10-24', client='3.87', official_server_available=False,
                  inputs=evidence, implemented_requests=[1033, 1048, 1051, 1074, 1305, 1306, 1311, 1322],
                  source_classes={'A': 'Original client UI/protocol/CSV', 'B': 'Inferred settlement, probabilities and missing server config'},
                  config='server_config/immortal_rules.json', documentation='docs/神仙模块规则与调试.md')
    (OUT / 'immortal_official_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print('Verified original assets and CSV values; wrote immortal audit evidence.')


if __name__ == '__main__':
    main()
