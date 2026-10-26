"""Original 1088 wire requests, economic invariants and persistence."""
import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from network_redirect import formation as f, item_sale as sale, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode


class ItemSaleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **kw: None)
        self.addCleanup(lambda: self.b.close())
        self.serial = 1000

    def add(self, tid=7010, count=20, **fields):
        role = self.b.profile()
        item = dict(id=f.new_id(role), attach_type=5, type_id=tid, count=count, level=1)
        item.update(fields)
        role['attachments'].append(item)
        self.b.save(role)
        return item['id']

    def request(self, items=None, raw=None):
        self.serial += 1
        self.packet = encode(1088, dict(serial_num=self.serial,
                            data=raw if raw is not None else summon.lua(dict(item_list=items))))
        self.replies = self.b.respond(self.packet, {'authenticated': True})
        self.decoded = [decode(p) for p in self.replies]
        self.assertEqual(self.decoded[-1][0], 1106)
        self.assertEqual(self.decoded[-1][2]['req_serial_num'], self.serial)
        return [(d['id'], login_fields(d['data'])) for m, _, d in self.decoded if m == 2998][-1]

    def reject(self, **kwargs):
        before = self.b.profile()
        self.assertEqual(self.request(**kwargs)[0], 55)
        self.assertEqual(self.b.profile(), before)

    def test_partial_and_full_sale_sync_order(self):
        ident = self.add()
        silver = self.b.profile()['silver_coin']
        self.assertEqual(self.request({7010: 3}), (153, {'silver_count': 3000}))
        role = self.b.profile()
        self.assertEqual(role['silver_coin'], silver + 3000)
        self.assertEqual(next(i['count'] for i in role['attachments'] if i['id'] == ident), 17)
        self.assertTrue(any(m == 1032 and d['id'] == ident and
                            {'type': 102, 'value': 17} in d['attr_list'] for m, _, d in self.decoded))
        mids = [m for m, _, _ in self.decoded]
        callback = next(n for n, (m, _, d) in enumerate(self.decoded) if m == 2998 and d['id'] == 153)
        self.assertLess(mids.index(1035), callback)
        self.assertTrue(any(m == 1032 and d['unit_type'] == 1 and
                            {'type': 7, 'value': silver + 3000} in d['attr_list'] for m, _, d in self.decoded))
        self.assertEqual(self.request({7010: 17})[0], 153)
        self.assertFalse(any(i['id'] == ident for i in self.b.profile()['attachments']))
        self.assertTrue(any(m == 1032 and d['id'] == ident and
                            {'type': 102, 'value': 0} in d['attr_list'] for m, _, d in self.decoded))
        self.reject(items={7010: 1})

    def test_every_original_type_and_multi_type_batch(self):
        self.assertEqual(set(sale.PRICES), set(range(7010, 7024)) | set(range(8009, 8023)))
        for tid in sale.PRICES:
            self.add(tid, 2)
            self.assertEqual(self.request({tid: 1}), (153, {'silver_count': 1000}))
        self.assertEqual(self.request(dict.fromkeys(sale.PRICES, 1)), (153, {'silver_count': 28000}))
        self.assertFalse(any(i['type_id'] in sale.PRICES for i in self.b.profile()['attachments']))

    def test_no_equipment_500_limit_or_level_gate(self):
        self.add(count=1200)
        self.assertEqual(self.b.profile()['level'], 1)
        self.assertEqual(self.request({7010: 1200}), (153, {'silver_count': 1200000}))

    def test_invalid_payloads_are_atomic(self):
        self.add()
        for raw in ('', '{}', '{item_list={}}', '{item_list=1}', '{item_list={7010,2}}',
                    '{item_list={[7010]=0}}', '{item_list={[7010]=-1}}',
                    '{item_list={[7010]=1.5}}', '{item_list={[7010]=true}}',
                    '{item_list={[7010]="2"}}', '{item_list={["7010"]=2}}',
                    '{item_list={[true]=2}}', '{item_list={[7010]=2147483648}}',
                    '{item_list={[7010]=2,[7010]=3}}', '{item_list={[7010]=1},silver_count=999999}',
                    '{item_list={[7010]=os.execute("false")}}', '{item_list={[7010]=1}}; return {}'):
            with self.subTest(raw=raw):
                self.reject(raw=raw)

    def test_unsupported_items_and_whole_batch_rollback(self):
        self.add()
        for tid in (1001, 1002, 2001, 6001, 7001, 8001, 999999):
            self.add(tid)
            self.reject(items={7010: 1, tid: 1})
        self.reject(items={7010: 1, 7011: 1})
        self.reject(items={7010: 21})
        # The settlement function itself must validate all entries before mutating.
        role = self.b.profile()
        before = copy.deepcopy(role)
        with self.assertRaises(f.Rejected):
            sale.settle(role, {'data': '{item_list={[7010]=1,[7011]=1}}'}, login_fields)
        self.assertEqual(role, before)

    def test_locked_bound_and_abnormal_stacks_are_protected(self):
        for field, value in (('is_lock', 1), ('owner_id', 42), ('equip_order', 1),
                             ('equip_pos', 1), ('level', 2), ('star_level', 1),
                             ('attach_type', 6), ('ext_skill_pos', 1), ('ext_awaken_pos', 1)):
            with self.subTest(field=field):
                role = self.b.profile(); role['attachments'] = []; self.b.save(role)
                self.add(**{field: value})
                self.reject(items={7010: 1})

    def test_split_stacks_skip_locked_and_preserve_other_items(self):
        first = self.add(count=2)
        locked = self.add(count=10, is_lock=1)
        last = self.add(count=5)
        other = self.add(1001, 8)
        self.assertEqual(self.request({7010: 4})[0], 153)
        counts = {i['id']: i['count'] for i in self.b.profile()['attachments']}
        self.assertEqual({k: counts[k] for k in (locked, last, other)}, {locked: 10, last: 3, other: 8})
        self.assertNotIn(first, counts)
        self.reject(items={7010: 4})

    def test_lock_unlock_via_original_protocol(self):
        ident = self.add()
        for flag in (1, 2):
            self.serial += 1
            self.b.respond(encode(1343, dict(serial_num=self.serial, des_id=ident, flag=flag)), {'authenticated': True})
            if flag == 1:
                self.reject(items={7010: 1})
        self.assertEqual(self.request({7010: 1})[0], 153)

    def test_replay_changed_payload_expired_and_retransmit(self):
        self.add()
        self.request({7010: 1})
        before = self.b.profile()
        self.assertEqual(self.b.respond(self.packet, {'authenticated': True}), self.replies)
        packet = encode(1088, dict(serial_num=self.serial, data='{item_list={[7010]=2}}'))
        replies = self.b.respond(packet, {'authenticated': True})
        self.assertTrue(any(m == 2998 and d['id'] == 55 for m, _, d in map(decode, replies)))
        self.b.formation_replies.clear()
        self.b.respond(self.packet, {'authenticated': True})
        self.b.respond(encode(1105, dict(req_serial_num=0)), {'authenticated': True})
        self.assertEqual(self.b.profile(), before)

    def test_balance_limit_and_encode_failure_rollback(self):
        self.add()
        role = self.b.profile(); role['silver_coin'] = sale.MAX_INT - 1000; self.b.save(role)
        self.assertEqual(self.request({7010: 1})[0], 153)
        self.assertEqual(self.b.profile()['silver_coin'], sale.MAX_INT)
        self.reject(items={7010: 1})
        role = self.b.profile(); role['silver_coin'] = 100; self.b.save(role)
        with patch.object(self.b, 'inventory', side_effect=ValueError('injected serialization failure')):
            self.reject(items={7010: 1})

    def test_restart_and_account_isolation(self):
        self.add()
        self.request({7010: 7})
        before = self.b.profile()
        self.b.close()
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **kw: None)
        self.assertEqual(self.b.profile(), before)
        with tempfile.TemporaryDirectory() as directory:
            other = Backend(Path(directory), 18770, lambda *a, **kw: None)
            try:
                replies = other.respond(encode(1088, dict(serial_num=1, data='{item_list={[7010]=1}}')), {'authenticated': True})
                self.assertTrue(any(m == 2998 and d['id'] == 55 for m, _, d in map(decode, replies)))
                self.assertEqual(self.b.profile(), before)
            finally:
                other.close()


if __name__ == '__main__':
    unittest.main()
