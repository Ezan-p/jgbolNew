"""Audit original packaged tables and bytecode constants used by recycling."""
import csv,hashlib,io,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from analysis.tools.luajit_static import parse
from network_redirect import cortege_recycle as r
idx=dict(x.split('====')[:2] for x in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
enc={r['logical']:r['encoding'] for r in json.loads((ROOT/'analysis/evidence/config_inventory.json').read_text())}
rows=[]
for name in ('fate_config','item_base','item_name','equip_transfer_config','equip_star_cost','equip_advance_cost','equip_enhance_cost'):
 logical='csv_config/'+name+'.csv'
 if logical not in idx:continue
 raw=(ROOT/'jgbol3.87/assets/release_'/idx[logical]).read_bytes()
 assert list(csv.reader(io.StringIO(raw.decode(enc[logical]))))==list(csv.reader(io.StringIO((ROOT/'analysis/configs'/(name+'.csv')).read_text(encoding='utf-8-sig')))),name
 rows.append(dict(logical=logical,sha256=hashlib.sha256(raw).hexdigest(),values_match=True))
logical='lua/ui/cortegeRecycleUI.lua';raw=(ROOT/'jgbol3.87/assets/release_'/idx[logical]).read_bytes();p=parse(raw)
assert p['protos'][40]['numbers'][:2]==[1,15]
rows.append(dict(logical=logical,sha256=hashlib.sha256(raw).hexdigest(),preview_increment=1,preview_level_modulo=15))
out=ROOT/'analysis/evidence/recycle';out.mkdir(exist_ok=True)
(out/'audit.json').write_text(json.dumps(dict(date='2026-10-26',official_server_available=False,evidence=rows,policy=r.load_rules()),ensure_ascii=False,indent=2)+'\n')
print('Original recycling tables and Lua numeric pool verified')
