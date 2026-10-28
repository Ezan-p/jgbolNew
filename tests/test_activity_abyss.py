"""九幽原版请求、离线NPC、经济闭环和持久化回归。"""
import copy
from pathlib import Path
from unittest.mock import patch
from tests.test_activity import ActivityCase, NOW
from network_redirect import activity, activity_abyss as abyss, activity_drug as drug, npc_players, summon, abyss_balance
from network_redirect.backend import Backend


class AbyssTests(ActivityCase):
    def setUp(self):
        super().setUp()
        role=self.b.profile();role['level']=80;self.b.save(role)
        self.call(1)

    def call(self,op,**data):
        out=self.req(1329,id=op,data=summon.lua(data));self.ok(out)
        return next(value for ident,value in out if ident==173 and value['flag']==op)

    def test_catalog_rank_top20_progress_restart_and_inspection(self):
        original=copy.deepcopy(npc_players.catalog())
        rank=self.call(7,top_type=1)
        self.assertEqual(len(rank['top_data']),20)
        self.assertGreater(rank['my_top']['order'],20)
        ids=[]
        for row in rank['top_data'].values():
            key=npc_players.resolve(row['role_id']);self.assertIsNotNone(key)
            p=original[key]['profile'];self.assertEqual(row['name'],p['role_name'])
            self.assertGreaterEqual(p['level'],70);ids.append(row['role_id'])
        self.assertEqual(len(set(ids)),20)
        self.ok(self.req(1039,des_type=2,des_id=ids[0]))
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.call(7,top_type=1),rank)
        with patch('network_redirect.backend.time.time',return_value=NOW+3*86400):
            advanced=self.call(7,top_type=1)
        self.assertGreater(advanced['top_data'][1]['layer'],rank['top_data'][1]['layer'])
        self.assertEqual(original,npc_players.catalog())
        self.assertEqual(self.call(7,top_type=2)['top_type'],2)

    def test_all_drop_columns_reachable_and_cap_idempotent(self):
        role=self.b.profile();r=self.b.activity_rules
        self.assertEqual({e[1] for _,group in abyss.DROPS[1] for e in group},{1401,1442,1431,1330})
        # Exercise every outer category at its first weighted position.
        for roll,tid in ((0,1401),(50,1442),(80,1431),(130,1330)):
            trial=copy.deepcopy(role)
            with patch.object(abyss.secrets,'randbelow',side_effect=[roll,0]):
                s=abyss.state(trial,NOW+300,r)
            self.assertEqual(s['bag'][0]['attach_type'],tid)
        with patch('network_redirect.backend.time.time',return_value=NOW+4*86400):
            self.call(10);s=self.b.profile()['activity']['abyss']
            self.assertLessEqual(len(s['bag']),4)
            self.assertEqual(sum(x['attach_count'] for x in s['bag']),576)
            self.assertGreater(s['item_count'],0)
            gain=abyss_balance.crystal_tick(self.b.profile(),s,r)
            self.assertEqual(s['crystals'],576*gain)
            self.call(10);self.assertEqual(s,self.b.profile()['activity']['abyss'])

    def test_double_expiry_partial_purchase_and_daily_statistics(self):
        with patch('network_redirect.backend.time.time',return_value=NOW+150):self.call(14,buy_hour=1)
        with patch('network_redirect.backend.time.time',return_value=NOW+3600):
            self.call(9);s=self.b.profile()['activity']['abyss']
            r=self.b.activity_rules
            gain=abyss_balance.crystal_tick(self.b.profile(),s,r)
            self.assertEqual(s['crystals'],23*gain)  # no retroactive double first tick
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            stats=self.call(9)['day_record']
            midnight=((NOW+8*3600)//86400+1)*86400-8*3600
            expected=(NOW+86400-midnight)//300+1
            self.assertEqual(stats['fight_count'],expected)
            self.assertEqual(stats['now_fight_len'],r['abyss_tick_seconds'])
            self.assertEqual(stats['crystals'],expected*gain)

    def test_shop_pool_is_six_items_and_refreshes_once_per_day(self):
        first=self.call(13)
        first_rows=list(first['shop_list'].values())
        self.assertEqual(len(first_rows),self.b.activity_rules['abyss_shop_daily_count'])
        self.assertEqual(len({(x['object_type'],x['attach_type'],x['attach_count'],x['attach_level']) for x in first_rows}),6)
        self.assertEqual(first,self.call(13))
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            second=self.call(13)
        self.assertNotEqual(first['shop_day'],second['shop_day'])
        second_rows=list(second['shop_list'].values())
        self.assertEqual(len(second_rows),6)
        self.assertTrue(all(x['buy_times']>0 for x in second_rows))

    def test_legacy_crystals_claim_exchange_and_no_duplicate(self):
        role=self.b.profile();s=role['activity']['abyss']
        summon.add_item(role,1441,321)
        s['bag']=[activity.prize_spec([5,1441,123,1])];self.b.save(role)
        self.call(5);role=self.b.profile()
        self.assertEqual(role['activity']['abyss']['crystals'],444)
        self.assertFalse(any(i['type_id']==1441 for i in role['attachments']))
        shop=self.call(13)['shop_list'];self.assertTrue(shop)
        row=shop[1];role=self.b.profile();role['activity']['abyss']['crystals']+=row['crystals'];self.b.save(role)
        self.call(12,index=1,count=1)
        self.assertEqual(self.b.profile()['activity']['abyss']['crystals'],444)
        self.call(1);self.assertEqual(self.b.profile()['activity']['abyss']['crystals'],444)

    def test_boss_quota_loss_restart_midnight_and_complete(self):
        info=self.call(16)['specter_info']
        self.assertEqual((info['fight_boss_times'],info['max_fight_count']),(0,5))
        # Real losing battles consume quota while retaining floor and pills.
        role=self.b.profile();state=role['activity']['abyss']
        state.update(boss=80,pills={'1':1501},reductions=[10000,0,0,0])
        self.b.save(role)
        for used in range(1,6):
            result=self.call(6)
            self.assertFalse(result['is_win'])
            self.assertEqual(result['specter_info']['fight_boss_times'],used)
            self.assertEqual(result['specter_info']['boss_layer'],80)
        before=self.b.profile()
        self.assertEqual(self.req(1329,id=6,data='{}')[0][0],55)
        self.assertEqual(before,self.b.profile())
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.call(16)['specter_info']['fight_boss_times'],5)
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            result=self.call(6)  # Direct click from yesterday's exhausted panel.
            self.assertEqual(result['specter_info']['fight_boss_times'],1)
            self.assertEqual(self.b.profile()['activity']['abyss']['pills'],{'1':1501})
            role=self.b.profile();role['activity']['abyss'].update(boss=81,complete=True)
            self.b.save(role);before=self.b.profile()
            error=self.req(1329,id=6,data='{}')
            self.assertEqual(error[0][0],55)
            self.assertIn('全部通关',str(error))
            self.assertEqual(before,self.b.profile())

    def test_pills_all_essence_families_and_grades(self):
        for recipe in range(25,29):
            for grade in range(4):
                role=self.b.profile();s=role['activity']['abyss'];s['recipes']=[recipe]
                row=drug.RECIPES[recipe];role['drug_level']=int(row['min_level'])
                for part in row['study_material(attach_type|attach_count|need_silver)'].split('/'):
                    tid,n,_=map(int,part.split('|'));summon.add_item(role,tid,n)
                with patch.object(drug.secrets,'randbelow',return_value=(0,60,85,95)[grade]):
                    packets=drug.settle(role,s,21,dict(index=recipe),self.b.activity_rules)
                tid=int(row['attach_type'])+20*grade
                self.assertTrue(any(i['type_id']==tid for i in role['attachments']),(recipe,grade,tid,packets))

    def test_rank_mail_cross_day_exactly_once_and_complete_state(self):
        role=self.b.profile();s=role['activity']['abyss'];s.update(boss=81,complete=True,boss_count=5)
        self.b.save(role);self.assertEqual(self.call(7,top_type=1)['my_top']['order'],1)
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            self.call(1);role=self.b.profile();s=role['activity']['abyss']
            self.assertEqual(s['boss_count'],0)
            mails=[m for k,m in role['welfare']['mails'].items() if k.startswith('abyss-rank-')]
            self.assertEqual(len(mails),1);self.assertEqual(mails[0]['prizes'],[[5,1001,1,1],[5,1002,1,1]])
            self.call(7,top_type=1);role=self.b.profile()
            self.call(7,top_type=1);self.assertEqual(role,self.b.profile())
            self.assertEqual(self.req(1329,id=6,data='{}')[0][0],55)
            self.assertEqual(self.req(1329,id=17,data='{index=1,type_id=1501}')[0][0],55)
            self.ok(self.req(1103,mail_id=mails[0]['mail_id'],flag=1))
            self.assertTrue(self.b.profile()['welfare']['mails'][mails[0]['delivery_key']]['claimed'])
            before=self.b.profile();self.req(1103,mail_id=mails[0]['mail_id'],flag=1)
            self.assertEqual(before,self.b.profile())

    def test_news_poll_drain_and_event_badge(self):
        with patch('network_redirect.backend.time.time',return_value=NOW+3600):
            packet=self.call(15)
            self.assertTrue(packet['new_list']);self.assertEqual(packet['specter_info']['event_count'],1)
            self.assertTrue(any(n['tip_type']==4 for n in packet['new_list'].values()))
            self.assertFalse(self.call(15)['new_list'])
            self.assertTrue(self.call(1)['news_list'])

    def test_expired_map_quick_mark_and_invalid_requests_atomic(self):
        role=self.b.profile();role['month_card_time']=NOW+100;summon.add_item(role,1431,1);self.b.save(role)
        self.call(3,op_type=1,type_id=1431);self.call(3,op_type=5,type_id=1431)
        with patch('network_redirect.backend.time.time',return_value=NOW+101):
            self.assertFalse(self.call(3,op_type=1,type_id=1431)['event_data']['mark_flag'])
            before=self.b.profile()
            for op,data in ((7,dict(top_type=99)),(2,dict(des_area=81)),(14,dict(buy_hour=-1)),(17,dict(index=True,type_id=1501))):
                self.assertEqual(self.req(1329,id=op,data=summon.lua(data))[0][0],55)
                self.assertEqual(before,self.b.profile())

    def test_soul_encounter_original_monster_and_persistent_hp(self):
        from network_redirect import activity_abyss_random as events
        role=self.b.profile();e=events.create(3,self.b.activity_rules)
        e.update(npc_type=7223,hp=100000000,max_hp=100000000)
        role['activity']['abyss']['events']=[e];self.b.save(role)
        preview=self.call(4,op_type=0)['event_data']['boss_info']
        self.assertEqual(preview['cortege_type'],7223)
        self.call(4,op_type=1)
        lineup=next(d for mid,_,d in self.decoded if mid==1028)
        self.assertEqual(lineup['lineup'][0]['des_type'],7223)
        remaining=self.b.profile()['activity']['abyss']['events'][0]['hp']
        self.assertLess(remaining,100000000)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        info=self.call(4,op_type=0)['event_data']['boss_info']
        self.assertEqual((info['hp'],info['max_hp'],info['free_times']),(remaining,100000000,2))
