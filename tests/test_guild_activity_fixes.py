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

    def unlock_search(self,layer=3):
        self.req(43,flag=1)
        role=self.b.profile();role['guild']['instances']['layer']=layer;self.b.save(role)

    def test_search_count_stepwise_sweep_reconnect_and_daily_reset(self):
        self.assertEqual(self.req(43,flag=1)[-1]['free_times'],0)
        before=self.b.profile()
        self.req(43,ok=False,flag=2);self.req(43,ok=False,flag=6)
        self.assertEqual(before,self.b.profile())
        self.unlock_search(1)
        for n in (1,2):
            result=self.req(43,flag=2)[-1]
            self.assertEqual((result['search_count'],result['free_times']),(n,5-n))
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.req(43,flag=1)[-1]['free_times'],3)
        result=self.req(43,flag=6)[-1];self.assertEqual((result['search_count'],result['free_times']),(5,0))
        before=self.b.profile();self.req(43,ok=False,flag=2);self.assertEqual(before,self.b.profile())
        self.unlock_search(2)
        result=self.req(43,flag=1)[-1];self.assertEqual((result['search_count'],result['free_times']),(5,5))
        self.unlock_search(3)
        result=self.req(43,flag=6)[-1];self.assertEqual((result['search_count'],result['free_times']),(15,0))
        self.now+=86400;result=self.req(43,flag=1)[-1]
        self.assertEqual((result['search_count'],result['free_times']),(0,0))

    def test_three_wins_unlock_five_searches_each_and_cannot_repeat(self):
        self.req(26)
        applicants=list(map(int,self.b.profile()['guild']['instances']['team']['applications']))
        self.req(28,role_list=applicants[:2])
        fighters=list(map(int,self.b.profile()['guild']['instances']['team']['members']))
        for floor in range(1,4):
            with patch('network_redirect.guild_instances.simulate',return_value=(1,[],{})):
                self.req(41,fight_list=fighters)
            info=self.req(44)[-1]['team']
            self.assertEqual((info['max_layer'],info['cleared_layer'],info['fight_count']),(3,floor,floor))
            self.assertEqual(info['can_continue'],floor<3)
            self.assertEqual(info['last_search_time'],self.now)
            result=self.req(43,flag=1)[-1]
            self.assertEqual((result['free_times'],result['earned_search_times']),(floor*5,floor*5))
            self.req(42)  # Replay is read-only, never another layer/quota grant.
            self.assertEqual(self.req(43,flag=1)[-1]['free_times'],floor*5)
        before=self.b.profile();self.req(41,ok=False,fight_list=fighters);self.assertEqual(before,self.b.profile())
        self.req(32);self.req(26)
        self.assertFalse(self.req(44)[-1]['team']['can_continue'])

    def test_failed_exploration_grants_no_searches(self):
        self.req(26)
        applicants=list(map(int,self.b.profile()['guild']['instances']['team']['applications']))
        self.req(28,role_list=applicants[:2])
        fighters=list(map(int,self.b.profile()['guild']['instances']['team']['members']))
        with patch('network_redirect.guild_instances.simulate',return_value=(4,[],{})):
            self.req(41,fight_list=fighters)
        info=self.req(44)[-1]['team']
        self.assertEqual((info['cleared_layer'],info['fight_count']),(0,1))
        self.assertTrue(info['can_continue'])
        self.assertEqual(self.req(43,flag=1)[-1]['free_times'],0)

    def test_legacy_search_board_replaces_obsolete_rewards_without_regranting(self):
        from network_redirect import daily
        for size in (18,25):
            for used in (0,2,5):
                with self.subTest(size=size,used=used):
                    self.now+=86400;self.unlock_search(1)
                    role=self.b.profile();a=role['guild']['instances']
                    a.pop('search_board_version',None)
                    a['search']=used;a['points']=used*10
                    a['search_tiles']=[dict(item=daily.spec([5,1003,1,1]),had_token=i<used) for i in range(size)]
                    a['search_order']=list(range(size,0,-1));self.b.save(role)
                    result=self.req(43,flag=1)[-1];after=self.b.profile()
                    self.assertEqual((result['board_size'],len(result['prize_items'])),(18,18))
                    self.assertEqual(set(result['search_order'].values()),set(range(1,19)))
                    self.assertEqual([t['had_token'] for t in after['guild']['instances']['search_tiles']],[i<used for i in range(18)])
                    self.assertTrue(all(t['item'] in [daily.spec(p) for p in self.b.guild_rules['search_rewards']] for t in after['guild']['instances']['search_tiles']))
                    self.assertEqual((result['search_count'],result['free_times'],result['all_point']),(used,5-used,used*10))
                    for key in ('gold_coin','silver_coin','attachments'):
                        self.assertEqual(role.get(key),after.get(key))
                    self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
                    again=self.req(43,flag=1)[-1]
                    self.assertEqual(result['prize_items'],again['prize_items'])
                    self.assertEqual(result['search_order'],again['search_order'])
                    if used<5:
                        swept=self.req(43,flag=6)[-1]
                        self.assertEqual(set(swept['prize_list']),set(range(used+1,6)))
                        for index,prize in swept['prize_list'].items():
                            for key in ('object_type','attach_type','attach_count','attach_level'):
                                self.assertEqual(prize[key],result['prize_items'][index]['item'][key])
                    before=self.b.profile();self.req(43,ok=False,flag=6);self.assertEqual(before,self.b.profile())

    def test_current_version_board_repairs_claimed_and_unclaimed_synthesis_scrolls(self):
        from network_redirect import daily, guild_instances
        from collections import Counter
        self.unlock_search(1)
        self.req(43,flag=2)
        role=self.b.profile();a=role['guild']['instances']
        original=copy.deepcopy(a['search_tiles'])
        history=copy.deepcopy(a['board'])
        a['search_board_version']=guild_instances.SEARCH_BOARD_VERSION
        for index in (0,1):a['search_tiles'][index]['item']=daily.spec([5,1003,1,1])
        self.b.save(role)
        result=self.req(43,flag=1)[-1];after=self.b.profile()
        repaired=after['guild']['instances']['search_tiles']
        self.assertEqual(repaired[2:],original[2:])
        self.assertEqual(Counter(tuple(t['item'].items()) for t in repaired),Counter(tuple(t['item'].items()) for t in original))
        self.assertTrue(repaired[0]['had_token']);self.assertFalse(repaired[1]['had_token'])
        self.assertEqual((result['search_count'],result['free_times'],result['all_point']),(1,4,10))
        self.assertEqual(after['guild']['instances']['board'],history)
        for key in ('gold_coin','silver_coin','attachments'):
            self.assertEqual(after.get(key),role.get(key))
        again=self.req(43,flag=1)[-1]
        self.assertEqual(result['prize_items'],again['prize_items'])
        draw=self.req(43,flag=2)[-1]
        self.assertEqual(draw['prize_list'][1]['attach_type'],repaired[1]['item']['attach_type'])
        self.assertNotEqual(draw['prize_list'][1]['attach_type'],1003)

    def test_reward_pool_counts_persistence_and_currency_item_grants(self):
        from collections import Counter
        self.unlock_search()
        initial=self.req(43,flag=1)[-1]
        spec=lambda p:tuple(p[k] for k in ('object_type','attach_type','attach_count','attach_level'))
        counts=Counter(spec(t['item']) for t in initial['prize_items'].values())
        self.assertEqual(counts,Counter({tuple(p):n for p,n in zip(self.b.guild_rules['search_rewards'],self.b.guild_rules['search_reward_slots'])}))
        # Place every reward tier in the earned prefix to verify all grant paths.
        role=self.b.profile();a=role['guild']['instances']
        a['search_tiles'].sort(key=lambda t:spec(t['item']))
        unique=[]
        for tile in a['search_tiles']:
            if tile['item'] not in [t['item'] for t in unique]:unique.append(tile)
        for tile in unique:a['search_tiles'].remove(tile)
        a['search_tiles']=unique+a['search_tiles'];self.b.save(role)
        expected=a['search_tiles'][:15]
        result=self.req(43,flag=6)[-1];after=self.b.profile()
        self.assertEqual((result['free_times'],result['search_count'],result['token_index']),(0,15,16))
        self.assertEqual(set(result['prize_list']),set(range(1,16)))
        for field,typ in (('silver_coin',12),('gold_coin',11)):
            reward=sum(t['item']['attach_count'] for t in expected if t['item']['object_type']==typ)
            self.assertEqual(after[field]-role[field],reward-(10 if typ==11 else 0))
        for tid in (1001,1029):
            count=lambda r:sum(t['count'] for t in r['attachments'] if t['type_id']==tid)
            reward=sum(t['item']['attach_count'] for t in expected if t['item']['object_type']==5 and t['item']['attach_type']==tid)
            self.assertEqual(count(after)-count(role),reward)

    def test_invalid_board_and_quota_configuration(self):
        from network_redirect import guild_offline, formation
        bad_rewards=copy.deepcopy(self.b.guild_rules['search_rewards']);bad_rewards[0]=[5,1003,1,1]
        for changes in (dict(search_daily=26),dict(search_per_layer=0),dict(team_daily=4),dict(search_reward_slots=[1]*8),dict(search_rewards=bad_rewards)):
            with self.subTest(changes=changes),self.assertRaises(formation.Rejected):
                guild_offline.validate_rules(dict(self.b.guild_rules,**changes))
