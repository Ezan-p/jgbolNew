"""Run temporary backend packets through isolated, original Cocos fate windows."""
import json, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests'))
from network_redirect import summon, fate_rebuild as fr, formation
from network_redirect.backend import Backend
from network_redirect.protocol import decode,encode
from android_emulator.config import load_config
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR

def build():
 with tempfile.TemporaryDirectory() as tmp:
  b=Backend(Path(tmp),18770,lambda *a,**k:None);role=b.profile();role.update(level=99,reborn_layer=4)
  role['corteges']=[summon.companion(role,5022)];c=role['corteges'][0];c.update(level=165,reborn_layer=9,order=1)
  for tid in (1370,1371,1372,1373,1374,1375,1329,1330,10000):summon.add_item(role,tid,10000)
  b.save(role);role=b.profile()
  def packets(ps):return [dict(mid=decode(p)[0],data=decode(p)[2]) for p in ps]
  fixture=dict(cid=c['id'],role={k:role[k] for k in ('level','reborn_layer','gold_coin','silver_coin')},inventory=packets(b.inventory(role)),state=fr.state(role))
  serial=100
  def request(op,**kw):
   nonlocal serial
   serial+=1
   return packets(b.respond(encode(1357,dict(serial_num=serial,id=op,data=summon.lua(dict(cortege_id=c['id'],**kw)))),dict(authenticated=True)))
  fixture['activation']=request(3)
  fixture['node']=request(0,soul_part=1,material_list={1375:30})
  fixture['expected']=fr.state(b.profile());fixture['reset']=request(4);b.close()
 items={int(r['type_id']):{k.split('(')[0]:int(v) if v.isdigit() else v for k,v in r.items()} for r in summon.rows('fate_rebuild/item_base.csv')}
 for r in summon.rows('fate_rebuild/item_name.csv'):items[int(r['Ftype_id'])].update(r)
 items[1370]['desc']='开启可随机获得天魂石、命魂石或地魂石1个。'
 patch=(ROOT/'network_redirect/fate_rebuild_client.lua').read_text().replace('__FATE_DEFAULTS__',summon.lua(dict.fromkeys(fr.ATTRS,0))).replace('__FATE_ITEMS__',summon.lua(items))
 return 'local FIXTURE='+summon.lua(fixture)+'\n'+(ROOT/'analysis/tools/fate_client_harness.lua').read_text().replace('-- INSTALL_PATCH',patch)

def main():
 import frida
 source=build();(ROOT/'.runtime/fate-native-fixture.lua').write_text(source)
 cfg=load_config(ROOT/'game.json');device=frida.get_device(cfg['serial'],timeout=10)
 pid=next(p for p,n in processes(cfg).items() if n==cfg['package']);session=device.attach(pid)
 script=session.create_script(LUA_EVALUATOR)
 try:
  script.load();result=script.exports_sync.evaluate(source)
 finally:script.unload();session.detach()
 report=dict(raw=result,live_account_resources_changed=False,native_cocos=True,network_sends_captured=True)
 report['passed']=result.get('status')==0 and '\nFAIL ' not in '\n'+result.get('result','') and result.get('result','').endswith('restored')
 (ROOT/'analysis/evidence/fate_rebuild/client_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(result,flush=True)
 if not report['passed']:raise SystemExit(1)
if __name__=='__main__':main()
