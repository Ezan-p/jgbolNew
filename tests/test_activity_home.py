"""Full native home protocol, NPC identity, durable welfare and failure atomicity."""
import copy
from pathlib import Path
from unittest.mock import patch
from test_activity import ActivityCase, NOW
from network_redirect import activity_home as h, activity_home_welfare as w, npc_players, summon, formation
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode


class HomeTests(ActivityCase):
    def home(self, op, **data):
        self.ok(self.req(1348,id=op,data=summon.lua(data)))
        return next(login_fields(d['data']) for mid,_,d in self.decoded if mid==1348 and d['id']==op)

    def prepared(self):
        self.home(1)
        r=self.b.profile();r.update(silver_coin=2000000000,gold_coin=100000)
        for tid in (1361,1362,1363,1364,1365,1345):summon.add_item(r,tid,100000)
        self.b.save(r)
        return r

    def rejected(self,op,**data):
        before=self.b.profile()
        self.assertEqual(self.req(1348,id=op,data=summon.lua(data))[0][0],55)
        self.assertEqual(before,self.b.profile())

    def test_npc_identity_stability_and_independent_visits(self):
        self.prepared(); entrance=self.home(1)
        self.assertTrue(entrance['config_data']['offline_home'])
        self.assertFalse(any(entrance['config_data']['activity_flag'].values()))
        data=self.home(13)['friend_data']
        self.assertEqual(len(data),10)
        for fid,f in data.items():
            profile=npc_players.catalog()[npc_players.resolve(fid)]['profile']
            self.assertEqual((f['name'],f['level']),(profile['role_name'],profile['level']))
            visited=self.home(6,friend_id=fid)
            self.assertEqual(visited['base_data']['point'],f['point'])
            self.assertEqual(visited['base_data']['level'],f['home_level'])
            self.assertEqual(len(visited['garden_data']['plant_data']),int(h.BUILD[2][visited['garden_data']['level']]['grid_count']))
            self.assertTrue(all(t['level']==0 for t in visited['train_data']['train_info'].values()))
        r=self.b.profile();r['level']=99;self.b.save(r)
        self.assertEqual(set(data),set(self.home(13)['friend_data']))
        self.rejected(6,friend_id=999)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(set(data),set(self.home(13)['friend_data']))

    def test_invitation_cap_no_empty_consumption_and_messages(self):
        self.prepared(); ids=list(self.home(13)['friend_data'])
        self.rejected(5,friend_id=ids[0])
        self.home(2,building_type=1);self.home(2,building_type=2)
        self.home(3,plant_grid=1,seed_type=1)
        for fid in ids[:5]:self.home(5,friend_id=fid)
        self.rejected(5,friend_id=ids[5])
        self.assertFalse(self.home(13)['friend_data'][ids[5]]['has_invited'])
        self.home(12,friend_id=ids[0],chat_msg='来访问好')
        self.assertEqual(len(self.home(6,friend_id=ids[0])['message_data']),2)
        self.rejected(12,friend_id=ids[0],chat_msg='bad\n')
        self.assertEqual(self.b.profile()['activity']['home']['plants']['1']['cur_plus_times'],5)

    def test_goals_both_tabs_claim_replay_and_restart(self):
        self.prepared();self.home(2,building_type=1)
        all_data=self.home(24,flag=1)['all_activity']
        self.assertEqual(set(all_data),{68,69,70,72})
        self.assertEqual(all_data[72][2]['target_list'][1]['status'],2)
        self.rejected(24,flag=2,act_type=72,main_type=1,index=1)
        self.home(24,flag=2,act_type=72,main_type=2,index=1)
        saved=self.b.profile();self.b.respond(self.packet,self.state);self.assertEqual(saved,self.b.profile())
        self.rejected(24,flag=2,act_type=72,main_type=2,index=1)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.home(24,flag=1)['all_activity'][72][2]['target_list'][1]['status'],3)
        self.rejected(24,flag=2,act_type=72,main_type=True,index=1)
        self.rejected(24,flag=2,act_type=70,index=-1)

    def test_growth_plan_incremental_claims_and_community(self):
        r=self.prepared();s=r['activity']['home'];s['build']={str(i):5 for i in h.KEYS};self.b.save(r)
        self.assertEqual(self.home(24,flag=1)['all_activity'][69]['total_gold'],100)
        gold=self.b.profile()['gold_coin'];self.home(24,flag=2,act_type=69)
        self.assertEqual(self.b.profile()['gold_coin'],gold+100)
        self.rejected(24,flag=2,act_type=69)
        self.home(24,flag=2,act_type=70,index=0)
        self.rejected(24,flag=2,act_type=70,index=0)
        self.rejected(24,flag=2,act_type=70,index=3)
        r=self.b.profile();s=r['activity']['home'];s['build']={str(i):20 for i in h.KEYS};s['level']=3;self.b.save(r)
        self.assertEqual(self.home(24,flag=1)['all_activity'][69]['total_gold'],900)
        self.home(24,flag=2,act_type=69)
        self.assertEqual(self.b.profile()['gold_coin'],gold+1000)
        for i in (1,2,3):self.home(24,flag=2,act_type=70,index=i)

    def test_race_training_final_board_mail_once_and_no_idle_rewards(self):
        self.prepared();self.home(2,building_type=1);self.home(2,building_type=4)
        self.home(20,train_type=1,consume_type=1,use_count=10)
        board=self.home(24,flag=1)['all_activity'][68]
        self.assertEqual(board['role_exp'],2000)
        self.assertEqual(len(board['rank_data']),11)
        before=self.b.profile();s=before['activity']['home']
        expected=next(row['order'] for row in w.rank(before,s,NOW,self.b.activity_rules,final=True) if not row['is_npc'])
        with patch('network_redirect.backend.time.time',return_value=NOW+8*86400):
            self.assertEqual(self.home(24,flag=1)['all_activity'][68]['role_exp'],0)
            mails=[m for key,m in self.b.profile()['welfare']['mails'].items() if key.startswith('home-race-')]
            self.assertEqual(len(mails),1);self.assertEqual(mails[0]['prizes'][0][2],w.rules()['race_gold'][expected-1])
            self.home(24,flag=1)
            self.assertEqual(len([k for k in self.b.profile()['welfare']['mails'] if k.startswith('home-race-')]),1)
            self.ok(self.req(1102,mail_id=mails[0]['mail_id'],flag=1))
            gold=self.b.profile()['gold_coin']
            self.req(1102,mail_id=mails[0]['mail_id'],flag=1)
            self.assertEqual(self.b.profile()['gold_coin'],gold)
        with patch('network_redirect.backend.time.time',return_value=NOW+30*86400):
            self.home(1)
            self.assertEqual(len([k for k in self.b.profile()['welfare']['mails'] if k.startswith('home-race-')]),1)

    def test_training_cap_spend_and_clock_rollback(self):
        r=self.prepared();r['activity']['home']['build']['4']=1;self.b.save(r)
        self.rejected(20,train_type=1,consume_type=3,use_count=1000)
        self.home(20,train_type=1,consume_type=1,use_count=10)
        with patch('network_redirect.backend.time.time',return_value=NOW-86400):
            self.rejected(20,train_type=1,consume_type=1,use_count=1)
        self.assertEqual(self.b.profile()['activity']['home']['welfare']['race_exp'],2000)

    def test_shop_refresh_keeps_daily_limits_and_rolls_over(self):
        self.prepared();shop=self.home(14)['shop_data']
        self.assertEqual((len(shop[1]),len(shop[2])),(5,3))
        self.assertNotIn(1363,[row['item']['attach_type'] for page in shop.values() for row in page.values()])
        self.assertEqual(shop[1][2]['item']['attach_count'],100)
        self.home(15,shop_page=2,item_index=1,buy_count=10)
        self.rejected(15,shop_page=2,item_index=1,buy_count=1)
        self.rejected(15,shop_page=1,item_index=6,buy_count=1)
        before=self.b.profile()
        self.home(15,shop_page=1,item_index=2,buy_count=10)
        after=self.b.profile()
        for tid,delta in ((1361,-1000),(1362,1000),(1363,0)):
            count=lambda role:sum(p['count'] for p in role['attachments'] if p['type_id']==tid)
            self.assertEqual(count(after)-count(before),delta)
        self.rejected(15,shop_page=1,item_index=2,buy_count=1)
        self.assertEqual(self.home(14,flush_flag=True)['shop_data'][1][2]['limit'],0)
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            self.assertEqual(self.home(14)['shop_data'][1][2]['limit'],10)

    def test_shop_removal_preserves_legacy_purchase_keys(self):
        r=self.prepared()
        purchases={'1':1,'2':2,'3':10,'4':3,'5':4,'6':5,'7':6,'8':7,'9':8}
        r['activity']['home']['purchases']=purchases.copy();self.b.save(r)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        shop=self.home(14)['shop_data']
        self.assertEqual([row['limit'] for row in shop[1].values()],[9,8,2,6,5])
        self.assertEqual([row['limit'] for row in shop[2].values()],[4,3,2])
        self.home(15,shop_page=1,item_index=3,buy_count=2)
        self.home(15,shop_page=2,item_index=1,buy_count=4)
        purchases.update({'4':5,'7':10})
        self.assertEqual(self.b.profile()['activity']['home']['purchases'],purchases)
        self.rejected(15,shop_page=1,item_index=3,buy_count=1)
        self.rejected(15,shop_page=2,item_index=1,buy_count=1)

    def test_prayer_unlock_starter_pet_and_main_level_limit(self):
        self.prepared();self.rejected(11)
        self.home(2,building_type=1);self.home(2,building_type=3);self.home(11)
        self.rejected(11);self.assertEqual(self.b.profile()['cortege_limit_plus'],5)
        self.home(2,building_type=5)
        self.assertEqual(len(self.b.profile()['activity']['home']['pets']),1)
        self.home(22);self.assertEqual(len(self.b.profile()['activity']['home']['pets']),1)

    def test_old_friend_migration_preserves_consumed_help(self):
        r=self.prepared();s=r['activity']['home'];s.pop('neighbours');s['offline_friends']={'900001':dict(
            day=s['day'],invited=True,messages=['旧留言'],plants={'1':dict(level=0,seed_type=1,start_time=NOW-100,
            gain_time=NOW+1000,cur_plus_times=1,total_plus_times=5,benefit_flag=False)})};self.b.save(r)
        data=self.home(13)['friend_data'];first=next(iter(data))
        self.assertTrue(data[first]['has_invited'])
        self.rejected(7,friend_id=900001,plant_grid=1)
        self.assertIn('旧留言',self.home(6,friend_id=first)['message_data'].values())

    def test_encoding_failure_rolls_back_rewards(self):
        self.prepared();self.home(2,building_type=1)
        with patch('network_redirect.activity_home.response',side_effect=OverflowError('fixture encoder failure')):
            self.rejected(24,flag=2,act_type=72,main_type=2,index=1)
        self.home(24,flag=2,act_type=72,main_type=2,index=1)

    def test_legacy_banked_training_remains_usable_without_new_race_points(self):
        r=self.prepared();s=r['activity']['home'];s['build']['4']=2
        s['train']['1']=dict(level=2,cur_exp=100000)
        before_gold=r['gold_coin'];self.b.save(r)
        self.home(1)
        r=self.b.profile();self.assertEqual(r['activity']['home']['train']['1']['level'],4)
        self.assertGreater(r['activity']['home']['train']['1']['cur_exp'],0)
        self.assertEqual(r['activity']['home']['welfare']['race_exp'],0)
        self.assertEqual(r['gold_coin'],before_gold)
