"""Install only the test package on guarded standalone32; hash official save."""
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / '.runtime/v106-test/device'
EVIDENCE = ROOT / 'analysis/evidence/v106_test'
ADB = [str(ROOT / '.runtime/sdk/platform-tools/adb'), '-s', 'emulator-5572']
OFFICIAL = 'com.sygame.jingubang.p360'
TEST = 'com.sygame.jingubang.test106'


def call(*args, timeout=30):
    return subprocess.check_output(ADB + list(args), timeout=timeout)


def official_save():
    raw = call('exec-out', 'cat', f'/data/data/{OFFICIAL}/files/save/game.sqlite3')
    assert raw.startswith(b'SQLite format 3')
    return hashlib.sha256(raw).hexdigest()


def test_save(name):
    raw = call('exec-out', 'cat', f'/data/data/{TEST}/files/test-save-v106/game.sqlite3')
    assert raw.startswith(b'SQLite format 3'), raw[:100]
    path = WORK / (name + '.sqlite3')
    path.write_bytes(raw)
    with sqlite3.connect(path.as_uri() + '?mode=ro', uri=True) as db:
        assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
        rows = db.execute('SELECT account,data FROM roles').fetchall()
        assert len(rows) == 1 and rows[0][0] == 'v106_fixed_test'
        role = json.loads(rows[0][1])
    assert (role['level'], role['vip_level'], role['gold_coin']) == (99, 10, 10000)
    assert role['guild']['unions']['2']['level'] == 5
    return role


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    assert call('emu', 'avd', 'name').decode().splitlines()[0] == 'standalone32'
    info = call('shell', 'dumpsys', 'package', OFFICIAL).decode()
    assert 'versionCode=106 ' in info
    original = official_save()
    official_apk = call('shell', 'pm', 'path', OFFICIAL).decode().strip()[8:]
    installed_hash = hashlib.sha256(call('exec-out', 'cat', official_apk, timeout=120)).hexdigest()
    expected = json.loads((ROOT / 'build/金箍棒3.87-离线单机-arm32-v106.manifest.json').read_text())
    assert installed_hash == expected['apk_sha256']
    result = call('install', '--no-streaming', '-r', str(ROOT / 'build/金箍棒ol测试版-v106.apk'), timeout=300)
    assert b'Success' in result, result
    assert official_save() == original
    print('Both APKs installed; official APK and save unchanged.', flush=True)
    call('shell', 'am', 'start', '-n', OFFICIAL + '/com.jgbol.offline.LauncherActivity')
    call('shell', 'am', 'start', '-n', TEST + '/com.jgbol.offline.LauncherActivity')
    meta = json.loads((ROOT / 'build/金箍棒ol测试版-v106.manifest.json').read_text())
    for attempt in range(120):
        logs = call('logcat', '-d', '-s', 'JGBOffline:I', '*:S').decode()
        if 'OFFLINE_READY ' + meta['program_sha256'] in logs:
            break
        if attempt % 10 == 0:
            print('Waiting for test runtime:', attempt * 3, 'seconds', flush=True)
        time.sleep(3)
    else:
        (EVIDENCE / 'device-startup.log').write_text(logs)
        raise RuntimeError('Test runtime not ready')
    (EVIDENCE / 'device-startup.log').write_text(logs)
    role = test_save('initial')
    assert official_save() == original
    info2 = call('shell', 'dumpsys', 'package', TEST).decode()
    uid = lambda text: text.split('userId=')[1].split()[0]
    assert uid(info) != uid(info2)
    (EVIDENCE / 'device-validation.json').write_text(json.dumps(dict(
        device='standalone32 / Android 6 ARMv7', test_apk_sha256=meta['apk_sha256'],
        official_apk_sha256=installed_hash, official_save_sha256_before=original,
        official_save_sha256_after=official_save(), different_android_uids=True,
        coexist_install=True, test_runtime_ready=True, fixed_role_count=1,
        level=role['level'], vip=role['vip_level'], gold=role['gold_coin'],
        guild_level=role['guild']['unions']['2']['level'],
        database_path=meta['player_database']), ensure_ascii=False, indent=2) + '\n')
    print('Test runtime ready; fixed starter valid; official save byte-identical.', flush=True)


if __name__ == '__main__':
    main()
