"""Persistent game time with HTTPS consensus in production entry points.

Policy 3 uses trusted UTC for display and a settlement high-water mark. Policy 2
is retained for old standalone analysis/test callers with no network service;
an already migrated clock never downgrades when the service is unavailable.

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
# Pure offline policy: ordinary reboot gaps are accepted, not authenticated.
WALL_JUMP_TOLERANCE = 5 * 60
MAX_OFFLINE_GAP = 30 * 86400
DEFERRED_MESSAGE = '检测到时间校准或异常离线间隔，该间隔暂未补算；游戏可继续，请检查系统日期。'


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
            # No continuous identity: restart credit uses the bounded wall policy.
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
    def __init__(self, directory, *, source=None, legacy_db=None, network_time=None):
        self.source = source or (network_time.source if network_time else SystemSource())
        self.network_time = network_time
        self.display_time = None
        self.path = str((Path(directory) / 'clock.sqlite3').resolve())
        existed = Path(self.path).exists()
        self.quarantined = False
        self.notice = None
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
                    if network_time is not None:
                        # No gameplay has observed this unverified wall anchor.
                        state.update(policy_version=3, settlement_floor=floor)
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
            if self.network_time is not None or state.get('policy_version') == 3:
                return self._network_sample(state, wall, elapsed)
            same_boot = state['boot'] == self.source.boot_id and elapsed >= state['elapsed']
            wall_keys = ('wall_reference', 'wall_elapsed', 'wall_seen')
            missing_baseline = not any(key in state for key in wall_keys)
            if not missing_baseline and not all(
                    type(state.get(key)) in (int, float) and math.isfinite(state[key])
                    and state[key] >= 0 for key in wall_keys):
                raise RuntimeError('Invalid wall-clock observation record')
            dirty = missing_baseline or state.get('policy_version') != 2
            state['policy_version'] = 2
            delta = elapsed - state['elapsed'] if same_boot else 0

            def defer(reason, seconds, *, active):
                nonlocal dirty
                state['notice_serial'] = state.get('notice_serial', 0) + 1
                state['deferred_gap'] = dict(id=state['notice_serial'], reason=reason,
                    seconds=seconds, observed=wall, game=state['game'], status='uncredited')
                state['deferred_history'] = (state.get('deferred_history', []) +
                                             [state['deferred_gap']])[-16:]
                state['wall_untrusted'] = active
                dirty = True

            if not missing_baseline:
                if same_boot:
                    # Keep the baseline fixed: incremental edits accumulate.
                    # Continuous time remains usable even while wall time is suspect.
                    deviation = wall - (state['wall_reference'] + elapsed - state['wall_elapsed'])
                    if abs(deviation) > WALL_JUMP_TOLERANCE:
                        if not state.get('wall_untrusted'):
                            defer('wall_discontinuity', deviation, active=True)
                    elif state.get('wall_untrusted'):
                        state['wall_untrusted'] = False
                        dirty = True
                else:
                    gap = wall - state['wall_seen']
                    # Never turn an already deferred adjustment into a reboot reward.
                    if state.get('wall_untrusted'):
                        defer('restart_after_discontinuity', gap, active=False)
                    elif gap < -WALL_JUMP_TOLERANCE or gap > MAX_OFFLINE_GAP:
                        defer('backward_reboot' if gap < 0 else 'long_offline_gap', gap, active=False)
                    elif not state.get('quarantined'):
                        delta = max(0, gap)
            if missing_baseline or not same_boot:
                # Upgrade existing saves without treating their dates as proof.
                state.update(wall_reference=wall, wall_elapsed=elapsed, wall_seen=wall)
            self.quarantined = bool(state.get('quarantined'))
            # Preserve old quarantines: historical records do not reliably prove
            # whether a wall anomaly was the only cause. No blanket unblocking.
            self.notice = state.get('deferred_gap')
            game = state['game'] + delta
            # At most one journal write per game second during normal requests.
            # Retain fractional remainder; do not truncate each interval.
            if dirty or not same_boot or int(game) != int(state['game']):
                state.update(game=game, elapsed=elapsed, boot=self.source.boot_id,
                             status='continuous' if same_boot else (
                                 'offline_credited' if delta > 0 else 'restart_reanchored'),
                             wall_seen=wall)
                self._write(state)
            self.display_time = int(game)
            return int(game)

    def _network_sample(self, state, wall, elapsed):
        """Called under the journal transaction; network work never holds its lock.

        Display follows authenticated consensus. Settlement has a high-water
        mark so correcting a future save cannot reopen a previously paid period.
        """
        from . import network_time
        previous = dict(state)
        same_boot = state['boot'] == self.source.boot_id and elapsed >= state['elapsed']
        if state.get('policy_version') != 3:
            state.update(policy_version=3, settlement_floor=state['game'])
        floor = state['settlement_floor']
        if type(floor) not in (int, float) or not math.isfinite(floor) or floor < 0:
            raise RuntimeError('Invalid settlement high-water mark')
        game = state['game'] + (elapsed - state['elapsed'] if same_boot else 0)
        trusted = state.get('network_anchor')
        fresh = False
        observation = None
        if self.network_time is not None:
            self.network_time.request()
            observation = self.network_time.read()
        if (observation is not None and observation.boot == self.source.boot_id
                and 0 <= elapsed - observation.elapsed <= 30
                and observation.token != (trusted or {}).get('token')
                and len(set(observation.hosts)) >= 2
                and set(observation.hosts) <= set(network_time.HOSTS)
                and math.isfinite(observation.epoch) and 1577836800 <= observation.epoch <= 4102444800
                and math.isfinite(observation.uncertainty) and 0 <= observation.uncertainty <= 10):
            game = observation.epoch + elapsed - observation.elapsed
            offset = wall - game
            baseline = state.get('trusted_wall_offset')
            diagnostic = state.get('wall_diagnostic')
            wall_changed = bool(diagnostic and (
                diagnostic['boot'] != self.source.boot_id or
                abs(wall - diagnostic['wall'] - (elapsed - diagnostic['elapsed'])) > WALL_JUMP_TOLERANCE))
            # First verification establishes a baseline; existing date errors are
            # not evidence of cheating. Automatic corrections toward real UTC
            # and VM pauses with a correct wall date must not be punished.
            if (baseline is not None and wall_changed and abs(offset) > WALL_JUMP_TOLERANCE
                    and abs(offset) - abs(baseline) > WALL_JUMP_TOLERANCE):
                state.update(quarantined=True, wall_anomaly=dict(
                    reason='network_confirmed_wall_change', deviation=offset - baseline,
                    observed=wall, trusted=game, hosts=list(observation.hosts)))
            predicted = state['game'] + (elapsed - state['elapsed'] if same_boot else 0)
            server_correction = same_boot and not wall_changed and abs(game - predicted) > WALL_JUMP_TOLERANCE
            if baseline is None or abs(offset) < abs(baseline) or server_correction:
                state['trusted_wall_offset'] = offset
                state['wall_diagnostic'] = dict(wall=wall, elapsed=elapsed, boot=self.source.boot_id)
            elif (not same_boot or (wall_changed and abs(offset) <= WALL_JUMP_TOLERANCE
                                    and abs(game - predicted) > WALL_JUMP_TOLERANCE)):
                # A verified VM pause is a new continuous-observation baseline.
                state['wall_diagnostic'] = dict(wall=wall, elapsed=elapsed, boot=self.source.boot_id)
            state['network_anchor'] = dict(epoch=observation.epoch, elapsed=observation.elapsed,
                boot=observation.boot, hosts=list(observation.hosts), token=observation.token,
                uncertainty=observation.uncertainty)
            state.update(wall_reference=wall, wall_elapsed=elapsed, wall_seen=wall,
                         wall_untrusted=False, status='network_synchronized')
            fresh = True
            trusted = state['network_anchor']
        elif not same_boot:
            state['status'] = 'network_required_after_restart'
            state.update(wall_reference=wall, wall_elapsed=elapsed, wall_seen=wall)
        # Failed requests do not remove trusted anchors or persistent punishment.
        # No wall-clock gap is credited, including before the first network sync.
        uncertain = (not trusted or trusted['boot'] != self.source.boot_id
                     or state.get('status') == 'network_required_after_restart')
        if not fresh and same_boot and trusted:
            wall_expected = state.get('wall_reference', wall) + elapsed - state.get('wall_elapsed', elapsed)
            if abs(wall - wall_expected) > WALL_JUMP_TOLERANCE:
                state['wall_untrusted'] = True
                if self.network_time is not None:
                    self.network_time.request(force=True)
        self.quarantined = bool(state.get('quarantined'))
        self.display_time = int(game)
        settlement = max(floor, game)
        if uncertain or state.get('wall_untrusted'):
            self.notice = dict(id='network-unavailable', message=network_time.WAIT_MESSAGE)
        elif floor - game > 5:
            self.notice = dict(id='future-settlement', message=network_time.FUTURE_MESSAGE)
        else:
            self.notice = None
        state.update(game=game, settlement_floor=settlement, elapsed=elapsed, boot=self.source.boot_id)
        # Preserve subsecond anchors without rewriting a journal on every query.
        if (fresh or not same_boot or int(game) != int(previous['game'])
                or any(state.get(key) != previous.get(key) for key in
                       ('policy_version', 'wall_untrusted', 'quarantined', 'status'))):
            self._write(state)
        return int(settlement)

    def request_network_sync(self):
        if self.network_time is not None:
            self.network_time.request(force=True)

    def close(self):
        self.db.close()


def now():
    context = _context.get()
    # Standalone analysis/unit helpers retain their explicit-time API. All
    # production Backend methods run inside bind_backend's context.
    return context[1] if context is not None else int(time.time())


def display_now():
    context = _context.get()
    return context[2] if context is not None else now()


@contextmanager
def scope(clock):
    context = _context.get()
    if context is not None and context[0] == clock.path:
        yield context[1]
        return
    value = clock.sample()
    token = _context.set((clock.path, value, getattr(clock, 'display_time', None) or value))
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
