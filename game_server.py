"""Standalone loopback game receiver with session logs and a real socket probe."""
import argparse
import asyncio
import contextlib
import errno
import hashlib
import json
import math
from pathlib import Path
import signal
import sys

from network_redirect.server import HEALTH, LIST_PATHS, LandingServer
from observability.events import SessionWriter


ROOT = Path(__file__).resolve().parent
SERVER_LIST = ROOT / 'analysis/server_lists/server_list.raw.txt'
SESSION_ROOT = ROOT / '.runtime/server/sessions'


def port_number(value):
    try:
        port = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError('端口须为 1024—65535 的整数') from exc
    if not 1024 <= port <= 65535:
        raise argparse.ArgumentTypeError('端口须为 1024—65535 的整数')
    return port


def duration_seconds(value):
    try:
        duration = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError('duration 须为有限非负数；0 表示持续运行') from exc
    if not math.isfinite(duration) or duration < 0:
        raise argparse.ArgumentTypeError('duration 须为有限非负数；0 表示持续运行')
    return duration


def event_message(kind, fields):
    if kind == 'local_accept':
        return f"接收连接：{fields.get('peer', '?')}"
    if kind == 'http_request':
        return (f"HTTP {fields['method']} {fields.get('host', '')}{fields['path']} "
                f"→ {fields['status']}，响应 {fields['response_bytes']} 字节")
    if kind == 'tcp_received':
        return f"TCP 收到 {fields['bytes']} 字节；累计 {fields.get('total_bytes', fields['bytes'])} 字节"
    if kind == 'tls_received':
        return f"TLS 请求已到达，收到 {fields['bytes']} 字节；基础模式不提供握手"
    if kind == 'local_connection_end':
        return f"连接结束：{fields.get('reason', 'closed')}"
    if kind == 'probe_result':
        return f"自检 {'通过' if fields['ok'] else '失败'}：{fields['path']}"
    return kind


async def probe(port, server_list, emit):
    """Check health and both cached list URLs through actual loopback sockets."""
    async def request(path, expected):
        reader, writer = await asyncio.open_connection('127.0.0.1', port, limit=16384)
        try:
            writer.write((f'GET {path} HTTP/1.1\r\nHost: 127.0.0.1:{port}\r\n'
                          'Connection: close\r\n\r\n').encode('ascii'))
            await writer.drain()
            head = await reader.readuntil(b'\r\n\r\n')
            lines = head.decode('iso-8859-1').split('\r\n')
            status = int(lines[0].split(' ', 2)[1])
            headers = dict(line.split(':', 1) for line in lines[1:] if ':' in line)
            content_length = next((value.strip() for key, value in headers.items()
                                   if key.lower() == 'content-length'), None)
            if status != 200 or content_length != str(len(expected)):
                raise RuntimeError(f'响应不符：HTTP {status}，Content-Length={content_length}')
            body = await reader.readexactly(len(expected))
            if body != expected or await reader.read(1):
                raise RuntimeError('响应内容与本地快照不一致')
            return dict(status=status, response_bytes=len(body),
                        sha256=hashlib.sha256(body).hexdigest())
        finally:
            writer.close()
            with contextlib.suppress(OSError):
                await writer.wait_closed()

    for path, expected in [('/__redirect_health', HEALTH),
                           *[(path, server_list) for path in sorted(LIST_PATHS)]]:
        try:
            result = await asyncio.wait_for(request(path, expected), timeout=5)
        except (OSError, ValueError, IndexError, RuntimeError, asyncio.TimeoutError,
                asyncio.IncompleteReadError, asyncio.LimitOverrunError) as exc:
            emit('probe_result', path=path, ok=False, level='E', reason=type(exc).__name__,
                 message=f'自检失败：{path}（{type(exc).__name__}）')
            raise RuntimeError(f'本地服务自检失败：{path}（{type(exc).__name__}）') from exc
        emit('probe_result', path=path, ok=True, **result)


