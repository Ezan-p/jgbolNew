"""Android 6-compatible logcat collection with dynamic package PID tracking."""
from collections import deque
import queue
import re
import subprocess
import threading
import time
from pathlib import Path

from android_emulator.config import device_environment
from android_emulator.manager import adb
from .events import parse_logcat


def package_processes(output, package):
    lines = output.splitlines()
    if not lines:
        raise RuntimeError('ps 未返回进程表')
    header = lines[0].split()
    if 'PID' not in header or not any(x in header for x in ('NAME', 'CMD', 'COMMAND', 'ARGS')):
        raise RuntimeError('无法识别设备 ps 表头：' + lines[0])
    pid_column = header.index('PID')
    found = {}
    for line in lines[1:]:
        columns = line.split()
        if len(columns) <= pid_column:
            continue
        name = columns[-1]
        if name == package or name.startswith(package + ':'):
            try:
                found[int(columns[pid_column])] = name
            except ValueError:
                continue
    return found


def processes(config):
    # API 23 toolbox ps has no -A; newer toybox ps needs -A for all processes.
    try:
        output = adb(config, 'shell', 'ps', '-A', timeout=5)
        if len(output.strip().splitlines()) <= 1:
            # Android 6 silently interprets -A as an unmatched process name.
            raise RuntimeError('ps -A 仅返回表头')
        return package_processes(output, config['package'])
    except (RuntimeError, subprocess.CalledProcessError):
        return package_processes(adb(config, 'shell', 'ps', timeout=5), config['package'])


class PackageFilter:
    def __init__(self, package):
        self.package = package
        self.pids = {}
        self.crash_writers = {}

    def accepts(self, event, clock=None):
        clock = time.monotonic() if clock is None else clock
        self.crash_writers = {k: v for k, v in self.crash_writers.items() if v > clock}
        if event['pid'] in self.pids:
            event['process'] = self.pids[event['pid']]
            return True
        # debuggerd writes the native stack under its own PID. Admit only a
        # positively identified crash block, never every device-wide DEBUG log.
        key = (event['pid'], event['tid'])
        if event['tag'] in ('DEBUG', 'crash_dump32', 'crash_dump64'):
            message = event['message']
            if '*** ***' in message or '>>> ' in message:
                self.crash_writers.pop(key, None)
            marker = re.search(r'>>>\s*([^ ]+)\s*<<<', message)
            if marker and (marker[1] == self.package or marker[1].startswith(self.package + ':')):
                self.crash_writers[key] = clock + 10
            if key in self.crash_writers:
                event['source'] = 'crash'
                event['process'] = self.package
                return True
        # Explicit process lifecycle records help correlate launches and ANRs.
        return event['tag'] in ('ActivityManager', 'ActivityTaskManager') and bool(
            re.search(r'(?<![\w.])' + re.escape(self.package) + r'(?![\w.])', event['message']))


