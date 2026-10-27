"""1246 original wire requests, ownership rates, inventory safety and persistence."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from network_redirect import formation as f, immortal, summon, xianyuan_fruit as fruit
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode


class XianyuanFruitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.addCleanup(lambda: self.b.close())
        self.serial = 1000
        self.ident = self.add(1246, 200)

    def add(self, tid, n, **fields):
        role = self.b.profile()
        item = dict(id=f.new_id(role), attach_type=5, type_id=tid, count=n, level=1)
        item.update(fields)
        role['attachments'].append(item)
        self.b.save(role)
        return item['id']

    def request(self, **changes):
        self.serial += 1
        req = dict(serial_num=self.serial, item_type=1246, item_id=self.ident,
                   item_count=1, des_type=10, des_id=5004)
        req.update(changes)
        self.packet = encode(1051, req)
        self.replies = self.b.respond(self.packet, {'authenticated': True})
        self.decoded = list(map(decode, self.replies))
        self.assertEqual(self.decoded[-1][0], 1106)
        self.assertEqual(self.decoded[-1][2]['req_serial_num'], req['serial_num'])
        return [(d['id'], login_fields(d['data'])) for m, _, d in self.decoded if m == 2998][-1]

    def reject(self, **changes):
        before = self.b.profile()
        self.assertEqual(self.request(**changes)[0], 55)
        self.assertEqual(self.b.profile(), before)

    def test_bootstrap_and_reconnect_supply_original_catalog_shape(self):
        rules = self.b.immortal_rules['xianyuan_fruit']
        expected = {int(r['cortege_type']) for r in summon.rows('adaptive_spirit_convert.csv')
                    if f.BASES[int(r['cortege_type'])]['quality'] == '5'}
        self.assertEqual(set(rules['soul_targets']), expected)
        for reconnect in (False, True):
            cfg = login_fields(decode(self.b.bootstrap(reconnect=reconnect)[0])[2]['data'])[27]
            self.assertEqual(set(cfg[10]), expected)
            self.assertEqual(set(cfg[5]), set(range(5001, 5006)))
            self.assertTrue(all(v is True for v in cfg[10].values()))

    def test_owned_unowned_and_realms_use_distinct_rates_and_namespaces(self):
        before = self.b.profile()
        for kind, tid, count, gain in ((10, 5004, 3, 30), (10, 5001, 2, 2),
                                       (5, 5001, 15, 150)):
            event, data = self.request(des_type=kind, des_id=tid, item_count=count)
            self.assertEqual((event, data['result'], data['type_id'], data['count']), (21, 1, 1246, count))
            self.assertEqual(data['attach_list'][1], dict(object_type=kind, attach_type=tid,
                                                        attach_count=gain, attach_level=1))
        role = self.b.profile()
        self.assertEqual(role['souls']['5004'], 30)
        self.assertEqual(role['souls']['5001'], 2)
        self.assertEqual(next(i['count'] for i in role['attachments'] if i['id'] == self.ident), 180)
        for key in ('silver_coin', 'gold_coin', 'corteges'):
            self.assertEqual(role[key], before[key])
        self.assertNotIn(5001, role['handbook']['4'])

    def test_every_catalog_target_and_special_owned_only_filter(self):
        for tid in self.b.immortal_rules['xianyuan_fruit']['soul_targets']:
            with self.subTest(tid=tid):
                if tid in fruit.OWNED_ONLY:
                    self.reject(des_id=tid)
                else:
                    self.assertEqual(self.request(des_id=tid)[0], 21)
                role = self.b.profile()
                if not any(c['type'] == tid for c in role['corteges']):
                    role['corteges'].append(summon.companion(role, tid))
                    self.b.save(role)
                previous = self.b.profile().get('souls', {}).get(str(tid), 0)
                self.assertEqual(self.request(des_id=tid)[0], 21)
                self.assertEqual(self.b.profile()['souls'][str(tid)], previous + 10)
        for tid in range(5001, 5006):
            self.assertEqual(self.request(des_type=5, des_id=tid)[0], 21)

    def test_soul_and_handbook_history_do_not_count_as_current_ownership(self):
        role = self.b.profile()
        role['souls'] = {'5001': 39, '5027': 100}
        role['handbook']['4'] += [5001, 5027]
        self.b.save(role)
        self.assertEqual(self.request(des_id=5001)[1]['attach_list'][1]['attach_count'], 1)
        self.reject(des_id=5027)

    def test_invalid_requests_leave_all_state_unchanged(self):
        for changes in (dict(item_count=0), dict(item_count=4294967295), dict(item_count=16),
                        dict(item_count=2147483647), dict(item_id=0), dict(item_id=self.ident+.5),
                        dict(item_type=1249), dict(item_type=5001), dict(des_type=4),
                        dict(des_type=0), dict(des_type=5, des_id=4001), dict(des_id=4001),
                        dict(des_id=999999), dict(des_id=5004.5)):
            with self.subTest(changes=changes):
                self.reject(**changes)

    def test_unavailable_stack_is_never_consumed(self):
        for field, value in (('is_lock', 1), ('owner_id', 42), ('equip_order', 1),
                             ('equip_pos', 1), ('ext_skill_pos', 1), ('ext_awaken_pos', 1),
                             ('star_level', 1), ('level', 2), ('attach_type', 6), ('count', 0)):
            with self.subTest(field=field):
                role = self.b.profile()
                item = next(i for i in role['attachments'] if i['id'] == self.ident)
                original = copy.deepcopy(item)
                item[field] = value
                self.b.save(role)
                self.reject()
                role = self.b.profile()
                role['attachments'] = [original if i['id'] == self.ident else i for i in role['attachments']]
                self.b.save(role)

    def test_split_stacks_partial_full_and_insufficient_inventory(self):
        role = self.b.profile()
        next(i for i in role['attachments'] if i['id'] == self.ident)['count'] = 2
        self.b.save(role)
        locked = self.add(1246, 100, is_lock=1)
        other = self.add(1246, 3)
        self.reject(item_count=6)
        self.assertEqual(self.request(item_count=4)[0], 21)
        counts = {i['id']: i['count'] for i in self.b.profile()['attachments']}
        self.assertNotIn(self.ident, counts)
        self.assertEqual((counts[locked], counts[other]), (100, 1))
        self.assertTrue(any(m == 1032 and d['id'] == self.ident and
                            {'type': 102, 'value': 0} in d['attr_list'] for m, _, d in self.decoded))
        self.ident = other
        self.assertEqual(self.request()[0], 21)
        self.reject()

    def test_result_follows_bag_and_soul_sync(self):
        self.request(item_count=15)
        mids = [m for m, _, _ in self.decoded]
        callback = next(i for i, (m, _, d) in enumerate(self.decoded) if m == 2998 and d['id'] == 21)
        self.assertLess(mids.index(1035), callback)
        self.assertLess(mids.index(1046), callback)
        souls = [s for m, _, d in self.decoded if m == 1046 for s in d['spirit_list']]
        self.assertIn(dict(type_id=5004, count=150), souls)

    def test_counts_overflow_and_encoding_failures_are_atomic(self):
        role = self.b.profile()
        role.setdefault('souls', {})['5004'] = fruit.MAX_COUNT - 9
        self.b.save(role)
        self.reject()
        self.add(5001, fruit.MAX_COUNT - 9)
        self.reject(des_type=5, des_id=5001)
        with patch.object(self.b, 'inventory', side_effect=ValueError('injected serialization failure')):
            self.reject(des_id=5002)

    def test_replay_conflict_expiry_restart_and_account_isolation(self):
        self.request(item_count=3)
        packet, replies, before = self.packet, self.replies, self.b.profile()
        self.assertEqual(self.b.respond(packet, {'authenticated': True}), replies)
        self.reject(serial_num=self.serial, item_count=2)
        self.b.immortal_replies.clear()
        self.b.respond(packet, {'authenticated': True})
        self.assertEqual(self.b.profile(), before)
        self.b.close()
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.assertEqual(self.b.profile(), before)
        other = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None, account='fruit-other')
        try:
            self.assertFalse(any(i['type_id'] == 1246 for i in other.profile()['attachments']))
            self.assertEqual(other.profile().get('souls', {}).get('5004', 0), 0)
        finally:
            other.close()

    def test_direct_rejection_does_not_partially_consume(self):
        role = self.b.profile()
        before = copy.deepcopy(role)
        with self.assertRaises(f.Rejected):
            fruit.exchange(role, dict(item_type=1246, item_id=self.ident, item_count=2,
                                      des_type=10, des_id=5027), self.b.immortal_rules['xianyuan_fruit'])
        self.assertEqual(role, before)

    def test_forty_unowned_souls_compose_then_rate_changes(self):
        for n in (15, 15, 10):
            self.assertEqual(self.request(des_id=5001, item_count=n)[0], 21)
        self.assertEqual(self.b.profile()['souls']['5001'], 40)
        self.serial += 1
        replies = self.b.respond(encode(1083, dict(serial_num=self.serial, type_id=5001)), {'authenticated': True})
        self.assertTrue(any(m == 2998 and d['id'] == 26 for m, _, d in map(decode, replies)))
        self.assertEqual(self.b.profile()['souls']['5001'], 0)
        self.assertEqual(self.request(des_id=5001)[1]['attach_list'][1]['attach_count'], 10)

    def test_invalid_catalog_rejected_at_startup(self):
        for changes in (dict(mode='official'), dict(soul_targets=[4001]), dict(soul_targets=[5001,5001]),
                        dict(soul_targets=[True]), dict(realm_targets=[1246]), dict(soul_targets=[])):
            rules = copy.deepcopy(self.b.immortal_rules)
            rules['xianyuan_fruit'].update(changes)
            path = Path(self.tmp.name) / 'rules.json'
            path.write_text(json.dumps(rules))
            with self.assertRaises(f.Rejected):
                immortal.load_rules(path)


if __name__ == '__main__':
    unittest.main()
