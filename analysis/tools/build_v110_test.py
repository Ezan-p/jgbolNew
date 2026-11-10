"""Build v110 plus implemented workspace updates with the existing test identity."""
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v106_test import certificate, digest, KEY, PACKAGE, PORT, ANDROID
from build_channel360 import JAVA, TOOLS, apktool, run
from offline_android.pack_payload import collect_files, verify_payload

BASE = ROOT / 'build/金箍棒ol离线正式版v110.apk'
PREVIOUS = ROOT / 'build/金箍棒ol测试版-v108.apk'
WORK = ROOT / '.runtime/v110-test'
EVIDENCE = ROOT / 'analysis/evidence/v110_test'
APK = WORK / '金箍棒ol测试版-v110.apk'
VERSION_NAME = '3.87-test.110.1'
BASE_SHA = '4f98c0ab98a574886b2b771a9ad82ace2bdcfaf6de89a389c3770cb078432375'
PREVIOUS_SHA = '5799df38409172fa0efc67e1a04418bed5c2c12119a4630366f564a607fdf5b8'


def main():
    assert not APK.exists(), 'Refusing to overwrite an existing candidate'
    assert KEY.is_file(), 'Existing test signing key required'
    assert digest(BASE.read_bytes()) == BASE_SHA
    assert digest(PREVIOUS.read_bytes()) == PREVIOUS_SHA
    WORK.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    sources = collect_files()
    source_hashes = {n: digest(p.read_bytes()) for n, p in sources.items()}
    with zipfile.ZipFile(BASE) as base, zipfile.ZipFile(PREVIOUS) as old:
        with zipfile.ZipFile(io.BytesIO(base.read('assets/offline/program.zip'))) as p:
            original = {n: p.read(n) for n in p.namelist()}
        entries = dict(original)
        entries.update({n: p.read_bytes() for n, p in sources.items()})
        from network_redirect.summon import client_source, load_rules
        # Workspace branding may be prepared for a separate formal release.
        # Set this artifact's label without editing that shared source file.
        def test_branding(data):
            value, count = re.subn(rb"label\('v\d+',0\.75\)", b"label('v110',0.75)", data)
            assert count == 1
            return value
        entries['offline_client.lua'] = test_branding(client_source(load_rules()).encode())
        entries['network_redirect/login_branding_client.lua'] = test_branding(
            entries['network_redirect/login_branding_client.lua'])
        # Keep the shipped supply algorithm and revision, so v108 saves are not refilled.
        with zipfile.ZipFile(io.BytesIO(old.read('assets/offline/program.zip'))) as p:
            for name in ('offline_android/test_edition_seed.py',
                         'offline_android/test_edition_v108.py', 'network_redirect/login.html'):
                entries[name] = p.read(name)
        # Keep the same allowance but use the already-implemented unified clock adapter.
        seed_path = ROOT / 'offline_android/test_edition_v108.py'
        entries['offline_android/test_edition_v108.py'] = seed_path.read_bytes()
        source_hashes['offline_android/test_edition_v108.py'] = digest(seed_path.read_bytes())
        backend = entries['offline_android/backend.py'].decode()
        for before, after in [('PORT = 18770', f'PORT = {PORT}'),
                ("self.files_dir / 'save'", "self.files_dir / 'test-save-v106'"),
                ('from network_redirect.accounts import Accounts',
                 'from offline_android.test_edition_v108 import fixed_accounts_class\n        Accounts = fixed_accounts_class()')]:
            assert backend.count(before) == 1
            backend = backend.replace(before, after)
        entries['offline_android/backend.py'] = backend.encode()
        changed = sorted(n for n in entries if entries[n] != original.get(n))
        manifest = json.loads(entries['payload-manifest.json'])
        indexed = {r['path']: r for r in manifest['files']}
        for name in changed:
            data = entries[name]
            indexed[name] = dict(path=name, size=len(data), sha256=digest(data), source='v110-test-workspace')
        manifest['files'] = sorted(indexed.values(), key=lambda r: r['path'])
        manifest['bundle_id'] = digest(json.dumps(manifest['files'], sort_keys=True, separators=(',', ':')).encode())
        manifest.update(player_database='files/test-save-v106/game.sqlite3', loopback_port=PORT)
        entries['payload-manifest.json'] = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
        with zipfile.ZipFile(WORK / 'program.zip', 'w', zipfile.ZIP_DEFLATED) as p:
            for name, data in entries.items():
                assert Path(name).suffix not in ('.db', '.sqlite3', '.pyc')
                p.writestr(name, data)
        # Extract the actual ZIP that will go into the APK for all regression checks.
        with zipfile.ZipFile(WORK / 'program.zip') as p:
            p.extractall(WORK / 'program')
        verify_payload(WORK / 'program')

    from offline_android.native import build_native
    build_native.build(WORK / 'liboffline-current-formal-port.so')
    native_source = (ROOT / 'offline_android/native/offline.c').read_bytes()
    (WORK / 'offline-test.c').write_bytes(native_source.replace(b'18770', str(PORT).encode()))
    run('/usr/bin/clang', '--target=armv7a-linux-androideabi21', '-marm', '-fPIC', '-Os',
        '-fno-stack-protector', '-fno-builtin', '-fvisibility=hidden', '-Wall', '-Wextra', '-Werror',
        '-c', WORK / 'offline-test.c', '-o', WORK / 'offline-test.o')
    run(TOOLS / 'lld-bin/lld', '-flavor', 'gnu', '-shared', '--hash-style=both', '--no-undefined',
        '-soname', 'liboffline.so', '-z', 'max-page-size=4096', WORK / 'offline-test.o',
        *[ROOT / '.runtime/offline-native' / n for n in build_native.IMPORTS], '-o', WORK / 'liboffline.so')

    # Start with the latest formal shell, including lifecycle and boot identity fixes.
    decoded, framework = WORK / 'decoded', ROOT / '.runtime/tools/apktool-framework'
    if '--reuse-shell' not in sys.argv:
        apktool('d', '-f', '-p', framework, '-o', decoded, BASE)
    ET.register_namespace('android', ANDROID[1:-1])
    tree = ET.parse(decoded / 'AndroidManifest.xml')
    root = tree.getroot()
    assert root.get('package') in ('com.sygame.jingubang.p360', PACKAGE)
    root.set('package', PACKAGE)
    for permission in list(root.findall('uses-permission')):
        if permission.get(ANDROID + 'name') in ('android.permission.WRITE_EXTERNAL_STORAGE',
                'android.permission.READ_EXTERNAL_STORAGE', 'android.permission.MOUNT_UNMOUNT_FILESYSTEMS'):
            root.remove(permission)
    for activity in root.find('application').findall('activity'):
        name = activity.get(ANDROID + 'name')
        if name.startswith('.'):
            activity.set(ANDROID + 'name', 'com.sygame.jingubang.p360' + name)
    tree.write(decoded / 'AndroidManifest.xml', encoding='utf-8', xml_declaration=True)
    for path in decoded.glob('res/values*/strings.xml'):
        path.write_text(re.sub(r'(<string name="app_name">).*?(</string>)',
                              r'\g<1>金箍棒ol测试版\2', path.read_text()))
    login = decoded / 'smali/com/syyx/sdkproxy/LocalLogin.smali'
    assert ':18770/' in login.read_text() or f':{PORT}/' in login.read_text()
    login.write_text(login.read_text().replace(':18770/', f':{PORT}/'))
    meta = decoded / 'apktool.yml'
    content = meta.read_text()
    for key, value in [('versionCode', '110'), ('versionName', VERSION_NAME)]:
        content, count = re.subn(r'(?m)^  ' + key + r':.*$', '  ' + key + ': ' + value, content)
        assert count == 1
    meta.write_text(content)
    if '--reuse-shell' not in sys.argv:
        apktool('b', '-p', framework, '-o', WORK / 'shell.apk', decoded)

    java_hashes = {}
    for source in sorted((ROOT / 'offline_android/java').rglob('*.java')):
        relative = source.relative_to(ROOT / 'offline_android/java')
        target = WORK / 'java' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        java_hashes[str(source.relative_to(ROOT))] = digest(source.read_bytes())
        target.write_text(source.read_text().replace('金箍棒 · 离线单机', '金箍棒ol测试版'))
    classes, dex = WORK / 'classes', WORK / 'dex'
    classes.mkdir(exist_ok=True)
    dex.mkdir(exist_ok=True)
    android = ROOT / '.runtime/offline-toolchain/android.jar'
    run(JAVA / 'bin/javac', '-source', '8', '-target', '8', '-classpath', android,
        '-d', classes, *sorted((WORK / 'java').rglob('*.java')))
    run(TOOLS / 'd8', '--min-api', '21', '--lib', android,
        '--output', dex, *sorted(classes.rglob('*.class')))
    program_hash = digest((WORK / 'program.zip').read_bytes())
    with zipfile.ZipFile(BASE) as base, zipfile.ZipFile(WORK / 'shell.apk') as shell:
        replacements = {n: shell.read(n) for n in ('AndroidManifest.xml', 'resources.arsc', 'classes.dex')}
        replacements['classes2.dex'] = (dex / 'classes.dex').read_bytes()
        replacements['lib/armeabi-v7a/liboffline.so'] = (WORK / 'liboffline.so').read_bytes()
        runtime_hash = digest(base.read('assets/offline/runtime.zip'))
        replacements.update({'assets/offline/program.zip': (WORK / 'program.zip').read_bytes(),
            'assets/offline/build.properties': f'program_sha256={program_hash}\nruntime_sha256={runtime_hash}\nversion_code=110\n'.encode()})
        with zipfile.ZipFile(WORK / 'unsigned.apk', 'w') as out:
            for entry in base.infolist():
                if not entry.filename.startswith('META-INF/'):
                    out.writestr(entry, replacements.get(entry.filename, base.read(entry)))
    run(TOOLS / 'zipalign', '-f', '4', WORK / 'unsigned.apk', WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'sign', '--ks', KEY, '--ks-key-alias', 'test106',
        '--ks-pass', 'pass:test-edition-only', '--out', APK, WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'verify', '--verbose', APK)
    run(TOOLS / 'zipalign', '-c', '4', APK)
    assert certificate(APK) == certificate(PREVIOUS) != certificate(BASE)
    badging = subprocess.check_output([str(TOOLS / 'aapt'), 'dump', 'badging', str(APK)], text=True)
    assert f"package: name='{PACKAGE}' versionCode='110' versionName='{VERSION_NAME}'" in badging
    assert "application-label:'金箍棒ol测试版'" in badging
    assert 'android.permission.WRITE_EXTERNAL_STORAGE' not in badging
    with zipfile.ZipFile(BASE) as base, zipfile.ZipFile(APK) as result:
        assert result.testzip() is None
        changed_apk = sorted(n for n in base.namelist() if not n.startswith('META-INF/') and base.read(n) != result.read(n))
        assert set(changed_apk) == set(replacements)
    assert digest(BASE.read_bytes()) == BASE_SHA and digest(PREVIOUS.read_bytes()) == PREVIOUS_SHA
    assert all(digest((ROOT / n).read_bytes()) == sha for n, sha in source_hashes.items()), 'Workspace changed during build'
    report = dict(apk=APK.name, apk_sha256=digest(APK.read_bytes()), apk_bytes=APK.stat().st_size,
        baseline=BASE.name, baseline_sha256=BASE_SHA, previous_test_sha256=PREVIOUS_SHA,
        package=PACKAGE, version_code=110, version_name=VERSION_NAME, port=PORT,
        certificate_sha256=certificate(APK), program_sha256=program_hash,
        player_database=f'/data/user/0/{PACKAGE}/files/test-save-v106/game.sqlite3',
        fixed_account='v106_fixed_test', supply_revision=108, initialize_only_once=True,
        contains_player_database=False, baselines_preserved=True,
        native_source_sha256=digest(native_source), java_source_sha256=java_hashes,
        workspace_source_sha256=source_hashes,
        changed_apk_entries=changed_apk, changed_program_entries=changed + ['payload-manifest.json'])
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    APK.with_suffix('.manifest.json').write_text(rendered)
    APK.with_suffix('.apk.sha256').write_text(report['apk_sha256'] + '  ' + APK.name + '\n')
    (EVIDENCE / 'build-validation.json').write_text(rendered)
    (EVIDENCE / 'badging.txt').write_text(badging)
    print(json.dumps({k: v for k, v in report.items() if k != 'workspace_source_sha256'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
