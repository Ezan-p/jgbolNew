"""Check native Mid-Autumn UI with temporary state and captured network sends."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis/tools')]
from network_redirect import activity, activity_moon as moon, activity_seasonal as season, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode
from android_emulator.config import load_config, device_environment
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR


def fixture():
    now=1793073600
    with tempfile.TemporaryDirectory() as tmp:
        b=Backend(Path(tmp),18770,lambda *a,**k:None);r=b.activity_rules;role=b.profile()
        activity.prepare(role,now,r);status=season.status(role,now,r)['midautumn_data']
        packets=season.settle(role,1333,dict(flag=1,src_type=1135),now,r)
        crafted,news=[login_fields(decode(p)[2]['data']) for p in packets]
        summon.add_item(role,1133,3);item=next(i for i in role['attachments'] if i['type_id']==1133)
        with patch.object(moon,'randbelow',side_effect=[0,6500,9999]):
            p=moon.use(role,dict(item_type=1133,item_id=item['id'],item_count=3,des_type=1,des_id=0),r)[0]
        data=dict(now=now,status=status,crafted=crafted,news=news,opened=login_fields(decode(p)[2]['data']))
        source='local MOON_PREVIEW=true\nlocal FIXTURE='+summon.lua(data)+'\n'+(ROOT/'analysis/tools/moon_client_harness.lua').read_text().replace('-- INSTALL_PATCH',moon.client_source(r))
        b.close();return source


def main():
    import frida
    config=load_config(ROOT/'game.json');pid=next(p for p,n in processes(config).items() if n==config['package'])
    session=frida.get_device(config['serial'],timeout=10).attach(pid)
    evaluator=LUA_EVALUATOR.replace('pending={code,resolve};',"const task={code,resolve};pending=task;setTimeout(()=>{if(pending===task){pending=null;resolve({status:-1,result:'No Lua frame'});}},15000);")
    script=session.create_script(evaluator)
    destination=ROOT/'analysis/evidence/moon';destination.mkdir(parents=True,exist_ok=True)
    report=dict(native_cocos=True,live_account_resources_changed=False,network_sends_captured=True)
    try:
        script.load();raw=script.exports_sync.evaluate(fixture());report['raw']=raw
        checks=[]
        if raw.get('status')==0:
            for line in raw['result'].splitlines():
                name,sep,rest=line.partition(':')
                if sep and rest.startswith(('true:','false:')):
                    ok,_,error=rest.partition(':');checks.append(dict(name=name,passed=ok=='true',error=error))
        report['checks']=checks;report['passed']=len(checks)==14 and all(c['passed'] for c in checks)
        if report['passed']:
            time.sleep(.6)
            shot=subprocess.run([str(config['adb_path']),'-s',config['serial'],'exec-out','screencap','-p'],env=device_environment(config),capture_output=True,timeout=15,check=True)
            (destination/'main.png').write_bytes(shot.stdout)
    finally:
        try:
            result=script.exports_sync.evaluate('if moonPreview then moonPreview.restore();moonPreview=nil end;return "restored"')
            report['restored']=result==dict(status=0,result='restored')
        finally:script.unload();session.detach()
        (destination/'client_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if not report.get('passed') or not report.get('restored'):raise SystemExit(1)


if __name__=='__main__':main()
