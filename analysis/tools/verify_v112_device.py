"""Upgrade only the explicitly identified disposable ARM32 QA emulator."""
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v112 import WORK, EVIDENCE, OUTPUT, BASE, BASE_SHA, PACKAGE, digest, report

ADB = [str(ROOT / '.runtime/sdk/platform-tools/adb'), '-s', 'emulator-5592']
DEVICE = WORK / 'device-validation'


def call(*args, timeout=30):
    return subprocess.check_output(ADB + list(args), timeout=timeout, stderr=subprocess.STDOUT)


def save_copy(label):
    destination = DEVICE / label
    assert not destination.exists()
    call('pull', f'/data/data/{PACKAGE}/files/save', str(destination), timeout=120)
    return {str(p.relative_to(destination)): digest(p.read_bytes())
            for p in destination.rglob('*') if p.is_file()}


def start(label, program_hash):
    call('logcat', '-c')
    call('shell', 'am', 'start', '-n', PACKAGE + '/com.jgbol.offline.LauncherActivity', timeout=60)
    deadline = time.monotonic() + 300
    while time.monotonic() < deadline:
        logs = call('logcat', '-d', '-s', 'JGBOffline:I', '*:S').decode(errors='replace')
        (EVIDENCE / f'device-{label}.log').write_text(logs)
        assert not any(s in logs for s in ('Offline startup failed', 'native_install_failed:', 'offline_lua_error:')), logs
        if 'OFFLINE_READY ' + program_hash in logs and 'offline_native_ready:' in logs:
            print(label, 'packaged runtime and native engine ready', flush=True)
            return
        print('Waiting for', label, 'runtime', flush=True)
        time.sleep(10)
    raise RuntimeError(label + ' startup timed out')


def main():
    DEVICE.mkdir(parents=True, exist_ok=True)
    sha = digest(OUTPUT.read_bytes())
    record = dict(apk_sha256=sha, passed=False, device='v110refreshqa / emulator-5592 / Android 6 ARM32',
                  candidate_installed=False, startup_ui_verified=False, physical_device_tested=False,
                  feature_touch_acceptance_completed=False)
    try:
        assert call('emu', 'avd', 'name').decode().splitlines()[0] == 'v110refreshqa'
        end = time.monotonic() + 900
        while call('shell', 'getprop', 'sys.boot_completed').strip() != b'1':
            assert time.monotonic() < end, 'QA Android did not boot'
            print('Waiting for dedicated QA Android boot', flush=True)
            time.sleep(10)
        installed = call('shell', 'pm', 'path', PACKAGE).decode().strip().removeprefix('package:')
        if installed:
            old = DEVICE / 'installed-old.apk'
            call('pull', installed, str(old), timeout=120)
            assert digest(old.read_bytes()) == BASE_SHA, 'Unexpected installed QA baseline'
        else:
            assert b'Success' in call('install', '--no-streaming', str(BASE), timeout=600)
        old_meta = json.loads((ROOT / 'analysis/evidence/v111-three-updates-20261110/build-validation.json').read_text())
        start('old-v111', old_meta['program_sha256'])
        call('shell', 'am', 'force-stop', PACKAGE)
        before = save_copy('old-save')
        assert before
        print('Installing formal v112 over v111', flush=True)
        assert b'Success' in call('install', '--no-streaming', '-r', str(OUTPUT), timeout=600)
        record['candidate_installed'] = True
        after = save_copy('after-install-save')
        assert before == after, 'Upgrade installation changed save bytes'
        record.update(v111_to_v112_upgrade_verified=True, complete_save_preserved_after_install=True,
                      old_save_hashes=before, after_install_save_hashes=after)
        info = call('shell', 'dumpsys', 'package', PACKAGE).decode()
        assert 'versionCode=112 ' in info and 'versionName=3.87-offline.12' in info
        installed = call('shell', 'pm', 'path', PACKAGE).decode().strip().removeprefix('package:')
        pulled = DEVICE / 'installed.apk'
        call('pull', installed, str(pulled), timeout=120)
        assert digest(pulled.read_bytes()) == sha
        record['installed_apk_hash_verified'] = True
        current = json.loads((EVIDENCE / 'build-validation.json').read_text())
        start('new-v112', current['program_sha256'])
        record.update(passed=True, new_program_ready=True, native_ready=True,
                      status='installation_and_runtime_passed_ui_unreviewed')
        time.sleep(20)
        (EVIDENCE / 'startup-home.png').write_bytes(call('exec-out', 'screencap', '-p', timeout=60))
        (EVIDENCE / 'device-window.log').write_bytes(call('shell', 'dumpsys', 'window', 'windows'))
        record['screenshot'] = 'startup-home.png'
        print('v111 -> v112 install, complete save bytes, installed APK hash and native startup passed', flush=True)
    except Exception as exc:
        record.update(status='device_validation_incomplete', error=str(exc))
        report('device-validation', record)
        raise
    report('device-validation', record)


if __name__ == '__main__':
    main()
