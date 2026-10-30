"""Exercise original market packets against isolated persistent accounts."""
import copy
from datetime import datetime, timezone, timedelta
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from network_redirect.backend import Backend, login_fields
from network_redirect import market
from network_redirect.protocol import encode, decode


class MarketTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.backend = Backend(Path(self.tmp.name), 18770, lambda *a, **kw: None)
        self.addCleanup(lambda: self.backend.close())
        self.rules = self.backend.market_rules
        self.now = int(datetime(2026, 10, 27, 12, 1, tzinfo=timezone(timedelta(hours=8))).timestamp())
        self.start = self.now - 60
        self.state = dict(authenticated=True, market_sale_time=self.start,
                          market_rotation_start=market.rotation_start(self.now, self.rules))
        self.serial = 100000
        role = self.backend.profile()
        role.update(gold_coin=10000, silver_coin=10000)
        self.backend.save(role)

    def request(self, mid=1057, **data):
        self.serial += 1
        self.packet = encode(mid, dict(serial_num=self.serial, **data))
        with patch('network_redirect.backend.time.time', return_value=self.now):
            self.replies = self.backend.respond(self.packet, self.state)
        rows = [decode(p) for p in self.replies]
        if mid != 1242:
            self.assertEqual(rows[-1][0], 1106)
            self.assertEqual(rows[-1][2]['req_serial_num'], self.serial)
        return [(p[2]['id'], login_fields(p[2]['data'])) for p in rows if p[0] == 2998]

    def buy(self, **changes):
        data = dict(first_send=0, page_id=2, index=1, type_id=1032, count=1)
        data.update(changes)
        return self.request(**data)[0][1]

    def count(self, type_id):
        return sum(i['count'] for i in self.backend.profile()['attachments']
                   if i['attach_type'] == 5 and i['type_id'] == type_id)

    def test_bootstrap_and_query_have_original_permanent_catalog(self):
        with patch('network_redirect.backend.time.time', return_value=self.now):
            packet = self.backend.bootstrap()[0]
        cfg = login_fields(decode(packet)[2]['data'])
        self.assertEqual(cfg[23], self.backend.formation_rules['equipment_advance'])
        goods = cfg[10]
        self.assertEqual(len(goods['cheap_item_list']), 8)
        self.assertEqual(len(goods['rich_item_list']), 15)  # forge tokens and regular-price buns
        self.assertNotIn(9137, goods['rich_item_list'])
        self.assertEqual(len(goods['limit_item_list']), 0)
        for raw in market.CATALOG:
            if raw['begin_time'] != '0':
                continue
            row = goods[market.LISTS[int(raw['page_id'])]][int(raw['index'])]
            self.assertEqual((row['object_type'], row['type_id'], row['count']), tuple([int(raw['type_id'].split('|')[0]), int(raw['type_id'].split('|')[1]), 20 if int(raw['index']) == 8 else int(raw['type_id'].split('|')[2])]))
            for key in ('buy_price', 'vip_level', 'order'):
                self.assertEqual(row[key], int(raw[key]))
            self.assertGreater(row['origin_price'], 0)
        event, query = self.request(first_send=1, page_id=1)[0]
        self.assertEqual(event, 24)
        self.assertEqual(query['first_send'], 1)
        self.assertEqual(query['rich_item_list'], goods['rich_item_list'])

    def test_batch_purchase_and_inventory_wire_order(self):
        before = self.count(1032)
        result = self.buy(count=3)
        self.assertEqual(result['result'], 1)
        self.assertEqual(self.count(1032), before + 3)
        self.assertEqual(self.backend.profile()['gold_coin'], 9850)
        ids = [decode(p)[0] for p in self.replies]
        self.assertLess(ids.index(1035), ids.index(2998))
        self.assertLess(ids.index(1032), ids.index(2998))

    def test_cheap_limit_and_next_day_refresh(self):
        self.assertEqual(self.buy(page_id=1, index=10)['result'], 1)
        self.assertEqual(self.buy(page_id=1, index=10)['result'], 7)
        goods = self.request(first_send=1)[0][1]
        self.assertEqual(goods['cheap_item_list'][10]['buy_limit_times'], 0)
        self.now += 86400
        self.assertEqual(self.buy(page_id=1, index=10)['result'], 1)

    def test_month_card_adds_only_one_discounted_soul_fate_pill(self):
        role = self.backend.profile()
        role['month_card_time'] = self.now + 86400 * 30
        self.backend.save(role)
        catalog = self.request(first_send=1, page_id=1)[0][1]
        self.assertEqual(catalog['cheap_item_list'][15]['buy_limit_times'], 2)
        self.assertEqual(catalog['cheap_item_list'][15]['buy_price'], 100)
        for index, row in catalog['cheap_item_list'].items():
            if index != 15:
                self.assertEqual(row['buy_limit_times'], 10 if row['type_id'] == 1022 else 1)
        before = self.count(1024)
        for remaining in (1, 0):
            self.assertEqual(self.buy(page_id=1, index=15, type_id=1024)['result'], 1)
            catalog = self.request(first_send=1, page_id=1)[0][1]
            self.assertEqual(catalog['cheap_item_list'][15]['buy_limit_times'], remaining)
        self.assertEqual(self.count(1024), before + 2)
        self.assertEqual(self.backend.profile()['gold_coin'], 9800)
        saved = self.backend.profile()
        self.assertEqual(self.buy(page_id=1, index=15, type_id=1024)['result'], 7)
        self.assertEqual(self.backend.profile(), saved)
        self.assertEqual(self.buy(page_id=1, index=10)['result'], 1)
        self.assertEqual(self.buy(page_id=1, index=10)['result'], 7)
        # The regular-price listing keeps its existing unrestricted batch policy.
        self.assertEqual(self.buy(page_id=2, index=16, type_id=1024, count=2)['result'], 1)

    def test_month_card_expiry_and_renewal_preserve_used_market_quota(self):
        role = self.backend.profile()
        role['month_card_time'] = self.now + 1
        self.backend.save(role)
        self.assertEqual(self.buy(page_id=1, index=15, type_id=1024)['result'], 1)
        self.now += 1
        catalog = self.request(first_send=1, page_id=1)[0][1]
        self.assertEqual(catalog['cheap_item_list'][15]['buy_limit_times'], 0)
        saved = self.backend.profile()
        self.assertEqual(self.buy(page_id=1, index=15, type_id=1024)['result'], 7)
        self.assertEqual(self.backend.profile(), saved)
        role = self.backend.profile()
        role['month_card_time'] = self.now + 86400 * 30
        self.backend.save(role)
        catalog = self.request(first_send=1, page_id=1)[0][1]
        self.assertEqual(catalog['cheap_item_list'][15]['buy_limit_times'], 1)
        self.assertEqual(self.buy(page_id=1, index=15, type_id=1024)['result'], 1)
        role = self.backend.profile()
        role['month_card_time'] += 86400 * 30
        self.backend.save(role)
        self.backend.close()
        self.backend = Backend(Path(self.tmp.name), 18770, lambda *a, **kw: None)
        catalog = self.request(first_send=1, page_id=1)[0][1]
        self.assertEqual(catalog['cheap_item_list'][15]['buy_limit_times'], 0)
        saved = self.backend.profile()
        self.assertEqual(self.buy(page_id=1, index=15, type_id=1024)['result'], 7)
        self.assertEqual(self.backend.profile(), saved)
        self.now += 86400
        catalog = self.request(first_send=1, page_id=1)[0][1]
        self.assertEqual(catalog['cheap_item_list'][15]['buy_limit_times'], 2)

    def test_discount_buns_price_quota_replay_restart_and_midnight(self):
        goods = self.request(first_send=1, page_id=1)[0][1]
        index, bun = next((i, row) for i, row in goods['cheap_item_list'].items()
                          if row['type_id'] == 1022)
        self.assertEqual((bun['count'], bun['origin_price'], bun['buy_price'],
                          bun['buy_limit_times'], bun['vip_level']), (1, 20, 5, 10, 0))
        stock, gold = self.count(1022), self.backend.profile()['gold_coin']
        for used in range(1, 11):
            self.assertEqual(self.buy(page_id=1, index=index, type_id=1022)['result'], 1)
            self.assertEqual(self.backend.respond(self.packet, self.state), self.replies)
            self.assertEqual(self.count(1022), stock + used)
            self.assertEqual(self.backend.profile()['gold_coin'], gold - 5 * used)
        saved = self.backend.profile()
        self.assertEqual(self.buy(page_id=1, index=index, type_id=1022)['result'], 7)
        self.assertEqual(self.backend.profile(), saved)
        self.backend.close()
        self.backend = Backend(Path(self.tmp.name), 18770, lambda *a, **kw: None)
        self.assertEqual(self.request(first_send=1)[0][1]['cheap_item_list'][index]['buy_limit_times'], 0)
        midnight = market.day_start(self.now, self.rules) + 86400
        self.now = midnight - 1
        self.assertEqual(self.buy(page_id=1, index=index, type_id=1022)['result'], 7)
        self.now = midnight
        self.assertEqual(self.request(first_send=1)[0][1]['cheap_item_list'][index]['buy_limit_times'], 10)
        self.assertEqual(self.buy(page_id=1, index=index, type_id=1022)['result'], 1)

    def test_discount_buns_failed_purchase_keeps_balance_and_quota(self):
        role = self.backend.profile(); role['gold_coin'] = 4; self.backend.save(role)
        saved = self.backend.profile()
        self.assertEqual(self.buy(page_id=1, index=24, type_id=1022)['result'], 6)
        self.assertEqual(self.backend.profile(), saved)
        self.assertEqual(self.request(first_send=1)[0][1]['cheap_item_list'][24]['buy_limit_times'], 10)

    def test_regular_buns_batch_price_and_independent_discount_quota(self):
        goods = self.request(first_send=1, page_id=2)[0][1]
        row = goods['rich_item_list'][25]
        self.assertEqual((row['type_id'], row['count'], row['buy_price'], row['money_type'],
                          row['vip_level'], row['is_day_limit']), (1022, 1, 20, 11, 0, 0))
        before, gold = self.count(1022), self.backend.profile()['gold_coin']
        result = self.buy(page_id=2, index=25, type_id=1022, count=12)
        self.assertEqual(result['result'], 1)
        self.assertEqual(self.count(1022), before + 12)
        self.assertEqual(self.backend.profile()['gold_coin'], gold - 240)
        saved = self.backend.profile()
        self.assertEqual(self.backend.respond(self.packet, self.state), self.replies)
        self.assertEqual(self.backend.profile(), saved)
        self.assertEqual(self.request(first_send=1)[0][1]['cheap_item_list'][24]['buy_limit_times'], 10)
        self.assertEqual(self.buy(page_id=1, index=24, type_id=1022)['result'], 1)
        self.assertEqual(self.buy(page_id=2, index=25, type_id=1022, count=3)['result'], 1)
        self.assertEqual(self.count(1022), before + 16)
        self.assertEqual(self.backend.profile()['gold_coin'], gold - 305)
        self.assertEqual(self.request(first_send=1)[0][1]['cheap_item_list'][24]['buy_limit_times'], 9)
        role = self.backend.profile(); role['gold_coin'] = 19; self.backend.save(role)
        saved = self.backend.profile()
        self.assertEqual(self.buy(page_id=2, index=25, type_id=1022)['result'], 6)
        self.assertEqual(self.backend.profile(), saved)

    def test_bundle_grants_twenty_and_preserves_vip_gate(self):
        self.assertEqual(self.buy(page_id=1, index=8, type_id=1001)['result'], 5)
        role = self.backend.profile()
        role['vip_level'] = 1
        self.backend.save(role)
        before = self.count(1001)
        self.assertEqual(self.buy(page_id=1, index=8, type_id=1001)['result'], 1)
        self.assertEqual(self.count(1001), before + 20)
        self.assertEqual(self.backend.profile()['gold_coin'], 9995)

    def test_rejected_requests_never_change_save(self):
        before = self.backend.profile()
        for changes in (dict(count=0), dict(count=1000), dict(index=255), dict(type_id=1006),
                        dict(page_id=3), dict(page_id=4), dict(first_send=2),
                        dict(page_id=1, index=10, count=2), dict(count=999)):
            with self.subTest(changes=changes):
                self.assertNotEqual(self.buy(**changes)['result'], 1)
                self.assertEqual(self.backend.profile(), before)

    def test_exact_balance_and_insufficient_balance(self):
        role = self.backend.profile()
        role['gold_coin'] = 50
        self.backend.save(role)
        self.assertEqual(self.buy()['result'], 1)
        before = self.backend.profile()
        self.assertEqual(self.buy()['result'], 6)
        self.assertEqual(self.backend.profile(), before)

    def test_duplicate_packet_and_changed_serial_reuse(self):
        self.buy()
        before, packet, replies = self.backend.profile(), self.packet, self.replies
        self.assertEqual(self.backend.respond(packet, self.state), replies)
        altered = encode(1057, dict(serial_num=self.serial, index=1, page_id=2, type_id=1032, count=2))
        self.assertIn('已过期', decode(self.backend.respond(altered, self.state)[0])[2]['data'])
        self.assertEqual(self.backend.profile(), before)

    def test_persistence_and_reconnect_do_not_reset_limits(self):
        self.buy(page_id=1, index=10)
        self.backend.close()
        self.backend = Backend(Path(self.tmp.name), 18770, lambda *a, **kw: None)
        with patch('network_redirect.backend.time.time', return_value=self.now):
            cfg = login_fields(decode(self.backend.bootstrap(reconnect=True)[0])[2]['data'])
        self.assertEqual(cfg[10]['cheap_item_list'][10]['buy_limit_times'], 0)

    def test_query_panic_uses_event_138_without_done(self):
        event, result = self.request(1242, sale_time=0)[0]
        self.assertEqual(event, 138)
        self.assertEqual(result['activity_data']['sale_time'], self.start)
        self.assertEqual(len(result['activity_data']['sale_item']), 2)
        self.assertEqual(result['activity_data']['item1_sale_count'], 3)
        self.assertNotIn(1106, [decode(p)[0] for p in self.replies])

    def test_original_price_boundaries(self):
        first = dict(price=150, discounts=[0.7]*6)
        for elapsed, expected in [(0, 150), (1, 105), (600, 105), (601, 105),
                                  (1200, 105), (3001, 105), (3600, 105), (3601, 150)]:
            self.assertEqual(market.current_price(self.start + elapsed, self.start, first), expected)

    def test_panic_purchase_cooldown_stock_and_phase_two(self):
        item = self.request(1242)[0][1]["activity_data"]["sale_item"][1]["item"]
        before = self.count(item["attach_type"])
        self.assertEqual(self.request(1241, buy_index=2)[0][1]['result'], 4)
        for i in range(3):
            result = self.request(1241, buy_index=1)[0][1]
            self.assertEqual(result['result'], 0)
            self.assertEqual(result['activity_data']['item1_sale_count'], 2 - i)
            if i == 0:
                saved = self.backend.profile()
                self.now += 9
                self.assertEqual(self.request(1241, buy_index=1)[0][1]['result'], 1)
                self.assertEqual(self.backend.profile(), saved)
                self.now -= 9
            self.now += 10
        self.assertEqual(self.count(item["attach_type"]), before + 3 * item["attach_count"])
        self.assertEqual(self.request(1241, buy_index=1)[0][1]['result'], 5)
        for i in range(1):
            self.assertEqual(self.request(1241, buy_index=2)[0][1]['result'], 0)
        saved = self.backend.profile()
        self.assertEqual(self.request(1241, buy_index=2)[0][1]['result'], 3)
        self.assertEqual(self.backend.profile(), saved)

    def test_panic_insufficient_and_invalid(self):
        role = self.backend.profile()
        role['gold_coin'] = 0
        self.backend.save(role)
        for index, result in ((1, 2), (0, 1), (3, 1)):
            self.assertEqual(self.request(1241, buy_index=index)[0][1]['result'], result)
            self.assertEqual(self.backend.profile(), role)

    def test_panic_closed_and_stale_session_rejected(self):
        before = self.backend.profile()
        for now in (self.start, self.start + 3601, self.start + 21601):
            self.now = now
            self.assertEqual(self.request(1241, buy_index=1)[0][1]['result'], 4)
            self.assertEqual(self.backend.profile(), before)
        self.request(1242, sale_time=self.start)
        self.assertEqual(self.request(1241, buy_index=1)[0][1]['result'], 0)

    def test_panic_inclusive_end_and_next_session_preserves_quota(self):
        self.now = self.start + 3600
        self.assertEqual(self.request(1241, buy_index=1)[0][1]['result'], 0)
        first = self.rules['panic']['pairs'][self.backend.profile()['market']['panic']['pair_index']]['first']
        self.assertEqual(self.backend.profile()['gold_coin'], 10000 - first['price'] * 70 // 100)
        self.now += 1
        result = self.request(1242)[0][1]
        self.assertEqual(result['activity_data']['sale_time'], self.start + 21600)
        self.assertEqual(result['activity_data']['item1_sale_count'], 2)
        self.assertEqual(result['role_data']['last_buy_item1'], self.start + 3600)

    def test_tuesday_thursday_saturday_schedule_and_sunday_preview(self):
        tz = timezone(timedelta(hours=8))
        for date, expected in [('2026-10-24T04:00', '2026-10-24T12:00'),
                               ('2026-10-27T13:01', '2026-10-27T18:00'),
                               ('2026-10-27T19:01', '2026-10-29T12:00'),
                               ('2026-10-29T19:01', '2026-10-31T12:00'),
                               ('2026-10-31T13:01', '2026-10-31T18:00'),
                               ('2026-10-31T19:01', '2026-11-03T12:00'),
                               ('2026-11-01T12:01', '2026-11-03T12:00')]:
            now = int(datetime.fromisoformat(date).replace(tzinfo=tz).timestamp())
            start = int(datetime.fromisoformat(expected).replace(tzinfo=tz).timestamp())
            self.assertEqual(market.sale_time(now, self.rules), start)

    def test_encode_failure_rolls_back_resources(self):
        before = self.backend.profile()
        with patch.object(self.backend, 'inventory', side_effect=ValueError('wire failure')):
            self.assertEqual(self.buy(), {'op_string': '集市数据无效，请刷新后重试'})
        self.assertEqual(self.backend.profile(), before)

    def test_corrected_catalog_rewards_and_removed_bag(self):
        role = self.backend.profile()
        role['vip_level'] = 1
        self.backend.save(role)
        goods = self.request(first_send=1)[0][1]
        self.assertEqual(goods['cheap_item_list'][8]['origin_price'], 10)
        self.assertEqual(goods['cheap_item_list'][9]['origin_price'], 100)
        result = self.buy(page_id=1, index=8, type_id=1001)
        self.assertEqual(result['attach_list'][1]['attach_count'], 20)
        with self.assertRaises(market.Rejected):
            market.buy(role, dict(page_id=2, index=9137, type_id=1243, count=1), self.now, self.rules)

    def test_all_pairs_grant_and_charge_exact_bundles(self):
        for index, pair in enumerate(self.rules['panic']['pairs']):
            with self.subTest(pair=index):
                role = self.backend.profile()
                state = market.prepare(role, self.now, self.rules)['panic']
                state.update(pair_index=index, sold=0, last_buy_item1=0, has_buy_item2=0)
                before = role['gold_coin']
                for n in range(3):
                    result = market.panic_buy(role, {'buy_index': 1}, self.now + n*10, self.rules, self.start)
                    self.assertEqual(result['attach_list'], [market.attachment(pair['first']['type_id'], pair['first']['count'])])
                result = market.panic_buy(role, {'buy_index': 2}, self.now + 30, self.rules, self.start)
                self.assertEqual(result['attach_list'], [market.attachment(pair['second']['type_id'], pair['second']['count'])])
                self.assertEqual(before - role['gold_coin'], 3 * (pair['first']['price'] * 70 // 100) + pair['second']['price'] * 70 // 100)
                with self.assertRaises(market.Rejected):
                    market.panic_buy(role, {'buy_index': 2}, self.now + 40, self.rules, self.start)

    def test_rotation_midnight_and_reconnect_keep_draw(self):
        role = self.backend.profile()
        initial = copy.deepcopy(market.prepare(role, self.now, self.rules)['panic'])
        market.panic_buy(role, {'buy_index': 1}, self.now, self.rules, self.start)
        self.backend.save(role)
        self.backend.close()
        self.backend = Backend(Path(self.tmp.name), 18770, lambda *a, **kw: None)
        role = self.backend.profile()
        for hours in (0, 6, 12, 35):
            state = market.prepare(role, self.start + hours * 3600 + 60, self.rules)['panic']
            self.assertEqual(state['pair_index'], initial['pair_index'])
            self.assertEqual(state['sold'], 1)
        thursday = self.start + 36 * 3600
        state = market.prepare(role, thursday, self.rules)['panic']
        self.assertEqual(state['rotation_start'], thursday)
        self.assertEqual(state['sold'], 0)
        self.assertEqual(state['has_buy_item2'], 0)
        # Independent selection is stable across repeated reads, not forced to differ.
        self.assertEqual(market.prepare(role, thursday+1, self.rules)['panic']['pair_index'], state['pair_index'])

    def test_old_preview_cannot_buy_new_rotation_even_with_same_sale_time(self):
        self.now = self.start + 2 * 86400 - 13 * 3600  # Wednesday 23:00
        self.request(1242)
        preview_time = self.state['market_sale_time']
        self.now = self.start + 2 * 86400 + 60
        self.assertEqual(preview_time, market.sale_time(self.now, self.rules))
        # Profile reads also recover energy; compare at the same simulated time
        # so normal recovery is not mistaken for a rejected market mutation.
        with patch('network_redirect.backend.time.time', return_value=self.now):
            before = self.backend.profile()
            self.assertEqual(self.request(1241, buy_index=1)[0][1]['result'], 4)
            self.assertEqual(self.backend.profile(), before)
        self.request(1242)
        self.assertEqual(self.request(1241, buy_index=1)[0][1]['result'], 0)

    def test_fixed_quote_matches_original_discount_and_debit_in_every_phase(self):
        for index, pair in enumerate(self.rules['panic']['pairs']):
            role = self.backend.profile()
            state = market.prepare(role, self.now, self.rules)['panic']
            state.update(pair_index=index, sold=0, last_buy_item1=0)
            first, second = market.selected_pair(state, self.rules)
            for elapsed in (-60, 0, 1, 600, 601, 3600, 3601):
                self.assertEqual(market.current_price(self.start + elapsed, self.start, first), pair['first']['price'] * 70 // 100)
            quote = market.panic_snapshot(role, self.now, self.rules)['activity_data']['sale_item']
            self.assertEqual(quote[0]['price'], pair['first']['price'])
            self.assertEqual(quote[0]['panic_price'], first['panic_price'])
            self.assertEqual(quote[1]['panic_price'], second['panic_price'])
            balance = role['gold_coin']
            market.panic_buy(role, {'buy_index': 1}, self.now, self.rules, self.start)
            self.assertEqual(balance-role['gold_coin'], quote[0]['panic_price'])

    def test_weighted_pool_ticket_boundaries_and_probabilities(self):
        pairs = self.rules['panic']['pairs']
        self.assertEqual(len(pairs), 18)
        self.assertEqual([p['weight'] for p in pairs], [3] * 18)
        hits = [0] * len(pairs)
        # Exhaust every ticket, including each boundary, without a flaky sample.
        for ticket in range(54):
            role = self.backend.profile()
            role.pop('market', None)
            with patch('network_redirect.market.hashlib.sha256') as digest:
                digest.return_value.digest.return_value = ticket.to_bytes(32, 'big')
                state = market.prepare(role, self.now, self.rules)['panic']
            hits[state['pair_index']] += 1
        self.assertEqual(hits, [3] * 18)

    def test_seven_new_gifts_cost_300_and_require_three_buns(self):
        pairs = self.rules['panic']['pairs'][11:]
        self.assertEqual([p['second']['type_id'] for p in pairs], [1247,1084,1085,1086,1098,1099,1205])
        for index, pair in enumerate(pairs, 11):
            role = self.backend.profile()
            state = market.prepare(role, self.now, self.rules)['panic']
            state.update(pair_index=index, sold=0, last_buy_item1=0, has_buy_item2=0)
            self.backend.save(role)
            self.assertEqual(pair['first'], dict(type_id=1020, count=1, price=20))
            quote = self.request(1242)[0][1]['activity_data']['sale_item'][2]
            self.assertEqual((quote['price'], quote['panic_price'], quote['per_buy_limit']), (429, 300, 1))
            self.assertEqual(self.request(1241, buy_index=2)[0][1]['result'], 4)
            for _ in range(3):
                self.assertEqual(self.request(1241, buy_index=1)[0][1]['result'], 0)
                self.now += 10
            before = self.count(pair['second']['type_id'])
            balance = self.backend.profile()['gold_coin']
            self.assertEqual(self.request(1241, buy_index=2)[0][1]['result'], 0)
            self.assertEqual(self.count(pair['second']['type_id']), before + 1)
            self.assertEqual(self.backend.profile()['gold_coin'], balance - 300)
            self.assertEqual(self.request(1241, buy_index=2)[0][1]['result'], 3)

    def test_nonstacking_gifts_keep_separate_inventory_ids(self):
        role = self.backend.profile()
        for tid in (1084, 1085, 1086, 1205):
            market.grant(role, tid, 1)
            market.grant(role, tid, 1)
            items = [i for i in role['attachments'] if i['type_id'] == tid and i['attach_type'] == 5]
            self.assertEqual([i['count'] for i in items], [1, 1])
            self.assertEqual(len({i['id'] for i in items}), 2)

    def test_pool_expansion_preserves_current_rotation_and_used_quota(self):
        role = self.backend.profile()
        legacy = copy.deepcopy(self.rules)
        legacy['panic']['pairs'] = legacy['panic']['pairs'][:11]
        state = market.prepare(role, self.now, legacy)['panic']
        state.update(pair_index=10, sold=3, has_buy_item2=1, last_buy_item1=self.now)
        expected = copy.deepcopy(state)
        self.assertEqual(market.prepare(role, self.now, self.rules)['panic'], expected)
        # The next scheduled refresh uses the expanded pool and resets quotas.
        with patch('network_redirect.market.hashlib.sha256') as digest:
            digest.return_value.digest.return_value = (53).to_bytes(32, 'big')
            state = market.prepare(role, self.now + 2 * 86400, self.rules)['panic']
        self.assertEqual((state['pair_index'], state['sold'], state['has_buy_item2']), (17, 0, 0))

    def test_saturday_midnight_reset_sessions_and_sunday_closed(self):
        role = self.backend.profile()
        saturday = self.start + 4 * 86400 - 12 * 3600
        previous = market.prepare(role, saturday-1, self.rules)['panic']
        previous.update(sold=3, has_buy_item2=1)
        self.assertEqual(previous['rotation_start'], saturday-2*86400)
        state = market.prepare(role, saturday, self.rules)['panic']
        self.assertEqual(state['rotation_start'], saturday)
        self.assertEqual((state['sold'], state['has_buy_item2']), (0, 0))
        pair_index = state['pair_index']
        # Saturday has both normal sessions; quotas are shared between them.
        for hour in (12, 18):
            start = saturday + hour*3600
            market.panic_buy(role, {'buy_index': 1}, start+1, self.rules, start)
        state = market.prepare(role, saturday+86400+12*3600, self.rules)['panic']
        self.assertEqual((state['pair_index'], state['sold']), (pair_index, 2))
        with self.assertRaises(market.Rejected) as error:
            market.panic_buy(role, {'buy_index': 1}, saturday+86400+12*3600,
                             self.rules, state['sale_time'])
        self.assertEqual(error.exception.result, 4)
        next_cycle = market.prepare(role, saturday+3*86400, self.rules)['panic']
        self.assertEqual(next_cycle['rotation_start'], saturday+3*86400)
        self.assertEqual(next_cycle['sold'], 0)

    def test_invalid_config_fails_at_startup(self):
        for mutate in (lambda r: r['panic'].update(discount_percent=50),
                       lambda r: r['panic']['pairs'][0]['first'].update(type_id=999999),
                       lambda r: r['panic'].update(hours=[24]),
                       lambda r: r['panic'].update(weekdays=[1,3]),
                       lambda r: r['panic'].update(pairs=[]),
                       lambda r: r['panic']['pairs'][0].pop('weight'),
                       lambda r: r['panic']['pairs'][0].update(weight=0),
                       lambda r: r['panic']['pairs'][0].update(weight=-1),
                       lambda r: r['panic']['pairs'][0].update(weight=True),
                       lambda r: r['panic']['pairs'][0].update(weight=1.5),
                       lambda r: r.update(cheap_daily_limit=0)):
            rules = copy.deepcopy(self.rules)
            mutate(rules)
            path = Path(self.tmp.name) / 'bad.json'
            path.write_text(json.dumps(rules))
            with self.assertRaises(ValueError):
                market.load_rules(path)


if __name__ == '__main__':
    unittest.main()
