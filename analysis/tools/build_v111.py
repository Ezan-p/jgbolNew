"""Build v111 on official v110, with byte-identical Nine Sky rules and assets."""
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
from build_channel360 import JAVA, TOOLS, apktool, run
from build_offline import PACKAGE, SIGNING_KEY, signer_certificate
from offline_android.pack_payload import build_payload, collect_files, verify_payload
from offline_android.native.build_native import build as build_native

BASE = ROOT / 'build/金箍棒ol离线正式版v110.apk'
BASE_SHA = '4f98c0ab98a574886b2b771a9ad82ace2bdcfaf6de89a389c3770cb078432375'
WORK = ROOT / '.runtime/v111-release'
EVIDENCE = ROOT / 'analysis/evidence/v111'
OUTPUT = WORK / '金箍棒ol离线正式版v111.apk'
VERSION_NAME = '3.87-offline.11'
NINE_SKY = ('network_redirect/activity_nine_sky.py', 'network_redirect/nine_sky_battle.py',
            'network_redirect/nine_sky_client.lua', 'server_config/nine_sky_rules.json')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def report(name, data):
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / (name + '.json')).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def source_check():
    tree = WORK / 'payload-new'
    verify_payload(tree)
    for name, path in collect_files().items():
        if name != 'network_redirect/login.html':
            assert path.read_bytes() == (tree / name).read_bytes(), name
    from network_redirect.summon import client_source, load_rules
    assert client_source(load_rules()).encode() == (tree / 'offline_client.lua').read_bytes()


