"""Reproduce scroll identities, source tables and UI logic from unmodified 3.87."""
import csv
import hashlib
import io
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.luajit_static import parse, listing

OUT = ROOT / 'analysis/evidence/expbooks'
TABLES = ['item_base.csv', 'item_name.csv', 'cortege_experience.csv',
          'achievements_config.csv', 'tollgate_config.csv', 'elite/elite_tollgate_config.csv',
          'hole/main_building_config.csv']


def main():
    OUT.mkdir(exist_ok=True)
    index = dict(line.split('====')[:2] for line in
                 (ROOT / 'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    enc = {r['logical']: r['encoding'] for r in json.loads(
        (ROOT / 'analysis/evidence/config_inventory.json').read_text())}
    evidence, tables = [], {}
    for name in TABLES:
        logical = 'csv_config/' + name
        raw = (ROOT / 'jgbol3.87/assets/release_' / index[logical]).read_bytes()
        original = list(csv.reader(io.StringIO(raw.decode(enc[logical]))))
        extracted = list(csv.reader(io.StringIO((ROOT / 'analysis/configs' / name).read_text(encoding='utf-8-sig'))))
        assert original == extracted, name
        tables[name] = [dict(zip(original[0], row)) for row in original[1:]]
        evidence.append(dict(logical=logical, sha256=hashlib.sha256(raw).hexdigest(),
                             rows=len(original)-1, csv_values_match=True))
    logical = 'lua/ui/expbookUI.lua'
    raw = (ROOT / 'jgbol3.87/assets/release_' / index[logical]).read_bytes()
    chunk = parse(raw)
    bytecode = '\n'.join('NUMERIC proto%d %r' % (p['id'], p['numbers']) for p in chunk['protos']) + '\n' + listing(chunk)
    (OUT / 'ui_expbookUI.txt').write_text(bytecode)
    for token in ('base_experience_plus', 'show_level', 'type_id', 'first_send',
                  'msg_consume_fairy_roll', "'lv': 2.5, 'rate': 0.2", "'lv': 3, 'rate': 0"):
        assert token in bytecode, token
    evidence.append(dict(logical=logical, sha256=hashlib.sha256(raw).hexdigest(),
                         listing='ui_expbookUI.txt'))
    names = {int(next(iter(r.values()))): r for r in tables['item_name.csv']}
    books = [dict(type_id=int(r['type_id']), name=names[int(r['type_id'])]['name'],
                  show_level=int(r['show_level']), experience=int(r['experience_plus']),
                  main_type=int(r['main_type']), sub_type=int(r['sub_type']),
                  resource=int(r['resource']), top_level=int(r['top_level']),
                  use_limit=int(r['use_limit']), use_target=int(r['use_target']),
                  product_desc=names[int(r['type_id'])]['product_desc'])
             for r in tables['item_base.csv'] if r['sub_type'] == '99']
    assert [r['type_id'] for r in books] == list(range(1041, 1081))
    sources = []
    for name in ('tollgate_config.csv', 'elite/elite_tollgate_config.csv'):
        for line, row in enumerate(tables[name], 2):
            for column, value in row.items():
                matches = [r['type_id'] for r in books if '|'+str(r['type_id'])+'|' in value]
                if matches: sources.append(dict(table=name, line=line, column=column, value=value, book_ids=matches))
    report = dict(date='2026-10-26', official_server_available=False,
                  source_classes={'A': 'Original packaged CSV and client bytecode',
                                  'B': 'Offline settlement, caps/overflow, potential and achievement trigger policy'},
                  inputs=evidence, books=books, configured_sources=sources,
                  achievement=next(r for r in tables['achievements_config.csv'] if r['id'] == '117'),
                  unresolved=['Original server overflow/refund and decimal rounding policy',
                              'Unpublished activity drop probabilities and level-to-tier mapping'])
    assert report['achievement']['id'] == '117'
    (OUT / 'official_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(f'Verified {len(evidence)-1} original CSV tables, 40 scroll IDs and expbookUI bytecode')


if __name__ == '__main__': main()
