"""Fixed plus weighted pet-shop listings, limits and save migration."""
import copy
import unittest
from fractions import Fraction
from itertools import permutations
from pathlib import Path
from unittest.mock import patch

from network_redirect import guild, guild_hunt, guild_offline, summon
from network_redirect.backend import Backend
from network_redirect.protocol import encode
from tests.test_guild_activity_fixes import GuildActivityFixTests


class GuildPetShopTests(unittest.TestCase):
    legacy_setup=GuildActivityFixTests.setUp
    req=GuildActivityFixTests.req

    def setUp(self):
        self.legacy_setup()
        with patch.object(guild_offline,'roll',return_value=0):self.req(91,two_type=1)
        role=self.b.profile()
        role['guild']['instances'].update(reputation=10000,total_reputation=1000)
        self.b.save(role)

    def item_count(self,tid):
        return sum(p['count'] for p in self.b.profile()['attachments'] if p['attach_type']==5 and p['type_id']==tid)

    def test_every_offer_charges_and_grants_advertised_batch(self):
        expected={1338:(1,20,13),1339:(1,40,13),1340:(1,60,13),1341:(1,100,13),
                  1345:(5,20,3),1347:(1,40,5),1348:(1,60,5),1349:(1,100,5),1346:(1,60,1)}
        seen=set()
        for day in range(2):
            if day:self.now+=86400
            with patch.object(guild_offline,'roll',side_effect=lambda s,n:n-1):offers=self.req(91,two_type=1)[0]['item_list']
            self.assertEqual(len(offers),6)
            self.assertEqual([offers[i]['item']['attach_type'] for i in (1,2,3)],[1338,1339,1345])
            for index,offer in offers.items():
                before=self.b.profile();tid=offer['item']['attach_type'];count=self.item_count(tid);seen.add(tid)
                self.assertEqual((offer['item']['attach_count'],offer['buy_reputation'],offer['left_times']),expected[tid])
                n=offer['left_times'];response=self.req(91,two_type=2,index=index,buy_count=n)[0]
                after=self.b.profile()
                self.assertEqual(after['guild']['instances']['reputation'],before['guild']['instances']['reputation']-offer['buy_reputation']*n)
                self.assertEqual(self.item_count(tid),count+offer['item']['attach_count']*n)
                self.assertEqual(response['cur_reputation'],after['guild']['instances']['reputation'])
                self.assertEqual(response['buy_item']['buy_reputation'],offer['buy_reputation'])
                self.assertEqual(response['buy_item']['left_times'],0)
                self.assertEqual(after['guild']['instances']['total_reputation'],1000)
                self.req(91,ok=False,two_type=2,index=index,buy_count=1)
                self.assertEqual(self.b.profile(),after)
        self.assertEqual(seen,set(expected))

    def test_integer_lua_numbers_and_duplicate_packet(self):
        before=self.item_count(1345);self.serial+=1
        packet=encode(1301,dict(serial_num=self.serial,id=91,data=summon.lua(dict(two_type=2,index=3.0,buy_count=3.0))))
        response=self.b.respond(packet,{'authenticated':True});after=self.b.profile()
        self.assertEqual(after['guild']['instances']['reputation'],9940)
        self.assertEqual(self.item_count(1345),before+15)
        self.assertEqual(self.b.respond(packet,{'authenticated':True}),response)
        self.assertEqual(self.b.profile(),after)
        self.assertEqual(self.req(91,two_type=1)[0]['item_list'][3]['left_times'],0)

    def test_invalid_parameters_unlock_balance_and_stock_are_atomic(self):
        for key,values in (('index',(True,0,-1,1.5,7,'3')),('buy_count',(True,0,-1,1.5,2147483648,'4'))):
            for value in values:
                with self.subTest(key=key,value=value):
                    args=dict(two_type=2,index=1,buy_count=1);args[key]=value
                    before=self.b.profile();self.req(91,ok=False,**args)
                    self.assertEqual(self.b.profile(),before)
        for reputation,total,index,count in ((1000,0,2,1),(39,1000,2,1),(1000,1000,1,14),(1000,100000,3,4),(1000,100000,6,6)):
            role=self.b.profile();role['guild']['instances'].update(reputation=reputation,total_reputation=total);self.b.save(role)
            before=self.b.profile();self.req(91,ok=False,two_type=2,index=index,buy_count=count)
            self.assertEqual(self.b.profile(),before)

    def test_daily_list_and_purchases_survive_restart_and_refresh(self):
        self.req(91,two_type=2,index=3,buy_count=2);old=self.req(91,two_type=1)[0]
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        with patch.object(guild_offline,'roll',side_effect=AssertionError('same day reroll')):
            self.assertEqual(self.req(91,two_type=1)[0],old)
            self.now=self.req(83)[0]['task_last_time']-1
            self.assertEqual(self.req(91,two_type=1)[0],old)
        self.now+=1
        before=self.b.profile();self.req(91,ok=False,two_type=2,index=3,buy_count=1)
        self.assertEqual(self.b.profile(),before)
        with patch.object(guild_offline,'roll',side_effect=lambda s,n:n-1):new=self.req(91,two_type=1)[0]
        self.assertEqual([o['item']['attach_type'] for o in new['item_list'].values()],[1338,1339,1345,1348,1349,1346])
        self.assertEqual(new['item_list'][3]['left_times'],3)
        self.assertEqual(new['cur_reputation'],9960)
        self.req(91,ok=False,two_type=2,index=1,buy_count=1,shop_day=old['shop_day'])
        self.req(91,ok=False,two_type=2,index=7,buy_count=1)

    def test_all_weighted_paths_and_ticket_boundaries(self):
        rules=guild.load_rules();weights={1340:25,1341:10,1347:25,1348:20,1349:5,1346:15}
        probabilities={tid:Fraction(0) for tid in weights}
        for chosen in permutations(weights,3):
            remaining=dict(weights);low=[];high=[];totals=[];prob=Fraction(1)
            for tid in chosen:
                total=sum(remaining.values());start=sum(w for k,w in remaining.items() if list(remaining).index(k)<list(remaining).index(tid))
                low.append(start);high.append(start+remaining[tid]-1);totals.append(total)
                prob*=Fraction(remaining.pop(tid),total)
            for tid in chosen:probabilities[tid]+=prob
            for tickets in (low,high):
                a=dict(day=1,shop_bought={},reputation=0)
                with patch.object(guild_offline,'roll',side_effect=tickets) as rng:
                    guild_hunt.prepare_shop(a,{},rules)
                self.assertEqual([call.args[1] for call in rng.call_args_list],totals)
                listed=[o['item']['attach_type'] for o in guild_hunt.shop(a,rules)['item_list']]
                self.assertEqual(listed[:3],[1338,1339,1345])
                self.assertEqual(set(listed[3:]),set(chosen));self.assertEqual(len(set(listed)),6)
        self.assertEqual(sum(probabilities.values()),3)
        self.assertEqual([round(float(p)*100,4) for p in probabilities.values()],[68.5353,35.1133,68.5353,60.1313,18.6712,49.0137])

    def test_random_row_maps_to_box_and_box_limit_is_one(self):
        self.now+=86400
        with patch.object(guild_offline,'roll',side_effect=lambda s,n:n-1):offers=self.req(91,two_type=1)[0]['item_list']
        self.assertEqual(offers[6]['item']['attach_type'],1346)
        before=self.item_count(1346);self.req(91,two_type=2,index=6,buy_count=1)
        self.assertEqual(self.item_count(1346),before+1)
        after=self.b.profile();self.req(91,ok=False,two_type=2,index=6,buy_count=1)
        self.assertEqual(self.b.profile(),after)

    def test_legacy_slot_purchases_migrate_once_without_material_debt(self):
        role=self.b.profile();a=role['guild']['instances']
        for key in ('pet_shop_v2','pet_shop_version','shop_goods_day','shop_view_day'):a.pop(key,None)
        a['shop_bought']={'1':3,'2':2,'3':4,'4':5,'5':6,'6':7};self.b.save(role)
        before=self.b.profile();self.req(91,ok=False,two_type=2,index=3,buy_count=1)
        self.assertEqual(self.b.profile(),before)
        with patch.object(guild_offline,'roll',return_value=0):offers=self.req(91,two_type=1)[0]['item_list']
        self.assertEqual([o['left_times'] for o in offers.values()],[9,8,3,7,6,5])
        self.assertEqual(self.req(91,two_type=1)[0]['item_list'],offers)
        self.assertEqual(self.b.profile()['attachments'],before['attachments'])

    def test_v2_same_day_migration_preserves_spending_and_reduces_training_limit(self):
        for bought,left in ((2,1),(3,0),(10,0)):
            role=self.b.profile();a=role['guild']['instances'];a.pop('pet_shop_version',None)
            a['shop_goods']=list(range(8));a['shop_bought']={'1338':4,'1345':bought,'1347':2};self.b.save(role)
            before=self.b.profile();self.req(91,ok=False,two_type=2,index=3,buy_count=1)
            self.assertEqual(self.b.profile(),before)
            with patch.object(guild_offline,'roll',return_value=0):offers=self.req(91,two_type=1)[0]['item_list']
            self.assertEqual([o['left_times'] for o in offers.values()],[9,13,left,13,13,3])
            self.assertEqual(self.b.profile()['guild']['instances']['shop_bought'],a['shop_bought'])
            self.assertEqual(self.b.profile()['attachments'],before['attachments'])
            self.assertEqual(self.b.profile()['guild']['instances']['reputation'],a['reputation'])
            with patch.object(guild_offline,'roll',side_effect=AssertionError('migration repeated')):
                self.assertEqual(self.req(91,two_type=1)[0]['item_list'],offers)

    def test_grant_failure_rolls_back_currency_and_stock(self):
        before=self.b.profile()
        with patch('network_redirect.guild_hunt.journey.grant',side_effect=ValueError('grant failed')):
            self.req(91,ok=False,two_type=2,index=3,buy_count=3)
        self.assertEqual(self.b.profile(),before)

    def test_config_rejects_invalid_pool_prices_weights_and_limits(self):
        rules=guild.load_rules()
        invalids=[('pet_shop_reputation',None),('pet_shop_reputation',[20]*9),
                  ('pet_shop_fixed_items',[1338,1339,1346]),('pet_shop_fixed_items',[1338,1339,1339]),
                  ('pet_shop_random_slots',True),('pet_shop_random_slots',4),
                  ('pet_shop_weights',None),('pet_shop_weights',[0]*9),('pet_shop_weights',[1]*9),
                  ('pet_shop_weights',[0,0,25,10,0,25,20,5,True]),('pet_shop_weights',[0,0,25,10,0,25,20,5,-1]),
                  ('pet_shop_daily_limits',[0,0,0,0,10,5,5,5,1]),('pet_shop_daily_limits',[0,0,0,0,3,5,5,5,2]),
                  ('pet_shop_daily_limits',[0,0,0,0,3,5,5,5,True]),('pet_shop_items',rules['pet_shop_items'][:-1])]
        for key,value in invalids:
            invalid=copy.deepcopy(rules);invalid[key]=value
            with self.subTest(key=key,value=value),self.assertRaises(ValueError):guild_offline.validate_rules(invalid)


del GuildActivityFixTests

if __name__=='__main__':unittest.main()
