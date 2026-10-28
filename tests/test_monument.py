import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from network_redirect.backend import Backend,login_fields
from network_redirect import monument,summon,guild,monument_wealth
from network_redirect.protocol import encode,decode
NOW=1792900800

class MonumentTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None);self.addCleanup(lambda:self.b.close())
        self.clock=patch('network_redirect.backend.time.time',return_value=NOW);self.clock.start();self.addCleanup(self.clock.stop)
        r=self.b.profile();r.update(level=30,gold_coin=10000,silver_coin=10000);self.b.save(r);self.serial=1000
    def request(self,mid,**d):
        self.serial+=1;self.packet=encode(mid,dict(serial_num=self.serial,**d))
        self.replies=self.b.respond(self.packet,dict(authenticated=True))
        return [(m,d) for m,_,d in map(decode,self.replies)]
    def event(self,out,event):
        return next(login_fields(d['data']) for m,d in out if m==2998 and d['id']==event)
    def ok(self,mid,**d):
        out=self.request(mid,**d)
        self.assertFalse(any(m==2998 and d['id']==55 for m,d in out),out)
        return out
    def test_champions_empty_and_mapping(self):
        d=self.event(self.ok(1128),130)['champion_list'];self.assertEqual(set(d),{1,2,3,4,5})
        from network_redirect import activity_rank
        champion=activity_rank.opponent(self.b.profile()['activity'],1)
        self.assertEqual(d[1]['name'],champion['name']);self.assertEqual(d[2]['name'],'离线论道者1');self.assertEqual(d[5]['name'],monument_wealth.ranking(self.b.profile(),NOW)['fortune_info'][0]['name'])
        self.assertEqual(self.b.profile()['union_id'],0)
    def test_original_numeric_switches(self):
        cfg=guild.client_config(self.b.guild_rules)['const_config']
        for k in ('open_union_match','open_world_match','open_feast'):self.assertIs(type(cfg[k]),int);self.assertGreater(cfg[k],0)
    def test_public_queries_never_join(self):
        self.ok(1301,id=18,data=summon.lua(dict(query_type=15)))
        for op,q in ((18,9),(18,10),(58,21),(58,22),(58,30)):
            before=self.b.profile()
            error=self.event(self.request(1301,id=op,data=summon.lua(dict(query_type=q))),55)
            self.assertEqual(error['op_string'],guild.WAR_CLOSED)
            self.assertEqual(self.b.profile(),before)
        r=self.b.profile();self.assertEqual(r['union_id'],0);self.assertEqual(r['gold_coin'],10000)
        out=self.request(1301,id=45,data='{}');self.event(out,55)
    def test_config_bootstrap_and_day(self):
        cfg=login_fields(decode(self.b.bootstrap()[0])[2]['data'])[19]
        self.assertLessEqual(cfg['begin_fight_time'],NOW);self.assertGreater(cfg['end_fight_time'],NOW)
        self.assertEqual(cfg['single_free_chanllenge_limit'],10)
    def test_failed_purchase_atomic(self):
        r=self.b.profile();r['gold_coin']=0;self.b.save(r);before=self.b.profile()
        self.event(self.request(1234,is_charge=1),55);self.assertEqual(self.b.profile(),before)
    def test_lineup(self):
        d=self.event(self.ok(1039,des_id=92001,des_type=1),11)
        self.assertEqual(d['role_name'],'离线论道者1');self.assertTrue(d['cortege_list'])
        self.assertEqual(next(iter(d['cortege_list'].values()))['type_id'],5004)
    def test_champion_updates(self):
        self.ok(1128);r=self.b.profile();r['activity']['rank_order']=1;r['single_score']=1000;self.b.save(r)
        d=self.event(self.ok(1128),130)['champion_list'];self.assertEqual(d[1]['name'],r['role_name']);self.assertEqual(d[2]['name'],r['role_name'])
    def test_weekly_public(self):
        s=monument.weekly_html().decode();self.assertIn('【B】',s);self.assertNotIn('access_token',s)

    def test_fortune_shared_between_champion_and_public_list(self):
        initial=self.event(self.ok(1128),130)['champion_list'][5]
        r=self.b.profile();monument_wealth.record(r,NOW,advanced_gift=1000);self.b.save(r)
        self.assertEqual(self.event(self.ok(1128),130)['champion_list'][5],initial)
        with patch('network_redirect.backend.time.time',return_value=NOW+7*86400):
            champion=self.event(self.ok(1128),130)['champion_list'][5]
            out=self.ok(1301,id=18,data=summon.lua(dict(query_type=15)))
            data=next(login_fields(d['data']) for m,d in out if m==1301)
            self.assertEqual(champion['name'],r['role_name'])
            self.assertEqual(data['fortune_info'][1]['name'],champion['name'])
            self.assertEqual(data['fortune_info'][1]['fortune'],50000)
        self.assertEqual(self.b.profile()['union_id'],0)

    def test_cross_tournament_disabled_for_all_levels_and_operations(self):
        for level in (1,30,99):
            r=self.b.profile();r['level']=level;self.b.save(r);before=self.b.profile()
            for mid,data in [(1231,{}),(1232,{}),(1233,{}),(1234,{'is_charge':1}),
                             (1235,{'streak_count':3}),(1236,{}),(1238,{}),
                             (1026,{'fight_type':18,'des_id':92001,'des_type':1,'des_value':1}),
                             (1244,{'fight_type':3})]:
                self.assertEqual(self.event(self.request(mid,**data),55)['op_string'],'离线模式，暂未开启')
                self.assertEqual(before,self.b.profile())
                repeated=[(m,d) for m,_,d in map(decode,self.b.respond(self.packet,dict(authenticated=True)))]
                self.assertEqual(self.event(repeated,55)['op_string'],'离线模式，暂未开启')
                self.assertEqual(before,self.b.profile())

class MonumentHTTPTests(unittest.IsolatedAsyncioTestCase):
    async def test_weekly_get_and_head(self):
        import asyncio
        from network_redirect.server import LandingServer
        server=LandingServer(0,b'',lambda *a,**k:None)
        await server.start()
        try:
            for method in ('GET','HEAD'):
                reader,writer=await asyncio.open_connection('127.0.0.1',server.port)
                writer.write((method+' /dailypaper HTTP/1.1\r\nHost: jgb.syyx.com\r\nConnection: close\r\n\r\n').encode());await writer.drain()
                data=await reader.read();writer.close();await writer.wait_closed()
                header,body=data.split(b'\r\n\r\n',1)
                self.assertIn(b'200 OK',header);self.assertIn(b'text/html; charset=utf-8',header)
                self.assertEqual(body,monument.weekly_html() if method=='GET' else b'')
        finally:await server.close()
