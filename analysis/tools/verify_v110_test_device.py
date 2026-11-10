"""Install v108 then v110 only on this build's disposable test110qa AVD."""
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / '.runtime/v110-test/device'
EVIDENCE = ROOT / 'analysis/evidence/v110_test'
ADB = [str(ROOT / '.runtime/sdk/platform-tools/adb'), '-s', 'emulator-5574']
PACKAGE = 'com.sygame.jingubang.test106'
APK = ROOT / '.runtime/v110-test/金箍棒ol测试版-v110.apk'


def call(*args, timeout=60):
    return subprocess.check_output(ADB + list(args), timeout=timeout)


def capture(name):
    raw = call('exec-out', 'cat', f'/data/data/{PACKAGE}/files/test-save-v106/game.sqlite3')
    assert raw.startswith(b'SQLite format 3')
    path = WORK / (name + '.sqlite3')
    path.write_bytes(raw)
    with sqlite3.connect(path.as_uri() + '?mode=ro', uri=True) as db:
        assert db.execute('pragma integrity_check').fetchone()[0] == 'ok'
        roles = {a: json.loads(data) for a, data in db.execute('select account,data from roles')}
    return hashlib.sha256(raw).hexdigest(), roles


def start(program_hash, stage):
    call('logcat', '-c')
    call('shell', 'am', 'start', '-n', PACKAGE + '/com.jgbol.offline.LauncherActivity')
    deadline = time.monotonic() + 600
    while time.monotonic() < deadline:
        logs = call('logcat', '-d', '-s', 'JGBOffline:I', '*:S').decode()
        (EVIDENCE / (stage + '-startup.log')).write_text(logs)
        assert not any(s in logs for s in ('offline_lua_error:', 'native_install_failed:', 'Offline startup failed')), logs
        if 'OFFLINE_READY ' + program_hash in logs and 'offline_native_ready:' in logs:
            print(stage + ' runtime ready', flush=True)
            return
        time.sleep(3)
    raise RuntimeError('Startup timeout: ' + logs[-3000:])


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    assert call('emu', 'avd', 'name').decode().splitlines()[0] == 'test110qa'
    deadline = time.monotonic() + 600
    while call('shell', 'getprop', 'sys.boot_completed').strip() != b'1':
        assert time.monotonic() < deadline, 'QA boot timeout'
        time.sleep(3)
    print('Dedicated fresh ARM32 QA booted', flush=True)
    old = ROOT / 'build/金箍棒ol测试版-v108.apk'
    old_meta = json.loads(old.with_suffix('.manifest.json').read_text())
    info = call('shell', 'dumpsys', 'package', PACKAGE).decode()
    if 'versionCode=110 ' not in info:
        if 'versionCode=108 ' not in info:
            assert b'Success' in call('install', '--no-streaming', '-r', str(old), timeout=600)
        start(old_meta['program_sha256'], 'v108')
        call('shell', 'am', 'force-stop', PACKAGE)
        before_hash, before_roles = capture('before')
        (WORK / 'before.json').write_text(json.dumps(dict(sha256=before_hash, roles=before_roles)))
        assert b'Success' in call('install', '--no-streaming', '-r', str(APK), timeout=600)
        assert capture('after-install')[0] == before_hash
        print('v108 to v110 install preserved database bytes', flush=True)
    else:
        prior = json.loads((WORK / 'before.json').read_text())
        before_hash, before_roles = prior['sha256'], prior['roles']
    meta = json.loads((EVIDENCE / 'build-validation.json').read_text())
    start(meta['program_sha256'], 'v110')
    time.sleep(10)
    (EVIDENCE / 'startup-home.png').write_bytes(call('exec-out', 'screencap', '-p'))
    call('shell', 'am', 'force-stop', PACKAGE)
    after_hash, after_roles = capture('after-launch')
    before, after = before_roles['v106_fixed_test'], after_roles['v106_fixed_test']
    for key in ('role_name', 'gold_coin', 'silver_coin', 'test_supply_revision', 'test_v108_silver_reserve'):
        assert before[key] == after[key], key
    for old_companion in before['corteges']:
        new = next(c for c in after['corteges'] if c['id'] == old_companion['id'])
        for key in ('type', 'level', 'evolve_level', 'reborn_layer', 'order'):
            assert old_companion.get(key, 0) == new.get(key, 0), key
    for item in before['attachments']:
        new = next(i for i in after['attachments'] if i['id'] == item['id'])
        for key in ('type_id', 'level', 'advance_level', 'cast_level', 'owner_id', 'equip_order'):
            assert item.get(key, 0) == new.get(key, 0), key
        if item['attach_type'] != 6:
            assert item['count'] == new['count']
    start(meta['program_sha256'], 'v110-restart')
    call('shell', 'am', 'force-stop', PACKAGE)
    assert capture('after-restart')[1] == after_roles
    assert 'versionCode=110 ' in call('shell', 'dumpsys', 'package', PACKAGE).decode()
    report = dict(passed=True, apk_sha256=meta['apk_sha256'], device='test110qa / Android 6 ARMv7',
        replacement_install=True, previous_version=108, new_version=110,
        install_save_byte_identical=True, existing_progress_preserved=True,
        supply_not_repeated=True, restart_role_values_identical=True,
        runtime_ready=True, no_startup_lua_errors=True, physical_device_test=False,
        before_sha256=before_hash, after_sha256=after_hash, screenshot='startup-home.png')
    (EVIDENCE / 'device-validation.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
