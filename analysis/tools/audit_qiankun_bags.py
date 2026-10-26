"""Read-only original-asset audit of bag acquisition and source-text candidates."""
import csv
import hashlib
import io
import json
import plistlib
import re
from pathlib import Path

from luajit_static import decode, listing, parse

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'analysis/evidence/qiankun_bags'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    index = dict(line.split('====')[:2] for line in
                 (ROOT / 'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    encodings = {r['logical']: r['encoding'] for r in json.loads(
        (ROOT / 'analysis/evidence/config_inventory.json').read_text())}
    hits, tables = [], {}
    for file in sorted((ROOT / 'analysis/configs').rglob('*.csv')):
        name = str(file.relative_to(ROOT / 'analysis/configs'))
        content = list(csv.DictReader(io.StringIO(file.read_text(encoding='utf-8-sig'))))
        tables[name] = content
        for line, row in enumerate(content, 2):
            for column, value in row.items():
                if isinstance(value, str) and re.search(r'(?:^|/)5\|103[1-4]\|', value):
                    hits.append(dict(table=name, line=line, column=column, row=row))
    selected = sorted({h['table'] for h in hits} | {
        'item_base.csv', 'item_name.csv', 'skill_base.csv', 'skill_name.csv',
        'tollgate_name.csv', 'vip_pri_config.csv', 'cards_tip.csv'})
    inputs = []
    for name in selected:
        logical = 'csv_config/' + name
        raw = (ROOT / 'jgbol3.87/assets/release_' / index[logical]).read_bytes()
        original = list(csv.reader(io.StringIO(raw.decode(encodings[logical]))))
        local = list(csv.reader(io.StringIO(
            (ROOT / 'analysis/configs' / name).read_text(encoding='utf-8-sig'))))
        assert original == local, logical
        inputs.append(dict(logical=logical, asset=index[logical],
                           sha256=hashlib.sha256(raw).hexdigest(), csv_matches=True))

    contracts = []
    for module in ['data', 'ui/omenUI', 'ui/dreamUI', 'ui/destinyUI',
                   'ui/friendsUI', 'ui/crossRankUI']:
        logical = 'lua/' + module + '.lua'
        raw = (ROOT / 'jgbol3.87/assets/release_' / index[logical]).read_bytes()
        chunk = parse(raw)
        names = {}
        for proto in chunk['protos']:
            for first, second in zip(proto['code'], proto['code'][1:]):
                op, _, _, _, d = decode(first)
                op2, _, _, _, d2 = decode(second)
                if op == 'FNEW' and op2 == 'GSET':
                    names[proto['kgc'][d]['id']] = proto['kgc'][d2]
        keep = []
        for proto in chunk['protos']:
            strings = [v for v in proto['kgc'] if isinstance(v, str)]
            if proto['line'] and (names.get(proto['id']) in ('getItemListFromStr', 'getItemFromStr') or any(
                word in s for s in strings for word in
                ['getOmenConfig', 'monster_top_prize', 'rank_prize.csv',
                 'gift_config.csv', 'own_wish_prizes', 'friends_lv_reward'])):
                keep.append(proto)
                contracts.append(dict(module=module, function=names.get(proto['id']),
                                      line=proto['line'], last_line=proto['last_line'], strings=strings))
        partial = dict(chunk, protos=keep)
        (OUT / (module.replace('/', '_') + '.txt')).write_text(listing(partial))
        inputs.append(dict(logical=logical, asset=index[logical],
                           sha256=hashlib.sha256(raw).hexdigest()))
    candidates = []
    for table, base_table, id_key, object_type in [
        ('item_name.csv', 'item_base.csv', 'Ftype_id', 5),
        ('skill_name.csv', 'skill_base.csv', 'type_id', 6),
    ]:
        bases = {r['type_id']: r for r in tables[base_table]}
        for r in tables[table]:
            if '乾坤袋' in (r.get('product_desc') or ''):
                tid = r[id_key]
                candidates.append(dict(object_type=object_type, id=int(tid), name=r['name'],
                                       quality=int(bases[tid]['quality']),
                                       source_text=r['product_desc'], bag_id=None,
                                       official_probability=None))
    logical = 'v2/String2.plist'
    raw = (ROOT / 'jgbol3.87/assets/release_' / index[logical]).read_bytes()
    strings = {}
    def collect_strings(value):
        for key, child in value.items():
            if isinstance(child, dict):
                collect_strings(child)
            elif isinstance(child, str) and '乾坤袋' in child:
                strings[key] = child
    collect_strings(plistlib.loads(raw))
    inputs.append(dict(logical=logical, asset=index[logical],
                       sha256=hashlib.sha256(raw).hexdigest()))
    report = dict(client='3.87', official_server_available=False,
                  scanned_csv_count=len(tables), inputs=inputs, acquisition_hits=hits,
                  output_source_mentions=candidates, contracts=contracts,
                  bag_related_strings=strings,
                  note='Source mentions do not establish per-bag pools or drop probabilities.')
    (OUT / 'audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(f'Verified {len(selected)} CSVs; {len(hits)} bag-reference cells; '
          f'{len(candidates)} output-source mentions.')


if __name__ == '__main__':
    main()
