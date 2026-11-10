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

    def test_reboot_crosses_week_once_and_preserves_settlement_after_reopen(self):
        before = self.exhaust()
        old_week = before['activity']['nine_sky']['start']
        self.backend.close()
        self.clock.close()
        self.source.boot_id = 'rebooted-device'
        self.source.seconds = 900000
        self.source.wall_seconds += 7 * 86400
        self.clock = game_clock.GameClock(self.path, source=self.source)
        self.addCleanup(self.clock.close)
        self.backend = Backend(self.path, 0, lambda *a, **k: None, clock=self.clock)
        self.heartbeat()
        role = self.backend.snapshot()
        self.assertEqual(role['server_time'], self.initial + 7 * 86400)
        self.assertEqual(role['activity']['nine_sky']['free_times'], 5)
        self.assertEqual(role['activity']['nine_sky']['stars'], 0)
        self.assertEqual(role['activity']['babel']['life'], 100)
        key = f'nine-sky-recycle-{old_week}'
        self.assertEqual(role['welfare']['mails'][key]['prizes'], [[5, 1001, 51, 1]])
        self.backend.close()
        self.clock.close()
        self.clock = game_clock.GameClock(self.path, source=self.source)
        self.addCleanup(self.clock.close)
        self.backend = Backend(self.path, 0, lambda *a, **k: None, clock=self.clock)
        self.heartbeat()
        repeated = self.backend.snapshot()
        for field in ('server_time', 'welfare'):
            self.assertEqual(repeated[field], role[field])
        for field in ('nine_sky', 'babel'):
            self.assertEqual(repeated['activity'][field], role['activity'][field])

    def test_food_weekly_settlement_uses_game_clock_and_restarts_without_duplicates(self):
        from network_redirect import activity_seasonal as season, summon
        role = self.backend.profile()
        for tid in (1134, 1208):summon.add_item(role, tid, 11)
        saved_week = season.state(role)['craft_weeks']['moon']['week']
        self.backend.save(role)
        # Small wall-clock edits do not advance the game's week.
        self.source.wall_seconds += 60
        self.heartbeat()
        self.assertNotIn(f'moon-recycle-{saved_week}',self.backend.profile()['welfare'].get('mails',{}))
        self.source.wall_seconds -= 60
        self.advance_to('2026-11-09T00:00:00')
        self.heartbeat()
        role = self.backend.profile()
        for name in ('moon','rice'):
            self.assertEqual(role['welfare']['mails'][f'{name}-recycle-{saved_week}']['prizes'],[[5,1001,1,1]])
        self.backend.close()
        self.backend = Backend(self.path,0,lambda *a,**k:None,clock=self.clock)
        self.heartbeat()
        self.assertEqual(role['welfare']['mails'],self.backend.profile()['welfare']['mails'])
