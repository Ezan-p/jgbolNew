"""Repackage the activity entry loader fix in v110, preserving Android and save identity."""
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
from offline_android.pack_payload import collect_files, verify_payload

WORK = ROOT / '.runtime/v110-activity-entry-fix-20261106'
EVIDENCE = ROOT / 'analysis/evidence/v110/activity-entry-fix-20261106'
RELEASE = ROOT / 'build/金箍棒3.87离线正式版v110.apk'
ARCHIVE = ROOT / 'build/archive/v110-before-activity-entry-fix-20261106'
BASE = ARCHIVE / RELEASE.name
APK = WORK / RELEASE.name
BASE_SHA = '6115c733f0522a5258c080e49a08ca0753bbb0d8b5589809e34e15ae7d48eb79'
SOURCES = (
    'network_redirect/activity_entry_client.lua',
    'network_redirect/yuanshi_client.lua',
    'network_redirect/summon.py',
)
SUITES = [
    'test_request_timing_client.RequestTimingClientTests',
    'test_request_wait.RequestWaitTests',
    'test_request_timing.TimingTests',
    'test_request_recovery.RequestRecoveryTests',
    'test_activity_performance.ActivityPerformanceTests',
    'test_activity_entry_client.ActivityEntryClientTests',
]

def digest(data):
    return hashlib.sha256(data).hexdigest()


