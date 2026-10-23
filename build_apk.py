"""Build the configured variant, or restore the original signed APK."""
from pathlib import Path
import os
import json
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parent


def build():
    config = json.loads((ROOT / 'game.json').read_text())
    if config.get('apk_variant') == '360-from-3.79':
        from build_channel360 import build as build360
        return build360(output=ROOT / config['apk'],
                        server_list_compat=config.get('server_list_compat', False))
    source = ROOT / config['apk_source']
    output = ROOT / config['apk']
    output.parent.mkdir(exist_ok=True)
    temporary = output.with_suffix('.tmp.apk')
    aligned = output.with_suffix('.aligned.apk')
    for name in ('AndroidManifest.xml', 'classes.dex', 'resources.arsc', 'META-INF/MANIFEST.MF'):
        if not (source / name).is_file():
            raise RuntimeError('缺少原始游戏文件：' + name)
    if not any(path.suffix.upper() in ('.RSA', '.DSA', '.EC')
               for path in (source / 'META-INF').iterdir()):
        raise RuntimeError('缺少原始 APK 签名块')
    try:
        with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(source.rglob('*')):
                if path.is_file() and path.name != '.DS_Store':
                    # Android AssetManager.openFd requires media to be stored.
                    compression = (zipfile.ZIP_STORED if path.suffix.lower() in
                                   ('.mp3', '.ogg', '.wav', '.mp4', '.arsc')
                                   else zipfile.ZIP_DEFLATED)
                    archive.write(path, path.relative_to(source).as_posix(),
                                  compress_type=compression)
        java = ROOT / '.runtime/java/jdk-17.0.20.1+1/Contents/Home'
        signer = ROOT / '.runtime/sdk/build-tools/35.0.0/apksigner'
        subprocess.run([str(signer.with_name('zipalign')), '-f', '4',
                        str(temporary), str(aligned)], check=True)
        subprocess.run([str(signer), 'verify', '--verbose', str(aligned)],
                       env={**os.environ, 'JAVA_HOME': str(java)}, check=True)
        aligned.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
        aligned.unlink(missing_ok=True)
    print('已还原并验证原始签名：', output)


if __name__ == '__main__':
    build()
