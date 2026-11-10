"""Freeze current gameplay and ship it under the explicitly requested v110 identity."""
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

WORK = ROOT / '.runtime/v110-refresh-20261110'
EVIDENCE = ROOT / 'analysis/evidence/v110-refresh-20261110'
BASE = ROOT / 'build/金箍棒ol离线正式版v110.apk'
LATEST = ROOT / 'build/金箍棒ol离线正式版v111.apk'
OUTPUT = WORK / BASE.name
ARCHIVE = ROOT / 'build/archive/v110-before-refresh-20261110'
BASE_SHA = '4f98c0ab98a574886b2b771a9ad82ace2bdcfaf6de89a389c3770cb078432375'
LATEST_SHA = '73db499548a76eb6250c412cf2e341b3808616a52dedd62f6598e5711bf659a9'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def report(name, data):
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / (name + '.json')).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def build():
    assert not OUTPUT.exists(), 'Candidate already exists; do not overwrite verified bytes'
    assert digest(BASE.read_bytes()) == BASE_SHA
    assert digest(LATEST.read_bytes()) == LATEST_SHA
    WORK.mkdir(parents=True, exist_ok=True)
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    backups = {}
    for p in sorted((ROOT / 'build').glob('*110*')):
        if not p.is_file() or '测试' in p.name:
            continue
        target = ARCHIVE / p.name
        if not target.exists():
            shutil.copy2(p, target)
        assert digest(target.read_bytes()) == digest(p.read_bytes())
        backups[p.name] = digest(p.read_bytes())
    report('original-release-backup', dict(directory=str(ARCHIVE.relative_to(ROOT)), files=backups))
    snapshot = WORK / 'source'
    hashes = {}
    for name, path in collect_files().items():
        target = snapshot / name
        target.parent.mkdir(parents=True, exist_ok=True)
        data = path.read_bytes()
        hashes[name] = digest(data)
        if name == 'network_redirect/login_branding_client.lua':
            assert data.count(b"label('v111',0.75)") == 1
            data = data.replace(b"label('v111',0.75)", b"label('v110',0.75)")
        target.write_bytes(data)
    report('source-snapshot', dict(source_hashes=hashes,
        version_override='Only snapshot login_branding_client.lua: v111 -> v110'))
    # A fresh interpreter prevents importing gameplay from the working tree.
    code = ('import sys;sys.path.insert(0,sys.argv[1]);'
            'from offline_android.pack_payload import build_payload;'
            'build_payload(sys.argv[3],root=sys.argv[2])')
    subprocess.run([sys.executable, '-I', '-c', code, str(ROOT), str(snapshot),
                    str(WORK / 'backend.zip')], check=True)
    with zipfile.ZipFile(LATEST) as latest, zipfile.ZipFile(BASE) as base:
        assert signer_certificate(BASE) == signer_certificate(LATEST)
        with zipfile.ZipFile(io.BytesIO(latest.read('assets/offline/program.zip'))) as old, \
                zipfile.ZipFile(WORK / 'backend.zip') as backend, \
                zipfile.ZipFile(WORK / 'program.zip', 'w') as new:
            for entry in backend.infolist():
                new.writestr(entry, backend.read(entry))
            for entry in old.infolist():
                if entry.filename.startswith('client/'):
                    new.writestr(entry, old.read(entry))
        program = (WORK / 'program.zip').read_bytes()
        runtime_hash = digest(latest.read('assets/offline/runtime.zip'))
        replacements = {
            'AndroidManifest.xml': base.read('AndroidManifest.xml'),
            'assets/offline/program.zip': program,
            'assets/offline/build.properties':
                f'program_sha256={digest(program)}\nruntime_sha256={runtime_hash}\nversion_code=110\n'.encode(),
        }
        with zipfile.ZipFile(WORK / 'unsigned.apk', 'w') as new:
            for entry in latest.infolist():
                if not entry.filename.startswith('META-INF/'):
                    new.writestr(entry, replacements.get(entry.filename, latest.read(entry)))
    run(TOOLS / 'zipalign', '-f', '4', WORK / 'unsigned.apk', WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'sign', '--ks', SIGNING_KEY, '--ks-key-alias', 'channel360',
        '--ks-pass', 'pass:local-test-only', '--out', OUTPUT, WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'verify', '--verbose', OUTPUT)
    run(TOOLS / 'zipalign', '-c', '4', OUTPUT)
    assert signer_certificate(OUTPUT) == signer_certificate(BASE)
    badging = subprocess.check_output([str(TOOLS / 'aapt'), 'dump', 'badging', str(OUTPUT)], text=True)
    assert f"package: name='{PACKAGE}' versionCode='110' versionName='3.87-offline.10'" in badging
    assert badging == subprocess.check_output([str(TOOLS / 'aapt'), 'dump', 'badging', str(BASE)], text=True)
    (EVIDENCE / 'badging.txt').write_text(badging)
    with zipfile.ZipFile(OUTPUT) as apk, zipfile.ZipFile(LATEST) as latest, \
            zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as payload, \
            zipfile.ZipFile(io.BytesIO(latest.read('assets/offline/program.zip'))) as old:
        assert apk.testzip() is None and payload.testzip() is None
        names = lambda z: {n for n in z.namelist() if not n.startswith('META-INF/')}
        assert names(apk) == names(latest)
        outer = sorted(n for n in names(apk) if apk.read(n) != latest.read(n))
        assert set(outer) == set(replacements)
        assert not any(Path(n).suffix in ('.sqlite3', '.db', '.pyc') or 'save' in Path(n).parts
                       for n in payload.namelist())
        changed = sorted(n for n in set(old.namelist()) | set(payload.namelist())
                         if n not in old.namelist() or n not in payload.namelist()
                         or old.read(n) != payload.read(n))
        assert not any(n.startswith('client/') for n in changed)
        payload.extractall(WORK / 'payload-new')
    manifest = verify_payload(WORK / 'payload-new')
    for name in hashes:
        if name != 'network_redirect/login.html':
            assert (snapshot / name).read_bytes() == (WORK / 'payload-new' / name).read_bytes(), name
    assert digest(BASE.read_bytes()) == BASE_SHA and digest(LATEST.read_bytes()) == LATEST_SHA
    data = dict(apk_sha256=digest(OUTPUT.read_bytes()), apk_bytes=OUTPUT.stat().st_size,
        version_code=110, version_name='3.87-offline.10', home_version_label='v110', package=PACKAGE,
        baseline=str(BASE.relative_to(ROOT)), baseline_sha256=BASE_SHA,
        content_baseline=str(LATEST.relative_to(ROOT)), content_baseline_sha256=LATEST_SHA,
        certificate_sha256=signer_certificate(OUTPUT), program_sha256=digest(program),
        runtime_sha256=runtime_hash, payload_bundle_id=manifest['bundle_id'],
        payload_files=len(manifest['files']), changed_apk_entries_from_v111=outer,
        changed_program_entries_from_v111=changed, source_hashes=hashes,
        contains_player_database=False, player_database='files/save/game.sqlite3',
        engine_client_runtime_native_java_preserved_from_latest_v111=True,
        feature_groups=10, release_revision='2026-11-10-ten-updates-v110')
    report('build-validation', data)
    OUTPUT.with_suffix('.manifest.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    OUTPUT.with_suffix('.apk.sha256').write_text(data['apk_sha256']+'  '+OUTPUT.name+'\n')
    print(json.dumps({k:data[k] for k in ('apk_sha256','apk_bytes','changed_program_entries_from_v111')}, ensure_ascii=False))


if __name__ == '__main__':
    build()
