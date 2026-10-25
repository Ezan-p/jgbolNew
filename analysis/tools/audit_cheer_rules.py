"""Reproduce 3.87 Bagua evidence and verify extracted CSV against APK assets."""
import ast
import csv
import hashlib
import io
import json
from pathlib import Path
from luajit_static import parse, listing
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'analysis/evidence/cheer'
MODULES=['ui/cheerSquadUI','ui/packageUI','ui/checkLineupUI','common/common_def','event_mgr']
TABLES=['cortege_cheer_config','cheer_skill_config','cortege_quality']
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
    for line in (OUT/'common_common_def.txt').read_text().splitlines():
        if "{'kind': 'table'" not in line:
            continue
        data = ast.literal_eval(line[line.index("{'kind'"):])['value']
        if isinstance(data, dict) and 'cheer_count' in data:
            prefixes = ('cheer_', 'heaven_', 'earth_', 'shake_', 'sunda_', 'water_', 'fire_', 'hill_', 'pool_')
            prefixes += tuple('un' + k for k in prefixes[1:])
            (OUT/'role_attributes.json').write_text(json.dumps({k:v for k,v in data.items() if k.startswith(prefixes)}, indent=2)+'\n')
    (OUT/'audit.json').write_text(json.dumps(dict(date='2026-10-25',client='3.87',official_server_available=False,inputs=evidence,implemented_requests=[1087],config='server_config/cheer_rules.json',documentation='docs/八卦系统规则与调试.md'),ensure_ascii=False,indent=2)+'\n')
    print('Verified 5 original Lua modules and 3 original CSV tables.')
if __name__=='__main__':main()
