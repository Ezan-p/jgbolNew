"""Resource boundary, persistence and real-wire regressions; no live saves."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from network_redirect import journey, formation, summon
from network_redirect.backend import Backend
from network_redirect.protocol import decode, encode

NOW = 1793145600  # 2026-10-28 08:00 Asia/Shanghai, on an hourly boundary.


class RecoveryRulesTests(unittest.TestCase):
    def setUp(self):
        self.rules = journey.load_rules()
        self.role = dict(strength=0, energy=0)
        journey.recover_resources(self.role, NOW, self.rules)

    def recover(self, seconds):
        journey.recover_resources(self.role, NOW + seconds, self.rules)
        return self.role['strength'], self.role['energy']

    def test_original_periods_and_exact_boundaries(self):
        self.assertEqual(self.recover(360), (0, 0))
        self.assertEqual(self.recover(900), (0, 0))
        self.assertEqual(self.recover(1799), (0, 0))
        self.assertEqual(self.recover(1800), (1, 0))
        self.assertEqual(self.recover(3599), (1, 0))
        self.assertEqual(self.recover(3600), (2, 1))

    def test_repeated_settlement_does_not_duplicate_or_lose_partial_time(self):
        for seconds in range(0, 3600, 17):
            self.recover(seconds)
        self.assertEqual(self.recover(3600), (2, 1))
        before = copy.deepcopy(self.role)
        self.recover(3600)
        self.assertEqual(self.role, before)

    def test_long_offline_caps_and_overflow_preserved(self):
        self.assertEqual(self.recover(365 * 86400), (30, 15))
        self.role.update(strength=75, energy=42)
        self.assertEqual(self.recover(366 * 86400), (75, 42))

    def test_full_capacity_discards_elapsed_ticks(self):
        self.role.update(strength=30, energy=15)
        self.recover(86400 + 100)
        self.role.update(strength=29, energy=14)
        self.assertEqual(self.recover(86400 + 101), (29, 14))
        self.assertEqual(self.recover(86400 + 1800), (30, 14))
        self.assertEqual(self.recover(86400 + 3600), (30, 15))

    def test_old_partial_checkpoints_follow_native_fixed_schedule(self):
        self.role['journey'].update(strength_recovery_at=NOW + 123,
                                    energy_recovery_at=NOW + 123)
        self.assertEqual(self.recover(1799), (0, 0))
        self.assertEqual(self.recover(1800), (1, 0))
        self.assertEqual(self.recover(3600), (2, 1))

    def test_missing_clocks_start_now_without_retroactive_grants(self):
        self.role.pop('journey')
        self.assertEqual(self.recover(365 * 86400 + 100), (0, 0))
        self.assertEqual(self.recover(365 * 86400 + 1800), (1, 0))

    def test_clock_rollback_never_reprocesses_ticks(self):
        self.assertEqual(self.recover(3600), (2, 1))
        self.role.update(strength=0, energy=0)
        self.assertEqual(self.recover(0), (0, 0))
        self.assertEqual(self.recover(3600), (0, 0))
        self.assertEqual(self.recover(7200), (2, 1))

    def test_midnight_is_one_tick_not_daily_refill(self):
        self.role['journey'].update(strength_recovery_at=NOW - 8 * 3600 - 1,
                                    energy_recovery_at=NOW - 8 * 3600 - 1)
        self.assertEqual(self.recover(-8 * 3600), (1, 1))

    def test_configuration_rejects_periods_native_ui_cannot_display(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'rules.json'
            for key, old in [('strength_recovery_seconds', 360), ('energy_recovery_seconds', 900)]:
                rules = dict(self.rules, **{key: old})
                path.write_text(json.dumps(rules))
                with self.assertRaises(formation.Rejected):
                    journey.load_rules(path)


class RecoveryBackendTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.clock = patch('network_redirect.backend.time.time', return_value=NOW).start()
        self.addCleanup(patch.stopall)
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.addCleanup(lambda: self.b.close())
        role = self.b.profile()
        role.update(strength=0, energy=0, level=60)
        self.b.save(role)

    def test_profile_recovers_before_non_journey_consumer_and_persists(self):
        self.clock.return_value = NOW + 3600
        role = self.b.profile()
        self.assertEqual((role['strength'], role['energy']), (2, 1))
        stored = json.loads(self.b.db.execute('SELECT data FROM roles').fetchone()[0])
        self.assertEqual(stored['energy'], 1)
        self.assertEqual(self.b.profile(), role)

    def test_restart_and_login_snapshot_recover_once(self):
        self.b.close()
        self.clock.return_value = NOW + 7200
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        packets = [decode(p) for p in self.b.bootstrap()]
        login = next(d for mid, _, d in packets if mid == 1017)
        self.assertEqual((login['strength'], login['energy']), (4, 2))
        self.assertEqual((login['renew_time1'], login['renew_time2']), (0, 0))
        self.assertEqual(login['server_time'], NOW + 7200)
        self.assertEqual(self.b.profile()['energy'], 2)

    def test_online_heartbeat_sends_authoritative_resource_values(self):
        self.clock.return_value = NOW + 3600
        packets = [decode(p) for p in self.b.respond(encode(2999, {}), {'authenticated': True})]
        self.assertEqual(packets[0][0], 2999)
        attrs = {a['type']: a['value'] for mid, _, d in packets if mid == 1032 and d['unit_type'] == 1
                 for a in d['attr_list']}
        self.assertEqual((attrs[101], attrs[102]), (2, 1))
        self.assertEqual(self.b.profile()['strength'], 2)

    def test_recovered_energy_available_to_rank_battle_without_heartbeat(self):
        state = {'authenticated': True}
        packets = self.b.respond(encode(1021, dict(serial_num=100001, flag=0)), state)
        board = next(d for mid, _, d in map(decode, packets) if mid == 1022)
        target = max((r for r in board['show_list'] if r['top_relation'] == 2), key=lambda r: r['order'])
        self.clock.return_value = NOW + 3600
        request = encode(1026, dict(serial_num=100002, fight_type=2, des_type=2,
                                   des_id=target['id'], des_value=target['order']))
        packets = self.b.respond(request, state)
        self.assertIn(1027, [decode(p)[0] for p in packets])
        self.assertEqual(self.b.profile()['energy'], 0)
        self.assertEqual(self.b.respond(request, state), packets)
        self.assertEqual(self.b.profile()['energy'], 0)

    def test_item_overflow_remains_after_offline_recovery(self):
        role = self.b.profile()
        summon.add_item(role, 1023, 2)
        item = next(i for i in role['attachments'] if i['type_id'] == 1023)
        self.b.save(role)
        self.b.respond(encode(1051, dict(serial_num=100001, item_type=1023, item_id=item['id'],
                                        item_count=2, des_type=1)), {'authenticated': True})
        self.assertEqual(self.b.profile()['energy'], 20)
        self.clock.return_value = NOW + 86400
        self.assertEqual(self.b.profile()['energy'], 20)

    def test_existing_save_missing_clocks_keeps_progress(self):
        role = self.b.profile()
        role['journey'].pop('strength_recovery_at')
        role['journey'].pop('energy_recovery_at')
        role['journey']['claimed_maps'] = [1]
        self.b.save(role)
        self.clock.return_value = NOW + 86400
        migrated = self.b.profile()
        self.assertEqual((migrated['strength'], migrated['energy']), (0, 0))
        self.assertEqual(migrated['journey']['claimed_maps'], [1])
        self.clock.return_value += 3600
        self.assertEqual(self.b.profile()['energy'], 1)

    def test_accounts_have_separate_checkpoints_and_balances(self):
        other = self.b.profile('another-player')
        other.update(strength=30, energy=15)
        self.b.save(other, 'another-player')
        self.clock.return_value = NOW + 3600
        self.assertEqual(self.b.profile()['energy'], 1)
        self.assertEqual(self.b.profile('another-player')['energy'], 15)


if __name__ == '__main__':
    unittest.main()