async def run(args):
    server_list = SERVER_LIST.read_bytes()
    writer = SessionWriter(SESSION_ROOT, dict(mode='basic-server', host='127.0.0.1',
        port=args.port, server_list=str(SERVER_LIST), server_list_bytes=len(server_list)),
        console=not args.quiet)

    def emit(kind, **fields):
        message = fields.pop('message', None)
        if message is None:
            message = event_message(kind, fields)
        elif kind in ('tcp_received', 'tls_received'):
            message = event_message(kind, fields) + '；' + message
        writer.emit(dict(source='server', tag='receiver', kind=kind, message=message, **fields))

    server = LandingServer(args.port, server_list, emit)
    stopped = asyncio.Event()
    loop = asyncio.get_running_loop()
    installed_signals = []
    reason = 'startup_failed'

    def stop(sig):
        nonlocal reason
        reason = signal.Signals(sig).name
        stopped.set()

    try:
        for sig in (signal.SIGINT, signal.SIGTERM):
            previous = signal.getsignal(sig)
            loop.add_signal_handler(sig, stop, sig)
            installed_signals.append((sig, previous))
        try:
            await server.start()
        except OSError as exc:
            if exc.errno == errno.EADDRINUSE:
                raise RuntimeError(f'127.0.0.1:{args.port} 已被占用；请先停止占用它的服务，'
                                   '或使用 --port 选择其他端口。') from exc
            raise
        endpoint = f'http://127.0.0.1:{server.port}'
        message = f'基础服务端已启动：{endpoint}；日志：{writer.directory}'
        emit('server_started', message=message, endpoint=endpoint,
             log_directory=str(writer.directory), port=server.port)
        if args.quiet:
            print(message, flush=True)
        print('按 Ctrl+C 停止服务。', flush=True)
        reason = 'stopped'
        if args.probe:
            await probe(server.port, server_list, emit)
        if args.duration:
            try:
                await asyncio.wait_for(stopped.wait(), timeout=args.duration)
            except asyncio.TimeoutError:
                reason = 'duration_elapsed'
        else:
            await stopped.wait()
        return 0
    except asyncio.CancelledError:
        reason = 'cancelled'
        raise
    except (OSError, RuntimeError, ValueError) as exc:
        if reason != 'startup_failed':
            reason = 'error'
        emit('server_error', level='E', message=str(exc), reason=type(exc).__name__)
        raise
    finally:
        try:
            await server.close()
        finally:
            emit('server_stopped', message=f'基础服务端已停止（{reason}）', reason=reason)
            writer.close()
            for sig, previous in installed_signals:
                loop.remove_signal_handler(sig)
                signal.signal(sig, previous)


def main(argv=None):
    parser = argparse.ArgumentParser(description='基础游戏服务端：监听本机请求并记录日志，无需模拟器或 Frida。')
    parser.add_argument('--port', type=port_number, default=18770, help='监听端口，默认 18770')
    parser.add_argument('--duration', type=duration_seconds, default=0,
                        help='自动停止前运行的秒数，0 表示持续运行（默认）')
    parser.add_argument('--quiet', action='store_true', help='不在终端逐条显示事件，仍保存完整日志')
    parser.add_argument('--probe', action='store_true', help='启动后通过真实连接自检健康端点和服务器列表')
    parser.add_argument('--summon-status', action='store_true',
                        help='校验共享的召唤推测配置并显示启用状态后退出，不启动监听')
    args = parser.parse_args(argv)
    try:
        if args.summon_status:
            from network_redirect.summon import rule_status
            print(json.dumps(rule_status(), ensure_ascii=False, indent=2))
            return 0
        return asyncio.run(run(args))
    except KeyboardInterrupt:
        return 130
    except (OSError, RuntimeError, ValueError) as exc:
        print(f'基础服务端错误：{exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
