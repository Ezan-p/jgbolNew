"""Build the small ARM32 native adapter with the existing Clang and SDK LLD.

The generated import stubs are link-time only, never packaged. At runtime the
Android linker resolves the named standard libraries supplied by the device.
"""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
ENGINE_SHA256 = '1ea4ed769527deae3ee79c60d2c749c6f4834b9c321f012d5784318d3112fe86'
IMPORTS = {
    'libc.so': 'mmap mprotect cacheflush open close read malloc free memcpy memset memcmp strlen strcmp snprintf getpeername getsockopt connect gethostbyname getaddrinfo clock_gettime',
    'libdl.so': 'dlopen dlsym dladdr',
    'liblog.so': '__android_log_print',
}


def build(output=None):
    source = ROOT / 'jgbol3.87/lib/armeabi/libxiyoujilua.so'
    if hashlib.sha256(source.read_bytes()).hexdigest() != ENGINE_SHA256:
        raise RuntimeError('Native adapter only supports the frozen 3.87 ARM32 engine')
    work = ROOT / '.runtime/offline-native'
    work.mkdir(parents=True, exist_ok=True)
    output = Path(output) if output else work / 'liboffline.so'
    output.parent.mkdir(parents=True, exist_ok=True)
    clang = '/usr/bin/clang'
    lld = ROOT / '.runtime/sdk/build-tools/35.0.0/lld-bin/lld'
    common = [clang, '--target=armv7a-linux-androideabi21', '-marm', '-fPIC']
    stubs = []
    for library, functions in IMPORTS.items():
        asm = work / (library + '.s')
        asm.write_text('.syntax unified\n.arm\n.text\n' + ''.join(
            f'.global {name}\n.type {name}, %function\n{name}:\n bx lr\n' for name in functions.split()))
        obj = asm.with_suffix('.o')
        subprocess.run(common + ['-c', str(asm), '-o', str(obj)], check=True)
        stub = work / library
        subprocess.run([str(lld), '-flavor', 'gnu', '-shared', '--hash-style=both', '-soname', library, str(obj), '-o', str(stub)], check=True)
        stubs.append(str(stub))
    obj = work / 'offline.o'
    subprocess.run(common + ['-Os', '-fno-stack-protector', '-fno-builtin', '-fvisibility=hidden', '-Wall', '-Wextra', '-Werror', '-c',
                            str(Path(__file__).with_name('offline.c')), '-o', str(obj)], check=True)
    subprocess.run([str(lld), '-flavor', 'gnu', '-shared', '--hash-style=both', '--no-undefined', '-soname', 'liboffline.so',
                    '-z', 'max-page-size=4096', str(obj), *stubs, '-o', str(output)], check=True)
    report = {'engine_sha256': ENGINE_SHA256, 'adapter_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
              'abi': 'armeabi-v7a', 'external_instrumentation': False,
              'jni': 'com.jgbol.offline.NativeBridge.install(String programRoot, String caPath)'}
    output.with_suffix('.json').write_text(json.dumps(report, indent=2) + '\n')
    print(output)
    return output


if __name__ == '__main__':
    build()
