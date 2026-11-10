"""Repackage the approved November 10 changes, retaining v111 update identity."""
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
from build_offline import SIGNING_KEY, signer_certificate
from offline_android.pack_payload import build_payload, collect_files, verify_payload

WORK = ROOT / '.runtime/v111-refresh-20261110'
EVIDENCE = ROOT / 'analysis/evidence/v111-refresh-20261110'
ARCHIVE = ROOT / 'build/archive/v111-before-refresh-20261110'
NAME = '金箍棒ol离线正式版v111.apk'
BASE = ARCHIVE / NAME
BASE_SHA = '7984bdc7a676c9c5aec9c07da143b83cf0c7d9a88870a14275f684ac72dd190a'
OUTPUT = WORK / NAME


def digest(data):
    return hashlib.sha256(data).hexdigest()


def report(name, data):
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / (name + '.json')).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def source_check(check_worktree=True):
    tree = WORK / 'payload-new'
    manifest = verify_payload(tree)
    if check_worktree:
        for name, path in collect_files().items():
            if name != 'network_redirect/login.html':
                assert path.read_bytes() == (tree / name).read_bytes(), name
        from network_redirect.summon import client_source, load_rules
        assert client_source(load_rules()).encode() == (tree / 'offline_client.lua').read_bytes()
    else:
        # Preserve the approved snapshot when a parallel user task edits source.
        build = json.loads((EVIDENCE / 'build-validation.json').read_text())
        assert digest(OUTPUT.read_bytes()) == build['apk_sha256']
        for name, sha in build['source_hashes'].items():
            if name != 'network_redirect/login.html':
                assert digest((tree / name).read_bytes()) == sha, name
        with zipfile.ZipFile(OUTPUT) as apk, zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as z:
            assert all(z.read(n) == (tree / n).read_bytes() for n in z.namelist())
        subprocess.run([sys.executable, '-I', '-c',
            'import sys,pathlib;sys.path.insert(0,sys.argv[1]);'
            'from network_redirect.summon import client_source,load_rules;'
            'assert client_source(load_rules()).encode()==(pathlib.Path(sys.argv[1])/"offline_client.lua").read_bytes()',
            str(tree)], check=True)
        drift = [n for n, sha in build['source_hashes'].items()
                 if digest((ROOT / n).read_bytes()) != sha]
        report('worktree-drift', dict(apk_sha256=build['apk_sha256'],
            changed_after_snapshot=drift, action='Retain approved frozen payload; leave later user edits untouched'))
    return manifest


