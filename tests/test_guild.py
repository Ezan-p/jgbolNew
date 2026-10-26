import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from network_redirect.backend import Backend,login_fields
from network_redirect.protocol import encode,decode
from network_redirect import guild,summon,daily
NOW=1792814400
class GuildTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None);self.addCleanup(lambda:self.b.close())
        self.clock=patch('network_redirect.backend.time.time',return_value=NOW);self.clock.start();self.addCleanup(self.clock.stop)
        self.serial=1000
        r=self.b.profile();r.update(level=30,gold_coin=100000,silver_coin=100000);self.b.save(r)
    def req(self,op,**d):
        self.serial+=1;self.packet=encode(1301,dict(serial_num=self.serial,id=op,data=summon.lua(d)))
        self.replies=self.b.respond(self.packet,{'authenticated':True})
        return [(m,x['id'],login_fields(x['data'])) for m,_,x in map(decode,self.replies) if m in (2998,1301)]
    def create(self):
        out=self.req(1,union_name='测试仙盟');self.assertFalse(any(i==55 for m,i,d in out));return out
    def role(self):return self.b.profile()
    def test_config(self):
        c=login_fields(decode(self.b.bootstrap()[0])[2]['data'])[8]
        self.assertEqual(c['const_config']['create_cost_gold'],500);self.assertEqual(c['right_config'][1]['right_list'][13],True)
    def test_list_create_and_reconnect(self):
        out=self.req(18,query_type=4,page=1);self.assertEqual(len(out[-1][2]['union_list']),4)
        self.create();r=self.role();self.assertEqual(r['union_rank'],1);self.assertEqual(r['gold_coin'],99500)
        self.assertEqual(self.b.respond(self.packet,{'authenticated':True}),self.replies)
        self.assertEqual(self.role(),r)
        self.assertEqual(self.req(18,query_type=1)[-1][2]['union_info']['name'],'测试仙盟')
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.role()['union_id'],r['union_id'])
    def test_level_cost_and_name(self):
        r=self.role();r['level']=1;self.b.save(r);before=self.role();self.assertEqual(self.req(1,union_name='测试仙盟')[-1][1],55);self.assertEqual(before,self.role())
        r['level']=30;r['gold_coin']=1;self.b.save(r);self.assertEqual(self.req(1,union_name='测试仙盟')[-1][1],55)
        self.assertEqual(self.req(1,union_name='x')[-1][1],55)
        self.assertEqual(self.req(1,union_name={'bad':1})[-1][1],55)
    def test_join_permissions_leave(self):
        self.req(4,union_id=1);self.assertEqual(self.role()['union_rank'],5)
        before=self.role();self.assertEqual(self.req(19,new_notify='恶意公告')[-1][1],55);self.assertEqual(before,self.role())
        self.req(3);self.assertEqual(self.role()['union_id'],0)
    def test_tree_and_daily(self):
        self.create();self.ok(36,count=50);self.req(14)
        s=self.req(34)[-1][2];self.assertEqual(s['tree_state'],2)
        self.req(35)
        for n in range(10):
            out=self.req(15,mission_id=1,mission_type=1,cultivate_type=1,cultivate_record_time=daily.day(NOW,self.b.guild_rules),cultivate_record_count=n)
            self.assertFalse(any(i==55 for m,i,d in out))
        r=self.role();self.assertEqual(r['union_contrib'],150);self.assertEqual(r['daily']['points']['9'],5)
        self.assertEqual(self.req(15,mission_id=1,mission_type=1,cultivate_type=1,cultivate_record_time=daily.day(NOW,self.b.guild_rules),cultivate_record_count=10)[-1][1],55)
        self.assertEqual(self.role(),r)
    def test_create_has_no_daily_count_limit(self):
        for _ in range(4):
            self.create()
            self.ok(13)
        self.assertEqual(self.role()['gold_coin'],100000-4*self.b.guild_rules['create_cost_gold'])
        self.assertEqual(self.role()['guild']['create_count'],4)
        self.create()
        before=self.role()
        self.assertEqual(self.req(1,union_name='重复创建')[-1][1],55)
        self.assertEqual(self.role(),before)

    def test_team_application_keys_are_client_role_ids(self):
        self.ok(4,union_id=80001);self.ok(26)
        applicants=self.ok(50)[-1][2]
        self.assertEqual(set(applicants),{800011,800012,800013})
        self.assertEqual(self.ok(44)[-1][2]['team']['apply_list'],applicants)
        # Original showJoinTeamPage copies the table key into row.id.
        selected=next(iter(applicants))
        self.ok(28,role_list=[selected])
        self.assertIn(str(selected),self.role()['guild']['instances']['team']['members'])
        self.assertNotIn(selected,self.ok(50)[-1][2])
        before=self.role()
        self.assertEqual(self.req(28,role_list=[selected])[-1][1],55)
        self.assertEqual(self.role(),before)
        rejected=next(iter(self.ok(50)[-1][2]))
        self.ok(29,role_list=[rejected]);self.assertNotIn(rejected,self.ok(50)[-1][2])
        self.ok(30);self.assertEqual(self.ok(50)[-1][2],{})

    def test_team_bulk_accept_fills_remaining_slots_and_keeps_waiting(self):
        self.ok(4,union_id=80001)
        r=self.role();g=r['guild']['unions']['80001']
        for ident in (810001,810002):g['members'][str(ident)]=guild.offline.npc(ident,'候补道友',NOW)
        self.b.save(r);self.ok(26)
        applicants=list(self.ok(50)[-1][2])
        self.assertEqual(len(applicants),5)
        result=self.ok(28,role_list=applicants)[-1][2]['team']
        team=self.role()['guild']['instances']['team']
        self.assertEqual(team['members'],['1']+[str(v) for v in applicants[:4]])
        self.assertEqual(set(team['applications']),{str(applicants[4])})
        self.assertEqual(result['apply_list'],{})
        self.assertEqual(self.ok(50)[-1][2],{})
        self.assertEqual(len(result['teams']),self.b.guild_rules['team_size'])
        self.ok(33,role_id=applicants[0])
        self.assertEqual(set(self.ok(50)[-1][2]),{applicants[4]})
        self.ok(28,role_list=[applicants[4]])
        self.assertEqual(len(self.role()['guild']['instances']['team']['members']),5)
        self.assertEqual(self.ok(50)[-1][2],{})

    def test_team_three_applicants_all_fit_five_member_capacity(self):
        self.ok(4,union_id=80001);self.ok(26)
        ids=list(self.ok(50)[-1][2]);self.ok(28,role_list=ids)
        team=self.ok(44)[-1][2]['team']
        self.assertEqual(team['max_count'],5)
        self.assertEqual(len(team['teams']),4)
        self.assertEqual(set(self.role()['guild']['instances']['team']['members']),{'1'}|set(map(str,ids)))

    def test_team_fight_minimum_and_maximum_boundaries(self):
        self.ok(4,union_id=1);self.ok(26)
        for size in (1,2,3,4,5,6):
            with self.subTest(size=size):
                r=self.role();g=r['guild']['unions']['1'];a=r['guild']['instances']
                ids=[1]+list(range(820001,820000+size))
                for ident in ids[1:]:g['members'][str(ident)]=guild.offline.npc(ident,'试战道友',NOW)
                a['team']['members']=list(map(str,ids));a['team']['applications']={};a['team_fights']=0;self.b.save(r)
                before=self.role()
                with patch('network_redirect.guild_instances.simulate',return_value=(4,[],{})) as battle:
                    if 3<=size<=5:
                        self.ok(41,fight_list=list(reversed(ids)))
                        battle.assert_called_once()
                        self.assertEqual(self.role()['guild']['instances']['team_fights'],1)
                        self.assertEqual(self.role()['guild']['instances']['team']['members'],list(map(str,reversed(ids))))
                    else:
                        self.assertEqual(self.req(41,fight_list=ids)[-1][1],55)
                        battle.assert_not_called();self.assertEqual(self.role(),before)

    def test_team_fight_rejects_forged_or_incomplete_roster(self):
        self.ok(4,union_id=1);self.ok(26);self.ok(28,role_list=[10001,10002])
        for data in ({},{'fight_list':[1,10001]},{'fight_list':[1,10001,10001]},
                     {'fight_list':[1,10001,99999]},{'fight_list':[True,10001,10002]},
                     {'fight_list':{2:1,3:10001,4:10002}}):
            before=self.role()
            with patch('network_redirect.guild_instances.simulate') as battle:
                self.assertEqual(self.req(41,**data)[-1][1],55)
                battle.assert_not_called();self.assertEqual(self.role(),before)

    def test_team_bulk_accept_checks_every_applicant_before_mutation(self):
        self.ok(4,union_id=80001);self.ok(26)
        applicants=list(self.ok(50)[-1][2]);before=self.role()
        self.assertEqual(self.req(28,role_list=applicants+[999999])[-1][1],55)
        self.assertEqual(self.role(),before)
        self.assertEqual(self.req(28,role_list=applicants+[applicants[0]])[-1][1],55)
        self.assertEqual(self.role(),before)

    def test_match_stage_and_group_detail_contract(self):
        self.create()
        for op,q in ((18,100),(58,32)):
            data=self.ok(op,query_type=q)[-1][2]['enter_data']
            self.assertEqual(data['union_data']['match_type']-20,1)
        self.ok(45)
        for op,q in ((18,8),(58,20)):
            data=self.ok(op,query_type=q)[-1][2]
            self.assertEqual(data['match_type']-20,1)
            self.assertEqual(data['bet_list'],{})
            self.assertLess(data['bet_time_info']['begin_time'],NOW)
            self.assertGreater(data['bet_time_info']['end_time'],NOW)
            for group in (6,7):
                pair=data['lineup_list'][group][1]
                for side in ('src','des'):
                    self.assertGreater(pair[side]['leader_id'],0)
                    self.assertEqual(pair[side]['match_type']-20,1)
                    self.assertTrue(pair[side]['union_name'])

    def test_match_detail_bets_use_leader_id(self):
        self.create();self.ok(45)
        self.ok(48,bet_type=1,union_id=int(self.role()['role_id']))
        data=self.ok(18,query_type=8)[-1][2]
        self.assertEqual(data['bet_list'],{int(self.role()['role_id']):True})
        self.assertEqual(self.role()['guild']['match']['bets']['1'],self.role()['union_id'])
        r=self.role();r['guild']['match']['fights']=1;self.b.save(r)
        self.assertEqual(self.ok(18,query_type=8)[-1][2]['bet_time_info']['end_time'],0)

    def test_tree_donation_dialog_rate_and_balance(self):
        self.create();data=self.ok(34)[-1][2]
        self.assertEqual(data['donate_rate'],self.b.guild_rules['donate_money_rate'])
        before=self.role();data=self.ok(36,count=7)[-1][2];after=self.role()
        self.assertEqual(after['gold_coin'],before['gold_coin']-7)
        self.assertEqual(data['union_money'],before['guild']['unions']['2']['money']+7*data['donate_rate'])
        self.assertEqual(data['donate_count'],7)
        self.assertEqual(after['cur_union_contrib'],7*self.b.guild_rules['donate_contrib_rate'])

    def test_donate_store_limits(self):
        self.create();self.req(36,count=100);self.assertEqual(self.role()['cur_union_contrib'],100)
        self.req(38);out=self.req(40,item_id=1,buy_count=5);self.assertEqual(out[-1][2]['item_info']['buy_times'],0)
        r=self.role();self.assertEqual(r['cur_union_contrib'],0)
        self.assertEqual(self.req(40,item_id=1,buy_count=1)[-1][1],55);self.assertEqual(self.role(),r)
        self.req(39);self.assertEqual(self.req(38)[-1][2]['item_list'][1]['buy_times'],5)
        for d in ({'count':-1},{'count':1.5},{'count':True},{'count':101}):self.assertEqual(self.req(36,**d)[-1][1],55)
    def test_announcement_rename_dismiss(self):
        self.create();self.req(19,new_notify='新公告');self.req(71,new_notify='内部公告');self.req(51,new_name='新仙盟')
        info=self.req(18,query_type=1)[-1][2]['union_info'];self.assertEqual(info['notify'],'新公告');self.assertEqual(info['name'],'新仙盟')
        self.req(13);self.assertEqual(self.role()['union_id'],0)
    def test_feast_duplicate(self):
        self.create();self.req(65,feast_type=1)
        self.assertEqual(self.req(18,query_type=14)[-1][2]['feast_data']['feast_type'],1)
        self.req(68);r=self.role();self.assertEqual(self.req(68)[-1][1],55);self.assertEqual(self.role(),r)
        self.req(67,gift_type=1,count=1);self.req(66,des_id=1);r=self.role();self.assertEqual(self.req(66,des_id=1)[-1][1],55);self.assertEqual(self.role(),r)
    def test_atomic_rollback(self):
        self.create();r=self.role();r['gold_coin']=0;self.b.save(r);self.req(14);before=self.role()
        self.req(15,mission_id=1,mission_type=1,cultivate_type=2,cultivate_record_time=daily.day(NOW,self.b.guild_rules),cultivate_record_count=0)
        self.assertEqual(before,self.role())
    def test_cross_day(self):
        self.create();self.req(36,count=100)
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):self.req(36,count=100)
        self.assertEqual(self.role()['union_contrib'],200)

    def ok(self,op,**d):
        out=self.req(op,**d)
        self.assertFalse(any(m==2998 and i==55 for m,i,x in out),out)
        return out
    def test_deep_queries(self):
        self.create()
        for op,d in [(18,dict(query_type=q)) for q in (3,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,100)]+[(n,{}) for n in (35,70,73,79,88,83,95)]+[(86,dict(two_type=1)),(91,dict(two_type=1)),(92,dict(two_type=1,query_type=1))]:
            with self.subTest(op=op,d=d):self.ok(op,**d)
    def test_search_shop_and_card(self):
        self.create();self.ok(26);self.ok(43,flag=1)
        self.ok(43,flag=2);self.ok(43,flag=2);self.ok(43,flag=3);self.ok(43,flag=4,index=1)
        r=self.role();self.assertEqual(r['guild']['instances']['points'],0)
        self.assertEqual(self.req(43,flag=4,index=1)[-1][1],55);self.assertEqual(self.role(),r)
        self.ok(43,flag=6);self.assertEqual(self.req(43,flag=2)[-1][1],55)
    def test_hunt_daily_and_shop(self):
        self.create()
        for i in (1,2,3):self.ok(84,task_index=i,task_type=1,pay_type=1)
        self.assertEqual(sum(p["count"] for p in self.role()["attachments"] if p["type_id"]==1346),3)
        r=self.role();self.assertEqual(self.req(84,task_index=1,task_type=1)[-1][1],55);self.assertEqual(r,self.role())
        self.ok(91,two_type=2,index=1,buy_count=1)
        self.assertEqual(self.role()['guild']['instances']['reputation'],40)
        self.ok(92,two_type=2,query_type=1);self.assertEqual(self.req(92,two_type=2)[-1][1],55)
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            self.ok(84,task_index=1,task_type=1,pay_type=1)
        self.assertEqual(self.role()['guild']['instances']['tasks'],[1])
    def test_wander_capture_and_enclosure(self):
        self.create();self.ok(86,two_type=2)
        for _ in range(3):
            if self.role()['guild']['instances']['field'] is None:break
            self.ok(87,two_type=2)
        self.assertEqual(self.req(87,two_type=2)[-1][1],55)
        for _ in range(3):self.ok(89)
        self.assertEqual(self.req(89)[-1][1],55)
    def test_escort_timer_and_replay(self):
        self.create();self.ok(69,flag=3,road_type=1);self.ok(69,flag=4,road_type=1);self.ok(69,flag=5,road_type=1)
        self.ok(69,flag=6,road_type=1,book_level=2,des_id=0)
        r=self.role();self.assertEqual(self.req(69,flag=11)[-1][1],55);self.assertEqual(r,self.role())
        with patch('network_redirect.backend.time.time',return_value=NOW+3601):self.ok(69,flag=11)
        r=self.role();self.assertEqual(r['cur_union_contrib'],20)
        self.assertEqual(self.req(69,flag=11)[-1][1],55);self.assertEqual(r,self.role())
    def battle(self,ft,**d):
        self.serial+=1
        packet=encode(1026,dict(serial_num=self.serial,fight_type=ft,des_type=1,des_value=0,des_id=90001,**d))
        replies=self.b.respond(packet,{'authenticated':True})
        decoded=[decode(p) for p in replies]
        self.assertFalse(any(m==2998 and x['id']==55 for m,_,x in decoded),[(m,x) for m,_,x in decoded if m==2998])
        self.assertTrue(any(m==1027 for m,_,x in decoded))
        return decoded
    def test_match_battle_prize(self):
        self.create();self.ok(45);self.battle(14);self.ok(72)
        r=self.role();order=r['guild']['match']['settlement']['order'];expected=100 if order==1 else 80 if order<=3 else 50
        self.assertEqual(r['guild']['unions']['2']['popularity'],expected)
        r=self.role();self.assertEqual(self.req(72)[-1][1],55);self.assertEqual(r,self.role())
    def test_nested_battles(self):
        self.create();r=self.role()
        for ident in (830001,830002,830003,830004):r['guild']['unions']['2']['members'][str(ident)]=guild.offline.npc(ident,'试战道友',NOW)
        self.b.save(r);self.ok(26);self.ok(28,role_list=[830001,830002,830003,830004]);self.ok(41,fight_list=[1,830001,830002,830003,830004]);self.ok(42)
        self.ok(80);self.ok(95)
        self.ok(84,task_index=1,task_type=2,pay_type=1)
    def test_tree_guard(self):
        self.create();self.ok(36,count=50);self.ok(14)
        with patch('network_redirect.backend.time.time',return_value=NOW+3601):self.battle(13)
    def test_original_cost_enum(self):
        self.assertEqual(guild.missions(self.b.guild_rules)[0]['cost_type'],4)

    def test_original_luxury_feast_rewards(self):
        self.create();self.ok(65,feast_type=3);before=self.role();self.ok(68)
        after=self.role();self.assertEqual(after['strength']-before['strength'],50)
        self.assertEqual(sum(i['count'] for i in after['attachments'] if i['attach_type']==5 and i['type_id']==1029)-sum(i['count'] for i in before['attachments'] if i['attach_type']==5 and i['type_id']==1029),3)
        self.assertEqual(after['train_tree_rate'],3)
        with patch('network_redirect.backend.time.time',return_value=NOW+3601):self.ok(34)
        self.assertEqual(self.role()['train_tree_rate'],0)
    def test_cross_battle_shop_and_prize(self):
        self.create();self.ok(58,query_type=32);self.ok(58,query_type=28,des_id=90001)
        self.assertEqual(self.role()['guild']['cross_match']['fights'],1)
        r=self.role();r['guild']['cross_match']['score']=20;self.b.save(r)
        self.ok(58,query_type=33);self.ok(58,query_type=34,index=1,count=2)
        r=self.role();self.assertEqual(self.req(58,query_type=34,index=1,count=1)[-1][1],55);self.assertEqual(r,self.role())
        self.ok(76);r=self.role();self.assertEqual(self.req(76)[-1][1],55);self.assertEqual(r,self.role())
    def test_offline_team_join_permissions(self):
        self.ok(4,union_id=1);self.ok(73);self.ok(27,leader_id=10001)
        self.assertEqual(self.role()['guild']['instances']['team']['captain'],10001)
        r=self.role();self.assertEqual(self.req(32)[-1][1],55);self.assertEqual(r,self.role())
        self.ok(31);self.ok(3);self.assertIsNone(self.role()['guild']['instances']['team'])
    def test_escort_compose_consumes_fragments(self):
        from network_redirect import journey
        self.create();r=self.role()
        for tid in (1301,1302,1303):journey.grant(r,[5,tid,1,1])
        self.b.save(r);self.ok(69,flag=2,ten_pick=1);r=self.role()
        self.assertEqual(self.req(69,flag=2,ten_pick=1)[-1][1],55);self.assertEqual(r,self.role())
    def test_bad_queries_atomic(self):
        self.create()
        for op,d in ((69,{'flag':99}),(91,{'two_type':2,'index':-1,'buy_count':1}),(58,{'query_type':34,'index':1,'count':-1}),(40,{'item_id':1,'buy_count':True})):
            before=self.role();self.assertEqual(self.req(op,**d)[-1][1],55);self.assertEqual(before,self.role())
    def test_old_serial_cannot_spend(self):
        self.create();self.ok(36,count=1);packet=self.packet
        self.ok(36,count=2);before=self.role();self.b.respond(packet,{'authenticated':True});self.assertEqual(before,self.role())
    def test_escort_rob_replay(self):
        self.create();self.ok(69,flag=3,road_type=1);self.ok(69,flag=10,des_id=91001)
        r=self.role();self.assertEqual(self.req(69,flag=10,des_id=91001)[-1][1],55);self.assertEqual(r,self.role())

    def test_real_chat_wire_and_history(self):
        self.create();self.serial+=1
        p=encode(1097,dict(serial_num=self.serial,channel=6,id=0,name='',chat_msg='仙盟聊天测试'))
        out=[decode(x) for x in self.b.respond(p,{'authenticated':True})]
        self.assertEqual([d['chat_msg'] for m,_,d in out if m==1098],['仙盟聊天测试'])
        self.assertEqual(self.ok(18,query_type=7)[-1][2]['chat_list'][1]['chat_msg'],'仙盟聊天测试')
        self.assertTrue(self.ok(18,query_type=6)[-1][2]['event_list'])
        r=self.role();r['guild']['unions']['2']['forbidden']=[dict(id=r['role_id'])];self.b.save(r)
        self.serial+=1;p=encode(1097,dict(serial_num=self.serial,channel=6,id=0,name='',chat_msg='禁言测试'))
        before=self.role();self.b.respond(p,{'authenticated':True});self.assertEqual(before,self.role())
    def test_protection_card_original_request(self):
        self.create();rid=int(self.role()['role_id'])
        self.ok(69,flag=8,des_id=rid);self.ok(69,flag=7)
        self.assertEqual(self.role()['guild']['escort']['credits'],1)
        self.ok(69,flag=6,road_type=1,book_level=1,des_id=rid)
        self.assertEqual(self.role()['guild']['escort']['credits'],0)
    def test_guild_lineup_queries(self):
        self.create()
        self.ok(58,query_type=29,des_id=90001);self.ok(58,query_type=31,des_id=90001)
        self.serial+=1
        p=encode(1039,dict(serial_num=self.serial,des_type=1,des_id=90001,flag=6,fight_id=0))
        out=[decode(x) for x in self.b.respond(p,{'authenticated':True})]
        self.assertTrue(any(m==2998 and d['id']==11 for m,_,d in out))

    def test_rejoin_keeps_daily_quotas(self):
        self.ok(4,union_id=1);self.ok(84,task_index=1,task_type=1,pay_type=1)
        self.ok(3);self.ok(4,union_id=1)
        before=self.role();self.assertEqual(self.req(84,task_index=1,task_type=1,pay_type=1)[-1][1],55);self.assertEqual(before,self.role())
    def test_offline_recruitment_permissions_and_team_review(self):
        self.create()
        pending=self.role()['guild']['unions']['2']['applications']
        target=int(next(iter(pending)))
        self.ok(5,role_id=target)
        self.ok(26);out=self.ok(50)[-1][2]
        self.assertTrue(out);self.assertEqual(out[target]['id'],target)
        self.ok(28,role_list=[target])
        self.assertIn(str(target),self.role()['guild']['instances']['team']['members'])
        before=self.role();self.assertEqual(self.req(28,role_id=target)[-1][1],55);self.assertEqual(before,self.role())
        self.ok(11,role_id=target,new_rank=7)
        r=self.role();g=r['guild']['unions']['2'];rid=str(int(r['role_id']))
        g['members'][rid]['rank']=3;self.b.save(r)
        before=self.role();self.assertEqual(self.req(25,role_id=target)[-1][1],55);self.assertEqual(before,self.role())

    def test_tree_threshold_and_sweep_rollback(self):
        self.create();before=self.role()
        self.assertEqual(self.req(14)[-1][1],55);self.assertEqual(before,self.role())
        self.assertEqual(self.ok(34)[-1][2]['require_pop'],50)
        self.ok(36,count=50);self.ok(14)
        before=self.role();self.ok(43,flag=6);after=self.role()
        self.assertEqual(before['gold_coin']-after['gold_coin'],10)
        self.assertEqual(len({x['index'] for x in after['guild']['instances']['board']}),5)
        self.assertEqual(self.req(43,flag=6)[-1][1],55);self.assertEqual(after,self.role())
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            r=self.role();r['gold_coin']=0;self.b.save(r);before=self.role()
            self.assertEqual(self.req(43,flag=6)[-1][1],55);self.assertEqual(before,self.role())

    def test_store_changes_and_money_audit(self):
        self.create();self.ok(36,count=10)
        first=self.ok(38)[-1][2]['item_list']
        self.ok(39);second=self.ok(38)[-1][2]['item_list']
        self.assertNotEqual(first[1]['item'],second[1]['item'])
        log=self.role()['guild']['unions']['2']['money_log']
        self.assertEqual(log[-1]['change'],100)
        self.assertEqual(log[-1]['balance'],1100)

    def test_feast_statistics_and_expiry(self):
        self.create();self.ok(65,feast_type=1);self.ok(67,gift_type=2,count=2);self.ok(66,des_id=1)
        row=self.ok(18,query_type=15)[-1][2]['fortune_info'][1]
        self.assertEqual((row['fortune'],row['contribute'],row['advanced_gift']),(105,100,2))
        with patch('network_redirect.backend.time.time',return_value=NOW+3601):
            data=self.ok(18,query_type=14)[-1][2]['feast_data']
            self.assertFalse(data['can_rece_award']);self.assertFalse(data['gift_data'][1]['can_grab'])
            self.assertTrue(any('宴席已经结束' in s for s in self.role()['guild']['unions']['2']['events']))

    def test_beast_entities_growth_and_atomic_materials(self):
        from network_redirect import guild_offline, guild_instances
        self.create();r=self.role();a=guild_instances.state(r['guild'])
        for _ in range(3):guild_offline.add_pet(a,101,r['guild'],self.b.guild_rules)
        for p in a['pet_entities']:p['quality']=1
        a['reputation']=100;self.b.save(r)
        for _ in range(4):self.ok(23,chat_msg='/喂养 1')
        self.ok(23,chat_msg='/合成 1 2');self.ok(23,chat_msg='/升星 1')
        a=self.role()['guild']['instances'];p=a['pet_entities'][0]
        self.assertEqual((p['level'],p['quality'],p['star'],len(a['pets'])),(2,2,2,1))
        before=self.role();self.assertEqual(self.req(23,chat_msg='/合成 1 1')[-1][1],55);self.assertEqual(before,self.role())
        self.ok(23,chat_msg='/灵兽');self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.role()['guild']['instances']['pet_entities'][0],p)

    def test_capture_failure_escape_and_update_events(self):
        self.create();out=self.ok(86,two_type=2)
        self.assertTrue(any(i==93 and d['update_list'] for m,i,d in out))
        with patch('network_redirect.guild_offline.roll',return_value=99):
            for _ in range(3):out=self.ok(87,two_type=2)
        self.assertTrue(any(i==94 for m,i,d in out));self.assertIsNone(self.role()['guild']['instances']['field'])
        self.assertEqual(len(self.role()['guild']['instances']['pets']),0)
        self.ok(86,two_type=2)
        with patch('network_redirect.guild_offline.roll',return_value=0):self.ok(87,two_type=2)
        self.assertEqual(len(self.role()['guild']['instances']['pet_entities']),1)

    def test_weekly_reward_cannot_reset_by_rejoin_or_day(self):
        self.ok(4,union_id=1);self.ok(84,task_index=1,task_type=1);self.ok(92,two_type=2)
        self.ok(3);self.ok(4,union_id=1)
        self.assertEqual(self.req(92,two_type=2)[-1][1],55)
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            self.ok(83);self.assertEqual(self.req(92,two_type=2)[-1][1],55)
        with patch('network_redirect.backend.time.time',return_value=NOW+7*86400):
            self.ok(83);self.assertEqual(self.role()['guild']['instances']['week_score'],0)
            self.assertEqual(self.req(92,two_type=2)[-1][1],55)

    def test_paid_task_limit_even_with_unused_free_tasks(self):
        self.create()
        for _ in range(3):self.ok(84,task_index=1,task_type=1,pay_type=2)
        before=self.role();self.assertEqual(self.req(84,task_index=2,task_type=1,pay_type=2)[-1][1],55);self.assertEqual(before,self.role())
        self.ok(84,task_index=2,task_type=1,pay_type=1)

    def test_match_life_merit_and_streak(self):
        from network_redirect import guild_match
        self.create();self.ok(45);role=self.role();s=role['guild'];s['fight_id']=1;g=s['unions']['2'];r=self.b.guild_rules
        def result(won):return (1 if won else 4,[],dict(fight_result_msg=dict(fight_result=[])))
        for won in (True,True,False):
            with patch('network_redirect.guild_combat.simulate',return_value=result(won)):
                guild_match.fight(role,s,g,dict(fight_type=14,des_id=90001),NOW,r,self.b.journey_rules)
        m=s['match'];self.assertEqual((m['streak'],m['max_streak'],m['life'],m['merit']),(0,2,75,10))
        self.assertEqual(m['target_life']['90001'],60)
        m['life']=0
        with self.assertRaises(guild.formation.Rejected):guild_match.fight(role,s,g,dict(fight_type=14,des_id=90002),NOW,r,self.b.journey_rules)

    def test_train_persistent_damage_and_support_limit(self):
        def replay():return (4,[],dict(fight_result_msg=dict(fight_result=[dict(is_src=True,damage_list=[100])])) )
        self.create()
        with patch('network_redirect.guild_instances.simulate',side_effect=lambda *a:replay()):
            self.ok(80)
            for _ in range(3):self.ok(78)
            before=self.role();self.assertEqual(self.req(78)[-1][1],55);self.assertEqual(before,self.role())
        a=self.role()['guild']['instances'];self.assertEqual(a['train_hp'],9600)
        self.assertEqual(a['train_support'],3);self.assertEqual(sum(v['damage'] for v in a['train_damage'].values()),400)
        data=self.ok(79)[-1][2];self.assertEqual(data['rest_time'],NOW+3600)
        self.assertEqual(data['boss_info']['boss_hp'],9600)

    def test_escort_protection_raid_and_blacklist(self):
        self.ok(4,union_id=1);self.ok(69,flag=15,des_id=10001)
        self.assertEqual(self.role()['guild']['escort']['credits'],1)
        self.ok(69,flag=6,road_type=1,book_level=1,des_id=10001)
        self.assertTrue(self.role()['guild']['escort']['active']['book']['had_protector'])
        with patch('network_redirect.backend.time.time',return_value=NOW+1801),patch('network_redirect.guild_offline.roll',return_value=0):
            out=self.ok(69,flag=12)[-1][2];row=out['berob_info'][1]
            self.assertEqual(row['rob_id'],91001);self.assertEqual(row['rob_contrib'],2)
            self.ok(69,flag=14,des_id=91001)
            self.assertTrue(self.ok(69,flag=12)[-1][2]['berob_info'][1]['is_black'])
            self.assertEqual(len(self.role()['guild']['escort']['raid_log']),1)

    def test_rules_validation(self):
        import json
        p=Path(self.tmp.name)/'rules.json'
        for key,value in (('catch_success_percent',101),('search_sweep_gold',-1),('pet_types',[106]),('rank_rights',{}),('team_size',6),('team_size',2),('team_min_fighters',2),('team_min_fighters',True)):
            r=copy.deepcopy(self.b.guild_rules);r[key]=value;p.write_text(json.dumps(r))
            with self.subTest(key=key),self.assertRaises(guild.formation.Rejected):guild.load_rules(p)

    def test_delayed_npc_application_and_join_quota(self):
        self.b.guild_rules['npc_auto_accept']=False
        out=self.ok(4,union_id=1);self.assertTrue(any(i==82 and d.get('event_id')==7 for m,i,d in out))
        self.assertEqual(self.role()['union_id'],0)
        with patch('network_redirect.backend.time.time',return_value=NOW+4):
            out=self.ok(18,query_type=1)
            self.assertEqual(self.role()['union_id'],1)
            self.assertTrue(any(i==82 and d.get('event_id')==8 for m,i,d in out))
        self.b.guild_rules['npc_auto_accept']=True
        for _ in range(2):self.ok(3);self.ok(4,union_id=1)
        self.ok(3);before=self.role();self.assertEqual(self.req(4,union_id=1)[-1][1],55);self.assertEqual(before,self.role())

    def test_trial_stage_prizes_cannot_repeat(self):
        self.create();self.ok(79);r=self.role();a=r['guild']['instances'];a.update(train_open=True,train_hp=7500,train_end=NOW+3600);self.b.save(r)
        self.ok(82);self.assertEqual(self.role()['guild']['instances']['train_claimed_stage'],1)
        before=self.role();self.assertEqual(self.req(82)[-1][1],55);self.assertEqual(before,self.role())
        r=self.role();r['guild']['instances'].update(train_hp=0,train_done=True);self.b.save(r)
        self.ok(82);self.assertEqual(self.role()['guild']['instances']['reputation'],40)
        self.assertEqual(self.role()['guild']['unions']['2']['money'],1400)

    def test_capture_token_and_abandon_contract(self):
        from network_redirect import journey
        self.create();r=self.role();journey.grant(r,[5,1338,1,1]);self.b.save(r)
        self.ok(86,two_type=2);before=self.role()['gold_coin']
        with patch('network_redirect.guild_offline.roll',return_value=0):out=self.ok(87,two_type=2)
        self.assertEqual(self.role()['gold_coin'],before)
        self.assertTrue(any(i==94 and d['catch_list'][1]['type_id'] in self.b.guild_rules['pet_types'] for m,i,d in out))
        self.ok(86,two_type=2);self.ok(87,two_type=1)
        self.assertIsNone(self.role()['guild']['instances']['field'])
        self.ok(86,two_type=2)

    def test_search_board_persists_and_matches_granted_prize(self):
        self.create();first=self.ok(43,flag=1)[-1][2]
        self.assertEqual(len(first['prize_items']),25);self.assertEqual(len(set(first['search_order'].values())),25)
        second=self.ok(43,flag=1)[-1][2];self.assertEqual(first['prize_items'],second['prize_items'])
        self.ok(43,flag=2);a=self.role()['guild']['instances']
        self.assertTrue(a['search_tiles'][0]['had_token'])
        self.assertEqual(a['board'][0]['attach_type'],first['prize_items'][1]['item']['attach_type'])
        self.assertEqual(a['board'][0]['attach_count'],first['prize_items'][1]['item']['attach_count'])

    def test_old_pet_ids_migrate_to_real_types(self):
        from network_redirect import guild_instances
        self.create();r=self.role();a=guild_instances.state(r['guild']);a.pop('pet_entities');a['pets']=[1,6,106,202];self.b.save(r)
        self.ok(88);a=self.role()['guild']['instances']
        self.assertEqual(a['pets'],[101,201,201,202]);self.assertEqual(len(a['pet_entities']),4)

if __name__=='__main__':unittest.main()