class LogcatCollector:
    def __init__(self, config, writer, *, snapshot=False, history=False):
        self.config, self.writer = config, writer
        self.snapshot, self.history = snapshot, history
        self.filter = PackageFilter(config['package'])
        self.pending = deque(maxlen=4096)
        self.dropped = 0
        self.rows = queue.Queue(maxsize=8192)
        self.done = threading.Event()
        self.proc = None
        self.reader = None
        self.last_poll = 0

    def refresh(self):
        found = processes(self.config)
        if found != self.filter.pids:
            self.writer.emit(dict(kind='processes', message='游戏进程更新', pids=found))
            self.filter.pids = found
        self.last_poll = time.monotonic()

    def start(self):
        self.refresh()
        args = ['logcat', '-b', 'main', '-b', 'system', '-b', 'crash', '-v', 'threadtime']
        if self.snapshot:
            args += ['-d']
        elif not self.history:
            args += ['-T', '1']
        # Explicit *:V overrides device/shell default tag filtering.
        args += ['*:V']
        self.proc = subprocess.Popen(
            [str(self.config['adb_path']), '-s', self.config['serial'], *args],
            env=device_environment(self.config), stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace', bufsize=1)
        self.reader = threading.Thread(target=self._read, daemon=True)
        self.reader.start()

    def _read(self):
        try:
            for line in self.proc.stdout:
                while not self.done.is_set():
                    try:
                        self.rows.put(line, timeout=.1)
                        break
                    except queue.Full:
                        continue
                if self.done.is_set():
                    break
        finally:
            self.done.set()

    def pump(self, final=False):
        clock = time.monotonic()
        if clock - self.last_poll >= 1 and not self.snapshot and not final:
            self.refresh()
        # Bound each batch so a noisy game cannot starve signals/PID refresh.
        for _ in range(2000):
            try:
                line = self.rows.get_nowait()
            except queue.Empty:
                break
            event = parse_logcat(line)
            if event:
                if self.filter.accepts(event):
                    self.writer.emit(event)
                elif not self.snapshot:
                    if len(self.pending) == self.pending.maxlen:
                        self.dropped += 1
                    self.pending.append((clock, event))
            elif line.strip() and not line.startswith('---------'):
                self.writer.emit(dict(level='W', kind='logcat_diagnostic', message=line.strip()[:2000]))
        waiting = deque(maxlen=self.pending.maxlen)
        for arrived, event in self.pending:
            if self.filter.accepts(event):
                self.writer.emit(event)
            elif clock - arrived < 3:
                waiting.append((arrived, event))
        self.pending = waiting
        if self.dropped:
            self.writer.emit(dict(level='W', kind='overflow', message='待归属日志缓冲溢出',
                                  dropped=self.dropped))
            self.dropped = 0
        if self.done.is_set() and self.rows.empty() and not final:
            code = self.proc.wait(timeout=5)
            if code or not self.snapshot:
                raise RuntimeError(f'logcat 采集结束（退出码 {code}），请检查设备连接后重新采集。')
            return False
        return True

    def close(self):
        self.done.set()
        if self.proc:
            if self.proc.poll() is None:
                self.proc.terminate()
                try:
                    self.proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    self.proc.kill()
                    self.proc.wait(timeout=3)
            if self.reader:
                self.reader.join(timeout=3)
            self.proc.stdout.close()


class FridaCollector:
    """Optional attachment, pinned to the exact configured ADB device and PID."""
    def __init__(self, config, writer):
        try:
            import frida
        except ImportError as exc:
            raise RuntimeError('缺少可选依赖 frida；请参照 docs/观测工具.md 安装，或去掉 --hook。') from exc
        self.device = frida.get_device(config['serial'], timeout=5)
        self.config, self.writer = config, writer
        self.session = self.script = None
        self.pid = None
        self.detached = threading.Event()
        self.last_attempt = 0
        self.failure = None
        self.source = (Path(__file__).parent / 'hooks/cocos_lua.js').read_text(encoding='utf-8')

    def on_message(self, message, data):
        if message.get('type') == 'send' and isinstance(message.get('payload'), dict):
            payload = message['payload']
            if payload.get('type') == 'events':
                for event in payload.get('events', [])[:256]:
                    self.writer.emit(dict(event, transport='frida', pid=self.pid))
            else:
                self.writer.emit(dict(source='observer', transport='frida', kind='hook_status',
                                      level='W' if payload.get('errors') or payload.get('missing') else 'I',
                                      message=str(payload), details=payload, pid=self.pid))
        else:
            self.failure = message.get('stack', str(message))
            self.writer.emit(dict(level='E', source='observer', transport='frida',
                                  kind='hook_error', message=self.failure, pid=self.pid))

    def attach(self, pid):
        self.close()
        self.detached.clear()
        self.pid = pid
        try:
            self.session = self.device.attach(pid)
            session = self.session
            def detached(*args):
                if self.session is session:
                    self.detached.set()
            def message_received(message, data):
                if self.session is session:
                    self.on_message(message, data)
            self.session.on('detached', detached)
            self.script = self.session.create_script(self.source)
            self.script.on('message', message_received)
            self.script.load()
        except Exception:
            self.close()
            raise
        self.writer.emit(dict(kind='hook_attached', message='已附加 Lua 观测脚本；覆盖情况见 hook_status', pid=pid))

    def update(self, pids):
        if self.failure:
            raise RuntimeError('Frida 脚本异常：' + self.failure)
        pid = next((p for p, name in pids.items() if name == self.config['package']), None)
        if self.pid and (self.detached.is_set() or self.pid != pid):
            self.writer.emit(dict(level='W', kind='hook_detached', message='游戏进程退出或钩子连接断开', pid=self.pid))
            self.close()
        if pid and not self.session and time.monotonic() - self.last_attempt >= 5:
            self.last_attempt = time.monotonic()
            self.attach(pid)

    def close(self):
        if self.script:
            try:
                self.script.exports_sync.flush()
                self.script.unload()
            except Exception:
                pass  # Target may already have exited; do not hide collector errors.
        if self.session:
            try:
                self.session.detach()
            except Exception:
                pass
        self.session = self.script = self.pid = None
