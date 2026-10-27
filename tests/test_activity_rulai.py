"""Rulai native wire contracts, recharge accounting, wheel and selectable bags."""
from recharge_helpers import funded_order
from collections import Counter
import json
from pathlib import Path
from unittest.mock import patch

from test_activity import ActivityCase, NOW
from network_redirect import activity_rulai as r, formation, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode, encode


class RulaiTests(ActivityCase):
    def call(self, op=0, data='{}'):
        return self.req(1351, id=op, data=data)

    def result(self, events):
        self.ok(events)
        return next(d for e, d in events if e == 200)

    def charge(self, product=1, order=None):
        events = self.req(1111, event_id=251, data=funded_order(self.b, product, order or f'rulai-{self.serial}'))
        self.assertTrue(any(e == 80 and 'local_vip' in d for e,d in events))

    def amount(self, tid):
        return sum(i['count'] for i in self.b.profile()['attachments'] if i['attach_type'] == 5 and i['type_id'] == tid)

    def test_original_contract_bootstrap_and_initial_no_free_draw(self):
        d = self.result(self.call())['pack_data']
        self.assertEqual(d['cur_count'], 0)
        self.assertEqual(d['order_pay'], 0)
        self.assertEqual(len(d['random_table']), 8)
        expected = [(1246, 3), (1031, 3), (6005, 5), (6004, 5),
                    (1249, 10), (1015, 5), (1367, 1), (1368, 1)]
        self.assertEqual([(p['attach_type'], p['attach_count'])
                          for p in d['random_table'].values()], expected)
        self.assertEqual(d['ext_info']['prize_flag'], 1)
        packets = [v for m, _, v in map(decode, self.b.bootstrap()) if m == 2998]
        schedule = next(login_fields(v['data'])[73][1] for v in packets if v['id'] == 113)
        self.assertLess(schedule['start_time'], NOW)
        self.assertGreater(schedule['end_time'], NOW)
        self.assertEqual(self.call(1)[0][0], 55)
        self.assertEqual(self.call(2)[0][0], 55)
        self.ok(self.req(1205, flag=0))

    def test_split_recharge_base_gold_and_repeat_order(self):
        for i in range(3):
            self.charge(1)
            d = self.result(self.call())['pack_data']
            self.assertEqual((d['order_pay'], d['cur_count']), ((i + 1) * 10, (i + 1) // 3))
        self.charge(2, 'same-order');before = self.b.profile()
        self.charge(2, 'same-order');self.assertEqual(before, self.b.profile())
        self.assertEqual(self.result(self.call())['pack_data']['cur_count'], 2)

    def test_all_eight_results_match_inventory_and_consume_one_chance(self):
        self.charge(4)
        cfg = r.load_rules();gold = self.b.profile()['gold_coin']
        for index, row in enumerate(cfg['pool'], 1):
            tid, n = row['reward'][1:3];before = self.amount(tid)
            with patch.object(r, 'draw', return_value=index):
                d = self.result(self.call(1))
            self.assertEqual(d['prize_index'], index)
            self.assertEqual(self.amount(tid) - before, n)
            self.assertEqual(d['prize_list'][1], dict(object_type=5, attach_type=tid,
                                                    attach_count=n, attach_level=1))
        self.assertEqual(self.b.profile()['activity']['rulai']['draws'], 8)
        self.assertEqual(self.b.profile()['gold_coin'], gold)

    def test_weight_boundaries(self):
        cfg = r.load_rules();offset = 0
        for i, row in enumerate(cfg['pool'], 1):
            for pick in (offset, offset + row['weight'] - 1):
                with patch.object(r.secrets, 'randbelow', return_value=pick):
                    self.assertEqual(r.draw(cfg), i)
            offset += row['weight']
        self.assertEqual(offset, 10000)
        # Exhaust the random integer domain: verify exact probabilities, not a
        # flaky random sample or just the configured weight values.
        with patch.object(r.secrets, 'randbelow', side_effect=range(offset)):
            counts = Counter(r.draw(cfg) for _ in range(offset))
        self.assertEqual(counts, dict(enumerate([1000, 2000, 1800, 1500, 1000, 2200, 400, 100], 1)))

    def test_replacement_rewards_can_be_used_and_fragments_composed(self):
        self.charge(4)
        self.charge(4)
        def win(index, times=1):
            with patch.object(r, 'draw', return_value=index):
                for _ in range(times):
                    self.result(self.call(1))
        def item(tid):
            return next(i for i in self.b.profile()['attachments']
                        if i['attach_type'] == 5 and i['type_id'] == tid)

        win(1)
        before = self.amount(1246)
        self.ok(self.req(1051, item_type=1246, item_id=item(1246)['id'], item_count=1,
                         des_type=5, des_id=5001))
        self.assertEqual(self.amount(1246), before - 1)
        win(2)
        before = self.amount(1031)
        self.ok(self.req(1051, item_type=1031, item_id=item(1031)['id'], item_count=1,
                         des_type=1, des_id=0))
        self.assertEqual(self.amount(1031), before - 1)

        role = self.b.profile()
        role.update(level=60, silver_coin=2000000)
        self.b.save(role)
        for index, tid, kind in ((3, 6005, 6), (4, 6004, 5)):
            before = self.amount(tid)
            win(index, 8)
            self.assertEqual(self.amount(tid) - before, 40)
            shard = item(tid)
            cfg = formation.ITEMS[tid]
            events = self.req(1053, compose_type=1, equip_type=int(cfg['sub_type']),
                              equip_quality=5, material_quality=5, material_count=1,
                              material_list=[dict(id=shard['id'])])
            self.ok(events)
            prize = next(d for e, d in events if e == 6)
            self.assertEqual(self.amount(tid), before)
            catalog = formation.SKILLS if kind == 6 else formation.ITEMS
            result = catalog[prize['equip_type']]
            self.assertEqual(result['quality'], '5')
            if kind == 6:
                self.assertEqual(result['use_mode(1-active，2-passive)'], '2')
            else:
                self.assertEqual(result['main_type'], '3')

    def test_recharge_at_exact_period_boundary_counts_in_new_period(self):
        cfg = r.load_rules()
        start, end = r.period(NOW, cfg)
        role = self.b.profile()
        r.record_charge(role, 500, start)
        self.assertEqual(role['activity']['rulai']['charge_gold'], 500)
        r.record_charge(role, 100, end)
        self.assertEqual(role['activity']['rulai']['start'], end)
        self.assertEqual(role['activity']['rulai']['charge_gold'], 100)

    def test_bonus_claim_once_independent_of_draws(self):
        self.charge(4)
        d = self.result(self.call())['pack_data']
        self.assertEqual(d['ext_info']['prize_flag'], 2)
        n = self.amount(1368);count = d['cur_count']
        self.result(self.call(2));self.assertEqual(self.amount(1368), n + 1)
        self.assertEqual(self.result(self.call())['pack_data']['cur_count'], count)
        self.assertEqual(self.result(self.call())['pack_data']['ext_info']['prize_flag'], 3)
        before = self.b.profile();self.assertEqual(self.call(2)[0][0], 55)
        self.assertEqual(before, self.b.profile())

    def test_every_official_bag_choice_and_batch(self):
        self.assertEqual(r.BAGS, {1367: {(10,5053):5,(5,1249):50},1368:{(10,5053):20,(5,1249):200}})
        for tid, choices in r.BAGS.items():
            for (typ, target), ratio in choices.items():
                role = self.b.profile();summon.add_item(role, tid, 2);self.b.save(role)
                item = next(i for i in role['attachments'] if i['type_id'] == tid)
                before = self.amount(1249) if typ == 5 else role.get('souls', {}).get('5053', 0)
                self.ok(self.req(1051, item_type=tid, item_id=item['id'], item_count=2, des_type=typ, des_id=target))
                after = self.amount(1249) if typ == 5 else self.b.profile()['souls']['5053']
                self.assertEqual(after - before, 2 * ratio)
                self.assertEqual(self.amount(tid), 0)

    def test_bad_parameters_and_atomic_failures(self):
        for op, data in [(3,'{}'),(255,'{}'),(1,'{prize_index=8}'),(0,'invalid'),(0,'{gold=999}')]:
            before = self.b.profile();self.assertEqual(self.call(op,data)[0][0], 55)
            self.assertEqual(before, self.b.profile())
        self.charge(2);before = self.b.profile()
        with patch('network_redirect.backend.activity.attributes', side_effect=ValueError('encode failure')):
            self.assertEqual(self.call(1)[0][0], 55)
        self.assertEqual(before, self.b.profile())

    def test_selected_bag_stack_locks_target_and_quantity(self):
        role = self.b.profile();summon.add_item(role, 1367, 3)
        first = next(i for i in role['attachments'] if i['type_id'] == 1367)
        second = dict(first, id=formation.new_id(role), count=2)
        role['attachments'].append(second);self.b.save(role)
        request = dict(item_type=1367,item_id=second['id'],item_count=1,des_type=10,des_id=5053)
        for changes in (dict(item_count=0),dict(item_count=16),dict(item_count=3),dict(des_type=4),dict(des_id=5046),dict(item_type=1368)):
            before = self.b.profile();self.assertEqual(self.req(1051,**dict(request,**changes))[0][0],55)
            self.assertEqual(before,self.b.profile())
        for flag in ('is_lock','owner_id','equip_pos'):
            role=self.b.profile();next(i for i in role['attachments'] if i['id']==second['id'])[flag]=1;self.b.save(role)
            before=self.b.profile();self.assertEqual(self.req(1051,**request)[0][0],55);self.assertEqual(before,self.b.profile())
            role=self.b.profile();next(i for i in role['attachments'] if i['id']==second['id'])[flag]=0;self.b.save(role)
        self.ok(self.req(1051,**request))
        counts={i['id']:i['count'] for i in self.b.profile()['attachments'] if i['type_id']==1367}
        self.assertEqual(counts,{first['id']:3,second['id']:1})

    def test_replay_reconnect_and_durable_state(self):
        self.charge(2);self.result(self.call(1));before=self.b.profile()
        self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
        self.assertEqual(before,self.b.profile())
        forged=encode(1351,dict(serial_num=self.serial,id=2,data='{}'))
        self.assertEqual(decode(self.b.respond(forged,self.state)[0])[2]['id'],55)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(before,self.b.profile())
        self.assertEqual(self.result(self.call())['pack_data']['cur_count'],0)

    def test_cross_day_season_reset_disabled_bags_and_clock_rollback(self):
        self.charge(4);self.result(self.call(2));before=self.b.profile()
        with patch('network_redirect.backend.time.time',return_value=NOW-1):
            self.assertEqual(self.call(1)[0][0],55)
        self.assertEqual(before,self.b.profile())
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            self.assertEqual(self.result(self.call())['pack_data']['cur_count'],16)
        end=self.b.profile()['activity']['rulai']['end']
        with patch('network_redirect.backend.time.time',return_value=end+1):
            d=self.result(self.call())['pack_data'];self.assertEqual((d['cur_count'],d['order_pay']),(0,0))
            self.assertEqual(d['ext_info']['prize_flag'],1)
        role=self.b.profile();bag=next(i for i in role['attachments'] if i['type_id']==1368)
        cfg=r.load_rules();cfg['enabled']=False
        with patch.object(r,'load_rules',return_value=cfg):
            self.assertEqual(self.call()[0][0],55)
            self.ok(self.req(1051,item_type=1368,item_id=bag['id'],item_count=1,des_type=10,des_id=5053))
            self.assertEqual(r.schedule(NOW,cfg),[dict(start_time=0,end_time=0)])

    def test_invalid_configuration(self):
        for key,value in [('mode','official'),('enabled',1),('period_days',0),('pool',[]),('bonus',[]),('rmb_per_draw',True)]:
            cfg=r.load_rules();cfg[key]=value
            p=Path(self.tmp.name)/'bad.json';p.write_text(json.dumps(cfg))
            with self.assertRaises(formation.Rejected):r.load_rules(p)

    def test_two_big_bags_compose_original_rulai_and_innate_spell(self):
        role=self.b.profile();summon.add_item(role,1368,2);self.b.save(role)
        bag=next(i for i in role['attachments'] if i['type_id']==1368)
        self.ok(self.req(1051,item_type=1368,item_id=bag['id'],item_count=2,des_type=10,des_id=5053))
        self.ok(self.req(1083,type_id=5053))
        role=self.b.profile();god=next(c for c in role['corteges'] if c['type']==5053)
        self.assertEqual(role['souls']['5053'],0)
        self.assertTrue(any(i.get('innate_owner_id')==god['id'] for i in role['attachments']))
        self.assertEqual(self.req(1083,type_id=5053)[0][0],55)

    def test_heartbeat_rollover_and_account_isolation(self):
        self.charge(2);start,end=r.period(NOW,r.load_rules())
        other=Backend(Path(self.tmp.name),18770,lambda *a,**k:None,account='another-rulai-player')
        try:
            self.assertEqual(r.state(other.profile(),NOW,r.load_rules())['charge_gold'],0)
        finally:other.close()
        with patch('network_redirect.backend.time.time',return_value=end+1):
            packets=self.b.respond(encode(2999,{}),self.state)
            updates=[login_fields(d['data']) for mid,_,d in map(decode,packets) if mid==2998 and d['id']==80]
            current=next(d['local_rulai'] for d in updates if 'local_rulai' in d)
            self.assertEqual(current['times'][1]['start_time'],end)
            self.assertEqual(current['pack_data']['cur_count'],0)
        self.assertEqual(self.b.profile()['activity']['rulai']['start'],end)
