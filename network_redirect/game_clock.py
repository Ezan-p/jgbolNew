"""Persistent offline game time. Wall time is only an unverified first anchor.

A separate journal is committed BEFORE gameplay; failed requests cannot roll it
back. No rewards live here. Role balances and settlement receipts retain their
existing single-database transaction. Never monkeypatch Python's time module.
"""
from contextvars import ContextVar
from contextlib import contextmanager
from functools import wraps, lru_cache
from datetime import date
import ctypes
import json
import math
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import time
import uuid

_context = ContextVar('game_clock', default=None)
_PROCESS_BOOT = 'process:' + uuid.uuid4().hex
_android_boot = None


def configure_android(files_dir):
    """Called before opening backends; Java writes identity on EVERY startup."""
    global _android_boot
    try:
        value = (Path(files_dir) / 'clock_boot_id').read_text().strip()
    except FileNotFoundError:
        # Old shells receiving a Python-only update have no bridge marker.
        # SystemSource will try the kernel identity, then a process-only ID.
        _android_boot = None
        return
    if not value or len(value) > 200:
        raise RuntimeError('Invalid Android clock boot identity')
    _android_boot = 'android:' + value


@lru_cache(maxsize=1)
def _mac_boot_identity():
    try:
        return subprocess.check_output(['/usr/sbin/sysctl', '-n', 'kern.bootsessionuuid'],
                                       text=True, stderr=subprocess.DEVNULL, timeout=2).strip()
    except (OSError, subprocess.SubprocessError):
        return None


class SystemSource:
    def __init__(self):
        self.wall = time.time
        if sys.platform.startswith('linux'):
            # Android/Linux CLOCK_BOOTTIME counts suspend, unlike MONOTONIC.
            if hasattr(time, 'CLOCK_BOOTTIME'):
                self.elapsed = lambda: time.clock_gettime(time.CLOCK_BOOTTIME)
            else:
                class Timespec(ctypes.Structure):
                    _fields_ = [('seconds', ctypes.c_long), ('nanos', ctypes.c_long)]
                libc = ctypes.CDLL(None, use_errno=True)
                def elapsed():
                    result = Timespec()
                    if libc.clock_gettime(7, ctypes.byref(result)) != 0:
                        raise OSError(ctypes.get_errno(), 'CLOCK_BOOTTIME unavailable')
                    return result.seconds + result.nanos / 1e9
                self.elapsed = elapsed
            try:
                identity = Path('/proc/sys/kernel/random/boot_id').read_text().strip()
            except OSError:
                identity = None
            self.boot_id = _android_boot or ('linux:' + identity if identity else _PROCESS_BOOT)
        elif sys.platform == 'darwin':
            # mach_continuous_time includes sleep on supported development Macs.
            class Timebase(ctypes.Structure):
                _fields_ = [('numer', ctypes.c_uint32), ('denom', ctypes.c_uint32)]
            lib = ctypes.CDLL('/usr/lib/libSystem.B.dylib')
            scale = Timebase()
            lib.mach_timebase_info(ctypes.byref(scale))
            lib.mach_continuous_time.restype = ctypes.c_uint64
            self.elapsed = lambda: lib.mach_continuous_time() * scale.numer / scale.denom / 1e9
            identity = _mac_boot_identity()
            self.boot_id = 'mac:' + identity if identity else _PROCESS_BOOT
        else:
            # Conservative fallback: no cross-process offline credit.
            self.elapsed = time.monotonic
            self.boot_id = _PROCESS_BOOT
        self.elapsed()  # Fail closed if the promised continuous source is absent.


def legacy_floor(db):
    """Keep observed history; never use expiration/end times as clock anchors."""
    floor = 0
    def visit(value):
        nonlocal floor
        if isinstance(value, dict):
            for key, item in value.items():
                if (key == 'clock' or key.endswith('_clock') or key.endswith('_recovery_at')):
                    if type(item) is int and 0 <= item <= 253402300799:
                        floor = max(floor, item)
                if key in {'day', 'shop_day', 'rank_day', 'strength_day', 'start_day', 'week_start_day'}:
                    # Existing game rules use UTC+8 day IDs; exclude counts,
                    # future deadlines and unrelated arbitrary numeric fields.
                    day_id = item
                    if isinstance(item, str):
                        try:
                            day_id = (date.fromisoformat(item) - date(1970, 1, 1)).days
                        except ValueError:
                            day_id = None
                    if type(day_id) is int and 0 <= day_id <= 2932896:
                        floor = max(floor, day_id * 86400 - 28800)
                visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)
    for row in db.execute('SELECT data FROM roles'):
        visit(json.loads(row[0]))
    return floor


