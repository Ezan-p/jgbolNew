"""Device inspection and lifecycle management, isolated by runtime directory."""
import json
import os
import signal
import socket
import subprocess
import time
from pathlib import Path
from .config import abi_error, device_environment, required_abis
from .profiles import emulator_command, emulator_environment, profile_for


def listening(port):
    with socket.socket() as sock:
        sock.settimeout(.3)
        return sock.connect_ex(('127.0.0.1', port)) == 0


def adb(config, *args, timeout=15):
    return subprocess.run([str(config['adb_path']), '-s', config['serial'], *map(str, args)],
                          env=device_environment(config), check=True, timeout=timeout,
                          capture_output=True, text=True).stdout.strip()


def inspect_device(config, *, apk=None):
    if not config['adb_path'].is_file():
        raise RuntimeError('未找到 ADB：' + str(config['adb_path']) + '。请部署 SDK 或配置 adb_path。')
    if adb(config, 'get-state') != 'device':
        raise RuntimeError('指定设备尚未连接或授权：' + config['serial'])
    if config['mode'] == 'emulator':
        names = adb(config, 'emu', 'avd', 'name').splitlines()
        if not names or names[0] != config['avd_name']:
            raise RuntimeError('设备不是本项目的 ' + config['avd_name'] + ' AVD，拒绝操作。')
    def prop(key):
        return adb(config, 'shell', 'getprop', key)
    abis, abis32 = prop('ro.product.cpu.abilist'), prop('ro.product.cpu.abilist32')
    if not abis:
        abis = ','.join(filter(None, (prop('ro.product.cpu.abi'), prop('ro.product.cpu.abi2'))))
    booted = prop('sys.boot_completed') == '1'
    required = required_abis(config, apk)
    error = abi_error(abis, abis32, required)
    return dict(serial=config['serial'], android=prop('ro.build.version.release'),
                abis=abis, abis32=abis32, required_abis=required, booted=booted,
                compatible=error is None, issue=error if booted else '安卓尚未完成启动，请稍后重试。')


def ready_device(config, *, apk=None):
    device = inspect_device(config, apk=apk) if apk is not None else inspect_device(config)
    if device['issue']:
        raise RuntimeError(device['issue'])
    return device


def error_text(exc):
    if isinstance(exc, subprocess.CalledProcessError):
        return (exc.stderr or exc.stdout or str(exc)).strip()
    return str(exc)


