"""Local listener + ADB reverse + Frida DNS/connect hooks; no APK mutation."""
import argparse
import asyncio
import contextlib
import fcntl
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

from android_emulator.config import load_config
from android_emulator.manager import adb, ready_device, error_text
from observability.collector import processes
from observability.events import SessionWriter
from .server import LandingServer

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def state_path(config):
    return config['runtime_dir'] / 'redirect' / 'active.json'


def read_state(config):
    path = state_path(config)
    return json.loads(path.read_text()) if path.exists() else {}


def owned(state):
    pid = state.get('pid')
    if type(pid) is not int or pid <= 1:
        return False
    result = subprocess.run(['ps', '-p', str(pid), '-o', 'command='], capture_output=True, text=True)
    return (result.stdout.strip() == state.get('command') and
            'redirect_game.py' in result.stdout and ' run' in result.stdout)


def ensure_frida(config):
    import frida
    if frida.__version__ != '16.2.1':
        raise RuntimeError('此 Android 6 环境已验证 Frida 16.2.1，请使用项目 .runtime/venv/bin/python')
    device = frida.get_device(config['serial'], timeout=5)
    try:
        device.enumerate_processes()
        return device
    except frida.ServerNotRunningError:
        pass
    if not adb(config, 'shell', 'id').startswith('uid=0('):
        raise RuntimeError('本模式需要目标模拟器的 root adbd')
    binary = config['runtime_dir'] / 'observer/frida-server-16.2.1-android-arm'
    if not binary.is_file():
        raise RuntimeError('缺少 Frida ARM32 server：' + str(binary))
    target = '/data/local/tmp/jgbol-observer-frida'
    adb(config, 'push', binary, target, timeout=60)
    adb(config, 'shell', 'chmod', '755', target)
    adb(config, 'shell', target, '-D', '-l', '127.0.0.1:27042', timeout=30)
    for attempt in range(20):
        try:
            device.enumerate_processes()
            break
        except (frida.TransportError, frida.ServerNotRunningError):
            if attempt == 19:
                raise
            time.sleep(.25)
    return device


async def poll_processes(config, stopped, emit, *, retry_delay=2, deadline=float('inf')):
    """Keep the listener and hooks alive when ADB temporarily stops responding.

    A failed query is not an empty process table: callers must not detach any
    existing session until a complete, successful snapshot is available.
    """
    failures = 0
    while not stopped.is_set() and time.monotonic() < deadline:
        try:
            current = await asyncio.to_thread(processes, config)
        except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
            failures += 1
            if failures == 1 or failures % 30 == 0:
                emit('process_poll_retry', level='W', attempts=failures,
                     message='ADB 进程查询暂时失败，保留本地服务并重试：' + error_text(exc))
            try:
                await asyncio.wait_for(stopped.wait(),
                                       timeout=min(retry_delay, max(0, deadline - time.monotonic())))
            except asyncio.TimeoutError:
                pass
        else:
            if failures:
                emit('process_poll_recovered', attempts=failures,
                     message='ADB 进程查询已恢复')
            return current
    return None


