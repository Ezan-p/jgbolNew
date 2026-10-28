"""Exchange counts are transactions, independent of the 40-shard prize."""
import copy
import unittest
from pathlib import Path
from unittest.mock import patch

from tests import test_equipment_crafting as crafting
from network_redirect import equipment_crafting as c, market, formation as f, summon
from network_redirect.backend import Backend

class ExchangeTests(unittest.TestCase):
    setUp = crafting.CraftingTests.setUp
    add = crafting.CraftingTests.add
    gear = crafting.CraftingTests.gear
    get = crafting.CraftingTests.get
    req = crafting.CraftingTests.req
    compose = crafting.CraftingTests.compose

    def materials(self):
        return [self.gear(quality=4) for _ in range(5)]

    def test_exchange_level_30_preserves_materials_below_threshold(self):
        self.add(1008, count=2)
        with patch.object(c.time, 'time', return_value=1793016000) as clock:
            for op, target in ((2, 2001), (3, 6001)):
                ids = self.materials()
                role = self.b.profile(); role['level'] = 29; self.b.save(role)
                before = self.b.profile()
                result = self.compose(ids[0], op, target, ids)[-1]
                self.assertEqual(result, (55, {'op_string': '装备兑换需角色30级开放'}))
                self.assertEqual(before, self.b.profile())
                role = self.b.profile(); role['level'] = 30; self.b.save(role)
                self.assertEqual(self.compose(ids[0], op, target, ids)[-1][0], 6)
                clock.return_value += c.WEEK

    def test_ordinary_fragment_compose_still_opens_at_level_5(self):
        item = self.add(6001, count=40)
        role = self.b.profile(); role['level'] = 5; self.b.save(role)
        self.assertEqual(self.compose(item)[-1][0], 6)

    def test_weekly_transactions_four_targets_replay_and_reconnect(self):
        now = 1793016000  # 2026-10-26, within the first fixture week.
        with patch.object(c.time, 'time', return_value=now) as clock:
            for week, tid in enumerate((6001, 6002, 6003, 6004)):
                clock.return_value = now + week*c.WEEK
                ids = self.materials()
                result = self.compose(ids[0], 3, tid, ids)[-1]
                self.assertEqual(result[0], 6)
                self.assertEqual(result[1]['count'], 40)
                snapshot = result[1]['equip_compose']
                self.assertEqual(snapshot['weekly_remaining'], 0)
                self.assertEqual(snapshot['exchange']['exchanged_count'], 1)
                self.assertIn('1/1', result[1]['exchange_notice'])
                self.assertIn('北京时间', result[1]['exchange_notice'])
                before = self.b.profile()
                self.assertEqual(self.b.respond(self.packet, {'authenticated': True}), self.replies)
                self.assertEqual(before, self.b.profile())
                self.assertFalse(any(i['id'] in ids for i in before['attachments']))
                extra = self.materials(); before = self.b.profile()
                self.assertEqual(self.compose(extra[0], 3, tid, extra)[-1][0], 55)
                self.assertEqual(before, self.b.profile())
            self.b.close();self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
            snapshot = self.req(1055, flag=0)[-1][1]['equip_compose']
            self.assertEqual(snapshot['weekly_remaining'], 0)

    def test_shared_limit_both_directions_and_same_equipment_next_week(self):
        with patch.object(c.time, 'time', return_value=1793016000) as clock:
            self.add(1008,count=5)
            for op, target in ((2,2001),(3,6001),(2,2001)):
                ids=self.materials()
                self.assertEqual(self.compose(ids[0],op,target,ids)[-1][0],6)
                ids=self.materials()
                for other,target2 in ((2,2001),(2,2002),(3,6001),(3,6004)):
                    before=self.b.profile()
                    result=self.compose(ids[0],other,target2,ids)[-1]
                    self.assertEqual(result[0],55)
                    self.assertIn('1/1',result[1]['op_string'])
                    self.assertEqual(before,self.b.profile())
                clock.return_value+=c.WEEK

    def test_monday_boundary_offline_and_clock_rollback(self):
        from datetime import datetime, timezone
        monday=int(datetime(2026,10,25,16,tzinfo=timezone.utc).timestamp())
        with patch.object(c.time,'time',return_value=monday-1) as clock:
            self.add(1008,count=3);ids=self.materials()
            self.assertEqual(self.compose(ids[0],2,2001,ids)[-1][0],6)
            prior=self.req(1055,flag=1)[-1][1]['equip_compose']
            self.assertEqual(prior['weekly_reset_at'],monday)
            self.assertEqual(prior['weekly_remaining'],0)
            clock.return_value=monday
            refreshed=self.req(1055,flag=1)[-1][1]['equip_compose']
            self.assertEqual(refreshed['weekly_remaining'],1)
            self.assertTrue(all(r['flag']==0 for r in refreshed['appoint'].values()))
            ids=self.materials();self.assertEqual(self.compose(ids[0],2,2001,ids)[-1][0],6)
            clock.return_value=monday-1
            self.assertEqual(self.req(1055,flag=1)[-1][1]['equip_compose']['weekly_remaining'],0)
            clock.return_value=monday+5*c.WEEK
            refreshed=self.req(1055,flag=1)[-1][1]['equip_compose']
            self.assertEqual(refreshed['weekly_remaining'],1)  # no accrued five-week credit
            self.assertEqual(refreshed['weekly_reset_at'],monday+6*c.WEEK)

    def test_legacy_migration_once_and_regular_fragment_compose_not_limited(self):
        role=self.b.profile();role['equipment_forge']=dict(appointed=['2001'],exchanged=10);self.b.save(role)
        self.assertEqual(self.req(1055,flag=0)[-1][1]['equip_compose']['weekly_remaining'],1)
        self.assertEqual(self.b.profile()['equipment_forge']['legacy'],dict(appointed=['2001'],exchanged=10))
        ids=self.materials();self.assertEqual(self.compose(ids[0],3,6002,ids)[-1][0],6)
        shard=next(i['id'] for i in self.b.profile()['attachments'] if i['type_id']==6002)
        self.assertEqual(self.compose(shard)[-1][0],6)
        self.assertEqual(self.req(1055,flag=0)[-1][1]['equip_compose']['weekly_remaining'],0)

    def test_invalid_materials_do_not_charge_token_or_count(self):
        self.add(1008, count=20)
        ids = self.materials()
        for field in ('is_lock', 'equip_order', 'owner_id', 'innate_owner_id', 'protogenic',
                      'advance_level', 'star_count', 'cur_spirit_count', 'reborn_bit', 'star_level'):
            original = self.b.profile();changed = copy.deepcopy(original)
            next(i for i in changed['attachments'] if i['id'] == ids[-1])[field] = 2
            self.b.save(changed)
            for op, tid in ((2, 2001), (3, 6002)):
                before = self.b.profile()
                self.assertEqual(self.compose(ids[0], op, tid, ids)[-1][0], 55, field)
                self.assertEqual(before, self.b.profile(), field)
            self.b.save(original)
        for selected in (ids[:4], ids+[ids[0]], [ids[0]]*5, ids[:4]+[99999999]):
            before = self.b.profile()
            self.assertEqual(self.compose(ids[0], 3, 6001, selected)[-1][0], 55)
            self.assertEqual(before, self.b.profile())
        talisman = self.gear(main=3,quality=4)
        before = self.b.profile()
        self.assertEqual(self.compose(ids[0],3,6001,ids[:4]+[talisman])[-1][0],55)
        self.assertEqual(before,self.b.profile())

    def test_original_enhanced_materials_are_consumed_without_silver_refund(self):
        ids=[self.gear(quality=4,level=20) for _ in range(5)]
        before=self.b.profile()['silver_coin']
        result=self.compose(ids[0],3,6001,ids)[-1]
        self.assertEqual(result[0],6)
        self.assertEqual(self.b.profile()['silver_coin'],before)
        self.assertFalse(any(i['id'] in ids for i in self.b.profile()['attachments']))

    def test_result_encoding_failure_rolls_back_inventory_token_and_quota(self):
        self.add(1008);ids=self.materials()
        native=summon.event
        def fail_result(eid,data):
            if eid==6:raise ValueError('simulated result encoding failure')
            return native(eid,data)
        for op,tid in ((2,2001),(3,6001)):
            before=self.b.profile()
            with patch.object(summon,'event',side_effect=fail_result):
                self.assertEqual(self.compose(ids[0],op,tid,ids)[-1][0],55)
            self.assertEqual(before,self.b.profile())

    def test_all_offered_equipment_and_original_token_mapping(self):
        rules = c.load_rules();role = self.b.profile()
        offers = c.compose_list(role, rules)['equip_compose']['appoint']
        self.assertGreater(len(offers), 3)
        for offer in offers:
            tid = offer['material_type'];cfg = f.ITEMS[tid]
            role = copy.deepcopy(self.b.profile())
            token = (1007 if int(cfg['quality']) == 5 else 1010) + int(cfg['main_type'])
            role['attachments'] = [dict(id=n,attach_type=5,type_id=next(t for t,r in f.ITEMS.items()
                if r['quality']=='4' and r['main_type']=='1'),count=1,level=1) for n in range(1,6)]
            role['attachments'].append(dict(id=6,attach_type=5,type_id=token,count=1,level=1))
            result=c.compose(role,dict(compose_type=2,equip_type=tid,equip_quality=int(cfg['quality']),
                material_quality=4,material_count=5,material_list=[dict(id=i) for i in range(1,6)]),rules)[0][1]
            self.assertEqual(result['equip_type'],tid)
            self.assertFalse(any(i['type_id']==token for i in role['attachments']))
            self.assertEqual(next(r for r in result['equip_compose']['appoint'] if r['material_type']==tid)['flag'],1)

    def test_market_tokens_use_original_prices_and_purchase_path(self):
        role=self.b.profile();rules=market.load_rules();now=1793073600
        goods=market.catalog(role,now,rules)['rich_item_list']
        rows=[r for r in goods.values() if r['type_id'] in range(1008,1014)]
        self.assertEqual({r['type_id']:r['buy_price'] for r in rows},
                         {1008:1500,1009:1500,1010:2000,1011:200,1012:200,1013:500})
        role['gold_coin']=10000
        for row in rows:
            before=role['gold_coin']
            market.buy(role,dict(page_id=2,index=row['index'],type_id=row['type_id'],count=1),now,rules)
            self.assertEqual(before-role['gold_coin'],row['buy_price'])

    def test_low_level_and_missing_token_are_atomic(self):
        ids=self.materials();before=self.b.profile()
        self.assertEqual(self.compose(ids[0],2,2001,ids)[-1][0],55)
        self.assertEqual(before,self.b.profile())
        role=self.b.profile();role['level']=4;self.b.save(role);before=self.b.profile()
        self.assertEqual(self.compose(ids[0],3,6001,ids)[-1][0],55)
        self.assertEqual(before,self.b.profile())
