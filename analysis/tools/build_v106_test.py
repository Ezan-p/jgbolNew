"""Isolated test edition from the exact published 19-change v106 APK."""
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from build_channel360 import JAVA, TOOLS, apktool, run
from offline_android.pack_payload import verify_payload

BASE = ROOT / 'build/金箍棒3.87-离线单机-arm32-v106.apk'
BASE_SHA = '228bb674fc7ea3bd6cad73895d6589d74ca5724210c9b99dbe8351ffd4a657d5'
WORK = ROOT / '.runtime/v106-test'
EVIDENCE = ROOT / 'analysis/evidence/v106_test'
OUTPUT = ROOT / 'build/金箍棒ol测试版-v106.apk'
PACKAGE = 'com.sygame.jingubang.test106'
PORT = 18776
KEY = ROOT / '.runtime/test-edition-signing/test106.p12'
ANDROID = '{http://schemas.android.com/apk/res/android}'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def certificate(path):
    out = subprocess.check_output([str(TOOLS / 'apksigner'), 'verify', '--print-certs', str(path)],
                                  env={**os.environ, 'JAVA_HOME': str(JAVA)}, text=True)
    return re.search(r'certificate SHA-256 digest: ([0-9a-f]+)', out)[1]


def payload():
    with zipfile.ZipFile(BASE) as z:
        with zipfile.ZipFile(io.BytesIO(z.read('assets/offline/program.zip'))) as p:
            entries = {n: p.read(n) for n in p.namelist()}
    old = dict(entries)
    backend = entries['offline_android/backend.py'].decode()
    assert backend.count('PORT = 18770') == 1
    backend = backend.replace('PORT = 18770', f'PORT = {PORT}')
    backend = backend.replace("self.files_dir / 'save'", "self.files_dir / 'test-save-v106'")
    backend = backend.replace('from network_redirect.accounts import Accounts',
        'from offline_android.test_edition_seed import fixed_accounts_class\n        Accounts = fixed_accounts_class()')
    entries['offline_android/backend.py'] = backend.encode()
    entries['offline_android/test_edition_seed.py'] = (ROOT / 'offline_android/test_edition_seed.py').read_bytes()
    entries['network_redirect/login.html'] = (ROOT / 'offline_android/test_edition_login.html').read_bytes()
    manifest = json.loads(entries['payload-manifest.json'])
    indexed = {entry['path']: entry for entry in manifest['files']}
    for name, data in entries.items():
        if name != 'payload-manifest.json' and (name not in old or old[name] != data):
            indexed[name] = dict(path=name, size=len(data), sha256=digest(data), source='test-edition')
    manifest['files'] = sorted(indexed.values(), key=lambda entry: entry['path'])
    manifest['bundle_id'] = digest(json.dumps(manifest['files'], sort_keys=True, separators=(',', ':')).encode())
    manifest.update(player_database='files/test-save-v106/game.sqlite3', loopback_port=PORT)
    entries['payload-manifest.json'] = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
    with zipfile.ZipFile(WORK / 'program.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in entries.items():
            z.writestr(name, data)
            path = WORK / 'program' / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    verify_payload(WORK / 'program')
    return sorted(n for n in entries if entries[n] != old.get(n))


def native_adapter():
    # Reproduce baseline first, ensuring the only source difference is the port.
    from offline_android.native import build_native
    baseline_native = build_native.build(WORK / 'liboffline-baseline.so')
    with zipfile.ZipFile(BASE) as z:
        assert baseline_native.read_bytes() == z.read('lib/armeabi-v7a/liboffline.so'), 'Native source drift'
    source = (ROOT / 'offline_android/native/offline.c').read_text().replace('18770', str(PORT))
    (WORK / 'offline-test.c').write_text(source)
    run('/usr/bin/clang', '--target=armv7a-linux-androideabi21', '-marm', '-fPIC', '-Os',
        '-fno-stack-protector', '-fno-builtin', '-fvisibility=hidden', '-Wall', '-Wextra', '-Werror',
        '-c', WORK / 'offline-test.c', '-o', WORK / 'offline-test.o')
    run(TOOLS / 'lld-bin/lld', '-flavor', 'gnu', '-shared', '--hash-style=both', '--no-undefined',
        '-soname', 'liboffline.so', '-z', 'max-page-size=4096', WORK / 'offline-test.o',
        *[ROOT / '.runtime/offline-native' / n for n in build_native.IMPORTS], '-o', WORK / 'liboffline.so')


def build(reuse_decode=False):
    assert digest(BASE.read_bytes()) == BASE_SHA, 'Published baseline has changed'
    WORK.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    changes = payload()
    native_adapter()
    decoded = WORK / 'decoded'
    framework = ROOT / '.runtime/tools/apktool-framework'
    if not reuse_decode:
        apktool('d', '-f', '-p', framework, '-o', decoded, BASE)
    ET.register_namespace('android', ANDROID[1:-1])
    tree = ET.parse(decoded / 'AndroidManifest.xml')
    root = tree.getroot()
    old_package = root.get('package')
    assert old_package in ('com.sygame.jingubang.p360', PACKAGE)
    root.set('package', PACKAGE)
    # No shared external storage permissions: all writes stay app-private.
    for permission in list(root.findall('uses-permission')):
        if permission.get(ANDROID + 'name') in (
                'android.permission.WRITE_EXTERNAL_STORAGE', 'android.permission.READ_EXTERNAL_STORAGE',
                'android.permission.MOUNT_UNMOUNT_FILESYSTEMS'):
            root.remove(permission)
    for activity in root.find('application').findall('activity'):
        name = activity.get(ANDROID + 'name')
        if name.startswith('.'):
            activity.set(ANDROID + 'name', 'com.sygame.jingubang.p360' + name)
    tree.write(decoded / 'AndroidManifest.xml', encoding='utf-8', xml_declaration=True)
    for strings in decoded.glob('res/values*/strings.xml'):
        text = strings.read_text()
        text = re.sub(r'(<string name="app_name">).*?(</string>)', r'\g<1>金箍棒ol测试版\2', text)
        strings.write_text(text)
    login = decoded / 'smali/com/syyx/sdkproxy/LocalLogin.smali'
    login.write_text(login.read_text().replace(':18770/', f':{PORT}/'))
    launcher = decoded / 'smali_classes2/com/jgbol/offline/LauncherActivity.smali'
    launcher.write_text(launcher.read_text().replace(
        json.dumps('金箍棒 · 离线单机'), json.dumps('金箍棒ol测试版')))
    metadata = decoded / 'apktool.yml'
    metadata.write_text(re.sub(r'(?m)^  versionName:.*$', '  versionName: 3.87-test.106.1', metadata.read_text()))
    shell = WORK / 'shell.apk'
    apktool('b', '-p', framework, '-o', shell, decoded)
    program_hash = digest((WORK / 'program.zip').read_bytes())
    with zipfile.ZipFile(BASE) as z, zipfile.ZipFile(shell) as compiled:
        runtime_hash = digest(z.read('assets/offline/runtime.zip'))
        replacements = {n: compiled.read(n) for n in ('AndroidManifest.xml', 'resources.arsc', 'classes.dex', 'classes2.dex')}
        replacements.update({
            'assets/offline/program.zip': (WORK / 'program.zip').read_bytes(),
            'lib/armeabi-v7a/liboffline.so': (WORK / 'liboffline.so').read_bytes(),
            'assets/offline/build.properties': f'program_sha256={program_hash}\nruntime_sha256={runtime_hash}\nversion_code=106\n'.encode()})
        with zipfile.ZipFile(WORK / 'unsigned.apk', 'w') as out:
            for entry in z.infolist():
                if not entry.filename.startswith('META-INF/'):
                    out.writestr(entry, replacements.get(entry.filename, z.read(entry)))
    if not KEY.exists():
        if OUTPUT.exists():
            raise RuntimeError('Test signing key missing; refusing to break test upgrades')
        KEY.parent.mkdir(parents=True, exist_ok=True)
        run(JAVA / 'bin/keytool', '-genkeypair', '-keystore', KEY, '-storetype', 'PKCS12',
            '-storepass', 'test-edition-only', '-keypass', 'test-edition-only', '-alias', 'test106',
            '-keyalg', 'RSA', '-keysize', '2048', '-validity', '10000',
            '-dname', 'CN=JGBOL v106 Isolated Test,OU=Test Edition,O=Local Development,C=CN')
        KEY.chmod(0o600)
    run(TOOLS / 'zipalign', '-f', '4', WORK / 'unsigned.apk', WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'sign', '--ks', KEY, '--ks-key-alias', 'test106',
        '--ks-pass', 'pass:test-edition-only', '--out', OUTPUT, WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'verify', '--verbose', OUTPUT)
    run(TOOLS / 'zipalign', '-c', '4', OUTPUT)
    cert = certificate(OUTPUT)
    assert cert != certificate(BASE)
    badging = subprocess.check_output([str(TOOLS / 'aapt'), 'dump', 'badging', str(OUTPUT)], text=True)
    assert f"package: name='{PACKAGE}'" in badging and "application-label:'金箍棒ol测试版'" in badging
    with zipfile.ZipFile(BASE) as z, zipfile.ZipFile(OUTPUT) as out:
        assert out.testzip() is None
        changed = sorted(n for n in z.namelist() if not n.startswith('META-INF/') and z.read(n) != out.read(n))
        assert set(changed) == set(replacements)
    assert digest(BASE.read_bytes()) == BASE_SHA
    report = dict(apk=OUTPUT.name, apk_sha256=digest(OUTPUT.read_bytes()), apk_bytes=OUTPUT.stat().st_size,
        baseline_sha256=BASE_SHA, package=PACKAGE, version_code=106, version_name='3.87-test.106.1',
        app_label='金箍棒ol测试版', certificate_sha256=cert, program_sha256=program_hash,
        player_database=f'/data/user/0/{PACKAGE}/files/test-save-v106/game.sqlite3',
        port=PORT, baseline_preserved=True, changed_apk_entries=changed, changed_program_entries=changes,
        contains_personal_database=False, fixed_account='v106_fixed_test', initialize_only_once=True)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    OUTPUT.with_suffix('.manifest.json').write_text(rendered)
    OUTPUT.with_suffix('.apk.sha256').write_text(report['apk_sha256'] + '  ' + OUTPUT.name + '\n')
    (EVIDENCE / 'build-validation.json').write_text(rendered)
    (EVIDENCE / 'badging.txt').write_text(badging)
    print(rendered)


if __name__ == '__main__':
    build('--reuse-decode' in sys.argv)
