"""Reproduce 1246 item identity and original client contracts without executing Lua."""
import csv
import hashlib
import io
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.luajit_static import parse, listing
from network_redirect import immortal, xianyuan_fruit

OUT = ROOT / 'analysis/evidence/xianyuan_fruit'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    index = dict(line.split('====')[:2] for line in
                 (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    enc = {r['logical']: r['encoding'] for r in json.loads(
        (ROOT/'analysis/evidence/config_inventory.json').read_text())}
    tables, inputs, excerpts = {}, [], []
    for name in ('item_base.csv', 'item_name.csv', 'adaptive_spirit_convert.csv',
                 'cortege/cortege_base_0.csv', 'cortege/cortege_name_0.csv', 'cortege_quality.csv',
                 'babel_tower_floor_prize.csv', 'exchange_zone.csv'):
        logical = 'csv_config/' + name
        raw = (ROOT/'jgbol3.87/assets/release_'/index[logical]).read_bytes()
        original = list(csv.reader(io.StringIO(raw.decode(enc[logical]))))
        extracted = list(csv.reader(io.StringIO((ROOT/'analysis/configs'/name).read_text(encoding='utf-8-sig'))))
        assert original == extracted, name
        tables[name] = [dict(zip(original[0], row)) for row in original[1:]]
        inputs.append(dict(logical=logical, sha256=hashlib.sha256(raw).hexdigest(), csv_values_match=True))
    for name, ranges in (
        ('ui/kickUI.lua', [(102,104), (198,210), (1058,1125), (1153,1277)]),
        ('ui/packageUI.lua', [(1859,1860)]),
        ('data.lua', [(3835,3835)]),
        ('ui/commonLayerUI.lua', [(464,466), (526,538)]),
        ('common/common_def.lua', [(132,154), (3684,3684)]),
    ):
        logical = 'lua/' + name
        raw = (ROOT/'jgbol3.87/assets/release_'/index[logical]).read_bytes()
        chunk = parse(raw)
        import re
        text = listing(chunk)
        excerpts.append(logical+'\n'+'\n'.join(line for line in text.splitlines()
                        if (m := re.search(r'\[L(\d+)\]', line)) and
                        any(a <= int(m[1]) <= b for a,b in ranges)))
        if name == 'ui/kickUI.lua':
            assert all(token in text for token in ('onGetCortList', 'getFruitCorts', 'msg_use_item',
                                                  "'value': {1: 5027, 2: 5046, 3: 5053}"))
        if name == 'common/common_def.lua':
            assert "'longer_hill': 27" in text
        inputs.append(dict(logical=logical, sha256=hashlib.sha256(raw).hexdigest()))
    names = {int(next(iter(r.values()))): r for r in tables['cortege/cortege_name_0.csv']}
    rules = immortal.load_rules()['xianyuan_fruit']
    report = dict(date='2026-10-26', official_server_available=False, inputs=inputs,
                  item=next(r for r in tables['item_base.csv'] if r['type_id']=='1246'),
                  name=next(r for r in tables['item_name.csv'] if next(iter(r.values()))=='1246'),
                  offline_soul_targets=[dict(type_id=t, original_name=names[t], owned_only=t in xianyuan_fruit.OWNED_ONLY)
                                        for t in rules['soul_targets']],
                  offline_realm_targets=rules['realm_targets'],
                  original_client=dict(config_section=27, soul_object_type=10, item_object_type=5,
                                       unowned_rate=1, owned_rate=10, realm_rate=10, max_batch=15,
                                       owned_only=sorted(xianyuan_fruit.OWNED_ONLY)),
                  unresolved=['Original longer_hill server catalog unavailable; local list is inferred',
                              'Original server validation and stack consumption policy unavailable',
                              'Longevity Hill activity 1323 remains unimplemented'])
    (OUT/'official_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    (OUT/'client_contracts.txt').write_text('\n\n'.join(excerpts)+'\n')
    print(f'Verified 8 original CSV files, 5 Lua assets; {len(rules["soul_targets"])} offline soul targets')


if __name__ == '__main__':
    main()
