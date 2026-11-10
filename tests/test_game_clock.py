"""Real clock journal with fake OS inputs, never mocking the effective game time."""
import ast
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from network_redirect import game_clock, activity_babel
from network_redirect.backend import Backend
from network_redirect.protocol import encode, decode

NOW = 1792814400


class Source:
    boot_id = 'boot-a'
    seconds = 100.0
    wall_seconds = NOW

    def wall(self):
        return self.wall_seconds

    def elapsed(self):
        return self.seconds

    def advance(self, seconds):
        self.seconds += seconds
        self.wall_seconds += seconds


class ClockTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)
        self.source = Source()

    def clock(self):
        clock = game_clock.GameClock(self.path, source=self.source)
        self.addCleanup(clock.close)
        return clock

    def test_forward_backward_and_incremental_wall_changes_ignored(self):
        clock = self.clock()
        for step, wall in enumerate([NOW + 365*86400, NOW - 365*86400, NOW, NOW+20, NOW+40]):
            self.source.wall_seconds = wall
            self.source.seconds = 100 + step*10
            self.assertEqual(clock.sample(), NOW + step*10)

    def test_both_wall_jumps_are_deferred_without_quarantine_across_reopen(self):
        for offset in (86400, -86400):
            with self.subTest(offset=offset), tempfile.TemporaryDirectory() as directory:
                source = Source()
                clock = game_clock.GameClock(directory, source=source)
                source.wall_seconds += offset
                self.assertEqual(clock.sample(), NOW)
                self.assertFalse(clock.quarantined)
                self.assertIsNotNone(clock.notice)
                source.wall_seconds = NOW
                source.boot_id = 'boot-b'
                source.seconds = 10
                clock.close()
                clock = game_clock.GameClock(directory, source=source)
                try:
                    self.assertFalse(clock.quarantined)
                    self.assertIsNotNone(clock.notice)
                    self.assertEqual(clock.sample(), NOW)
                finally:
                    clock.close()

    def test_small_adjustments_accumulate_against_fixed_baseline(self):
        clock = self.clock()
        self.source.wall_seconds += game_clock.WALL_JUMP_TOLERANCE
        clock.sample()
        self.assertFalse(clock.quarantined)
        self.source.advance(60)
        clock.sample()
        self.assertFalse(clock.quarantined)
        self.source.wall_seconds += 1
        clock.sample()
        self.assertFalse(clock.quarantined)
        self.assertIsNotNone(clock.notice)

    def test_normal_elapsed_sleep_and_reboot_do_not_quarantine(self):
        clock = self.clock()
        self.source.advance(30 * 86400)
        self.assertEqual(clock.sample(), NOW + 30 * 86400)
        self.assertFalse(clock.quarantined)
        self.source.boot_id = 'boot-b'
        self.source.seconds = 10
        self.source.wall_seconds += 7 * 86400
        clock.sample()
        self.assertFalse(clock.quarantined)
        self.source.advance(600)
        clock.sample()
        self.assertFalse(clock.quarantined)

    def test_reboot_backward_date_is_detected(self):
        clock = self.clock()
        self.source.advance(86400)
        clock.sample()
        self.source.boot_id = 'boot-b'
        self.source.seconds = 10
        self.source.wall_seconds -= 86400
        clock.sample()
        self.assertFalse(clock.quarantined)
        self.assertIsNotNone(clock.notice)

    def test_old_signed_clock_establishes_wall_baseline_without_penalty(self):
        clock = self.clock()
        state = json.loads(clock.db.execute('SELECT data FROM clock').fetchone()[0])
        for key in ('wall_reference', 'wall_elapsed', 'wall_seen'):
            del state[key]
        with clock.db:
            clock._write(state)
        self.source.wall_seconds += 365 * 86400
        self.assertEqual(clock.sample(), NOW)
        self.assertFalse(clock.quarantined)
        self.source.wall_seconds += 86400
        clock.sample()
        self.assertFalse(clock.quarantined)
        self.assertIsNotNone(clock.notice)

    def test_android_bridge_old_shell_fallback_and_invalid_marker(self):
        with patch.object(game_clock, '_android_boot', None):
            game_clock.configure_android(self.path)
            self.assertIsNone(game_clock._android_boot)
            marker = self.path / 'clock_boot_id'
            marker.write_text('device:test:count:12')
            game_clock.configure_android(self.path)
            self.assertEqual(game_clock._android_boot, 'android:device:test:count:12')
            marker.write_text('')
            with self.assertRaises(RuntimeError):
                game_clock.configure_android(self.path)

    def test_process_restart_counts_sleep_and_offline_same_boot(self):
        self.clock()
        self.source.seconds += 3*86400
        self.source.wall_seconds += 365*86400
        restarted = self.clock()
        self.assertEqual(restarted.sample(), NOW+3*86400)
        self.assertFalse(restarted.quarantined)
        self.assertIsNotNone(restarted.notice)

    def test_device_restart_discards_unknown_gap_even_when_uptime_grows(self):
        first = self.clock()
        self.source.seconds += 60
        self.assertEqual(first.sample(), NOW+60)
        self.source.boot_id = 'boot-b'
        self.source.seconds = 900000  # Comparison alone cannot identify reboots.
        self.source.wall_seconds += 365*86400
        second = self.clock()
        self.assertEqual(second.sample(), NOW+60)
        self.source.seconds += 30
        self.assertEqual(second.sample(), NOW+90)
        self.assertEqual(first.sample(), NOW+90)

    def test_fractional_progress_not_lost_to_frequent_requests(self):
        clock = self.clock()
        for step in range(1, 101):
            self.source.seconds = 100 + step/10
            clock.sample()
        self.assertEqual(clock.sample(), NOW+10)

    def test_repeated_abnormally_long_reboot_gaps_are_not_credited(self):
        clock = self.clock()
        for reboot in range(10):
            self.source.boot_id = 'restart-' + str(reboot)
            self.source.seconds = 5000 + reboot*10000
            self.source.wall_seconds += 31*86400
            self.assertEqual(clock.sample(), NOW)

    def test_shared_accounts_do_not_double_count(self):
        one, two = self.clock(), self.clock()
        self.source.seconds += 60
        self.assertEqual(one.sample(), NOW+60)
        self.assertEqual(two.sample(), NOW+60)
        self.source.seconds += 60
        self.assertEqual(two.sample(), NOW+120)
        self.assertEqual(one.sample(), NOW+120)

    def test_corrupt_and_missing_row_fail_closed(self):
        clock = self.clock()
        with clock.db:
            clock.db.execute('UPDATE clock SET data=?', ('{}',))
        with self.assertRaises(RuntimeError):
            clock.sample()
        with self.assertRaises(RuntimeError):
            self.clock()
        with clock.db:
            clock.db.execute('DELETE FROM clock')
        with self.assertRaises(RuntimeError):
            clock.sample()
        with self.assertRaises(RuntimeError):
            self.clock()

    def test_legacy_clock_preserved_not_future_expiry(self):
        db = sqlite3.connect(':memory:')
        self.addCleanup(db.close)
        db.execute('CREATE TABLE roles (data TEXT)')
        role = {'activity': {'babel': {'clock': NOW+1000}}, 'expiry': NOW+90000,
                'journey': {'strength_recovery_at': NOW+2000}}
        db.execute('INSERT INTO roles VALUES (?)', (json.dumps(role),))
        clock = game_clock.GameClock(self.path, source=self.source, legacy_db=db)
        self.addCleanup(clock.close)
        self.assertEqual(clock.sample(), NOW+2000)
        self.assertFalse(clock.quarantined)

    def test_legacy_daily_only_history_does_not_move_backwards(self):
        db = sqlite3.connect(':memory:')
        self.addCleanup(db.close)
        db.execute('CREATE TABLE roles (data TEXT)')
        db.execute('INSERT INTO roles VALUES (?)', (json.dumps({'summon': {'day': '2026-11-05'}}),))
        clock = game_clock.GameClock(self.path, source=self.source, legacy_db=db)
        self.addCleanup(clock.close)
        self.assertEqual(clock.sample(), 1793808000)  # Nov 5, 00:00 UTC+8.

    def test_context_one_sample_and_cleanup_on_failure(self):
        @game_clock.bind_backend
        class Example:
            def __init__(self, clock):
                self.clock = clock
            def inner(self):
                return game_clock.now()
            def outer(self):
                first = game_clock.now()
                self.clock.source.seconds += 50
                return first, self.inner()
            def failure(self):
                raise ValueError('rejected')
        obj = Example(self.clock())
        self.assertEqual(obj.outer(), (NOW, NOW))
        with self.assertRaises(ValueError):
            obj.failure()
        self.assertIsNone(game_clock._context.get())
        self.source.boot_id = 'boot-b'
        self.assertEqual(self.clock().sample(), NOW+50)

    def test_production_wall_reads_are_explicitly_allowlisted(self):
        root = Path(__file__).resolve().parents[1] / 'network_redirect'
        allowed = {'game_clock.py', 'accounts.py'}
        offending = []
        for path in root.glob('*.py'):
            if path.name in allowed:
                continue
            for node in ast.walk(ast.parse(path.read_text())):
                if not isinstance(node, ast.Call):
                    continue
                name = ast.unparse(node.func)
                if name in ('time.time', 'datetime.now', 'datetime.today', 'date.today'):
                    offending.append((path.name, node.lineno, name))
        self.assertEqual(offending, [])


class BackendClockTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)
        self.source = Source()
        patcher = patch('network_redirect.game_clock.SystemSource', return_value=self.source)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.backend = Backend(self.path, 18770, lambda *a, **k: None)
        self.addCleanup(lambda: self.backend.close())
        role = self.backend.profile()
        role.update(level=60, strength=0, energy=0)
        self.backend.save(role)
        self.backend.snapshot()
        role = self.backend.profile()
        role.update(strength=0, energy=0)
        activity_babel.state(role, NOW, self.backend.activity_rules)
        self.backend.save(role)

    def test_global_snapshot_ignores_forward_and_backward_wall_time(self):
        original = self.backend.snapshot()
        # Warm once; subsequent snapshots must be stable at fixed game time.
        original = self.backend.snapshot()
        for offset in (86400, 8*86400, 365*86400, -365*86400, 0):
            self.source.wall_seconds = NOW+offset
            current = self.backend.snapshot()
            self.assertEqual(current['time_guard']['blocked'], [])
            self.assertEqual(current, original)
        self.assertEqual(current['server_time'], NOW)

    def test_real_elapsed_restores_resources_and_daily_state_then_restart(self):
        original = self.backend.snapshot()
        self.source.advance(1800)
        current = self.backend.snapshot()
        self.assertEqual(current['strength'], original['strength']+1)
        self.assertEqual(current['activity']['babel']['energy_tick'], (NOW+1800)//1800)
        self.source.advance(86400)
        current = self.backend.snapshot()
        self.assertGreater(current['activity']['babel']['shop_day'], original['activity']['babel']['shop_day'])
        self.backend.close()
        self.source.wall_seconds += 365*86400
        self.backend = Backend(self.path, 18770, lambda *a, **k: None)
        self.assertEqual(self.backend.snapshot()['server_time'], NOW+88200)
        self.source.boot_id = 'boot-b'
        self.source.seconds = 15
        self.assertEqual(self.backend.snapshot()['server_time'], NOW+88200)

    def test_new_account_cannot_reanchor_to_modified_wall_time(self):
        self.backend.snapshot()
        self.source.wall_seconds += 365*86400
        other = Backend(self.path, 18770, lambda *a, **k: None, account='another-player')
        try:
            self.assertEqual(other.snapshot()['server_time'], NOW)
        finally:
            other.close()

    def test_heartbeat_returns_game_time_not_client_or_system_time(self):
        self.backend.snapshot()
        self.source.seconds += 10
        self.source.wall_seconds += 365*86400
        packet = encode(2999, dict(time=NOW+999999, random_key=0, delay_time=0))
        replies = self.backend.respond(packet, {'authenticated': True})
        heartbeat = next(data for mid, _, data in map(decode, replies) if mid == 2999)
        self.assertEqual(heartbeat['time'], NOW+10)

    def test_disposable_seed_backend_shares_owner_clock_without_closing_it(self):
        self.source.wall_seconds += 365*86400
        with tempfile.TemporaryDirectory() as temporary:
            scratch = Backend(Path(temporary), 18770, lambda *a, **k: None,
                              clock=self.backend.clock)
            try:
                self.assertEqual(scratch.snapshot()['server_time'], NOW)
                self.assertFalse((Path(temporary) / 'clock.sqlite3').exists())
            finally:
                scratch.close()
        self.assertEqual(self.backend.snapshot()['server_time'], NOW)
