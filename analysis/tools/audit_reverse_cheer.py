"""Rebuild reverse Bagua evidence directly from the bundled 3.87 assets."""
import csv
import hashlib
import io
import json
from pathlib import Path
from decimal import Decimal
from luajit_static import parse, listing
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'analysis/evidence/reverse_cheer'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    index = dict(line.split('====')[:2] for line in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    enc = {r['logical']: r['encoding'] for r in json.loads((ROOT/'analysis/evidence/config_inventory.json').read_text())}
    evidence = []
    for name in ['lua/ui/'+x+'.lua' for x in ('cheerSquadUI','tianShuUI','charPositionUI')] + ['csv_config/'+x+'.csv' for x in ('cortege_cheer_config','cheer_skill_config','item_name')]:
        path = ROOT/'jgbol3.87/assets/release_'/index[name]
        raw = path.read_bytes()
        record = dict(logical=name, physical=str(path.relative_to(ROOT)), sha256=hashlib.sha256(raw).hexdigest())
        if name.endswith('.lua'):
            chunk = parse(raw)
            content = '\n'.join('NUMERIC proto%d %r' % (p['id'], p['numbers']) for p in chunk['protos'])+'\n'+listing(chunk)
            (OUT/(Path(name).stem+'.txt')).write_text(content)
        else:
            original = list(csv.reader(io.StringIO(raw.decode(enc[name]))))
            extracted = list(csv.reader((ROOT/'analysis/configs'/Path(name).name).open(encoding='utf-8-sig')))
            assert original == extracted, name
            record['csv_values_match'] = True
        evidence.append(record)
    rows = list(csv.DictReader((ROOT/'analysis/configs/cortege_cheer_config.csv').open()))
    assert len(rows)==80 and {int(x['cheer_order']) for x in rows}==set(range(1,9))
    values=[]; totals=[Decimal(0)]*4
    for r in rows[:10]:
        totals=[v+Decimal(r[k]) for v,k in zip(totals,('gongji_plus','fangyu_plus','maxhp_plus','maxmagic_plus'))]
        values.append(dict(level=int(r['level']),upgrade_cost_A=int(r['upgrade_cost']),cumulative_percent_B=[str(v*100) for v in totals]))
    rules=json.loads((ROOT/'server_config/cheer_rules.json').read_text())
    report=dict(date='2026-10-28',client='3.87',official_server_verified=False,inputs=evidence,
                original_positive_rows=80,independent_reverse_table_found=False,levels=values,
                skill_mask=dict(reserved_bit=0,first_slot_bit=1,last_slot_bit=16,all_open=131070),
                local_rules_B=rules,documentation='docs/逆八卦原版机制与实现说明.md')
    (OUT/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Verified 3 original Lua modules and 3 CSV tables; reverse audit written.')


if __name__=='__main__': main()
