"""Request baseline isolation and scan bounds, without wall-clock assertions."""
import copy
import json
import random
import unittest
from unittest.mock import patch

from tests.test_activity import ActivityCase, NOW
from network_redirect import activity, combat_power, formation, immortal, journey, reborn, summon
from network_redirect.request_timing import (
    current, recalculation_cache, request_cache, role_baselines,
)


class RolePerformanceTests(unittest.TestCase):
    def setUp(self):
        self.case = ActivityCase()
        self.case.setUp()
        self.addCleanup(self.case.doCleanups)
        self.b = self.case.b

    def test_query_reuses_baseline_without_copying_whole_role(self):
        self.case.ok(self.case.req(1353, id=1, data='{}'))
        original = copy.deepcopy
        def no_role_copy(value, *args, **kwargs):
            if isinstance(value, dict) and 'role_id' in value:
                self.fail('unchanged query copied the whole role')
            return original(value, *args, **kwargs)
        metrics = {}
        token = current.set(metrics)
        try:
            with patch.object(copy, 'deepcopy', side_effect=no_role_copy):
                self.case.ok(self.case.req(1353, id=1, data='{}'))
        finally:
            current.reset(token)
        self.assertEqual(metrics['role_baseline_loads'], 1)
        self.assertGreaterEqual(metrics['role_baseline_hits'], 3)
        self.assertEqual(metrics['recalculate_calls'], 1)
        self.assertEqual(metrics['save_unchanged'], 1)
        self.assertIsNone(role_baselines.get())
        self.assertIsNone(recalculation_cache.get())

    @request_cache
    def test_working_roles_and_unsaved_baselines_are_detached(self):
        first = self.b.profile()
        second = self.b.profile()
        _, baseline = self.b.stored_role()
        self.assertIs(self.b.operation_baseline(first), baseline)
        first['attachments'][0]['level'] += 1
        first['gold_coin'] -= 1
        detached = self.b.operation_baseline(first)
        first['attachments'][0]['level'] += 1
        self.assertEqual(second, baseline)
        self.assertNotEqual(detached, first)
        self.assertNotEqual(detached, baseline)
        self.assertIs(self.b.stored_role()[1], baseline)

    @request_cache
    def test_save_rebases_and_retains_previous_snapshot(self):
        role = self.b.profile()
        raw, previous = self.b.stored_role()
        role['gold_coin'] -= 7
        self.b.save(role)
        new_raw, latest = self.b.stored_role()
        self.assertNotEqual(raw, new_raw)
        self.assertEqual(previous, json.loads(raw))
        self.assertEqual(latest['gold_coin'], previous['gold_coin'] - 7)
        role['gold_coin'] -= 2
        self.b.save(role)
        self.assertEqual(self.b.stored_role()[1]['gold_coin'], previous['gold_coin'] - 9)
        self.assertEqual(latest['gold_coin'], previous['gold_coin'] - 7)

    @request_cache
    def test_direct_sql_and_rollback_refresh_baseline(self):
        raw, previous = self.b.stored_role()
        changed = dict(previous, gold_coin=previous['gold_coin'] + 1)
        self.b.db.execute('UPDATE roles SET data=? WHERE account=?',
                          (json.dumps(changed), self.b.account))
        self.assertEqual(self.b.stored_role()[1], changed)
        self.b.db.rollback()
        self.assertEqual(self.b.stored_role(), (raw, previous))

    @request_cache
    def test_baselines_are_separate_for_accounts_and_missing_roles(self):
        _, first = self.b.stored_role()
        self.assertEqual(self.b.stored_role('other'), (None, None))
        other = self.b.profile('other')
        self.assertEqual(self.b.stored_role('other')[1], other)
        self.assertIs(self.b.stored_role()[1], first)
        self.assertNotEqual(other['register_account'], first['register_account'])

    def test_failed_operation_cannot_leak_into_next_request(self):
        before = self.b.profile()
        def fail(role, *args, **kwargs):
            role['gold_coin'] = 0
            role['attachments'].clear()
            raise formation.Rejected('fixture rejection')
        with patch.object(activity, 'settle', side_effect=fail):
            self.assertEqual(self.case.req(1353, id=1, data='{}')[0][0], 55)
        self.assertEqual(self.b.profile(), before)
        self.assertIsNone(role_baselines.get())
        self.case.ok(self.case.req(1353, id=1, data='{}'))
        self.assertEqual(self.b.profile()['gold_coin'], before['gold_coin'])

    def test_exception_restores_outer_cache_context(self):
        outer = {}
        token = role_baselines.set(outer)
        try:
            @request_cache
            def fail():
                self.b.stored_role()
                raise RuntimeError('fixture')
            with self.assertRaises(RuntimeError):
                fail()
            self.assertIs(role_baselines.get(), outer)
            self.assertEqual(outer, {})
            self.assertIsNone(recalculation_cache.get())
        finally:
            role_baselines.reset(token)

    def test_attribute_sync_does_not_mutate_baseline(self):
        before = self.b.profile()
        before.pop('top_score', None)
        before.pop('train_gongji_index', None)
        original = copy.deepcopy(before)
        role = copy.deepcopy(before)
        role['gold_coin'] -= 1
        self.b.activity_changes(before, role, 1030)
        self.assertEqual(before, original)

    @request_cache
    def test_legacy_achievement_packets_do_not_mutate_baseline(self):
        role = self.b.profile()
        role.pop('achievements')
        self.b.db.execute('UPDATE roles SET data=? WHERE account=?',
                          (json.dumps(role), self.b.account))
        self.b.db.commit()
        _, before = self.b.stored_role()
        self.b.achievement_context = (1353, {'id': 1})
        self.b.save(role)
        self.assertNotIn('achievements', before)
        self.assertIn('achievements', self.b.stored_role()[1])

    @request_cache
    def test_complete_cache_tracks_nested_state_rules_and_key_types(self):
        role = self.b.profile()
        rules = copy.deepcopy(self.b.formation_rules)
        recalculation_cache.get().clear()
        role['fixture_history'] = {1: {'events': [1]}}
        with patch.object(combat_power, 'recalculate', wraps=combat_power.recalculate) as calc:
            formation.recalculate(role, rules)
            role['collection_bonuses'] = dict(role['collection_bonuses'])
            formation.recalculate(role, rules)
            self.assertEqual(calc.call_count, 1)
            role['fixture_history'][1]['events'].append(2)
            formation.recalculate(role, rules)
            role['fixture_history']['1'] = role['fixture_history'].pop(1)
            formation.recalculate(role, rules)
            rules['combat_weights']['gongji'] += 1
            formation.recalculate(role, rules)
            with patch('network_redirect.game_clock.now', return_value=NOW + 1):
                formation.recalculate(role, rules)
            self.assertEqual(calc.call_count, 5)

    def test_migrations_without_change_report_produce_same_state(self):
        original = self.b.profile()
        original['corteges'][0].pop('next_exp', None)
        original['corteges'][0].pop('reborn_vein_level', None)
        original.pop('handbook', None)
        for module, rules in ((formation, self.b.formation_rules),
                              (immortal, self.b.immortal_rules), (reborn, self.b.reborn_rules)):
            a, b = copy.deepcopy(original), copy.deepcopy(original)
            module.prepare(a, rules)
            self.assertIsNone(module.prepare(b, rules, track_changes=False))
            self.assertEqual(a, b)

    def test_panel_scans_inventory_once_for_many_companions(self):
        role = self.b.profile()
        for _ in range(15):
            role['corteges'].append(summon.companion(role, 5004))
        formation.prepare(role, self.b.formation_rules)
        class Inventory(list):
            scans = 0
            def __iter__(self):
                self.scans += 1
                return super().__iter__()
        role['attachments'] = Inventory(role['attachments'])
        combat_power.recalculate(role, self.b.formation_rules, now=NOW)
        self.assertEqual(role['attachments'].scans, 1)
        for c in role['corteges']:
            self.assertEqual(role['combat_power_breakdown']['companions'][str(c['id'])]['essence'],
                             combat_power.essence_score(role, c))

    def test_innate_migration_keeps_inventory_priority_and_claims_once(self):
        role = self.b.profile()
        first = role['corteges'][0]
        second = summon.companion(role, first['type'])
        second['order'] = first['order']  # legacy conflicting formation slots
        role['corteges'].append(second)
        explicit = next(i for i in role['attachments'] if i.get('innate_owner_id') == first['id'])
        legacy = dict(explicit, id=formation.new_id(role), innate_owner_id=0, owner_id=0)
        role['attachments'].insert(0, legacy)
        formation.prepare(role, self.b.formation_rules)
        self.assertEqual(legacy['innate_owner_id'], first['id'])
        second_items = [i for i in role['attachments'] if i.get('innate_owner_id') == second['id']]
        self.assertEqual(len(second_items), 1)
        self.assertNotEqual(second_items[0]['id'], legacy['id'])

    def test_map_index_matches_full_scan_for_snapshots_and_updates(self):
        rng = random.Random(101)
        role = self.b.profile()
        role['journey']['gates'] = {
            f'{kind}:{gid}': dict(pass_star=rng.randrange(4), day_count=0, flush_count=0)
            for kind, gates in journey.GATES.items() for gid in gates}
        old = copy.deepcopy(role)
        for progress in role['journey']['gates'].values():
            progress['pass_star'] = min(3, progress['pass_star'] + 1)
        actual = journey.snapshots(role), journey.updates(role, old)
        def completed(role, kind, mid, stars=1):
            return all(journey.progress(role, kind, gid)['pass_star'] >= stars
                       for gid, gate in journey.GATES[kind].items() if int(gate['map_id']) == mid)
        with patch.object(journey, 'completed', side_effect=completed):
            expected = journey.snapshots(role), journey.updates(role, old)
        self.assertEqual(actual, expected)
