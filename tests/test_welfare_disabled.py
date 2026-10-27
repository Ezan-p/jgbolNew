"""Shipping menu removal, legacy requests and automatic payout regression."""
import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from network_redirect import welfare
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode, encode

NOW = 1793066400
REMOVED = {24, 33, 34, 35, 48, 67, 71, 74}
RETAINED = [20, 22, 7, 16, 23, 21, 32, 36, 60]


class DisabledWelfareTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.backend = Backend(Path(self.temp.name), 1, lambda *a, **k: None)
        self.addCleanup(lambda: self.backend.close())
        self.rules = self.backend.welfare_rules
        self.serial = 0

    def request(self, mid, **values):
        self.serial += 1
        with patch('network_redirect.backend.time.time', return_value=NOW):
            packets = self.backend.respond(encode(mid, dict(serial_num=self.serial, **values)),
                                           dict(authenticated=True))
        return [(data['id'], login_fields(data['data']))
                for kind, _, data in map(decode, packets) if kind == 2998]

    def test_menu_passive_refresh_and_hints_exclude_removed_entries(self):
        role = self.backend.profile()
        welfare.record_charge(role, 10000, NOW, self.rules)
        self.backend.save(role)
        menu = next(data for event, data in self.request(1127, flag=1, act_type=0, index=0) if event == 127)
        self.assertEqual(list(menu['order_list'].values()), RETAINED)
        self.assertEqual(set(menu['all_activity']), set(RETAINED))
        state = welfare.client_state(role, NOW, self.rules)
        self.assertEqual(set(state['all_activity']), set(RETAINED))
        hints = login_fields(decode(welfare.hint(role, NOW, self.rules))[2]['data'])
        self.assertTrue(all(hints[24]['activity_info']['had_prize_flag'][a] is False for a in REMOVED))
        self.assertEqual(role['welfare']['turn_results'], {})
        self.assertNotIn('max_streak', role['welfare'])

    def test_removed_requests_rejected_without_changing_save(self):
        role = self.backend.profile()
        welfare.record_charge(role, 10000, NOW, self.rules)
        self.backend.save(role)
        requests = [(1127, dict(flag=flag, act_type=a, index=1))
                    for a in REMOVED for flag in (1, 2)]
        requests += [(1239, dict(buy_count=1)), (1215, dict(prize_id=1))]
        requests += [(1352, dict(id=op, data='{index=1}')) for op in (2, 3)]
        for mid, data in requests:
            with self.subTest(mid=mid, data=data):
                before = copy.deepcopy(self.backend.profile())
                self.assertTrue(any(event == 55 for event, _ in self.request(mid, **data)))
                self.assertEqual(self.backend.profile(), before)

    def test_daily_and_activity_queries_report_closed(self):
        daily = next(data for event, data in self.request(1352, id=1, data='{}') if event == 202)
        self.assertFalse(daily['data']['isopen'])
        spring = next(data for event, data in self.request(1216, flag=1) if event == 93)
        self.assertEqual(spring, dict(start_time=0, end_time=0, total_charge_count=0))
        activity = next(data for event, data in self.request(1205, flag=0) if event == 47)
        self.assertEqual(activity['spring_info'], spring)

    def test_recharge_no_longer_pays_removed_automatic_rewards(self):
        role = self.backend.profile()
        before = role['gold_coin']
        welfare.record_charge(role, 1000, NOW, self.rules)
        self.assertEqual(role['gold_coin'] - before, 1000)  # first-charge double only
        welfare.record_charge(role, 1000, NOW + 86400, self.rules)
        self.assertEqual(role['gold_coin'] - before, 1000)
        self.assertFalse(any(key.split(':')[0] in ('48', '67') for key in role['welfare']['claims']))
        welfare.prepare(role, NOW + 29 * 86400, self.rules)
        self.assertNotIn('anniversary', role['welfare'].get('mails', {}))

    def test_existing_claims_and_issued_mail_are_preserved(self):
        role = self.backend.profile()
        legacy = dict(self.rules, order=sorted(welfare.TYPES))
        welfare.record_charge(role, 10000, NOW, legacy)
        welfare.prepare(role, NOW + 29 * 86400, legacy)
        previous = copy.deepcopy(role['welfare'])
        welfare.prepare(role, NOW + 29 * 86400, self.rules)
        self.assertEqual(role['welfare']['claims'], previous['claims'])
        self.assertEqual(role['welfare']['mails'], previous['mails'])
        self.backend.save(role)
        self.backend.close()
        self.backend = Backend(Path(self.temp.name), 1, lambda *a, **k: None)
        self.assertEqual(self.backend.welfare_rules['order'], RETAINED)
        self.assertEqual(self.backend.profile()['welfare']['mails'], previous['mails'])


if __name__ == '__main__':
    unittest.main()