def report(name, data):
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def prepare():
    assert not APK.exists(), 'Candidate already exists'
    assert digest(RELEASE.read_bytes()) == BASE_SHA, 'Release baseline changed'
    WORK.mkdir(parents=True, exist_ok=True)
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for source in [*RELEASE.parent.glob(RELEASE.stem + '.*'), ROOT / 'build/v110更新说明.txt']:
        target = ARCHIVE / source.name
        if target.exists():
            assert target.read_bytes() == source.read_bytes(), target
        else:
            shutil.copy2(source, target)
    certificate = signer_certificate(BASE)
    from offline_android.native.build_native import build as build_native
    native = build_native(WORK / 'liboffline.so')
    replacements = {name: (ROOT / name).read_bytes() for name in SOURCES}
    from network_redirect.summon import client_source, load_rules
    replacements['offline_client.lua'] = client_source(load_rules()).encode('utf-8')
    with zipfile.ZipFile(BASE) as old:
        original = old.read('assets/offline/program.zip')
        buffer = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(original)) as before, zipfile.ZipFile(buffer, 'w') as after:
            manifest = json.loads(before.read('payload-manifest.json'))
            assert set(replacements) <= {row['path'] for row in manifest['files']}
            for row in manifest['files']:
                if row['path'] in replacements:
                    data = replacements[row['path']]
                    assert data != before.read(row['path']), row['path']
                    row.update(size=len(data), sha256=digest(data))
            manifest['bundle_id'] = digest(json.dumps(manifest['files'], sort_keys=True,
                                                      separators=(',', ':')).encode())
            replacements['payload-manifest.json'] = (json.dumps(manifest, ensure_ascii=False,
                                                                sort_keys=True, indent=2) + '\n').encode()
            for entry in before.infolist():
                after.writestr(entry, replacements.get(entry.filename, before.read(entry)))
        program = buffer.getvalue()
        properties = old.read('assets/offline/build.properties').decode()
        assert properties.count(digest(original)) == 1
        properties = properties.replace(digest(original), digest(program))
        outer = {'assets/offline/program.zip': program,
                 'assets/offline/build.properties': properties.encode(),
                 'lib/armeabi-v7a/liboffline.so': native.read_bytes()}
        with zipfile.ZipFile(WORK / 'unsigned.apk', 'w') as after:
            for entry in old.infolist():
                if not entry.filename.startswith('META-INF/'):
                    after.writestr(entry, outer.get(entry.filename, old.read(entry)))
    run(TOOLS / 'zipalign', '-f', '4', WORK / 'unsigned.apk', WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'sign', '--ks', SIGNING_KEY, '--ks-key-alias', 'channel360',
        '--ks-pass', 'pass:local-test-only', '--out', APK, WORK / 'aligned.apk')
    assert signer_certificate(APK) == certificate
    run(TOOLS / 'apksigner', 'verify', '--verbose', APK)
    run(TOOLS / 'zipalign', '-c', '4', APK)
    badging = lambda p: subprocess.check_output([str(TOOLS / 'aapt'), 'dump', 'badging', str(p)])
    assert badging(BASE) == badging(APK)
    with zipfile.ZipFile(BASE) as old, zipfile.ZipFile(APK) as new:
        assert new.testzip() is None
        names = lambda z: {n for n in z.namelist() if not n.startswith('META-INF/')}
        assert names(old) == names(new)
        changed = sorted(n for n in names(old) if old.read(n) != new.read(n))
        assert changed == sorted(outer), changed
        with zipfile.ZipFile(io.BytesIO(original)) as before, \
                zipfile.ZipFile(io.BytesIO(new.read('assets/offline/program.zip'))) as after:
            assert after.testzip() is None
            assert set(before.namelist()) == set(after.namelist())
            changed_program = sorted(n for n in after.namelist() if before.read(n) != after.read(n))
            assert changed_program == sorted(replacements), changed_program
            assert not any(Path(n).suffix in ('.db', '.sqlite3', '.pyc') or
                           'save' in Path(n).parts for n in after.namelist())
            after.extractall(WORK / 'payload-new')
    verify_payload(WORK / 'payload-new')
    checked = 0
    for name, path in collect_files().items():
        if name != 'network_redirect/login.html':
            assert path.read_bytes() == (WORK / 'payload-new' / name).read_bytes(), name
            checked += 1
    from network_redirect.summon import client_source, load_rules
    assert client_source(load_rules()) == (WORK / 'payload-new/offline_client.lua').read_text()
    result = json.loads(BASE.with_suffix('.manifest.json').read_text())
    for name, expected in result['java_source_sha256'].items():
        assert digest((ROOT / name).read_bytes()) == expected, name
    assert digest(BASE.read_bytes()) == BASE_SHA
    result.update(release_revision='v110-activity-entry-fix-20261106', feature_groups=6, incremental_fix_groups=3,
        baseline=str(BASE.relative_to(ROOT)), baseline_sha256=BASE_SHA,
        apk_sha256=digest(APK.read_bytes()), apk_bytes=APK.stat().st_size,
        program_sha256=digest(program), payload_bundle_id=manifest['bundle_id'],
        changed_apk_entries=changed, changed_program_entries=changed_program,
        same_version_update=True, android_manifest_unchanged=True,
        offline_java_bridge_updated=False, offline_native_adapter_updated=True,
        native_adapter_sha256=digest(native.read_bytes()),
        native_source_sha256=digest((ROOT / 'offline_android/native/offline.c').read_bytes()),
        save_schema_and_path_unchanged=True, contains_player_database=False,
        workspace_files_checked=checked, previous_evidence='analysis/evidence/v110/request-fixes-20261106',
        update_evidence=str(EVIDENCE.relative_to(ROOT)))
    APK.with_suffix('.manifest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    APK.with_suffix('.apk.sha256').write_text(result['apk_sha256'] + '  ' + APK.name + '\n')
    report('build-validation.json', result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def verify():
    worker = r'''
import hashlib, json, pathlib, sys, unittest
program, root, destination, sha, suites = sys.argv[1:]
sys.path[:0] = [program, str(pathlib.Path(root)/'tests'), root, '/private/tmp/jgbol-wait-test-deps']
suites = json.loads(suites)
def cases(node):
    if isinstance(node, unittest.TestSuite):
        for child in node:
            yield from cases(child)
    else:
        yield node
unique = {c.id().removeprefix('tests.'): c for c in cases(unittest.defaultTestLoader.loadTestsFromNames(suites))}
result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(unique.values()))
modules = []
for name, module in list(sys.modules.items()):
    if name.startswith('network_redirect.') and getattr(module, '__file__', None):
        assert pathlib.Path(module.__file__).resolve().is_relative_to(pathlib.Path(program).resolve()), name
        modules.append(name)
pathlib.Path(destination).write_text(json.dumps(dict(apk_sha256=sha, passed=result.wasSuccessful(),
    tests=result.testsRun, suites=suites, test_ids=list(unique), actual_packaged_modules=modules,
    failures=len(result.failures), errors=len(result.errors), skipped=len(result.skipped)), indent=2)+'\n')
raise SystemExit(not result.wasSuccessful())
'''
    with (EVIDENCE / 'protocol-tests.log').open('w') as log:
        subprocess.run([sys.executable, '-I', '-c', worker, str(WORK / 'payload-new'), str(ROOT),
                        str(EVIDENCE / 'protocol-validation.json'), digest(APK.read_bytes()),
                        json.dumps(SUITES)], stdout=log, stderr=subprocess.STDOUT, check=True)
    print((EVIDENCE / 'protocol-tests.log').read_text()[-1000:])
    verify_lua()


def verify_lua():
    worker = r"""
import pathlib, sys
root, work, evidence = map(pathlib.Path, sys.argv[1:])
sys.path.insert(0, str(root))
from analysis.tools import verify_v110
verify_v110.WORK = work
verify_v110.EVIDENCE = evidence
sys.argv = ['verify_v110', 'lua', '--candidate', str(work)]
verify_v110.main()
"""
    with (EVIDENCE / 'lua-tests.log').open('w') as log:
        subprocess.run([sys.executable, '-I', '-c', worker, str(ROOT), str(WORK), str(EVIDENCE)],
                       stdout=log, stderr=subprocess.STDOUT, check=True)
    print((EVIDENCE / 'lua-tests.log').read_text())


def verify_save():
    # The existing migration verifier starts with the preserved v109 and uses
    # a disposable copy of the QA database; it never changes the source save.
    from analysis.tools import verify_v110_payload
    verify_v110_payload.OUTPUT = APK
    verify_v110_payload.WORK = WORK
    verify_v110_payload.EVIDENCE = EVIDENCE
    verify_v110_payload.main()


def device():
    # Same-version replacement on the dedicated QA AVD, without downgrading.
    from analysis.tools import verify_v110_device
    verify_v110_device.WORK = WORK / 'device'
    verify_v110_device.EVIDENCE = EVIDENCE
    verify_v110_device.APK = APK
    verify_v110_device.BASE = BASE
    verify_v110_device.main(expected_version=110, install_baseline=False)


def startup():
    from analysis.tools import verify_v110_startup_ui
    verify_v110_startup_ui.EVIDENCE = EVIDENCE
    verify_v110_startup_ui.main()


def publish():
    sha = digest(APK.read_bytes())
    validation = json.loads((EVIDENCE / 'protocol-validation.json').read_text())
    assert validation['passed'] and validation['apk_sha256'] == sha and validation['tests'] >= 40 and validation['skipped'] == 0
    assert json.loads((EVIDENCE / 'build-validation.json').read_text())['apk_sha256'] == sha
    lua = json.loads((EVIDENCE / 'lua-validation.json').read_text())
    assert lua['passed'] and lua['apk_sha256'] == sha
    for name in ('payload-save-validation', 'device-validation', 'startup-ui-validation'):
        check = json.loads((EVIDENCE / (name + '.json')).read_text())
        assert check['apk_sha256'] == sha
        if name == 'payload-save-validation':
            assert check['existing_role_values_preserved'] and check['source_qa_save_unchanged']
        elif name == 'device-validation':
            assert check['same_version_update'] and check['save_byte_identical_after_install']
            assert check['new_program_ready'] and check['all_existing_tables_preserved_after_start']
        else:
            assert check['cold_start_native_branding_verified'] and check['no_lua_error']
            device_check = json.loads((EVIDENCE / 'device-validation.json').read_text())
            assert check['save_hash_after_ui'] == device_check['after_stop']['sha256']
    verify_payload(WORK / 'payload-new')
    for name, path in collect_files().items():
        if name != 'network_redirect/login.html':
            assert path.read_bytes() == (WORK / 'payload-new' / name).read_bytes(), name
    build = json.loads((EVIDENCE / 'build-validation.json').read_text())
    for name, expected in build['java_source_sha256'].items():
        assert digest((ROOT / name).read_bytes()) == expected, name
    from network_redirect.summon import client_source, load_rules
    assert client_source(load_rules()).encode() == (WORK / 'payload-new/offline_client.lua').read_bytes()
    assert digest(BASE.read_bytes()) == digest(RELEASE.read_bytes()) == BASE_SHA
    for name in SOURCES:
        assert (ROOT / name).read_bytes() == (WORK / 'payload-new' / name).read_bytes(), name
    native_hash = json.loads((EVIDENCE / 'build-validation.json').read_text())['native_adapter_sha256']
    assert digest((WORK / 'liboffline.so').read_bytes()) == native_hash
    guard = json.loads((EVIDENCE / 'native-guard-validation.json').read_text())
    assert guard['passed'] and len(guard['checks']) == 12
    assert guard['native_source_sha256'] == build['native_source_sha256'] == digest((ROOT / 'offline_android/native/offline.c').read_bytes())
    archive = RELEASE.with_suffix('.apk.zip')
    temporary = archive.with_name(archive.name + '.tmp')
    with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(APK, APK.name)
    with zipfile.ZipFile(temporary) as z:
        assert z.testzip() is None and digest(z.read(APK.name)) == sha
    for suffix in ('.apk', '.manifest.json', '.apk.sha256', '.apk.idsig'):
        source, target = APK.with_suffix(suffix), RELEASE.with_suffix(suffix)
        staged = target.with_name(target.name + '.tmp')
        shutil.copy2(source, staged)
        staged.replace(target)
    temporary.replace(archive)
    assert digest(RELEASE.read_bytes()) == sha
    report('published-release.json', dict(published=True, apk_sha256=sha, version_code=110,
        same_version_update=True, protocol_tests=validation['tests'],
        native_guard_checks=len(guard['checks']), activity_ui_touch_completed=False,
        device_limitations='activity-device-limitation.json',
        baseline_preserved=str(BASE.relative_to(ROOT)), device_test_performed=True, physical_device_test=False,
        downloads=[str(RELEASE.relative_to(ROOT)), str(archive.relative_to(ROOT))]))
    print(RELEASE)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['prepare', 'verify', 'verify_save', 'device', 'startup', 'publish'])
    globals()[parser.parse_args().stage]()
