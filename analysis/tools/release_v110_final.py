"""Package current sources on the v110 retry fix, verify, then replace distribution."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from build_channel360 import TOOLS, run
from build_offline import SIGNING_KEY, signer_certificate
from offline_android.pack_payload import build_payload, collect_files, verify_payload

REVISION = 'formal-latest-20261106'
WORK = ROOT / '.runtime' / ('v110-' + REVISION)
EVIDENCE = ROOT / 'analysis/evidence/v110' / REVISION
ARCHIVE = ROOT / 'build/archive/v110-before-formal-latest-20261106'
BASE = ROOT / 'build/candidates/金箍棒3.87离线v110-补丁重试待验收.apk'
BASE_SHA = '5b2a5ba229a7bb12ea70bf7efa87cdf4ff418b9b19698d8e0b2c6f9a3356c300'
OLD = ROOT / 'build/金箍棒3.87离线正式版v110.apk'
APK = WORK / '金箍棒ol离线正式版v110.apk'
TARGET = ROOT / 'build' / APK.name
SUITES = [
    'test_gift_codes', 'test_activity_fish', 'test_activity_rulai',
    'test_qiankun_bags', 'test_activity_moon', 'test_activity_rice',
    'test_resource_preload', 'test_role_performance', 'test_achievement_performance',
    'test_achievements', 'test_achievement_hotupdate', 'test_combat_power',
    'test_formation', 'test_immortal', 'test_immortal_hotupdate', 'test_journey',
    'test_reborn', 'test_reborn_hotupdate', 'test_activity', 'test_activity_performance',
    'test_summon', 'test_request_wait', 'test_request_recovery', 'test_request_timing',
    'test_request_timing_client', 'test_activity_entry_client', 'test_game_clock',
    'test_time_guard', 'test_activity_clock_boundaries', 'test_activity_nine_sky',
    'test_babel_hotupdate', 'test_item_rewards', 'test_vip',
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def report(name, value):
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / (name + '.json')).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def check_sources():
    tree = WORK / 'payload-new'
    verify_payload(tree)
    files = collect_files()
    for name, path in files.items():
        if name != 'network_redirect/login.html':
            assert path.read_bytes() == (tree / name).read_bytes(), name
    from network_redirect.summon import client_source, load_rules
    assert client_source(load_rules()).encode() == (tree / 'offline_client.lua').read_bytes()
    return len(files) - 1


def prepare():
    assert not APK.exists(), 'Already built; use verify/publish for the staged APK'
    assert sha(BASE.read_bytes()) == BASE_SHA
    WORK.mkdir(parents=True, exist_ok=True)
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    backups = {}
    for path in [*OLD.parent.glob(OLD.stem + '.*'),
                 *BASE.parent.glob(BASE.stem + '.*'), ROOT / 'build/v110更新说明.txt']:
        destination = ARCHIVE / path.name
        if destination.exists():
            assert destination.read_bytes() == path.read_bytes(), path
        else:
            shutil.copy2(path, destination)
        backups[str(path.relative_to(ROOT))] = sha(path.read_bytes())
    report('backups', backups)
    manifest = build_payload(WORK / 'backend.zip')
    with zipfile.ZipFile(BASE) as old:
        old_program = old.read('assets/offline/program.zip')
        with zipfile.ZipFile(io.BytesIO(old_program)) as before, \
                zipfile.ZipFile(WORK / 'backend.zip') as backend, \
                zipfile.ZipFile(WORK / 'program.zip', 'w') as after:
            for entry in backend.infolist():
                after.writestr(entry, backend.read(entry))
            for entry in before.infolist():
                if entry.filename.startswith('client/'):
                    after.writestr(entry, before.read(entry))
        program = (WORK / 'program.zip').read_bytes()
        with zipfile.ZipFile(io.BytesIO(old_program)) as before, zipfile.ZipFile(io.BytesIO(program)) as after:
            assert after.testzip() is None
            names = set(before.namelist()) | set(after.namelist())
            changes = sorted(n for n in names if n not in before.namelist() or
                             n not in after.namelist() or before.read(n) != after.read(n))
            assert not any(n.startswith('client/') for n in changes)
            assert not any(Path(n).suffix in ('.db', '.sqlite3', '.pyc') or
                           'save' in Path(n).parts for n in after.namelist())
            after.extractall(WORK / 'payload-new')
        properties = old.read('assets/offline/build.properties').decode()
        assert properties.count(sha(old_program)) == 1
        replacements = {'assets/offline/program.zip': program,
                        'assets/offline/build.properties': properties.replace(sha(old_program), sha(program)).encode()}
        with zipfile.ZipFile(WORK / 'unsigned.apk', 'w') as new:
            for entry in old.infolist():
                if not entry.filename.startswith('META-INF/'):
                    new.writestr(entry, replacements.get(entry.filename, old.read(entry)))
    run(TOOLS / 'zipalign', '-f', '4', WORK / 'unsigned.apk', WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'sign', '--ks', SIGNING_KEY, '--ks-key-alias', 'channel360',
        '--ks-pass', 'pass:local-test-only', '--out', APK, WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'verify', '--verbose', APK)
    run(TOOLS / 'zipalign', '-c', '4', APK)
    assert signer_certificate(BASE) == signer_certificate(APK)
    badging = lambda path: subprocess.check_output([str(TOOLS / 'aapt'), 'dump', 'badging', str(path)])
    metadata = badging(APK)
    assert metadata == badging(BASE)
    assert b"versionCode='110' versionName='3.87-offline.10'" in metadata
    (EVIDENCE / 'badging.txt').write_bytes(metadata)
    native_report = json.loads((ROOT / 'analysis/evidence/v110/guangsu-retry-20261106/candidate-validation.json').read_text())
    assert sha((ROOT / 'offline_android/native/offline.c').read_bytes()) == native_report['native_source_sha256']
    with zipfile.ZipFile(BASE) as old, zipfile.ZipFile(APK) as new:
        assert new.testzip() is None
        names = lambda z: {n for n in z.namelist() if not n.startswith('META-INF/')}
        assert names(old) == names(new)
        outer_changes = sorted(n for n in names(old) if old.read(n) != new.read(n))
        assert outer_changes == sorted(replacements)
        assert sha(new.read('lib/armeabi-v7a/liboffline.so')) == native_report['native_adapter_sha256']
    result = dict(revision=REVISION, apk=APK.name, apk_sha256=sha(APK.read_bytes()),
                  apk_bytes=APK.stat().st_size, version_code=110, version_name='3.87-offline.10',
                  home_version_label='v110', baseline=str(BASE.relative_to(ROOT)), baseline_sha256=BASE_SHA,
                  program_sha256=sha(program), payload_bundle_id=manifest['bundle_id'],
                  payload_files=len(manifest['files']), current_source_files_verified=check_sources(),
                  changed_program_entries=changes, changed_apk_entries=outer_changes,
                  certificate_sha256=signer_certificate(APK), android_manifest_unchanged=True,
                  native_retry_preserved=True, native_adapter_sha256=native_report['native_adapter_sha256'],
                  contains_player_database=False, player_database='files/save/game.sqlite3',
                  device_tested=False, physical_device_tested=False)
    report('build-validation', result)
    APK.with_suffix('.manifest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    APK.with_suffix('.apk.sha256').write_text(result['apk_sha256'] + '  ' + APK.name + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)


def verify():
    worker = r'''
import hashlib, json, pathlib, sys, unittest
root, work, evidence, apk, suites = sys.argv[1:]
root, work, evidence = map(pathlib.Path, (root, work, evidence))
program = work / 'payload-new'
sys.path[:0] = [str(program), str(root / 'tests'), str(root), '/private/tmp/jgbol-wait-test-deps']
# The resource-preload closure test also imports the host-only packaging tool.
# Runtime modules still resolve from the extracted APK; pack_payload is not shipped.
import offline_android
offline_android.__path__.append(str(root / 'offline_android'))
suites = json.loads(suites)
loaded = unittest.defaultTestLoader.loadTestsFromNames(suites)
def cases(node):
    if isinstance(node, unittest.TestSuite):
        for child in node: yield from cases(child)
    else: yield node
unique = {c.id().removeprefix('tests.'): c for c in cases(loaded)}
result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(unique.values()))
modules = []
for name, module in list(sys.modules.items()):
    if name.startswith('network_redirect.') and getattr(module, '__file__', None):
        assert pathlib.Path(module.__file__).resolve().is_relative_to(program.resolve()), name
        modules.append(name)
report = dict(apk_sha256=hashlib.sha256(pathlib.Path(apk).read_bytes()).hexdigest(),
    passed=result.wasSuccessful(), tests=result.testsRun, errors=len(result.errors),
    failures=len(result.failures), skipped=len(result.skipped), suites=suites,
    test_ids=list(unique), failed_test_ids=[c.id() for c, _ in result.errors + result.failures],
    actual_packaged_modules=modules)
(evidence / 'protocol-validation.json').write_text(json.dumps(report, indent=2)+'\n')
raise SystemExit(not result.wasSuccessful() or bool(result.skipped))
'''
    with (EVIDENCE / 'protocol-tests.log').open('w') as log:
        subprocess.run([sys.executable, '-I', '-u', '-c', worker, str(ROOT), str(WORK),
                        str(EVIDENCE), str(APK), json.dumps(SUITES)], stdout=log, stderr=subprocess.STDOUT, check=True)
    print((EVIDENCE / 'protocol-tests.log').read_text()[-800:], flush=True)
    verify_finish()


def verify_finish():
    validation = json.loads((EVIDENCE / 'protocol-validation.json').read_text())
    assert validation['passed'] and validation['apk_sha256'] == sha(APK.read_bytes())
    worker = r'''
import pathlib, sys
root, work, evidence, apk = sys.argv[1:]
sys.path.insert(0, root)
from analysis.tools import verify_v110
verify_v110.OUTPUT = pathlib.Path(apk)
verify_v110.EVIDENCE = pathlib.Path(evidence)
sys.argv = ['verify_v110', 'lua', '--candidate', work]
verify_v110.main()
'''
    with (EVIDENCE / 'lua-tests.log').open('w') as log:
        subprocess.run([sys.executable, '-I', '-c', worker, str(ROOT), str(WORK), str(EVIDENCE), str(APK)],
                       stdout=log, stderr=subprocess.STDOUT, check=True)
    from analysis.tools import verify_v110_payload
    verify_v110_payload.OUTPUT = APK
    verify_v110_payload.WORK = WORK
    verify_v110_payload.EVIDENCE = EVIDENCE
    verify_v110_payload.main()
    check_sources()


def retry_test_environment():
    """Recheck missing host-helper/Lua dependencies, preserving initial evidence."""
    import re
    initial = json.loads((EVIDENCE / 'protocol-validation.json').read_text())
    test_id = 'test_resource_preload.ResourcePreloadPlanTests.test_shared_payload_and_desktop_cleanup_include_preloader'
    assert initial['failed_test_ids'] == [test_id] and initial['errors'] == 1
    assert not initial['failures']
    assert initial['apk_sha256'] == sha(APK.read_bytes())
    logs = (EVIDENCE / 'protocol-tests.log').read_text()
    assert "ModuleNotFoundError: No module named 'offline_android.pack_payload'" in logs
    skipped = [f'{group}.{method}' for method, group in re.findall(
        r"^(test_\w+) \(([^)]+)\) \.\.\. skipped 'requires lupa.lua51'$", logs, re.M)]
    assert len(skipped) == initial['skipped'] == 40
    selected = [test_id, *skipped]
    report('protocol-initial-validation', initial)
    worker = r'''
import json, pathlib, sys, unittest
root, program, names = sys.argv[1:]
names = json.loads(names)
sys.path[:0] = [program, str(pathlib.Path(root) / 'tests'), root, '/private/tmp/jgbol-wait-test-deps']
import offline_android
assert pathlib.Path(offline_android.__file__).resolve().is_relative_to(pathlib.Path(program).resolve())
offline_android.__path__.append(str(pathlib.Path(root) / 'offline_android'))
result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names))
assert result.testsRun == len(names) and result.wasSuccessful() and not result.skipped
for name, module in list(sys.modules.items()):
    if name.startswith('network_redirect.') and getattr(module, '__file__', None):
        assert pathlib.Path(module.__file__).resolve().is_relative_to(pathlib.Path(program).resolve()), name
'''
    with (EVIDENCE / 'environment-recheck.log').open('w') as log:
        subprocess.run([sys.executable, '-I', '-c', worker, str(ROOT), str(WORK / 'payload-new'), json.dumps(selected)],
                       stdout=log, stderr=subprocess.STDOUT, check=True)
    initial.update(passed=True, errors=0, skipped=0, failed_test_ids=[], initial_environment_errors=1,
                   initial_environment_skips=40, rechecked_test_ids=selected,
                   host_only_helper='offline_android.pack_payload', lua_test_dependency='/private/tmp/jgbol-wait-test-deps',
                   initial_report='protocol-initial-validation.json')
    report('protocol-validation', initial)
    verify_finish()


def publish():
    digest = sha(APK.read_bytes())
    for name in ('build-validation', 'protocol-validation', 'lua-validation', 'payload-save-validation',
                 'device-validation', 'startup-ui-validation'):
        result = json.loads((EVIDENCE / (name + '.json')).read_text())
        assert result['apk_sha256'] == digest
        if name in ('protocol-validation', 'lua-validation'):
            assert result['passed'] and not result.get('skipped', 0)
        if name == 'payload-save-validation':
            assert result['existing_role_values_preserved'] and result['source_qa_save_unchanged']
        if name == 'device-validation':
            assert result['new_program_ready'] and result['save_byte_identical_after_install']
            assert result['all_existing_tables_preserved_after_start']
        if name == 'startup-ui-validation':
            assert result['cold_start_native_branding_verified'] and result['no_lua_error']
    assert '\nOK\n' in (EVIDENCE / 'host-android-tests.log').read_text()
    check_sources()
    backups = json.loads((EVIDENCE / 'backups.json').read_text())
    old_artifacts = [ROOT / name for name in backups if name != 'build/v110更新说明.txt']
    for path in old_artifacts:
        assert sha(path.read_bytes()) == backups[str(path.relative_to(ROOT))]
        assert path.read_bytes() == (ARCHIVE / path.name).read_bytes()
    assert not TARGET.exists(), 'Release already exists'
    metadata = json.loads((EVIDENCE / 'build-validation.json').read_text())
    metadata.update(device_tested=True, qa_same_version_install_verified=True,
                    qa_cold_start_verified=True, baseline_archive=str((ARCHIVE / BASE.name).relative_to(ROOT)),
                    protocol_tests=json.loads((EVIDENCE / 'protocol-validation.json').read_text())['tests'],
                    save_migration_verified=True, guangsu_activity_page_verified=False)
    APK.with_suffix('.manifest.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n')
    distribution = WORK / (APK.name + '.zip')
    with zipfile.ZipFile(distribution, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(APK, APK.name)
        z.write(ROOT / 'build/v110更新说明.txt', 'v110更新说明.txt')
        z.write(APK.with_suffix('.apk.sha256'), APK.name + '.sha256')
    with zipfile.ZipFile(distribution) as z:
        assert z.testzip() is None and sha(z.read(APK.name)) == digest
    for source in [APK, APK.with_suffix('.apk.sha256'), APK.with_suffix('.apk.idsig'),
                   APK.with_suffix('.manifest.json'), distribution]:
        target = TARGET.parent / source.name
        temporary = target.with_name(target.name + '.tmp')
        shutil.copy2(source, temporary)
        assert temporary.read_bytes() == source.read_bytes()
        temporary.replace(target)
    assert sha(TARGET.read_bytes()) == digest
    for path in old_artifacts:
        path.unlink()
    report('published-release', dict(published=True, apk_sha256=digest,
           apk=str(TARGET.relative_to(ROOT)), distribution=str(TARGET.relative_to(ROOT))+'.zip',
           archive=str(ARCHIVE.relative_to(ROOT)), version_code=110,
           old_release_and_candidate_archived=True, physical_device_tested=False))
    print(TARGET, flush=True)


def device():
    """Replace only the dedicated QA installation after a complete save/APK backup."""
    import time
    from analysis.tools import verify_v110_device as qa
    from analysis.tools.verify_v105_update import database_snapshot
    qa.WORK = WORK / 'device'
    qa.WORK.mkdir(parents=True, exist_ok=True)
    assert qa.call('emu', 'avd', 'name').decode().splitlines()[0] == 'standalone32'
    assert qa.call('shell', 'getprop', 'sys.boot_completed').strip() == b'1'
    info = qa.call('shell', 'dumpsys', 'package', qa.PACKAGE).decode()
    assert 'versionCode=110 ' in info
    qa.call('shell', 'am', 'force-stop', qa.PACKAGE)
    qa.call('pull', '/data/data/' + qa.PACKAGE + '/files/save', str(qa.WORK / 'original-save'), timeout=180)
    original = qa.capture('original')
    installed = qa.call('shell', 'pm', 'path', qa.PACKAGE).decode().strip().removeprefix('package:')
    original_apk = qa.WORK / 'original.apk'
    qa.call('pull', installed, str(original_apk), timeout=180)
    assert signer_certificate(original_apk) == signer_certificate(APK)
    print('QA save and installed APK backed up', flush=True)
    result = qa.call('install', '--no-streaming', '-r', str(APK), timeout=300).decode()
    assert 'Success' in result, result
    installed_save = qa.capture('after-install-v110')
    assert original == installed_save
    print('QA replacement install passed; save bytes unchanged', flush=True)
    build = json.loads((EVIDENCE / 'build-validation.json').read_text())
    qa.call('logcat', '-c')
    qa.call('shell', 'am', 'start', '-n', qa.PACKAGE + '/com.jgbol.offline.LauncherActivity')
    deadline = time.monotonic() + 360
    while True:
        logs = qa.call('logcat', '-d', '-s', 'JGBOffline:I', '*:S').decode()
        assert 'Offline startup failed' not in logs, logs
        if 'OFFLINE_READY ' + build['program_sha256'] in logs:
            break
        if time.monotonic() > deadline:
            (EVIDENCE / 'device-startup.log').write_text(logs)
            raise TimeoutError('QA program startup timed out')
        time.sleep(2)
    (EVIDENCE / 'device-startup.log').write_text(logs)
    qa.call('shell', 'am', 'force-stop', qa.PACKAGE)
    stopped = qa.capture('after-stop-v110')
    old_tables = database_snapshot(qa.WORK / 'original.sqlite3')
    new_tables = database_snapshot(qa.WORK / 'after-stop-v110.sqlite3')
    assert old_tables == new_tables
    boot_id = qa.call('exec-out', 'cat', '/data/data/' + qa.PACKAGE + '/files/clock_boot_id').decode().strip()
    assert boot_id.startswith(('device:', 'kernel:', 'process:'))
    report('device-validation', dict(apk_sha256=build['apk_sha256'],
           device='standalone32 / emulator-5572 / Android 6 ARMv7',
           installed_baseline_sha256=sha(original_apk.read_bytes()), replacement_install=True,
           same_version_update=True, save_byte_identical_after_install=True,
           all_existing_tables_preserved_after_start=True, new_program_ready=True,
           boot_identity_bridge_verified=True, original=original, after_install=installed_save,
           after_stop=stopped, physical_device_test=False))
    from analysis.tools import verify_v110_startup_ui as ui
    ui.EVIDENCE = EVIDENCE
    ui.main()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['prepare', 'verify', 'retry_test_environment', 'device', 'publish'])
    globals()[parser.parse_args().stage]()
