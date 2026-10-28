#!/usr/bin/env python3
"""Export the shared tower schedule and check its deterministic progression."""
import csv
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import activity_land_encounters as e, formation, activity
out=ROOT/'analysis/evidence/land';out.mkdir(parents=True,exist_ok=True)
records=[];units=[]
for hell in (False,True):
    rows=e.schedule(hell)
    assert len({x['type_id'] for x in rows})==64
    for i,x in enumerate(rows):
        if i:
            assert x['power']>rows[i-1]['power']
            assert all(x['units'][0][k]>rows[i-1]['units'][0][k] for k in formation.STATS)
            assert all(x['units'][0][k]*100>=rows[i-1]['units'][0][k]*(100+e.rules()['min_floor_growth_percent']) for k in formation.STATS)
        records.append(dict(world='hell' if hell else 'normal',layer=x['layer'],name=x['name'],
                            type_id=x['type_id'],level=x['level'],count=len(x['units']),power=x['power'],
                            lineup='|'.join(str(u['type']) for u in x['units']),
                            **{k:x['units'][0][k] for k in formation.STATS}))
        for u in x['units']:
            units.append(dict(world='hell' if hell else 'normal',layer=x['layer'],
                              order=u['order'],type_id=u['type'],name=e.NAMES[u['type']],
                              level=u['level'],**{k:u[k] for k in formation.STATS},
                              skills='|'.join(f'{skill}:{level}' for skill,level in u['skills'])))
assert all(b['power']>a['power'] for a,b in zip(e.schedule(False),e.schedule(True)))
with (out/'tower_schedule.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator='\n');w.writeheader();w.writerows(records)
with (out/'tower_units.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(units[0]),lineterminator='\n');w.writeheader();w.writerows(units)
r=activity.load_rules();pool=r['land_card_rewards']
assert len(pool)==8 and len({tuple(p) for p in pool})==8
audit=dict(revision=e.rules()['revision'],rule_class='B',floors_per_world=64,distinct_chiefs=64,
           strictly_increasing_chief_stats=True,strictly_increasing_army_power=True,
           growth={k:e.rules()[k] for k in ('normal_start_level','hell_start_level','normal_level_step',
                   'hell_level_step','stat_percent','min_floor_growth_percent')},
           rewards=dict(pool=pool,normal_cards=5,hell_cards=3,draw='uniform_without_replacement_random_order',
                        costs=r['land_card_gold'],full_card_rewards=r['land_full_card_rewards'],
                        sweep_rewards=r['land_sweep_rewards']),
           unit_rows=len(units),
           original_sources=['analysis/configs/cortege/cortege_base_0.csv','analysis/configs/cortege/cortege_name_0.csv'],
           missing_original_rule='No per-floor prey boss mapping in extracted CSV inventory or landUI/data loaders.',
           native_contract=dict(portrait_target='1-based visible slot',inspection='enemy.role_id',visible_slots=4),
           evidence='landUI L1751/L1767/L1783/L1807; data L1344-1410')
(out/'tower_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(audit,ensure_ascii=False))
