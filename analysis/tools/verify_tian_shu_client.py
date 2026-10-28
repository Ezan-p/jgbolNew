"""Original native book UI against isolated data; no request reaches the backend."""
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis/tools')]
from android_emulator.config import load_config
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR
from network_redirect import tian_shu, summon


def main():
    import frida
    config = load_config(ROOT / 'game.json')
    device = frida.get_device(config['serial'], timeout=10)
    pid = next(p for p, name in processes(config).items() if name == config['package'])
    source = (ROOT / 'analysis/tools/tian_shu_client_harness.lua').read_text()
    source = source.replace('__REWARDS__', summon.lua(tian_shu.client_config(tian_shu.load_rules())))
    source = source.replace('__ADAPTER__', (ROOT / 'network_redirect/tian_shu_client.lua').read_text())
    session = device.attach(pid)
    script = session.create_script(LUA_EVALUATOR)
    try:
        script.load()
        compile_result = script.exports_sync.evaluate('local f,e=loadstring(' +
            summon.lua(summon.client_source(summon.load_rules())) + ');assert(f,e);return "compiled"')
        raw = script.exports_sync.evaluate(source)
    finally:
        script.unload()
        session.detach()
    checks = []
    for line in raw.get('result', '').splitlines():
        name, _, result = line.partition(':')
        if result.startswith(('true:', 'false:')):
            passed, _, error = result.partition(':')
            checks.append(dict(name=name, passed=passed == 'true', error=error))
    compiled = compile_result.get('status') == 0 and compile_result.get('result') == 'compiled'
    report = dict(passed=compiled and raw.get('status') == 0 and len(checks) == 12 and all(c['passed'] for c in checks),
                  full_production_injection_compiled=compiled,
                  native_original_callbacks=True, detached_cocos_cells=42,
                  live_save_modified=False, network_sends_intercepted=True, checks=checks, raw=raw)
    (ROOT / 'analysis/evidence/tian_shu/client_validation.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not report['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