def build():
    assert not OUTPUT.exists(), 'Do not overwrite an existing candidate'
    original = ROOT / 'build' / NAME
    assert digest(original.read_bytes()) == BASE_SHA
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    backup = {}
    for path in sorted((ROOT / 'build').glob('*111*')):
        if not path.is_file():
            continue
        target = ARCHIVE / path.name
        if not target.exists():
            shutil.copy2(path, target)
        assert digest(target.read_bytes()) == digest(path.read_bytes()), path
        backup[path.name] = digest(target.read_bytes())
    report('original-release-backup', dict(baseline_sha256=BASE_SHA, files=backup,
                                          directory=str(ARCHIVE.relative_to(ROOT))))
    WORK.mkdir(parents=True, exist_ok=True)
    certificate = signer_certificate(BASE)
    previous = json.loads((ROOT / 'analysis/evidence/v111/build-validation.json').read_text())
    assert digest((ROOT / 'offline_android/native/offline.c').read_bytes()) == previous['native_source_sha256']
    for name, checksum in previous['java_source_sha256'].items():
        assert digest((ROOT / name).read_bytes()) == checksum, name
    manifest = build_payload(WORK / 'backend.zip')
    with zipfile.ZipFile(BASE) as base:
        with zipfile.ZipFile(io.BytesIO(base.read('assets/offline/program.zip'))) as old:
            with zipfile.ZipFile(WORK / 'backend.zip') as backend, zipfile.ZipFile(WORK / 'program.zip', 'w') as new:
                for entry in backend.infolist():
                    new.writestr(copy.copy(entry), backend.read(entry))
                for entry in old.infolist():
                    if entry.filename.startswith('client/'):
                        new.writestr(copy.copy(entry), old.read(entry))
            with zipfile.ZipFile(WORK / 'program.zip') as new:
                assert new.testzip() is None
                names = set(old.namelist()) | set(new.namelist())
                changes = sorted(n for n in names if n not in old.namelist() or
                                 n not in new.namelist() or old.read(n) != new.read(n))
                assert not any(n.startswith('client/') or 'nine_sky' in n for n in changes)
                assert not any(Path(n).suffix in ('.sqlite3', '.db', '.pyc') or
                               'save' in Path(n).parts for n in new.namelist())
                new.extractall(WORK / 'payload-new')
            old.extractall(WORK / 'payload-old')
        program = (WORK / 'program.zip').read_bytes()
        runtime_hash = digest(base.read('assets/offline/runtime.zip'))
        replacements = {'assets/offline/program.zip': program,
                        'assets/offline/build.properties':
                        f'program_sha256={digest(program)}\nruntime_sha256={runtime_hash}\nversion_code=111\n'.encode()}
        with zipfile.ZipFile(WORK / 'unsigned.apk', 'w') as new:
            for entry in base.infolist():
                if not entry.filename.startswith('META-INF/'):
                    new.writestr(copy.copy(entry), replacements.get(entry.filename, base.read(entry)))
    source_check()
    run(TOOLS / 'zipalign', '-f', '4', WORK / 'unsigned.apk', WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'sign', '--ks', SIGNING_KEY, '--ks-key-alias', 'channel360',
        '--ks-pass', 'pass:local-test-only', '--out', OUTPUT, WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'verify', '--verbose', OUTPUT)
    run(TOOLS / 'zipalign', '-c', '4', OUTPUT)
    assert signer_certificate(OUTPUT) == certificate
    badging = subprocess.check_output([str(TOOLS / 'aapt'), 'dump', 'badging', str(OUTPUT)], text=True)
    assert "versionCode='111' versionName='3.87-offline.11'" in badging
    assert badging == subprocess.check_output([str(TOOLS / 'aapt'), 'dump', 'badging', str(BASE)], text=True)
    (EVIDENCE / 'badging.txt').write_text(badging)
    with zipfile.ZipFile(BASE) as old, zipfile.ZipFile(OUTPUT) as new:
        names = lambda z: {n for n in z.namelist() if not n.startswith('META-INF/')}
        assert names(old) == names(new) and new.testzip() is None
        outer = sorted(n for n in names(old) if old.read(n) != new.read(n))
        assert set(outer) == set(replacements)
        with zipfile.ZipFile(io.BytesIO(new.read('assets/offline/program.zip'))) as payload:
            assert all(payload.read(n) == (WORK / 'payload-new' / n).read_bytes() for n in payload.namelist())
    assert digest(BASE.read_bytes()) == BASE_SHA
    source_check()
    data = dict(apk=NAME, apk_sha256=digest(OUTPUT.read_bytes()), apk_bytes=OUTPUT.stat().st_size,
                baseline=str(BASE.relative_to(ROOT)), baseline_sha256=BASE_SHA,
                version_code=111, version_name='3.87-offline.11', release_revision='2026-11-10',
                certificate_sha256=certificate, program_sha256=digest(program), runtime_sha256=runtime_hash,
                payload_bundle_id=manifest['bundle_id'], payload_files=len(manifest['files']),
                changed_program_entries=changes, changed_apk_entries=outer,
                original_engine_client_runtime_native_java_preserved=True,
                contains_player_database=False, player_database='files/save/game.sqlite3',
                source_hashes={str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in collect_files().values()})
    report('build-validation', data)
    OUTPUT.with_suffix('.manifest.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    OUTPUT.with_suffix('.apk.sha256').write_text(data['apk_sha256'] + '  ' + NAME + '\n')
    print(json.dumps({k: data[k] for k in ('apk_sha256', 'apk_bytes', 'changed_program_entries')}, ensure_ascii=False))


if __name__ == '__main__':
    build()