class Manager:
    def __init__(self, config, *, gateway_command=None):
        self.config = config
        self.runtime = config['runtime_dir']
        self.state_path = self.runtime / 'processes.json'
        self.python = config['python_path']
        self.gateway_command = gateway_command or [str(self.python), str(Path(__file__).with_name('run.py')),
                                                   '--config', str(config['config_path']), 'serve']

    def environment(self):
        for name in ('android-user', 'logs', 'pycache'):
            (self.runtime / name).mkdir(parents=True, exist_ok=True)
        return device_environment(self.config)

    def read_state(self):
        return json.loads(self.state_path.read_text()) if self.state_path.exists() else {}

    def write_state(self, state):
        self.runtime.mkdir(parents=True, exist_ok=True)
        if state:
            temporary = self.state_path.with_suffix('.tmp')
            temporary.write_text(json.dumps(state))
            temporary.replace(self.state_path)
        elif self.state_path.exists():
            self.state_path.unlink()

    def command_for(self, name):
        if name == 'emulator':
            return emulator_command(self.config)
        if name == 'gateway':
            return list(map(str, self.gateway_command))
        for service in self.config['services']:
            if service['name'] == name:
                return [str(self.python), str(service['script'])]
        return None

    def owned_pid(self, name, pid):
        if type(pid) is not int or pid <= 1:
            return False
        command = self.command_for(name)
        if command is None:
            return False
        result = subprocess.run(['ps', '-p', str(pid), '-o', 'command='], capture_output=True, text=True)
        # ps can omit quoting around spaces in paths. Match full command arguments
        # in order; emulator ownership also requires the selected AVD and port.
        actual = result.stdout.strip()
        if name == 'emulator':
            executable = str(profile_for(self.config)['emulator'])
            return (actual.startswith(executable + ' ') and
                    f"-avd {self.config['avd_name']} " in actual + ' ' and
                    f"-port {self.config['console_port']} " in actual + ' ')
        # Python may print its resolved executable rather than its venv alias.
        expected = ' '.join(command[1:])
        return actual.endswith(' ' + expected)

    def wait_for_port(self, port, process, timeout=60):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise RuntimeError(f'服务退出（端口 {port}），请检查 {self.runtime}/logs/')
            if listening(port):
                return
            time.sleep(.25)
        raise RuntimeError(f'等待端口 {port} 超时，请检查 {self.runtime}/logs/')

    def spawn(self, name, port, state, *, env=None, timeout=15):
        with (self.runtime / 'logs' / (name + '.log')).open('ab') as log:
            process = subprocess.Popen(self.command_for(name), env=env or self.environment(),
                                       stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        state[name] = process.pid
        self.write_state(state)
        self.wait_for_port(port, process, timeout)

    def start(self):
        config = self.config
        self.environment()
        if not self.python.is_file():
            raise RuntimeError('缺少 Python 环境：' + str(self.python) + '；请安装 requirements.lock.txt。')
        state = self.read_state()
        targets = [('gateway', config['web_port'])] + [(s['name'], s['port']) for s in config['services']]
        if config['mode'] == 'emulator':
            targets.insert(0, ('emulator', config['grpc_port']))
        for name, port in targets:
            if listening(port) and (name not in state or not self.owned_pid(name, state[name])):
                raise RuntimeError(f'端口 {port} 属于未跟踪的服务，拒绝接管。')
            if not listening(port) and name in state and self.owned_pid(name, state[name]):
                raise RuntimeError(f'{name} 进程仍在启动或异常，请检查日志；拒绝重复启动。')
        for service in config['services']:
            if not service['script'].is_file():
                raise RuntimeError('缺少附加服务脚本：' + str(service['script']))
        if config['mode'] == 'emulator' and not listening(config['grpc_port']):
            if not profile_for(config)['emulator'].is_file() or not (self.runtime / 'avd' / (config['avd_name'] + '.ini')).is_file():
                raise RuntimeError('尚未部署内置模拟器/AVD，请完成环境部署，或使用 adb 模式。')
            if listening(config['console_port']) or listening(config['console_port'] + 1):
                raise RuntimeError('安卓控制/ADB 端口已占用，拒绝替换其他模拟器。')
            self.spawn('emulator', config['grpc_port'], state, env=emulator_environment(config), timeout=60)
        if config['mode'] == 'adb':
            ready_device(config)
        for service in config['services']:
            if not listening(service['port']):
                self.spawn(service['name'], service['port'], state)
        if not listening(config['web_port']):
            self.spawn('gateway', config['web_port'], state)
        print(f"{config['title']}游戏台：http://127.0.0.1:{config['web_port']}；使用 doctor 检查设备兼容性。")

    def stop(self, gateway_only=False):
        state = self.read_state()
        # Close browser clients and optional services before the emulator.
        for name, pid in reversed(list(state.items())):
            if gateway_only and name != 'gateway':
                continue
            if self.config['mode'] == 'adb' and name == 'emulator':
                continue
            if self.owned_pid(name, pid):
                try:
                    os.kill(pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                for _ in range(50):
                    if not self.owned_pid(name, pid):
                        break
                    time.sleep(.1)
                if self.owned_pid(name, pid):
                    raise RuntimeError(f'{name} 尚未退出，保留进程记录，请稍后重试。')
            state.pop(name, None)
            self.write_state(state)
        print('已停止本项目服务。ADB 模式下不会关闭外部设备或模拟器。')

    def launch(self):
        ready_device(self.config)
        output = adb(self.config, 'shell', 'am', 'start', '-W', '-n', self.config['component'], timeout=120)
        if any(text in output for text in ('Error:', 'Error type', 'Exception')):
            raise RuntimeError(output)
        print(output)

    def install(self, apk=None):
        apk = Path(apk).expanduser().resolve() if apk else self.config.get('apk')
        if not apk or not apk.is_file():
            raise RuntimeError('未找到 APK，请配置 apk 或使用 install --apk /路径/游戏.apk。')
        ready_device(self.config, apk=apk)
        print(adb(self.config, 'install', '--no-streaming', '-r', str(apk), timeout=600))
        # Reuse the checked APK's ABI list even when --apk overrides the config.
        original = self.config
        try:
            self.config = {**original, 'required_abis': required_abis(original, apk)}
            self.launch()
        finally:
            self.config = original

    def doctor(self):
        config = self.config
        report = dict(game=config['title'], mode=config['mode'], runtime_profile=config['runtime_profile'],
                      runtime_dir=str(self.runtime), package=config['package'], component=config['component'],
                      apk_exists=bool(config.get('apk') and config['apk'].is_file()),
                      ports={str(config[k]): listening(config[k]) for k in ('console_port', 'grpc_port', 'web_port')},
                      services={s['name']: dict(port=s['port'], listening=listening(s['port'])) for s in config['services']})
        try:
            report['device'] = inspect_device(config)
            ok = not report['device']['issue'] and all(s['listening'] for s in report['services'].values())
        except (RuntimeError, OSError, ValueError, subprocess.SubprocessError) as exc:
            report['device_error'] = error_text(exc)
            ok = False
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return ok
