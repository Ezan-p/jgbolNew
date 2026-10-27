"""Pet-shop purchases follow the stock and price advertised to native Lua."""
import copy
import unittest
from pathlib import Path

from network_redirect import guild, guild_offline, summon
from network_redirect.backend import Backend
from network_redirect.protocol import encode
from tests.test_guild_activity_fixes import GuildActivityFixTests


class GuildPetShopTests(unittest.TestCase):
    legacy_setup=GuildActivityFixTests.setUp
    req=GuildActivityFixTests.req

    def setUp(self):
        self.legacy_setup()
        self.req(91,two_type=1)
        role=self.b.profile()
        role['guild']['instances'].update(reputation=1000,total_reputation=1000)
        self.b.save(role)

    def item_count(self,tid):
        return sum(p['count'] for p in self.b.profile()['attachments'] if p['attach_type']==5 and p['type_id']==tid)

    def test_charm_prices_are_distinct_and_charge_the_advertised_amount(self):
        offers=self.req(91,two_type=1)[0]['item_list']
        prices={row['item']['attach_type']:row['buy_reputation'] for row in offers.values() if row['item']['attach_type'] in (1338,1339,1340,1341)}
        self.assertEqual(prices,{1338:20,1339:40,1340:60,1341:100})
        for index,offer in offers.items():
            before=self.b.profile()
            response=self.req(91,two_type=2,index=index,buy_count=2)[0]
            after=self.b.profile()
            self.assertEqual(after['guild']['instances']['reputation'],before['guild']['instances']['reputation']-offer['buy_reputation']*2)
            self.assertEqual(response['cur_reputation'],after['guild']['instances']['reputation'])
            self.assertEqual(response['buy_item']['buy_reputation'],offer['buy_reputation'])
            self.assertEqual(response['buy_item']['left_times'],offer['left_times']-2)
            self.assertEqual(after['guild']['instances']['total_reputation'],1000)

    def test_batch_above_three_and_integer_lua_numbers_are_accepted_once(self):
        offer=self.req(91,two_type=1)[0]['item_list'][3]
        self.assertEqual(offer['left_times'],13)
        before=self.item_count(1338)
        self.serial+=1
        packet=encode(1301,dict(serial_num=self.serial,id=91,data=summon.lua(dict(two_type=2,index=3.0,buy_count=13.0))))
        response=self.b.respond(packet,{'authenticated':True})
        after=self.b.profile()
        self.assertEqual(after['guild']['instances']['reputation'],740)
        self.assertEqual(self.item_count(1338),before+13)
        self.assertEqual(self.b.respond(packet,{'authenticated':True}),response)
        self.assertEqual(self.b.profile(),after)
        self.assertEqual(self.req(91,two_type=1)[0]['item_list'][3]['left_times'],0)
        before=self.b.profile();self.req(91,ok=False,two_type=2,index=3,buy_count=1)
        self.assertEqual(self.b.profile(),before)

    def test_purchase_rejects_invalid_indices_and_counts_without_mutating(self):
        for key,values in (('index',(True,0,-1,1.5,7,'3')),('buy_count',(True,0,-1,1.5,2147483648,'4'))):
            for value in values:
                with self.subTest(key=key,value=value):
                    args=dict(two_type=2,index=3,buy_count=1);args[key]=value
                    before=self.b.profile();self.req(91,ok=False,**args)
                    self.assertEqual(self.b.profile(),before)

    def test_unlock_balance_and_remaining_stock_fail_atomically(self):
        for reputation,total,index,count in ((1000,0,4,1),(39,1000,4,1),(1000,1000,3,14)):
            with self.subTest(reputation=reputation,total=total,index=index,count=count):
                role=self.b.profile();role['guild']['instances'].update(reputation=reputation,total_reputation=total);self.b.save(role)
                before=self.b.profile();self.req(91,ok=False,two_type=2,index=index,buy_count=count)
                self.assertEqual(self.b.profile(),before)

    def test_purchases_survive_reconnect_and_stock_resets_at_daily_boundary(self):
        self.req(91,two_type=2,index=4,buy_count=4)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.req(91,two_type=1)[0]['item_list'][4]['left_times'],9)
        deadline=self.req(83)[0]['task_last_time']
        self.now=deadline-1
        self.assertEqual(self.req(91,two_type=1)[0]['item_list'][4]['left_times'],9)
        self.now=deadline
        response=self.req(91,two_type=1)[0]
        self.assertEqual(response['item_list'][4]['left_times'],13)
        self.assertEqual(response['cur_reputation'],840)
        self.assertEqual(response['item_list'][4]['buy_reputation'],40)

    def test_config_requires_positive_complete_increasing_charm_prices(self):
        rules=guild.load_rules()
        for prices in (None,[],[20]*6,[20,20,20,40,60,True],[20,20,20,40,60,0],[20,20,40,20,60,100]):
            invalid=copy.deepcopy(rules);invalid['pet_shop_reputation']=prices
            with self.subTest(prices=prices),self.assertRaises(ValueError):guild_offline.validate_rules(invalid)


del GuildActivityFixTests


if __name__=='__main__':unittest.main()
