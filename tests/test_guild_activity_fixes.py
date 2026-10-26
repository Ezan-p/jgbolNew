import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from network_redirect import guild_instances, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode

FRIDAY = 1792728000


class GuildActivityFixTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.addCleanup(lambda:self.b.close());self.serial=20000;self.now=FRIDAY
        clock=patch('network_redirect.backend.time.time',side_effect=lambda:self.now)
        clock.start();self.addCleanup(clock.stop)
        role=self.b.profile();role.update(level=50,gold_coin=100000,silver_coin=100000);self.b.save(role)
        self.req(1,union_name='仙盟活动修复')
        role=self.b.profile();role['guild']['unions']['2']['popularity']=4000;self.b.save(role)
        self.req(5,role_list=list(map(int,role['guild']['unions']['2']['applications'])))

    def req(self,op,ok=True,**data):
        self.serial+=1
        replies=[decode(p) for p in self.b.respond(encode(1301,dict(serial_num=self.serial,id=op,data=summon.lua(data))),{'authenticated':True})]
        errors=[d for m,_,d in replies if m==2998 and d['id']==55]
        self.assertEqual(bool(errors),not ok,errors)
        return [login_fields(d['data']) for m,_,d in replies if m==1301]

    def test_pet_calendar_is_open_on_all_seven_days(self):
        r=self.b.guild_rules
        self.assertFalse(r['train_weekend_only']);self.assertFalse(r['lucky_weekend_only']);self.assertTrue(r['hunt_weekend_open'])
        for day in range(7):
            self.now=FRIDAY+day*86400
            info=self.req(79)[-1]
            self.assertEqual(info['result'],61)
            self.assertGreater(info['last_time'],self.now)
            self.assertLessEqual(info['last_time']-self.now,86400)
            self.assertEqual(len(self.req(83)[-1]['union_task']),3)
        self.req(89)
        self.assertEqual(self.b.profile()['guild']['instances']['lucky_week_used'],1)

    def test_escort_claim_survives_reconnect_and_other_road(self):
        self.req(69,flag=6,road_type=2,book_level=1,des_id=0)
        trip=self.b.profile()['guild']['escort']['active']
        running=self.req(69,flag=3,road_type=1)[-1]
        self.assertTrue(running['escort_active']);self.assertFalse(running['can_rece_prize'])
        self.assertEqual(running['on_road_type'],2);self.assertEqual(running['escort_end_time'],trip['book']['end_time'])
        before=self.b.profile();self.req(69,ok=False,flag=11);self.assertEqual(before,self.b.profile())
        self.now=trip['book']['end_time']
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        ready=self.req(69,flag=9,road_type=3)[-1];self.assertTrue(ready['can_rece_prize'])
        result=self.req(69,flag=11)[-1]
        self.assertEqual(result['item_info'][1]['attach_type'],1302)
        self.assertFalse(result['escort_active']);self.assertFalse(result['can_rece_prize']);self.assertEqual(result['on_road_type'],0)
        before=self.b.profile();self.req(69,ok=False,flag=11);self.assertEqual(before,self.b.profile())
        self.req(69,flag=6,road_type=1,book_level=1,des_id=0)

    def test_escort_cross_day_does_not_lose_unclaimed_reward(self):
        self.req(69,flag=6,road_type=3,book_level=1,des_id=0)
        self.now+=86400
        self.assertTrue(self.req(69,flag=3,road_type=1)[-1]['can_rece_prize'])
        self.assertEqual(self.req(69,flag=11)[-1]['item_info'][1]['attach_type'],1303)

    def test_search_count_stepwise_sweep_reconnect_and_daily_reset(self):
        self.assertEqual(self.req(43,flag=1)[-1]['free_times'],5)
        for n in (1,2):
            result=self.req(43,flag=2)[-1]
            self.assertEqual((result['search_count'],result['free_times']),(n,5-n))
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.req(43,flag=1)[-1]['free_times'],3)
        result=self.req(43,flag=6)[-1];self.assertEqual((result['search_count'],result['free_times']),(5,0))
        before=self.b.profile();self.req(43,ok=False,flag=2);self.assertEqual(before,self.b.profile())
        self.now+=86400;result=self.req(43,flag=1)[-1]
        self.assertEqual((result['search_count'],result['free_times']),(0,5))

    def test_floor_cap_is_not_completed_floors_or_attempt_count(self):
        self.req(26)
        info=self.req(44)[-1]['team'];self.assertEqual((info['max_layer'],info['cleared_layer'],info['fight_count']),(3,0,0))
        role=self.b.profile();a=role['guild']['instances']
        a.update(layer=1,team_fights=2,team_last_fight_time=self.now);self.b.save(role)
        info=self.req(44)[-1]['team'];self.assertEqual((info['max_layer'],info['cleared_layer'],info['fight_count']),(3,1,2))
        self.assertEqual(info['last_search_time'],self.now)
        treasure=self.req(43,flag=1)[-1];self.assertEqual((treasure['max_layer'],treasure['cleared_layer'],treasure['free_times']),(3,1,5))
        self.now+=86400;self.req(26)
        info=self.req(44)[-1]['team'];self.assertEqual((info['max_layer'],info['cleared_layer'],info['last_search_time']),(3,0,0))
