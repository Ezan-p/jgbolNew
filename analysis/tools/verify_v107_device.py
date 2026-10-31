"""Verify replacement installation only on the existing standalone32 QA AVD."""
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / '.runtime/v107-build/device'
EVIDENCE = ROOT / 'analysis/evidence/v107'
ADB = [str(ROOT / '.runtime/sdk/platform-tools/adb'), '-s', 'emulator-5572']
PACKAGE = 'com.sygame.jingubang.p360'
BASE = ROOT / 'build/金箍棒3.87离线正式版v106.apk'
APK = ROOT / '.runtime/v107-build/金箍棒3.87离线正式版v107.apk'


def call(*args, timeout=60):
    return subprocess.check_output(ADB + list(args), timeout=timeout)


def capture(name):
    path = WORK / (name + '.sqlite3')
    path.write_bytes(call('exec-out', 'cat', '/data/data/' + PACKAGE + '/files/save/game.sqlite3'))
    with sqlite3.connect(path.as_uri() + '?mode=ro', uri=True) as db:
        assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
        counts = {t: db.execute('SELECT count(*) FROM ' + t).fetchone()[0] for t in ('accounts', 'roles')}
        assert counts['accounts'] > 0 and counts['roles'] > 0
    return dict(sha256=hashlib.sha256(path.read_bytes()).hexdigest(), counts=counts, integrity='ok')


def install(apk):
    result = call('install', '--no-streaming', '-r', str(apk), timeout=300).decode()
    assert 'Success' in result, result
    print('Replace installation successful:', apk.name, flush=True)


def main(expected_version=106, install_baseline=True):
    WORK.mkdir(parents=True, exist_ok=True)
    assert call('emu', 'avd', 'name').decode().splitlines()[0] == 'standalone32'
    for _ in range(180):
        if call('shell', 'getprop', 'sys.boot_completed').strip() == b'1':
            break
        time.sleep(2)
    else:
        raise RuntimeError('QA emulator did not boot')
    info = call('shell', 'dumpsys', 'package', PACKAGE).decode()
    assert f'versionCode={expected_version} ' in info, 'Unexpected QA installation version'
    call('shell', 'am', 'force-stop', PACKAGE)
    original = capture('original')
    installed = call('shell', 'pm', 'path', PACKAGE).decode().strip().removeprefix('package:')
    installed_copy = WORK / 'original.apk'
    call('pull', installed, str(installed_copy), timeout=180)
    print('Backed up existing QA database; counts:', original['counts'], flush=True)
    if install_baseline:
        install(BASE)
    else:
        assert hashlib.sha256(installed_copy.read_bytes()).digest() == hashlib.sha256(BASE.read_bytes()).digest(), \
            'Installed QA baseline differs from preserved release'
    baseline = capture('baseline')
    assert original == baseline
    install(APK)
    after_install = capture('after-install-v107')
    assert baseline == after_install, 'Replacement installation changed the QA database'
    info = call('shell', 'dumpsys', 'package', PACKAGE).decode()
    assert 'versionCode=107 ' in info and 'versionName=3.87-offline.7' in info
    call('logcat', '-c')
    call('shell', 'am', 'start', '-n', PACKAGE + '/com.jgbol.offline.LauncherActivity')
    manifest = json.loads(APK.with_suffix('.manifest.json').read_text())
    ready = 'OFFLINE_READY ' + manifest['program_sha256']
    for attempt in range(180):
        logs = call('logcat', '-d', '-s', 'JGBOffline:I', '*:S').decode()
        if ready in logs:
            break
        if attempt % 15 == 0:
            print('Waiting for v107 bundled runtime:', attempt * 2, 'seconds', flush=True)
        time.sleep(2)
    else:
        (EVIDENCE / 'device-startup.log').write_text(logs)
        raise RuntimeError('v107 program did not become ready')
    (EVIDENCE / 'device-startup.log').write_text(logs)
    started = capture('after-start-v107')
    assert started == baseline, 'Startup changed the QA database'
    # Stop the isolated QA game before the final durable database read.
    call('shell', 'am', 'force-stop', PACKAGE)
    stopped = capture('after-stop-v107')
    assert stopped == baseline
    report = dict(date='2026-10-31', device='standalone32 / emulator-5572 / Android 6 ARMv7',
        apk_sha256=manifest['apk_sha256'], baseline_apk_sha256=manifest['baseline_sha256'],
        package=PACKAGE, version_code=107, version_name=manifest['version_name'],
        certificate_sha256=manifest['certificate_sha256'], replacement_install=True,
        same_version_update=expected_version == 107,
        save_byte_identical_after_install_start_and_stop=True,
        original=original, baseline=baseline, after_install=after_install,
        after_start=started, after_stop=stopped, new_program_ready=True,
        program_sha256=manifest['program_sha256'], player_devices_modified=False,
        physical_device_test=False)
    (EVIDENCE / 'device-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    main()
