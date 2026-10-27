"""Real wire requests, disposable saves: reward -> use -> spend -> reload."""
import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from network_redirect import summon, qiankun_bags, guild
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode

NOW = 1793073600


class ConsumableTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        clock = patch('network_redirect.backend.time.time', return_value=NOW)
        clock.start()
        self.addCleanup(clock.stop)
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.addCleanup(lambda: self.b.close())
        self.serial = 10000
        r = self.b.profile()
        r.update(level=80, gold_coin=100000, strength=0, vip_level=1)
        self.b.save(r)

    def req(self, mid, **data):
        self.serial += 1
        self.packet = encode(mid, dict(serial_num=self.serial, **data))
        self.replies = self.b.respond(self.packet, {'authenticated': True})
        self.rows = [decode(p) for p in self.replies]
        self.assertEqual(self.rows[-1][0], 1106)
        self.assertEqual(self.rows[-1][2]['req_serial_num'], self.serial)
        self.events = {d['id']: login_fields(d['data']) for m, _, d in self.rows if m == 2998}
        return self.events

    def add(self, tid, count=1):
        r = self.b.profile()
        summon.add_item(r, tid, count)
        self.b.save(r)
        return next(i['id'] for i in r['attachments'] if i['type_id'] == tid)

    def use(self, tid, ident, **overrides):
        return self.req(1051, **dict(dict(item_type=tid, item_id=ident, item_count=1,
                                        des_type=1, des_id=0), **overrides))

    def join(self):
        self.req(1301, id=1, data=summon.lua(dict(union_name='道具回归仙盟')))
        self.assertNotIn(55, self.events)

    def attrs(self):
        return {a['type']: a['value'] for m, _, d in self.rows if m == 1032
                and d['unit_type'] == 1 for a in d['attr_list']}

    def test_small_bun_reward_use_and_journey_spend(self):
        ident = self.add(1032)
        with patch.object(qiankun_bags, 'draw', return_value=[5, 1020, 1, 1]):
            self.use(1032, ident)
        r = self.b.profile()
        bun = next(i for i in r['attachments'] if i['type_id'] == 1020)
        self.use(1020, bun['id'])
        self.assertEqual(self.events[21]['effect_value'], 5)
        self.assertEqual(self.attrs()[101], 5)
        self.assertFalse(any(i['id'] == bun['id'] for i in self.b.profile()['attachments']))
        self.assertTrue(any(m == 1032 and d['id'] == bun['id'] and d['unit_type'] == 5
                            for m, _, d in self.rows))
        self.req(1026, fight_type=1, des_type=1, des_id=101)
        self.assertNotIn(55, self.events)
        self.assertEqual(self.b.profile()['strength'], 4)

    def test_small_bun_preserves_daily_quota_and_overcap(self):
        ident = self.add(1020, 11)
        r = self.b.profile()
        r.update(strength=60, strength_item_count=r['strength_item_limit'], strength_item_time=NOW-10)
        self.b.save(r)
        before = self.b.profile()
        for _ in range(11):
            self.use(1020, ident)
            self.assertNotIn(55, self.events)
        after = self.b.profile()
        self.assertEqual(after['strength'], 115)
        for key in ('strength_item_count', 'strength_item_time', 'energy', 'energy_item_count'):
            self.assertEqual(after[key], before[key])
        self.assertEqual(after['achievements']['daily'].get('447'), before['achievements']['daily'].get('447'))

    def test_small_bun_cannot_be_bought_with_1058(self):
        before = self.b.profile()
        self.req(1058, type_id=1020)
        self.assertIn(55, self.events)
        self.assertEqual(self.b.profile(), before)

    def test_contribution_reward_use_and_store_spend(self):
        self.join()
        ident = self.add(1121)
        self.use(1121, ident)
        r = self.b.profile()
        token = next(i for i in r['attachments'] if i['type_id'] == 1029)
        before = (r['union_contrib'], r['cur_union_contrib'])
        self.use(1029, token['id'])
        self.assertEqual(self.events[21], dict(result=1, type_id=1029, count=1, effect_value=100))
        self.assertEqual((self.attrs()[146], self.attrs()[148]), (before[0]+100, before[1]+100))
        r = self.b.profile()
        member = r['guild']['unions'][str(r['union_id'])]['members'][str(int(r['role_id']))]
        self.assertEqual((member['totalcontrib'], member['contrib']), (before[0]+100, before[1]+100))
        self.req(1301, id=38, data='{}')
        store = next(login_fields(d['data']) for m, _, d in self.rows if m == 1301 and d['id'] == 38)
        offer = next(v for v in store['item_list'].values() if v['cost_contrib'] <= 100)
        self.req(1301, id=40, data=summon.lua(dict(item_id=offer['id'], buy_count=1)))
        self.assertNotIn(55, self.events)
        r = self.b.profile()
        self.assertEqual(r['union_contrib'], before[0]+100)
        self.assertEqual(r['cur_union_contrib'], before[1]+100-offer['cost_contrib'])

    def test_contribution_batch_fixed_value_and_no_side_rewards(self):
        self.join()
        ident = self.add(1029, 16)
        r = self.b.profile()
        r['guild']['feast_buff_end'] = NOW+3600
        r.update(contrib_plus_rate=5, train_tree_rate=5)
        self.b.save(r)
        before = self.b.profile()
        self.use(1029, ident, item_count=15, des_id=r['role_id'])
        after = self.b.profile()
        self.assertEqual(self.events[21]['effect_value'], 1500)
        self.assertEqual(after['cur_union_contrib']-before['cur_union_contrib'], 1500)
        self.assertEqual(next(i['count'] for i in after['attachments'] if i['id'] == ident), 1)
        for k in ('contrib_plus_rate', 'train_tree_rate', 'strength', 'energy', 'gold_coin'):
            self.assertEqual(after[k], before[k])
        for k in ('money', 'popularity'):
            key = str(after['union_id'])
            self.assertEqual(after['guild']['unions'][key][k], before['guild']['unions'][key][k])
        self.use(1029, ident)
        self.assertEqual(self.events[21]['effect_value'], 100)

    def test_contribution_requires_real_membership(self):
        ident = self.add(1029)
        for broken in ('none', 'missing_union', 'missing_member'):
            with self.subTest(broken=broken):
                r = self.b.profile()
                if broken == 'missing_union':
                    r['union_id'] = 999999
                elif broken == 'missing_member':
                    guild.prepare(r, NOW, self.b.guild_rules)
                    r['union_id'] = 1
                    r['guild']['unions']['1']['members'].pop(str(int(r['role_id'])), None)
                self.b.save(r)
                before = self.b.profile()
                self.use(1029, ident)
                self.assertIn(55, self.events)
                self.assertEqual(self.b.profile(), before)

    def test_invalid_targets_counts_and_inventory_are_atomic(self):
        self.join()
        for tid in (1020, 1029):
            ident = self.add(tid, 2)
            other = self.add(1001)
            bad = [dict(item_count=0), dict(item_count=65535), dict(item_count=16),
                   dict(item_count=3), dict(des_type=4), dict(des_id=99999),
                   dict(item_id=99999999), dict(item_id=other)]
            if tid == 1020:
                bad.append(dict(item_count=2))
            for overrides in bad:
                with self.subTest(tid=tid, overrides=overrides):
                    before = self.b.profile()
                    self.use(tid, ident, **overrides)
                    self.assertIn(55, self.events)
                    self.assertEqual(self.b.profile(), before)
            for field, value in (('is_lock', True), ('attach_type', 6), ('count', 0)):
                with self.subTest(tid=tid, field=field):
                    before = self.b.profile()
                    r = copy.deepcopy(before)
                    next(i for i in r['attachments'] if i['id'] == ident)[field] = value
                    self.b.save(r)
                    baseline = self.b.profile()
                    self.use(tid, ident)
                    self.assertIn(55, self.events)
                    self.assertEqual(self.b.profile(), baseline)
                    self.b.save(before)

    def test_retransmission_stale_serial_and_depleted_stack(self):
        self.join()
        for tid in (1020, 1029):
            with self.subTest(tid=tid):
                ident = self.add(tid)
                self.use(tid, ident)
                self.assertNotIn(55, self.events)
                before = self.b.profile()
                self.assertEqual(self.b.respond(self.packet, {'authenticated': True}), self.replies)
                self.assertEqual(self.b.profile(), before)
                _, _, request = decode(self.packet)
                request['des_id'] = before['role_id']
                rejected = self.b.respond(encode(1051, request), {'authenticated': True})
                self.assertTrue(any(m == 2998 and d['id'] == 55 for m, _, d in map(decode, rejected)))
                self.assertEqual(self.b.profile(), before)
                self.use(tid, ident)
                self.assertIn(55, self.events)
                self.assertEqual(self.b.profile(), before)

    def test_effect_and_inventory_survive_database_reopen(self):
        self.join()
        for tid in (1020, 1029):
            self.use(tid, self.add(tid, 2))
            self.assertNotIn(55, self.events)
        before = self.b.profile()
        self.b.close()
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        after = self.b.profile()
        for key in ('strength', 'union_contrib', 'cur_union_contrib', 'attachments'):
            self.assertEqual(after[key], before[key])
        for tid in (1020, 1029):
            self.use(tid, next(i['id'] for i in after['attachments'] if i['type_id'] == tid))
            self.assertNotIn(55, self.events)
        self.assertEqual(self.b.profile()['strength'], 10)
        self.assertEqual(self.b.profile()['cur_union_contrib'], 200)

    def test_regular_resource_callbacks_and_quotas_remain_valid(self):
        for tid, key in ((1022, 'strength'), (1023, 'energy')):
            before = self.b.profile()
            self.use(tid, self.add(tid), item_count=0)
            self.assertEqual(self.events[21]['effect_value'], 10)
            self.assertEqual(self.b.profile()[key], before[key]+10)
            self.assertEqual(self.b.profile()[key+'_item_count'], before[key+'_item_count']+1)


if __name__ == '__main__':
    unittest.main()
