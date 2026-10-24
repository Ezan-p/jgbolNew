"""Reproduce 3.87 rebirth evidence and verify extracted CSV against APK assets."""
import csv
import hashlib
import io
import json
from pathlib import Path
from luajit_static import parse, listing
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'analysis/evidence/reborn'
MODULES=['ui/roleRebornUI','ui/ascensionUI','ui/equipAscUI','ui/equipCastUI','ui/wakeUI','ui/runeUI','common/common_def','event_mgr']
TABLES=['cortege_reborn_config','cortege_reborn_layer','cortege_reborn_vein','cortege_reborn_effect','equip_reborn_base','equip_reborn_advance','equip_reborn_fate','equip_reborn_level_plus','awaken_skill_conf','awaken_skill_rate','ext_star_config','star_config','star_relation_config','star_element_open','star_element_relation','star_level_exp','star_decompose_config']
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    index=dict(line.split('====')[:2] for line in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    enc={r['logical']:r['encoding'] for r in json.loads((ROOT/'analysis/evidence/config_inventory.json').read_text())}
    evidence=[]
    for name in ['lua/'+m+'.lua' for m in MODULES]+['csv_config/'+t+'.csv' for t in TABLES]:
        path=ROOT/'jgbol3.87/assets/release_'/index[name]
        row=dict(logical=name,physical=str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        if name.endswith('.csv'):
            original=list(csv.reader(io.StringIO(path.read_bytes().decode(enc[name]))))
            extracted=ROOT/'analysis/configs'/Path(name).name
            assert original==list(csv.reader(io.StringIO(extracted.read_text(encoding='utf-8-sig')))),name
            row['csv_values_match']=True
        else:
            chunk=parse(path.read_bytes())
            text='\n'.join('NUMERIC proto%d %r'%(p['id'],p['numbers']) for p in chunk['protos'])+'\n'+listing(chunk)
            (OUT/(name.removeprefix('lua/').removesuffix('.lua').replace('/','_')+'.txt')).write_text(text)
        evidence.append(row)
    (OUT/'audit.json').write_text(json.dumps(dict(date='2026-10-24',client='3.87',official_server_available=False,inputs=evidence,implemented_requests=[1328,1332,1337,1338,1339,1340,1341,1342],config='server_config/reborn_rules.json',documentation='docs/转生模块规则与调试.md'),ensure_ascii=False,indent=2)+'\n')
    print('Verified 8 original Lua modules and 17 original CSV tables.')
if __name__=='__main__':main()
