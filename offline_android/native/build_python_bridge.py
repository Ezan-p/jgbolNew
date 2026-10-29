"""Compile the ARM32 JNI CPython host with the project's existing LLVM tools."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / '.runtime/offline-toolchain'


def build():
    TOOLS.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).with_name('python_bridge.c')
    obj = TOOLS / 'python_bridge.o'
    output = TOOLS / 'libpython_bootstrap.so'
    # Import libraries are generated solely for the linker. The device supplies
    # the real libc.so; these harmless symbol stubs must never enter the APK.
    stubs = TOOLS / 'link-stubs'
    stubs.mkdir(exist_ok=True)
    assembly = stubs / 'libc.s'
    assembly.write_text('.syntax unified\n.arm\n.text\n' + ''.join(
        f'.global {name}\n.type {name}, %function\n{name}:\n bx lr\n'
        for name in ('free', 'malloc', 'snprintf', 'strdup', 'strlen')))
    subprocess.run(['/usr/bin/clang', '--target=armv7a-linux-androideabi21', '-marm',
                    '-fPIC', '-c', str(assembly), '-o', str(stubs / 'libc.o')], check=True)
    lld = ROOT / '.runtime/sdk/build-tools/35.0.0/lld-bin/lld'
    subprocess.run([str(lld), '-flavor', 'gnu', '-shared', '-soname', 'libc.so',
                    str(stubs / 'libc.o'), '-o', str(stubs / 'libc.so')], check=True)
    subprocess.run(['/usr/bin/clang', '--target=armv7a-linux-androideabi21', '-marm',
                    '-fPIC', '-O2', '-fno-stack-protector', '-fvisibility=hidden',
                    '-c', str(source), '-o', str(obj)], check=True)
    subprocess.run([str(lld), '-flavor', 'gnu', '-shared', '--hash-style=both', '--no-undefined',
                    '-soname', 'libpython_bootstrap.so', '-z', 'max-page-size=16384',
                    '-o', str(output), str(obj), str(stubs / 'libc.so'),
                    str(TOOLS / 'python-arm32/jniLibs/armeabi-v7a/libpython3.11.so')], check=True)
    return output


if __name__ == '__main__':
    print(build())
