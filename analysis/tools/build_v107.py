"""Build v107 from the preserved official v106, retaining its identity and save path."""
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from build_channel360 import TOOLS, apktool, run
from build_offline import PACKAGE, SIGNING_KEY, signer_certificate
from offline_android.pack_payload import build_payload, verify_payload

BASE = ROOT / 'build/金箍棒3.87离线正式版v106.apk'
OUTPUT = ROOT / '.runtime/v107-build/金箍棒3.87离线正式版v107.apk'
WORK = ROOT / '.runtime/v107-build'
EVIDENCE = ROOT / 'analysis/evidence/v107'
VERSION_NAME = '3.87-offline.7'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def badging(apk):
    return subprocess.check_output([str(TOOLS / 'aapt'), 'dump', 'badging', str(apk)], text=True)


def build(base_version=106, native_adapter=None):
    if OUTPUT.exists():
        raise ValueError('Refusing to overwrite the existing v107 candidate APK')
    WORK.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    certificate = signer_certificate(BASE)
    baseline_metadata = badging(BASE)
    assert base_version == 106
    assert digest(BASE.read_bytes()) == '140d850a791267cfcdae725b5cd9e650cfb3fffff894759bb024ff17cf5ed494'
    assert f"package: name='{PACKAGE}' versionCode='{base_version}'" in baseline_metadata
    baseline_hash = digest(BASE.read_bytes())
    payload = build_payload(WORK / 'backend.zip')
    program = WORK / 'program.zip'
    with zipfile.ZipFile(BASE) as base:
        previous_bytes = base.read('assets/offline/program.zip')
        runtime_hash = digest(base.read('assets/offline/runtime.zip'))
        assert 'runtime_sha256=' + runtime_hash in base.read('assets/offline/build.properties').decode()
        with zipfile.ZipFile(io.BytesIO(previous_bytes)) as previous, \
                zipfile.ZipFile(WORK / 'backend.zip') as backend, zipfile.ZipFile(program, 'w') as new:
            for entry in backend.infolist():
                new.writestr(entry, backend.read(entry))
            # Preserve exactly the client assets shipped in the baseline v106.
            for entry in previous.infolist():
                if entry.filename.startswith('client/'):
                    new.writestr(entry, previous.read(entry))
    with zipfile.ZipFile(program) as new, zipfile.ZipFile(io.BytesIO(previous_bytes)) as previous:
        assert new.testzip() is None
        assert not any(Path(n).suffix in ('.db', '.sqlite3', '.pyc') or
                       'save' in Path(n).parts for n in new.namelist())
        changed_program = sorted(n for n in set(previous.namelist()) | set(new.namelist())
            if n not in previous.namelist() or n not in new.namelist() or previous.read(n) != new.read(n))
        assert not any(n.startswith('client/') for n in changed_program)
        new.extractall(WORK / 'program')
    assert verify_payload(WORK / 'program')['bundle_id'] == payload['bundle_id']
    # Compile only the manifest; preserve every other original APK entry.
    if base_version == 106:
        decoded = WORK / 'decoded'
        framework = ROOT / '.runtime/tools/apktool-framework'
        apktool('d', '-f', '-s', '-p', framework, '-o', decoded, BASE)
        metadata = decoded / 'apktool.yml'
        content = metadata.read_text()
        for name, value in (('versionCode', '107'), ('versionName', VERSION_NAME)):
            content, count = re.subn(r'(?m)^  ' + name + r':.*$', '  ' + name + ': ' + value, content)
            assert count == 1, name
        metadata.write_text(content)
        shell = WORK / 'manifest-shell.apk'
        apktool('b', '-p', framework, '-o', shell, decoded)
    program_hash = digest(program.read_bytes())
    replacements = {
        'assets/offline/program.zip': program.read_bytes(),
        'assets/offline/build.properties':
            f'program_sha256={program_hash}\nruntime_sha256={runtime_hash}\nversion_code=107\n'.encode(),
    }
    if native_adapter is not None:
        replacements['lib/armeabi-v7a/liboffline.so'] = Path(native_adapter).read_bytes()
    if base_version == 106:
        with zipfile.ZipFile(shell) as compiled:
            replacements['AndroidManifest.xml'] = compiled.read('AndroidManifest.xml')
    with zipfile.ZipFile(BASE) as base, zipfile.ZipFile(WORK / 'unsigned.apk', 'w') as new:
        for entry in base.infolist():
            if not entry.filename.startswith('META-INF/'):
                new.writestr(entry, replacements.get(entry.filename, base.read(entry)))
    run(TOOLS / 'zipalign', '-f', '4', WORK / 'unsigned.apk', WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'sign', '--ks', SIGNING_KEY, '--ks-key-alias', 'channel360',
        '--ks-pass', 'pass:local-test-only', '--out', OUTPUT, WORK / 'aligned.apk')
    assert signer_certificate(OUTPUT) == certificate
    run(TOOLS / 'apksigner', 'verify', '--verbose', OUTPUT)
    run(TOOLS / 'zipalign', '-c', '4', OUTPUT)
    result_metadata = badging(OUTPUT)
    assert f"package: name='{PACKAGE}' versionCode='107' versionName='{VERSION_NAME}'" in result_metadata
    def without_versions(text):
        return re.sub(r"version(?:Code|Name)='[^']*'", '', text)
    assert without_versions(baseline_metadata) == without_versions(result_metadata)
    with zipfile.ZipFile(BASE) as base, zipfile.ZipFile(OUTPUT) as new:
        assert new.testzip() is None
        names = lambda z: {n for n in z.namelist() if not n.startswith('META-INF/')}
        assert names(base) == names(new)
        changed = sorted(n for n in names(base) if base.read(n) != new.read(n))
        assert set(changed) == set(replacements), changed
    assert digest(BASE.read_bytes()) == baseline_hash
    report = dict(release_revision='v107-fourteen-updates-20261031', feature_groups=14, home_version_label='v107', version_code=107, version_name=VERSION_NAME, package=PACKAGE,
        apk=OUTPUT.name, apk_sha256=digest(OUTPUT.read_bytes()), apk_bytes=OUTPUT.stat().st_size,
        baseline=BASE.name, baseline_sha256=baseline_hash, certificate_sha256=certificate,
        program_sha256=program_hash, runtime_sha256=runtime_hash, payload_bundle_id=payload['bundle_id'],
        payload_files=len(payload['files']), changed_apk_entries=changed,
        changed_program_entries=changed_program, player_database='files/save/game.sqlite3',
        contains_player_database=False,
        original_game_java_native_runtime_video_unchanged=native_adapter is None,
        original_game_engine_unchanged=True, offline_native_adapter_updated=native_adapter is not None,
        baseline_preserved=True)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    OUTPUT.with_suffix('.manifest.json').write_text(rendered)
    OUTPUT.with_suffix('.apk.sha256').write_text(report['apk_sha256'] + '  ' + OUTPUT.name + '\n')
    (EVIDENCE / 'build-validation.json').write_text(rendered)
    (EVIDENCE / 'badging.txt').write_text(result_metadata)
    print(rendered)


if __name__ == '__main__':
    build()
