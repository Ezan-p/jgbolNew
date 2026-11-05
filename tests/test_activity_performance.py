"""Synchronization must follow actual changes, including rollover and rewards."""
import copy
from unittest.mock import patch
from tests.test_activity import ActivityCase, NOW
from network_redirect import activity, formation, combat_power, summon
from network_redirect.request_timing import current, request_cache


class ActivityPerformanceTests(ActivityCase):
    def test_babel_query_skips_global_prepare_and_unchanged_snapshots(self):
        self.ok(self.req(1353, id=1, data='{}'))
        writes = self.b.db.total_changes
        with patch.object(activity, 'prepare', side_effect=AssertionError('unrelated activity preparation')):
            self.ok(self.req(1353, id=1, data='{}'))
        self.assertEqual(writes, self.b.db.total_changes)
        self.assertFalse({1034, 1035, 1044, 1046} & {mid for mid, _, _ in self.decoded})
        self.assertEqual(self.decoded[-1][0], 1106)

    def test_empty_move_persists_without_inventory_and_replay_is_idempotent(self):
        self.legacy_babel_floor()
        writes = self.b.db.total_changes
        self.ok(self.req(1353, id=2, data=summon.lua(dict(target_pos=dict(row=2, column=1)))))
        self.assertGreater(self.b.db.total_changes, writes)
        self.assertFalse({1034, 1035, 1044, 1046} & {mid for mid, _, _ in self.decoded})
        role = self.b.profile()
        self.assertEqual(role['activity']['babel']['locale'], dict(row=2, column=1))
        writes = self.b.db.total_changes
        self.b.respond(self.packet, self.state)
        self.assertEqual(writes, self.b.db.total_changes)

    def test_move_with_reward_sends_inventory_and_persists_reward_once(self):
        self.legacy_babel_floor()
        self.ok(self.req(1353, id=2, data=summon.lua(dict(target_pos=dict(row=1, column=2)))))
        self.assertIn(1035, [mid for mid, _, _ in self.decoded])
        self.assertNotIn(1034, [mid for mid, _, _ in self.decoded])
        from network_redirect.activity_babel import item_count
        self.assertEqual(item_count(self.b.profile(), 20005), 1)
        self.b.respond(self.packet, self.state)
        self.assertEqual(item_count(self.b.profile(), 20005), 1)

    def test_reward_domains_and_zero_values_are_synced(self):
        before = self.b.profile()
        role = copy.deepcopy(before)
        role['gold_coin'] = 0
        role['attachments'] = []
        role['souls'] = {'5004': 1}
        from network_redirect.protocol import decode
        packets = [decode(p) for p in self.b.activity_changes(before, role, 1353)]
        self.assertIn(1035, [m for m, _, _ in packets])
        self.assertIn(1046, [m for m, _, _ in packets])
        self.assertNotIn(1034, [m for m, _, _ in packets])
        self.assertNotIn(1044, [m for m, _, _ in packets])
        attrs = [a for m, _, d in packets if m == 1032 and d['unit_type'] == 1 for a in d['attr_list']]
        self.assertEqual([a for a in attrs if a['type'] == 8], [dict(type=8, value=0)])

    def test_query_sends_resources_recovered_during_profile_load(self):
        role = self.b.profile()
        role['strength'] = 0
        role['journey']['strength_recovery_at'] = NOW - self.b.journey_rules['strength_recovery_seconds']
        self.b.save(role)
        self.ok(self.req(1353, id=1, data='{}'))
        values = [a['value'] for mid, _, data in self.decoded if mid == 1032 and data['unit_type'] == 1
                  for a in data['attr_list'] if a['type'] == 101]
        self.assertEqual(values, [1])

    def test_save_unchanged_does_not_write_but_changes_do(self):
        role = self.b.profile()
        self.b.save(role)
        writes = self.b.db.total_changes
        self.b.save(role)
        self.assertEqual(self.b.db.total_changes, writes)
        role['gold_coin'] -= 1
        self.b.save(role)
        self.assertGreater(self.b.db.total_changes, writes)
        self.assertEqual(self.b.profile()['gold_coin'], role['gold_coin'])

    def test_unchanged_role_still_commits_pending_other_table_write(self):
        role = self.b.profile()
        self.b.save(role)
        self.b.db.execute("INSERT INTO settings VALUES ('performance_test', 'committed')")
        self.assertTrue(self.b.db.in_transaction)
        self.b.save(role)
        self.assertFalse(self.b.db.in_transaction)
        import sqlite3
        with sqlite3.connect(self.b.db.execute('PRAGMA database_list').fetchone()[2]) as db:
            self.assertEqual(db.execute("SELECT value FROM settings WHERE key='performance_test'").fetchone(),
                             ('committed',))

    def test_recalculation_cache_invalidates_on_mutation_and_time(self):
        role = self.b.profile()
        metrics = {}
        token = current.set(metrics)
        self.addCleanup(current.reset, token)
        @request_cache
        def run():
            formation.recalculate(role, self.b.formation_rules)
            formation.recalculate(role, self.b.formation_rules)
            role['corteges'][0]['level'] += 1
            formation.recalculate(role, self.b.formation_rules)
            with patch('network_redirect.game_clock.now', return_value=NOW + 1):
                formation.recalculate(role, self.b.formation_rules)
        with patch.object(combat_power, 'recalculate', wraps=combat_power.recalculate) as calc:
            run()
            self.assertEqual(calc.call_count, 3)
        self.assertEqual(metrics['recalculate_skipped'], 1)
