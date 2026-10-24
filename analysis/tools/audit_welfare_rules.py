"""Re-extract welfare evidence directly from original APK resources, with hashes."""
import hashlib,json,sys
from pathlib import Path
from luajit_static import parse,listing
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'analysis/evidence/welfare'
def main():
 OUT.mkdir(exist_ok=True)
 index=dict(line.split('====')[:2] for line in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
 inputs=[]
 for name in ['ui/actNoticeUI','ui/bonusLayerUI','ui/rechargeUI','data','event_mgr','common/common_def']:
  path=ROOT/'jgbol3.87/assets/release_'/index['lua/'+name+'.lua'];chunk=parse(path.read_bytes())
  (OUT/(name.replace('/','_')+'.txt')).write_text('\n'.join('NUMERIC proto%d %r'%(p['id'],p['numbers']) for p in chunk['protos'])+'\n'+listing(chunk))
  inputs.append(dict(logical='lua/'+name+'.lua',physical=str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
 (OUT/'audit.json').write_text(json.dumps(dict(inputs=inputs,official_server_available=False,requests=[1127,1239,1352,1201,1112],events=[127,135,202,60,80]),indent=2)+'\n')
if __name__=='__main__':main()