class GameClock:
    def __init__(self, directory, *, source=None, legacy_db=None):
        self.source = source or SystemSource()
        self.path = str((Path(directory) / 'clock.sqlite3').resolve())
        existed = Path(self.path).exists()
        self.db = sqlite3.connect(self.path, timeout=10)
        try:
            os.chmod(self.path, 0o600)
            self.db.execute('PRAGMA synchronous=FULL')
            self.db.execute('CREATE TABLE IF NOT EXISTS clock (id INTEGER PRIMARY KEY CHECK(id=1), data TEXT NOT NULL)')
            with self.db:
                self.db.execute('BEGIN IMMEDIATE')
                if self.db.execute('SELECT 1 FROM clock WHERE id=1').fetchone() is None:
                    if existed:
                        raise RuntimeError('Existing game clock has no anchor; refusing to reset')
                    floor = legacy_floor(legacy_db) if legacy_db is not None else 0
                    initial = max(float(self.source.wall()), floor)
                    state = dict(version=1, boot=self.source.boot_id, elapsed=self.source.elapsed(),
                                 game=initial, status='initial_unverified', legacy_floor=floor)
                    self._write(state)
            self.sample()
        except BaseException:
            self.db.close()
            raise

    def _write(self, state):
        self.db.execute('INSERT OR REPLACE INTO clock VALUES (1, ?)', (json.dumps(state),))

    def sample(self):
        """Serialize across accounts/processes. Journal before any reward work."""
        with self.db:
            self.db.execute('BEGIN IMMEDIATE')
            elapsed = self.source.elapsed()
            if not math.isfinite(elapsed) or elapsed < 0:
                raise RuntimeError('Invalid monotonic clock')
            row = self.db.execute('SELECT data FROM clock WHERE id=1').fetchone()
            if row is None:
                raise RuntimeError('Game clock state missing; refusing to reinitialize')
            state = json.loads(row[0])
            if (state.get('version') != 1 or not isinstance(state.get('boot'), str)
                    or not all(type(state.get(k)) in (int, float) and math.isfinite(state[k])
                               and state[k] >= 0 for k in ('game', 'elapsed'))):
                raise RuntimeError('Invalid game clock state; refusing wall-clock fallback')
            same_boot = state['boot'] == self.source.boot_id and elapsed >= state['elapsed']
            game = state['game'] + (elapsed - state['elapsed'] if same_boot else 0)
            # At most one journal write per game second during normal requests.
            # Retain fractional remainder; do not truncate each interval.
            if not same_boot or int(game) != int(state['game']):
                state.update(game=game, elapsed=elapsed, boot=self.source.boot_id,
                             status='continuous' if same_boot else 'restart_gap_discarded')
                self._write(state)
            return int(game)

    def close(self):
        self.db.close()


def now():
    context = _context.get()
    # Standalone analysis/unit helpers retain their explicit-time API. All
    # production Backend methods run inside bind_backend's context.
    return context[1] if context is not None else int(time.time())


@contextmanager
def scope(clock):
    context = _context.get()
    if context is not None and context[0] == clock.path:
        yield context[1]
        return
    token = _context.set((clock.path, clock.sample()))
    try:
        yield _context.get()[1]
    finally:
        _context.reset(token)


def bind_backend(cls):
    """One snapshot for an outer Backend call, including nested save/helpers."""
    def decorate(fn):
        @wraps(fn)
        def wrapped(self, *args, **kwargs):
            with scope(self.clock):
                return fn(self, *args, **kwargs)
        return wrapped
    for name, fn in list(vars(cls).items()):
        if callable(fn) and not name.startswith('__') and name != 'close':
            setattr(cls, name, decorate(fn))
    return cls
