"""Original wire packets, economy, daily transitions and durable receipts."""
from recharge_helpers import funded_order
import json
from pathlib import Path
from unittest.mock import patch

from test_activity import ActivityCase

NOW = 1793150400  # 2026-10-28 12:00 UTC+8, safely inside the 28-day season
from network_redirect import activity_yuanshi as y, formation, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode


class YuanshiTests(ActivityCase):
    def setUp(self):
        super().setUp()
        self.clock.stop()
        self.clock = patch("network_redirect.backend.time.time", return_value=NOW)
        self.clock.start(); self.addCleanup(self.clock.stop)

    def call(self, flag=0, index=0):
        return self.req(1334, flag=flag, index=index)

    def data(self, events):
        self.ok(events)
        return next(d for e, d in events if e == 179)

    def ys(self):
        return self.b.profile()['activity']['yuanshi']

    def amount(self, tid):
        return sum(i['count'] for i in self.b.profile()['attachments'] if i['attach_type'] == 5 and i['type_id'] == tid)

    def charge(self, product=1, order=None):
        self.req(1111, event_id=251, data=funded_order(self.b, product, order or f'yuanshi-{self.serial}'))

    def test_bootstrap_and_original_contract(self):
        d = self.data(self.call())
        self.assertEqual((d['free_times'], d['cur_progress'], d['gift_list']), (1, 0, {}))
        self.assertEqual(len(d['gift_config']), 5)
        shop = self.data(self.call(3))['shop_config']
        self.assertEqual([i['attach_type'] for i in shop.values()], [1807, 1808])
        self.assertEqual([i['buy_times'] for i in shop.values()], [0, 1])
        packets = self.b.bootstrap()
        configs = [login_fields(v['data']) for m, _, v in map(decode, packets) if m == 2998 and v['id'] == 80]
        cfg = next(c[24]['yuanshi_info'] for c in configs if 24 in c)
        self.assertLess(cfg['begin_time'], NOW)
        self.assertGreater(cfg['end_time'], NOW)

    def test_free_offering_progress_claim_then_souls(self):
        r = self.b.profile(); summon.add_item(r, 1807, 10); self.b.save(r)
        for i in range(10):
            d = self.data(self.call(2)); self.assertEqual(d['cur_progress'], (i + 1) * 10)
        self.assertEqual(self.amount(1807), 1)
        self.assertFalse(self.ys()['claimed'])
        self.assertEqual(self.ys()['wish_days'], 1)
        self.data(self.call(2))
        c = next(c for c in self.b.profile()['corteges'] if c['type'] == 5046)
        self.assertEqual(c['level'], 120); self.assertGreater(c['hp'], 450)
        self.assertTrue(any(i.get('innate_owner_id') == c['id'] for i in self.b.profile()['attachments']))
        self.assertEqual(self.amount(1807), 1)  # claiming never consumes a prayer
        d = self.data(self.call(2))
        self.assertEqual(d['prize_list'][1]['object_type'], 10)
        self.assertEqual(self.b.profile()['souls']['5046'], 1)
        before = self.b.profile(); self.assertEqual(self.call(2)[0][0], 55)
        self.assertEqual(before, self.b.profile())

    def test_daily_misses_carry_stock_and_purchase(self):
        self.data(self.call())
        with patch('network_redirect.backend.time.time', return_value=NOW + 3 * 86400):
            d = self.data(self.call(3)); self.assertEqual(d['shop_config'][1]['buy_times'], 3)
            self.data(self.call(2)); self.assertEqual(self.ys()['free'], 0)
            gold = self.b.profile()['gold_coin']
            for left in (2, 1, 0):
                d = self.data(self.call(4, 1)); self.assertEqual(d['shop_config'][1]['buy_times'], left)
            self.assertEqual(gold - self.b.profile()['gold_coin'], 300)
            self.assertEqual(self.amount(1807), 3)
            self.assertEqual(self.call(4, 1)[0][0], 55)
        with patch('network_redirect.backend.time.time', return_value=NOW + 4 * 86400):
            self.assertEqual(self.data(self.call(3))['shop_config'][1]['buy_times'], 0)
            self.assertEqual(self.ys()['free'], 1)

    def test_ten_free_days_and_free_claim_with_no_items(self):
        start, _ = y.period(NOW, y.load_rules())
        # New isolated enrollment near the start of a season.
        for i in range(10):
            with patch('network_redirect.backend.time.time', return_value=start + 3600 + i * 86400):
                self.data(self.call(2))
        with patch('network_redirect.backend.time.time', return_value=start + 3600 + 9 * 86400):
            self.data(self.call(2)); self.assertTrue(self.ys()['claimed'])
        self.assertEqual(self.ys()['wishes'], 10)

    def test_recharge_five_tiers_one_per_day_and_accumulated_claims(self):
        start, _ = y.period(NOW, y.load_rules())
        for day in range(5):
            with patch('network_redirect.backend.time.time', return_value=start + 3600 + day * 86400):
                # 50 RMB in gold cards unlocks any next tier; never two on one day.
                self.charge(2); self.charge(2)
                d = self.data(self.call()); self.assertEqual(len(d['gift_list']), day + 1)
                self.assertEqual(list(d['gift_list'].values()), list(range(day + 1, 0, -1)))
        with patch('network_redirect.backend.time.time', return_value=start + 3600 + 4 * 86400):
            before = self.amount(1807); self.data(self.call(1, 1))
            self.assertEqual(self.amount(1807) - before, 5)
            self.assertEqual(self.call(1, 1)[0][0], 55)
            for i in range(2, 6): self.data(self.call(1, i))
            self.assertEqual(list(self.data(self.call())['gift_list'].values()), [0] * 5)

    def test_threshold_and_any_recharge_reopens_previous_gift(self):
        self.charge(1); self.data(self.call(1, 1))
        with patch('network_redirect.backend.time.time', return_value=NOW + 86400):
            self.charge(1); self.assertEqual(list(self.data(self.call())['gift_list'].values()), [1])
            self.charge(1); self.assertEqual(len(self.ys()['activated']), 1)
            self.charge(1); self.assertEqual(list(self.data(self.call())['gift_list'].values()), [1, 1])
            self.charge(2); self.assertEqual(len(self.ys()['activated']), 2)
        before = self.b.profile()
        with patch('network_redirect.backend.time.time', return_value=NOW + 86400):
            self.charge(1, 'unique-charge-order')
            after = self.b.profile(); self.charge(1, 'unique-charge-order')
            self.assertEqual(after, self.b.profile())

    def test_bag_shop_use_duplicate_and_selected_stack(self):
        self.data(self.call(4, 2)); self.assertEqual(self.call(4, 2)[0][0], 55)
        r = self.b.profile(); item = next(i for i in r['attachments'] if i['type_id'] == 1808)
        req = dict(item_type=1808, item_id=item['id'], item_count=1, des_type=1, des_id=r['role_id'])
        self.ok(self.req(1051, **req)); self.assertEqual(self.amount(1808), 0)
        self.assertEqual(next(c for c in self.b.profile()['corteges'] if c['type'] == 5046)['level'], 120)
        r = self.b.profile(); summon.add_item(r, 1808, 2); self.b.save(r)
        item = next(i for i in r['attachments'] if i['type_id'] == 1808)
        req.update(item_id=item['id'], item_count=2)
        self.ok(self.req(1051, **req)); self.assertEqual(self.b.profile()['souls']['5046'], 80)
        self.assertEqual(self.req(1051, **req)[0][0], 55)

    def test_invalid_input_lock_balance_and_atomicity(self):
        self.data(self.call(2))
        for flag, index in [(5, 0), (0, 1), (2, 1), (3, 1), (4, 0), (4, 3), (1, 6), (1, 1)]:
            before = self.b.profile(); self.assertEqual(self.call(flag, index)[0][0], 55)
            self.assertEqual(before, self.b.profile())
        r = self.b.profile(); summon.add_item(r, 1807, 1)
        next(i for i in r['attachments'] if i['type_id'] == 1807)['is_lock'] = True
        r['gold_coin'] = 0; self.b.save(r); before = self.b.profile()
        self.assertEqual(self.call(2)[0][0], 55); self.assertEqual(self.call(4, 2)[0][0], 55)
        self.assertEqual(before, self.b.profile())

    def test_replay_restart_and_encoding_failure(self):
        self.data(self.call(2)); before = self.b.profile()
        self.assertEqual(self.b.respond(self.packet, self.state_for_wire()), self.replies)
        self.assertEqual(before, self.b.profile())
        forged = encode(1334, dict(serial_num=self.serial, flag=4, index=2))
        self.assertEqual(decode(self.b.respond(forged, self.state_for_wire())[0])[2]['id'], 55)
        with patch('network_redirect.backend.activity.attributes', side_effect=ValueError('encoding failure')):
            self.assertEqual(self.call(4, 2)[0][0], 55)
        self.assertEqual(before, self.b.profile())
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.assertEqual(before, self.b.profile()); self.assertEqual(self.call(2)[0][0], 55)

    def state_for_wire(self):
        return {'authenticated': True}

    def test_clock_rollback_season_reset_and_disabled(self):
        self.data(self.call(2)); before = self.b.profile()
        with patch('network_redirect.backend.time.time', return_value=NOW - 1):
            self.assertEqual(self.call(2)[0][0], 55)
        self.assertEqual(before, self.b.profile())
        end = self.ys()['end']
        with patch('network_redirect.backend.time.time', return_value=end):
            d = self.data(self.call()); self.assertEqual((d['cur_progress'], d['free_times']), (0, 1))
        cfg = y.load_rules(); cfg['enabled'] = False
        with patch.object(y, 'load_rules', return_value=cfg):
            self.assertEqual(y.client_config(NOW)['end_time'], 0)
            self.assertEqual(self.call()[0][0], 55)

    def test_bad_configuration(self):
        for key, value in [('mode', 'official'), ('daily_free', 0), ('progress_per_wish', 101),
                           ('activation_rmb', [0, 30, 50]), ('gifts', []), ('enabled', 1)]:
            cfg = y.load_rules(); cfg[key] = value
            p = Path(self.tmp.name) / 'bad.json'; p.write_text(json.dumps(cfg))
            with self.assertRaises(formation.Rejected): y.load_rules(p)

    def test_disabled_does_not_enroll_on_charge_and_existing_bag_still_works(self):
        cfg = y.load_rules(); cfg['enabled'] = False
        r = self.b.profile(); summon.add_item(r, 1808, 1); self.b.save(r)
        item = next(i for i in r['attachments'] if i['type_id'] == 1808)
        with patch.object(y, 'load_rules', return_value=cfg):
            self.charge(1)
            self.assertNotIn('yuanshi', self.b.profile()['activity'])
            self.ok(self.req(1051, item_type=1808, item_id=item['id'], item_count=1, des_type=1, des_id=0))
        self.assertTrue(any(c['type'] == 5046 for c in self.b.profile()['corteges']))

    def test_bag_lock_selected_stack_and_invalid_target(self):
        r = self.b.profile(); summon.add_item(r, 1808, 1)
        first = next(i for i in r['attachments'] if i['type_id'] == 1808)
        second = dict(first, id=formation.new_id(r), count=2, is_lock=True)
        r['attachments'].append(second); self.b.save(r)
        req = dict(item_type=1808, item_id=second['id'], item_count=1, des_type=1, des_id=0)
        before = self.b.profile(); self.assertEqual(self.req(1051, **req)[0][0], 55)
        self.assertEqual(before, self.b.profile())
        r = self.b.profile(); next(i for i in r['attachments'] if i['id'] == second['id'])['is_lock'] = False
        self.b.save(r); before = self.b.profile()
        self.assertEqual(self.req(1051, **dict(req, des_id=999))[0][0], 55)
        self.assertEqual(before, self.b.profile())
        self.ok(self.req(1051, **req))
        counts = {i['id']: i['count'] for i in self.b.profile()['attachments'] if i['type_id'] == 1808}
        self.assertEqual(counts, {first['id']: 1, second['id']: 1})
