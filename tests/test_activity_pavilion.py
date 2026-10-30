"""Real 1227 packets, original catalog, local recharge/mail, limits and rollback."""
from recharge_helpers import funded_order
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_activity import ActivityCase, NOW
from network_redirect import activity_pavilion as p, formation, summon
from network_redirect.backend import Backend
from network_redirect.protocol import encode, decode


class PavilionTests(ActivityCase):
    def test_client_uses_same_original_catalog_with_normalized_headers(self):
        tables = p.client_tables()
        for row in tables['csv_config/exchange_zone.csv']:
            source = p.SHOP[int(row['index'])]
            self.assertEqual(row['goldon_count'], source['goldon_count'])
            self.assertEqual(row['attach_list'], source['attach_list'])
            self.assertEqual(row['max_buy_count'], source['max_buy_count'])
            self.assertIn('name', row); self.assertEqual(row['first_prize'], '')
        source = summon.client_source(self.b.summon_rules)
        self.assertNotIn('__PAVILION_TABLES__', source)
        self.assertIn('csv_config/exchange_zone.csv', source)

    def test_gem_mail_supported_levels_and_nonstacking(self):
        from network_redirect import system_mail, journey
        role = self.b.profile()
        system_mail.deliver(role, key='pavilion-gem-test', title='灵石', body='测试',
                            prizes=[[5,1092,2,8]], now=NOW, rules=self.b.welfare_rules)
        before = copy.deepcopy(role)
        with self.assertRaises(formation.Rejected):
            system_mail.deliver(role, key='pavilion-gem-invalid', title='灵石', body='测试',
                                prizes=[[5,1092,1,255]], now=NOW, rules=self.b.welfare_rules)
        self.assertEqual(role, before)
        journey.grant(role, [5,1090,3,9])
        stones = [i for i in role['attachments'] if i['type_id']==1090 and i['level']==9]
        self.assertEqual(len(stones), 3)
        self.assertEqual(len({i['id'] for i in stones}), 3)
        self.assertTrue(all(i['count']==1 for i in stones))

    def call(self, flag=1, **kw):
        return self.req(1227, **dict(dict(flag=flag, index=0, count=0, ten_card=0, five_card=0), **kw))

    def data(self, events):
        self.ok(events)
        return next(d for e, d in events if e == 195)

    def amount(self, tid):
        return sum(i['count'] for i in self.b.profile()['attachments'] if i['attach_type'] == 5 and i['type_id'] == tid)

    def stock(self, *items):
        r = self.b.profile()
        for tid, count in items: summon.add_item(r, tid, count)
        self.b.save(r)

    def charge(self, order='pavilion-order', product=106):
        return self.req(1111, event_id=251, data=funded_order(self.b, product, order))

    def claim_mails(self):
        mails = self.b.profile()['welfare'].get('mails', {})
        for key, mail in mails.items():
            if key.startswith('pavilion-') and not mail['claimed']:
                self.ok(self.req(1103, mail_id=mail['mail_id']))

    def test_entry_status_native_catalog(self):
        events = self.req(1205, flag=0); self.ok(events)
        status = next(d for e, d in events if e == 47)['pavilion_data']
        self.assertLess(status['begin_time'], NOW); self.assertGreater(status['end_time'], NOW)
        d = self.data(self.call())
        self.assertEqual(len(d['exchange_info']), 10)
        self.assertEqual(len(d['charge_info']), 4)
        for i, row in p.SHOP.items():
            self.assertEqual(d['exchange_info'][i]['left_buy_count'], int(row['max_buy_count']))
        self.assertFalse(d['had_prize'])

    def test_all_nine_original_rewards_and_first_mail(self):
        self.stock((1141, 3000))
        for index, row in p.SHOP.items():
            d = self.data(self.call(2, index=index, count=1))
            expected = p.specs(row['attach_list'])
            self.assertEqual([[v['object_type'],v['attach_type'],v['attach_count'],v['attach_level']]
                              for v in d['attach_list'].values()], expected)
            mails = [m for key,m in self.b.profile()['welfare']['mails'].items()
                     if key.startswith('pavilion-first-') and key.endswith('-'+str(index))]
            self.assertEqual(len(mails), 1)
            self.assertEqual(mails[0]['prizes'], p.specs(row['gift_prize']))
        self.claim_mails()
        self.assertEqual(self.b.profile()['achievements']['totals'].get('125', 0), 0)
        # Original level-9/8 stones must retain their CSV levels, not become piles of level-1 stones.
        self.assertTrue(any(i['type_id']==1090 and i['level']==9 for i in self.b.profile()['attachments']))

    def test_discount_batch_one_card_per_gift_and_zero_floor(self):
        self.stock((1141, 200), (1142, 3), (1143, 3))
        before = self.amount(1141)
        self.data(self.call(2, index=3, count=3, five_card=1, ten_card=2))
        self.assertEqual(self.amount(1141), before - 35)
        self.assertEqual(self.amount(1142), 2); self.assertEqual(self.amount(1143), 1)
        self.data(self.call(2, index=9, count=1, ten_card=1))
        self.assertEqual(self.amount(1141), before - 35)
        old = self.b.profile()
        self.assertEqual(self.call(2, index=9, count=1, five_card=2)[0][0], 55)
        self.assertEqual(old, self.b.profile())

    def test_limits_first_bonus_once_duplicate_and_changed_serial(self):
        self.stock((1141, 1000))
        self.data(self.call(2, index=3, count=10))
        packet, replies, before = self.packet, self.replies, self.b.profile()
        self.assertEqual(self.b.respond(packet, self.state), replies)
        self.assertEqual(before, self.b.profile())
        bad = encode(1227, dict(serial_num=self.serial, flag=2, index=3, count=1))
        self.assertEqual(decode(self.b.respond(bad, self.state)[0])[2]['id'], 55)
        self.data(self.call(2, index=3, count=5))
        before = self.b.profile()
        self.assertEqual(len([k for k in before['welfare']['mails'] if k.startswith('pavilion-first-')]), 1)
        self.assertEqual(self.call(2, index=3, count=1)[0][0], 55)
        self.assertEqual(before, self.b.profile())

    def test_recharge_mail_base_bonus_claim_all_gifts_order_idempotence(self):
        self.charge()
        s = self.b.profile()['pavilion']
        self.assertEqual(s['charge_gold'], 10000)
        self.assertEqual(s['bricks_earned'], 1350)  # 1000 + 10 + 40 + 100 + 200
        self.assertEqual(self.amount(1141), 0)  # native text promises mail delivery
        self.claim_mails(); self.assertEqual(self.amount(1141), 1350)
        d = self.data(self.call())
        self.assertTrue(d['had_prize']); self.assertEqual(d['charge_money'], 1000)
        self.assertEqual(d['exchange_info'][1]['left_buy_count'], 6)
        self.assertEqual(d['exchange_info'][1]['plus_times'], 1)
        for index in range(1, 5): self.data(self.call(3, index=index))
        self.assertFalse(self.data(self.call())['had_prize'])
        self.assertEqual(self.amount(1142), 2); self.assertEqual(self.amount(1143), 2)
        before = self.b.profile(); self.charge()
        self.assertEqual(self.b.profile()['pavilion'], before['pavilion'])
        self.assertEqual(self.amount(1141), 1350)
        for index in range(1, 5): self.assertEqual(self.call(3, index=index)[0][0], 55)

    def test_locked_recharge_not_counted_or_backfilled_after_unlock(self):
        role = self.b.profile(); role['level'] = 29; self.b.save(role)
        before = self.b.profile()
        self.charge('locked-pavilion-order')
        locked = self.b.profile()
        self.assertEqual(locked['charge_gold'] - before['charge_gold'], 10000)
        self.assertGreater(locked['gold_coin'], before['gold_coin'])
        self.assertGreater(locked['vip_level'], before['vip_level'])
        self.assertEqual(locked['pavilion'], before['pavilion'])
        self.assertFalse(any(k.startswith('pavilion-charge-') for k in locked['welfare'].get('mails', {})))
        self.assertEqual(self.amount(1141), 0)

        locked['level'] = 30; self.b.save(locked)
        self.charge('locked-pavilion-order')  # Replaying the old order cannot grant bricks.
        self.assertEqual(self.b.profile()['pavilion'], before['pavilion'])
        self.charge('unlocked-pavilion-order', product=101)
        role = self.b.profile()
        self.assertEqual(role['pavilion']['charge_gold'], 100)
        self.assertEqual(role['pavilion']['bricks_earned'], 20)  # 10 RMB + first tier only.
        data = self.data(self.call())
        self.assertEqual(data['charge_money'], 10)
        self.assertEqual(data['exchange_info'][1]['left_buy_count'], 3)
        self.assertEqual(data['charge_info'][2]['state'], 1)  # Locked recharge adds no global progress.
        self.claim_mails(); self.assertEqual(self.amount(1141), 20)

    def test_locked_month_fund_and_bag_card_skip_pavilion_rewards(self):
        role = self.b.profile(); role['level'] = 29; self.b.save(role)
        before = self.b.profile()['pavilion']
        for product in (201, 202):
            self.charge(f'locked-product-{product}', product=product)
        role = self.b.profile()
        self.assertGreater(role['month_card_time'], NOW)
        self.assertEqual(role['buy_growup'], 1)
        card = next(i for i in role['attachments'] if i['type_id'] == 1152)
        self.req(1051, item_id=card['id'], item_type=1152, item_count=1,
                 des_type=1, des_id=role['role_id'])
        role = self.b.profile()
        self.assertEqual(role['charge_gold'], 1450)  # 50 + 45 + 50 RMB.
        self.assertEqual(role['pavilion'], before)
        self.assertFalse(any(k.startswith('pavilion-charge-') for k in role['welfare'].get('mails', {})))
        self.assertEqual(self.amount(1141), 0)

    def test_locked_fractional_principal_does_not_carry_into_unlock(self):
        role = self.b.profile(); role['level'] = 29
        before = copy.deepcopy(role)
        p.record_charge(role, 9, NOW)
        self.assertEqual(role, before)
        role['level'] = 30
        p.record_charge(role, 1, NOW)
        self.assertEqual(role['pavilion']['charge_gold'], 1)
        self.assertEqual(role['pavilion']['bricks_earned'], 0)

    def test_bad_inputs_locked_and_insufficient_atomic(self):
        for kw in (dict(flag=0),dict(flag=4),dict(flag=1,count=1),dict(flag=3,index=1),
                   dict(flag=2,index=99,count=1),dict(flag=2,index=1,count=0),
                   dict(flag=2,index=9,count=10000),dict(flag=2,index=1,count=1)):
            old = self.b.profile(); self.assertEqual(self.call(**kw)[0][0], 55)
            self.assertEqual(self.b.profile(), old)
        self.stock((1141, 300), (1143, 1))
        r = self.b.profile()
        for i in r['attachments']:
            if i['type_id']==1143:i['is_lock']=True
        self.b.save(r); old=self.b.profile()
        self.assertEqual(self.call(2,index=1,count=1,ten_card=1)[0][0],55)
        self.assertEqual(self.b.profile(),old)
        for i in r['attachments']:
            if i['type_id']==1141:i['is_lock']=True
        self.b.save(r); old=self.b.profile()
        self.assertEqual(self.call(2,index=1,count=1)[0][0],55)
        self.assertEqual(self.b.profile(),old)

    def test_ascension_next_unlock_hint_and_cap(self):
        # Native destinyUI L509-511 displays the NEXT increase only when
        # left_buy_count == 0, need_charge > 0 and plus_times > 0.
        self.stock((1141, 10000))
        self.data(self.call(2, index=1, count=3))
        row = self.data(self.call())['exchange_info'][1]
        self.assertEqual((row['left_buy_count'], row['need_charge'], row['plus_times']), (0, 300, 1))
        self.charge('unlock-one')  # 1000 RMB, three additional purchases
        self.data(self.call(2, index=1, count=3))
        row = self.data(self.call())['exchange_info'][1]
        self.assertEqual((row['left_buy_count'], row['need_charge'], row['plus_times']), (0, 200, 1))
        self.charge('unlock-two'); self.charge('unlock-three')
        self.data(self.call(2, index=1, count=7))
        row = self.data(self.call())['exchange_info'][1]
        self.assertEqual((row['left_buy_count'], row['need_charge'], row['plus_times']), (0, 0, 0))
        self.charge('beyond-cap')
        self.assertEqual(self.data(self.call())['exchange_info'][1]['left_buy_count'], 0)
        self.assertEqual(self.call(2, index=1, count=1)[0][0], 55)

    def test_fractional_principal_and_all_six_bonus_tiers(self):
        role = self.b.profile()
        p.record_charge(role, 9, NOW)
        self.assertEqual(role['pavilion']['bricks_earned'], 0)
        p.record_charge(role, 1, NOW)
        self.assertEqual(role['pavilion']['bricks_earned'], 1)
        p.record_charge(role, 49990, NOW)
        self.assertEqual(role['pavilion']['bricks_earned'], 6150)
        self.assertEqual(sum(m['prizes'][0][2] for k, m in role['welfare']['mails'].items()
                             if k.startswith('pavilion-charge-')), 6150)
        p.record_charge(role, 10, NOW)
        self.assertEqual(role['pavilion']['bricks_earned'], 6151)

    def test_restart_fortnight_rollover_mail_persists_and_clock_rollback(self):
        self.charge(); self.claim_mails(); self.data(self.call(2,index=2,count=1))
        self.data(self.call(3,index=1)); before=self.b.profile()
        self.b.close(); self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.b.profile(),before)
        end=before['pavilion']['end']
        with patch('network_redirect.backend.time.time',return_value=end):
            d=self.data(self.call())
            self.assertEqual(d['exchange_info'][2]['left_buy_count'],1)
            self.assertFalse(d['had_prize']); self.assertEqual(d['charge_money'],0)
            mails = self.b.profile()['welfare']['mails']
            self.assertTrue(all(mails[k] == v for k, v in before['welfare']['mails'].items()))
            refunds = [m for k, m in mails.items() if k.startswith('pavilion-recycle-')]
            self.assertEqual(len(refunds), 1)
            self.assertEqual(refunds[0]['prizes'], [[5, 1001, 1200, 1]])
            self.assertEqual(self.amount(1141), 0)
        before=self.b.profile(); self.assertEqual(self.call()[0][0],55)
        self.assertEqual(self.b.profile(),before)

    def test_actual_local_peer_contribution_and_period_isolation(self):
        peer=copy.deepcopy(self.b.profile()); peer['role_id']+=1
        p.record_charge(peer,10000,NOW)
        self.b.db.execute('INSERT INTO roles VALUES (?,?)',('pavilion-peer',json.dumps(peer)))
        self.b.db.commit()
        self.assertTrue(self.data(self.call())['had_prize'])
        self.data(self.call(3,index=4))
        self.assertEqual(self.b.profile()['pavilion']['charge_gold'],0)
        end=self.b.profile()['pavilion']['end']
        with patch('network_redirect.backend.time.time',return_value=end):
            self.assertFalse(self.data(self.call())['had_prize'])

    def refunds(self):
        return [m for k, m in self.b.profile()['welfare'].get('mails', {}).items()
                if k.startswith('pavilion-recycle-')]

    def test_exact_fortnight_boundary_resets_all_progress_and_reearns_bonuses(self):
        self.charge('first-period'); self.claim_mails()
        self.data(self.call(2, index=1, count=1))
        for i in range(1, 5): self.data(self.call(3, index=i))
        old = self.b.profile(); end = old['pavilion']['end']
        self.assertEqual(end - old['pavilion']['start'], 14 * 86400)
        with patch('network_redirect.backend.time.time', return_value=end - 1):
            self.assertEqual(self.data(self.call())['charge_money'], 1000)
        with patch('network_redirect.backend.time.time', return_value=end):
            d = self.data(self.call())
            self.assertEqual((d['begin_time'], d['end_time']), (end, end + 14 * 86400))
            self.assertEqual(d['charge_money'], 0)
            self.assertTrue(all(g['count'] == 0 and g['state'] == 1 for g in d['charge_info'].values()))
            self.assertEqual(d['exchange_info'][1]['left_buy_count'], 3)
            self.assertEqual(d['exchange_info'][1]['state'], 1)
            self.assertEqual(self.amount(1141), 0)
            self.assertEqual((self.amount(1142), self.amount(1143)), (2, 2))
            self.charge('first-period')  # A previous order must never count again.
            self.assertEqual(self.b.profile()['pavilion']['charge_gold'], 0)
            self.charge('second-period')
            self.assertEqual(self.b.profile()['pavilion']['bricks_earned'], 1350)
            self.data(self.call(3, index=4))
            self.claim_mails(); self.data(self.call(2, index=1, count=1))
            firsts = [k for k in self.b.profile()['welfare']['mails'] if k.startswith('pavilion-first-')]
            self.assertEqual(len(firsts), 2)
            self.assertEqual(len(self.refunds()), 1)
            self.assertEqual(self.refunds()[0]['prizes'], [[5, 1001, 1050, 1]])

    def test_unclaimed_mixed_mail_and_locked_bricks_recycled_once_after_offline_gap(self):
        from network_redirect import system_mail
        self.charge(); self.stock((1141, 7), (1142, 2))
        role = self.b.profile()
        for item in role['attachments']:
            if item['type_id'] == 1141: item['is_lock'] = True
        system_mail.deliver(role, key='mixed-bricks', title='混合附件', body='测试',
                            prizes=[[5, 1141, 3, 1], [5, 1001, 4, 1]], now=NOW, rules=self.b.welfare_rules)
        self.b.save(role)
        with patch('network_redirect.backend.time.time', return_value=role['pavilion']['end'] + 42 * 86400):
            self.data(self.call())
            refund = self.refunds()[0]
            self.assertEqual(refund['prizes'], [[5, 1001, 1360, 1]])
            self.assertIn('背包7个、未领取邮件1353个', refund['mail_body'])
            self.assertEqual(self.amount(1141), 0)
            mixed = self.b.profile()['welfare']['mails']['mixed-bricks']
            self.assertEqual(mixed['prizes'], [[5, 1001, 4, 1]])
            self.assertFalse(mixed['claimed'])
            self.ok(self.req(1103, mail_id=mixed['mail_id']))
            before_peaches = self.amount(1001)
            self.ok(self.req(1103, mail_id=refund['mail_id']))
            self.assertEqual(self.amount(1001), before_peaches + 1360)
            self.assertEqual(self.req(1103, mail_id=refund['mail_id'])[0][0], 55)
            self.data(self.call()); self.assertEqual(len(self.refunds()), 1)
            self.assertEqual(self.amount(1142), 2)

    def test_direct_old_mail_claim_at_boundary_cannot_restore_bricks(self):
        self.charge()
        role = self.b.profile()
        m = next(m for k, m in role['welfare']['mails'].items() if k.startswith('pavilion-charge-'))
        with patch('network_redirect.backend.time.time', return_value=role['pavilion']['end']):
            self.ok(self.req(1103, mail_id=m['mail_id']))
            self.assertEqual(self.amount(1141), 0)
            self.assertEqual(self.b.profile()['pavilion']['charge_gold'], 0)
            self.assertEqual(self.refunds()[0]['prizes'], [[5, 1001, 1350, 1]])

    def test_mail_read_and_heartbeat_refresh_without_opening_pavilion(self):
        self.charge()
        role = self.b.profile(); end = role['pavilion']['end']
        m = next(m for k, m in role['welfare']['mails'].items() if k.startswith('pavilion-charge-'))
        with patch('network_redirect.backend.time.time', return_value=end):
            events = self.req(1102, mail_id=m['mail_id'], flag=0)
            self.ok(events)
            self.assertEqual(next(d for e, d in events if e == 14)['attach_count'], 0)
            self.assertEqual(len(self.refunds()), 1)
            self.stock((1141, 9))
        with patch('network_redirect.backend.time.time', return_value=end + 14 * 86400):
            replies = self.b.respond(encode(2999, {}), self.state)
            self.assertEqual(decode(replies[0])[0], 2999)
            self.assertEqual(self.amount(1141), 0)
            self.assertEqual(len(self.refunds()), 2)
            self.assertEqual(self.b.profile()['pavilion']['start'], end + 14 * 86400)

    def test_recharge_at_boundary_settles_old_mail_before_new_principal(self):
        self.charge('period-old')
        end = self.b.profile()['pavilion']['end']
        with patch('network_redirect.backend.time.time', return_value=end):
            self.charge('period-new')
            self.assertEqual(self.b.profile()['pavilion']['charge_gold'], 10000)
            self.assertEqual(self.b.profile()['pavilion']['bricks_earned'], 1350)
            self.assertEqual(self.refunds()[0]['prizes'], [[5, 1001, 1350, 1]])
            self.claim_mails(); self.assertEqual(self.amount(1141), 1350)

    def test_legacy_week_migration_same_start_or_second_week_and_peer_isolation(self):
        r = p.load_rules(); start, end = p.period(NOW, r)
        for offset in (0, 7 * 86400):
            with self.subTest(offset=offset):
                role = self.b.profile()
                role['pavilion'] = dict(start=start+offset, end=start+offset+7*86400,
                    clock=start+offset, charge_gold=100, bricks_earned=20, bought={'9': 1}, claimed=[1])
                p.mail(role, f'pavilion-charge-{start+offset}-100', '天机阁充值金砖', [[5, 1141, 20, 1]], start+offset)
                peer = copy.deepcopy(role)
                data = p.catalog(role, NOW, r, [peer])
                self.assertFalse(data['had_prize'])
                self.assertEqual(data['charge_money'], 0)
                self.assertEqual((data['begin_time'], data['end_time']), (start, end))
                p.record_charge(role, 100, NOW)
                self.assertEqual(role['pavilion']['bricks_earned'], 20)
                mails = role['welfare']['mails']
                self.assertTrue(mails[f'pavilion-charge-{start+offset}-100']['claimed'])
                self.assertFalse(mails[f'pavilion-charge-{start}-{end}-100']['claimed'])

    def test_rollover_mail_and_encoding_failure_leave_no_partial_conversion(self):
        self.charge(); self.stock((1141, 10))
        old = self.b.profile()
        with patch('network_redirect.backend.time.time', return_value=old['pavilion']['end']):
            old = self.b.profile()  # Unrelated achievement daily migration precedes the transaction.
            with patch.object(p, 'mail', side_effect=formation.Rejected('mail failed')):
                self.assertEqual(self.call()[0][0], 55)
            self.assertEqual(self.b.profile(), old)
            with patch('network_redirect.backend.activity.attributes', side_effect=ValueError('encode failed')):
                self.assertEqual(self.call()[0][0], 55)
            self.assertEqual(self.b.profile(), old)
            self.data(self.call())
            self.assertEqual(self.refunds()[0]['prizes'], [[5, 1001, 1360, 1]])

    def test_empty_rollover_does_not_send_empty_refund(self):
        role = self.b.profile()
        with patch('network_redirect.backend.time.time', return_value=role['pavilion']['end']):
            self.data(self.call())
            self.assertFalse(self.refunds())

    def test_encoding_and_mail_failure_roll_back_resources(self):
        self.stock((1141,500))
        old=self.b.profile()
        with patch('network_redirect.activity_pavilion.mail', side_effect=formation.Rejected('mail failed')):
            self.assertEqual(self.call(2,index=1,count=1)[0][0],55)
        self.assertEqual(old,self.b.profile())
        with patch('network_redirect.backend.activity.attributes',side_effect=ValueError('encode failed')):
            self.assertEqual(self.call(2,index=1,count=1)[0][0],55)
        self.assertEqual(old,self.b.profile())

    def test_disabled_and_invalid_config(self):
        r=p.load_rules()
        with patch.object(p,'load_rules',return_value=dict(r,enabled=False)):
            self.assertFalse(p.status(self.b.profile(),NOW)['end_time'])
            self.assertEqual(self.call()[0][0],55)
        for key,value in [('gold_per_rmb',0),('enabled',1),('mode','official'),('period_days',True),('batch_limit',10000)]:
            with tempfile.TemporaryDirectory() as tmp:
                path=Path(tmp)/'bad.json'; path.write_text(json.dumps(dict(r,**{key:value})))
                with self.assertRaises(formation.Rejected):p.load_rules(path)


if __name__=='__main__': unittest.main()
