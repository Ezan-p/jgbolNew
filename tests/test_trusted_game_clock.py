"""Trusted Beijing clock, reward high-water marks and persistent punishment."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from network_redirect import game_clock, network_time as nt, activity_babel, time_guard
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode
from tests.test_game_clock import Source, NOW


class Service:
    def __init__(self, source):
        self.source = source
        self.observation = None
        self.requests = []
        self.serial = 0
    def set(self, epoch):
        self.serial += 1
        self.observation = nt.Observation(epoch, self.source.seconds, self.source.wall(),
            self.source.boot_id, nt.HOSTS[:2], 1, str(self.serial))
    def request(self, force=False):
        self.requests.append(force)
    def read(self):
        return self.observation
    def close(self):
        pass
    def wait(self):
        return self.read()


class TrustedClockTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)
        self.source = Source();self.service = Service(self.source)
        self.service.set(NOW)
        self.clock = game_clock.GameClock(self.path, network_time=self.service)
        self.addCleanup(lambda: self.clock.close())

    def state(self):
        return json.loads(self.clock.db.execute('SELECT data FROM clock').fetchone()[0])

    def reopen(self, service=True):
        self.clock.close()
        self.clock = game_clock.GameClock(self.path, source=self.source,
            network_time=self.service if service else None)
        return self.clock.sample()

    def test_network_forward_corrects_historical_lag_and_vm_pause(self):
        self.source.wall_seconds += 28800
        self.service.set(NOW + 28800)  # guest uptime frozen, real wall correct
        self.assertEqual(self.clock.sample(), NOW + 28800)
        self.assertEqual(self.clock.display_time, NOW + 28800)
        self.assertFalse(self.clock.quarantined)
        self.assertIsNone(self.clock.notice)
        self.assertEqual(self.reopen(), NOW + 28800)

    def test_reboot_31_days_syncs_without_local_gap_limit(self):
        self.source.boot_id = 'boot-b';self.source.seconds = 10
        self.source.wall_seconds += 31 * 86400
        self.service.set(NOW + 31 * 86400)
        self.assertEqual(self.reopen(), NOW + 31 * 86400)
        self.assertFalse(self.clock.quarantined)

    def test_unverified_reboot_cannot_credit_forward_wall_date(self):
        self.source.boot_id = 'boot-b';self.source.seconds = 10
        self.source.wall_seconds += 365 * 86400
        self.service.observation = None
        self.assertEqual(self.reopen(), NOW)
        self.assertEqual(self.clock.notice['message'], nt.WAIT_MESSAGE)
        self.source.seconds += 60
        self.assertEqual(self.clock.sample(), NOW + 60)
        # Even if reopened without a service, persisted v3 never falls back to v2.
        self.source.boot_id = 'boot-c';self.source.seconds = 10
        self.assertEqual(self.reopen(service=False), NOW + 60)

    def test_forward_backward_wall_change_requires_network_evidence(self):
        for offset in (86400, -86400):
            with self.subTest(offset=offset), tempfile.TemporaryDirectory() as tmp:
                source = Source();service = Service(source);service.set(NOW)
                clock = game_clock.GameClock(tmp, network_time=service)
                source.wall_seconds += offset
                self.assertEqual(clock.sample(), NOW)
                self.assertFalse(clock.quarantined)  # local difference alone insufficient
                service.set(NOW)
                self.assertEqual(clock.sample(), NOW)
                self.assertTrue(clock.quarantined)
                source.wall_seconds = NOW;service.set(NOW)
                clock.close();clock = game_clock.GameClock(tmp, network_time=service)
                self.assertTrue(clock.quarantined)
                clock.close()

    def test_small_cumulative_changes_and_automatic_correction_toward_utc(self):
        for offset in (100, 200, 300):
            self.source.wall_seconds = NOW + offset;self.service.set(NOW)
            self.clock.sample();self.assertFalse(self.clock.quarantined)
        self.source.wall_seconds = NOW + 301;self.service.set(NOW)
        self.clock.sample();self.assertTrue(self.clock.quarantined)

    def test_first_wrong_system_date_is_baseline_not_punishment(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Source();source.wall_seconds += 86400
            service = Service(source);service.set(NOW)
            clock = game_clock.GameClock(tmp, network_time=service)
            self.assertEqual(clock.sample(), NOW)
            source.wall_seconds = NOW;service.set(NOW)
            self.assertEqual(clock.sample(), NOW)
            self.assertFalse(clock.quarantined)
            clock.close()

    def test_network_backward_correction_updates_display_without_reopening_rewards(self):
        self.source.advance(86400);self.service.set(NOW + 86400)
        self.assertEqual(self.clock.sample(), NOW + 86400)
        self.service.set(NOW)
        self.clock.sample()
        self.assertEqual(self.clock.display_time, NOW)
        self.assertEqual(self.clock.sample(), NOW + 86400)
        self.assertEqual(self.state()['settlement_floor'], NOW + 86400)
        self.assertFalse(self.clock.quarantined)

    def test_v2_future_history_preserved_and_display_corrected(self):
        state = self.state();state.pop('network_anchor');state.pop('trusted_wall_offset')
        state.update(policy_version=2, game=NOW+86400)
        with self.clock.db:self.clock._write(state)
        self.service.set(NOW)
        self.assertEqual(self.reopen(), NOW+86400)
        self.assertEqual(self.clock.display_time, NOW)
        self.assertFalse(self.clock.quarantined)
        self.assertEqual(self.clock.notice['message'], nt.FUTURE_MESSAGE)
        self.source.advance(86401);self.service.set(NOW+86401)
        self.assertEqual(self.clock.sample(), NOW+86401)
        self.assertIsNone(self.clock.notice)

    def test_v2_lag_catches_up_and_old_quarantine_stays(self):
        state = self.state();state.update(policy_version=2, game=NOW-28800, quarantined=True)
        with self.clock.db:self.clock._write(state)
        self.service.set(NOW)
        self.assertEqual(self.reopen(), NOW)
        self.assertTrue(self.clock.quarantined)

    def test_corrupt_signed_record_still_rejected(self):
        with self.clock.db:self.clock.db.execute("UPDATE clock_integrity SET seal='bad'")
        with self.assertRaises(RuntimeError):self.clock.sample()

    def test_modified_clock_restores_signed_history_and_quarantines(self):
        state = self.state();state['game'] += 86400
        with self.clock.db:self.clock.db.execute('UPDATE clock SET data=?', (json.dumps(state),))
        self.assertEqual(self.clock.sample(), NOW)
        self.assertTrue(self.clock.quarantined)

    def test_context_has_one_authoritative_display_and_settlement_snapshot(self):
        with game_clock.scope(self.clock):
            self.assertEqual(game_clock.now(), NOW)
            self.assertEqual(game_clock.display_now(), NOW)
            self.source.advance(10)
            with game_clock.scope(self.clock):
                self.assertEqual(game_clock.display_now(), NOW)
        self.assertIsNone(game_clock._context.get())

    def test_backend_future_calibration_cannot_duplicate_daily_or_weekly_state(self):
        backend = Backend(self.path, 0, lambda *a, **k: None, clock=self.clock)
        self.addCleanup(backend.close)
        role = backend.profile();role['level']=60
        activity_babel.state(role, NOW, backend.activity_rules);backend.save(role)
        before = backend.snapshot()
        self.source.advance(8*86400);self.service.set(NOW+8*86400)
        after = backend.snapshot()
        self.service.set(NOW+7*86400)
        corrected = backend.snapshot()
        self.assertEqual(corrected['server_time'], NOW+7*86400)
        self.assertEqual(corrected['activity']['babel'], after['activity']['babel'])
        self.assertEqual(corrected['daily'], after['daily'])
        self.assertEqual(corrected['welfare'], after['welfare'])
        self.assertFalse(self.clock.quarantined)

    def test_resume_packet_requests_sync_and_penalty_is_persisted_for_role(self):
        backend = Backend(self.path, 0, lambda *a, **k: None, clock=self.clock)
        self.addCleanup(backend.close);backend.bootstrap()
        session = {'authenticated':True}
        backend.respond(encode(2999, dict(delay_time=nt.RESUME_MARKER)), session)
        self.assertIn(True, self.service.requests)
        self.source.wall_seconds += 86400;self.service.set(NOW)
        replies = backend.respond(encode(2999, {}), session)
        notices = [login_fields(d['data'])['op_string'] for mid, _, d in map(decode,replies)
                   if mid==2998 and d['id']==55]
        self.assertEqual(notices,[time_guard.MESSAGE])
        self.assertEqual(backend.profile()['time_guard']['blocked'],['*'])
        self.source.wall_seconds = NOW;self.service.set(NOW)
        backend.respond(encode(2999, {}), session)
        self.assertEqual(backend.profile()['time_guard']['blocked'],['*'])

    def test_offset_change_after_reboot_is_confirmed_and_persistent(self):
        self.source.boot_id='boot-b';self.source.seconds=10
        self.source.wall_seconds+=86400
        self.service.set(NOW+3600)
        self.assertEqual(self.reopen(),NOW+3600)
        self.assertTrue(self.clock.quarantined)
        self.source.wall_seconds=NOW+3600;self.service.set(NOW+3600)
        self.assertEqual(self.reopen(),NOW+3600)
        self.assertTrue(self.clock.quarantined)

    def test_reset_elapsed_same_boot_waits_for_network(self):
        self.source.seconds=5;self.source.wall_seconds+=86400
        self.service.observation=None
        self.assertEqual(self.reopen(),NOW)
        self.assertEqual(self.clock.notice['message'],nt.WAIT_MESSAGE)
        self.source.advance(10)
        self.assertEqual(self.clock.sample(),NOW+10)
        self.assertEqual(self.clock.notice['message'],nt.WAIT_MESSAGE)

    def test_stale_or_single_source_result_cannot_advance_clock(self):
        from dataclasses import replace
        self.service.set(NOW+86400)
        self.service.observation=replace(self.service.observation,hosts=(nt.HOSTS[0],))
        self.assertEqual(self.clock.sample(),NOW)
        self.service.set(NOW+86400)
        self.source.advance(31)
        self.assertEqual(self.clock.sample(),NOW+31)
        self.assertEqual(self.clock.display_time,NOW+31)

    def test_switching_accounts_uses_one_clock_and_one_network_service(self):
        from network_redirect.accounts import Accounts
        with tempfile.TemporaryDirectory() as tmp:
            accounts=Accounts(Path(tmp),0,lambda *a,**k:None,network_time=self.service)
            try:
                accounts.start_session('alice');accounts.start_session('bob')
                self.assertIs(accounts.backends['alice'].clock,accounts.base.clock)
                self.assertIs(accounts.backends['bob'].clock,accounts.base.clock)
                self.assertIs(accounts.base.clock.network_time,self.service)
            finally:accounts.close()

    def test_beijing_reset_settings_all_remain_eight(self):
        found=[]
        def visit(value):
            if isinstance(value,dict):
                for key,item in value.items():
                    if key in ('timezone_offset_hours','reset_utc_offset_hours'):
                        found.append(item);self.assertEqual(item,8)
                    visit(item)
            elif isinstance(value,list):
                for item in value:visit(item)
        for path in Path('server_config').glob('*.json'):
            visit(json.loads(path.read_text()))
        self.assertGreater(len(found),10)
