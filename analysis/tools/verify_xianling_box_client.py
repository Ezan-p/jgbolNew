"""Capture original box UI requests and settle them in a disposable database."""
import json
import contextlib
from pathlib import Path
import sys
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis/tools')]
from android_emulator.config import load_config
from observability.collector import processes
from network_redirect import summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode
from verify_guild_client import LUA_EVALUATOR


def main():
    import frida
    config = load_config(ROOT / 'game.json')
    pid = next(p for p, name in processes(config).items() if name == config['package'])
    session = frida.get_device(config['serial'], timeout=10).attach(pid)
    script = session.create_script(LUA_EVALUATOR)
    answers = []
    done = threading.Event()
    try:
        script.load()
        def evaluate():
            try:
                answers.append(script.exports_sync.evaluate((ROOT / 'tests/xianling_box_client_regression.lua').read_text()))
            except Exception as exc:
                answers.append({'error': str(exc)})
            finally:
                done.set()
        worker = threading.Thread(target=evaluate, daemon=True)
        worker.start()
        if not done.wait(30):
            raise RuntimeError('Native Lua evaluation timed out')
        assert answers and answers[0].get('status') == 0, answers
        report = login_fields(answers[0]['result'])
        assert report['passed'] and report['checks'] == 10 and report['restored'], report
    finally:
        with contextlib.suppress(Exception):
            script.unload()
        with contextlib.suppress(Exception):
            session.detach()
    with tempfile.TemporaryDirectory() as tmp:
        backend = Backend(Path(tmp), 18790, lambda *a, **k: None)
        try:
            for serial, row in sorted(report['requests'].items()):
                req = row['data']
                role = backend.profile()
                role['attachments'].append(dict(id=9001249, attach_type=5, type_id=1249,
                                                 level=1, count=req['item_count']))
                backend.save(role)
                packets = backend.respond(encode(row['mid'], dict(req, serial_num=serial)), {'authenticated': True})
                events = [(d['id'], login_fields(d['data'])) for m, _, d in map(decode, packets) if m == 2998]
                assert not any(kind == 55 for kind, _ in events), events
                prize = next(data for kind, data in events if kind == 21)
                assert prize['count'] == req['item_count']
                assert prize['attach_list'][1]['attach_type'] == req['des_id']
                assert prize['attach_list'][1]['attach_count'] == req['item_count']
                assert not any(i['type_id'] == 1249 for i in backend.profile()['attachments'])
            report['backend_cases'] = len(report['requests'])
        finally:
            backend.close()
    report['live_save_modified'] = False
    (ROOT / '.runtime/xianling-box-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(f"{report['checks']} native UI checks and {report['backend_cases']} captured-request settlements passed; live save unchanged")


if __name__ == '__main__':
    main()
