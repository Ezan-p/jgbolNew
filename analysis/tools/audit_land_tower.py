#!/usr/bin/env python3
"""Export the shared tower schedule and check its deterministic progression."""
import csv
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import activity_land_encounters as e, formation, activity
from network_redirect import activity_land_npc as npc, activity_land_rewards as rewards
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
rewards.validate_cards(r)
guards=[]
for map_level,level in enumerate(r['land_guard_level_by_map'],1):
    previous_min=None
    for tower_type,tier in enumerate(r['land_guard_tier_by_type'],1):
        candidates=[npc.catalog()[key] for key in npc.guard_pool(map_level,tower_type,r)]
        powers=[npc.power(n,8) for n in candidates]
        assert powers and (previous_min is None or max(powers)<previous_min)
        old_level=(24,50,70,90)[map_level-1]
        old_tier=('T5','T4','T3','T5')[tower_type-1]
        old_max=max(npc.power(n,8) for n in npc.catalog().values()
                    if n['role']['level']==old_level and n['tier']==old_tier)
        if tower_type<=2:
            assert min(powers)>old_max*2
        else:
            prior_tier=('T2','T3')[tower_type-3]
            prior_min=min(npc.power(n,8) for n in npc.catalog().values()
                          if n['role']['level']==level and n['tier']==prior_tier)
            assert max(powers)<prior_min*0.4
        previous_min=min(powers)
        for n in candidates:
            rate=r['land_tower_soul_by_type'][tower_type-1]
            guards.append(dict(map_level=map_level,tower_type=tower_type,npc_id=n['npc_id'],
                               name=n['role']['name'],level=level,tier=tier,count=len(npc.units(n['npc_id'],8)),
                               power=npc.power(n,8),soul_per_minute=rate,
                               total_soul=rate*(r['land_tower_duration']//r['land_tower_tick'])))
with (out/'tower_guards.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(guards[0]),lineterminator='\n');w.writeheader();w.writerows(guards)
audit=dict(revision=e.rules()['revision'],rule_class='B',floors_per_world=64,distinct_chiefs=64,
           strictly_increasing_chief_stats=True,strictly_increasing_army_power=True,
           growth={k:e.rules()[k] for k in ('normal_start_level','hell_start_level','normal_level_step',
                   'hell_level_step','stat_percent','min_floor_growth_percent',
                   'normal_stat_multiplier','hell_stat_multiplier')},
           rewards=dict(pool=pool,normal_cards=5,hell_cards=3,draw='weighted_category_with_stone_cap_then_shuffle',
                        stone_card_limits=dict(normal=2,hell=1),
                        category_weights=r['land_card_weights'],
                        costs=r['land_card_gold'],full_card_rewards=r['land_full_card_rewards'],
                        sweep_rewards=r['land_sweep_rewards']),
           unit_rows=len(units),guard_rows=len(guards),
           top_guard_min_exceeds_twice_202610_max=True,
           entry_guard_max_below_40_percent_of_20261109_min=True,
           travel_soul_by_map=r['land_travel_soul_by_map'],tower_soul_by_type=r['land_tower_soul_by_type'],
           original_sources=['analysis/configs/cortege/cortege_base_0.csv','analysis/configs/cortege/cortege_name_0.csv'],
           missing_original_rule='No per-floor prey boss mapping in extracted CSV inventory or landUI/data loaders.',
           native_contract=dict(portrait_target='1-based visible slot',inspection='enemy.role_id',visible_slots=4),
           evidence='landUI L1751/L1767/L1783/L1807; data L1344-1410')
(out/'tower_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(audit,ensure_ascii=False))
