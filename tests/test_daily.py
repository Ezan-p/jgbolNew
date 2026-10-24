"""Daily/checkin binary integration tests using disposable persistent accounts."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from network_redirect import daily, summon, formation, activity, journey
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode

NOW = 1792814400  # fixed UTC+8 daytime, independent of host timezone


class DailyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.addCleanup(lambda: self.b.close())
        self.clock = patch('network_redirect.backend.time.time', return_value=NOW)
        self.clock.start(); self.addCleanup(self.clock.stop)
        self.serial = 1000

    def req(self, mid=1347, **kw):
        self.serial += 1
        self.packet = encode(mid, dict(serial_num=self.serial, **kw))
        self.replies = self.b.respond(self.packet, {'authenticated': True})
        self.assertEqual(decode(self.replies[-1])[0], 1106)
        return [(d['id'], login_fields(d['data'])) for m, _, d in map(decode, self.replies) if m == 2998]

    def role(self): return self.b.profile()
    def points(self, kind): return self.role().get('daily', {}).get('points', {}).get(str(kind), 0)

    def test_bootstrap_and_empty_query(self):
        cfg = login_fields(decode(self.b.bootstrap()[0])[2]['data'])
        self.assertEqual(len(cfg[3]), 7); self.assertEqual(cfg[9][1]['day_index'], 3)
        out = self.req(id=1, data='{}')[-1][1]
        self.assertEqual(out['point'], 0); self.assertEqual(len(out['point_data']), 9)
        self.assertEqual([b['status'] for b in out['point_prize'].values()], [1]*5)
        self.assertEqual(self.req(1206, checkin_type=1)[-1][1]['checkin_data']['checkin_day_count'], 0)

    def test_checkin_duplicate_new_serial_and_restart(self):
        before = self.role()
        out = self.req(1206, checkin_type=3, day_index=999999)[-1][1]
        self.assertEqual(out['checkin_result'], 1)
        self.assertEqual(self.role()['gold_coin'] - before['gold_coin'], 10)
        self.assertEqual(self.points(1), 10)
        after = self.role()
        self.assertEqual(self.b.respond(self.packet, {'authenticated': True}), self.replies)
        self.assertEqual(self.req(1206, checkin_type=3)[-1][1]['checkin_result'], 2)
        self.assertEqual(after, self.role())
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.assertEqual(self.req(1206, checkin_type=3)[-1][1]['checkin_result'], 2)
        self.assertEqual(after, self.role())

    def test_midnight_and_lifetime_bonus(self):
        r = self.b.daily_rules
        midnight = (daily.day(NOW, r) + 1)*86400-r['timezone_offset_hours']*3600
        with patch('network_redirect.backend.time.time', return_value=midnight-1):
            self.req(1206, checkin_type=3)
        with patch('network_redirect.backend.time.time', return_value=midnight):
            self.assertEqual(self.req(id=1, data='{}')[-1][1]['point'], 10)
            self.req(1206, checkin_type=3)
            self.assertEqual(self.role()['daily']['checkin_count'], 2)
            self.assertEqual(self.req(1206, checkin_type=2, day_index=3)[-1][1]['checkin_result'], 3)
        with patch('network_redirect.backend.time.time', return_value=midnight+86400):
            self.req(1206, checkin_type=3)
            data = self.req(1206, checkin_type=1)[-1][1]['checkin_data']
            self.assertEqual(data['checkin_take_bonus'], {3: True})
            self.assertEqual(self.req(1206, checkin_type=2, day_index=3)[-1][1]['checkin_result'], 1)
            after = self.role()
            self.assertEqual(self.req(1206, checkin_type=2, day_index=3)[-1][1]['checkin_result'], 2)
            self.assertEqual(after, self.role())

    def test_seventh_tier_no_reset_on_missed_day(self):
        for i in range(9):
            with patch('network_redirect.backend.time.time', return_value=NOW+i*2*86400):
                before = self.role()['gold_coin']; self.req(1206, checkin_type=3)
                self.assertEqual(self.role()['gold_coin']-before, self.b.daily_rules['checkin'][min(i,6)]['gold_count'])
        self.assertEqual(self.role()['daily']['checkin_count'], 9)

    def test_all_boxes_caps_preview_claims_and_reset(self):
        role = self.role()
        for i in range(1,10): daily.record(role, i, 1000, NOW, self.b.daily_rules)
        self.b.save(role)
        out = self.req(id=1, data='{}')[-1][1]
        self.assertEqual(out['point'], 110)
        for i in range(1,6):
            before = self.role(); out = self.req(id=2, data=summon.lua({'prize_id': i}))[-1][1]
            self.assertEqual(out['status'], 3); self.assertTrue(out['prize_list'])
            after = self.role(); self.assertNotEqual(before, after)
            self.assertEqual(self.req(id=2, data=summon.lua({'prize_id': i}))[-1][0],55)
            self.assertEqual(after, self.role())
        self.assertEqual(self.req(id=1, data='{}')[-1][1]['point'],110)
        with patch('network_redirect.backend.time.time', return_value=NOW+7*86400):
            out = self.req(id=1, data='{}')[-1][1]
            self.assertEqual(out['point'],0)
            self.assertTrue(all(b['status']==1 for b in out['point_prize'].values()))

    def test_invalid_and_unearned_claims_are_atomic(self):
        self.req(id=1, data='{}')
        for data in ['{prize_id=1,point=100000}', '{prize_id=-1}', '{prize_id=1.5}', '{prize_id=true}', '{prize_id=100}', 'os.execute("false")']:
            before = self.role(); self.assertEqual(self.req(id=2, data=data)[-1][0],55)
            self.assertEqual(before,self.role())
        self.assertEqual(self.req(id=3,data='{has_prize=true}')[-1][0],55)

    def test_encode_failure_rolls_back_rewards_and_flags(self):
        before = self.role()
        with patch('network_redirect.backend.encode', side_effect=ValueError('injected wire failure')):
            # complete also uses encode, so call the transaction with a mocked completion only.
            with patch.object(self.b, 'complete', side_effect=lambda serial, replies: replies):
                p = encode(1206, dict(serial_num=12345,checkin_type=3))
                self.b.respond(p, {'authenticated':True})
        self.assertEqual(before,self.role())

    def test_stale_or_altered_serial_does_not_repeat(self):
        self.req(1206,checkin_type=3); before=self.role()
        p=encode(1206,dict(serial_num=self.serial,checkin_type=2,day_index=3))
        self.assertEqual(login_fields(decode(self.b.respond(p,{'authenticated':True})[0])[2]['data'])['op_string'],'日常请求已过期，请刷新后重试')
        self.assertEqual(before,self.role())

    def test_real_activity_refresh_visit_and_divination(self):
        role=self.role();role.update(level=99,silver_coin=10000000,gold_coin=10000)
        self.b.save(role)
        self.req(1029,flag=1);self.assertEqual(self.points(3),0)
        self.req(1029,flag=2);self.assertEqual(self.points(3),5)
        self.b.respond(self.packet,{'authenticated':True});self.assertEqual(self.points(3),5)
        self.req(1030,visit_index=1,op_type=1);self.assertEqual(self.points(8),0)
        self.req(1030,visit_index=1,op_type=2);self.assertEqual(self.points(8),5)
        self.req(1030,visit_index=1,op_type=2);self.assertEqual(self.points(8),5)
        self.req(1337,event_type=1,data='{}');self.assertEqual(self.points(6),0)
        self.req(1337,event_type=2,data='{}');self.assertEqual(self.points(6),2)
        self.req(1337,event_type=3,data='{}');self.assertEqual(self.points(6),10)

    def test_tracking_does_not_count_queries_and_cross_day_old_totals(self):
        role=self.role();before=copy.deepcopy(role)
        daily.track(role,before,1029,{'flag':1},[],NOW,self.b.daily_rules,login_fields)
        self.assertEqual(daily.snapshot(role,NOW,self.b.daily_rules)['point'],0)
        before['activity']={'day':daily.day(NOW,self.b.daily_rules)-1,'rape_refreshes':5}
        role['activity']={'day':daily.day(NOW,self.b.daily_rules),'rape_refreshes':1}
        daily.track(role,before,1029,{'flag':2},[],NOW,self.b.daily_rules,login_fields)
        self.assertEqual(role['daily']['points']['3'],5)

    def test_real_journey_and_sweep_only_count_accepted_attempts(self):
        self.req(1026,fight_type=1,des_type=1,des_id=101)
        self.assertEqual(self.points(2),2)
        self.req(1026,fight_type=1,des_type=1,des_id=99999)
        self.assertEqual(self.points(2),2)
        role=self.role();role.update(level=30,strength=100)
        self.b.save(role)
        self.req(1061,tollgate_type=1,tollgate_id=101,sweep_count=3)
        self.assertEqual(self.points(2),8)
        self.req(1061,tollgate_type=1,tollgate_id=101,sweep_count=3)
        self.assertEqual(self.points(2),8)

    def test_real_party_travel_and_finished_duty(self):
        role=self.role();role.update(level=60,gold_coin=100000,silver_coin=100000,energy=100)
        for c in role['corteges']:c['level']=200
        self.b.save(role)
        self.req(1026,fight_type=6);self.assertEqual(self.points(5),5)
        self.req(1302,id=1,data='{}');self.assertEqual(self.points(7),0)
        self.req(1302,id=3,data='{}');self.assertEqual(self.points(7),2)
        self.req(1302,id=3,data='{}');self.assertEqual(self.points(7),2)
        self.req(1043,flag=0);self.req(1043,plus_type=1,plus_index=1)
        for _ in range(100):
            d=self.role()['activity']['duty']
            if d['phase']=='finished':break
            if d.get('pending_silver',0):self.req(1043,plus_type=3)
            elif d['phase']=='exchange':self.req(1043,plus_type=2,plus_index=1)
            else:self.req(1026,fight_type=5,des_type=3,des_value=d['round'])
        self.assertEqual(self.role()['activity']['duty']['phase'],'finished')
        self.assertEqual(self.points(4),10)
        self.req(1043,flag=1);self.assertEqual(self.points(4),10)

    def test_heartbeat_and_reconnect_restore_hint_without_opening_panel(self):
        role=self.role();daily.record(role,2,10,NOW,self.b.daily_rules);self.b.save(role)
        hints=[login_fields(d['data']) for m,_,d in map(decode,self.b.bootstrap()) if m==2998 and d['id']==198]
        self.assertEqual(hints,[{'id':3,'has_prize':True}])
        with patch('network_redirect.backend.time.time',return_value=NOW+7*86400):
            packets=self.b.respond(encode(2999,{}),{'authenticated':True})
            hints=[login_fields(d['data']) for m,_,d in map(decode,packets) if m==2998 and d['id']==198]
            self.assertEqual(hints,[{'id':3,'has_prize':False}])

    def test_config_validation(self):
        for change in [lambda r:r.update(mode='official'),lambda r:r['tasks'].pop(),
                       lambda r:r['point_prizes'][0].update(point=0),
                       lambda r:r['checkin'].pop(),lambda r:r['checkin_bonus'][0].update(prize=[5,999999,1,1])]:
            r=copy.deepcopy(self.b.daily_rules);change(r)
            path=Path(self.tmp.name)/'bad.json';path.write_text(json.dumps(r))
            with self.assertRaises(formation.Rejected):daily.load_rules(path)

    def test_highest_box_reachable_without_deferred_union_tree(self):
        role=self.role()
        for kind in range(1,9):daily.record(role,kind,1000,NOW,self.b.daily_rules)
        self.b.save(role)
        out=self.req(id=1,data='{}')[-1][1]
        self.assertEqual(out['point'],105)
        self.assertEqual(out['point_data'][9]['cur_point'],0)
        self.assertEqual(self.req(id=2,data='{prize_id=5}')[-1][1]['status'],3)

    def test_daily_limits_reset_but_weekly_total_and_claims_survive(self):
        role=self.role();daily.record(role,2,20,NOW,self.b.daily_rules);self.b.save(role)
        self.req(id=2,data='{prize_id=1}')
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            out=self.req(id=1,data='{}')[-1][1]
            self.assertEqual(out['point'],20)
            self.assertEqual(out['point_data'][2]['cur_point'],0)
            self.assertEqual(out['point_prize'][1]['status'],3)
            self.req(1206,checkin_type=3)
            self.assertEqual(self.req(id=1,data='{}')[-1][1]['point'],30)
            self.assertEqual(self.req(id=2,data='{prize_id=1}')[-1][0],55)

    def test_exact_monday_midnight_resets_weekly_rewards(self):
        r=self.b.daily_rules
        monday=((daily.week(NOW,r)+1)*7-3)*86400-r['timezone_offset_hours']*3600
        self.assertEqual(daily.week(monday,r),daily.week(monday-1,r)+1)
        with patch('network_redirect.backend.time.time',return_value=monday-1):
            role=self.role();daily.record(role,2,10,monday-1,r);self.b.save(role)
            self.req(1206,checkin_type=3)
            self.req(id=2,data='{prize_id=1}')
        with patch('network_redirect.backend.time.time',return_value=monday):
            out=self.req(id=1,data='{}')[-1][1]
            self.assertEqual(out['point'],0)
            self.assertEqual(out['point_prize'][1]['status'],1)
            self.assertEqual(self.role()['daily']['checkin_count'],1)
            self.req(1206,checkin_type=3)
            role=self.role();daily.record(role,2,5,monday,r);self.b.save(role)
            self.assertEqual(self.req(id=2,data='{prize_id=1}')[-1][1]['status'],3)

if __name__=='__main__':unittest.main()
