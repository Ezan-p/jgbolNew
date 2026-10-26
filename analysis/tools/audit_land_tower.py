#!/usr/bin/env python3
"""Export the shared tower schedule and check its deterministic progression."""
import csv
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import activity_land_encounters as e, formation
out=ROOT/'analysis/evidence/land';out.mkdir(parents=True,exist_ok=True)
records=[]
for hell in (False,True):
    rows=e.schedule(hell)
    assert len({x['type_id'] for x in rows})==64
    for i,x in enumerate(rows):
        if i:
            assert x['power']>rows[i-1]['power']
            assert all(x['units'][0][k]>rows[i-1]['units'][0][k] for k in formation.STATS)
        records.append(dict(world='hell' if hell else 'normal',layer=x['layer'],name=x['name'],
                            type_id=x['type_id'],level=x['level'],count=len(x['units']),power=x['power'],
                            lineup='|'.join(str(u['type']) for u in x['units']),
                            **{k:x['units'][0][k] for k in formation.STATS}))
assert all(b['power']>a['power'] for a,b in zip(e.schedule(False),e.schedule(True)))
with (out/'tower_schedule.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
audit=dict(revision=e.rules()['revision'],rule_class='B',floors_per_world=64,distinct_chiefs=64,
           strictly_increasing_chief_stats=True,strictly_increasing_army_power=True,
           original_sources=['analysis/configs/cortege/cortege_base_0.csv','analysis/configs/cortege/cortege_name_0.csv'],
           missing_original_rule='No per-floor prey boss mapping in extracted CSV inventory or landUI/data loaders.',
           native_contract=dict(portrait_target='1-based visible slot',inspection='enemy.role_id',visible_slots=4),
           evidence='landUI L1751/L1767/L1783/L1807; data L1344-1410')
(out/'tower_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(audit,ensure_ascii=False))
