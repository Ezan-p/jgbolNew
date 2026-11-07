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
import hashlib
import hmac
import secrets
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
# Wall time is diagnostic only; it must never advance reward time.
WALL_JUMP_TOLERANCE = 5 * 60


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
        self.quarantined = False
        self.db = sqlite3.connect(self.path, timeout=10)
        try:
            os.chmod(self.path, 0o600)
            self.db.execute('PRAGMA synchronous=FULL')
            self.db.execute('CREATE TABLE IF NOT EXISTS clock (id INTEGER PRIMARY KEY CHECK(id=1), data TEXT NOT NULL)')
            self.db.execute('CREATE TABLE IF NOT EXISTS clock_integrity (id INTEGER PRIMARY KEY CHECK(id=1), data TEXT NOT NULL, seal TEXT NOT NULL)')
            key_path = Path(directory) / 'clock_integrity.key'
            if not key_path.exists():
                if self.db.execute('SELECT 1 FROM clock_integrity').fetchone():
                    raise RuntimeError('时钟校验密钥缺失，请恢复完整备份')
                try:
                    with key_path.open('xb') as stream:
                        stream.write(secrets.token_bytes(32))
                    key_path.chmod(0o600)
                except FileExistsError:
                    pass
            self.integrity_key = key_path.read_bytes()
            if len(self.integrity_key) != 32:
                raise RuntimeError('时钟校验密钥无效')
            with self.db:
                self.db.execute('BEGIN IMMEDIATE')
                if self.db.execute('SELECT 1 FROM clock WHERE id=1').fetchone() is None:
                    if existed:
                        raise RuntimeError('Existing game clock has no anchor; refusing to reset')
                    floor = legacy_floor(legacy_db) if legacy_db is not None else 0
                    wall = float(self.source.wall())
                    elapsed = self.source.elapsed()
                    initial = max(wall, floor)
                    state = dict(version=1, boot=self.source.boot_id, elapsed=elapsed,
                                 game=initial, status='initial_unverified', legacy_floor=floor,
                                 wall_reference=wall, wall_elapsed=elapsed, wall_seen=wall)
                    self._write(state)
            self.sample()
        except BaseException:
            self.db.close()
            raise

    def _write(self, state):
        state['integrity_version'] = 1
        data = json.dumps(state)
        seal = hmac.new(self.integrity_key, data.encode(), hashlib.sha256).hexdigest()
        self.db.execute('INSERT OR REPLACE INTO clock VALUES (1, ?)', (data,))
        self.db.execute('INSERT OR REPLACE INTO clock_integrity VALUES (1, ?, ?)', (data, seal))

    def sample(self):
        """Serialize across accounts/processes. Journal before any reward work."""
        with self.db:
            self.db.execute('BEGIN IMMEDIATE')
            elapsed = self.source.elapsed()
            if not math.isfinite(elapsed) or elapsed < 0:
                raise RuntimeError('Invalid monotonic clock')
            wall = float(self.source.wall())
            if not math.isfinite(wall) or wall < 0:
                raise RuntimeError('Invalid system clock')
            row = self.db.execute('SELECT data FROM clock WHERE id=1').fetchone()
            if row is None:
                raise RuntimeError('Game clock state missing; refusing to reinitialize')
            state = json.loads(row[0])
            if (state.get('version') != 1 or not isinstance(state.get('boot'), str)
                    or not all(type(state.get(k)) in (int, float) and math.isfinite(state[k])
                               and state[k] >= 0 for k in ('game', 'elapsed'))):
                raise RuntimeError('Invalid game clock state; refusing wall-clock fallback')
            checkpoint = self.db.execute('SELECT data,seal FROM clock_integrity WHERE id=1').fetchone()
            if checkpoint is not None:
                data, seal = checkpoint
                expected = hmac.new(self.integrity_key, data.encode(), hashlib.sha256).hexdigest()
                if not hmac.compare_digest(expected, seal):
                    raise RuntimeError('可信时钟校验记录损坏，请恢复完整备份')
                if json.loads(data) != state:
                    # A valid-shaped edited clock must not advance any rewards.
                    state = json.loads(data)
                    state['quarantined'] = True
                    self._write(state)
            else:
                if state.get('integrity_version'):
                    raise RuntimeError('可信时钟校验记录缺失，请恢复完整备份')
                # One-time upgrade of the previous clock schema, no guilt inferred.
                self._write(state)
            same_boot = state['boot'] == self.source.boot_id and elapsed >= state['elapsed']
            wall_keys = ('wall_reference', 'wall_elapsed', 'wall_seen')
            missing_baseline = not any(key in state for key in wall_keys)
            if not missing_baseline and not all(
                    type(state.get(key)) in (int, float) and math.isfinite(state[key])
                    and state[key] >= 0 for key in wall_keys):
                raise RuntimeError('Invalid wall-clock observation record')
            dirty = missing_baseline
            if not missing_baseline and not state.get('quarantined'):
                # Keep one baseline per boot, so small repeated edits accumulate.
                expected_wall = state['wall_reference'] + elapsed - state['wall_elapsed']
                deviation = wall - (expected_wall if same_boot else state['wall_seen'])
                # Across reboots, forward gaps cannot be distinguished from a
                # normal shutdown offline. Backward movement is still observable.
                if ((same_boot and abs(deviation) > WALL_JUMP_TOLERANCE) or
                        (not same_boot and deviation < -WALL_JUMP_TOLERANCE)):
                    state.update(quarantined=True, wall_anomaly=dict(
                        direction='forward' if deviation > 0 else 'backward',
                        deviation=deviation, observed=wall))
                    dirty = True
            if missing_baseline or not same_boot:
                # Upgrade existing saves without treating their dates as proof.
                state.update(wall_reference=wall, wall_elapsed=elapsed, wall_seen=wall)
            self.quarantined = bool(state.get('quarantined'))
            game = state['game'] + (elapsed - state['elapsed'] if same_boot else 0)
            # At most one journal write per game second during normal requests.
            # Retain fractional remainder; do not truncate each interval.
            if dirty or not same_boot or int(game) != int(state['game']):
                state.update(game=game, elapsed=elapsed, boot=self.source.boot_id,
                             status='continuous' if same_boot else 'restart_gap_discarded',
                             wall_seen=max(state['wall_seen'], wall))
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
