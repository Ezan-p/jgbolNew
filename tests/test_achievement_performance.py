"""Achievement cache correctness, request isolation and bounded map scans."""
import copy
import random
import unittest
from unittest.mock import patch

from network_redirect import achievements as a, journey, summon
from network_redirect.backend import login_fields
from network_redirect.request_timing import (
    achievement_refresh_cache, current, request_cache,
)
from tests import test_activity

NOW = test_activity.NOW


def role_fixture():
    return dict(role_id=1, corteges=[], attachments=[], activity={}, summon={},
                journey=dict(gates={}, claimed_maps=[]))


class AchievementRefreshTests(unittest.TestCase):
    def test_duplicate_refresh_skips_scan_but_not_outside_request(self):
        role = role_fixture()
        metrics = {}
        token = current.set(metrics)
        self.addCleanup(current.reset, token)
        @request_cache
        def run():
            a.refresh(role, NOW)
            expected = copy.deepcopy(role)
            a.refresh(role, NOW)
            self.assertEqual(role, expected)
        with patch.object(a, '_refresh', wraps=a._refresh) as scan:
            run()
            self.assertEqual(scan.call_count, 1)
            run()
            self.assertEqual(scan.call_count, 2)
            a.refresh(role, NOW)
            a.refresh(role, NOW)
            self.assertEqual(scan.call_count, 4)
        self.assertEqual(metrics['achievement_refresh_skipped'], 2)
        self.assertEqual(metrics['achievement_refresh_calls'], 4)
        self.assertIsNone(achievement_refresh_cache.get())

    @request_cache
    def test_full_domain_changes_match_uncached_refresh(self):
        role = role_fixture()
        c = summon.companion(role, 5004)
        role['corteges'].append(c)
        role['attachments'].append(dict(id=800, attach_type=6, type_id=22, level=1, count=0))
        a.refresh(role, NOW)
        mutations = [
            lambda r: r.update(vip_level=2),
            lambda r: r.update(reborn_layer=2),
            lambda r: r['corteges'][0].update(evolve_level=20),
            lambda r: r['attachments'][0].update(level=10),
            lambda r: r['activity'].update(rank_order=1, duty_best=100),
            lambda r: r['activity'].update(abyss=dict(boss=10)),
            lambda r: r['activity'].update(home=dict(pets=[dict(id=99, quality=4)])),
            lambda r: r.update(spirit_array=[dict(activated=True, skill_list=[5]*6)]),
            lambda r: r['journey']['gates'].update({f'1:{gid}': dict(pass_star=3)
                                                   for gid in journey.GATES_BY_MAP[1][1]}),
            lambda r: r['journey']['gates'].update({'2:101': dict(pass_star=3)}),
            lambda r: a.add(r, 101),
            lambda r: r.update(tao_point=0),
            lambda r: r['achievements']['observed'].clear(),
            lambda r: r.pop('achievements'),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                mutate(role)
                expected = copy.deepcopy(role)
                a._refresh(expected, NOW)
                with patch.object(a, '_refresh', wraps=a._refresh) as scan:
                    a.refresh(role, NOW)
                    self.assertEqual(scan.call_count, 1)
                self.assertEqual(role, expected)
                self.assertEqual(a.packets(role), a.packets(expected))

    @request_cache
    def test_fallback_rank_and_missing_journey_invalidate(self):
        role = role_fixture()
        role.pop('journey')
        a.refresh(role, NOW)
        role['top_order'] = 1
        role['journey'] = dict(gates={})
        expected = copy.deepcopy(role)
        a._refresh(expected, NOW)
        a.refresh(role, NOW)
        self.assertEqual(role, expected)
        self.assertEqual(role['achievements']['totals']['215'], 1)

    @request_cache
    def test_unrelated_fields_and_equal_replacements_do_not_rescan(self):
        role = role_fixture()
        a.refresh(role, NOW)
        role.update(gold_coin=100, task_progress=1, benchmark_history=[{1: 'record'}])
        role['activity'] = dict(role['activity'])
        role['attachments'] = list(role['attachments'])
        with patch.object(a, '_refresh', side_effect=AssertionError('unexpected scan')):
            a.refresh(role, NOW)

    @request_cache
    def test_event_tracking_and_save_tracking_still_award(self):
        role = role_fixture()
        a.refresh(role, NOW)
        before = copy.deepcopy(role)
        a.record_events(role, [summon.event(43, dict(feed_result=2))], NOW, login_fields)
        role['activity']['convert_total'] = 1
        expected = copy.deepcopy(role)
        token = achievement_refresh_cache.set(None)
        try:
            a.track(expected, before, 1353, {}, NOW)
        finally:
            achievement_refresh_cache.reset(token)
        a.track(role, before, 1353, {}, NOW)
        self.assertEqual(role, expected)
        self.assertEqual(role['achievements']['totals']['108'], 1)
        self.assertEqual(role['achievements']['totals']['106'], 1)

    @request_cache
    def test_rank_boundary_and_midnight_do_not_reuse_old_time(self):
        role = role_fixture()
        role['activity']['rank_order'] = 1
        a.refresh(role, NOW)
        a.daily_add(role, 446, 60, NOW, '1:101')
        a.refresh(role, NOW)
        for now in (NOW + 86399, NOW + 86400, NOW - 1):
            expected = copy.deepcopy(role)
            a._refresh(expected, now)
            a.refresh(role, now)
            self.assertEqual(role, expected)
        self.assertNotIn('446', role['achievements']['totals'])
        self.assertEqual(role['achievements']['totals']['425'], 1)

    @request_cache
    def test_legacy_stone_observations_are_recovered_once(self):
        role = role_fixture()
        state = a.state(role)
        state['totals']['563'] = 200
        state['observed'] = {f'563:{i}': 1 for i in range(220)}
        a.refresh(role, NOW)
        self.assertEqual(state['totals']['563'], 220)
        with patch.object(a, '_refresh', side_effect=AssertionError('migration repeated')):
            a.refresh(role, NOW)

    @request_cache
    def test_other_role_never_reuses_first_role_cache(self):
        role = role_fixture()
        a.refresh(role, NOW)
        other = copy.deepcopy(role)
        with patch.object(a, '_refresh', wraps=a._refresh) as scan:
            a.refresh(other, NOW)
            a.refresh(role, NOW)
            self.assertEqual(scan.call_count, 2)

    def test_failed_refresh_and_nested_requests_restore_context(self):
        outer = {}
        token = achievement_refresh_cache.set(outer)
        self.addCleanup(achievement_refresh_cache.reset, token)
        @request_cache
        def run():
            role = role_fixture()
            with patch.object(a, '_refresh', side_effect=ValueError('fixture failure')):
                with self.assertRaises(ValueError):
                    a.refresh(role, NOW)
            self.assertEqual(achievement_refresh_cache.get(), {})
            a.refresh(role, NOW)
            cached = achievement_refresh_cache.get().copy()
            @request_cache
            def nested():
                self.assertEqual(achievement_refresh_cache.get(), {})
                a.refresh(role_fixture(), NOW)
                raise RuntimeError('nested failure')
            with self.assertRaises(RuntimeError):
                nested()
            self.assertEqual(achievement_refresh_cache.get(), cached)
        run()
        self.assertIs(achievement_refresh_cache.get(), outer)
        self.assertEqual(outer, {})

    def test_map_index_and_both_thresholds_match_original_predicate(self):
        rng = random.Random(443)
        for kind, maps in journey.MAPS.items():
            for mid in maps:
                self.assertEqual(journey.MAP_GATE_KEYS[kind][mid], tuple(
                    f'{kind}:{gid}' for gid, row in journey.GATES[kind].items()
                    if int(row['map_id']) == mid))
        for scenario in ('missing', 'one_star', 'three_stars', 'mixed', 'legacy_extra'):
            with self.subTest(scenario=scenario):
                role = role_fixture()
                gates = role['journey']['gates']
                for gid in journey.GATES[1]:
                    if scenario != 'missing':
                        gates[f'1:{gid}'] = dict(pass_star=(1 if scenario == 'one_star' else
                            rng.randrange(4) if scenario == 'mixed' else 3))
                if scenario == 'legacy_extra':
                    gates['1:9999999'] = dict(pass_star=0)
                    gates['2:9999999'] = dict(pass_star=3)
                expected = {(ident, str(mid)): int(journey.completed(role, 1, mid, stars))
                            for mid in journey.MAPS[1] for ident, stars in ((443, 1), (444, 3))}
                with patch.object(a, 'observe', wraps=a.observe) as observed, patch.object(
                        journey, 'completed', side_effect=AssertionError('duplicate map scan')):
                    a.refresh(role, NOW)
                actual = {(args[1], args[3]): args[2] for args, _ in observed.call_args_list
                          if args[1] in (443, 444)}
                self.assertEqual(actual, expected)

    def test_map_progress_is_read_at_most_once_per_gate(self):
        class Progress(dict):
            reads = 0
            def get(self, key, default=None):
                if key.startswith('1:'):
                    self.reads += 1
                return super().get(key, default)
        role = role_fixture()
        gates = Progress({f'1:{gid}': dict(pass_star=3) for gid in journey.GATES[1]})
        role['journey']['gates'] = gates
        a.refresh(role, NOW)
        self.assertEqual(gates.reads, len(journey.GATES[1]))


class AchievementRequestTests(unittest.TestCase):
    def setUp(self):
        self.case = test_activity.ActivityCase()
        self.case.setUp()
        self.addCleanup(self.case.doCleanups)
        self.b = self.case.b

    def test_query_scans_once_per_request_with_unchanged_packets_and_save(self):
        self.case.ok(self.case.req(1353, id=1, data='{}'))
        writes = self.b.db.total_changes
        for _ in range(2):
            metrics = {}
            token = current.set(metrics)
            try:
                self.case.ok(self.case.req(1353, id=1, data='{}'))
            finally:
                current.reset(token)
            self.assertEqual(metrics['achievement_refresh_calls'], 1)
            self.assertEqual(metrics['achievement_refresh_skipped'], 1)
            self.assertFalse({1034, 1035, 1066} & {mid for mid, _, _ in self.case.decoded})
            self.assertEqual(self.b.db.total_changes, writes)
            self.assertIsNone(achievement_refresh_cache.get())

    def test_reward_after_profile_refresh_reaches_persistence_and_packets(self):
        self.case.ok(self.case.req(1353, id=1, data='{}'))
        def reward(role, *args, **kwargs):
            role['attachments'].append(dict(id=900000, attach_type=6, type_id=22, level=10, count=0))
            return []
        with patch('network_redirect.activity.settle', side_effect=reward):
            self.case.ok(self.case.req(1353, id=1, data='{}'))
        saved = self.b.profile()
        self.assertEqual(saved['achievements']['totals']['416'], 1)
        rows = [row for mid, _, data in self.case.decoded if mid == 1066 for row in data['achievements']]
        self.assertEqual(next(row['times'] for row in rows if row['id'] == 416), 1)
        writes = self.b.db.total_changes
        self.b.respond(self.case.packet, self.case.state)
        self.assertEqual(self.b.db.total_changes, writes)
        self.assertEqual(self.b.profile()['achievements']['totals']['416'], 1)
