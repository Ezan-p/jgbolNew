"""Replace-install v105 only on the guarded standalone32 QA device."""
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import time

root = Path(__file__).resolve().parents[2]
work = root / '.runtime/v105-reconcile-qa'
evidence = root / 'analysis/evidence/v105_reconcile'
adb = [str(root / '.runtime/sdk/platform-tools/adb'), '-s', 'emulator-5572']
package = 'com.sygame.jingubang.p360'
apk = work / '金箍棒3.87-离线单机-arm32-v105.apk'
manifest = json.loads(apk.with_suffix('.manifest.json').read_text())
def call(*args, timeout=60):
    return subprocess.check_output(adb + list(args), timeout=timeout)
def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def capture(name):
    target = work / name
    target.write_bytes(call('exec-out', 'cat', '/data/data/' + package + '/files/save/game.sqlite3'))
    with sqlite3.connect(target.as_uri() + '?mode=ro', uri=True) as db:
        assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
        counts = {table: db.execute('SELECT count(*) FROM ' + table).fetchone()[0] for table in ('roles', 'accounts')}
    return digest(target), counts
assert call('emu', 'avd', 'name').decode().splitlines()[0] == 'standalone32'
for _ in range(90):
    if call('shell', 'getprop', 'sys.boot_completed').strip() == b'1':
        break
    time.sleep(2)
else:
    raise AssertionError('QA device did not boot')
call('shell', 'am', 'force-stop', package)
installed = call('shell', 'pm', 'path', package).decode().strip().removeprefix('package:')
call('pull', installed, str(work / 'device-baseline.apk'), timeout=120)
assert digest(work / 'device-baseline.apk') == digest(work / 'baseline-v105.apk')
before, counts = capture('device-before.sqlite3')
print('Verified baseline v105 and backed up QA save:', counts, flush=True)
result = call('install', '--no-streaming', '-r', str(apk), timeout=240).decode()
assert 'Success' in result, result
print('Same-version replace install succeeded', flush=True)
after, after_counts = capture('device-after-install.sqlite3')
assert after == before and after_counts == counts
call('logcat', '-c')
call('shell', 'am', 'start', '-n', package + '/com.jgbol.offline.LauncherActivity')
ready = 'OFFLINE_READY ' + manifest['program_sha256']
for _ in range(90):
    logs = call('logcat', '-d', '-s', 'JGBOffline:I', '*:S').decode()
    if ready in logs:
        break
    time.sleep(2)
else:
    raise AssertionError('New runtime did not become ready')
(evidence / 'device-startup.log').write_text(logs)
started, started_counts = capture('device-after-start.sqlite3')
assert started == before and started_counts == counts
report = dict(date='2026-10-29', device='standalone32 / emulator-5572 / Android 6 API23 ARMv7',
    apk_sha256=digest(apk), baseline_apk_sha256=digest(work / 'device-baseline.apk'),
    package=package, version_code=105, certificate_sha256=manifest['certificate_sha256'],
    same_version_replace_install=True, save_before_after_install_and_start_byte_identical=True,
    save_sha256=dict(before=before, after_install=after, after_start=started),
    counts=counts, integrity='ok', new_program_ready=True, program_sha256=manifest['program_sha256'],
    player_emulators_modified=False, physical_device_test=False)
(evidence / 'device-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)
