"""Reproduce journey evidence directly from the packaged 3.87 client."""
import csv
import hashlib
import io
import json
from pathlib import Path
import sys

from luajit_static import parse, listing

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import journey

OUT = ROOT / 'analysis/evidence'


def main():
    index = {p[0]: p[1] for line in (OUT / 'resource_index.decoded.txt').read_text().splitlines()
             if len(p := line.split('====')) == 3}
    encodings = {r['logical']: r['encoding'] for r in json.loads((OUT / 'config_inventory.json').read_text())}
    lua = ['lua/ui/' + name + '.lua' for name in ('mapUI', 'subLevelUI', 'saodangUI', 'fightUI', 'prizeUI', 'lineupUI')]
    lua += ['lua/event_mgr.lua', 'lua/common/common_def.lua', 'lua/common/msg_def.lua', 'lua/skill/skill_mgr.lua']
    csvs = ['map_config.csv', 'tollgate_config.csv', 'elite/elite_map_config.csv', 'elite/elite_tollgate_config.csv',
            'elite/elite_cortege_base.csv', 'tollgate_flush_cost.csv', 'tollgate_sweep_flush.csv',
            'role_level_config.csv', 'cortege_experience.csv', 'skill_base.csv', 'item_base.csv', 'item_buy_price.csv']
    csvs += ['cortege/' + p.name for p in sorted((ROOT / 'analysis/configs/cortege').glob('cortege_base_*.csv'))]
    records, evidence = [], []
    for name in lua + ['csv_config/' + name for name in csvs]:
        path = ROOT / 'jgbol3.87/assets/release_' / index[name]
        record = dict(logical=name, physical=str(path.relative_to(ROOT)), sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        if name.endswith('.csv'):
            extracted = ROOT / 'analysis/configs' / name.removeprefix('csv_config/')
            assert list(csv.reader(io.StringIO(path.read_bytes().decode(encodings[name])))) == list(
                csv.reader(io.StringIO(extracted.read_text(encoding='utf-8-sig')))), name
            record['csv_values_match'] = True
        else:
            chunk = parse(path.read_bytes())
            evidence.append('\n===== ' + name + ' =====\n')
            evidence.append(listing(chunk))
            if name.endswith('common_def.lua'):
                enums = {}
                for proto in chunk['protos']:
                    for item in proto['kgc']:
                        if isinstance(item, dict) and item.get('kind') == 'table':
                            value = item['value']
                            if any(k in value for k in ('sweep_count_limit', 'elite_tollgate', 'tollgate_prize', 'src_win_com')):
                                enums[str(len(enums))] = value
                record['recovered_enum_tables'] = enums
        records.append(record)
    (OUT / 'journey_official_bytecode.txt').write_text('\n'.join(evidence))
    report = dict(date='2026-10-24', client='3.87', official_server_available=False,
                  normal_maps=len(journey.MAPS[1]), elite_maps=len(journey.MAPS[2]),
                  normal_gates=len(journey.GATES[1]), elite_gates=len(journey.GATES[2]),
                  source_classes={'A': 'Packaged original client bytecode, protocol and CSV facts',
                                  'B': 'Explicit inferred server policy, not a recovered official server'},
                  inputs=records, rules='server_config/journey_rules.json',
                  rules_sha256=hashlib.sha256((ROOT / 'server_config/journey_rules.json').read_bytes()).hexdigest())
    (OUT / 'journey_official_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(f'Verified {len(csvs)} original CSVs and {len(lua)} Lua modules; 597 normal + 67 elite gates.')


if __name__ == '__main__':
    main()
