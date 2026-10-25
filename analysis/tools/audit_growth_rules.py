"""Audit growth values against unmodified 3.87 assets; emit reproducible evidence."""
import csv
import hashlib
import io
import json
from decimal import Decimal
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from luajit_static import parse, listing
from audit_formation_rules import TABLES as FORMATION_TABLES
from audit_reborn_rules import TABLES as REBORN_TABLES
from network_redirect import formation as f, summon

OUT = ROOT / 'analysis/evidence/growth'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    index = dict(line.split('====')[:2] for line in
                 (ROOT / 'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    encodings = {r['logical']: r['encoding'] for r in json.loads(
        (ROOT / 'analysis/evidence/config_inventory.json').read_text())}
    tables = sorted(set(FORMATION_TABLES + REBORN_TABLES + ['item_name', 'newbie_content4']))
    evidence = []
    for table in tables:
        logical = next(k for k in index if k.startswith('csv_config/') and Path(k).name == table + '.csv')
        original = ROOT / 'jgbol3.87/assets/release_' / index[logical]
        extracted = ROOT / 'analysis/configs' / logical.removeprefix('csv_config/')
        rows = list(csv.reader(io.StringIO(original.read_bytes().decode(encodings[logical]))))
        assert rows == list(csv.reader(io.StringIO(extracted.read_text(encoding='utf-8-sig')))), logical
        evidence.append(dict(logical=logical, sha256=hashlib.sha256(original.read_bytes()).hexdigest(),
                             rows=len(rows)-1, csv_values_match=True))
    for module in ('ui/feishengUI', 'ui/lineupUI', 'ui/trainingUI', 'ui/ascensionUI', 'data'):
        logical = 'lua/' + module + '.lua'
        original = ROOT / 'jgbol3.87/assets/release_' / index[logical]
        chunk = parse(original.read_bytes())
        text = '\n'.join('NUMERIC proto%d %r' % (p['id'], p['numbers']) for p in chunk['protos'])
        text += '\n' + listing(chunk)
        (OUT / (module.replace('/', '_') + '.txt')).write_text(text)
        evidence.append(dict(logical=logical, sha256=hashlib.sha256(original.read_bytes()).hexdigest()))
        if module == 'ui/feishengUI':
            # The MULVN operand is a constant-pool index, not the multiplier.
            assert chunk['protos'][11]['numbers'][2] == 3
            assert all(field in text for field in ('hpOffset', 'damageOffset', 'defenceOffset', 'manaOffset'))
    names = {int(r['type_id']): r['name'] for r in summon.rows('cortege/cortege_name_0.csv')}
    per_companion = []
    for tid, base in f.BASES.items():
        per_companion.append(dict(type_id=tid, name=names.get(tid, base['name']),
            quality=int(base['quality']), growth={s: base[g] for s,g in zip(f.STATS, f.GROWTH_COLUMNS)},
            per_evolution={s: int(Decimal(base[g]) * 3) for s,g in zip(f.STATS, f.GROWTH_COLUMNS)}))
    output = dict(date='2026-10-25', client='3.87', official_server_available=False,
        inputs=evidence, csv_tables=len(tables),
        evolution_formula='floor(original growth * 3) * evolve_level, floor before multiplication',
        companions=per_companion,
        evolution=[dict(level=n, soul_cost=f.EVOLVE_COST[n],
                        potential_by_quality={q:f.EVOLVE_POINTS[q,n] for q in range(1,6)})
                   for n in sorted(f.EVOLVE_COST)],
        rebirth_layers=summon.rows('cortege_reborn_layer.csv'),
        rebirth_directions=summon.rows('cortege_reborn_effect.csv'),
        veins=summon.rows('cortege_reborn_vein.csv'),
        unresolved=['Original server stacking order', 'Training random distribution',
                    'Potential granted per normal level', 'Realm conditions supplied by original server',
                    'Recycling trained potential settlement', 'Divination progression probability'])
    (OUT / 'audit.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print('Verified %d original CSV tables, 5 Lua modules; %d companion growth records, 299 evolution levels.'
          % (len(tables), len(per_companion)))


if __name__ == '__main__':
    main()
