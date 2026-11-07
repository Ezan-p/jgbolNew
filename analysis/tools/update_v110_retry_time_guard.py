"""Add clock-jump quarantine to the v110 retry candidate, preserving its native fix."""
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

TARGET = ROOT / 'build/candidates/金箍棒3.87离线v110-补丁重试待验收.apk'
ARCHIVE = ROOT / 'build/archive/v110-retry-before-time-guard-20261106'
BASE = ARCHIVE / TARGET.name
BASE_SHA = '6d50e4be289cb51d4737ac821488f536f95b5612925515c4b95020a4e79fe275'
WORK = ROOT / '.runtime/v110-retry-time-guard-20261106'
EVIDENCE = ROOT / 'analysis/evidence/v110/retry-time-guard-20261106'
APK = WORK / TARGET.name
SOURCES = tuple('network_redirect/' + name + '.py' for name in (
    'game_clock', 'time_guard', 'backend', 'summon', 'activity_party'))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def report(name, data):
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / (name + '.json')).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def check_sources():
    verify_payload(WORK / 'payload-new')
    checked = 0
    for name, path in collect_files().items():
        if name != 'network_redirect/login.html':
            assert path.read_bytes() == (WORK / 'payload-new' / name).read_bytes(), name
            checked += 1
    from network_redirect.summon import client_source, load_rules
    assert client_source(load_rules()).encode() == (WORK / 'payload-new/offline_client.lua').read_bytes()
    return checked


