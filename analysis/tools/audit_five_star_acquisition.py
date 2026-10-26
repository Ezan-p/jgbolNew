"""Audit acquisition evidence from original 3.87 assets; no game execution."""
import csv
import hashlib
import io
import json
from pathlib import Path

from luajit_static import listing, parse

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'analysis/evidence/five_star_acquisition'
TABLES = [
    'item_base', 'item_name', 'skill_base', 'skill_name', 'item_receive_config',
    'material_transform', 'skill_material_transform', 'item_exchange_config',
    'equip_compose_random', 'item_buy_config', 'tollgate_config', 'tollgate_name',
    'map_name', 'undergo_ordeal/elite_tollgate_config',
    'cortege/cortege_base_0', 'cortege/cortege_name_0', 'happiness_bag_config',
]


def rows(name):
    with (ROOT / 'analysis/configs' / (name + '.csv')).open(encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    index = dict(line.split('====')[:2] for line in
                 (ROOT / 'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    encodings = {r['logical']: r['encoding'] for r in json.loads(
        (ROOT / 'analysis/evidence/config_inventory.json').read_text())}
    inputs = []
    for name in TABLES:
        logical = 'csv_config/' + name + '.csv'
        raw = (ROOT / 'jgbol3.87/assets/release_' / index[logical]).read_bytes()
        original = list(csv.reader(io.StringIO(raw.decode(encodings[logical]))))
        local = list(csv.reader(io.StringIO(
            (ROOT / 'analysis/configs' / (name + '.csv')).read_text(encoding='utf-8-sig'))))
        assert original == local, logical
        inputs.append(dict(logical=logical, asset=index[logical],
                           sha256=hashlib.sha256(raw).hexdigest(), csv_matches=True))
    for module in ['smithUI', 'forgeUI', 'equipPieceUI', 'qiankunnizhuan', 'prizeUI', 'packageUI']:
        logical = 'lua/ui/' + module + '.lua'
        raw = (ROOT / 'jgbol3.87/assets/release_' / index[logical]).read_bytes()
        (OUT / (module + '.txt')).write_text(listing(parse(raw)))
        inputs.append(dict(logical=logical, asset=index[logical],
                           sha256=hashlib.sha256(raw).hexdigest()))

    names = {r['Ftype_id']: r for r in rows('item_name')}
    skill_names = {r['type_id']: r for r in rows('skill_name')}
    equipment = [dict(id=int(r['type_id']), kind=int(r['main_type']),
                      name=names[r['type_id']]['name'],
                      source_text=names[r['type_id']]['product_desc'])
                 for r in rows('item_base')
                 if r['quality'] == '5' and r['main_type'] in ('1', '2', '3')]
    skills = [dict(id=int(r['type_id']), mode=int(r['use_mode(1-active，2-passive)']),
                   name=skill_names[r['type_id']]['name'],
                   source_text=skill_names[r['type_id']]['product_desc'])
              for r in rows('skill_base') if r['quality'] == '5']
    targets = {(5, r['id']) for r in equipment} | {(6, r['id']) for r in skills}
    reward_hits = []
    for table in ['item_receive_config', 'tollgate_config', 'undergo_ordeal/elite_tollgate_config']:
        for line, row in enumerate(rows(table), 2):
            for column, value in row.items():
                if not (column == 'attach_data' or 'prize(' in column):
                    continue
                for value_tuple in value.split('/'):
                    parts = value_tuple.split('|')
                    if len(parts) >= 4 and (int(parts[0]), int(parts[1])) in targets:
                        reward_hits.append(dict(table=table, line=line, column=column,
                                                tuple=value_tuple, row=row))
    item_base = {r['type_id']: r for r in rows('item_base')}
    bag_sources = []
    for typ, source_rows, bases, id_key in [
        (5, rows('item_name'), item_base, 'Ftype_id'),
        (6, rows('skill_name'), {r['type_id']: r for r in rows('skill_base')}, 'type_id'),
    ]:
        for row in source_rows:
            if '乾坤袋' not in (row.get('product_desc') or ''):
                continue
            tid = row[id_key]
            bag_sources.append(dict(object_type=typ, id=int(tid), name=row['name'],
                                    quality=int(bases[tid]['quality']),
                                    main_type=int(bases[tid]['main_type']) if typ == 5 else None,
                                    source_text=row['product_desc'],
                                    bag_id=None, count=None, official_probability=None))
    local_rules = json.loads((ROOT / 'server_config/vip_rules.json').read_text())
    weight_sum = sum(r['weight'] for r in local_rules['bag_pool'])
    local_pool = [dict(**r, probability=r['weight'] / weight_sum)
                  for r in local_rules['bag_pool']]
    local_inputs = []
    for name in ['server_config/vip_rules.json', 'network_redirect/vip.py',
                 'network_redirect/backend.py', 'network_redirect/immortal.py']:
        local_inputs.append(dict(path=name, sha256=hashlib.sha256((ROOT / name).read_bytes()).hexdigest()))
    report = dict(client='3.87', official_server_available=False, inputs=inputs,
                  equipment=equipment, skills=skills, reward_hits=reward_hits,
                  material_recipes=rows('material_transform'),
                  skill_recipes=rows('skill_material_transform'),
                  bag_source_mentions=bag_sources,
                  nonzero_item_random_weigth=[r for r in item_base.values()
                                             if r['random_weigth'] not in ('', '0')],
                  local_bag_rules=dict(mode=local_rules['mode'], inputs=local_inputs,
                                      vip_bag_id=1031, pool=local_pool))
    (OUT / 'audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(f'Verified {len(TABLES)} CSVs; {len(equipment)} five-star equipment, '
          f'{len(skills)} five-star skills, {len(reward_hits)} reward tuples.')


if __name__ == '__main__':
    main()
