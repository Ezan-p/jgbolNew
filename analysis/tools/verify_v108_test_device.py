"""Upgrade only the standalone32 test app; verify both database identities."""
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / '.runtime/v108-test/device'
EVIDENCE = ROOT / 'analysis/evidence/v108_test'
ADB = [str(ROOT / '.runtime/sdk/platform-tools/adb'), '-s', 'emulator-5572']
OFFICIAL = 'com.sygame.jingubang.p360'
TEST = 'com.sygame.jingubang.test106'


def call(*args, timeout=60):
    return subprocess.check_output(ADB + list(args), timeout=timeout)


def capture(package, directory, name):
    raw = call('exec-out', 'cat', f'/data/data/{package}/files/{directory}/game.sqlite3')
    assert raw.startswith(b'SQLite format 3')
    p = WORK / (name + '.sqlite3')
    p.write_bytes(raw)
    with sqlite3.connect(p.as_uri() + '?mode=ro', uri=True) as db:
        assert db.execute('pragma integrity_check').fetchone()[0] == 'ok'
        rows = {account: json.loads(data) for account, data in db.execute('select account,data from roles')}
    return hashlib.sha256(raw).hexdigest(), rows


def start(meta):
    call('logcat', '-c')
    call('shell', 'am', 'start', '-n', TEST + '/com.jgbol.offline.LauncherActivity')
    deadline = time.monotonic() + 240
    while time.monotonic() < deadline:
        logs = call('logcat', '-d', '-s', 'JGBOffline:I', '*:S').decode()
        assert 'offline_lua_error:' not in logs and 'native_install_failed:' not in logs
        if 'OFFLINE_READY ' + meta['program_sha256'] in logs and 'offline_native_ready:' in logs:
            (EVIDENCE / 'device-startup.log').write_text(logs)
            return
        time.sleep(2)
    raise RuntimeError(logs)


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    assert call('emu', 'avd', 'name').decode().splitlines()[0] == 'standalone32'
    before_info = call('shell', 'dumpsys', 'package', TEST).decode()
    previous_version = 106 if 'versionCode=106 ' in before_info else 108
    assert f'versionCode={previous_version} ' in before_info
    for package in (OFFICIAL, TEST):
        call('shell', 'am', 'force-stop', package)
    if '--restore-qa-baseline' in sys.argv:
        source = ROOT / '.runtime/v108-test/device-first-candidate/test-before.sqlite3'
        assert source.is_file()
        # Only the guarded QA app's own backed-up database is restored.
        call('push', str(source), f'/data/data/{TEST}/files/test-save-v106/game.sqlite3')
        uid = before_info.split('userId=')[1].split()[0]
        call('shell', 'chown', uid + ':' + uid, f'/data/data/{TEST}/files/test-save-v106/game.sqlite3')
    official_before = capture(OFFICIAL, 'save', 'official-before')
    old_hash, old_roles = capture(TEST, 'test-save-v106', 'test-before')
    old = old_roles['v106_fixed_test']
    apk_path = call('shell', 'pm', 'path', TEST).decode().strip().removeprefix('package:')
    call('pull', apk_path, str(WORK / 'test-before.apk'), timeout=180)
    meta = json.loads((EVIDENCE / 'build-validation.json').read_text())
    result = call('install', '--no-streaming', '-r', str(ROOT / 'build' / meta['apk']), timeout=300)
    assert b'Success' in result, result
    assert capture(TEST, 'test-save-v106', 'test-after-install')[0] == old_hash
    assert capture(OFFICIAL, 'save', 'official-after-install')[0] == official_before[0]
    print('Final v108 replacement installed with original v106 save; installation preserved both databases', flush=True)
    start(meta)
    time.sleep(18)
    (EVIDENCE / 'startup-home.png').write_bytes(call('exec-out', 'screencap', '-p'))
    call('shell', 'am', 'force-stop', TEST)
    new_hash, new_roles = capture(TEST, 'test-save-v106', 'test-after-launch')
    new = new_roles['v106_fixed_test']
    assert new['gold_coin'] == old['gold_coin'] + 100000
    assert new['test_supply_revision'] == 108
    assert new['role_name'] == old['role_name']
    for c in old['corteges']:
        after = next(x for x in new['corteges'] if x['id'] == c['id'])
        assert all(after.get(k, 0) == c.get(k, 0) for k in ('type','level','evolve_level','reborn_layer','order'))
    for i in old['attachments']:
        after = next(x for x in new['attachments'] if x['id'] == i['id'])
        assert all(after.get(k, 0) == i.get(k, 0) for k in ('type_id','level','advance_level','cast_level','owner_id','equip_order'))
        assert after['count'] >= i['count']
    start(meta)
    call('shell', 'am', 'force-stop', TEST)
    restarted_hash, restarted = capture(TEST, 'test-save-v106', 'test-after-restart')
    assert restarted_hash == new_hash and restarted == new_roles
    assert capture(OFFICIAL, 'save', 'official-after-all')[0] == official_before[0]
    official_info = call('shell', 'dumpsys', 'package', OFFICIAL).decode()
    test_info = call('shell', 'dumpsys', 'package', TEST).decode()
    uid = lambda info: info.split('userId=')[1].split()[0]
    assert uid(official_info) != uid(test_info)
    assert 'versionCode=108 ' in test_info
    report = dict(apk_sha256=meta['apk_sha256'], device='standalone32 / Android 6 ARMv7',
        replacement_install=True, previous_version=previous_version, new_version=108, original_v106_save_used=True,
        official_save_sha256=official_before[0], official_save_unchanged=True,
        previous_test_save_sha256=old_hash, migrated_test_save_sha256=new_hash,
        existing_progress_preserved=True, additive_gold=100000, restart_save_byte_identical=True,
        independent_uids=True, runtime_ready=True, no_startup_lua_errors=True,
        screenshot='startup-home.png')
    (EVIDENCE / 'device-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
