"""Append the three Taixu updates to the released formal v112, preserving its shell."""
import copy
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
from build_offline import PACKAGE, SIGNING_KEY, signer_certificate
from offline_android.pack_payload import collect_files, verify_payload

WORK = ROOT / '.runtime/v112-taixu-20261113'
EVIDENCE = ROOT / 'analysis/evidence/v112-taixu-20261113'
BASE = ROOT / '.runtime/v112-release-20261113/金箍棒ol离线正式版v112.apk'
BASE_SHA = '1f77439d339e671d0cd5e147d5ed304ba5335e430215e55c5302c02d0759c53a'
OUTPUT = WORK / '金箍棒ol离线正式版v112-三项更新-20261113.apk'
VERSION_NAME = '3.87-offline.12'
FEATURE_GROUPS = 12
APPENDED_FEATURE_GROUPS = 3
RELEASE_REVISION = '2026-11-13-formal-v112-taixu'
CHANGES = {'network_redirect/activity.py', 'network_redirect/activity_arena.py',
           'network_redirect/taixu_client.lua', 'server_config/activity_rules.json',
           'server_config/taixu_rules.json'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def report(name, data):
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / (name + '.json')).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def build():
    assert not OUTPUT.exists(), 'Candidate already exists'
    assert digest(BASE.read_bytes()) == BASE_SHA
    WORK.mkdir(parents=True, exist_ok=True)
    snapshot = WORK / 'source'
    hashes = {}
    for name, path in collect_files(ROOT).items():
        target = snapshot / name
        target.parent.mkdir(parents=True, exist_ok=True)
        data = path.read_bytes()
        target.write_bytes(data)
        hashes[name] = digest(data)
    report('source-snapshot', dict(source_hashes=hashes))
    subprocess.run([sys.executable, '-I', '-c',
        'import sys;sys.path.insert(0,sys.argv[1]);'
        'from offline_android.pack_payload import build_payload;'
        'build_payload(sys.argv[3],root=sys.argv[2])',
        str(ROOT), str(snapshot), str(WORK / 'backend.zip')], check=True)
    with zipfile.ZipFile(BASE) as base, \
            zipfile.ZipFile(io.BytesIO(base.read('assets/offline/program.zip'))) as old, \
            zipfile.ZipFile(WORK / 'backend.zip') as backend, \
            zipfile.ZipFile(WORK / 'program.zip', 'w') as new:
        old.extractall(WORK / 'payload-baseline')
        for entry in backend.infolist():
            new.writestr(entry, backend.read(entry))
        for entry in old.infolist():
            if entry.filename.startswith('client/'):
                new.writestr(entry, old.read(entry))
        runtime_hash = digest(base.read('assets/offline/runtime.zip'))
    program = (WORK / 'program.zip').read_bytes()
    replacements = {
        'assets/offline/program.zip': program,
        'assets/offline/build.properties':
            f'program_sha256={digest(program)}\nruntime_sha256={runtime_hash}\nversion_code=112\n'.encode(),
    }
    with zipfile.ZipFile(BASE) as old, zipfile.ZipFile(WORK / 'unsigned.apk', 'w') as new:
        for entry in old.infolist():
            if not entry.filename.startswith('META-INF/'):
                new.writestr(copy.copy(entry), replacements.get(entry.filename, old.read(entry)))
    run(TOOLS / 'zipalign', '-f', '4', WORK / 'unsigned.apk', WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'sign', '--ks', SIGNING_KEY, '--ks-key-alias', 'channel360',
        '--ks-pass', 'pass:local-test-only', '--out', OUTPUT, WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'verify', '--verbose', OUTPUT)
    run(TOOLS / 'zipalign', '-c', '4', OUTPUT)
    assert signer_certificate(OUTPUT) == signer_certificate(BASE)
    badging = subprocess.check_output([str(TOOLS / 'aapt'), 'dump', 'badging', str(OUTPUT)], text=True)
    assert f"package: name='{PACKAGE}' versionCode='112' versionName='{VERSION_NAME}'" in badging
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / 'badging.txt').write_text(badging)
    with zipfile.ZipFile(OUTPUT) as apk, zipfile.ZipFile(BASE) as base, \
            zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as new, \
            zipfile.ZipFile(io.BytesIO(base.read('assets/offline/program.zip'))) as old:
        assert apk.testzip() is None and new.testzip() is None
        names = lambda z: {n for n in z.namelist() if not n.startswith('META-INF/')}
        assert names(apk) == names(base)
        outer = sorted(n for n in names(apk) if apk.read(n) != base.read(n))
        assert set(outer) == set(replacements), outer
        changes = sorted(n for n in set(new.namelist()) | set(old.namelist())
            if n not in new.namelist() or n not in old.namelist() or new.read(n) != old.read(n))
        assert set(changes) == CHANGES | {'offline_client.lua', 'payload-manifest.json'}, changes
        assert not any(Path(n).suffix in ('.sqlite3', '.db', '.pyc') or 'save' in Path(n).parts
                       or n.startswith('offline_android/test_edition') for n in new.namelist())
        new.extractall(WORK / 'payload-new')
    payload = verify_payload(WORK / 'payload-new')
    assert payload['player_database'] == 'files/save/game.sqlite3' and payload['loopback_port'] == 18770
    for name, sha in hashes.items():
        if name != 'network_redirect/login.html':
            assert digest((WORK / 'payload-new' / name).read_bytes()) == sha, name
    # Historical v111 payload for the existing v111 -> v112 save migration check.
    (WORK / 'payload-old').symlink_to(ROOT / '.runtime/v112-release-20261113/payload-old', target_is_directory=True)
    shutil.copytree(ROOT / 'tests', WORK / 'tests', ignore=shutil.ignore_patterns('__pycache__'))
    report('test-snapshot', dict(files={str(p.relative_to(WORK / 'tests')): digest(p.read_bytes())
        for p in (WORK / 'tests').rglob('*') if p.is_file()}))
    data = dict(apk_sha256=digest(OUTPUT.read_bytes()), apk_bytes=OUTPUT.stat().st_size,
        version_code=112, version_name=VERSION_NAME, home_version_label='v112', package=PACKAGE,
        baseline=str(BASE.relative_to(ROOT)), baseline_sha256=BASE_SHA,
        certificate_sha256=signer_certificate(OUTPUT), program_sha256=digest(program),
        runtime_sha256=runtime_hash, payload_bundle_id=payload['bundle_id'],
        payload_files=len(payload['files']), changed_apk_entries_from_v112=outer,
        changed_program_entries_from_v112=changes, source_hashes=hashes,
        contains_player_database=False, contains_test_supply=False,
        player_database=payload['player_database'], engine_client_runtime_native_java_preserved=True,
        feature_groups=FEATURE_GROUPS, appended_feature_groups=APPENDED_FEATURE_GROUPS,
        release_revision=RELEASE_REVISION)
    report('build-validation', data)
    OUTPUT.with_suffix('.manifest.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    OUTPUT.with_suffix('.apk.sha256').write_text(data['apk_sha256'] + '  ' + OUTPUT.name + '\n')
    assert digest(BASE.read_bytes()) == BASE_SHA
    print(json.dumps({k: data[k] for k in ('apk_sha256', 'apk_bytes', 'changed_program_entries_from_v112')}, ensure_ascii=False))


if __name__ == '__main__':
    build()
