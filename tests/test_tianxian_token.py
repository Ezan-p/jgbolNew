"""Tianxian token: real 1051 packets, inventory sync and disposable saves."""
import copy
from pathlib import Path
from unittest.mock import patch

from test_activity import ActivityCase
from network_redirect import summon
from network_redirect.backend import Backend
from network_redirect.protocol import decode, encode


class TianxianTokenTests(ActivityCase):
    def add(self, tid, count):
        role = self.b.profile()
        summon.add_item(role, tid, count)
        self.b.save(role)
        return next(i['id'] for i in role['attachments'] if i['type_id'] == tid)

    def count(self, tid):
        return sum(i['count'] for i in self.b.profile()['attachments'] if i['type_id'] == tid)

    def use(self, ident, **overrides):
        return dict(self.req(1051, **dict(dict(item_type=1363, item_id=ident,
            item_count=1, des_type=1, des_id=0), **overrides)))

    def test_single_batch_sync_and_home_shop_spend(self):
        ident = self.add(1363, 16)
        before = self.count(1361)
        for count in (1, 15):
            events = self.use(ident, item_count=count)
            self.assertNotIn(55, events)
            self.assertEqual(events[21], dict(result=1, type_id=1363, count=count,
                                              effect_value=5000 * count))
        self.assertEqual(self.count(1363), 0)
        self.assertEqual(self.count(1361), before + 80000)
        self.assertTrue(any(m == 1032 and d['unit_type'] == 5 and d['id'] == ident
                            and dict((a['type'], a['value']) for a in d['attr_list'])[102] == 0
                            for m, _, d in self.decoded))
        snapshot = [i for m, _, d in self.decoded if m == 1035 for i in d['attach_list']]
        self.assertEqual(next(i['count'] for i in snapshot if i['type_id'] == 1361), before + 80000)
        self.assertFalse(any(i['id'] == ident for i in snapshot))
        wood = self.count(1362)
        self.ok(self.req(1348, id=15, data=summon.lua(dict(shop_page=1, item_index=2, buy_count=1))))
        self.assertEqual(self.count(1361), before + 79900)
        self.assertEqual(self.count(1362), wood + 100)

    def test_invalid_requests_leave_save_unchanged(self):
        ident = self.add(1363, 20)
        other = self.add(1362, 10)
        for changes in (dict(item_count=0), dict(item_count=16), dict(item_count=65535),
                        dict(des_type=4), dict(des_id=999999), dict(item_id=other),
                        dict(item_id=99999999)):
            with self.subTest(changes=changes):
                before = self.b.profile()
                self.assertIn(55, self.use(ident, **changes))
                self.assertEqual(self.b.profile(), before)
        for field, value in (('is_lock', True), ('attach_type', 6), ('count', 0),
                             ('owner_id', 1), ('equip_pos', 1)):
            before = self.b.profile()
            role = copy.deepcopy(before)
            next(i for i in role['attachments'] if i['id'] == ident)[field] = value
            self.b.save(role)
            baseline = self.b.profile()
            with self.subTest(field=field):
                self.assertIn(55, self.use(ident))
                self.assertEqual(self.b.profile(), baseline)
            self.b.save(before)

    def test_replay_depletion_and_restart(self):
        ident = self.add(1363, 2)
        self.assertNotIn(55, self.use(ident))
        before = self.b.profile()
        self.assertEqual(self.b.respond(self.packet, self.state), self.replies)
        self.assertEqual(self.b.profile(), before)
        request = decode(self.packet)[2]
        request['des_id'] = before['role_id']
        replies = self.b.respond(encode(1051, request), self.state)
        self.assertTrue(any(m == 2998 and d['id'] == 55 for m, _, d in map(decode, replies)))
        self.assertEqual(self.b.profile(), before)
        self.assertIn(55, self.use(ident, item_count=2))
        self.assertEqual(self.b.profile(), before)
        self.b.close()
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.assertEqual(self.b.profile()['attachments'], before['attachments'])
        self.assertNotIn(55, self.use(ident, des_id=before['role_id']))
        after = self.b.profile()
        self.assertIn(55, self.use(ident))
        self.assertEqual(self.b.profile(), after)
        self.assertEqual(self.count(1361), 10000)

    def test_use_before_home_unlock_and_existing_coin_stack(self):
        coin = self.add(1361, 123)
        ident = self.add(1363, 1)
        role = self.b.profile()
        role['level'] = 1
        self.b.save(role)
        self.assertNotIn(55, self.use(ident))
        self.assertEqual(self.count(1361), 5123)
        self.assertTrue(any(m == 1032 and d['id'] == coin and d['unit_type'] == 5
                            and dict((a['type'], a['value']) for a in d['attr_list'])[102] == 5123
                            for m, _, d in self.decoded))

    def test_response_encoding_failure_rolls_back_exchange(self):
        ident = self.add(1363, 1)
        before = self.b.profile()
        with patch.object(self.b, 'inventory', side_effect=ValueError('encoding failed')):
            self.assertIn(55, self.use(ident))
        self.assertEqual(self.b.profile(), before)
