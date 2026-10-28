"""Run original 3.87 guide state/callbacks without sending or editing the live save."""
import json
import sys
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
    pid = next(p for p, name in processes(config).items() if name == config['package'])
    session = device.attach(pid)
    script = session.create_script(LUA_EVALUATOR)
    try:
        script.load()
        raw = script.exports_sync.evaluate((ROOT / 'analysis/tools/new_role_guide_client_harness.lua').read_text())
    finally:
        script.unload()
        session.detach()
    checks = []
    for line in raw.get('result', '').splitlines():
        name, _, result = line.partition(':')
        if result.startswith(('true:', 'false:')):
            passed, _, error = result.partition(':')
            checks.append(dict(name=name, passed=passed == 'true', error=error))
    report = dict(passed=raw.get('status') == 0 and len(checks) == 19 and all(c['passed'] for c in checks),
                  native_original_callbacks=True, live_save_modified=False, checks=checks, raw=raw)
    (ROOT / 'analysis/evidence/new_role_guide/client_validation.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not report['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
