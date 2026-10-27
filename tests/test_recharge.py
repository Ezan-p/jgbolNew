"""Real wire gold-card transactions, account isolation and downstream benefits."""
import struct
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from network_redirect import summon, daily, activity_rulai, formation
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode

NOW = 1793066400  # 2026-10-27 10:00 UTC+8


class GoldCardRechargeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.clock = patch('network_redirect.backend.time.time', return_value=NOW)
        self.clock.start(); self.addCleanup(self.clock.stop)
        self.b = Backend(Path(self.tmp.name), 18790, lambda *a, **k: None)
        self.addCleanup(lambda: self.b.close())
        self.serial = 500

    def req(self, mid=1111, **data):
        self.serial += 1
        self.packet = encode(mid, dict(serial_num=self.serial, **data))
        self.replies = self.b.respond(self.packet, dict(authenticated=True))
        self.assertEqual(decode(self.replies[-1])[0], 1106)
        return [(d['id'], login_fields(d['data']))
                for m, _, d in map(decode, self.replies) if m == 2998]

    def charge(self, item=102, large=1, small=0, order=None, **extra):
        data = dict(item_id=item, large_count=large, small_count=small,
                    order_id=order or f'card-order-{self.serial}')
        data.update(extra)
        return self.req(event_id=251, data=summon.lua(data))

    def stock(self, large=20, small=40):
        role = self.b.profile()
        if large: summon.add_item(role, 1152, large)
        if small: summon.add_item(role, 1156, small)
        self.b.save(role)

    def count(self, tid):
        return sum(i['count'] for i in self.b.profile()['attachments']
                   if i['attach_type'] == 5 and i['type_id'] == tid)

    def unchanged(self, fn):
        before = self.b.profile()
        out = fn()
        self.assertTrue(any(e == 55 for e, _ in out), out)
        self.assertEqual(before, self.b.profile())
        return out

    def assert_statistics(self, role, gold):
        self.assertEqual(role['charge_gold'], gold)
        self.assertEqual(role['xianling']['charge'], gold)
        self.assertEqual(role['pavilion']['charge_gold'], gold)
        self.assertEqual(role['activity']['rulai']['charge_gold'], gold)
        self.assertEqual(role['activity']['yuanshi']['charge_gold'], gold)
        key = str(daily.day(NOW, self.b.welfare_rules))
        self.assertEqual(role['welfare']['charge_days'][key], gold)

    def test_mixed_cards_fund_all_counters_and_vip_by_principal(self):
        self.stock(2, 20)
        before = self.b.profile()
        self.charge(item=103, large=1, small=10)
        role = self.b.profile()
        self.assertEqual((self.count(1152), self.count(1156)), (1, 10))
        self.assert_statistics(role, 1000)
        self.assertEqual(role['vip_level'], 3)
        self.assertGreaterEqual(role['gold_coin'] - before['gold_coin'], 2110)
        self.assertTrue(role['first_charge'])
        # First-charge and product gifts cannot increase the principal ledger.
        self.assertGreater(role['gold_coin'] - before['gold_coin'], role['charge_gold'])

    def test_insufficient_locked_owned_and_equipped_cards_are_not_spendable(self):
        self.unchanged(lambda: self.charge())
        self.stock(1, 0)
        for field in ('is_lock', 'owner_id', 'equip_pos'):
            role = self.b.profile()
            card = next(i for i in role['attachments'] if i['type_id'] == 1152)
            card[field] = 1
            self.b.save(role)
            self.unchanged(lambda: self.charge())
            role = self.b.profile()
            next(i for i in role['attachments'] if i['type_id'] == 1152)[field] = 0
            self.b.save(role)
        self.charge()
        self.assertEqual(self.count(1152), 0)
        self.assert_statistics(self.b.profile(), 500)

    def test_counts_types_exact_value_and_server_owned_price(self):
        self.stock()
        for large, small in [(0, 0), (0, 9), (0, 11), (2, 0), (-1, 20),
                             (True, 0), (1.0, 0), ('1', 0), (1, -1)]:
            with self.subTest(large=large, small=small):
                self.unchanged(lambda: self.charge(large=large, small=small))
        self.unchanged(lambda: self.charge(item=999))
        self.unchanged(lambda: self.charge(order='bad'))
        self.unchanged(lambda: self.req(event_id=251, data='os.execute("false")'))
        # Forged amount fields can be rejected or ignored, never credited.
        self.charge(gold=999999, price_rmb=1, bonus=999999)
        role = self.b.profile()
        self.assertIn(role['charge_gold'], (0, 500))
        self.assertLess(role['gold_coin'], 10000)

    def test_two_unlocked_stacks_consumed_without_touching_locked_stack(self):
        self.stock(1, 0)
        role = self.b.profile()
        card = next(i for i in role['attachments'] if i['type_id'] == 1152)
        card['is_lock'] = True
        role['attachments'].extend([dict(card, id=card['id'] + 100, is_lock=False, count=1),
                                    dict(card, id=card['id'] + 101, is_lock=False, count=1)])
        self.b.save(role)
        self.charge(item=103, large=2)
        cards = [i for i in self.b.profile()['attachments'] if i['type_id'] == 1152]
        self.assertEqual(len(cards), 1)
        self.assertEqual((cards[0]['id'], cards[0]['count'], cards[0]['is_lock']),
                         (card['id'], 1, True))

    def test_legacy_simulator_and_unfunded_prebuy_cannot_credit(self):
        self.stock()
        self.unchanged(lambda: self.req(event_id=250,
                        data='{item_id=106,order_id="legacy-free-order"}'))
        for event, item in [(1, 1), (2, 7), (3, 8)]:
            self.unchanged(lambda: self.req(1112, event_id=event,
                                            data=summon.lua(dict(item_id=item))))

    def test_exact_packet_order_reconnect_and_conflicting_order(self):
        self.stock()
        self.charge(order='durable-gold-card')
        after = self.b.profile()
        self.assertEqual(self.b.respond(self.packet, dict(authenticated=True)), self.replies)
        self.assertEqual(after, self.b.profile())
        self.charge(order='durable-gold-card')
        self.assertEqual(after, self.b.profile())
        self.unchanged(lambda: self.charge(large=0, small=10, order='durable-gold-card'))
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18790, lambda *a, **k: None)
        self.charge(order='durable-gold-card')
        self.assertEqual(after, self.b.profile())
        with patch('network_redirect.backend.time.time', return_value=NOW + 40 * 86400):
            self.charge(order='durable-gold-card')
        self.assertEqual(self.b.profile()['charge_gold'], 500)
        self.assertEqual(self.count(1152), 19)

    def test_encoding_failure_rolls_back_cards_order_rewards_and_hooks(self):
        self.stock()
        with patch.object(self.b, 'inventory', side_effect=struct.error('injected encoding failure')):
            self.unchanged(lambda: self.charge(order='rollback-gold-card'))
        self.charge(order='rollback-gold-card')
        self.assertEqual(self.count(1152), 19)
        self.assert_statistics(self.b.profile(), 500)

    def test_same_order_is_account_scoped(self):
        self.stock()
        self.charge(order='same-across-accounts')
        original = self.b
        other = Backend(Path(self.tmp.name), 18790, lambda *a, **k: None,
                        account='recharge-second-account')
        try:
            self.b = other
            self.stock(1, 0)
            self.charge(order='same-across-accounts')
            self.assert_statistics(self.b.profile(), 500)
        finally:
            self.b = original
            other.close()
        self.assert_statistics(self.b.profile(), 500)

    def test_month_card_daily_claim_expiry_renewal_and_no_recharge_for_daily_gold(self):
        self.stock()
        self.charge(item=201)
        bought = self.b.profile()
        self.assertEqual(bought['month_card_time'], NOW + 30 * 86400)
        self.assert_statistics(bought, 500)
        before_gold = bought['gold_coin']
        out = self.req(1201, flag=9, id=0)
        self.assertIn((74, dict(result=1, gold_count=100)), out)
        self.assertEqual(self.b.profile()['gold_coin'], before_gold + 100)
        self.assert_statistics(self.b.profile(), 500)
        self.unchanged(lambda: self.req(1201, flag=9, id=0))
        # A renewal cannot grant a second reward for the same natural day.
        self.charge(item=201)
        self.assertEqual(self.b.profile()['month_card_time'], NOW + 60 * 86400)
        self.unchanged(lambda: self.req(1201, flag=9, id=0))
        self.unchanged(lambda: self.charge(item=201))
        with patch('network_redirect.backend.time.time', return_value=NOW + 86400):
            old = self.b.profile()['gold_coin']
            self.req(1201, flag=9, id=0)
            self.assertEqual(self.b.profile()['gold_coin'], old + 100)
        with patch('network_redirect.backend.time.time', return_value=NOW + 60 * 86400):
            self.unchanged(lambda: self.req(1201, flag=9, id=0))

    def test_growth_fund_is_paid_once_and_reaches_every_charge_hook(self):
        self.stock(0, 18)
        before = self.b.profile()
        self.charge(item=202, large=0, small=9)
        role = self.b.profile()
        self.assertTrue(role['buy_growup'])
        self.assertEqual(self.count(1156), 9)
        self.assert_statistics(role, 450)
        self.assertFalse(role['first_charge'])
        self.unchanged(lambda: self.charge(item=202, large=0, small=9))

    def test_direct_card_use_counts_principal_and_consumes_selected_stack(self):
        self.stock(0, 3)
        role = self.b.profile()
        item = next(i for i in role['attachments'] if i['type_id'] == 1156)
        args = dict(item_type=1156, item_id=item['id'], item_count=2,
                    des_type=1, des_id=role['role_id'])
        self.req(1051, **args)
        self.assertEqual(self.count(1156), 1)
        self.assert_statistics(self.b.profile(), 100)
        self.assertEqual(self.b.respond(self.packet, dict(authenticated=True)), self.replies)
        self.assertEqual(self.count(1156), 1)

    def test_period_boundary_charge_resets_event_ledgers_without_resetting_vip(self):
        self.stock()
        self.charge()
        _, end = activity_rulai.period(NOW, activity_rulai.load_rules())
        with patch('network_redirect.backend.time.time', return_value=end):
            self.charge(order='new-season-charge')
        role = self.b.profile()
        self.assertEqual(role['charge_gold'], 1000)
        self.assertEqual(role['activity']['rulai']['charge_gold'], 500)

    def test_operator_mail_to_inventory_to_payment_to_first_reward_complete_loop(self):
        from network_redirect import system_mail
        role = self.b.profile()
        status, mail = system_mail.deliver(role, key='test-gold-card-issue',
            title='金卡发放', body='充值系统闭环测试', prizes=[[5, 1152, 1, 1], [5, 1156, 2, 1]],
            now=NOW, rules=self.b.welfare_rules)
        self.assertEqual(status, 'delivered')
        self.b.save(role)
        self.assertEqual((self.count(1152), self.count(1156)), (0, 0))
        self.req(1102, mail_id=mail['mail_id'], flag=0)
        out = self.req(1103, mail_id=mail['mail_id'])
        self.assertTrue(any(e == 15 and d['result'] == 1 for e, d in out))
        self.assertEqual((self.count(1152), self.count(1156)), (1, 2))
        self.charge()
        self.assertEqual((self.count(1152), self.count(1156)), (0, 2))
        self.assert_statistics(self.b.profile(), 500)
        out = self.req(1201, flag=6, id=0)
        self.assertTrue(any(e == 60 and d['attach_list'] for e, d in out))
        self.unchanged(lambda: self.req(1201, flag=6, id=0))
        self.unchanged(lambda: self.req(1103, mail_id=mail['mail_id']))
        # Reissuing the same operator batch cannot refill the spent card.
        role = self.b.profile()
        status, _ = system_mail.deliver(role, key='test-gold-card-issue',
            title='金卡发放', body='充值系统闭环测试', prizes=[[5, 1152, 1, 1], [5, 1156, 2, 1]],
            now=NOW, rules=self.b.welfare_rules)
        self.assertEqual(status, 'already_claimed')
        self.b.save(role)
        self.assertEqual(self.count(1152), 0)

    def test_bootstrap_exports_server_catalog_inventory_and_native_month_state(self):
        self.stock(3, 4)
        config = login_fields(decode(self.b.bootstrap()[0])[2]['data'])
        card = config['local_recharge']
        self.assertEqual((card['large_count'], card['small_count']), (3, 4))
        self.assertEqual((card['large_rmb'], card['small_rmb']), (50, 5))
        products = {p['id']: p for p in card['products'].values()}
        self.assertEqual([products[i]['rmb'] for i in range(101, 107)],
                         [10, 50, 100, 200, 500, 1000])
        self.assertEqual((products[201]['rmb'], products[202]['rmb']), (50, 45))
        self.assertEqual(card['month']['daily_gold'], 100)
        self.charge(item=201)
        config = login_fields(decode(self.b.bootstrap()[0])[2]['data'])
        self.assertEqual(config['local_vip']['month_card_time'], NOW + 30 * 86400)
        self.assertEqual(config['local_recharge']['large_count'], 2)

    def test_failure_in_last_activity_hook_rolls_back_earlier_side_effects(self):
        self.stock()
        with patch.object(activity_rulai, 'record_charge',
                          side_effect=formation.Rejected('injected activity failure')):
            self.unchanged(lambda: self.charge(order='hook-rollback-order'))
        self.charge(order='hook-rollback-order')
        self.assert_statistics(self.b.profile(), 500)
        self.assertEqual(self.count(1152), 19)

    def test_two_backend_connections_cannot_spend_the_same_last_card(self):
        self.stock(1, 0)
        other = Backend(Path(self.tmp.name), 18790, lambda *a, **k: None)
        try:
            # Both connections inspect the same pre-payment inventory.
            self.assertEqual(sum(i['count'] for i in other.profile()['attachments']
                                 if i['type_id'] == 1152), 1)
            self.charge(order='connection-one-order')
            after = self.b.profile()
            packet = encode(1111, dict(serial_num=501, event_id=251,
                data=summon.lua(dict(item_id=102, large_count=1, small_count=0,
                                     order_id='connection-two-order'))))
            replies = other.respond(packet, dict(authenticated=True))
            self.assertTrue(any(m == 2998 and d['id'] == 55 for m, _, d in map(decode, replies)))
            self.assertEqual(other.profile(), after)
            self.assertEqual(self.b.profile(), after)
        finally:
            other.close()

    def test_bag_order_survives_restart_and_allows_fresh_use_with_reset_serial(self):
        self.stock(0, 3)
        item = next(i for i in self.b.profile()['attachments'] if i['type_id'] == 1156)
        args = dict(item_type=1156, item_id=item['id'], item_count=1, des_type=1, des_id=0)
        self.req(event_id=253, data=summon.lua(dict(args, order_id='card-use-session-one')))
        old_packet = self.packet
        self.assertEqual(self.count(1156), 2)
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18790, lambda *a, **k: None)
        # Original client request serials restart at a fixed value. Order IDs do not.
        self.serial = 500
        self.req(event_id=253, data=summon.lua(dict(args, order_id='card-use-session-two')))
        self.assertEqual(decode(old_packet)[2]['serial_num'], decode(self.packet)[2]['serial_num'])
        self.assertEqual(self.count(1156), 1)
        self.assert_statistics(self.b.profile(), 100)
        self.req(event_id=253, data=summon.lua(dict(args, order_id='card-use-session-one')))
        self.assertEqual(self.count(1156), 1)
        self.unchanged(lambda: self.req(event_id=253,
            data=summon.lua(dict(args, item_count=2, order_id='card-use-session-one'))))

    def test_month_card_daily_reward_depends_only_on_expiry_and_claim_day(self):
        self.stock()
        self.charge(item=201)
        initial_gold = self.b.profile()['gold_coin']
        self.assertNotIn('month_card_rewards_remaining', self.b.profile())
        for day in range(30):
            with patch('network_redirect.backend.time.time', return_value=NOW + day * 86400):
                out = self.req(1201, flag=9, id=0)
                self.assertIn((74, dict(result=1, gold_count=100)), out)
        self.assertEqual(self.b.profile()['gold_coin'] - initial_gold, 3000)
        self.assertNotIn('month_card_rewards_remaining', self.b.profile())
        # The 31st calendar day starts before 30 elapsed days have finished.
        with patch('network_redirect.backend.time.time', return_value=NOW + 30 * 86400 - 3600):
            self.assertIn((74, dict(result=1, gold_count=100)), self.req(1201, flag=9, id=0))
        with patch('network_redirect.backend.time.time', return_value=NOW + 30 * 86400):
            self.unchanged(lambda: self.req(1201, flag=9, id=0))
        self.assertEqual(self.b.profile()['charge_gold'], 500)

    def test_month_reward_restart_midnight_clock_rollback_and_expired_credit(self):
        self.stock()
        self.charge(item=201)
        with patch('network_redirect.backend.time.time', return_value=NOW - 1):
            self.unchanged(lambda: self.req(1201, flag=9, id=0))
        self.req(1201, flag=9, id=0)
        self.assertNotIn('month_card_rewards_remaining', self.b.profile())
        next_midnight = ((NOW + 8 * 3600) // 86400 + 1) * 86400 - 8 * 3600
        with patch('network_redirect.backend.time.time', return_value=next_midnight - 1):
            self.unchanged(lambda: self.req(1201, flag=9, id=0))
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18790, lambda *a, **k: None)
        with patch('network_redirect.backend.time.time', return_value=next_midnight):
            self.req(1201, flag=9, id=0)
            self.assertNotIn('month_card_rewards_remaining', self.b.profile())
        with patch('network_redirect.backend.time.time', return_value=NOW + 31 * 86400):
            self.charge(item=201, order='renew-expired-month')
            self.assertNotIn('month_card_rewards_remaining', self.b.profile())
            self.assertEqual(self.b.profile()['month_card_time'], NOW + 61 * 86400)
            self.req(1201, flag=9, id=0)
            self.assertNotIn('month_card_rewards_remaining', self.b.profile())

    def test_definite_failure_receipt_preserves_inventory_orders_and_saved_role(self):
        self.stock(1, 2)
        before = self.b.profile()
        stored = self.b.db.execute('SELECT data FROM roles WHERE account=?', (self.b.account,)).fetchone()[0]

        def check_receipt(events, order):
            receipt = next(d['local_recharge'] for e, d in events
                           if e == 80 and 'failed_order_id' in d.get('local_recharge', {}))
            self.assertEqual(receipt['failed_order_id'], order)
            self.assertEqual((receipt['large_count'], receipt['small_count']), (1, 2))
            self.assertEqual(receipt['last_order_id'], '')
            self.assertEqual(self.b.profile(), before)
            self.assertEqual(self.b.profile().get('recharge', {}).get('orders', {}), {})
            self.assertEqual(self.b.db.execute('SELECT data FROM roles WHERE account=?',
                                              (self.b.account,)).fetchone()[0], stored)

        check_receipt(self.charge(large=0, small=10, order='failed-insufficient-cards'),
                      'failed-insufficient-cards')
        item = next(i for i in before['attachments'] if i['type_id'] == 1156)
        check_receipt(self.req(event_id=253, data=summon.lua(dict(
            order_id='failed-bag-count', item_type=1156, item_id=item['id'],
            item_count=3, des_type=1, des_id=0))), 'failed-bag-count')
        with patch.object(self.b, 'inventory', side_effect=struct.error('injected encode failure')):
            check_receipt(self.charge(order='failed-after-debit'), 'failed-after-debit')
        # A definite rollback leaves the original order usable on an explicit retry.
        self.charge(order='failed-after-debit')
        self.assertEqual(self.count(1152), 0)
        self.assert_statistics(self.b.profile(), 500)

    def test_broken_state_renderer_still_acks_failure_and_rolls_back_payment(self):
        self.stock(1, 0)
        before = self.b.profile()
        with patch('network_redirect.backend.recharge.client_state',
                   side_effect=ValueError('injected state-render failure')) as renderer:
            out = self.charge(order='state-render-failure')
            # Both the success snapshot and the fallback failure snapshot fail.
            self.assertEqual(renderer.call_count, 2)
        self.assertEqual([e for e, _ in out], [55])
        self.assertEqual(decode(self.replies[-1])[0], 1106)
        self.assertEqual(self.b.profile(), before)
        self.assertEqual(self.b.profile().get('recharge', {}).get('orders', {}), {})
        self.charge(order='state-render-failure')
        self.assertEqual(self.count(1152), 0)
        self.assert_statistics(self.b.profile(), 500)

    def test_obsolete_month_quota_does_not_block_daily_claim(self):
        role = self.b.profile()
        role.update(month_card_time=NOW + 2 * 86400, month_card_rewards_remaining=0)
        self.b.save(role)
        config = login_fields(decode(self.b.bootstrap()[0])[2]['data'])
        self.assertNotIn('rewards_remaining', config['local_recharge']['month'])
        self.assertTrue(any(e == 74 for e, _ in self.req(1201, flag=9, id=0)))
        self.assertNotIn('month_card_rewards_remaining', self.b.profile())

    def test_payment_and_backpack_use_send_passive_state_without_navigation(self):
        self.stock()
        out = self.charge()
        item = next(i for i in self.b.profile()['attachments'] if i['type_id'] == 1156)
        bag = dict(item_id=item['id'],item_type=1156,item_count=1,des_type=1,des_id=0)
        outputs = [out, self.req(event_id=253, data=summon.lua(dict(bag,order_id='passive-bag-order'))),
                   self.req(1051, **bag)]
        for output in outputs:
            self.assertFalse({47,48,93,127} & {e for e,_ in output})
            passive = next(d['local_welfare'] for e,d in output if e == 80 and 'local_welfare' in d)
            self.assertGreater(passive['spring_info']['total_charge_count'],0)
            self.assertIn(22,passive['all_activity'])

    def test_growth_fund_purchase_cancel_equivalent_and_every_level_reward_once(self):
        self.stock(0, 18)
        # Merely querying the page cannot buy a fund or debit the cards.
        out=self.req(1127,flag=1,act_type=22,index=0)
        self.assertEqual(self.count(1156),18)
        self.assertEqual(self.b.profile()['buy_growup'],0)
        self.unchanged(lambda:self.req(1127,flag=2,act_type=22,index=0))
        self.charge(item=202,large=0,small=9,order='fund-full-lifecycle')
        self.assertEqual(self.count(1156),9)
        self.assert_statistics(self.b.profile(),450)
        self.unchanged(lambda:self.charge(item=202,large=0,small=9,order='fund-purchase-again'))
        for row in self.b.welfare_rules['fund']:
            role=self.b.profile();role['level']=row['level'];self.b.save(role)
            before=self.b.profile()['gold_coin']
            out=self.req(1127,flag=2,act_type=22,index=0)
            self.assertTrue(any(e==127 and d['flag']==2 for e,d in out))
            self.assertEqual(self.b.profile()['gold_coin']-before,sum(p[2] for p in row['prizes'] if p[0]==11))
            self.assertEqual(self.b.profile()['charge_gold'],450)
            self.unchanged(lambda:self.req(1127,flag=2,act_type=22,index=0))
        self.b.close();self.b=Backend(Path(self.tmp.name),18790,lambda *a,**k:None)
        self.unchanged(lambda:self.req(1127,flag=2,act_type=22,index=0))

    def test_growth_fund_can_claim_all_eligible_tiers_after_welfare_expiry(self):
        self.stock(0,9)
        self.charge(item=202,large=0,small=9)
        role=self.b.profile();role['level']=99;self.b.save(role)
        with patch('network_redirect.backend.time.time',return_value=NOW+31*86400):
            before=self.b.profile()['gold_coin']
            out=self.req(1127,flag=2,act_type=22,index=0)
            self.assertTrue(any(e==127 and d['flag']==2 for e,d in out))
            self.assertEqual(self.b.profile()['gold_coin']-before,
                             sum(p[2] for r in self.b.welfare_rules['fund'] for p in r['prizes'] if p[0]==11))
            self.unchanged(lambda:self.req(1127,flag=2,act_type=22,index=0))

    def test_success_log_failure_keeps_committed_payment_successful_and_idempotent(self):
        self.stock(1, 0)
        logged = []

        def broken_success_log(kind, **payload):
            logged.append(kind)
            if kind == 'game_vip_ok':
                raise ValueError('injected telemetry failure after commit')

        with patch.object(self.b, 'emit', side_effect=broken_success_log):
            out = self.charge(order='success-log-failure')
        self.assertIn('game_vip_ok', logged)
        self.assertNotIn('game_vip_rejected', logged)
        receipt = next(d['local_recharge'] for e, d in out if e == 80 and 'local_recharge' in d)
        self.assertEqual(receipt['last_order_id'], 'success-log-failure')
        self.assertNotIn('failed_order_id', receipt)
        self.assertEqual(self.count(1152), 0)
        self.assert_statistics(self.b.profile(), 500)
        committed = self.b.profile()
        self.charge(order='success-log-failure')
        self.assertEqual(self.b.profile(), committed)


if __name__ == '__main__':
    unittest.main()
