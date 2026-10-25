"""Verify original equipment tables byte-for-value; preserve Lua evidence."""
import csv
import hashlib
import io
import json
import sys
from pathlib import Path
from luajit_static import parse, listing
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import equipment as e, formation as f, summon, equipment_crafting as crafting, reborn
OUT=ROOT/'analysis/evidence/equipment'
TABLES=['item_base','item_name','equip_enhance_cost','equip_enhance_weight','equip_star_cost',
'equip_advance_cost','equip_advance_worth','equip_reborn_base','equip_reborn_advance',
'equip_reborn_fate','equip_reborn_level_plus','stone_cost_worth','stone_reborn_cost_worth',
'ling_stone_value','equip_transfer_config','equip_compose_random','item_sell_config',
'material_transform','material_transform_index','item_exchange_config','skill_material_transform','jingpo_transform']
MODULES=['ui/stoneUI','ui/stoneUpgradeUI','ui/stoneCastUI','ui/equipAscUI','ui/equipCastUI',
'ui/equipmentUpgradeUI','ui/equipAdvanceUI','ui/equipTransUI','ui/equipPieceUI','ui/packageUI',
'ui/forgeUI','ui/smithUI','ui/batchSaleUI','ui/cortegeRecycleUI','ui/skillUpgradeUI','ui/jpChangeUI','ui/charPositionUI']

def main():
 OUT.mkdir(exist_ok=True)
 idx=dict(x.split('====')[:2] for x in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
 enc={r['logical']:r['encoding'] for r in json.loads((ROOT/'analysis/evidence/config_inventory.json').read_text())}
 evidence=[]
 for name in ['csv_config/'+t+'.csv' for t in TABLES]+['lua/'+m+'.lua' for m in MODULES]:
  path=ROOT/'jgbol3.87/assets/release_'/idx[name];raw=path.read_bytes()
  row=dict(logical=name,sha256=hashlib.sha256(raw).hexdigest())
  if name.endswith('.csv'):
   original=list(csv.reader(io.StringIO(raw.decode(enc[name]))))
   assert original==list(csv.reader(io.StringIO((ROOT/'analysis/configs'/Path(name).name).read_text(encoding='utf-8-sig')))),name
   row.update(rows=len(original)-1,csv_values_match=True)
  else:
   c=parse(raw)
   (OUT/(name.removeprefix('lua/').removesuffix('.lua').replace('/','_')+'.txt')).write_text('\n'.join('NUMERIC proto%d %r'%(p['id'],p['numbers']) for p in c['protos'])+'\n'+listing(c))
  evidence.append(row)
 names={int(next(iter(r.values()))):r['name'] for r in summon.rows('item_name.csv')}
 gear=[]
 for tid,cfg in f.ITEMS.items():
  if int(cfg['main_type']) not in (1,2,3):continue
  gear.append(dict(type_id=tid,name=names.get(tid,''),quality=int(cfg['quality']),kind=int(cfg['main_type']),
                   base=e.base_effect(dict(type_id=tid,level=1)).to_eng_string(),growth=cfg['upgrade_plus'],top_level=int(cfg['top_level'])))
 report=dict(date='2026-10-25',client='3.87',official_server_available=False,inputs=evidence,
             equipment=gear,stone_rates=[dict(kind=k,level=l,rate=str(e.stone_rate(k,l))) for k in (1,2,3) for l in range(1,13)],
             original_formula='B = (base + (level-1)*growth*(1+reborn*0.12))*(1+star_level); floor(B)+floor(B*sum(stone_rates))+floor(B*advance_rate+advance_flat)+floor(B*cast_rate+cast_flat)',
             inferred_stone_rules=e.load_rules(), inferred_crafting_rules=crafting.load_rules(),
             inferred_attribute_policy=f.load_rules()['attribute_policy'], initial_cast_level=reborn.load_rules()['equip_initial_cast_level'],
             implemented_protocols=[1052,1053,1054,1055,1056,1073,1074,1079,1225,1328],
             official_unverified=['Failure compensation increment/distribution','Server-wide stat stacking order and advance extra base','Server enable levels except explicit client gates','Enhancement batch count','Initial casting level','Activity recipes/limits and recovery policy'])
 (OUT/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print('Verified %d CSV tables, %d Lua modules, %d equipment records, 36 stone coefficients.'%(len(TABLES),len(MODULES),len(gear)))
if __name__=='__main__':main()
