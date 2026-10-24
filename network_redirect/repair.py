"""Explicit recovery for stale Frida after an Android runtime restart."""
import fcntl
import os
import signal
import time

from android_emulator.manager import adb
from observability.collector import package_processes
from .cli import owned, read_state, state_path

TARGET = '/data/local/tmp/jgbol-observer-frida'


def reset_login(config):
    """Stop only this project's controller and injection binary; preserve data."""
    directory = state_path(config).parent
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / 'repair.lock').open('w') as repair_lock:
        try:
            fcntl.flock(repair_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError('另一个登录修复正在进行，请等待完成') from exc
        state = read_state(config)
        if state and (state.get('config') != str(config['config_path']) or
                      state.get('serial') != config['serial']):
            raise RuntimeError('服务状态不属于当前配置，拒绝清理')
        print('正在停止旧登录服务……', flush=True)
        if owned(state):
            os.kill(state['pid'], signal.SIGTERM)
            deadline = time.monotonic() + 12
            while owned(state) and time.monotonic() < deadline:
                time.sleep(.2)
            if owned(state):
                print('旧服务停止超时，结束已核验的项目进程。', flush=True)
                os.kill(state['pid'], signal.SIGKILL)
        # Wait for the controller's lock, including after forced termination.
        with (directory / 'run.lock').open('a') as run_lock:
            deadline = time.monotonic() + 5
            while True:
                try:
                    fcntl.flock(run_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() >= deadline:
                        raise RuntimeError('仍有本地服务占用锁，停止修复以避免冲突')
                    time.sleep(.1)
            # Stop the app before removing its in-memory hooks.
            adb(config, 'shell', 'am', 'force-stop', config['package'], timeout=30)
            output = adb(config, 'shell', 'ps', timeout=15)
            for pid, name in package_processes(output, TARGET).items():
                if name != TARGET:
                    continue
                command = adb(config, 'shell', 'cat', f'/proc/{pid}/cmdline', timeout=10)
                if command.split('\x00')[0] != TARGET:
                    raise RuntimeError('注入进程身份已变化，请重新运行修复')
                adb(config, 'shell', 'kill', '-9', str(pid), timeout=10)
            # A crashed controller can leave its own reverse mapping behind.
            if state:
                port = state.get('port')
                if type(port) is not int or not 1024 <= port <= 65535:
                    raise RuntimeError('旧服务端口无效，拒绝清理映射')
                mappings = adb(config, 'reverse', '--list').splitlines()
                if any(line.split()[1:] == [f'tcp:{port}', f'tcp:{port}'] for line in mappings):
                    adb(config, 'reverse', '--remove', f'tcp:{port}')
                if state_path(config).exists():
                    state_path(config).unlink()
        print('旧登录注入已清理，正在重新启动并自检……', flush=True)
