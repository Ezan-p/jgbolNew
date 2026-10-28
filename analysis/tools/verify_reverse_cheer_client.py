"""Run isolated original entry/bit decoding checks; never send gameplay requests."""
import json
import sys
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis/tools')]
from android_emulator.config import load_config
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR


def main():
    import frida
    config=load_config(ROOT/'game.json')
    device=frida.get_device(config['serial'],timeout=10)
    session=device.attach(next(p for p,n in processes(config).items() if n==config['package']))
    script=session.create_script(LUA_EVALUATOR)
    try:
        script.load()
        deadline=time.monotonic()+40
        while True:
            state=script.exports_sync.evaluate('return tostring(package.loaded.ms~=nil)')
            if state.get('result')=='true': break
            if time.monotonic()>deadline: raise RuntimeError('Original game modules not loaded; enter game before rerunning')
            time.sleep(1)
        result=script.exports_sync.evaluate((ROOT/'analysis/tools/reverse_cheer_client_harness.lua').read_text())
        report=dict(date='2026-10-28',live_save_modified=False,raw=result)
        report['passed']=result.get('status')==0
        if report['passed']: report['validation']=json.loads(result['result'])
        out=ROOT/'analysis/evidence/reverse_cheer/client_validation.json'
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps(report,ensure_ascii=False))
        if not report['passed']: raise SystemExit(1)
    finally:
        script.unload(); session.detach()


if __name__=='__main__': main()
