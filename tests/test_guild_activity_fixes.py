import tempfile
import copy
import unittest
from pathlib import Path
from unittest.mock import patch

from network_redirect import summon
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
            deadline=self.req(88)[-1]['task_last_time']
            self.assertGreater(deadline,self.now)
            self.assertLessEqual(deadline-self.now,86400)
            self.assertEqual((deadline+r['timezone_offset_hours']*3600)%86400,0)
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


    def test_legacy_search_board_migrates_without_reroll_or_duplicate_rewards(self):
        for used in (0,2,5):
            with self.subTest(used=used):
                self.now+=86400
                self.req(43,flag=1)
                for _ in range(used):self.req(43,flag=2)
                role=self.b.profile();a=role['guild']['instances']
                original=copy.deepcopy(a['search_tiles'])
                a['search_tiles']+=copy.deepcopy(a['search_tiles'][:7])
                # The reported freeze: reward 5 is at display slot 20 of 25.
                a['search_order']=[15,9,7,3,20,11,17,22,1,6,13,19,8,23,21,5,18,14,10,12,25,24,4,16,2]
                self.b.save(role)
                result=self.req(43,flag=1)[-1];after=self.b.profile()
                self.assertEqual((result['board_size'],len(result['prize_items'])),(18,18))
                self.assertEqual(set(result['search_order'].values()),set(range(1,19)))
                self.assertEqual(after['guild']['instances']['search_tiles'],original)
                self.assertEqual((result['search_count'],result['free_times'],result['all_point']),(used,5-used,used*10))
                for key in ('gold_coin','silver_coin','attachments'):
                    self.assertEqual(role.get(key),after.get(key))
                self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
                again=self.req(43,flag=1)[-1]
                self.assertEqual(result['prize_items'],again['prize_items'])
                self.assertEqual(result['search_order'],again['search_order'])
                if used<5:
                    gold=self.b.profile()['gold_coin']
                    swept=self.req(43,flag=6)[-1]
                    self.assertEqual(set(swept['prize_list']),set(range(used+1,6)))
                    for index,prize in swept['prize_list'].items():
                        item=result['prize_items'][index]['item']
                        for key in ('object_type','attach_type','attach_count','attach_level'):
                            self.assertEqual(prize[key],item[key])
                    self.assertEqual(self.b.profile()['gold_coin'],gold-self.b.guild_rules['search_sweep_gold'])
                before=self.b.profile();self.req(43,ok=False,flag=6)
                self.assertEqual(before,self.b.profile())


    def test_search_board_capacity_and_last_reward_cursor(self):
        from network_redirect import guild_offline, formation
        rules=dict(self.b.guild_rules,search_daily=19)
        with self.assertRaises(formation.Rejected):guild_offline.validate_rules(rules)
        self.b.guild_rules['search_daily']=18
        initial=self.req(43,flag=1)[-1]
        result=self.req(43,flag=6)[-1]
        self.assertEqual((result['free_times'],result['search_count'],result['token_index']),(0,18,19))
        self.assertEqual(set(result['prize_list']),set(range(1,19)))
        self.assertEqual(result['prize_list'][18]['attach_count'],initial['prize_items'][18]['item']['attach_count'])
