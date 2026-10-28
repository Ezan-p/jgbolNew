"""Native Cocos smoke check with disposable response fixtures and intercepted sends."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis/tools')]
from android_emulator.config import load_config
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR
from build_abyss_client_fixture import main as build


def main():
    import frida
    build();cfg=load_config(ROOT/'game.json');report=dict(native_cocos=True,live_save_modified=False)
    session=script=None
    try:
        pid=next(p for p,n in processes(cfg).items() if n==cfg['package'])
        session=frida.get_device(cfg['serial'],timeout=10).attach(pid)
        source=LUA_EVALUATOR.replace('pending={code,resolve};',
            "const task={code,resolve};pending=task;setTimeout(()=>{if(pending===task){pending=null;resolve({status:-1,result:'No Lua frame'});}},15000);")
        script=session.create_script(source);script.load()
        def evaluate(code):
            result=script.exports_sync.evaluate(code)
            if result.get('status')!=0:raise RuntimeError(result)
            return result['result']
        evaluate("local ms=assert(package.loaded.ms);assert(ms.d_mainUI.g_playerInfo.role_id);return 'ready'")
        report['fixture']=json.loads(evaluate((ROOT/'.runtime/abyss-native-fixture.lua').read_text()))
        report['passed']=report['fixture']['passed']==report['fixture']['total']
    except Exception as exc:
        report.update(passed=False,error=str(exc))
    finally:
        if script:script.unload()
        if session:session.detach()
        (ROOT/'analysis/evidence/abyss/native_repaired_20261028.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if not report['passed']:raise SystemExit(1)


if __name__=='__main__':main()
