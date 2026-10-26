"""Verify every used array table against the packaged 3.87 resources."""
import csv
import hashlib
import io
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import spirit_array as a
idx=dict(x.split('====')[:2] for x in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
enc={r['logical']:r['encoding'] for r in json.loads((ROOT/'analysis/evidence/config_inventory.json').read_text())}
result=[]
for name in ('ling_active','ling_upgrade','ling_effect','ling_stone_value','ling_pos_name','ling_first'):
 logical='csv_config/'+name+'.csv';raw=(ROOT/'jgbol3.87/assets/release_'/idx[logical]).read_bytes()
 original=list(csv.reader(io.StringIO(raw.decode(enc[logical]))))
 extracted=list(csv.reader(io.StringIO((ROOT/'analysis/configs'/(name+'.csv')).read_text(encoding='utf-8-sig'))))
 assert original==extracted,name
 result.append(dict(logical=logical,physical=idx[logical],sha256=hashlib.sha256(raw).hexdigest(),rows=len(original)-1,values_match=True))
assert len(a.NEEDS)==21 and len(a.EFFECTS)==62
assert all(len(x['effect_value'].split('/'))==5 for x in a.EFFECTS)
out=ROOT/'analysis/evidence/spirit_array';out.mkdir(exist_ok=True)
(out/'audit.json').write_text(json.dumps(dict(date='2026-10-26',client='3.87',official_server_available=False,tables=result,policy=a.RULES),ensure_ascii=False,indent=2)+'\n')
print('Verified six original tables, 21 positions, 62 effect rows, five levels.')
