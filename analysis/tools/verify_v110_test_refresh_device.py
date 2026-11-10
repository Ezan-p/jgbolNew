"""Validate old/new v110 on the disposable v111refreshqa ARM32 emulator only."""
import io
import json
from pathlib import Path
import subprocess
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v110_test_refresh import APK, PREVIOUS, WORK, EVIDENCE, digest, report

ADB = [str(ROOT / '.runtime/sdk/platform-tools/adb'), '-s', 'emulator-5590']
PACKAGE = 'com.sygame.jingubang.test106'
DEVICE = WORK / 'device'


def call(*args, timeout=30):
    return subprocess.check_output(ADB + list(args), timeout=timeout, stderr=subprocess.STDOUT)


def save_copy(label):
    path = DEVICE / label
    assert not path.exists()
    call('pull', f'/data/data/{PACKAGE}/files/test-save-v106', str(path), timeout=120)
    return {str(p.relative_to(path)): digest(p.read_bytes()) for p in path.rglob('*') if p.is_file()}


def start(label, apk):
    with zipfile.ZipFile(apk) as z:
        program_hash = digest(z.read('assets/offline/program.zip'))
    call('logcat', '-c')
    call('shell', 'am', 'start', '-n', PACKAGE + '/com.jgbol.offline.LauncherActivity', timeout=60)
    deadline = time.monotonic() + 480
    while time.monotonic() < deadline:
        log = call('logcat', '-d', '-s', 'JGBOffline:I', '*:S').decode(errors='replace')
        (EVIDENCE / f'device-{label}.log').write_text(log)
        assert not any(x in log for x in ('Offline startup failed', 'native_install_failed:', 'offline_lua_error:')), log[-4000:]
        if 'OFFLINE_READY ' + program_hash in log and 'offline_native_ready:' in log:
            print(label, 'runtime and native engine ready', flush=True)
            return
        print('Waiting for', label, 'runtime', flush=True)
        time.sleep(10)
    raise RuntimeError(label + ' startup timed out')


def main():
    DEVICE.mkdir(parents=True, exist_ok=True)
    data = dict(passed=False, apk_sha256=digest(APK.read_bytes()), candidate_installed=False,
                device='v111refreshqa / emulator-5590 / Android 6 ARM32', physical_device_tested=False)
    try:
        assert call('emu', 'avd', 'name').decode().splitlines()[0] == 'v111refreshqa'
        deadline = time.monotonic() + 420
        while call('shell', 'getprop', 'sys.boot_completed').strip() != b'1':
            if time.monotonic() >= deadline:
                raise RuntimeError('Dedicated QA emulator boot timed out')
            print('Waiting for dedicated QA boot', flush=True)
            time.sleep(10)
        installed = call('shell', 'pm', 'path', PACKAGE).decode().strip()
        if installed:
            path = DEVICE / 'existing.apk'
            call('pull', installed.removeprefix('package:'), str(path), timeout=180)
            assert digest(path.read_bytes()) == digest(PREVIOUS.read_bytes()), 'Unexpected existing test APK; do not replace'
        else:
            print('Installing original v110 test package', flush=True)
            assert b'Success' in call('install', '--no-streaming', str(PREVIOUS), timeout=900)
        start('old-v110', PREVIOUS)
        call('shell', 'am', 'force-stop', PACKAGE)
        before = save_copy('old-save')
        assert before
        print('Installing refreshed v110 test package', flush=True)
        assert b'Success' in call('install', '--no-streaming', '-r', str(APK), timeout=900)
        data['candidate_installed'] = True
        after = save_copy('after-install-save')
        assert before == after, 'Replacement changed saved files'
        start('new-v110', APK)
        (EVIDENCE / 'device-startup.png').write_bytes(call('exec-out', 'screencap', '-p', timeout=60))
        info = call('shell', 'dumpsys', 'package', PACKAGE).decode()
        assert 'versionCode=110 ' in info and 'versionName=3.87-test.110.1' in info
        path = call('shell', 'pm', 'path', PACKAGE).decode().strip().removeprefix('package:')
        call('pull', path, str(DEVICE / 'installed.apk'), timeout=180)
        assert digest((DEVICE / 'installed.apk').read_bytes()) == data['apk_sha256']
        data.update(passed=True, complete_save_preserved_after_install=True,
                    old_save_hashes=before, after_install_save_hashes=after,
                    installed_apk_hash_verified=True, new_program_ready=True, native_ready=True,
                    screenshot='device-startup.png', status='awaiting_screenshot_review')
    except Exception as exc:
        data.update(status='device_validation_incomplete', reason=str(exc))
    report('device-validation', data)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    raise SystemExit(not data['passed'])


if __name__ == '__main__':
    main()
