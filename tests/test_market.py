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
        self.state = dict(authenticated=True, market_sale_time=self.start)
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
        self.assertEqual(len(goods['cheap_item_list']), 7)
        self.assertEqual(len(goods['rich_item_list']), 9)
        self.assertEqual(goods['rich_item_list'][9137]['type_id'], 1243)
        self.assertEqual(len(goods['limit_item_list']), 0)
        for raw in market.CATALOG:
            if raw['begin_time'] != '0':
                continue
            row = goods[market.LISTS[int(raw['page_id'])]][int(raw['index'])]
            self.assertEqual((row['object_type'], row['type_id'], row['count']), tuple(map(int, raw['type_id'].split('|'))))
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

    def test_bundle_grants_ten_and_preserves_vip_gate(self):
        self.assertEqual(self.buy(page_id=1, index=8, type_id=1001)['result'], 5)
        role = self.backend.profile()
        role['vip_level'] = 1
        self.backend.save(role)
        before = self.count(1001)
        self.assertEqual(self.buy(page_id=1, index=8, type_id=1001)['result'], 1)
        self.assertEqual(self.count(1001), before + 10)
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
        self.assertEqual(result['activity_data']['item1_sale_count'], 10)
        self.assertNotIn(1106, [decode(p)[0] for p in self.replies])

    def test_original_price_boundaries(self):
        first = self.rules['panic']['first']
        for elapsed, expected in [(0, 150), (1, 135), (600, 135), (601, 120),
                                  (1200, 120), (3001, 60), (3600, 60), (3601, 150)]:
            self.assertEqual(market.current_price(self.start + elapsed, self.start, first), expected)

    def test_panic_purchase_cooldown_stock_and_phase_two(self):
        before = self.count(1006)
        self.assertEqual(self.request(1241, buy_index=2)[0][1]['result'], 4)
        for i in range(10):
            result = self.request(1241, buy_index=1)[0][1]
            self.assertEqual(result['result'], 0)
            self.assertEqual(result['activity_data']['item1_sale_count'], 9 - i)
            if i == 0:
                saved = self.backend.profile()
                self.now += 9
                self.assertEqual(self.request(1241, buy_index=1)[0][1]['result'], 1)
                self.assertEqual(self.backend.profile(), saved)
                self.now -= 9
            self.now += 10
        self.assertEqual(self.count(1006), before + 10)
        self.assertEqual(self.request(1241, buy_index=1)[0][1]['result'], 5)
        for i in range(3):
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

    def test_panic_inclusive_end_and_next_session_reset(self):
        self.now = self.start + 3600
        self.assertEqual(self.request(1241, buy_index=1)[0][1]['result'], 0)
        self.assertEqual(self.backend.profile()['gold_coin'], 9940)
        self.now += 1
        result = self.request(1242)[0][1]
        self.assertEqual(result['activity_data']['sale_time'], self.start + 21600)
        self.assertEqual(result['activity_data']['item1_sale_count'], 10)
        self.assertEqual(result['role_data']['last_buy_item1'], 0)

    def test_original_weekly_schedule_and_weekend_preview(self):
        tz = timezone(timedelta(hours=8))
        for date, expected in [('2026-10-24T04:00', '2026-10-27T12:00'),
                               ('2026-10-27T13:01', '2026-10-27T18:00'),
                               ('2026-10-27T19:01', '2026-10-29T12:00'),
                               ('2026-10-29T19:01', '2026-11-03T12:00')]:
            now = int(datetime.fromisoformat(date).replace(tzinfo=tz).timestamp())
            start = int(datetime.fromisoformat(expected).replace(tzinfo=tz).timestamp())
            self.assertEqual(market.sale_time(now, self.rules), start)

    def test_encode_failure_rolls_back_resources(self):
        before = self.backend.profile()
        with patch.object(self.backend, 'inventory', side_effect=ValueError('wire failure')):
            self.assertEqual(self.buy(), {'op_string': '集市数据无效，请刷新后重试'})
        self.assertEqual(self.backend.profile(), before)

    def test_invalid_config_fails_at_startup(self):
        for mutate in (lambda r: r['panic']['first'].update(discounts=[0.5]),
                       lambda r: r['panic']['first'].update(type_id=999999),
                       lambda r: r['panic'].update(hours=[24]),
                       lambda r: r.update(cheap_daily_limit=0)):
            rules = copy.deepcopy(self.rules)
            mutate(rules)
            path = Path(self.tmp.name) / 'bad.json'
            path.write_text(json.dumps(rules))
            with self.assertRaises(ValueError):
                market.load_rules(path)


if __name__ == '__main__':
    unittest.main()
