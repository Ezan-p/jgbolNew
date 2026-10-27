import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from network_redirect.backend import Backend, login_fields
from network_redirect import vip, summon, journey, activity, reborn_stars
from network_redirect.protocol import encode, decode
from recharge_helpers import funded_order

NOW=1792814400
class VipTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.b=Backend(Path(self.tmp.name),18790,lambda *a,**k:None)
        self.addCleanup(lambda:self.b.close());self.serial=200
        clock=patch('network_redirect.backend.time.time',return_value=NOW);clock.start();self.addCleanup(clock.stop)
        funded_order(self.b,101,'seed-test-cards')
    def req(self,mid=1201,**data):
        self.serial+=1;self.packet=encode(mid,dict(serial_num=self.serial,**data))
        self.reply=self.b.respond(self.packet,dict(authenticated=True))
        self.assertEqual(decode(self.reply[-1])[0],1106)
        return [(d['id'],login_fields(d['data'])) for m,_,d in map(decode,self.reply) if m==2998]
    def fixture(self,v=10):
        r=self.b.profile();r.update(vip_level=v,level=70,gold_coin=100000,silver_coin=100000000);self.b.save(r);return r
    def test_config_and_login(self):
        self.fixture(3)
        cfg=login_fields(decode(self.b.bootstrap()[0])[2]['data'])
        self.assertEqual(len(cfg[1]),11)
        for v in range(11):
            self.assertEqual(cfg[1][v]['day_pick_cortege_limit'],{1:0,2:0,3:0})
        r=self.b.snapshot();self.assertEqual(r['strength_item_limit'],10);self.assertEqual(r['rape_flush_limit'],6)
    def test_daily_all_tiers(self):
        for v in range(11):
            self.fixture(v);r=self.b.profile();r['take_vip_gold_time']=0;self.b.save(r)
            before=self.b.profile();out=self.req(flag=5,id=999)
            if not v:self.assertEqual(out[-1][0],55);continue
            self.assertEqual(out[-1][0],58)
            after=self.b.profile();self.assertEqual(after['gold_coin']-before['gold_coin'],self.b.vip_rules['daily_gold'][v])
            self.assertEqual(self.b.respond(self.packet,dict(authenticated=True)),self.reply)
            self.assertEqual(self.req(flag=5,id=0)[-1][0],55)
    def test_midnight_restart_and_upgrade_same_day(self):
        self.fixture(1);self.req(flag=5,id=0)
        self.fixture(10);self.assertEqual(self.req(flag=5,id=0)[-1][0],55)
        self.b.close();self.b=Backend(Path(self.tmp.name),18790,lambda *a,**k:None)
        self.assertEqual(self.req(flag=5,id=0)[-1][0],55)
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):self.assertEqual(self.req(flag=5,id=0)[-1][0],58)
    def test_all_gifts_exact_csv_and_use(self):
        self.fixture()
        for v in range(1,11):
            self.assertEqual(self.req(flag=7,id=v)[-1][0],59)
            self.assertEqual(self.req(flag=7,id=v)[-1][0],55)
            r=self.b.profile();item=next(x for x in r['attachments'] if x['type_id']==1100+v)
            silver=r['silver_coin']
            out=self.req(1051,item_type=item['type_id'],item_id=item['id'],item_count=1,des_type=1,des_id=0)
            self.assertEqual(out[-1][0],21,out)
            csvsilver=int(vip.GIFTS[v]['attach_data'].split('/')[0].split('|')[-1])
            self.assertEqual(self.b.profile()['silver_coin']-silver,csvsilver)
            self.assertFalse(any(x['type_id']==1100+v for x in self.b.profile()['attachments']))
        self.assertEqual(self.b.profile()['vip_gift'],sum(1<<i for i in range(1,11)))
    def test_invalid_gifts_do_not_mutate(self):
        self.fixture(1)
        for ident in (0,2,11,2**32-1):
            before=self.b.profile();self.assertEqual(self.req(flag=7,id=ident)[-1][0],55);self.assertEqual(before,self.b.profile())
    def test_bag_gate_lock_and_batch(self):
        r=self.fixture(0);summon.add_item(r,1031,15);self.b.save(r)
        item=next(x for x in r['attachments'] if x['type_id']==1031)
        args=dict(item_type=1031,item_id=item['id'],item_count=15,des_type=1,des_id=0)
        self.assertEqual(self.req(1051,**args)[-1][0],55)
        self.fixture(1)
        with patch('network_redirect.qiankun_bags.draw',return_value=[12,1,30000,1]):out=self.req(1051,**args)
        self.assertEqual(out[-1][0],21);self.assertEqual(len(out[-1][1]['attach_list']),15)
        self.assertEqual(self.req(1051,**args)[-1][0],55)
    def test_recharge_replay_and_restart(self):
        self.req(1111,event_id=251,data='{item_id=103,large_count=2,small_count=0,order_id="test-order-0003"}')
        r=self.b.profile();self.assertEqual((r['charge_gold'],r['vip_level'],r['gold_coin']),(1000,3,2230))
        self.assertEqual(self.b.respond(self.packet,dict(authenticated=True)),self.reply)
        self.assertEqual(self.b.profile(),r)
        self.assertEqual(self.req(1111,event_id=251,data='{item_id=999,gold=999999}')[-1][0],55)
        self.b.close();self.b=Backend(Path(self.tmp.name),18790,lambda *a,**k:None)
        self.assertEqual(self.b.profile(),r)
        self.req(1111,event_id=251,data='{item_id=103,large_count=2,small_count=0,order_id="test-order-0003"}')
        self.assertEqual(self.b.profile(),r)

    def test_limits_all_levels(self):
        for v in range(1,11):
            r=self.fixture(v);journey.prepare(r,NOW,self.b.journey_rules);activity.prepare(r,NOW,self.b.activity_rules)
            for key,table in [('strength_item_limit',vip.RESOURCE),('top_fight_limit',vip.RANK),('rape_flush_limit',vip.RAPE),('convert_fight_limit',vip.CONVERT),('tollgate_flush_limit',vip.REFRESH)]:self.assertEqual(r[key],table[v])
            r.pop('divination',None)
            reborn_stars.divination(r,dict(event_type=1,data='{}'),self.b.reborn_rules,login_fields,NOW)
            self.assertEqual(r['divination']['divi_count'],vip.DIVINATION[v]);self.assertEqual(r['divination']['buy_count'],v*10)
    def test_divination_upgrade_and_day(self):
        r=self.fixture(1);req=dict(event_type=1,data='{}')
        reborn_stars.divination(r,req,self.b.reborn_rules,login_fields,NOW)
        r['divination']['divi_count']-=3;r['vip_level']=3
        reborn_stars.divination(r,req,self.b.reborn_rules,login_fields,NOW)
        self.assertEqual(r['divination']['divi_count'],17)
        reborn_stars.divination(r,req,self.b.reborn_rules,login_fields,NOW+86400)
        self.assertEqual(r['divination']['divi_count'],20)
    def test_unauthenticated(self):
        with self.assertRaises(ValueError):
            self.b.respond(encode(1111,dict(serial_num=1,event_id=251,data='{item_id=1}')),{})

    def test_buy_resource_limit_and_upgrade_preserves_used(self):
        self.fixture(1)
        for _ in range(5):
            self.assertNotIn(55,[e for e,d in self.req(1058,type_id=1022)])
        self.assertEqual(self.req(1058,type_id=1022)[-1][0],55)
        self.fixture(2)
        for _ in range(3):self.assertNotIn(55,[e for e,d in self.req(1058,type_id=1022)])
        self.assertEqual(self.req(1058,type_id=1022)[-1][0],55)
        self.assertEqual(self.b.profile()['strength_item_count'],8)

    def test_encoding_failure_rolls_back_reward_and_order(self):
        r=self.fixture(4);r['gold_coin']=2**32-1;self.b.save(r)
        before=self.b.profile()
        self.assertEqual(self.req(flag=5,id=0)[-1][0],55)
        self.assertEqual(self.b.profile(),before)
        self.req(1111,event_id=251,data='{item_id=101,large_count=0,small_count=2,order_id="overflow-order"}')
        self.assertEqual(self.b.profile(),before)

    def test_invalid_orders_and_duplicate_conflicts(self):
        for data in ('{}','{item_id=1}','{item_id=101,large_count=0,small_count=2,order_id="bad"}','os.execute("no")'):
            before=self.b.profile();self.assertEqual(self.req(1111,event_id=251,data=data)[-1][0],55);self.assertEqual(before,self.b.profile())
        self.req(1111,event_id=251,data='{item_id=101,large_count=0,small_count=2,order_id="duplicate-order"}')
        before=self.b.profile()
        self.req(1111,event_id=251,data='{item_id=102,large_count=1,small_count=0,order_id="duplicate-order"}')
        self.assertEqual(before,self.b.profile())

    def test_original_layout_products_bonus_and_monthly_base(self):
        expected = [(100,0),(500,50),(1000,110),(2000,240),(5000,650),(10000,1500)]
        for index,(base,bonus) in enumerate(expected,1):
            product=next(p for p in self.b.recharge_rules['products'] if p.get('ui_index')==index)
            self.assertEqual((product['gold'],product['bonus']),(base,bonus))
            before=self.b.profile()
            self.req(1111,event_id=251,data=funded_order(self.b,product['id'],f'original-ui-{index}'))
            after=self.b.profile()
            self.assertEqual(after['gold_coin']-before['gold_coin'],base+bonus+(base if index==1 else 0)+(60 if index==1 else 0)+(30*(base//500) if index>1 else 0))
            self.assertEqual(after['charge_gold']-before['charge_gold'],base)
            self.assertEqual(after['xianling']['charge'],sum(x[0] for x in expected[:index]))
            self.req(1111,event_id=251,data=funded_order(self.b,product['id'],f'original-ui-{index}'))
            self.assertEqual(self.b.profile(),after)

    def test_original_products_replay_after_restart(self):
        self.req(1111,event_id=251,data='{item_id=104,large_count=4,small_count=0,order_id="original-ui-restart"}')
        before=self.b.profile()
        self.b.close();self.b=Backend(Path(self.tmp.name),18790,lambda *a,**k:None)
        self.req(1111,event_id=251,data='{item_id=104,large_count=4,small_count=0,order_id="original-ui-restart"}')
        self.assertEqual(self.b.profile(),before)
