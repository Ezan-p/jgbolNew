"""Update six v109 payload files without rebuilding the Android shell."""
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

WORK = ROOT / '.runtime/v109-latest'
EVIDENCE = ROOT / 'analysis/evidence/v109/latest-update'
RELEASE = ROOT / 'build/金箍棒3.87离线正式版v109.apk'
ARCHIVE = ROOT / 'build/archive/v109-before-latest-four-20261103'
BASE = ARCHIVE / RELEASE.name
APK = WORK / RELEASE.name
BASE_SHA = '78515804aea4127a668c2b036a25b968dc70f01193ee0ce6e0d0e9f614130998'
SOURCES = (
    'network_redirect/activity_babel.py',
    'network_redirect/combat_power.py',
    'server_config/cheer_rules.json',
    'server_config/gift_code_rules.json',
    'analysis/npc_design/rank_500/catalog.json',
    'analysis/npc_design/rank_500/profiles.json',
)
SUITES = [
    'test_activity_babel', 'test_babel_hotupdate', 'test_cheer',
    'test_cheer_attributes', 'test_feature_levels', 'test_market',
    'test_combat_power', 'test_formation', 'test_gift_codes',
    'test_item_rewards', 'test_equipment_crafting', 'test_recharge',
    'test_activity_rank', 'test_rank_rewards', 'test_npc_players',
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
    for source in [*RELEASE.parent.glob(RELEASE.stem + '.*'), ROOT / 'build/v109更新说明.txt']:
        target = ARCHIVE / source.name
        if target.exists():
            assert target.read_bytes() == source.read_bytes(), target
        else:
            shutil.copy2(source, target)
    certificate = signer_certificate(BASE)
    replacements = {name: (ROOT / name).read_bytes() for name in SOURCES}
    with zipfile.ZipFile(BASE) as old:
        original = old.read('assets/offline/program.zip')
        buffer = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(original)) as before, zipfile.ZipFile(buffer, 'w') as after:
            manifest = json.loads(before.read('payload-manifest.json'))
            assert set(SOURCES) <= {row['path'] for row in manifest['files']}
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
                 'assets/offline/build.properties': properties.encode()}
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
            after.extractall(WORK / 'program')
    verify_payload(WORK / 'program')
    checked = 0
    for name, path in collect_files().items():
        if name != 'network_redirect/login.html':
            assert path.read_bytes() == (WORK / 'program' / name).read_bytes(), name
            checked += 1
    from network_redirect.summon import client_source, load_rules
    assert client_source(load_rules()) == (WORK / 'program/offline_client.lua').read_text()
    result = json.loads(BASE.with_suffix('.manifest.json').read_text())
    result.update(release_revision='v109-latest-four-20261103', feature_groups=16,
        baseline=str(BASE.relative_to(ROOT)), baseline_sha256=BASE_SHA,
        apk_sha256=digest(APK.read_bytes()), apk_bytes=APK.stat().st_size,
        program_sha256=digest(program), payload_bundle_id=manifest['bundle_id'],
        changed_apk_entries=changed, changed_program_entries=changed_program,
        same_version_update=True, android_manifest_unchanged=True,
        save_schema_and_path_unchanged=True, contains_player_database=False,
        workspace_files_checked=checked, previous_evidence='analysis/evidence/v109',
        update_evidence=str(EVIDENCE.relative_to(ROOT)))
    APK.with_suffix('.manifest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    APK.with_suffix('.apk.sha256').write_text(result['apk_sha256'] + '  ' + APK.name + '\n')
    report('build-validation.json', result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def verify():
    worker = r'''
import hashlib, json, pathlib, sys, unittest
program, root, destination, sha, suites = sys.argv[1:]
sys.path[:0] = [program, str(pathlib.Path(root)/'tests'), root]
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
        subprocess.run([sys.executable, '-I', '-c', worker, str(WORK / 'program'), str(ROOT),
                        str(EVIDENCE / 'protocol-validation.json'), digest(APK.read_bytes()),
                        json.dumps(SUITES)], stdout=log, stderr=subprocess.STDOUT, check=True)
    print((EVIDENCE / 'protocol-tests.log').read_text()[-1000:])


def publish():
    sha = digest(APK.read_bytes())
    validation = json.loads((EVIDENCE / 'protocol-validation.json').read_text())
    assert validation['passed'] and validation['apk_sha256'] == sha and validation['tests'] > 200
    assert json.loads((EVIDENCE / 'build-validation.json').read_text())['apk_sha256'] == sha
    assert digest(BASE.read_bytes()) == digest(RELEASE.read_bytes()) == BASE_SHA
    for name in SOURCES:
        assert (ROOT / name).read_bytes() == (WORK / 'program' / name).read_bytes(), name
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
    report('published-release.json', dict(published=True, apk_sha256=sha, version_code=109,
        same_version_update=True, protocol_tests=validation['tests'],
        baseline_preserved=str(BASE.relative_to(ROOT)), device_test_performed=False,
        downloads=[str(RELEASE.relative_to(ROOT)), str(archive.relative_to(ROOT))]))
    print(RELEASE)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['prepare', 'verify', 'publish'])
    globals()[parser.parse_args().stage]()
