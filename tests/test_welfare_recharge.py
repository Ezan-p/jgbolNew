"""Single orders, native spring gifts and weekly/daily boundaries."""
import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from network_redirect import daily, formation, welfare
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode, encode

NOW = 1792857600


class WelfareRechargeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.backend = Backend(Path(self.temp.name), 1, lambda *a, **k: None)
        self.rules = self.backend.welfare_rules
        # Explicit opt-in for legacy reward mechanics, disabled in production.
        self.rules['order'] = sorted(welfare.TYPES)
        self.rules['spring_charge_enabled'] = True
        self.serial = 0

    def tearDown(self):
        self.backend.close()
        self.temp.cleanup()

    def role(self):
        role = self.backend.profile()
        welfare.prepare(role, NOW, self.rules)
        return role

    def request(self, mid, now=NOW, **values):
        self.serial += 1
        with patch('network_redirect.backend.time.time', return_value=now):
            replies = self.backend.respond(encode(mid, dict(serial_num=self.serial, **values)), dict(authenticated=True))
        return [(data['id'], login_fields(data['data'])) for kind, _, data in map(decode, replies) if kind == 2998]

    def test_split_orders_do_not_unlock_single_charge_tier(self):
        role = self.role()
        welfare.record_charge(role, 50, NOW, self.rules)
        welfare.record_charge(role, 50, NOW, self.rules)
        single = welfare.single_catalog(role, NOW, self.rules)
        self.assertEqual(single['max_rmb'], 5)
        self.assertEqual(single['rows'][0]['status'], 1)  # 6 yuan
        self.assertEqual(welfare.catalog(role, NOW, self.rules)[23]['prize_list'][1]['status'], 2)
        with self.assertRaises(formation.Rejected):
            welfare.claim_single(role, 1, NOW, self.rules)
        welfare.record_charge(role, 300, NOW, self.rules, fund=True)
        single = welfare.single_catalog(role, NOW, self.rules)
        self.assertEqual(single['max_rmb'], 30)
        self.assertEqual([x['status'] for x in single['rows']], [2, 2, 1, 1])

    def test_single_reward_once_and_persists(self):
        role = self.role()
        welfare.record_charge(role, 1000, NOW, self.rules)
        before = role['gold_coin']
        welfare.claim_single(role, 2, NOW, self.rules)
        self.assertEqual(role['gold_coin'] - before, self.rules['single_charge'][1]['prizes'][0][2])
        self.backend.save(role)
        self.backend.close()
        self.backend = Backend(Path(self.temp.name), 1, lambda *a, **k: None)
        saved = self.backend.profile()
        self.assertEqual(welfare.single_catalog(saved, NOW, self.rules)['rows'][1]['status'], 3)
        with self.assertRaises(formation.Rejected):
            welfare.claim_single(saved, 2, NOW, self.rules)
        for invalid in (0, 5, -1, True, '1'):
            with self.assertRaises(formation.Rejected):
                welfare.claim_single(saved, invalid, NOW, self.rules)

    def test_single_does_not_infer_legacy_daily_total_or_accept_invalid_amounts(self):
        role = self.role()
        role['welfare']['charge_days'] = {str(daily.day(NOW, self.rules)): 50000}
        role['welfare'].pop('single_max_gold')
        self.assertEqual(welfare.single_catalog(role, NOW, self.rules)['max_rmb'], 0)
        for invalid in (0, -1, True, 1.5, '50'):
            before = copy.deepcopy(role)
            with self.assertRaises(formation.Rejected):
                welfare.record_charge(role, invalid, NOW, self.rules)
            self.assertEqual(role, before)

    def test_native_spring_query_claim_threshold_and_restart(self):
        role = self.role()
        welfare.record_charge(role, 50, NOW, self.rules)
        self.backend.save(role)
        query = next(data for event, data in self.request(1216, flag=1) if event == 93)
        self.assertEqual(query[1]['status'], 1)
        self.assertEqual(query['total_charge_count'], 5)
        before = self.backend.profile()
        self.assertEqual(self.request(1215, prize_id=1)[-1][0], 55)
        self.assertEqual(before, self.backend.profile())
        welfare.record_charge(role, 50, NOW, self.rules)
        self.backend.save(role)
        event = next(data for event, data in self.request(1215, prize_id=1) if event == 92)
        self.assertEqual(event['status'], 3)
        self.assertEqual(event['prize_info']['min_money_range'], 6)
        self.assertTrue(event['prize_info']['prize_list'])
        before = self.backend.profile()
        self.assertEqual(self.request(1215, prize_id=1)[-1][0], 55)
        self.assertEqual(before, self.backend.profile())
        self.backend.close()
        self.backend = Backend(Path(self.temp.name), 1, lambda *a, **k: None)
        self.assertEqual(self.request(1215, prize_id=1)[-1][0], 55)

    def test_spring_and_single_closed_at_exact_end(self):
        role = self.role()
        welfare.record_charge(role, 1000, NOW, self.rules)
        end = role['welfare']['start'] + self.rules['season_days'] * 86400
        self.assertEqual(welfare.single_catalog(role, end - 1, self.rules)['rows'][0]['status'], 2)
        self.assertEqual(welfare.single_catalog(role, end, self.rules)['rows'][0]['status'], 1)
        with self.assertRaises(formation.Rejected):
            welfare.claim_single(role, 1, end, self.rules)
        self.assertEqual(welfare.spring_info(role, end, self.rules)[1]['status'], 1)
        with self.assertRaises(formation.Rejected):
            welfare.spring_settle(role, 1215, dict(prize_id=1), end, self.rules)
        before = copy.deepcopy(role['welfare']['charge_days'])
        welfare.record_charge(role, 5000, end, self.rules)
        self.assertEqual(role['welfare']['charge_days'], before)
        self.assertEqual(role['welfare']['single_max_gold'], 1000)

    def test_weekly_monday_zero_boundary_and_daily_independence(self):
        day = daily.day(NOW, self.rules)
        monday = (welfare.week_start(day) + 7) * 86400 - self.rules['timezone_offset_hours'] * 3600
        role = self.role()
        welfare.record_charge(role, 300, monday - 1, self.rules)
        welfare.settle(role, 1352, dict(id=2, data='{index=1}'), monday - 1, self.rules, login_fields)
        sunday = welfare.catalog(role, monday - 1, self.rules)[74]['data']
        self.assertEqual(sunday['total_charge'], 30)
        self.assertEqual(sunday['total_charge_data'][0]['status'], 3)
        monday_data = welfare.catalog(role, monday, self.rules)[74]['data']
        self.assertEqual(monday_data['total_charge'], 0)
        self.assertEqual(monday_data['total_charge_data'][0]['status'], 1)
        self.assertEqual(monday_data['charge_rmb'], 0)
        welfare.record_charge(role, 300, monday, self.rules)
        monday_data = welfare.catalog(role, monday, self.rules)[74]['data']
        self.assertEqual(monday_data['total_charge_data'][0]['status'], 2)
        welfare.settle(role, 1352, dict(id=2, data='{index=1}'), monday, self.rules, login_fields)
        self.assertEqual(welfare.catalog(role, monday, self.rules)[23]['prize_list']['total_charge_count'], 60)

    def test_legacy_weekly_claims_stay_claimed_for_upgrade_week(self):
        role = self.role()
        welfare.record_charge(role, 1000, NOW, self.rules)
        state = role['welfare']
        state['claims'].append('74:100')
        state.pop('weekly_claims_migrated')
        self.assertEqual(welfare.catalog(role, NOW, self.rules)[74]['data']['total_charge_data'][0]['status'], 3)
        self.assertEqual(state['claims'].count('74:100:' + welfare.week_period(daily.day(NOW, self.rules))), 1)

    def test_utc8_day_and_streak_gap(self):
        role = self.role()
        next_midnight = (daily.day(NOW, self.rules) + 1) * 86400 - self.rules['timezone_offset_hours'] * 3600
        welfare.record_charge(role, 100, next_midnight - 1, self.rules)
        before = welfare.catalog(role, next_midnight - 1, self.rules)
        self.assertEqual(before[71]['charge_rmb'], 10)
        after = welfare.catalog(role, next_midnight, self.rules)
        self.assertEqual(after[71]['charge_rmb'], 0)
        welfare.record_charge(role, 100, next_midnight, self.rules)
        self.assertEqual(welfare.catalog(role, next_midnight, self.rules)[71]['day'], 2)
        welfare.record_charge(role, 100, next_midnight + 2 * 86400, self.rules)
        self.assertEqual(welfare.catalog(role, next_midnight + 2 * 86400, self.rules)[71]['day'], 2)


if __name__ == '__main__':
    unittest.main()