def build():
    assert not OUTPUT.exists(), 'Refusing to overwrite a built candidate'
    assert digest(BASE.read_bytes()) == BASE_SHA
    WORK.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    certificate = signer_certificate(BASE)
    with zipfile.ZipFile(BASE) as baseline:
        old_program = baseline.read('assets/offline/program.zip')
        runtime_hash = digest(baseline.read('assets/offline/runtime.zip'))
        with zipfile.ZipFile(io.BytesIO(old_program)) as old:
            # Stop rather than accidentally shipping excluded Nine Sky changes.
            for name in NINE_SKY:
                assert old.read(name) == (ROOT / name).read_bytes(), name
            previous_rules = json.loads(old.read('server_config/activity_rules.json'))
            current_rules = json.loads((ROOT / 'server_config/activity_rules.json').read_text())
            for key in previous_rules.keys() | current_rules.keys():
                if previous_rules.get(key) != current_rules.get(key):
                    assert key.startswith(('abyss_', 'land_')), key
    payload = build_payload(WORK / 'backend.zip')
    with zipfile.ZipFile(io.BytesIO(old_program)) as old, \
            zipfile.ZipFile(WORK / 'backend.zip') as backend, \
            zipfile.ZipFile(WORK / 'program.zip', 'w') as new:
        for entry in backend.infolist():
            new.writestr(entry, backend.read(entry))
        for entry in old.infolist():
            if entry.filename.startswith('client/'):
                new.writestr(entry, old.read(entry))
    program = (WORK / 'program.zip').read_bytes()
    with zipfile.ZipFile(io.BytesIO(old_program)) as old, zipfile.ZipFile(io.BytesIO(program)) as new:
        assert new.testzip() is None
        changes = sorted(n for n in set(old.namelist()) | set(new.namelist())
                         if n not in old.namelist() or n not in new.namelist() or old.read(n) != new.read(n))
        assert not any(n.startswith('client/') or 'nine_sky' in n for n in changes)
        assert not any(Path(n).suffix in ('.db', '.sqlite3', '.pyc') or 'save' in Path(n).parts
                       for n in new.namelist())
        new.extractall(WORK / 'payload-new')
    source_check()
    decoded = WORK / 'decoded'
    framework = ROOT / '.runtime/tools/apktool-framework'
    apktool('d', '-f', '-s', '-p', framework, '-o', decoded, BASE)
    metadata = decoded / 'apktool.yml'
    content = metadata.read_text()
    for name, value in (('versionCode', '111'), ('versionName', VERSION_NAME)):
        content, count = re.subn(r'(?m)^  ' + name + r':.*$', '  ' + name + ': ' + value, content)
        assert count == 1
    metadata.write_text(content)
    shell = WORK / 'manifest-shell.apk'
    apktool('b', '-p', framework, '-o', shell, decoded)
    native_source_hash = digest((ROOT / 'offline_android/native/offline.c').read_bytes())
    native = build_native(WORK / 'liboffline.so')
    assert digest((ROOT / 'offline_android/native/offline.c').read_bytes()) == native_source_hash
    classes, dex = WORK / 'classes', WORK / 'dex'
    classes.mkdir(exist_ok=True)
    dex.mkdir(exist_ok=True)
    java_sources = sorted((ROOT / 'offline_android/java').rglob('*.java'))
    java_hashes = {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in java_sources}
    android = ROOT / '.runtime/offline-toolchain/android.jar'
    run(JAVA / 'bin/javac', '-source', '8', '-target', '8', '-classpath', android, '-d', classes, *java_sources)
    run(TOOLS / 'd8', '--min-api', '21', '--lib', android, '--output', dex, *sorted(classes.rglob('*.class')))
    with zipfile.ZipFile(shell) as compiled:
        manifest = compiled.read('AndroidManifest.xml')
    replacements = {
        'AndroidManifest.xml': manifest,
        'assets/offline/program.zip': program,
        'assets/offline/build.properties':
            f'program_sha256={digest(program)}\nruntime_sha256={runtime_hash}\nversion_code=111\n'.encode(),
        'lib/armeabi-v7a/liboffline.so': native.read_bytes(),
        'classes2.dex': (dex / 'classes.dex').read_bytes(),
    }
    with zipfile.ZipFile(BASE) as old, zipfile.ZipFile(WORK / 'unsigned.apk', 'w') as new:
        for entry in old.infolist():
            if not entry.filename.startswith('META-INF/'):
                new.writestr(entry, replacements.get(entry.filename, old.read(entry)))
    run(TOOLS / 'zipalign', '-f', '4', WORK / 'unsigned.apk', WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'sign', '--ks', SIGNING_KEY, '--ks-key-alias', 'channel360',
        '--ks-pass', 'pass:local-test-only', '--out', OUTPUT, WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'verify', '--verbose', OUTPUT)
    run(TOOLS / 'zipalign', '-c', '4', OUTPUT)
    assert signer_certificate(OUTPUT) == certificate
    badging = lambda p: subprocess.check_output([str(TOOLS / 'aapt'), 'dump', 'badging', str(p)], text=True)
    info = badging(OUTPUT)
    assert f"package: name='{PACKAGE}' versionCode='111' versionName='{VERSION_NAME}'" in info
    strip = lambda s: re.sub(r"version(?:Code|Name)='[^']*'", '', s)
    assert strip(info) == strip(badging(BASE))
    (EVIDENCE / 'badging.txt').write_text(info)
    with zipfile.ZipFile(BASE) as old, zipfile.ZipFile(OUTPUT) as new:
        assert new.testzip() is None
        names = lambda z: {n for n in z.namelist() if not n.startswith('META-INF/')}
        assert names(old) == names(new)
        outer_changes = sorted(n for n in names(old) if old.read(n) != new.read(n))
        assert set(outer_changes) <= set(replacements)
        assert {'AndroidManifest.xml', 'assets/offline/program.zip', 'assets/offline/build.properties',
                'lib/armeabi-v7a/liboffline.so'} <= set(outer_changes)
    assert digest(BASE.read_bytes()) == BASE_SHA
    assert all(digest((ROOT / n).read_bytes()) == h for n, h in java_hashes.items())
    source_check()
    result = dict(apk=OUTPUT.name, apk_sha256=digest(OUTPUT.read_bytes()), apk_bytes=OUTPUT.stat().st_size,
                  version_code=111, version_name=VERSION_NAME, home_version_label='v111', package=PACKAGE,
                  baseline=str(BASE.relative_to(ROOT)), baseline_sha256=BASE_SHA,
                  certificate_sha256=certificate, program_sha256=digest(program), runtime_sha256=runtime_hash,
                  payload_bundle_id=payload['bundle_id'], payload_files=len(payload['files']),
                  changed_program_entries=changes, changed_apk_entries=outer_changes,
                  nine_sky_unchanged=list(NINE_SKY), native_source_sha256=native_source_hash,
                  native_adapter_sha256=digest(native.read_bytes()), java_source_sha256=java_hashes,
                  contains_player_database=False, player_database='files/save/game.sqlite3',
                  original_engine_and_client_assets_preserved=True, device_tested=False, physical_device_tested=False)
    report('build-validation', result)
    OUTPUT.with_suffix('.manifest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    OUTPUT.with_suffix('.apk.sha256').write_text(result['apk_sha256'] + '  ' + OUTPUT.name + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    build()
