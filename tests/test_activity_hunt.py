"""Real 1226 packets: geometry, economy, resets, rewards and atomic persistence."""
import copy
import json
from pathlib import Path
from unittest.mock import patch
from test_activity import ActivityCase, NOW
from network_redirect import activity_hunt as h, activity_hunt_geometry as g, summon, formation
from network_redirect.backend import Backend
from network_redirect.protocol import encode, decode


class HuntTests(ActivityCase):
    def call(self,flag=1,**kw):return self.req(1226,flag=flag,**dict(dict(count=0,index=0),**kw))
    def data(self,events):
        self.ok(events);return next(v for e,v in events if e==155)
    def setup_hunt(self,**values):
        self.data(self.call());r=self.b.profile();r['activity']['hunt'].update(values);self.b.save(r)
    def hunt(self):return self.b.profile()['activity']['hunt']
    def amount(self,tid):return sum(v['count'] for v in self.b.profile()['attachments'] if v['attach_type']==5 and v['type_id']==tid)
    def use(self,tid,n=1):
        r=self.b.profile();summon.add_item(r,tid,n);self.b.save(r)
        i=next(v for v in r['attachments'] if v['attach_type']==5 and v['type_id']==tid)
        return self.req(1051,item_type=tid,item_id=i['id'],item_count=n,des_type=1,des_id=r['role_id'])

    def test_original_tables_status_level_and_entry(self):
        d=self.data(self.call())
        self.assertEqual(d['role_hunt_data']['left_energy'],400)
        self.assertEqual(h.BALLS,{1:dict(need_energy=20,bump_times=1),2:dict(need_energy=40,bump_times=3),3:dict(need_energy=60,bump_times=5)})
        self.assertEqual([v['soul_value'] for v in h.SOULS.values()],[20,40,60,100,200])
        status=next(v for e,v in self.req(1205,flag=0) if e==47)['hunt_data']
        self.assertTrue(status['is_open']);self.assertLess(status['begin_time'],NOW);self.assertGreater(status['end_time'],NOW)
        r=self.b.profile();r['level']=19;self.b.save(r)
        self.assertEqual(self.call()[0][0],55)

    def test_generated_boards_and_every_angle(self):
        for _ in range(30):
            board=g.board(h.SOULS);self.assertTrue(11<=len(board)<=16)
            self.assertTrue(all(g.inside(p['x'],p['y'],35) for p in board))
            self.assertTrue(all((a['x']-b['x'])**2+(a['y']-b['y'])**2>=65**2
                                for i,a in enumerate(board) for b in board[i+1:]))
        board=[dict(x=0,y=180,soul_type=1),dict(x=0,y=280,soul_type=2)]
        for angle in range(30,151):
            for ball in h.BALLS.values():
                move,caught=g.trace(board,angle,ball['bump_times'],30)
                path=move['move_path'];self.assertLessEqual(len(path),ball['bump_times']+2)
                self.assertTrue(all(g.inside(p['x'],p['y']) for p in path[1:]))
                self.assertEqual(sum(len(p['soul_list']) for p in path),len(caught))

    def test_aiming_combo_clear_and_energy_debit(self):
        self.setup_hunt(points=[dict(x=0,y=180,soul_type=1),dict(x=0,y=280,soul_type=2)])
        d=self.data(self.call(2,count=1,index=90));move=d['move_result']
        self.assertEqual(move['base_soul'],60);self.assertEqual(move['extra_soul'],6)
        self.assertTrue(move['board_cleared']);self.assertEqual(self.hunt()['soul'],66)
        self.assertEqual(self.hunt()['day_score'],66);self.assertEqual(self.hunt()['week_score'],66)
        self.assertEqual(self.hunt()['energy'],380);self.assertEqual(self.hunt()['shots'],1)
        self.assertGreaterEqual(len(d['role_hunt_data']['point_list']),11)

    def test_miss_partial_hit_trap_and_unique_captures(self):
        board=[dict(x=0,y=180,soul_type=3),dict(x=300,y=400,soul_type=5)]
        self.setup_hunt(points=board)
        d=self.data(self.call(2,count=3,index=90))
        self.assertEqual(d['move_result']['base_soul'],60)
        self.assertNotIn('point_list',d['role_hunt_data'])
        self.assertEqual(self.hunt()['points'],board[1:])
        move,caught=g.trace([],30,5,30)
        self.assertFalse(caught)
        self.assertTrue(any(g.trace([],angle,5,30)[0]['trap_hit'] for angle in range(30,151)))

    def test_all_tiers_cost_and_reject_forged_values(self):
        self.setup_hunt(points=[dict(x=300,y=400,soul_type=1)])
        for ball,cost in [(1,20),(2,40),(3,60)]:
            before=self.hunt()['energy'];self.data(self.call(2,count=ball,index=90))
            self.assertEqual(before-self.hunt()['energy'],cost)
        for ball,angle in [(0,90),(4,90),(1,29),(1,151),(1,4294967295)]:
            before=self.b.profile();self.assertEqual(self.call(2,count=ball,index=angle)[0][0],55);self.assertEqual(before,self.b.profile())
        for values in [dict(energy=19),dict(energy=400,shots=100)]:
            self.setup_hunt(**values);before=self.b.profile()
            self.assertEqual(self.call(2,count=1,index=90)[0][0],55);self.assertEqual(before,self.b.profile())

    def test_energy_exchange_caps_and_no_rank_inflation(self):
        self.setup_hunt(soul=10000)
        self.data(self.call(3,count=600));self.assertEqual(self.hunt()['energy'],1000);self.assertEqual(self.hunt()['soul'],4000)
        self.assertEqual(self.hunt()['day_score'],0)
        for n in [0,1,1001]:
            before=self.b.profile();self.assertEqual(self.call(3,count=n)[0][0],55);self.assertEqual(before,self.b.profile())

    def test_map_refresh_limit_and_restart_preserves_board(self):
        self.setup_hunt()
        for _ in range(3):self.data(self.call(4))
        self.assertEqual(self.call(4)[0][0],55);before=self.b.profile()
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(before,self.b.profile());self.assertEqual(self.data(self.call())['role_hunt_data']['left_flush_times'],0)

    def test_shop_all_six_goods_limits_and_paid_refresh(self):
        self.setup_hunt(soul=100000)
        self.assertEqual(len(self.data(self.call(5))['store_data']['item_list']),6)
        for index,row in enumerate(h.load_rules()['shop'],1):
            tid=row['reward'][1];before=self.amount(tid);n=row['limit']
            d=self.data(self.call(6,index=index,count=n));self.assertEqual(d['buy_times'],0)
            self.assertEqual(self.amount(tid)-before,n*row['reward'][2])
            self.assertEqual(self.call(6,index=index,count=1)[0][0],55)
        balance=self.hunt()['soul'];self.data(self.call(7));self.assertEqual(self.hunt()['soul'],balance-200)
        self.assertEqual(self.hunt()['bought'],{})

    def test_separate_midnight_and_six_am_resets(self):
        self.setup_hunt(soul=5000,energy=0,shots=7,refreshes=2)
        self.data(self.call(6,index=1,count=1))
        midnight=(h.day(NOW,self.b.activity_rules)+1)*86400-28800
        with patch('network_redirect.backend.time.time',return_value=midnight):
            self.data(self.call());s=self.hunt();self.assertEqual(s['energy'],400);self.assertEqual(s['shots'],0)
            self.assertEqual(s['refreshes'],0);self.assertEqual(s['bought'],{'1':1})
        with patch('network_redirect.backend.time.time',return_value=midnight+21600):
            self.data(self.call(5));self.assertEqual(self.hunt()['bought'],{})
        with patch('network_redirect.backend.time.time',return_value=midnight+10*86400):
            self.data(self.call());self.assertEqual(self.hunt()['energy'],1000)

    def test_daily_original_mail_reward_once_and_claim(self):
        self.setup_hunt(day_score=100000)
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            self.data(self.call());self.data(self.call())
            mails=[m for k,m in self.b.profile()['welfare']['mails'].items() if k.startswith('hunt-day-')]
            self.assertEqual(len(mails),1);self.assertEqual(mails[0]['prizes'],h.rewards('day',1))
            before=self.amount(1036);self.ok(self.req(1103,mail_id=mails[0]['mail_id']))
            self.assertEqual(self.amount(1036)-before,15)
            self.req(1103,mail_id=mails[0]['mail_id']);self.assertEqual(self.amount(1036)-before,15)

    def test_weekly_original_reward_title_claim_and_history(self):
        self.setup_hunt(week_score=100000,day_score=100000)
        monday=((self.hunt()['week']+1)*7+4)*86400-28800
        with patch('network_redirect.backend.time.time',return_value=monday):
            d=self.data(self.call(10));self.assertTrue(d['had_prize']);self.assertFalse(d['had_got_prize'])
            self.assertEqual(d['my_order']['order'],1);title=self.b.profile()['profile_titles']['133']
            self.assertEqual(title['begintime'],monday);self.assertEqual(title['endtime'],monday+604800)
            self.data(self.call(11));self.assertEqual(self.call(11)[0][0],55)
            self.assertTrue(self.data(self.call(10))['had_got_prize'])
            for flag in [8,9,12,13]:self.data(self.call(flag))
            self.assertEqual(self.data(self.call(13))['my_order']['soul_count'],100000)

    def test_long_absence_no_phantom_awards_and_unclaimed_mail(self):
        self.setup_hunt(week_score=100000,day_score=100000)
        with patch('network_redirect.backend.time.time',return_value=NOW+30*86400):
            self.data(self.call())
            mails=[m for k,m in self.b.profile()['welfare']['mails'].items() if k.startswith('hunt-')]
            self.assertEqual(len(mails),2);self.assertFalse(self.data(self.call(10))['had_prize'])
            self.assertNotIn('133',self.b.profile()['profile_titles'])

    def test_card_and_both_reward_boxes_consumable(self):
        self.setup_hunt();self.ok(self.use(1036,3));self.assertEqual(self.hunt()['soul'],300)
        self.assertEqual(self.hunt()['day_score'],0)
        for box,pool in [(1037,list(range(5001,5006))),(1324,[1310,1311,1312,1313,1314,1320,1321,1322,1323])]:
            before=sum(self.amount(t) for t in pool);self.ok(self.use(box,10))
            self.assertEqual(sum(self.amount(t) for t in pool)-before,10)

    def test_duplicate_serial_changed_payload_and_encoding_rollback(self):
        self.setup_hunt();self.data(self.call(2,count=1,index=90))
        before=self.b.profile();packet=self.packet;replies=self.replies
        self.assertEqual(self.b.respond(packet,self.state),replies)
        self.assertEqual(before,self.b.profile())
        bad=encode(1226,dict(serial_num=self.serial,flag=2,count=3,index=90))
        self.assertEqual(decode(self.b.respond(bad,self.state)[0])[2]['id'],55)
        with patch('network_redirect.backend.activity.attributes',side_effect=ValueError('encoding failed')):
            self.assertEqual(self.call(2,count=1,index=90)[0][0],55)
        self.assertEqual(before,self.b.profile())

    def test_clock_rollback_and_bad_config(self):
        self.setup_hunt();before=self.b.profile()
        with patch('network_redirect.backend.time.time',return_value=NOW-1):self.assertEqual(self.call(2,count=1,index=90)[0][0],55)
        self.assertEqual(before,self.b.profile())
        for key,value in [('mode','official'),('daily_shots',0),('energy_exchange_rate',0),('capture_radius',100)]:
            r=h.load_rules();r[key]=value;p=Path(self.tmp.name)/'bad.json';p.write_text(json.dumps(r))
            with self.assertRaises(formation.Rejected):h.load_rules(p)
