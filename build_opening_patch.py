"""Add opening playback to the shipped offline v102 without repacking its backend."""
import json
from pathlib import Path
import re
import shutil
import zipfile

from build_channel360 import JAVA, TOOLS, apktool, run
from build_offline import CERTIFICATE, SIGNING_KEY, signer_certificate
from opening_patch.apply_patch import apply, sha256
from opening_patch.build_patch import build_delta

ROOT = Path(__file__).resolve().parent
WORK = ROOT / '.runtime/opening-build'
BASE = ROOT / 'build/金箍棒3.87-离线单机-arm32.apk'
BASE_SHA256 = '87b6a851c3a4edf0ef79f098792f765b699966a4b967022efcbf21fb822c3c95'
OUTPUT = ROOT / 'build/金箍棒3.87-开场动画更新-v103.apk'


def build():
    if sha256(BASE) != BASE_SHA256:
        raise ValueError('Expected the preserved v102 APK; refusing to patch another baseline')
    signer_certificate(BASE)
    WORK.mkdir(parents=True, exist_ok=True)
    decoded = WORK / 'decoded'
    framework = ROOT / '.runtime/tools/apktool-framework'
    apktool('d', '-f', '-s', '-p', framework, '-o', decoded, BASE)
    metadata = decoded / 'apktool.yml'
    text = metadata.read_text()
    text, count = re.subn(r'(?m)^  versionCode:.*$', '  versionCode: 103', text)
    if count != 1:
        raise ValueError('Missing version code')
    text = re.sub(r'(?m)^  versionName:.*$', '  versionName: 3.87-offline.2-opening', text)
    metadata.write_text(text)
    shell = WORK / 'manifest-shell.apk'
    apktool('b', '-p', framework, '-o', shell, decoded)
    classes, dex = WORK / 'classes', WORK / 'dex'
    for directory in (classes, dex):
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir()
    android = ROOT / '.runtime/offline-toolchain/android.jar'
    run(JAVA / 'bin/javac', '-source', '8', '-target', '8', '-classpath', android,
        '-d', classes, *sorted((ROOT / 'offline_android/java').rglob('*.java')))
    run(TOOLS / 'd8', '--min-api', '21', '--lib', android, '--output', dex,
        *sorted(classes.rglob('*.class')))
    unsigned = WORK / 'unsigned.apk'
    with zipfile.ZipFile(BASE) as source, zipfile.ZipFile(shell) as compiled, \
            zipfile.ZipFile(unsigned, 'w') as dest:
        for entry in source.infolist():
            if entry.filename.startswith('META-INF/'):
                continue
            data = source.read(entry)
            if entry.filename == 'AndroidManifest.xml':
                data = compiled.read(entry.filename)
            elif entry.filename == 'classes2.dex':
                data = (dex / 'classes.dex').read_bytes()
            elif entry.filename == 'res/raw/video.mp4':
                # Android resource playback requires an uncompressed file descriptor.
                data = (ROOT / 'opening_patch/opening.mp4').read_bytes()
                entry.compress_type = zipfile.ZIP_STORED
            dest.writestr(entry, data)
    aligned = WORK / 'aligned.apk'
    run(TOOLS / 'zipalign', '-f', '4', unsigned, aligned)
    run(TOOLS / 'apksigner', 'sign', '--ks', SIGNING_KEY, '--ks-key-alias', 'channel360',
        '--ks-pass', 'pass:local-test-only', '--out', OUTPUT, aligned)
    signer_certificate(OUTPUT)
    run(TOOLS / 'apksigner', 'verify', '--verbose', OUTPUT)
    run(TOOLS / 'zipalign', '-c', '4', OUTPUT)
    changed = []
    with zipfile.ZipFile(BASE) as base, zipfile.ZipFile(OUTPUT) as target:
        assert target.testzip() is None
        for name in base.namelist():
            if not name.startswith('META-INF/') and base.read(name) != target.read(name):
                changed.append(name)
        assert set(changed) == {'AndroidManifest.xml', 'classes2.dex', 'res/raw/video.mp4'}, changed
        assert target.read('res/raw/video.mp4') == (ROOT / 'opening_patch/opening.mp4').read_bytes()
    package = WORK / 'package'
    package.mkdir(exist_ok=True)
    meta = build_delta(BASE, OUTPUT, package / 'opening.patch')
    rebuilt = WORK / 'reconstructed.apk'
    rebuilt.unlink(missing_ok=True)
    apply(BASE, package / 'opening.patch', rebuilt)
    assert sha256(rebuilt) == sha256(OUTPUT)
    run(TOOLS / 'apksigner', 'verify', rebuilt)
    shutil.copy2(ROOT / 'opening_patch/apply_patch.py', package / 'apply_patch.py')
    shutil.copy2(ROOT / 'opening_patch/使用说明.txt', package / '使用说明.txt')
    report = dict(base_sha256=meta['base_sha256'], target_sha256=meta['target_sha256'],
                  target_size=meta['target_size'], changed_entries=changed,
                  version_code=103, certificate_sha256=CERTIFICATE,
                  delta_bytes=(package / 'opening.patch').stat().st_size,
                  compression_changes={'res/raw/video.mp4': 'DEFLATED -> STORED'},
                  exact_reconstruction_verified=True,
                  video_sha256=sha256(ROOT / 'opening_patch/opening.mp4'),
                  video_encoding='H.264 Baseline L3.0, 480x270, 15fps; AAC-LC 44.1kHz mono')
    (package / '校验清单.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    OUTPUT.with_suffix('.sha256').write_text(sha256(OUTPUT) + '  ' + OUTPUT.name + '\n')
    bundle = ROOT / 'build/金箍棒3.87-开场动画补丁-v102到v103.zip'
    with zipfile.ZipFile(bundle, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(package.iterdir()):
            archive.write(path, path.name)
    print(json.dumps(dict(apk=str(OUTPUT), patch=str(bundle), **report), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    build()
