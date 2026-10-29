"""Fetch and verify fixed ARM32 CPython build inputs; never contacts a device.

Run once online, then use --offline for repeat builds. All downloads are cached
under .runtime/offline-toolchain. Android system libraries are NOT copied: the
native build scripts generate link-time symbol stubs with the original SONAME.
The stubs are not runtime implementations and must never be packaged in an APK.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / '.runtime/offline-toolchain'
MAVEN = 'https://repo.maven.apache.org/maven2/'
ARTIFACTS = {
    'target-3.11.0-2-armeabi-v7a.zip': (
        MAVEN + 'com/chaquo/python/target/3.11.0-2/target-3.11.0-2-armeabi-v7a.zip',
        '501fcc51608a2d5c11d9dcd468fe14e3183724f634a39fa0bcb35372ef20b08a'),
    'target-3.11.0-2-stdlib.zip': (
        MAVEN + 'com/chaquo/python/target/3.11.0-2/target-3.11.0-2-stdlib.zip',
        '73fc09eca913690809e6aec36f39b4475055062c10313c5fdc2a683e0b4e7257'),
    'android.jar': (
        MAVEN + 'com/google/android/android/4.1.1.4/android-4.1.1.4.jar',
        '84072541cbb711eff89f7277100ff854929a446dba7ceb1b195c340e0b4fd3cb'),
}


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def acquire(name, url, expected, offline):
    destination = CACHE / name
    if destination.exists():
        if sha256(destination) != expected:
            raise RuntimeError(f'缓存校验失败，请检查并移走后重试：{destination}')
        return destination
    if offline:
        raise RuntimeError(f'缺少离线构建缓存：{destination}\n下载来源：{url}\nSHA256：{expected}')
    temporary = destination.with_name(destination.name + '.download')
    try:
        with urllib.request.urlopen(url, timeout=60) as response, temporary.open('wb') as stream:
            shutil.copyfileobj(response, stream)
        if sha256(temporary) != expected:
            raise RuntimeError(f'下载校验失败：{url}')
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)
    return destination


def extract_python(archive):
    destination = CACHE / 'python-arm32'
    with zipfile.ZipFile(archive) as source:
        members = [entry for entry in source.infolist() if not entry.is_dir()]
        for entry in members:
            path = Path(entry.filename)
            if path.is_absolute() or '..' in path.parts:
                raise RuntimeError('Unsafe archive path: ' + entry.filename)
        # Verify extracted bytes too, so a stale marker cannot hide corruption.
        matches = destination.is_dir() and all(
            (destination / entry.filename).is_file()
            and (destination / entry.filename).read_bytes() == source.read(entry)
            for entry in members)
        if matches:
            return destination
        if destination.exists():
            raise RuntimeError(f'已提取的Python目录与固定版本不符：{destination}；请检查后移走再重试')
        stage = CACHE / ('python-arm32.extracting-' + str(os.getpid()))
        try:
            stage.mkdir()
            source.extractall(stage)
            stage.replace(destination)
        finally:
            if stage.exists():
                shutil.rmtree(stage)
    return destination


def prepare(offline=False):
    CACHE.mkdir(parents=True, exist_ok=True)
    for name, (url, expected) in ARTIFACTS.items():
        acquire(name, url, expected, offline)
    runtime = extract_python(CACHE / 'target-3.11.0-2-armeabi-v7a.zip')
    report = {
        'artifacts': {name: {'url': url, 'sha256': digest}
                      for name, (url, digest) in ARTIFACTS.items()},
        'python_include': str(runtime / 'include/python3.11'),
        'python_native': str(runtime / 'jniLibs/armeabi-v7a'),
        'python_modules': str(runtime / 'lib-dynload/armeabi-v7a'),
        'python_stdlib': str(CACHE / 'target-3.11.0-2-stdlib.zip'),
        'jni_system_libraries': 'Generated link-time stubs only; never package libc.so/libdl.so/liblog.so.',
    }
    (CACHE / 'toolchain-manifest.json').write_text(json.dumps(report, indent=2) + '\n')
    required = [ROOT / '.runtime/sdk/build-tools/35.0.0/lld-bin/lld',
                ROOT / '.runtime/sdk/build-tools/35.0.0/d8', Path('/usr/bin/clang')]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError('还需现有项目Android SDK 35.0.0构建工具和Xcode Command Line Tools：' + ', '.join(missing))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--offline', action='store_true', help='仅验证已有缓存，不访问网络')
    args = parser.parse_args()
    prepare(args.offline)
    print('ARM32 Python/Android 构建缓存校验完成：' + str(CACHE))
