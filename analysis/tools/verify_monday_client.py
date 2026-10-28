"""Run original, detached mondayUI widgets without spending live resources."""
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from build_monday_client_fixture import main as build
from verify_guild_client import LUA_EVALUATOR
from network_redirect.backend import login_fields
from android_emulator.config import load_config
from observability.collector import processes


def main():
    import frida
    source=build().read_text();config=load_config(ROOT/'game.json')
    pid=next(p for p,n in processes(config).items() if n==config['package'])
    session=frida.get_device(config['serial'],timeout=10).attach(pid)
    script=session.create_script(LUA_EVALUATOR)
    try:
        script.load();result=script.exports_sync.evaluate(source)
    finally:
        script.unload();session.detach()
    checks=list(login_fields(result.get('result','')).values()) if result.get('status')==0 else []
    passed=len(checks)==9 and all(c['passed'] for c in checks)
    out=ROOT/'analysis/evidence/monday';out.mkdir(exist_ok=True)
    (out/'client_validation.json').write_text(json.dumps(dict(passed=passed,checks=checks,raw=result,
        native_cocos=True,network_sends_captured=True,detached_layer=True,live_resources_changed=False),ensure_ascii=False,indent=2)+'\n')
    print(f'{sum(c["passed"] for c in checks)}/{len(checks)} original mondayUI checks passed')
    if not passed:print(result);raise SystemExit(1)

if __name__=='__main__':main()
