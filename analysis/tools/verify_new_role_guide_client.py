"""Run original 3.87 guide state/callbacks without sending or editing the live save."""
import json
import sys
import tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis/tools')]
from android_emulator.config import load_config
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR
from network_redirect.backend import Backend
from network_redirect.protocol import encode, decode
from network_redirect import summon


def upgrade_fixture():
    with tempfile.TemporaryDirectory() as tmp:
        backend = Backend(Path(tmp), 18770, lambda *a, **k: None, account='guide-fixture')
        try:
            for stage in (1, 2, 3, 5, 6, 7, 8, 9, 10):
                role = backend.profile()
                name = ('验证行者' if stage == 1 else '1' if stage == 2 else
                        str(int(role['corteges'][1]['id'])) if stage == 6 else
                        str(int(next(i['id'] for i in role['attachments'] if i['type_id'] == 2041))) if stage == 9 else '')
                replies = backend.respond(encode(1204, dict(serial_num=stage, stage=stage,
                                          name=name, head_type=101)), {'authenticated': True})
            event = next(decode(p)[2] for p in replies if decode(p)[0] == 2998 and decode(p)[2]['id'] == 2)
            assert backend.profile()['level'] == 2
            return event
        finally:
            backend.close()


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
        upgrade = script.exports_sync.evaluate('local UPGRADE=' + summon.lua(upgrade_fixture()) + '\n' +
            (ROOT / 'analysis/tools/new_role_guide_upgrade_harness.lua').read_text())
    finally:
        script.unload()
        session.detach()
    checks = []
    for line in (raw.get('result', '') + '\n' + upgrade.get('result', '')).splitlines():
        name, _, result = line.partition(':')
        if result.startswith(('true:', 'false:')):
            passed, _, error = result.partition(':')
            checks.append(dict(name=name, passed=passed == 'true', error=error))
    report = dict(passed=raw.get('status') == 0 and upgrade.get('status') == 0 and len(checks) == 23 and all(c['passed'] for c in checks),
                  native_original_callbacks=True, live_save_modified=False, checks=checks, raw=raw, upgrade=upgrade)
    (ROOT / 'analysis/evidence/new_role_guide/client_validation.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not report['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
