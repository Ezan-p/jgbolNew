"""Build 3.87 game content with the original 3.79 / 360 Android integration.

Inputs are read-only. Requires Apktool 2.12.1 at .runtime/tools/apktool.jar.
The output uses a local test certificate, not either publisher's certificate.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parent
WORK = ROOT / '.runtime/channel360'
JAVA = ROOT / '.runtime/java/jdk-17.0.20.1+1/Contents/Home'
TOOLS = ROOT / '.runtime/sdk/build-tools/35.0.0'
APKTOOL = ROOT / '.runtime/tools/apktool.jar'
OUTPUT = ROOT / 'build/jgbol3.87-360.apk'
ENV = {**os.environ, 'JAVA_HOME': str(JAVA)}


def run(*args):
    subprocess.run([str(a) for a in args], check=True, env=ENV)


def apktool(*args):
    run(JAVA / 'bin/java', '-jar', APKTOOL, *args)


def shell_input(version):
    source = ROOT / f'jgbol3.{version}'
    target = WORK / f'shell-{version}.apk'
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob('*')):
            relative = path.relative_to(source)
            if path.is_file() and path.name != '.DS_Store' and (
                    relative.parts[0] == 'res' or len(relative.parts) == 1):
                archive.write(path, relative.as_posix())
    return target


def build(output=None, server_list_compat=False):
    output = Path(output) if output is not None else OUTPUT
    if not APKTOOL.is_file():
        raise RuntimeError('请先将 Apktool 2.12.1 放到 .runtime/tools/apktool.jar')
    WORK.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    decoded = WORK / 'decoded'
    newer = WORK / 'new-shell'
    framework = ROOT / '.runtime/tools/apktool-framework'
    apktool('d', '-f', '-p', framework, '-o', decoded, shell_input('79'))
    apktool('d', '-f', '-r', '-p', framework, '-o', newer, shell_input('87'))

    # Keep 3.87's engine-side Java glue with its unchanged 3.87 native library.
    shutil.rmtree(decoded / 'smali/org/cocos2dx')
    shutil.copytree(newer / 'smali/org/cocos2dx', decoded / 'smali/org/cocos2dx')
    # Native JNI exports name the UC Activity. Move only the Activity class and
    # its inner classes; preserve the 360 application ID, SDK and resource IDs.
    old_class = 'com/sygame/jingubang/p360/xiyoujilua'
    new_class = 'com/sygame/jingubang/uc/xiyoujilua'
    for path in (decoded / 'smali').rglob('*.smali'):
        text = path.read_text()
        updated = text.replace(old_class, new_class).replace(
            old_class.replace('/', '.'), new_class.replace('/', '.'))
        if updated != text:
            path.write_text(updated)
    activity_dir = decoded / 'smali/com/sygame/jingubang/uc'
    activity_dir.mkdir(parents=True, exist_ok=True)
    for path in (decoded / 'smali/com/sygame/jingubang/p360').glob('xiyoujilua*.smali'):
        path.rename(activity_dir / path.name)
    bridge = (decoded / 'smali/com/syyx/sdkproxy/ThirdPartyAPI.smali').read_text()
    if 'const/16 v0, 0x6b' not in bridge or 'Lcom/qihoo/gamecenter/sdk' not in bridge:
        raise RuntimeError('3.79 SDK 或渠道号与预期不符')
    activity = (activity_dir / 'xiyoujilua.smali').read_text()
    native = (ROOT / 'jgbol3.87/lib/armeabi/libxiyoujilua.so').read_bytes()
    for name in re.findall(r'\.method .*? native (\w+)\(', activity):
        symbol = ('Java_com_sygame_jingubang_uc_xiyoujilua_' + name).encode()
        if symbol not in native:
            raise RuntimeError('3.87 native 缺少 Activity JNI 入口：' + name)
    manifest = decoded / 'AndroidManifest.xml'
    manifest.write_text(manifest.read_text().replace(
        old_class.replace('/', '.'), new_class.replace('/', '.')))
    metadata = decoded / 'apktool.yml'
    metadata.write_text(metadata.read_text().replace(
        'versionCode: 79', 'versionCode: 87').replace('versionName: 3.79', 'versionName: 3.87'))
    shell = WORK / 'shell-360-unsigned.apk'
    apktool('b', '-p', framework, '-o', shell, decoded)

    # SDK assets come from 3.79. All game assets, speech assets and native
    # libraries come from 3.87. Never mix either version's release_ directory.
    payload = {}
    for path in (ROOT / 'jgbol3.79/assets').rglob('*'):
        relative = path.relative_to(ROOT / 'jgbol3.79')
        if path.is_file() and relative.parts[1] not in ('release_', 'model'):
            payload[relative.as_posix()] = path
    for folder in ('assets/release_', 'assets/model', 'lib'):
        for path in (ROOT / 'jgbol3.87' / folder).rglob('*'):
            if path.is_file():
                payload[path.relative_to(ROOT / 'jgbol3.87').as_posix()] = path
    patched_asset = None
    if server_list_compat:
        from analysis.tools.patch_server_list import patch
        import base64
        alphabet = 'yfglmnovwxapzdechijkqrstbuHOMICDJPQRSTUVWXYZABKEFGLN39+0126-4785_'
        encoded = (ROOT / 'jgbol3.87/assets/release_/index.txt').read_text().split('\n', 1)[1]
        index = base64.b64decode(encoded.translate(str.maketrans(
            alphabet, 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=')),
            validate=True).decode('gb18030')
        rows = [line.split('====') for line in index.splitlines()]
        physical = next(row[1] for row in rows if row[0] == 'lua/update/update_mgr.lua')
        patched_asset = 'assets/release_/' + physical
        patched_file = WORK / 'update_mgr-list-compat.data'
        patched_file.write_bytes(patch(payload[patched_asset].read_bytes()))
        payload[patched_asset] = patched_file
    unsigned = WORK / 'unsigned.apk'
    with zipfile.ZipFile(shell) as source, zipfile.ZipFile(unsigned, 'w') as dest:
        for entry in source.infolist():
            if not entry.filename.startswith('META-INF/'):
                dest.writestr(entry, source.read(entry))
        for name, path in sorted(payload.items()):
            if path.name == '.DS_Store':
                continue
            compression = (zipfile.ZIP_STORED if path.suffix.lower() in
                           ('.mp3', '.ogg', '.wav', '.mp4', '.arsc') else zipfile.ZIP_DEFLATED)
            dest.write(path, name, compress_type=compression)
    aligned = WORK / 'aligned.apk'
    run(TOOLS / 'zipalign', '-f', '4', unsigned, aligned)
    keystore = WORK / 'local-test.p12'
    if not keystore.exists():
        run(JAVA / 'bin/keytool', '-genkeypair', '-keystore', keystore,
            '-storepass', 'local-test-only', '-keypass', 'local-test-only',
            '-alias', 'channel360', '-keyalg', 'RSA', '-keysize', '2048',
            '-validity', '3650', '-dname', 'CN=JGBOL Local Channel Test')
        keystore.chmod(0o600)
    run(TOOLS / 'apksigner', 'sign', '--ks', keystore, '--ks-key-alias', 'channel360',
        '--ks-pass', 'pass:local-test-only', '--out', output, aligned)
    run(TOOLS / 'apksigner', 'verify', '--verbose', output)
    run(TOOLS / 'zipalign', '-c', '4', output)
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        for name, path in payload.items():
            if path.name != '.DS_Store':
                assert archive.read(name) == path.read_bytes(), name
        assert not any(n.startswith('assets/ucgamesdk/') for n in archive.namelist())
    report = {
        'apk': str(output.relative_to(ROOT)),
        'sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
        'package': 'com.sygame.jingubang.p360',
        'activity': 'com.sygame.jingubang.uc.xiyoujilua',
        'versionName': '3.87', 'versionCode': 87,
        'channel': 107, 'channel_name': 'p360_na',
        'game_native_and_assets': 'jgbol3.87; payload verified against originals except listed patches',
        'server_list_compat': server_list_compat,
        'patched_asset': patched_asset,
        'android_sdk_integration': 'jgbol3.79 with 3.87 Cocos2dx Java glue',
        'signature': 'local test certificate',
        'payload_files_verified': len(payload),
        'remote_login_verified': False,
    }
    report_name = 'build-list-report.json' if server_list_compat else 'build-report.json'
    (WORK / report_name).write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print('已构建并验证：', output)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--server-list-compat', action='store_true')
    args = parser.parse_args()
    build(ROOT / 'build/jgbol3.87-360-list.apk' if args.server_list_compat else OUTPUT,
          server_list_compat=args.server_list_compat)
