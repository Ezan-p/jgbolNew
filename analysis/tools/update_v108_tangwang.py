"""Build, verify and publish the save-compatible Tangwang update to official v108."""
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
from offline_android.pack_payload import verify_payload

WORK = ROOT / '.runtime/v108-tangwang'
EVIDENCE = ROOT / 'analysis/evidence/v108_tangwang'
RELEASE = ROOT / 'build/金箍棒3.87离线正式版v108.apk'
ARCHIVE = ROOT / 'build/archive/v108-before-tangwang-20261031'
BASE = ARCHIVE / RELEASE.name
APK = WORK / RELEASE.name
BASE_SHA = 'c3005ec187e15c9c5b7e963b1976211c4fe65bdcb9cd873dbab65dfced179350'
SOURCES = ('network_redirect/activity_tangwang.py', 'network_redirect/tangwang_client.lua',
           'network_redirect/backend.py')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_report(name, value):
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def build():
    assert not APK.exists(), 'Candidate already exists'
    assert digest(RELEASE.read_bytes()) == BASE_SHA, 'Official v108 baseline changed'
    WORK.mkdir(parents=True, exist_ok=True)
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for source in (RELEASE, RELEASE.with_suffix('.apk.zip'), RELEASE.with_suffix('.manifest.json'),
                   RELEASE.with_suffix('.apk.sha256'), RELEASE.with_suffix('.apk.idsig'),
                   ROOT / 'build/v108更新说明.txt'):
        target = ARCHIVE / source.name
        if target.exists():
            assert target.read_bytes() == source.read_bytes(), target
        else:
            shutil.copy2(source, target)
    certificate = signer_certificate(BASE)
    from network_redirect.summon import client_source, load_rules
    replacements = {name: (ROOT / name).read_bytes() for name in SOURCES}
    replacements['offline_client.lua'] = client_source(load_rules()).encode()
    with zipfile.ZipFile(BASE) as old:
        original_program = old.read('assets/offline/program.zip')
        program = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(original_program)) as previous, zipfile.ZipFile(program, 'w') as updated:
            assert previous.read('offline_client.lua').replace(
                previous.read(SOURCES[1]), replacements[SOURCES[1]]) == replacements['offline_client.lua']
            manifest = json.loads(previous.read('payload-manifest.json'))
            for row in manifest['files']:
                if row['path'] in replacements:
                    data = replacements[row['path']]
                    row.update(size=len(data), sha256=digest(data))
            manifest['bundle_id'] = digest(json.dumps(manifest['files'], sort_keys=True,
                                                      separators=(',', ':')).encode())
            replacements['payload-manifest.json'] = json.dumps(manifest, ensure_ascii=False, indent=2).encode()
            assert set(replacements) <= set(previous.namelist())
            for entry in previous.infolist():
                updated.writestr(entry, replacements.get(entry.filename, previous.read(entry)))
        with zipfile.ZipFile(io.BytesIO(program.getvalue())) as updated:
            assert updated.testzip() is None
            updated.extractall(WORK / 'program')
        verify_payload(WORK / 'program')
        properties = old.read('assets/offline/build.properties').decode()
        assert properties.count(digest(original_program)) == 1
        properties = properties.replace(digest(original_program), digest(program.getvalue()))
        apk_replacements = {'assets/offline/program.zip': program.getvalue(),
                            'assets/offline/build.properties': properties.encode()}
        with zipfile.ZipFile(WORK / 'unsigned.apk', 'w') as updated:
            for entry in old.infolist():
                if not entry.filename.startswith('META-INF/'):
                    updated.writestr(entry, apk_replacements.get(entry.filename, old.read(entry)))
    run(TOOLS / 'zipalign', '-f', '4', WORK / 'unsigned.apk', WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'sign', '--ks', SIGNING_KEY, '--ks-key-alias', 'channel360',
        '--ks-pass', 'pass:local-test-only', '--out', APK, WORK / 'aligned.apk')
    assert signer_certificate(APK) == certificate
    run(TOOLS / 'apksigner', 'verify', '--verbose', APK)
    run(TOOLS / 'zipalign', '-c', '4', APK)
    badging = lambda path: subprocess.check_output([str(TOOLS / 'aapt'), 'dump', 'badging', str(path)])
    assert badging(BASE) == badging(APK)
    with zipfile.ZipFile(BASE) as old, zipfile.ZipFile(APK) as updated:
        assert updated.testzip() is None
        names = lambda z: {n for n in z.namelist() if not n.startswith('META-INF/')}
        assert names(old) == names(updated)
        changed = sorted(n for n in names(old) if old.read(n) != updated.read(n))
        assert changed == sorted(apk_replacements)
        with zipfile.ZipFile(io.BytesIO(original_program)) as previous, \
                zipfile.ZipFile(io.BytesIO(updated.read('assets/offline/program.zip'))) as current:
            assert set(previous.namelist()) == set(current.namelist())
            changed_program = sorted(n for n in current.namelist() if current.read(n) != previous.read(n))
            assert changed_program == sorted(replacements)
    report = json.loads(BASE.with_suffix('.manifest.json').read_text())
    report.update(release_revision='v108-tangwang-batch-20261031', feature_groups=11,
        baseline=str(BASE.relative_to(ROOT)), baseline_sha256=BASE_SHA,
        apk_sha256=digest(APK.read_bytes()), apk_bytes=APK.stat().st_size,
        program_sha256=digest(program.getvalue()), payload_bundle_id=manifest['bundle_id'],
        changed_apk_entries=changed, changed_program_entries=changed_program,
        same_version_update=True, android_manifest_unchanged=True,
        save_schema_and_path_unchanged=True, contains_player_database=False)
    APK.with_suffix('.manifest.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    APK.with_suffix('.apk.sha256').write_text(report['apk_sha256'] + '  ' + APK.name + '\n')
    write_report('build-validation.json', report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


def payload():
    sys.path.insert(0, '/private/tmp/jgbol-rank-lua')
    from analysis.tools import verify_v108_payload as verify
    verify.BASE, verify.APK, verify.WORK, verify.EVIDENCE = BASE, APK, WORK, EVIDENCE
    verify.main()


def protocol():
    worker = r'''
import json, pathlib, sys, unittest
program, root, report, sha = sys.argv[1:]
sys.path[:0] = [program, str(pathlib.Path(root)/'tests'), root]
suites = ['test_activity_tangwang', 'test_activity', 'test_activity_rank']
result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(suites))
modules = []
for name, module in list(sys.modules.items()):
    if name.startswith('network_redirect.') and getattr(module, '__file__', None):
        assert pathlib.Path(module.__file__).resolve().is_relative_to(pathlib.Path(program).resolve()), name
        modules.append(name)
pathlib.Path(report).write_text(json.dumps(dict(apk_sha256=sha, passed=result.wasSuccessful(),
    tests=result.testsRun, suites=suites, actual_packaged_modules=modules), indent=2)+'\n')
raise SystemExit(not result.wasSuccessful())
'''
    subprocess.run([sys.executable, '-I', '-c', worker, str(WORK / 'payload-new'), str(ROOT),
                    str(EVIDENCE / 'protocol-validation.json'), digest(APK.read_bytes())], check=True)


def device():
    from analysis.tools import verify_v108_device as verify
    verify.BASE, verify.APK, verify.WORK, verify.EVIDENCE = BASE, APK, WORK / 'device', EVIDENCE
    verify.main(expected_version=108, install_baseline=False)
    from analysis.tools import verify_v108_startup_ui as ui
    ui.EVIDENCE = EVIDENCE
    ui.main()


def publish():
    sha = digest(APK.read_bytes())
    read = lambda name: json.loads((EVIDENCE / name).read_text())
    for name in ('build-validation.json', 'payload-save-validation.json', 'protocol-validation.json',
                 'device-validation.json', 'startup-ui-validation.json'):
        assert read(name)['apk_sha256'] == sha, name
    assert read('payload-save-validation.json')['all_database_tables_equal_after_upgrade_and_restart']
    assert read('payload-save-validation.json')['source_qa_save_unchanged']
    assert read('protocol-validation.json')['passed']
    assert read('device-validation.json')['save_byte_identical_after_install_start_and_stop']
    assert read('startup-ui-validation.json')['cold_start_native_branding_verified']
    assert digest(BASE.read_bytes()) == digest(RELEASE.read_bytes()) == BASE_SHA
    for suffix in ('.apk', '.manifest.json', '.apk.sha256', '.apk.idsig'):
        source, target = APK.with_suffix(suffix), RELEASE.with_suffix(suffix)
        temporary = target.with_name(target.name + '.tmp')
        shutil.copy2(source, temporary)
        temporary.replace(target)
    archive = RELEASE.with_suffix('.apk.zip')
    temporary = archive.with_name(archive.name + '.tmp')
    with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(RELEASE, RELEASE.name)
    with zipfile.ZipFile(temporary) as z:
        assert z.testzip() is None and digest(z.read(RELEASE.name)) == sha
    temporary.replace(archive)
    assert digest(RELEASE.read_bytes()) == sha
    write_report('published-release.json', dict(published=True, apk_sha256=sha,
        version_code=108, save_preservation_verified=True, baseline_preserved=str(BASE.relative_to(ROOT)),
        downloads=[str(RELEASE.relative_to(ROOT)), str(archive.relative_to(ROOT))]))
    print(RELEASE)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['build', 'payload', 'protocol', 'device', 'publish'])
    globals()[parser.parse_args().stage]()
