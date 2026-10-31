"""Validate the test edition repair without replacing/resetting either edition's save."""
import hashlib
import io
import json
from pathlib import Path
import sqlite3
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v106_test_stone_fix import BASE, APK, WORK, EVIDENCE
from analysis.tools.verify_v106_test_device import call, official_save, TEST


def capture(name):
    raw = call('exec-out', 'cat', f'/data/data/{TEST}/files/test-save-v106/game.sqlite3')
    assert raw.startswith(b'SQLite format 3')
    path = WORK / (name + '.sqlite3')
    path.write_bytes(raw)
    with sqlite3.connect(path.as_uri()+'?mode=ro', uri=True) as db:
        assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    return hashlib.sha256(raw).hexdigest()


def main():
    assert call('emu', 'avd', 'name').decode().splitlines()[0] == 'standalone32'
    build = json.loads((EVIDENCE/'build-validation.json').read_text())
    assert hashlib.sha256(APK.read_bytes()).hexdigest() == build['apk_sha256']
    call('shell', 'am', 'force-stop', TEST)
    official_before = official_save()
    before = capture('device-before')
    installed_path = call('shell', 'pm', 'path', TEST).decode().strip().removeprefix('package:')
    installed = WORK/'device-original.apk'
    call('pull', installed_path, str(installed), timeout=180)
    assert hashlib.sha256(installed.read_bytes()).hexdigest() == build['baseline_sha256']
    # Confirm identity-specific resources remain byte-identical in the two payloads.
    with zipfile.ZipFile(BASE) as old, zipfile.ZipFile(APK) as new:
        with zipfile.ZipFile(io.BytesIO(old.read('assets/offline/program.zip'))) as a, \
             zipfile.ZipFile(io.BytesIO(new.read('assets/offline/program.zip'))) as b:
            for name in ('offline_android/backend.py', 'offline_android/test_edition_seed.py', 'network_redirect/login.html'):
                assert a.read(name) == b.read(name)
    installed_result = call('install', '--no-streaming', '-r', str(APK), timeout=300)
    assert b'Success' in installed_result, installed_result
    assert capture('device-after-install') == before
    call('shell', 'am', 'start', '-n', TEST+'/com.jgbol.offline.LauncherActivity')
    for _ in range(120):
        logs = call('logcat', '-d', '-s', 'JGBOffline:I', '*:S').decode()
        if 'OFFLINE_READY '+build['program_sha256'] in logs:
            break
        time.sleep(2)
    else:
        raise RuntimeError('Test repair runtime did not become ready')
    assert capture('device-after-start') == before
    call('shell', 'am', 'force-stop', TEST)
    assert capture('device-after-stop') == before
    assert official_save() == official_before
    report = dict(apk_sha256=build['apk_sha256'], device='standalone32 / emulator-5572 / Android 6 ARMv7',
        test_save_sha256=before, official_save_sha256=official_before,
        same_version_replacement=True, test_save_unchanged_after_install_start_stop=True,
        official_save_unchanged=True, test_seed_and_backend_unchanged=True, runtime_ready=True)
    (EVIDENCE/'device-validation.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
