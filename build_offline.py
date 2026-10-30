"""Build the self-contained ARMv7 game; never read or bundle player databases.

Run with .runtime/venv/bin/python build_offline.py. Requires the preserved local
APK, fixed signing key, Android build tools and prepared offline-toolchain.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
import zipfile

from build_channel360 import JAVA, TOOLS, apktool, run
from offline_android.pack_payload import build_payload

ROOT = Path(__file__).resolve().parent
WORK = ROOT / '.runtime/offline-build'
TOOLCHAIN = ROOT / '.runtime/offline-toolchain'
PACKAGE = 'com.sygame.jingubang.p360'
CERTIFICATE = 'de10334b708a60c1edabcfa76b0115991f2554d19a475c23662120e723080c1e'
SIGNING_KEY = ROOT / '.runtime/channel360/local-test.p12'
BASELINE = ROOT / 'build/jgbol3.87-local.apk'
ANDROID = '{http://schemas.android.com/apk/res/android}'


def digest(path):
    result = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(chunk)
    return result.hexdigest()


def put(archive, name, data, compressed=True):
    info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
    info.external_attr = 0o100600 << 16
    archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED if compressed else zipfile.ZIP_STORED)


def signer_certificate(apk):
    output = subprocess.check_output([str(TOOLS / 'apksigner'), 'verify', '--print-certs', str(apk)],
                                     env={**os.environ, 'JAVA_HOME': str(JAVA)}, text=True)
    match = re.search(r'certificate SHA-256 digest: ([0-9a-f]+)', output)
    if not match or match[1] != CERTIFICATE:
        raise RuntimeError('APK certificate does not match the fixed update identity')
    return match[1]


def program_bundle():
    backend_zip = WORK / 'backend.zip'
    payload = build_payload(backend_zip)
    overlay = TOOLCHAIN / 'device-release_w'
    evidence = TOOLCHAIN / 'device-release_w-sha256.json'
    if not overlay.is_dir() or not evidence.is_file():
        raise RuntimeError('Missing verified current client release_w snapshot')
    expected_overlay = json.loads(evidence.read_text())
    actual_overlay = {path.relative_to(overlay).as_posix(): digest(path)
                      for path in overlay.rglob('*') if path.is_file() and path.name != '.DS_Store'}
    if actual_overlay != expected_overlay:
        raise RuntimeError('Client resource snapshot no longer matches its frozen SHA256 inventory')
    output = WORK / 'program.zip'
    overlay_files = []
    with zipfile.ZipFile(backend_zip) as source, zipfile.ZipFile(output, 'w') as dest:
        for name in source.namelist():
            put(dest, name, source.read(name))
        for path in sorted(overlay.rglob('*')):
            if path.is_file() and path.name != '.DS_Store':
                relative = path.relative_to(overlay).as_posix()
                if relative.endswith(('.sqlite3', '.db')):
                    raise RuntimeError('Unexpected database in client resource snapshot')
                put(dest, 'client/release_w/' + relative, path.read_bytes())
                overlay_files.append(dict(path=relative, sha256=digest(path), size=path.stat().st_size))
        put(dest, 'client/overlay-manifest.json', json.dumps(overlay_files, indent=2).encode())
    return output, payload, overlay_files


def runtime_bundle():
    output = WORK / 'runtime.zip'
    with zipfile.ZipFile(output, 'w') as archive:
        put(archive, 'stdlib.zip', (TOOLCHAIN / 'target-3.11.0-2-stdlib.zip').read_bytes(), False)
        modules = TOOLCHAIN / 'python-arm32/lib-dynload/armeabi-v7a'
        if not modules.is_dir():
            raise RuntimeError('Missing ARM32 Python extension modules')
        for path in sorted(modules.iterdir()):
            if path.is_file():
                put(archive, 'modules/' + path.name, path.read_bytes())
    return output


def build(output=None, version_code=105, reuse_decode=False):
    output = Path(output or ROOT / f'build/金箍棒3.87-离线单机-arm32-v{version_code}.apk').resolve()
    WORK.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    if not SIGNING_KEY.is_file():
        raise RuntimeError('Fixed signing key missing; refusing to generate a new incompatible key')
    signer_certificate(BASELINE)
    from offline_android.native.build_python_bridge import build as build_python
    from offline_android.native.build_native import build as build_native
    python_bridge = build_python()
    native = build_native()
    program, payload, overlay = program_bundle()
    runtime = runtime_bundle()
    decoded = WORK / 'decoded'
    if not reuse_decode or not decoded.is_dir():
        apktool('d', '-f', '-p', ROOT / '.runtime/tools/apktool-framework', '-o', decoded, BASELINE)
    manifest = decoded / 'AndroidManifest.xml'
    ET.register_namespace('android', ANDROID[1:-1])
    tree = ET.parse(manifest)
    root = tree.getroot()
    if root.get('package') != PACKAGE:
        raise RuntimeError('Unexpected baseline package name')
    root.set(ANDROID + 'installLocation', 'internalOnly')
    app = root.find('application')
    app.set(ANDROID + 'name', 'com.jgbol.offline.OfflineApplication')
    app.set(ANDROID + 'allowBackup', 'false')
    app.set(ANDROID + 'extractNativeLibs', 'true')
    for activity in list(app.findall('activity')):
        if activity.get(ANDROID + 'name') == 'com.jgbol.offline.LauncherActivity':
            app.remove(activity)
            continue
        for item in list(activity.findall('intent-filter')):
            if any(action.get(ANDROID + 'name') == 'android.intent.action.MAIN' for action in item.findall('action')):
                activity.remove(item)
        activity.set(ANDROID + 'exported', 'false')
    launcher = ET.SubElement(app, 'activity', {
        ANDROID + 'name': 'com.jgbol.offline.LauncherActivity', ANDROID + 'exported': 'true',
        ANDROID + 'screenOrientation': 'landscape',
        ANDROID + 'theme': '@android:style/Theme.NoTitleBar.Fullscreen',
        ANDROID + 'configChanges': 'keyboardHidden|orientation|screenSize'})
    intent = ET.SubElement(launcher, 'intent-filter')
    ET.SubElement(intent, 'action', {ANDROID + 'name': 'android.intent.action.MAIN'})
    ET.SubElement(intent, 'category', {ANDROID + 'name': 'android.intent.category.LAUNCHER'})
    tree.write(manifest, encoding='utf-8', xml_declaration=True)
    meta = decoded / 'apktool.yml'
    text = meta.read_text()
    for name, value in [('minSdkVersion', '21'), ('targetSdkVersion', '22'),
                        ('versionCode', str(version_code)), ('versionName', '3.87-offline.5-new-role-opening')]:
        text, count = re.subn(r'(?m)^(  ' + name + r':).*$', r'\g<1> ' + value, text)
        if count != 1:
            raise RuntimeError('Missing APK metadata: ' + name)
    meta.write_text(text)
    from offline_android.patch_lifecycle import patch as patch_lifecycle
    patch_lifecycle(decoded)
    from offline_android.patch_opening import patch as patch_opening
    patch_opening(decoded)
    label = decoded / 'res/values/strings.xml'
    text = label.read_text()
    text = re.sub(r'(<string name="app_name">).*?(</string>)', r'\g<1>金箍棒·离线单机\2', text)
    label.write_text(text)
    assets = decoded / 'assets/offline'
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copy2(program, assets / 'program.zip')
    shutil.copy2(runtime, assets / 'runtime.zip')
    shutil.copy2(ROOT / 'offline_android/THIRD_PARTY_NOTICES', assets / 'THIRD_PARTY_NOTICES')
    (assets / 'build.properties').write_text(
        f'program_sha256={digest(program)}\nruntime_sha256={digest(runtime)}\nversion_code={version_code}\n')
    libs = decoded / 'lib'
    shutil.rmtree(libs)
    abi = libs / 'armeabi-v7a'
    abi.mkdir(parents=True)
    with zipfile.ZipFile(BASELINE) as source:
        for name in ('libxiyoujilua.so', 'libpocketsphinx_jni.so'):
            (abi / name).write_bytes(source.read('lib/armeabi/' + name))
    for path in sorted((TOOLCHAIN / 'python-arm32/jniLibs/armeabi-v7a').glob('*.so')):
        shutil.copy2(path, abi / path.name)
    shutil.copy2(python_bridge, abi / 'libpython_bootstrap.so')
    shutil.copy2(native, abi / 'liboffline.so')
    classes = WORK / 'classes'
    classes.mkdir(exist_ok=True)
    run(JAVA / 'bin/javac', '-source', '8', '-target', '8', '-classpath', TOOLCHAIN / 'android.jar',
        '-d', classes, *sorted((ROOT / 'offline_android/java').rglob('*.java')))
    dex = WORK / 'dex'
    dex.mkdir(exist_ok=True)
    run(TOOLS / 'd8', '--min-api', '21', '--lib', TOOLCHAIN / 'android.jar',
        '--output', dex, *sorted(classes.rglob('*.class')))
    shell = WORK / 'shell.apk'
    apktool('b', '-p', ROOT / '.runtime/tools/apktool-framework', '-o', shell, decoded)
    unsigned = WORK / 'unsigned.apk'
    with zipfile.ZipFile(shell) as source, zipfile.ZipFile(unsigned, 'w') as dest:
        for entry in source.infolist():
            if not entry.filename.startswith('META-INF/') and entry.filename != 'classes2.dex':
                data = source.read(entry)
                if entry.filename == 'res/raw/video.mp4':
                    data = (ROOT / 'opening_patch/opening.mp4').read_bytes()
                    entry.compress_type = zipfile.ZIP_STORED
                dest.writestr(entry, data)
        put(dest, 'classes2.dex', (dex / 'classes.dex').read_bytes())
    aligned = WORK / 'aligned.apk'
    run(TOOLS / 'zipalign', '-f', '4', unsigned, aligned)
    run(TOOLS / 'apksigner', 'sign', '--ks', SIGNING_KEY, '--ks-key-alias', 'channel360',
        '--ks-pass', 'pass:local-test-only', '--out', output, aligned)
    signer_certificate(output)
    run(TOOLS / 'apksigner', 'verify', '--verbose', output)
    run(TOOLS / 'zipalign', '-c', '4', output)
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise RuntimeError('APK ZIP integrity failed')
        if archive.read('assets/offline/program.zip') != program.read_bytes():
            raise RuntimeError('Program bundle changed during packaging')
        game_names = [name for name in archive.namelist() if name.startswith('assets/release_/')]
        with zipfile.ZipFile(BASELINE) as baseline:
            for name in game_names:
                if archive.read(name) != baseline.read(name):
                    raise RuntimeError('Original game resource changed: ' + name)
    report = dict(apk=str(output), sha256=digest(output), bytes=output.stat().st_size,
                  package=PACKAGE, certificate_sha256=CERTIFICATE, version_code=version_code,
                  min_sdk=21, target_sdk=22, abi='armeabi-v7a',
                  baseline_apk_sha256=digest(BASELINE), program_sha256=digest(program),
                  runtime_sha256=digest(runtime), payload=payload,
                  client_overlay=overlay, original_game_assets_verified=len(game_names),
                  player_database='files/save/game.sqlite3',
                  runtime_requires_external_frida=False, runtime_requires_adb=False)
    report_path = output.with_suffix('.manifest.json')
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print('Built and verified:', output)
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--version-code', type=int, default=105)
    parser.add_argument('--reuse-decode', action='store_true')
    args = parser.parse_args()
    build(args.output, args.version_code, args.reuse_decode)
