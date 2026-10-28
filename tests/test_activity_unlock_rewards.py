"""Locked activities cannot earn passive gifts or recharge entitlements."""
import copy
from unittest.mock import patch

from recharge_helpers import funded_order
from test_activity import ActivityCase, NOW
from network_redirect import activity_rulai as rulai, activity_yuanshi as yuanshi


class ActivityUnlockRewardTests(ActivityCase):
    def setUp(self):
        super().setUp()
        self.set_level(19)

    def set_level(self, level):
        role = self.b.profile(); role['level'] = level; self.b.save(role)

    def count(self, tid):
        return sum(i['count'] for i in self.b.profile()['attachments']
                   if i['attach_type'] == 5 and i['type_id'] == tid)

    def charge(self, product, order):
        return self.req(1111, event_id=251, data=funded_order(self.b, product, order))

    def test_fish_daily_gifts_start_on_unlock_without_backfill(self):
        for offset in (0, 86400, 2 * 86400):
            with patch('network_redirect.backend.time.time', return_value=NOW + offset):
                self.b.bootstrap()
                self.ok(self.req(1205, flag=0))
                self.ok(self.req(1205, flag=0))
                self.assertEqual(self.count(1026), 0)
                self.assertEqual(self.b.profile()['activity']['seasonal']['fish']['gift_day'], -1)
        with patch('network_redirect.backend.time.time', return_value=NOW + 2 * 86400):
            self.set_level(20)
            self.ok(self.req(1205, flag=0)); self.ok(self.req(1205, flag=0))
            self.assertEqual(self.count(1026), self.b.activity_rules['fish_daily_nets'])
        with patch('network_redirect.backend.time.time', return_value=NOW + 3 * 86400):
            self.ok(self.req(1205, flag=0))
            self.assertEqual(self.count(1026), 2 * self.b.activity_rules['fish_daily_nets'])

    def test_all_payment_routes_skip_locked_rewards_and_old_orders_stay_skipped(self):
        for product in (101, 201, 202):
            self.charge(product, f'locked-activity-{product}')
        role = self.b.profile()
        card = next(i for i in role['attachments'] if i['type_id'] == 1152)
        self.req(1051, item_id=card['id'], item_type=1152, item_count=1,
                 des_type=1, des_id=role['role_id'])
        role = self.b.profile()
        self.assertEqual(role['charge_gold'], 1550)
        self.assertGreater(role['month_card_time'], NOW)
        self.assertEqual(role['buy_growup'], 1)
        for key in ('yuanshi', 'rulai', 'nine_sky'):
            self.assertNotIn(key, role['activity'])
        self.set_level(20)
        self.charge(101, 'locked-activity-101')
        self.assertNotIn('yuanshi', self.b.profile()['activity'])
        self.charge(102, 'unlocked-activity-order')
        role = self.b.profile()
        self.assertEqual(role['charge_gold'], 2050)
        self.assertEqual(role['activity']['yuanshi']['charge_gold'], 500)
        self.assertEqual(role['activity']['yuanshi']['gift_counts'], [1])
        self.assertEqual(role['activity']['rulai']['charge_gold'], 500)
        cfg = rulai.load_rules()
        self.assertEqual(rulai.remaining(role['activity']['rulai'], cfg),
                         500 // (cfg['rmb_per_draw'] * cfg['gold_per_rmb']))
        self.charge(102, 'unlocked-activity-order')
        self.assertEqual(self.b.profile(), role)

    def test_locked_hooks_leave_existing_activity_progress_untouched(self):
        role = self.b.profile()
        rulai.state(role, NOW, rulai.load_rules())
        yuanshi.state(role, NOW, yuanshi.load_rules())
        before = copy.deepcopy(role)
        rulai.record_charge(role, 499, NOW)
        yuanshi.record_charge(role, 299, NOW)
        self.assertEqual(role, before)
        role['level'] = 20
        rulai.record_charge(role, 1, NOW)
        yuanshi.record_charge(role, 1, NOW)
        self.assertEqual(role['activity']['rulai']['charge_gold'], 1)
        self.assertEqual(role['activity']['yuanshi']['charge_gold'], 1)

    def test_free_attempts_and_yuanshi_shop_do_not_accrue_before_unlock(self):
        self.charge(102, 'locked-before-days-pass')
        for offset in (0, 2 * 86400):
            with patch('network_redirect.backend.time.time', return_value=NOW + offset):
                self.ok(self.req(1205, flag=0))
                for mid, args in ((1309, dict(id=1, data='{}')),
                                  (1334, dict(flag=0, index=0)),
                                  (1351, dict(id=0, data='{}'))):
                    before = self.b.profile()
                    self.assertEqual(self.req(mid, **args)[0][0], 55)
                    self.assertEqual(self.b.profile(), before)
                self.assertNotIn('nine_sky', self.b.profile()['activity'])
                self.assertNotIn('yuanshi', self.b.profile()['activity'])
        with patch('network_redirect.backend.time.time', return_value=NOW + 2 * 86400):
            self.set_level(20)
            self.ok(self.req(1309, id=1, data='{}'))
            self.ok(self.req(1334, flag=0, index=0))
            role = self.b.profile()
            self.assertEqual(role['activity']['nine_sky']['free_times'], 5)
            self.assertEqual(role['activity']['yuanshi']['free'], 1)
            self.assertEqual(role['activity']['yuanshi']['offering_stock'], 0)
            self.assertEqual(role['activity']['yuanshi']['gift_counts'], [])
