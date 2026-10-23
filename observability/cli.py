"""CLI: observe, snapshot, doctor, and replay. Default mode has no pip dependencies."""
import argparse
import importlib.util
import json
from pathlib import Path
import signal
import subprocess
import sys
import threading
import time

from android_emulator.config import load_config
from android_emulator.manager import adb, ready_device, error_text
from .collector import LogcatCollector, FridaCollector, processes
from .events import LEVELS, SessionWriter, matches, render, replay_paths

ROOT = Path(__file__).resolve().parents[1]


def parser():
    p = argparse.ArgumentParser(description='金箍棒 Cocos2d-x / Lua 统一观测工具')
    p.add_argument('--config', type=Path, default=ROOT / 'game.json')
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('doctor', help='检查设备、游戏进程和可选依赖')
    for name in ('collect', 'snapshot', 'replay'):
        s = sub.add_parser(name)
        s.add_argument('--level', choices=LEVELS, default='V', help='终端最低级别；不影响保存')
        s.add_argument('--source', action='append', default=[], choices=['engine', 'lua', 'android', 'crash', 'observer'])
        s.add_argument('--contains', help='终端消息筛选（忽略大小写）')
        if name == 'replay':
            s.add_argument('path', type=Path, help='会话目录或 JSONL 文件')
            continue
        s.add_argument('--output', type=Path, help='会话根目录，默认 .runtime/observations')
        s.add_argument('--max-mb', type=float, default=8, help='每个日志文件滚动阈值，默认 8 MiB')
        s.add_argument('--backups', type=int, default=4, help='每种日志保留的旧分卷数，默认 4')
        s.add_argument('--quiet', action='store_true', help='仅保存，隐藏逐条日志')
        if name == 'collect':
            s.add_argument('--duration', type=float, default=0, help='采集秒数，0 表示持续到 Ctrl+C')
            s.add_argument('--history', action='store_true', help='先采集现有 logcat 缓冲区')
            s.add_argument('--launch', action='store_true', help='开始采集后启动游戏 Activity')
            s.add_argument('--hook', action='store_true', help='使用 Frida 补充 Lua 日志钩子')
    return p


def replay(args):
    paths = replay_paths(args.path)
    if not paths:
        raise ValueError('未找到 events.jsonl')
    errors = 0
    for path in paths:
        with path.open(encoding='utf-8') as stream:
            for number, line in enumerate(stream, 1):
                try:
                    event = json.loads(line)
                    if not isinstance(event, dict) or not isinstance(event.get('message'), str):
                        raise ValueError('不是事件对象')
                    if matches(event, args.level, args.source, args.contains):
                        print(render(event))
                except (ValueError, TypeError, KeyError) as exc:
                    errors += 1
                    print(f'{path}:{number}: 跳过损坏记录：{exc}', file=sys.stderr)
    return 1 if errors else 0


def collect(config, args):
    import math
    if not math.isfinite(args.max_mb) or args.max_mb < .01 or args.backups < 1:
        raise ValueError('--max-mb 必须是至少 0.01 的有限值，--backups 必须至少为 1')
    duration = getattr(args, 'duration', 0)
    if not math.isfinite(duration) or duration < 0:
        raise ValueError('--duration 必须是非负有限值')
    device = ready_device(config)
    writer = SessionWriter(args.output or config['runtime_dir'] / 'observations',
        dict(package=config['package'], serial=config['serial'], device=device,
             mode=args.command, hook_requested=getattr(args, 'hook', False)),
        max_bytes=int(args.max_mb * 1024 * 1024), backups=args.backups,
        level=args.level, sources=args.source, contains=args.contains, console=not args.quiet)
    print('观测会话：' + str(writer.directory), file=sys.stderr, flush=True)
    stopped = threading.Event()
    old_handlers = {}
    collector = LogcatCollector(config, writer, snapshot=args.command == 'snapshot',
                                history=getattr(args, 'history', False))
    hook = None
    result = 0
    try:
        for sig in (signal.SIGINT, signal.SIGTERM):
            old_handlers[sig] = signal.signal(sig, lambda *_: stopped.set())
        writer.emit(dict(message='开始统一日志采集'))
        collector.start()
        if getattr(args, 'hook', False):
            hook = FridaCollector(config, writer)
            hook.update(collector.filter.pids)
        if getattr(args, 'launch', False):
            output = adb(config, 'shell', 'am', 'start', '-W', '-n', config['component'], timeout=120)
            if 'Error' in output or 'Exception' in output:
                raise RuntimeError(output)
            writer.emit(dict(kind='launch', message=output))
        deadline = time.monotonic() + duration if duration else float('inf')
        while not stopped.is_set() and time.monotonic() < deadline:
            if not collector.pump():
                break
            if hook:
                hook.update(collector.filter.pids)
            stopped.wait(.05)
    except Exception as exc:
        result = 1
        writer.emit(dict(level='E', kind='collector_error', message=error_text(exc)))
        print('采集失败：' + error_text(exc), file=sys.stderr)
    finally:
        collector.close()
        while not collector.rows.empty():
            collector.pump(final=True)
        if hook:
            hook.close()
        writer.emit(dict(message='采集结束', kind='session_end', exit_code=result))
        writer.close()
        for sig, handler in old_handlers.items():
            signal.signal(sig, handler)
    return result


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == 'replay':
            return replay(args)
        config = load_config(args.config)
        if args.command == 'doctor':
            device = ready_device(config)
            print(json.dumps(dict(device=device, processes=processes(config),
                                  frida_installed=importlib.util.find_spec('frida') is not None,
                                  hook_script=str(ROOT / 'observability/hooks/cocos_lua.js')),
                             ensure_ascii=False, indent=2))
            return 0
        return collect(config, args)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        print(error_text(exc), file=sys.stderr)
        return 1
