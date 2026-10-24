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
        out=self.req(18,query_type=4,page=1);self.assertEqual(len(out[-1][2]['union_list']),1)
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
        self.create();self.req(14)
        s=self.req(34)[-1][2];self.assertEqual(s['tree_state'],2)
        self.req(35)
        for n in range(10):
            out=self.req(15,mission_id=1,mission_type=1,cultivate_type=1,cultivate_record_time=daily.day(NOW,self.b.guild_rules),cultivate_record_count=n)
            self.assertFalse(any(i==55 for m,i,d in out))
        r=self.role();self.assertEqual(r['union_contrib'],100);self.assertEqual(r['daily']['points']['9'],5)
        self.assertEqual(self.req(15,mission_id=1,mission_type=1,cultivate_type=1,cultivate_record_time=daily.day(NOW,self.b.guild_rules),cultivate_record_count=10)[-1][1],55)
        self.assertEqual(self.role(),r)
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
        r=self.role();self.assertEqual(self.req(84,task_index=1,task_type=1)[-1][1],55);self.assertEqual(r,self.role())
        self.ok(91,two_type=2,index=1,buy_count=1)
        self.assertEqual(self.role()['guild']['instances']['reputation'],10)
        self.ok(92,two_type=2,query_type=1);self.assertEqual(self.req(92,two_type=2)[-1][1],55)
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            self.ok(84,task_index=1,task_type=1,pay_type=1)
        self.assertEqual(self.role()['guild']['instances']['tasks'],[1])
    def test_wander_capture_and_enclosure(self):
        self.create();self.ok(86,two_type=2);self.ok(87,two_type=1);self.ok(87,two_type=2)
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
        self.assertEqual(self.role()['guild']['unions']['2']['popularity'],100)
        r=self.role();self.assertEqual(self.req(72)[-1][1],55);self.assertEqual(r,self.role())
    def test_nested_battles(self):
        self.create();self.ok(26);self.ok(41);self.ok(42)
        self.ok(80);self.ok(95)
        self.ok(84,task_index=1,task_type=2,pay_type=1)
    def test_tree_guard(self):
        self.create();self.ok(14)
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
if __name__=='__main__':unittest.main()