async def run(config, args):
    directory = state_path(config).parent
    directory.mkdir(parents=True, exist_ok=True)
    lock = (directory / 'run.lock').open('w')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError as exc:
        lock.close()
        raise RuntimeError('本项目重定向已在运行；先执行 status 或 stop') from exc
    writer = None
    backend = None
    server = None
    reverse_added = False
    sessions = {}
    retry_after = {}
    spawned = None
    stopped = asyncio.Event()
    loop = asyncio.get_running_loop()
    errors = []
    try:
        await asyncio.to_thread(ready_device, config)
        device = await asyncio.to_thread(ensure_frida, config)
        writer = SessionWriter(directory / 'sessions', dict(package=config['package'],
            serial=config['serial'], port=args.port, mode='local-offline' if args.offline else 'dns-connect-redirect'), console=not args.quiet)
        def emit(kind, **fields):
            message = fields.pop('message', None)
            if message is None:
                if kind == 'dns_redirect':
                    message = f"DNS {fields['host']} → {fields['target']}"
                elif kind == 'connect_redirect':
                    message = f"TCP {fields['original_host']}:{fields['original_port']} → {fields['target']}"
                elif kind == 'http_request':
                    message = f"HTTP {fields['method']} {fields['host']}{fields['path']} → {fields['status']}"
                else:
                    message = kind
            writer.emit(dict(source='network', kind=kind, message=message, **fields))
        tls = None
        ca_path = '/data/local/tmp/jgbol-local-ca.pem'
        if args.offline:
            from .accounts import Accounts
            from .tls import LocalTLS
            backend = Accounts(config['runtime_dir'] / 'offline', args.port, emit)
            tls = await asyncio.to_thread(LocalTLS, config['runtime_dir'] / 'offline/tls')
            await asyncio.to_thread(adb, config, 'push', tls.ca, ca_path)
            await asyncio.to_thread(adb, config, 'shell', 'chmod', '644', ca_path)
        server = LandingServer(args.port, (ROOT / 'analysis/server_lists/server_list.raw.txt').read_bytes(), emit,
                               backend=backend, tls=tls)
        await server.start()
        # Never replace or remove another tool's reverse mapping.
        mappings = await asyncio.to_thread(adb, config, 'reverse', '--list')
        if any(len(line.split()) >= 2 and line.split()[1] == f'tcp:{args.port}' for line in mappings.splitlines()):
            raise RuntimeError(f'设备 tcp:{args.port} 已有 reverse 映射，拒绝接管')
        await asyncio.to_thread(adb, config, 'reverse', '--no-rebind', f'tcp:{args.port}', f'tcp:{args.port}')
        reverse_added = True
        hook_config = dict(port=args.port, offline=args.offline, caPath=ca_path)
        if backend:
            from .summon import client_source
            hook_config['summonClientSource'] = client_source(backend.summon_rules)
        source = 'const REDIRECT_CONFIG = ' + json.dumps(hook_config) + ';\n' + (HERE / 'hooks.js').read_text()
        if args.offline:
            source += '\n' + (HERE / 'summon_client.js').read_text()
            source += '\n' + (HERE / 'offline.js').read_text()
        if args.probe:
            source += '\n' + (HERE / 'probe.js').read_text()
            if args.offline:
                source += '\n' + (HERE / 'native_tls_probe.js').read_text()

        def attach(pid, name):
            session = device.attach(pid)
            def message(msg, data):
                if msg.get('type') == 'send':
                    payload = dict(msg['payload'])
                    kind = payload.pop('kind')
                    emit(kind, process=name, **payload)
                    if kind == 'offline_error':
                        errors.append(payload.get('message', kind))
                else:
                    errors.append(msg.get('stack', str(msg)))
                    emit('hook_error', message=errors[-1], level='E')
            try:
                script = session.create_script(source)
                script.on('message', message)
                script.load()
                status = script.exports_sync.status()
                if not {'connect', 'getaddrinfo'} <= set(status['installed']):
                    raise RuntimeError('必要网络钩子未就绪')
            except Exception:
                session.detach()
                raise
            sessions[pid] = (session, script)
            emit('process_attached', pid=pid, process=name)
            return script

        async def attach_discovered(pid, name):
            if time.monotonic() < retry_after.get(pid, 0):
                return
            try:
                await asyncio.to_thread(attach, pid, name)
                retry_after.pop(pid, None)
            except Exception as exc:
                # SDK workers may exit between ps and injection. Keep the main
                # process redirected, and retry live workers with a backoff.
                retry_after[pid] = time.monotonic() + 5
                emit('attach_retry', pid=pid, process=name, level='W', message=str(exc))

        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, stopped.set)
        if not args.attach:
            await asyncio.to_thread(adb, config, 'shell', 'am', 'force-stop', config['package'])
            spawned = await asyncio.to_thread(device.spawn, [config['package']])
            await asyncio.to_thread(attach, spawned, config['package'])
            await asyncio.to_thread(device.resume, spawned)
            spawned = None
        current = await asyncio.to_thread(processes, config)
        for pid, name in current.items():
            if pid not in sessions:
                if name == config['package']:
                    await asyncio.to_thread(attach, pid, name)
                else:
                    await attach_discovered(pid, name)
        if not any(current.get(pid) == config['package'] for pid in sessions):
            raise RuntimeError('未找到游戏进程；去掉 --attach 以冷启动并注入')
        if args.probe:
            script = next(iter(sessions.values()))[1]
            result = await asyncio.to_thread(script.exports_sync.probe)
            emit('probe_result', result=result)
            if not (result['dns'] == 0 and result['resolved'] == '127.0.0.1'
                    and all(result[key].get('ok') and result[key].get('caller_port_unchanged') for key in ('ipv4', 'ipv6'))):
                raise RuntimeError('本地链路自检失败：' + json.dumps(result))
            if args.offline:
                for _ in range(100):
                    if await asyncio.to_thread(script.exports_sync.offlinestatus):
                        break
                    if errors:
                        raise RuntimeError(errors[0])
                    await asyncio.sleep(.2)
                else:
                    raise RuntimeError('等待本地 SDK/TLS 初始化超时')
                tls_result = await asyncio.to_thread(script.exports_sync.tlsprobe)
                emit('tls_probe_result', result=tls_result)
                if tls_result['status'] != 200:
                    raise RuntimeError('Android HTTPS 自检失败')
                native_result = await asyncio.to_thread(script.exports_sync.nativetlsprobe)
                emit('native_tls_probe_result', result=native_result)
                if native_result != dict(curl_result=0, http_status=200, response_bytes=24):
                    raise RuntimeError('Native HTTPS 自检失败：' + json.dumps(native_result))
        active = dict(pid=os.getpid(), config=str(config['config_path']), package=config['package'],
                      serial=config['serial'], port=args.port, offline=args.offline, session=str(writer.directory),
                      command=subprocess.run(['ps', '-p', str(os.getpid()), '-o', 'command='],
                                             capture_output=True, text=True, check=True).stdout.strip())
        temporary = state_path(config).with_suffix('.tmp')
        temporary.write_text(json.dumps(active, ensure_ascii=False, indent=2) + '\n')
        temporary.replace(state_path(config))
        emit('redirect_ready', message=f'本地重定向已启用，127.0.0.1:{args.port}', **active)
        deadline = time.monotonic() + args.duration if args.duration else float('inf')
        while not stopped.is_set() and time.monotonic() < deadline:
            if errors:
                raise RuntimeError('网络钩子异常：' + errors[0])
            current = await poll_processes(config, stopped, emit, deadline=deadline)
            if current is None:
                break
            for pid in list(sessions):
                if pid not in current or sessions[pid][0].is_detached:
                    session, script = sessions.pop(pid)
                    with contextlib.suppress(Exception):
                        session.detach()
                    emit('process_detached', pid=pid)
            for pid, name in current.items():
                if pid not in sessions:
                    await attach_discovered(pid, name)
            for pid in list(retry_after):
                if pid not in current:
                    retry_after.pop(pid, None)
            try:
                await asyncio.wait_for(stopped.wait(), timeout=.5)
            except asyncio.TimeoutError:
                pass
        return 0
    finally:
        # A failed early injection must never leave a suspended app behind.
        if spawned is not None:
            with contextlib.suppress(Exception):
                await asyncio.to_thread(device.kill, spawned)
        for session, script in sessions.values():
            if args.offline:
                with contextlib.suppress(Exception):
                    await asyncio.to_thread(script.exports_sync.offlinecleanup)
            with contextlib.suppress(Exception):
                await asyncio.to_thread(script.unload)
            with contextlib.suppress(Exception):
                await asyncio.to_thread(session.detach)
        if reverse_added:
            try:
                await asyncio.to_thread(adb, config, 'reverse', '--remove', f'tcp:{args.port}')
            except Exception as exc:
                print('移除 reverse 失败，请设备重连后执行 adb reverse --remove tcp:' + str(args.port) + ': ' + str(exc), file=sys.stderr)
        if server:
            await server.close()
        if backend:
            backend.close()
        if writer:
            writer.emit(dict(kind='redirect_stopped', message='钩子已卸载，本地接收结束'))
            writer.close()
        if state_path(config).exists() and read_state(config).get('pid') == os.getpid():
            state_path(config).unlink()
        lock.close()