def prepare():
    assert not APK.exists(), 'Staged candidate already exists'
    assert digest(TARGET.read_bytes()) == BASE_SHA, 'Retry candidate baseline changed'
    WORK.mkdir(parents=True, exist_ok=True)
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for source in [*TARGET.parent.glob(TARGET.stem + '.*'), ROOT / 'build/v110更新说明.txt']:
        target = ARCHIVE / source.name
        if target.exists():
            assert target.read_bytes() == source.read_bytes(), target
        else:
            shutil.copy2(source, target)
    replacements = {name: (ROOT / name).read_bytes() for name in SOURCES}
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
        outer = {'assets/offline/program.zip': program, 'assets/offline/build.properties':
                 properties.replace(digest(original), digest(program)).encode()}
        with zipfile.ZipFile(WORK / 'unsigned.apk', 'w') as after:
            for entry in old.infolist():
                if not entry.filename.startswith('META-INF/'):
                    after.writestr(entry, outer.get(entry.filename, old.read(entry)))
    run(TOOLS / 'zipalign', '-f', '4', WORK / 'unsigned.apk', WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'sign', '--ks', SIGNING_KEY, '--ks-key-alias', 'channel360',
        '--ks-pass', 'pass:local-test-only', '--out', APK, WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'verify', '--verbose', APK)
    run(TOOLS / 'zipalign', '-c', '4', APK)
    assert signer_certificate(APK) == signer_certificate(BASE)
    badging = lambda path: subprocess.check_output([str(TOOLS / 'aapt'), 'dump', 'badging', str(path)])
    assert badging(BASE) == badging(APK)
    with zipfile.ZipFile(BASE) as old, zipfile.ZipFile(APK) as new:
        assert new.testzip() is None
        names = lambda z: {n for n in z.namelist() if not n.startswith('META-INF/')}
        assert names(old) == names(new)
        changed = sorted(n for n in names(old) if old.read(n) != new.read(n))
        assert changed == sorted(outer), changed
        native_sha = digest(new.read('lib/armeabi-v7a/liboffline.so'))
        native_check = json.loads((ROOT / 'analysis/evidence/v110/guangsu-retry-20261106/candidate-validation.json').read_text())
        assert native_sha == native_check['native_adapter_sha256']
        with zipfile.ZipFile(io.BytesIO(original)) as before, zipfile.ZipFile(io.BytesIO(program)) as after:
            assert after.testzip() is None
            assert set(before.namelist()) == set(after.namelist())
            changed_program = sorted(n for n in after.namelist() if before.read(n) != after.read(n))
            assert changed_program == sorted(replacements), changed_program
            assert not any(Path(n).suffix in ('.db', '.sqlite3', '.pyc') or
                           'save' in Path(n).parts for n in after.namelist())
            after.extractall(WORK / 'payload-new')
    result = dict(revision='v110-retry-time-guard-20261106', candidate=str(TARGET.relative_to(ROOT)),
        baseline=str(BASE.relative_to(ROOT)), baseline_sha256=BASE_SHA,
        apk_sha256=digest(APK.read_bytes()), apk_bytes=APK.stat().st_size,
        program_sha256=digest(program), payload_bundle_id=manifest['bundle_id'],
        payload_file_count=len(manifest['files']), workspace_files_checked=check_sources(),
        changed_apk_entries=changed, changed_program_entries=changed_program,
        same_certificate=True, android_manifest_unchanged=True, version_code=110,
        native_retry_preserved=True, native_adapter_sha256=native_sha,
        contains_player_database=False, save_path_unchanged=True,
        device_tested=False, physical_device_tested=False, formal_release_replaced=False)
    APK.with_suffix('.manifest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    APK.with_suffix('.apk.sha256').write_text(result['apk_sha256'] + '  ' + APK.name + '\n')
    report('build-validation', result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def verify():
    worker = r'''
import json, pathlib, sys, unittest
program, root, destination, sha = sys.argv[1:]
sys.path[:0] = [program, root]
suites = ['tests.test_game_clock', 'tests.test_time_guard', 'tests.test_activity_clock_boundaries',
          'tests.test_summon', 'tests.test_activity_party']
result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(suites))
modules = []
for name, module in list(sys.modules.items()):
    if name.startswith('network_redirect.') and getattr(module, '__file__', None):
        assert pathlib.Path(module.__file__).resolve().is_relative_to(pathlib.Path(program).resolve()), name
        modules.append(name)
pathlib.Path(destination).write_text(json.dumps(dict(apk_sha256=sha, passed=result.wasSuccessful(),
    tests=result.testsRun, suites=suites, actual_packaged_modules=modules,
    failures=len(result.failures), errors=len(result.errors), skipped=len(result.skipped)), indent=2)+'\n')
raise SystemExit(not result.wasSuccessful())
'''
    with (EVIDENCE / 'protocol-tests.log').open('w') as log:
        subprocess.run([sys.executable, '-I', '-c', worker, str(WORK / 'payload-new'), str(ROOT),
                        str(EVIDENCE / 'protocol-validation.json'), digest(APK.read_bytes())],
                       stdout=log, stderr=subprocess.STDOUT, check=True)
    print((EVIDENCE / 'protocol-tests.log').read_text()[-1000:])
    from analysis.tools import verify_v110_payload
    verify_v110_payload.OUTPUT = APK
    verify_v110_payload.WORK = WORK
    verify_v110_payload.EVIDENCE = EVIDENCE
    verify_v110_payload.main()


def publish():
    sha = digest(APK.read_bytes())
    validation = json.loads((EVIDENCE / 'protocol-validation.json').read_text())
    assert validation['passed'] and validation['apk_sha256'] == sha and not validation['skipped']
    assert json.loads((EVIDENCE / 'build-validation.json').read_text())['apk_sha256'] == sha
    save = json.loads((EVIDENCE / 'payload-save-validation.json').read_text())
    assert save['apk_sha256'] == sha and save['existing_role_values_preserved'] and save['source_qa_save_unchanged']
    check_sources()
    assert digest(BASE.read_bytes()) == digest(TARGET.read_bytes()) == BASE_SHA
    for suffix in ('.apk', '.manifest.json', '.apk.sha256', '.apk.idsig'):
        source, target = APK.with_suffix(suffix), TARGET.with_suffix(suffix)
        staged = target.with_name(target.name + '.tmp')
        shutil.copy2(source, staged)
        staged.replace(target)
    assert digest(TARGET.read_bytes()) == sha
    report('published-candidate', dict(candidate=str(TARGET.relative_to(ROOT)), apk_sha256=sha,
        baseline=str(BASE.relative_to(ROOT)), tests=validation['tests'], device_tested=False,
        formal_release_replaced=False))
    print(TARGET)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['prepare', 'verify', 'publish'])
    globals()[parser.parse_args().stage]()
