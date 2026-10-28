"""Check native Dragon Boat UI with temporary state and captured network sends."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis/tools')]
from network_redirect import activity, activity_rice as rice, activity_moon as moon, activity_seasonal as season, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode
from android_emulator.config import load_config, device_environment
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR


def fixture():
    now=1793073600
    with tempfile.TemporaryDirectory() as tmp:
        b=Backend(Path(tmp),18770,lambda *a,**k:None);r=b.activity_rules;role=b.profile()
        activity.prepare(role,now,r);status=season.status(role,now,r)['dragon_boat_info']
        summon.add_item(role,1208,150);summon.add_item(role,1209,150)
        ids=[next(i['id'] for i in role['attachments'] if i['type_id']==t) for t in (1208,1209)]
        for _ in range(10):
            packet=season.settle(role,1126,dict(compose_type=1,material_count=2,material_list=[dict(id=i) for i in ids]),now,r)[0]
        crafted=login_fields(decode(packet)[2]['data'])
        summon.add_item(role,1216,3);item=next(i for i in role['attachments'] if i['type_id']==1216)
        with patch.object(rice,'randbelow',side_effect=[0,6500,9999]):
            p=rice.use(role,dict(item_type=1216,item_id=item['id'],item_count=3,des_type=1,des_id=0),r)[0]
        data=dict(now=now,status=status,crafted=crafted,opened=login_fields(decode(p)[2]['data']))
        summon.add_item(role,1133,1);item=next(i for i in role['attachments'] if i['type_id']==1133)
        with patch.object(moon,'randbelow',return_value=6500):
            p=moon.use(role,dict(item_type=1133,item_id=item['id'],item_count=1,des_type=1,des_id=0),r)[0]
        data['opened_moon']=login_fields(decode(p)[2]['data'])
        summon.add_item(role,1217,1);item=next(i for i in role['attachments'] if i['type_id']==1217)
        p=season.use_food(role,dict(item_type=1217,item_id=item['id'],item_count=1,des_type=1,des_id=0),r)[0]
        data['opened_legacy']=login_fields(decode(p)[2]['data'])
        source='local RICE_PREVIEW=true\nlocal FIXTURE='+summon.lua(data)+'\n'+(ROOT/'analysis/tools/rice_client_harness.lua').read_text().replace('-- INSTALL_PATCH',rice.client_source(r))
        b.close();return source


def main():
    import frida
    config=load_config(ROOT/'game.json');pid=next(p for p,n in processes(config).items() if n==config['package'])
    session=frida.get_device(config['serial'],timeout=10).attach(pid)
    evaluator=LUA_EVALUATOR.replace('pending={code,resolve};',"const task={code,resolve};pending=task;setTimeout(()=>{if(pending===task){pending=null;resolve({status:-1,result:'No Lua frame'});}},15000);")
    script=session.create_script(evaluator)
    destination=ROOT/'analysis/evidence/rice';destination.mkdir(parents=True,exist_ok=True)
    report=dict(native_cocos=True,live_account_resources_changed=False,network_sends_captured=True)
    try:
        script.load();raw=script.exports_sync.evaluate(fixture());report['raw']=raw
        checks=[]
        if raw.get('status')==0:
            for line in raw['result'].splitlines():
                name,sep,rest=line.partition(':')
                if sep and rest.startswith(('true:','false:')):
                    ok,_,error=rest.partition(':');checks.append(dict(name=name,passed=ok=='true',error=error))
        report['checks']=checks;report['passed']=len(checks)==16 and all(c['passed'] for c in checks)
        if report['passed']:
            time.sleep(.6)
            shot=subprocess.run([str(config['adb_path']),'-s',config['serial'],'exec-out','screencap','-p'],env=device_environment(config),capture_output=True,timeout=15,check=True)
            (destination/'main.png').write_bytes(shot.stdout)
    finally:
        try:
            result=script.exports_sync.evaluate('if ricePreview then ricePreview.restore();ricePreview=nil end;return "restored"')
            report['restored']=result==dict(status=0,result='restored')
        finally:script.unload();session.detach()
        (destination/'client_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if not report.get('passed') or not report.get('restored'):raise SystemExit(1)


if __name__=='__main__':main()
