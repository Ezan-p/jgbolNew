"""Upgrade disposable shipped-test saves, preserving grants and shared trusted time."""
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v110_test_refresh import WORK, EVIDENCE, APK, PREVIOUS, digest

WORKER = r'''
import collections,json,pathlib,sys,time,secrets
program,directory,mode=sys.argv[1:]
sys.path.insert(0,program)
from offline_android import test_edition_v110 as seed
from network_redirect import game_clock,formation
path=pathlib.Path(directory)
service=None
if mode!='old':
 from network_redirect import network_time
 class Service:
  def __init__(self):
   self.source=game_clock.SystemSource();self.requests=[];self.closed=False
   self.observation=network_time.Observation(time.time(),self.source.elapsed(),self.source.wall(),self.source.boot_id,network_time.HOSTS[:2],1,secrets.token_hex(16))
  def read(self):return self.observation
  def request(self,force=False):self.requests.append(force)
  def close(self):self.closed=True
 service=Service()
kwargs={'network_time':service} if service else {}
a=seed.fixed_accounts_class()(path,18776,lambda *a,**k:None,**kwargs)
b=a.backends[seed.ACCOUNT]
role=b.profile()
if mode=='old':
 role['role_name']='v110整合升级检查'
 role['gold_coin']-=1234
 role['test_v111_sentinel']={'preserve':[1,2,3]}
 formation.debit_item(role,1431,7)
 gear=next(i for i in role['attachments'] if i['attach_type']==5 and i['type_id']==2044)
 gear.update(count=3,level=30,is_lock=1)
 b.save(role,gameplay=False)
 (path/'before.json').write_text(json.dumps(b.profile()))
else:
 before=json.loads((path/'before.json').read_text())
 assert a.base.clock is b.clock
 assert b.clock.network_time is service
 state=json.loads(b.clock.db.execute('SELECT data FROM clock').fetchone()[0])
 assert state['policy_version']==3 and state['status']=='network_synchronized'
 assert not b.clock.quarantined
 for k in ('role_name','gold_coin','silver_coin','test_v108_silver_reserve','test_supply_revision','test_v111_sentinel',seed.MARKER):
  assert role[k]==before[k],k
 def totals(r):
  out=collections.Counter()
  for i in r['attachments']:out[i['attach_type'],i['type_id']]+=i['count']
  return out
 assert totals(role)==totals(before),'item totals changed'
 for c in before['corteges']:
  after=next(x for x in role['corteges'] if x['id']==c['id'])
  for k in ('type','level','evolve_level','reborn_layer','order'):assert after.get(k)==c.get(k),k
 for old in before['attachments']:
  after=next(x for x in role['attachments'] if x['id']==old['id'])
  for k in ('level','advance_level','cast_level','owner_id','equip_order','is_lock'):
   assert after.get(k,0)==old.get(k,0),(old['id'],k)
 assert all(i['count']==1 for i in role['attachments'] if i['attach_type']==5 and int(formation.ITEMS.get(i['type_id'],{}).get('main_type',0)) in (1,2,3))
 assert seed.grant_maps(b) is False
 assert role.get('test_supply_revision')==108
 (path/(mode+'.json')).write_text(json.dumps(role))
a.close()
if service:assert service.closed
'''


def main():
    previous=WORK/'upgrade-previous'
    with zipfile.ZipFile(PREVIOUS) as apk, zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as z:
        z.extractall(previous)
    with tempfile.TemporaryDirectory(prefix='v111-test-upgrade-') as temp:
        for mode,program in [('old',previous),('new',WORK/'program'),('restart',WORK/'program')]:
            subprocess.run([sys.executable,'-I','-c',WORKER,str(program),temp,mode],check=True,timeout=180)
        first=json.loads((Path(temp)/'new.json').read_text())
        second=json.loads((Path(temp)/'restart.json').read_text())
        for key in ('attachments','corteges','gold_coin','silver_coin','test_supply_revision','test_v110_abyss_maps_500_v1'):
            assert first[key]==second[key],key
    report=dict(passed=True,apk_sha256=digest(APK.read_bytes()),source=PREVIOUS.name,
        disposable_save=True,existing_progress_preserved=True,item_totals_preserved=True,
        legacy_equipment_split=True,original_equipment_investment_preserved=True,
        supply_not_repeated=True,maps_not_refilled_after_consumption=True,
        shared_network_clock=True,network_policy_migrated=True,restart_preserves_inventory=True)
    (EVIDENCE/'upgrade-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
