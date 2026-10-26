"""Real 1104 packets, original event-18 contract and atomic coupon settlement."""
import copy
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

from network_redirect import formation, gift_codes
from network_redirect.backend import Backend, CLIENT_CONFIG, login_fields
from network_redirect.protocol import encode, decode, DEFS

NOW = 1792972800


class GiftCodeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.b = self.backend()
        self.addCleanup(lambda: self.b.close())
        self.serial = 0
        self.b.profile()

    def backend(self, account='local-player'):
        return Backend(Path(self.tmp.name), 18770, lambda *a, **kw: None, account=account)

    def request(self, code='JGBOL387', flag=0, serial=None, backend=None):
        self.serial += 1
        self.packet = encode(1104, dict(serial_num=self.serial if serial is None else serial, sn=code, flag=flag))
        with patch('network_redirect.backend.time.time', return_value=NOW):
            self.replies = (backend or self.b).respond(self.packet, {'authenticated': True})
        self.decoded = [decode(p) for p in self.replies]
        return next(login_fields(d['data']) for m, _, d in self.decoded if m == 2998 and d['id'] == 18)

    def claims(self):
        return self.b.db.execute('SELECT * FROM gift_code_claims ORDER BY code,account').fetchall()

    def reject(self, result, **kw):
        before, claims = self.b.profile(), self.claims()
        self.assertEqual(self.request(**kw)['result'], result)
        self.assertEqual(self.b.profile(), before)
        self.assertEqual(self.claims(), claims)

    def test_original_contract_and_entry(self):
        self.assertEqual(DEFS[1104], 'serial_num=I,sn=S[32],flag=B')
        self.assertIn('gift_card=true', CLIENT_CONFIG)
        result = self.request()
        self.assertEqual(result['client_flag'], 0)
        self.assertEqual(result['attach_count'], 3)
        self.assertEqual(result['attach_list'][1], dict(object_type=11, attach_type=0, attach_count=300, attach_level=1))
        self.assertEqual(result['name'], '本地启程礼包')
        self.assertEqual(self.decoded[-1][0], 1106)
        self.assertEqual(self.decoded[-1][2]['req_serial_num'], self.serial)

    def test_reward_and_sync_before_callback(self):
        before = self.b.profile()
        self.assertEqual(self.request()['result'], 1)
        after = self.b.profile()
        self.assertEqual(after['gold_coin'] - before['gold_coin'], 300)
        self.assertEqual(after['silver_coin'] - before['silver_coin'], 100000)
        count = lambda r: sum(i['count'] for i in r['attachments'] if i['type_id'] == 1001)
        self.assertEqual(count(after) - count(before), 10)
        callback = next(i for i, (m, _, d) in enumerate(self.decoded) if m == 2998 and d['id'] == 18)
        self.assertTrue(any(m == 1035 for m, _, _ in self.decoded[:callback]))
        self.assertTrue(any(m == 1032 for m, _, _ in self.decoded[:callback]))

    def test_two_independent_gifts(self):
        self.assertEqual(self.request()['result'], 1)
        self.assertEqual(self.request('JGBOLGIFT')['result'], 1)
        self.assertEqual(len(self.claims()), 2)

    def test_case_and_outer_whitespace(self):
        self.assertEqual(self.request('  jgbol387  ')['result'], 1)
        self.reject(13)

    def test_invalid_codes(self):
        for code in ('', 'UNKNOWN', 'JGB OL387', '礼包', 'x' * 31, 'JGBOL387\nBAD'):
            with self.subTest(code=code): self.reject(2, code=code)

    def test_disabled_unissued_and_time_boundaries(self):
        row = self.b.gift_code_rules['codes'][0]
        row['enabled'] = False
        self.reject(2)
        row.update(enabled=True, issued=False)
        self.reject(4)
        row.update(issued=True, starts_at=NOW+1)
        self.reject(4)
        row.update(starts_at=NOW-10, expires_at=NOW)
        self.reject(14)
        row.update(starts_at=NOW, expires_at=NOW+1)
        self.assertEqual(self.request()['result'], 1)

    def test_bindings(self):
        row = self.b.gift_code_rules['codes'][0]
        for field, value, result in [('account','someone',6),('role_id',999,7),('server_id',999,8),('platform','official',9)]:
            with self.subTest(field=field):
                row[field] = value
                self.reject(result)
                del row[field]
        role = self.b.profile()
        row.update(account=self.b.account, role_id=int(role['role_id']), server_id=role['area_id'], platform='local')
        self.assertEqual(self.request()['result'], 1)

    def test_repeat_and_mutually_exclusive_group(self):
        self.assertEqual(self.request()['result'], 1)
        self.reject(13)
        self.b.gift_code_rules['codes'][1]['group'] = self.b.gift_code_rules['codes'][0]['group']
        self.reject(12, code='JGBOLGIFT')

    def test_exact_replay_and_serial_reuse(self):
        self.request()
        replies, packet, before = self.replies, self.packet, self.b.profile()
        self.assertEqual(self.b.respond(packet, {'authenticated': True}), replies)
        self.assertEqual(before, self.b.profile())
        self.reject(15, code='JGBOLGIFT', serial=1)
        self.reject(15, serial=0)

    def test_restart_preserves_claims(self):
        self.request()
        self.b.close()
        self.b = self.backend()
        self.reject(13)

    def test_other_account_shared_code(self):
        self.request()
        other = self.backend('other')
        try: self.assertEqual(self.request(backend=other)['result'], 1)
        finally: other.close()
        self.assertEqual(len(self.claims()), 2)

    def test_global_single_use(self):
        self.b.gift_code_rules['codes'][0]['max_uses'] = 1
        self.request()
        other = self.backend('other')
        other.gift_code_rules['codes'][0]['max_uses'] = 1
        try: self.assertEqual(self.request(backend=other)['result'], 5)
        finally: other.close()
        self.assertEqual(len(self.claims()), 1)

    def test_concurrent_global_limit(self):
        # Each worker owns its SQLite connection, like independent server instances.
        def claim(account):
            b = self.backend(account)
            try:
                b.gift_code_rules['codes'][0]['max_uses'] = 1
                packets = b.respond(encode(1104, dict(serial_num=1, sn='JGBOL387', flag=0)), {'authenticated': True})
                return next(login_fields(d['data'])['result'] for m, _, d in map(decode, packets) if m == 2998 and d['id'] == 18)
            finally: b.close()
        with ThreadPoolExecutor(max_workers=2) as pool:
            self.assertEqual(sorted(pool.map(claim, ['a', 'b'])), [1, 5])
        self.assertEqual(len(self.claims()), 1)

    def test_overflow_rolls_back(self):
        role = self.b.profile()
        role['gold_coin'] = 2147483647
        self.b.save(role)
        self.reject(15)

    def test_encoder_failure_rolls_back_ledger_and_rewards(self):
        with patch.object(self.b, 'inventory', side_effect=ValueError('encode failure')):
            self.reject(15)
        self.assertEqual(self.request()['result'], 1)

    def test_save_failure_rolls_back_ledger(self):
        with patch.object(self.b, 'save', side_effect=ValueError('save failure')):
            self.reject(15)
        self.assertEqual(self.request()['result'], 1)

    def test_unsupported_friend_flag(self):
        for flag in (1, 2, 3, 255):
            self.reject(15, flag=flag)
            self.assertEqual(next(login_fields(d['data']) for m, _, d in self.decoded if m == 2998)['client_flag'], flag)

    def test_unauthenticated(self):
        with self.assertRaises(ValueError):
            self.b.respond(encode(1104, dict(serial_num=1, sn='JGBOL387')), {})
        self.assertEqual(self.claims(), [])

    def test_invalid_configuration(self):
        for change in ({'code':'a'}, {'max_uses':-1}, {'expires_at':1,'starts_at':2}, {'prizes':[[5,999999,1,1]]}, {'prizes':[]}, {'prizes':[[11,0,True,1]]}):
            rules = copy.deepcopy(self.b.gift_code_rules)
            rules['codes'][0].update(change)
            with self.subTest(change=change), self.assertRaises(formation.Rejected): gift_codes.validate(rules)
        rules = copy.deepcopy(self.b.gift_code_rules)
        rules['codes'].append(copy.deepcopy(rules['codes'][0]))
        with self.assertRaises(formation.Rejected): gift_codes.validate(rules)


if __name__ == '__main__':
    unittest.main()
