"""Install old/new v111 only on the disposable v111refreshqa ARM32 AVD."""
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v111_refresh import WORK, EVIDENCE, OUTPUT, BASE, digest, report

ADB = [str(ROOT / '.runtime/sdk/platform-tools/adb'), '-s', 'emulator-5590']
PACKAGE = 'com.sygame.jingubang.p360'
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
    deadline = time.monotonic() + 600
    while time.monotonic() < deadline:
        logs = call('logcat', '-d', '-s', 'JGBOffline:I', '*:S').decode(errors='replace')
        (EVIDENCE / f'device-{label}.log').write_text(logs)
        assert not any(s in logs for s in ('Offline startup failed', 'native_install_failed:', 'offline_lua_error:')), logs
        if 'OFFLINE_READY ' + program_hash in logs and 'offline_native_ready:' in logs:
            print(label, 'packaged runtime and native engine ready', flush=True)
            return
        print('Waiting for', label, 'runtime', flush=True)
        time.sleep(10)
    raise RuntimeError(label + ' startup timed out; inspect device log')


def main():
    DEVICE.mkdir(parents=True, exist_ok=True)
    checksum = digest(OUTPUT.read_bytes())
    assert call('emu', 'avd', 'name').decode().splitlines()[0] == 'v111refreshqa'
    deadline = time.monotonic() + 900
    while call('shell', 'getprop', 'sys.boot_completed').strip() != b'1':
        if time.monotonic() >= deadline:
            logs = call('logcat', '-d', '-t', '1500', timeout=60)
            (EVIDENCE / 'device-environment-failure.log').write_bytes(logs)
            report('device-validation', dict(apk_sha256=checksum, passed=False,
                status='environment_unavailable', candidate_installed=False,
                summary='新建独立ARM32 QA模拟器未完成Android首次启动，本次未完成设备安装与冷启动验收；包内验证另行记录。'))
            return
        print('Waiting for disposable Android first boot', flush=True)
        time.sleep(15)
    installed_path = call('shell', 'pm', 'path', PACKAGE).decode().strip()
    if installed_path:
        # The first install can finish dex compilation after the host timeout.
        # Resume only when the disposable device contains the exact old APK.
        old_apk = DEVICE / 'installed-old.apk'
        call('pull', installed_path.removeprefix('package:'), str(old_apk), timeout=180)
        assert digest(old_apk.read_bytes()) == digest(BASE.read_bytes())
        print('Resuming after verified old v111 installation', flush=True)
    else:
        print('Installing preserved old v111 in disposable QA', flush=True)
        assert b'Success' in call('install', '--no-streaming', str(BASE), timeout=900)
    old = json.loads((ROOT / 'analysis/evidence/v111/build-validation.json').read_text())
    start('old-v111', old['program_sha256'])
    call('shell', 'am', 'force-stop', PACKAGE)
    before = save_copy('old-save')
    assert before
    print('Replacement installing refreshed v111', flush=True)
    assert b'Success' in call('install', '--no-streaming', '-r', str(OUTPUT), timeout=900)
    after = save_copy('after-install-save')
    assert before == after, 'Replacement installation changed save bytes'
    current = json.loads((EVIDENCE / 'build-validation.json').read_text())
    start('new-v111', current['program_sha256'])
    time.sleep(15)
    screenshot = call('exec-out', 'screencap', '-p', timeout=60)
    (EVIDENCE / 'startup-home.png').write_bytes(screenshot)
    info = call('shell', 'dumpsys', 'package', PACKAGE).decode()
    assert 'versionCode=111 ' in info and 'versionName=3.87-offline.11' in info
    installed = call('shell', 'pm', 'path', PACKAGE).decode().strip().removeprefix('package:')
    pulled = DEVICE / 'installed.apk'
    call('pull', installed, str(pulled), timeout=180)
    assert digest(pulled.read_bytes()) == checksum
    report('device-validation', dict(apk_sha256=checksum, passed=True,
        status='awaiting_screenshot_review', device='v111refreshqa / emulator-5590 / Android 6 ARM32',
        same_version_replacement_verified=True, complete_save_preserved_after_install=True,
        old_save_hashes=before, after_install_save_hashes=after,
        installed_apk_hash_verified=True, new_program_ready=True, native_ready=True,
        screenshot='startup-home.png', physical_device_tested=False,
        summary='独立ARM32 QA模拟器旧v111到新v111同版本覆盖安装通过，安装前后完整save字节一致，新载荷和原生引擎冷启动就绪。'))


if __name__ == '__main__':
    main()