def main(argv=None):
    p = argparse.ArgumentParser(description='DNS/寻址 + connect 本地重定向（不修改 APK）')
    p.add_argument('--config', type=Path, default=ROOT / 'game.json')
    sub = p.add_subparsers(dest='command', required=True)
    for command in ('run', 'start'):
        s = sub.add_parser(command, help='前台运行' if command == 'run' else '后台启动')
        s.add_argument('--port', type=int, default=18770)
        s.add_argument('--attach', action='store_true', help='附加现有进程；默认冷启动以覆盖主进程早期请求')
        s.add_argument('--probe', action='store_true', help='用独立测试 socket 验证 DNS、IPv4、IPv6 链路')
        s.add_argument('--duration', type=float, default=0)
        s.add_argument('--quiet', action='store_true')
        s.add_argument('--offline', action='store_true', help='启用本地 TLS、账号注册登录和 LS/BS 业务接入')
    sub.add_parser('status')
    sub.add_parser('stop')
    args = p.parse_args(argv)
    try:
        config = load_config(args.config)
        state = read_state(config)
        if args.command == 'status':
            print(json.dumps(dict(state, running=owned(state)), ensure_ascii=False, indent=2))
            return 0
        if args.command == 'stop':
            if owned(state):
                os.kill(state['pid'], signal.SIGTERM)
                for _ in range(100):
                    if not state_path(config).exists():
                        print('已停止重定向，后续连接恢复原始寻址。')
                        return 0
                    time.sleep(.1)
                raise RuntimeError('停止尚未完成，请检查后台日志')
            print('重定向未运行。')
            return 0
        import math
        if not 1024 <= args.port <= 65535 or not math.isfinite(args.duration) or args.duration < 0:
            raise ValueError('端口须为 1024—65535；duration 须为有限非负数')
        if args.command == 'run':
            return asyncio.run(run(config, args))
        if owned(state):
            if state.get('offline', False) != args.offline or state['port'] != args.port:
                raise RuntimeError('运行参数不同；先 stop，再用新参数 start')
            print('重定向已运行：' + state['session'])
            return 0
        directory = state_path(config).parent
        directory.mkdir(parents=True, exist_ok=True)
        command = [str(config['python_path']), str(ROOT / 'redirect_game.py'), '--config',
                   str(config['config_path']), 'run', '--port', str(args.port), '--duration', str(args.duration)]
        command += [flag for flag, enabled in [('--attach', args.attach), ('--probe', args.probe), ('--quiet', args.quiet), ('--offline', args.offline)] if enabled]
        with (directory / 'controller.log').open('ab') as log:
            child = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        for _ in range(240):
            state = read_state(config)
            if state.get('pid') == child.pid and owned(state):
                print('重定向已启用：' + state['session'])
                return 0
            if child.poll() is not None:
                raise RuntimeError('启动失败，请查看 ' + str(directory / 'controller.log'))
            time.sleep(.25)
        child.terminate()
        raise RuntimeError('启动超时，已请求清理；请检查 controller.log')
    except Exception as exc:
        print(error_text(exc), file=sys.stderr)
        return 1
