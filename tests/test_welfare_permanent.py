"""Shipping welfare: permanent availability, lifetime receipts and legacy migration."""
import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from network_redirect import daily, summon, welfare
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode, encode

NOW = 1793066400


class PermanentWelfareTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.backend = Backend(Path(self.temp.name), 1, lambda *a, **k: None)
        self.addCleanup(lambda: self.backend.close())
        self.serial = 0
        self.now = NOW
        self.rules = self.backend.welfare_rules

    def request(self, mid=1127, **values):
        self.serial += 1
        packet = encode(mid, dict(serial_num=self.serial, **values))
        with patch('network_redirect.backend.time.time', return_value=self.now):
            replies = self.backend.respond(packet, dict(authenticated=True))
        return [(data['id'], login_fields(data['data']))
                for kind, _, data in map(decode, replies) if kind == 2998]

    def claim(self, activity, index=0):
        if activity == 20:
            return self.request(1201, flag=6, id=0)
        return self.request(act_type=activity, index=index, flag=2)

    def ready(self):
        role = self.backend.profile()
        role.update(level=60, vip_level=10, buy_growup=1, silver_coin=1000000)
        welfare.record_charge(role, 10000, NOW, self.rules)
        state = role['welfare']
        day = daily.day(NOW, self.rules)
        state['login_days'] = list(range(day-6, day+1))
        state['start'] = NOW-400*86400
        summon.add_item(role, 1001, 100)
        self.backend.save(role)
        return role

    def test_all_seven_query_and_passive_state_have_no_deadline(self):
        role = self.ready()
        for now in (NOW, NOW+1000*86400):
            catalog = welfare.client_state(role, now, self.rules)['all_activity']
            self.assertEqual(set(catalog), welfare.PERMANENT_TYPES)
            for activity, info in catalog.items():
                self.assertTrue(info['permanent'], activity)
                self.assertEqual(info['end_time'], 0, activity)
            self.assertEqual(catalog[23]['prize_list']['end_time'], 0)
            self.assertEqual(catalog[32]['flush_time'], 0)

    def test_every_reward_once_after_old_expiry_across_days_and_restart(self):
        self.ready()
        rewards = [(20, 0), (22, 0), (7, 0), (16, 0), (23, 0)]
        rewards += [(21, i) for i in range(11)] + [(32, 1), (32, 2)]
        for activity, index in rewards:
            with self.subTest(first=(activity, index)):
                self.assertTrue(any(event in (60, 127) for event, _ in self.claim(activity, index)))
                before = self.backend.profile()
                self.assertTrue(any(event == 55 for event, _ in self.claim(activity, index)))
                self.assertEqual(before, self.backend.profile())
        self.backend.close()
        self.backend = Backend(Path(self.temp.name), 1, lambda *a, **k: None)
        for now in (NOW+86400, NOW+1000*86400):
            self.now = now
            for activity, index in rewards:
                with self.subTest(now=now, activity=activity, index=index), patch('network_redirect.backend.time.time', return_value=now):
                    before = self.backend.profile()
                    self.assertTrue(any(event == 55 for event, _ in self.claim(activity, index)))
                    self.assertEqual(before, self.backend.profile())

    def test_old_exchange_receipts_migrate_without_unlocking_or_consuming_materials(self):
        role = self.ready()
        old = ['32:1:19000', '32:1:19001', '32:2:19002']
        role['welfare']['claims'].extend(old)
        self.backend.save(role)
        for _ in range(2):
            role = self.backend.profile()
            catalog = welfare.catalog(role, NOW, self.rules)
            self.assertEqual(catalog[32]['take_flag'], [True, True])
            for key in old + ['32:1', '32:2']:
                self.assertEqual(role['welfare']['claims'].count(key), 1)
            self.backend.save(role)
        before = self.backend.profile()
        for index in (1, 2):
            self.assertTrue(any(event == 55 for event, _ in self.claim(32, index)))
            self.assertEqual(before, self.backend.profile())

    def test_late_charge_unlocks_only_unclaimed_tiers(self):
        role = self.ready()
        role['welfare']['charge_days'] = {}
        role['welfare']['claims'] = ['23:1']
        self.backend.save(role)
        before = self.backend.profile()
        self.assertTrue(any(event == 55 for event, _ in self.claim(23)))
        self.assertEqual(before, self.backend.profile())
        welfare.record_charge(role, 300, NOW, self.rules)
        self.backend.save(role)
        before = role['gold_coin']
        self.assertTrue(any(event == 127 for event, _ in self.claim(23)))
        self.assertEqual(self.backend.profile()['gold_coin'] - before, 60)
        self.assertEqual(welfare.catalog(self.backend.profile(), NOW, self.rules)[23]['prize_list'][2]['status'], 3)

    def test_same_packet_replay_does_not_double_exchange(self):
        self.ready()
        packet = encode(1127, dict(serial_num=900, act_type=32, index=1, flag=2))
        with patch('network_redirect.backend.time.time', return_value=NOW):
            replies = self.backend.respond(packet, dict(authenticated=True))
            before = copy.deepcopy(self.backend.profile())
            self.assertEqual(replies, self.backend.respond(packet, dict(authenticated=True)))
            self.assertEqual(before, self.backend.profile())
        self.assertIn('32:1', before['welfare']['claims'])


if __name__ == '__main__':
    unittest.main()
