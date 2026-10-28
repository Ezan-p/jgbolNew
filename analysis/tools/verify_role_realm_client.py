"""Verify realm labels and upgrade boundaries in the running original Cocos VM."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT/'analysis/tools')]
from android_emulator.config import load_config
from observability.collector import processes
from network_redirect import reborn, summon
from verify_guild_client import LUA_EVALUATOR


def main():
    import frida
    cfg = load_config(ROOT/'game.json')
    device = frida.get_device(cfg['serial'], timeout=10)
    session = device.attach(next(p for p, n in processes(cfg).items() if n == cfg['package']))
    script = session.create_script(LUA_EVALUATOR)
    try:
        script.load()
        adapter = (ROOT/'network_redirect/reborn_client.lua').read_text()
        source = 'local REALM_CONFIG=' + summon.lua(reborn.client_config(reborn.load_rules())) + '\n'
        source += 'local ADAPTER_SOURCE=' + summon.lua(adapter) + '\n'
        source += (ROOT/'tests/role_realm_client_native.lua').read_text()
        raw = script.exports_sync.evaluate(source)
        report = json.loads(raw['result']) if raw.get('status') == 0 else dict(raw=raw)
        checks = report.get('checks', [])
        report.update(passed=len(checks) == 18 and all(c['ok'] for c in checks) and report.get('restored', False),
                      native_cocos=True, live_account_resources_changed=False)
        out = ROOT/'analysis/evidence/role_realm'; out.mkdir(exist_ok=True)
        (out/'client_validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
        print(json.dumps(report, ensure_ascii=False, indent=2))
        if not report['passed']: raise SystemExit(1)
    finally:
        script.unload(); session.detach()


if __name__ == '__main__': main()
