"""Replay disposable achievement snapshots in native Cocos; restore UI state."""
import json
from pathlib import Path
import runpy
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis/tools')]
from verify_guild_client import LUA_EVALUATOR

def main():
    import frida
    from android_emulator.config import load_config
    from observability.collector import processes
    runpy.run_path(str(ROOT/'analysis/tools/build_achievement_client_fixture.py'))
    config=load_config(ROOT/'game.json')
    pid=next(p for p,n in processes(config).items() if n==config['package'])
    session=frida.get_device(config['serial'],timeout=5).attach(pid)
    script=session.create_script(LUA_EVALUATOR)
    try:
        script.load()
        result=script.exports_sync.evaluate((ROOT/'.runtime/achievement-fixture.lua').read_text())
        assert result.get('status')==0,result
        text=result['result']
        assert 'restored=true' in text and 'error=nil' in text and '=false' not in text,text
        report=dict(passed=True,native_cocos=True,live_save_modified=False,result=text)
        (ROOT/'analysis/evidence/achievement_hotupdate/native_client.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps(report,ensure_ascii=False,indent=2))
    finally:
        script.unload();session.detach()

if __name__=='__main__':main()
