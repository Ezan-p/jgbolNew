"""Daily illusion offers, legacy migration and transactional native purchases."""
import copy
import json
from pathlib import Path
from unittest.mock import patch

from test_activity_taixu import TaixuCase
from test_activity import NOW
from network_redirect import activity, activity_undergo as u, summon
from network_redirect.backend import Backend, login_fields


class TaixuShopTests(TaixuCase):
    def query(self):
        self.ok(self.call(3))
        return next(login_fields(d['data']) for mid, _, d in self.decoded if mid == 1349)

    def balance(self, tid):
        return sum(i['count'] for i in self.b.profile()['attachments']
                   if i['attach_type'] == 5 and i['type_id'] == tid)

    def fund(self):
        role = self.b.profile(); summon.add_item(role, 1366, 1000000); self.b.save(role)

    def test_six_unique_stable_offers_restart_and_all_pool_reachable(self):
        first = self.query(); self.assertEqual(len(first), 6)
        self.assertEqual(len({p['attach_type'] for p in first.values()}), 6)
        for p in first.values():
            self.assertEqual(p['buy_times'], 3 if p['crystals'] >= 1000 else 5)
        self.assertEqual(self.query(), first)
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.assertEqual(self.query(), first)
        seen = set(); combinations = set()
        role = self.b.profile()
        for offset in range(90):
            s = u.state(role, NOW + offset * 86400, self.b.activity_rules)
            ids = tuple(p['reward'][1] for p in s['shop'])
            self.assertEqual(len(set(ids)), 6); seen.update(ids); combinations.add(ids)
        self.assertEqual(seen, {p['reward'][1] for p in self.b.activity_rules['undergo_shop']})
        self.assertGreater(len(combinations), 80)

    def test_every_product_batch_grants_exact_bundle_and_packet_replay(self):
        self.query(); self.fund()
        for product in self.b.activity_rules['undergo_shop']:
            with self.subTest(item=product['reward'][1]):
                role = self.b.profile(); s = role['activity']['undergo']
                s['shop'][0] = copy.deepcopy(product); s['purchases'] = {}; self.b.save(role)
                tid = product['reward'][1]; before = self.balance(tid); currency = self.balance(1366)
                self.ok(self.call(5, dict(index=1, count=3, shop_token=s['shop_token'])))
                self.assertEqual(self.balance(tid)-before, product['reward'][2]*3)
                self.assertEqual(currency-self.balance(1366), product['cost']*3)
                result = next(login_fields(d['data']) for mid, _, d in self.decoded if mid == 1349)
                self.assertEqual(result['attach_list'][1]['buy_times'], product['limit']-3)
                after = self.b.profile()
                self.assertEqual(self.b.respond(self.packet, self.state), self.replies)
                self.assertEqual(self.b.profile(), after)
                remaining = product['limit']-3
                if remaining:
                    self.ok(self.call(5, dict(index=1, count=remaining)))
                after = self.b.profile()
                self.assertEqual(self.call(5, dict(index=1, count=1))[0][0], 55)
                self.assertEqual(self.b.profile(), after)

    def test_midnight_stale_views_cannot_buy_replacement(self):
        first = self.query(); self.fund(); old = self.b.profile()['activity']['undergo']['shop_token']
        midnight = ((NOW + 8*3600)//86400 + 1)*86400 - 8*3600
        with patch('network_redirect.backend.time.time', return_value=midnight-1):
            self.ok(self.call(5, dict(index=1, count=first[1]['buy_times'], shop_token=old)))
            self.assertEqual(self.query()[1]['buy_times'], 0)
        before = self.b.profile()
        with patch('network_redirect.backend.time.time', return_value=midnight):
            for data in (dict(index=1, count=1), dict(index=1, count=1, shop_token=old)):
                self.assertEqual(self.call(5, data)[0][0], 55)
                self.assertEqual(self.b.profile()['attachments'], before['attachments'])
                self.assertEqual(self.b.profile()['activity']['undergo'], before['activity']['undergo'])
            fresh = self.query()
            for p in fresh.values():
                self.assertEqual(p['buy_times'], 3 if p['crystals'] >= 1000 else 5)
            self.assertNotEqual(fresh[1]['shop_token'], old)
            before = self.b.profile()
            self.assertEqual(self.call(5, dict(index=1, shop_token=old))[0][0], 55)
            self.assertEqual(self.b.profile(), before)
            self.ok(self.call(5, dict(index=1, count=1, shop_token=fresh[1]['shop_token'])))

    def test_legacy_usage_migrates_by_item_without_refunds_or_extra_limits(self):
        role = self.b.profile(); s = u.state(role, NOW, self.b.activity_rules)
        for key in list(s):
            if key.startswith('shop'): del s[key]
        s['purchases'] = {'1':20, '2':2, '3':7, '4':3}
        old_items = copy.deepcopy(role['attachments']); self.b.save(role)
        self.query(); migrated = self.b.profile()
        self.assertEqual(migrated['attachments'], old_items)
        self.assertEqual(migrated['activity']['undergo']['purchases'],
                         {'1001':20, '1343':2, '1034':7, '1024':3})
        s = migrated['activity']['undergo']
        s['shop'] = copy.deepcopy(self.b.activity_rules['undergo_shop'][:6])
        counts = {p['attach_type']:p['buy_times'] for p in u.shop(s, self.b.activity_rules)}
        self.assertEqual([counts[i] for i in (1001,1343,1024,1034)], [0,3,0,0])

    def test_balance_update_preserves_daily_goods_order_and_used_counts(self):
        self.query(); self.fund()
        role = self.b.profile(); s = role['activity']['undergo']
        s['shop'] = copy.deepcopy(self.b.activity_rules['undergo_shop'][:6])
        for row in s['shop']: row['limit'] = 5
        s.update(shop_revision='taixu-shop-2026-10-28-v1', shop_token='old-token',
                 shop_view_token='old-token', purchases={'1024':4, '1001':2})
        old_ids = [p['reward'][1] for p in s['shop']]
        self.b.save(role); before = copy.deepcopy(role['attachments'])
        rows = self.query(); current = self.b.profile()['activity']['undergo']
        self.assertEqual([p['reward'][1] for p in current['shop']], old_ids)
        self.assertEqual(current['purchases'], {'1024':4, '1001':2})
        self.assertEqual(self.b.profile()['attachments'], before)
        self.assertEqual(rows[1]['buy_times'], 3)
        self.assertEqual(rows[3]['buy_times'], 0)
        self.assertNotEqual(rows[1]['shop_token'], 'old-token')
        before = self.b.profile()
        self.assertEqual(self.call(5, dict(index=3))[0][0], 55)
        self.assertEqual(self.call(5, dict(index=1, shop_token='old-token'))[0][0], 55)
        self.assertEqual(self.b.profile(), before)
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.assertEqual(self.query(), rows)

    def test_bad_parameters_insufficient_funds_and_encoding_failure_are_atomic(self):
        self.query(); before = self.b.profile()
        self.assertEqual(self.call(5, dict(index=1, count=1))[0][0], 55)
        self.assertEqual(self.b.profile(), before)
        self.fund(); before = self.b.profile()
        for data in (dict(index=0), dict(index=7), dict(index=True), dict(index=1, count=0),
                     dict(index=1, count=-1), dict(index=1, count=1.5), dict(index=1, count=True),
                     dict(index=1, count=6), dict(index=1, shop_token='forged')):
            self.assertEqual(self.call(5, data)[0][0], 55); self.assertEqual(self.b.profile(), before)
        with patch('network_redirect.activity_undergo.encode', side_effect=ValueError('bad response')):
            self.assertEqual(self.call(5, dict(index=1, count=1))[0][0], 55)
        self.assertEqual(self.b.profile(), before)

    def test_config_rejects_missing_pool_duplicate_wrong_quantity_and_wrong_limits(self):
        original = self.b.activity_rules
        for kind in ('missing', 'duplicate', 'quantity', 'limit', 'high_limit', 'count', 'price'):
            r = copy.deepcopy(original)
            if kind == 'missing': r['undergo_shop'].pop()
            if kind == 'duplicate': r['undergo_shop'][1] = copy.deepcopy(r['undergo_shop'][0])
            if kind == 'quantity': r['undergo_shop'][0]['reward'][2] = 10
            if kind == 'limit': r['undergo_shop'][0]['limit'] = 3
            if kind == 'high_limit': r['undergo_shop'][2]['limit'] = 5
            if kind == 'count': r['undergo_shop_daily_count'] = 5
            if kind == 'price': r['undergo_shop'][0]['cost'] = 0
            path = Path(self.tmp.name)/'invalid-rules.json'; path.write_text(json.dumps(r))
            with self.subTest(kind=kind), self.assertRaises(ValueError): activity.load_rules(path)
