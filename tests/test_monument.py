import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from network_redirect.backend import Backend,login_fields
from network_redirect import monument,summon,guild
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
    def fight(self,paid=0):
        info=self.event(self.ok(1232),100);v=next(iter(info['enemy'].values()))
        return self.ok(1026,fight_type=18,des_type=v['rank'],des_id=v['player_id'],des_value=paid)
    def test_champions_empty_and_mapping(self):
        d=self.event(self.ok(1128),130)['champion_list'];self.assertEqual(set(d),{1,2,3,4,5})
        self.assertTrue(d[1]['name'].startswith('离线·1·'));self.assertEqual(d[2]['name'],'离线论道者1');self.assertEqual(d[5],{'name':'虚位以待'})
        self.assertEqual(self.b.profile()['union_id'],0)
    def test_original_numeric_switches(self):
        cfg=guild.client_config(self.b.guild_rules)['const_config']
        for k in ('open_union_match','open_world_match','open_feast'):self.assertIs(type(cfg[k]),int);self.assertGreater(cfg[k],0)
    def test_public_queries_never_join(self):
        for op,q in ((18,9),(18,10),(18,15),(58,21),(58,22),(58,30)):
            self.ok(1301,id=op,data=summon.lua(dict(query_type=q)))
        r=self.b.profile();self.assertEqual(r['union_id'],0);self.assertEqual(r['gold_coin'],10000)
        out=self.request(1301,id=45,data='{}');self.event(out,55)
    def test_config_bootstrap_and_day(self):
        cfg=login_fields(decode(self.b.bootstrap()[0])[2]['data'])[19]
        self.assertLessEqual(cfg['begin_fight_time'],NOW);self.assertGreater(cfg['end_fight_time'],NOW)
        self.assertEqual(cfg['single_free_chanllenge_limit'],10)
    def test_leaderboard_contract(self):
        d=next(d for m,d in self.ok(1236) if m==1237)
        self.assertEqual(d['top_count'],6);self.assertEqual([v['rank'] for v in d['top_list']],list(range(1,7)))
        self.assertEqual(d['top_list'][-1]['player_name'],'本地行者')
    def test_match_and_refresh_persist(self):
        a=self.event(self.ok(1232),100);b=self.event(self.ok(1234,is_charge=0),102)
        self.assertNotEqual(a['enemy'],b['enemy']);r=self.b.profile();self.assertEqual(r['single_free_flush_count'],1)
        self.assertEqual(r['single_next_flush_time'],NOW+2700)
        self.event(self.request(1234,is_charge=0),55);self.assertEqual(self.b.profile(),r)
        self.ok(1234,is_charge=1);self.assertEqual(self.b.profile()['gold_coin'],9990)
    def test_replay_and_stale_serial(self):
        self.ok(1234,is_charge=1);before=self.b.profile()
        self.assertEqual(self.b.respond(self.packet,dict(authenticated=True)),self.replies)
        self.assertEqual(self.b.profile(),before)
        old=encode(1234,dict(serial_num=self.serial-1,is_charge=1));out=self.b.respond(old,dict(authenticated=True))
        self.assertEqual(decode(out[0])[2]['id'],55);self.assertEqual(self.b.profile(),before)
    def test_failed_purchase_atomic(self):
        r=self.b.profile();r['gold_coin']=0;self.b.save(r);before=self.b.profile()
        self.event(self.request(1234,is_charge=1),55);self.assertEqual(self.b.profile(),before)
    def test_free_battle_and_limits(self):
        out=self.fight();r=self.b.profile();self.assertEqual(r['single_free_challenge'],1);self.assertGreater(r['single_score'],0)
        self.assertEqual(r['monument']['fights'],1);self.assertTrue(any(m==1027 for m,d in out))
        r['single_free_challenge']=10;self.b.save(r);before=self.b.profile()
        v=self.event(self.ok(1232),100)['enemy'][1]
        self.event(self.request(1026,fight_type=18,des_id=v['player_id'],des_type=v['rank'],des_value=0),55)
        self.assertEqual(self.b.profile()['single_score'],before['single_score'])
    def test_paid_battle_debits_once(self):
        self.fight(1);r=self.b.profile();self.assertEqual(r['gold_coin'],9980);self.assertEqual(r['single_charge_challenge'],1)
        self.assertEqual(self.b.respond(self.packet,dict(authenticated=True)),self.replies);self.assertEqual(r,self.b.profile())
    def test_invalid_target_and_flag(self):
        self.ok(1232);r=self.b.profile()
        self.event(self.request(1026,fight_type=18,des_id=123,des_type=1,des_value=0),55)
        self.event(self.request(1234,is_charge=2),55);self.assertEqual(self.b.profile(),r)
    def test_lineup(self):
        d=self.event(self.ok(1039,des_id=92001,des_type=1),11)
        self.assertEqual(d['role_name'],'离线论道者1');self.assertTrue(d['cortege_list'])
        self.assertEqual(next(iter(d['cortege_list'].values()))['type_id'],5004)
    def test_rank_claim_atomic_restart(self):
        self.event(self.request(1238),55);self.fight();self.ok(1238);r=self.b.profile()
        self.assertTrue(r['monument']['rank_claimed']);self.event(self.request(1238),55);self.assertEqual(self.b.profile(),r)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.event(self.request(1238),55);self.assertEqual(self.b.profile(),r)
    def test_streak_claim(self):
        self.ok(1232);r=self.b.profile();r['max_win_streak_count']=5;self.b.save(r)
        before=r['silver_coin'];d=self.event(self.ok(1235,streak_count=3),103)
        self.assertEqual(d['streak_count'],3);self.assertEqual(self.b.profile()['silver_coin'],before+3000)
        self.event(self.request(1235,streak_count=3),55);self.event(self.request(1235,streak_count=10),55)
        self.assertTrue(self.event(self.ok(1231),104)['got_prize'][3])
    def test_day_rollover(self):
        self.fight();self.ok(1238);r=self.b.profile();score=r['single_score']
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):self.ok(1232)
        r=self.b.profile();self.assertEqual(r['single_score'],score);self.assertEqual(r['single_free_challenge'],0)
        self.assertFalse(r['monument']['rank_claimed']);self.assertEqual(r['monument']['fights'],0)
    def test_champion_updates(self):
        self.ok(1128);r=self.b.profile();r['activity']['rank_order']=1;r['single_score']=1000;self.b.save(r)
        d=self.event(self.ok(1128),130)['champion_list'];self.assertEqual(d[1]['name'],r['role_name']);self.assertEqual(d[2]['name'],r['role_name'])
    def test_record_payload(self):
        self.fight();out=self.ok(1244,fight_type=3)
        d=self.event(out,152);self.assertIn('records',d);self.assertEqual(self.event(out,44)['fight_type'],118)
    def test_weekly_public(self):
        s=monument.weekly_html().decode();self.assertIn('【B】',s);self.assertNotIn('access_token',s)
    def test_low_level_can_view_cannot_fight(self):
        r=self.b.profile();r['level']=1;self.b.save(r)
        self.ok(1128);self.assertFalse(self.event(self.ok(1232),100)['has_qulify'])
        self.event(self.request(1234,is_charge=1),55)

    def test_three_phase_costs(self):
        start=monument.client_config(NOW,self.b.monument_rules)['begin_fight_time']
        for offset,cost in ((3600,20),(21*3600,20),(23*3600+60,100)):
            with patch('network_redirect.backend.time.time',return_value=start+offset):
                before=self.b.profile()['gold_coin'];self.fight(1)
                self.assertEqual(self.b.profile()['gold_coin'],before-cost)
        with patch('network_redirect.backend.time.time',return_value=start+23*3600+120):
            v=self.event(self.ok(1232),100)['enemy'][1]
            self.event(self.request(1026,fight_type=18,des_id=v['player_id'],des_type=v['rank'],des_value=0),55)
    def test_fortune_shared_between_champion_and_public_list(self):
        self.ok(1128);r=self.b.profile();g=r['guild']['unions']['80001']
        g['feast']={'day':r['guild']['day'],'stats':{'42':dict(id=42,name='离线赠礼者',fortune=300,contribute=20,normal_gift=1,advanced_gift=0)}}
        self.b.save(r)
        d=self.event(self.ok(1128),130);self.assertEqual(d['champion_list'][5]['name'],'离线赠礼者')
        out=self.ok(1301,id=18,data=summon.lua(dict(query_type=15)))
        self.assertTrue(any('离线赠礼者' in d.get('data','') for m,d in out));self.assertEqual(self.b.profile()['union_id'],0)

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
