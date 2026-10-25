"""Reproduce original 3.87 monument contracts without running bytecode."""
import csv,hashlib,io,json
from pathlib import Path
from luajit_static import parse,listing
ROOT=Path(__file__).resolve().parents[2]
def main():
 out=ROOT/'analysis/evidence/monument';out.mkdir(exist_ok=True)
 idx=dict(l.split('====')[:2] for l in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
 names=['ui/monumentUI','ui/mainUI','ui/crossRankUI','ui/rankUI','ui/guildFightUI','ui/crossRealm','ui/guildPartyUI','event_mgr','common/common_def','data','ui/fightrecordUI']
 records=[]
 for n in names:
  p=ROOT/'jgbol3.87/assets/release_'/idx['lua/'+n+'.lua'];c=parse(p.read_bytes())
  (out/(n.replace('/','_')+'.txt')).write_text(listing(c))
  records.append(dict(logical='lua/'+n+'.lua',physical=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 enc={v['logical']:v['encoding'] for v in json.loads((ROOT/'analysis/evidence/config_inventory.json').read_text())}
 for name in ('rank_prize','crossRank_realm_config'):
  logical='csv_config/'+name+'.csv';p=ROOT/'jgbol3.87/assets/release_'/idx[logical]
  original=list(csv.reader(io.StringIO(p.read_bytes().decode(enc[logical]))))
  extracted=list(csv.reader(io.StringIO((ROOT/'analysis/configs'/ (name+'.csv')).read_text(encoding='utf-8-sig'))))
  assert original==extracted,logical
  records.append(dict(logical=logical,physical=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),csv_values_match=True))
 (out/'audit.json').write_text(json.dumps(dict(client='3.87',official_server_available=False,inputs=records),ensure_ascii=False,indent=2)+'\n')
 print('Verified 11 original Lua modules and 2 original CSV tables')
if __name__=='__main__':main()
