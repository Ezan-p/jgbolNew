"""Audit non-equipment item candidates; speculation is not an official loot table."""
import csv
import hashlib
import io
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'analysis/evidence/qiankun_bags/material_candidates.json'

# Explicit editorial hypotheses, never inferred merely from missing source text.
COMMON = {1001, 1003, 1005, 1006, 1007, 1022, 1023, 1024}
ADVANCED = {1015, 1090, 1091, 1092, 1093, 1095, 1100, 1246, 1249,
            1313, 1314, 1315, 1320, 1321, 1322, 1323, 1336}


def main():
    index = dict(line.split('====')[:2] for line in
                 (ROOT / 'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    encodings = {r['logical']: r['encoding'] for r in json.loads(
        (ROOT / 'analysis/evidence/config_inventory.json').read_text())}
    tables, inputs = {}, []
    for name in ['item_name.csv', 'item_base.csv']:
        logical = 'csv_config/' + name
        raw = (ROOT / 'jgbol3.87/assets/release_' / index[logical]).read_bytes()
        original = raw.decode(encodings[logical])
        local = (ROOT / 'analysis/configs' / name).read_text(encoding='utf-8-sig')
        assert list(csv.reader(io.StringIO(original))) == list(csv.reader(io.StringIO(local))), name
        tables[name] = list(csv.DictReader(io.StringIO(original)))
        inputs.append({'logical': logical, 'asset': index[logical],
                       'sha256': hashlib.sha256(raw).hexdigest(), 'csv_matches': True})
    bases = {int(r['type_id']): r for r in tables['item_base.csv']}
    names = tables['item_name.csv']
    assert len({int(r['Ftype_id']) for r in names}) == len(names)
    entries = []
    excluded = []
    for line, row in enumerate(names, 2):
        tid = int(row['Ftype_id'])
        base = bases[tid]
        if int(base['main_type']) in (1, 2, 3):
            excluded.append(tid)
            continue
        source = row.get('product_desc') or ''
        if '乾坤袋' in source:
            status, reason = 'A_原文案支持', '来源明确写开启乾坤袋；未分配袋种。'
        elif tid in COMMON:
            status, reason = 'B1_通用资源假说', '常用消耗或功能与综合资源袋定位相容；没有开袋直接证据。'
        elif tid in ADVANCED:
            status, reason = 'B2_进阶资源弱假说', '可设想为高档袋补充资源；原文案指向其他渠道，关联比B1更弱。'
        else:
            status, reason = 'C_无开袋依据暂不纳入', '未找到开袋绑定；需单独证据，来源为空也不能推定可开出。'
        entries.append({'id': tid, 'name': row['name'], 'description': row['desc'],
                        'source_text': source, 'source_line': line,
                        'main_type': int(base['main_type']), 'sub_type': int(base['sub_type']),
                        'status': status, 'reason': reason,
                        'bag_id': None, 'official_probability': None})
    result = {'scope': 'item_name全表中main_type不为1/2/3的物品；包含用于排除审查的礼包和专属道具，不等于候选奖池。法术、神仙实体和货币对象另计。',
              'inputs': inputs, 'total_item_rows': len(names),
              'excluded_equipment_count': len(excluded), 'reviewed_count': len(entries),
              'status_counts': dict(Counter(r['status'] for r in entries)), 'items': entries}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('items', 'inputs')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
