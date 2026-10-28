"""Check native party reward UI with temporary state and captured network sends."""
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis/tools')]
from android_emulator.config import load_config, device_environment
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR


def fixture():
    return (ROOT/'analysis/tools/party_client_harness.lua').read_text().replace('-- INSTALL_PATCH', (ROOT/'network_redirect/party_client.lua').read_text())


def main():
    import frida
    config=load_config(ROOT/'game.json');pid=next(p for p,n in processes(config).items() if n==config['package'])
    session=frida.get_device(config['serial'],timeout=10).attach(pid)
    evaluator=LUA_EVALUATOR.replace('pending={code,resolve};',"const task={code,resolve};pending=task;setTimeout(()=>{if(pending===task){pending=null;resolve({status:-1,result:'No Lua frame'});}},15000);")
    script=session.create_script(evaluator)
    destination=ROOT/'analysis/evidence/party';destination.mkdir(parents=True,exist_ok=True)
    report=dict(native_cocos=True,live_account_resources_changed=False,network_sends_captured=True)
    try:
        script.load();raw=script.exports_sync.evaluate(fixture());report['raw']=raw
        checks=[]
        if raw.get('status')==0:
            for line in raw['result'].splitlines():
                name,sep,rest=line.partition(':')
                if sep and rest.startswith(('true:','false:')):
                    ok,_,error=rest.partition(':');checks.append(dict(name=name,passed=ok=='true',error=error))
        report['checks']=checks;report['passed']=len(checks)==9 and all(c['passed'] for c in checks)
        if report['passed']:
            time.sleep(.6)
            shot=subprocess.run([str(config['adb_path']),'-s',config['serial'],'exec-out','screencap','-p'],env=device_environment(config),capture_output=True,timeout=15,check=True)
            (destination/'rewards_page_1.png').write_bytes(shot.stdout)
            script.exports_sync.evaluate('partyPreview.nextPage();return "page2"')
            time.sleep(.3)
            shot=subprocess.run([str(config['adb_path']),'-s',config['serial'],'exec-out','screencap','-p'],env=device_environment(config),capture_output=True,timeout=15,check=True)
            (destination/'rewards_page_2.png').write_bytes(shot.stdout)
    finally:
        try:
            result=script.exports_sync.evaluate('if partyPreview then partyPreview.restore();partyPreview=nil end;return "restored"')
            report['restore_result']=result
            report['restored']=result==dict(status=0,result='restored')
        finally:script.unload();session.detach()
        (destination/'client_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if not report.get('passed') or not report.get('restored'):raise SystemExit(1)


if __name__=='__main__':main()
