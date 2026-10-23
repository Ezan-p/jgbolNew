"""Normalized events, bounded rotating storage and terminal rendering."""
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import threading
import uuid

LEVELS = {'V': 0, 'D': 1, 'I': 2, 'W': 3, 'E': 4, 'F': 5}
THREADTIME = re.compile(
    r'^(\d\d-\d\d\s+\d\d:\d\d:\d\d\.\d+)\s+(\d+)\s+(\d+)\s+([VDIWEFA])\s+([^:]+): ?(.*)$')
SECRET = re.compile(
    r'''(?ix)(["']?(?:access_token|auth_key|password|passwd|token|authorization)["']?\s*[:=]\s*)'''
    r'''(?:"[^"\n]*"|'[^'\n]*'|(?:Bearer\s+|Basic\s+)?[^\s&,;}\]]+)''')


def now():
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds')


def redact(value):
    if isinstance(value, str):
        return SECRET.sub(r'\1[REDACTED]', value)
    if isinstance(value, dict):
        return {str(k): '[REDACTED]' if str(k).lower() in
                ('access_token', 'auth_key', 'password', 'passwd', 'token', 'authorization')
                else redact(v) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v) for v in value]
    return value


def classify(tag, message):
    """Logcat attribution is heuristic; exact Lua events come from the hook."""
    if tag in ('ActivityManager', 'ActivityTaskManager'):
        return 'android'
    text = (tag + ' ' + message).lower()
    if any(s in text for s in ('lua', 'stack traceback', '[string "')):
        return 'lua'
    if 'cocos' in text or 'xiyoujilua' in text:
        return 'engine'
    if tag.lower() in ('androidruntime', 'debug', 'libc'):
        return 'crash'
    return 'android'


def parse_logcat(line):
    match = THREADTIME.match(line.rstrip('\r\n'))
    if not match:
        return None
    stamp, pid, tid, level, tag, message = match.groups()
    tag = tag.strip()
    return dict(device_time=stamp, pid=int(pid), tid=int(tid),
                level='F' if level == 'A' else level, tag=tag,
                source=classify(tag, message), transport='logcat',
                kind='log', message=message)


def matches(event, level='V', sources=(), contains=None):
    return (LEVELS.get(event.get('level'), 2) >= LEVELS[level]
            and (not sources or event.get('source') in sources)
            and (not contains or contains.casefold() in event.get('message', '').casefold()))


def render(event):
    # Escape control characters, including embedded newlines and ANSI sequences.
    message = json.dumps(event.get('message', ''), ensure_ascii=False)[1:-1]
    return (f"{event.get('device_time') or event.get('time', '')} "
            f"{event.get('level', 'I')} {event.get('source', '?')}/"
            f"{event.get('tag', '')} [{event.get('pid', '-')}:{event.get('tid', '-')}] {message}")


class SessionWriter:
    def __init__(self, root, metadata, *, max_bytes=8 * 1024 * 1024, backups=4,
                 level='V', sources=(), contains=None, console=True):
        self.session = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-') + uuid.uuid4().hex[:8]
        self.directory = Path(root) / self.session
        self.directory.mkdir(parents=True)
        self.metadata = dict(metadata, session=self.session, started_at=now(), schema=1)
        (self.directory / 'session.json').write_text(
            json.dumps(redact(self.metadata), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        self.max_bytes, self.backups = max_bytes, backups
        self.level, self.sources, self.contains = level, sources, contains
        self.console = console
        self.lock = threading.Lock()
        self.sequence = 0
        self.counts = Counter()
        self.closed = False
        self.files = {name: (self.directory / name).open('ab') for name in ('events.jsonl', 'console.log')}

    def _write(self, name, text):
        data = text.encode('utf-8')
        stream = self.files[name]
        if stream.tell() and stream.tell() + len(data) > self.max_bytes:
            stream.close()
            path = self.directory / name
            for i in range(self.backups, 0, -1):
                target = Path(str(path) + '.' + str(i))
                source = path if i == 1 else Path(str(path) + '.' + str(i - 1))
                if source.exists():
                    source.replace(target)
            stream = self.files[name] = path.open('wb')
        stream.write(data)
        stream.flush()

    def emit(self, event):
        with self.lock:
            if self.closed:
                return
            self.sequence += 1
            record = dict(time=now(), level='I', source='observer', tag='observer',
                          transport='host', kind='status')
            record.update(redact(event))
            record.update(schema=1, session=self.session, sequence=self.sequence)
            record['message'] = str(record.get('message', ''))[:16384]
            self.counts[record['source']] += 1
            self.counts['level:' + record['level']] += 1
            self._write('events.jsonl', json.dumps(record, ensure_ascii=False) + '\n')
            line = render(record)
            self._write('console.log', line + '\n')
            if self.console and matches(record, self.level, self.sources, self.contains):
                try:
                    print(line, flush=True)
                except BrokenPipeError:
                    self.console = False

    def close(self):
        with self.lock:
            if self.closed:
                return
            self.closed = True
            for stream in self.files.values():
                stream.close()
            (self.directory / 'summary.json').write_text(json.dumps(dict(
                session=self.session, ended_at=now(), events=self.sequence,
                counts=dict(self.counts), retention=dict(max_bytes=self.max_bytes,
                                                       backups=self.backups)),
                ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def replay_paths(path):
    path = Path(path)
    if path.is_dir():
        base = path / 'events.jsonl'
        backups = sorted((p for p in path.glob('events.jsonl.*') if p.suffix[1:].isdigit()),
                         key=lambda p: int(p.suffix[1:]), reverse=True)
        return backups + ([base] if base.exists() else [])
    return [path]
