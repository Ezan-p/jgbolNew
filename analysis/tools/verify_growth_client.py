"""Validate the patched native growth renderer in temporary Cocos nodes; no live requests."""
import json
import subprocess
import sys
import time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis/tools')]
from android_emulator.config import load_config
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR


def main():
    import frida
    config = load_config(ROOT / 'game.json')
    device = frida.get_device(config['serial'], timeout=10)
    session = device.attach(next(p for p, name in processes(config).items() if name == config['package']))
    script = session.create_script(LUA_EVALUATOR)
    out = ROOT / 'analysis/evidence/welfare'
    try:
        script.load()
        script.exports_sync.evaluate('local v=package.loaded.ms.d_actNoticeUI;if v._localGrowthRestore then v._localGrowthRestore() end')
        result = script.exports_sync.evaluate((ROOT / 'network_redirect/welfare_client.lua').read_text())
        assert result['status'] == 0, result
        result = script.exports_sync.evaluate((ROOT / 'tests/growth_client_native.lua').read_text())
        report = dict(passed=result['status'] == 0 and result.get('result') == 'passed:8',
                      native_cocos=True, live_save_modified=False, raw=result)
        (out / 'growth_client_validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
        print(json.dumps(report, ensure_ascii=False))
        if not report['passed']:
            raise SystemExit(1)
        time.sleep(0.5)
        (out / 'growth_permanent.png').write_bytes(subprocess.check_output(
            [str(config['adb_path']), '-s', config['serial'], 'exec-out', 'screencap', '-p']))
    finally:
        script.exports_sync.evaluate("CCDirector:sharedDirector():getRunningScene():removeChildByTag(19877,true)")
        script.unload()
        session.detach()


if __name__ == '__main__':
    main()
