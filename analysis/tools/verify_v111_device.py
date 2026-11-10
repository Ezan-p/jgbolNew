"""Upgrade the dedicated standalone32 QA AVD, preserving and comparing its save."""
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v111 import BASE, BASE_SHA, OUTPUT, WORK, EVIDENCE, digest, report
from analysis.tools.verify_v105_update import database_snapshot
from build_offline import signer_certificate

ADB = [str(ROOT / '.runtime/sdk/platform-tools/adb'), '-s', 'emulator-5572']
PACKAGE = 'com.sygame.jingubang.p360'
DEVICE = WORK / 'device'


def call(*args, timeout=60):
    return subprocess.check_output(ADB + list(args), timeout=timeout)


def pull_save(label):
    target = DEVICE / label
    assert not target.exists()
    call('pull', '/data/data/' + PACKAGE + '/files/save', str(target), timeout=180)
    return target, {str(p.relative_to(target)): digest(p.read_bytes()) for p in target.rglob('*') if p.is_file()}


def main():
    DEVICE.mkdir(parents=True, exist_ok=True)
    assert call('emu', 'avd', 'name').decode().splitlines()[0] == 'standalone32'
    deadline = time.monotonic() + 900
    while call('shell', 'getprop', 'sys.boot_completed').strip() != b'1':
        assert time.monotonic() < deadline, 'QA emulator did not finish booting'
        print('Waiting for dedicated ARM32 QA boot', flush=True)
        time.sleep(10)
    info = call('shell', 'dumpsys', 'package', PACKAGE).decode()
    assert 'versionCode=110 ' in info, info
    call('shell', 'am', 'force-stop', PACKAGE)
    before, hashes = pull_save('original-save')
    installed = call('shell', 'pm', 'path', PACKAGE).decode().strip().removeprefix('package:')
    previous = DEVICE / 'original.apk'
    call('pull', installed, str(previous), timeout=180)
    assert digest(previous.read_bytes()) == BASE_SHA, 'Unexpected installed baseline; preserved for review'
    assert signer_certificate(previous) == signer_certificate(OUTPUT)
    print('Backed up complete QA save and verified official v110 baseline', flush=True)
    install = call('install', '--no-streaming', '-r', str(OUTPUT), timeout=300).decode()
    assert 'Success' in install, install
    after, after_hashes = pull_save('after-install-save')
    assert hashes == after_hashes, 'Replacement installation changed save bytes'
    info = call('shell', 'dumpsys', 'package', PACKAGE).decode()
    assert 'versionCode=111 ' in info and 'versionName=3.87-offline.11' in info
    print('v111 replacement installed; complete save is byte-identical', flush=True)
    build = json.loads((EVIDENCE / 'build-validation.json').read_text())
    call('logcat', '-c')
    call('shell', 'am', 'start', '-n', PACKAGE + '/com.jgbol.offline.LauncherActivity')
    deadline = time.monotonic() + 600
    while True:
        logs = call('logcat', '-d', '-s', 'JGBOffline:I', '*:S').decode()
        (EVIDENCE / 'device-startup.log').write_text(logs)
        assert not any(s in logs for s in ('Offline startup failed', 'native_install_failed:', 'offline_lua_error:')), logs
        if 'OFFLINE_READY ' + build['program_sha256'] in logs and 'offline_native_ready:' in logs:
            break
        assert time.monotonic() < deadline, 'QA native startup timed out'
        print('Waiting for packaged runtime and native client', flush=True)
        time.sleep(10)
    time.sleep(20)
    (EVIDENCE / 'startup-home.png').write_bytes(call('exec-out', 'screencap', '-p'))
    logs = call('logcat', '-d', '-s', 'JGBOffline:I', '*:S').decode()
    (EVIDENCE / 'device-startup.log').write_text(logs)
    assert not any(s in logs for s in ('Offline startup failed', 'native_install_failed:', 'offline_lua_error:')), logs
    call('shell', 'am', 'force-stop', PACKAGE)
    stopped, final_hashes = pull_save('after-start-stop-save')
    assert database_snapshot(before / 'game.sqlite3') == database_snapshot(stopped / 'game.sqlite3')
    report('device-validation', dict(apk_sha256=build['apk_sha256'], passed=True,
        device='standalone32 / emulator-5572 / Android 6 ARMv7', baseline_sha256=BASE_SHA,
        upgrade_from=110, upgrade_to=111, complete_save_byte_identical_after_install=True,
        all_game_tables_preserved_after_start=True, new_program_ready=True, native_ready=True,
        no_lua_error=True, physical_device_tested=False, screenshot='startup-home.png',
        awaiting_screenshot_review=True, backup=str(before.relative_to(ROOT)),
        original_save_hashes=hashes, after_start_save_hashes=final_hashes))
    print('QA v110 -> v111 passed. Review startup-home.png before release.', flush=True)


if __name__ == '__main__':
    main()
