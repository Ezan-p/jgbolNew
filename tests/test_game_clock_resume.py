"""Offline catch-up uses real SQLite journals and controlled OS input."""
import json
from pathlib import Path
import tempfile
import unittest

from network_redirect import game_clock
from tests.test_game_clock import Source, NOW


class ResumeClockTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.source = Source()
        self.clock = game_clock.GameClock(self.tmp.name, source=self.source)
        self.addCleanup(lambda: self.clock.close())

    def reopen(self):
        self.clock.close()
        self.clock = game_clock.GameClock(self.tmp.name, source=self.source)
        return self.clock.sample()

    def state(self):
        return json.loads(self.clock.db.execute('SELECT data FROM clock').fetchone()[0])

    def test_shutdown_eight_hours_and_repeated_reopen_credit_once(self):
        self.source.boot_id = 'boot-b'
        self.source.seconds = 10
        self.source.wall_seconds += 8 * 3600
        self.assertEqual(self.reopen(), NOW + 8 * 3600)
        for _ in range(4):
            self.assertEqual(self.reopen(), NOW + 8 * 3600)
        self.source.advance(60)
        self.assertEqual(self.clock.sample(), NOW + 8 * 3600 + 60)
        self.assertIsNone(self.clock.notice)
        self.assertFalse(self.clock.quarantined)

    def test_missing_boot_identity_and_shared_connections_do_not_double_credit(self):
        self.source.boot_id = 'process:new'
        self.source.advance(3600)
        self.assertEqual(self.reopen(), NOW + 3600)
        with game_clock.scope(self.clock):
            self.assertEqual(game_clock.now(), NOW + 3600)
        other = game_clock.GameClock(self.tmp.name, source=self.source)
        try:
            self.assertEqual(other.sample(), NOW + 3600)
        finally:
            other.close()
        self.source.boot_id = 'process:third'
        self.assertEqual(self.reopen(), NOW + 3600)

    def test_same_boot_offline_is_not_limited_to_thirty_days(self):
        self.source.advance(60 * 86400)
        self.assertEqual(self.reopen(), NOW + 60 * 86400)
        self.assertIsNone(self.clock.notice)

    def test_thirty_day_boundary_and_large_gap_not_partially_paid(self):
        self.source.boot_id = 'boot-b'
        self.source.advance(game_clock.MAX_OFFLINE_GAP)
        self.assertEqual(self.reopen(), NOW + game_clock.MAX_OFFLINE_GAP)
        self.source.boot_id = 'boot-c'
        self.source.advance(game_clock.MAX_OFFLINE_GAP + 1)
        self.assertEqual(self.reopen(), NOW + game_clock.MAX_OFFLINE_GAP)
        self.assertEqual(self.clock.notice['reason'], 'long_offline_gap')
        self.assertEqual(self.clock.notice['seconds'], game_clock.MAX_OFFLINE_GAP + 1)
        self.assertFalse(self.clock.quarantined)
        self.source.advance(10)
        self.assertEqual(self.clock.sample(), NOW + game_clock.MAX_OFFLINE_GAP + 10)
        self.source.boot_id = 'boot-d'
        self.source.advance(600)
        self.assertEqual(self.reopen(), NOW + game_clock.MAX_OFFLINE_GAP + 610)

    def test_vm_pause_does_not_freeze_future_gameplay_or_pay_on_restart(self):
        self.source.wall_seconds += 8 * 3600  # guest elapsed timer was frozen
        self.assertEqual(self.reopen(), NOW)
        self.assertFalse(self.clock.quarantined)
        self.assertTrue(self.state()['wall_untrusted'])
        first_notice = self.clock.notice.copy()
        self.source.advance(3600)
        self.assertEqual(self.clock.sample(), NOW + 3600)
        self.assertEqual(self.clock.notice, first_notice)
        self.source.boot_id = 'boot-b'
        self.source.seconds = 5
        self.assertEqual(self.reopen(), NOW + 3600)
        self.assertFalse(self.state()['wall_untrusted'])
        self.assertEqual(self.state()['deferred_history'][0], first_notice)
        self.source.boot_id = 'boot-c'
        self.source.wall_seconds += 600
        self.assertEqual(self.reopen(), NOW + 4200)

    def test_restoring_wall_baseline_resumes_future_offline_credit(self):
        self.source.wall_seconds -= 86400
        self.clock.sample()
        self.source.advance(60)
        self.assertEqual(self.clock.sample(), NOW + 60)
        self.source.wall_seconds = NOW + 60
        self.clock.sample()
        self.assertFalse(self.state()['wall_untrusted'])
        self.source.boot_id = 'boot-b'
        self.source.wall_seconds += 3600
        self.assertEqual(self.reopen(), NOW + 3660)

    def test_backward_reboot_never_rewinds_game_and_records_deferred_gap(self):
        self.source.boot_id = 'boot-b'
        self.source.wall_seconds -= 86400
        self.assertEqual(self.reopen(), NOW)
        self.assertEqual(self.clock.notice['reason'], 'backward_reboot')
        self.assertFalse(self.clock.quarantined)
        self.source.advance(600)
        self.assertEqual(self.clock.sample(), NOW + 600)

    def test_old_quarantine_not_automatically_cleared(self):
        state = self.state()
        state.pop('policy_version')
        state.update(quarantined=True, wall_anomaly={'deviation': 86400})
        with self.clock.db:
            self.clock._write(state)
        self.source.boot_id = 'boot-b'
        self.source.wall_seconds += 3600
        self.assertEqual(self.reopen(), NOW)
        self.assertTrue(self.clock.quarantined)

    def test_signed_v1_migration_preserves_history_and_credits_only_new_gap(self):
        state = self.state()
        state.pop('policy_version')
        state['game'] += 86400  # existing game date is ahead of wall date
        with self.clock.db:
            self.clock._write(state)
        self.source.boot_id = 'boot-b'
        self.source.wall_seconds += 600
        self.assertEqual(self.reopen(), NOW + 86400 + 600)
        self.assertFalse(self.clock.quarantined)

    def test_checkpoint_survives_later_business_failure(self):
        self.source.boot_id = 'boot-b'
        self.source.wall_seconds += 3600
        with self.assertRaises(ValueError):
            with game_clock.scope(self.clock):
                self.assertEqual(game_clock.now(), NOW + 3600)
                raise ValueError('business transaction failed after clock commit')
        self.assertEqual(self.reopen(), NOW + 3600)
