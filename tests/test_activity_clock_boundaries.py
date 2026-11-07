"""Refresh through the real clock journal and wire handlers, using fake OS inputs."""
import copy
from datetime import datetime
from pathlib import Path
import tempfile
import unittest

from network_redirect import game_clock
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode, encode
from tests.test_game_clock import Source


def timestamp(value):
    return int(datetime.fromisoformat(value + '+08:00').timestamp())


class ActivityClockBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)
        self.source = Source()
        self.initial = timestamp('2026-11-02T23:59:59')
        self.source.wall_seconds = self.initial
        self.clock = game_clock.GameClock(self.path, source=self.source)
        self.addCleanup(self.clock.close)
        self.backend = Backend(self.path, 0, lambda *a, **k: None, clock=self.clock)
        self.addCleanup(lambda: self.backend.close())
        self.serial = 1000
        role = self.backend.profile()
        role['level'] = 60
        self.backend.save(role)
        self.backend.snapshot()
        for mid in (1309, 1353):
            self.serial += 1
            replies = self.backend.respond(
                encode(mid, dict(serial_num=self.serial, id=1, data='{}')),
                {'authenticated': True})
            self.assert_no_error(replies)

    def assert_no_error(self, replies):
        errors = [login_fields(d['data']) for m, _, d in map(decode, replies)
                  if m == 2998 and d['id'] == 55]
        self.assertEqual(errors, [])

    def advance_to(self, value):
        self.source.advance(100 + timestamp(value) - self.initial - self.source.seconds)

    def heartbeat(self):
        replies = self.backend.respond(
            encode(2999, dict(time=2147483647, random_key=0, delay_time=0)),
            {'authenticated': True})
        self.assert_no_error(replies)
        self.assertFalse(self.backend.profile()['time_guard']['blocked'])
        return replies

    def exhaust(self):
        role = self.backend.profile()
        sky = role['activity']['nine_sky']
        sky.update(free_times=0, stars=101)
        sky['purchases']['1'] = [1] * 6
        tower = role['activity']['babel']
        tower.update(life=1, energy=0, refresh_times=0, purchases={'1': 1},
                     history_floor=20, participated=True)
        self.backend.save(role)
        return copy.deepcopy(role)

    def test_tolerated_wall_adjustments_do_not_refresh_but_real_midnight_does_once(self):
        before = self.exhaust()
        for offset in (20, -20, 60, -60, 0):
            self.source.wall_seconds = self.initial + offset
            self.heartbeat()
            role = self.backend.profile()
            for key in ('nine_sky', 'babel'):
                self.assertEqual(role['activity'][key], before['activity'][key])
        self.source.advance(1)
        self.heartbeat()
        role = self.backend.profile()
        sky, tower = role['activity']['nine_sky'], role['activity']['babel']
        self.assertEqual(sky['free_times'], 5)
        self.assertEqual(sky['purchases']['1'], [0] * 6)
        self.assertEqual(sky['stars'], 101)
        self.assertEqual((tower['life'], tower['refresh_times'], tower['purchases']), (100, 1, {}))
        self.assertEqual(tower['energy'], 1)
        self.heartbeat()
        repeated = self.backend.profile()
        for key in ('nine_sky', 'babel'):
            self.assertEqual(repeated['activity'][key], role['activity'][key])

    def test_monday_boundary_resets_and_recycles_exactly_once(self):
        self.advance_to('2026-11-08T23:59:59')
        self.heartbeat()
        before = self.exhaust()
        old_sky = before['activity']['nine_sky']
        old_tower = before['activity']['babel']
        self.heartbeat()
        self.assertEqual(self.backend.profile()['activity']['nine_sky']['start'], old_sky['start'])
        self.source.advance(1)
        self.heartbeat()
        role = self.backend.profile()
        sky, tower = role['activity']['nine_sky'], role['activity']['babel']
        self.assertEqual(sky['start'], timestamp('2026-11-09T00:00:00'))
        self.assertEqual((sky['stars'], sky['credits'], sky['steps'], sky['free_times']), (0, 0, 0, 5))
        self.assertEqual((tower['week'], tower['cur_floor'], tower['history_floor']),
                         (old_tower['week'] + 1, 1, 1))
        key = f'nine-sky-recycle-{old_sky["start"]}'
        self.assertEqual(role['welfare']['mails'][key]['prizes'], [[5, 1001, 51, 1]])
        self.heartbeat()
        self.assertEqual(self.backend.profile()['welfare']['mails'], role['welfare']['mails'])

    def test_thursday_settlement_is_separate_from_monday_reset(self):
        before = self.exhaust()
        week = before['activity']['babel']['week']
        key = f'babel-rank-{week}'
        self.advance_to('2026-11-04T23:59:59')
        self.heartbeat()
        self.assertNotIn(key, self.backend.profile()['welfare'].get('mails', {}))
        self.source.advance(1)
        self.heartbeat()
        role = self.backend.profile()
        self.assertIn(key, role['welfare']['mails'])
        self.assertIn(f'babel-stage-{week}-20', role['welfare']['mails'])
        self.assertEqual(role['activity']['babel']['history_floor'], 20)
        self.heartbeat()
        self.assertEqual(self.backend.profile()['welfare']['mails'], role['welfare']['mails'])

    def test_same_boot_reopen_counts_normal_offline_time(self):
        self.exhaust()
        self.backend.close()
        self.clock.close()
        self.source.advance(7 * 86400)
        self.clock = game_clock.GameClock(self.path, source=self.source)
        self.addCleanup(self.clock.close)
        self.backend = Backend(self.path, 0, lambda *a, **k: None, clock=self.clock)
        role = self.backend.snapshot()
        self.assertEqual(role['server_time'], self.initial + 7 * 86400)
        self.assertEqual(role['activity']['nine_sky']['stars'], 0)
        self.assertEqual(role['activity']['nine_sky']['free_times'], 5)
        self.assertEqual(role['activity']['babel']['life'], 100)
        self.assertFalse(role['time_guard']['blocked'])

    def test_device_reboot_does_not_invent_offline_day_or_freeze_future_progress(self):
        before = self.exhaust()
        self.source.boot_id = 'rebooted-device'
        self.source.seconds = 900000
        self.source.wall_seconds += 7 * 86400
        self.heartbeat()
        role = self.backend.profile()
        for key in ('nine_sky', 'babel'):
            self.assertEqual(role['activity'][key], before['activity'][key])
        self.source.advance(1)
        self.heartbeat()
        role = self.backend.profile()
        self.assertEqual(role['activity']['nine_sky']['free_times'], 5)
        self.assertEqual(role['activity']['babel']['life'], 100)
