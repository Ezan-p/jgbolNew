import copy
from pathlib import Path
import tempfile
import json
from unittest.mock import patch

from test_activity import ActivityCase
from network_redirect import activity_monday as m, formation, summon
from network_redirect.backend import Backend
from network_redirect.protocol import decode, encode

MONDAY = 1792987200  # 2026-10-26 12:00 UTC+8
SUNDAY = MONDAY - 86400


class MondayTests(ActivityCase):
    def setUp(self):
        super().setUp()
        # ActivityCase stores the patcher rather than its mock.
        self.clock.stop()
        self.timer = patch('network_redirect.backend.time.time', return_value=SUNDAY)
        self.time = self.timer.start(); self.addCleanup(self.timer.stop)

    def call(self, flag=1, level=0, op_type=0):
        return self.req(1219, flag=flag, level=level, op_type=op_type)

    def data(self, events, eid=112):
        self.ok(events)
        return next(d for e, d in events if e == eid)

    def task(self, kind):
        role = self.b.profile(); s = m.state(role, int(self.time.return_value), m.load_rules())
        s['task'].update(cur_task=kind, finish_time=0, recv_time=0)
        self.b.save(role)

    def test_entry_four_slots_closed_and_monday(self):
        d = self.data(self.call())
        self.assertIn(7, d['week_prize_config'])
        self.assertEqual(len(d['activity_data']['show_list']), 4)
        self.assertEqual(d['activity_data']['prize_list'], {1:10,2:20,3:30,4:40})
        self.assertEqual(self.call(3,1)[-1][0],55)
        self.time.return_value=MONDAY
        d = self.data(self.call())
        self.assertIn(1,d['week_prize_config'])
        self.assertEqual(len(d['activity_data']['prize_list']),4)
        self.assertTrue(d['can_rece'])
        self.assertEqual(d['exchange_item']['attach_count'],1000)

    def test_actual_training_task_claim_and_replay(self):
        self.task(6)
        role=self.b.profile(); c=role['corteges'][0]; c['culture_point']=100
        summon.add_item(role,1001,20); self.b.save(role)
        self.assertEqual(self.call(2)[-1][0],55)
        self.ok(self.req(1081,cortege_id=c['id'],train_type=1,intensive=False))
        self.assertGreater(self.b.profile()['activity']['monday']['task']['finish_time'],0)
        d=self.data(self.call(2)); self.assertEqual(d['add_count'],10)
        before=self.b.profile(); packet=self.packet; replies=self.replies
        self.assertEqual(self.b.respond(packet,self.state),replies)
        self.assertEqual(self.b.profile(),before)
        self.assertEqual(self.call(2)[-1][0],55)

    def test_all_nine_tasks_use_committed_deltas(self):
        for kind in range(1,10):
            with self.subTest(kind=kind):
                self.task(kind); before=self.b.profile(); after=copy.deepcopy(before)
                a=after['activity']; req={};mid=1205
                if kind==1:after['strength']-=1;mid=1026
                if kind==2:after['energy']-=1;mid=1026
                if kind==3:a['duty']={'phase':'fighting'};mid=1026;req={'fight_type':5}
                if kind==4:a['fight_id']=a.get('fight_id',0)+1;mid=1026;req={'fight_type':3}
                if kind==5:a['rape_total_refreshes']=a.get('rape_total_refreshes',0)+1;mid=1029
                if kind==6:after['corteges'][0]['pending_training']={'points':1};mid=1081
                if kind==7:a['visits']={'1':{'claimed':False}};mid=1030;req={'op_type':1}
                if kind==8:a['convert_total']=a.get('convert_total',0)+1;mid=1026;req={'fight_type':10}
                if kind==9:after['journey']['last_fight']={'id':99};mid=1026;req={'fight_type':1}
                untouched=copy.deepcopy(before)
                m.track(untouched,before,mid,req,SUNDAY)
                self.assertEqual(untouched['activity']['monday']['task']['finish_time'],0)
                m.track(after,before,mid,req,SUNDAY)
                self.assertEqual(after['activity']['monday']['task']['finish_time'],SUNDAY)

    def test_consumption_survives_same_request_recovery(self):
        for kind, field, ft, area in [(1,'strength',1,'journey'),(2,'energy',3,'activity')]:
            self.task(kind);before=self.b.profile();after=copy.deepcopy(before)
            after[field]+=10
            m.track(after,before,1026,dict(fight_type=ft),SUNDAY)
            self.assertEqual(after['activity']['monday']['task']['finish_time'],0)
            after[area]['fight_id']=before[area].get('fight_id',0)+1
            m.track(after,before,1026,dict(fight_type=ft),SUNDAY)
            self.assertEqual(after['activity']['monday']['task']['finish_time'],SUNDAY)

    def test_randomize_each_slot_daily_and_freeze_monday(self):
        original=self.data(self.call())['activity_data']['show_list']
        for i in range(1,5):
            d=self.data(self.req(1243,index=i),142)
            self.assertNotEqual(d['attach_data']['attach_data'],original[i]['attach_data'])
            before=self.b.profile()
            self.assertEqual(self.req(1243,index=i)[-1][0],55)
            self.assertEqual(self.b.profile(),before)
        frozen=self.b.profile()['activity']['monday']['goods']
        self.time.return_value=MONDAY
        self.data(self.call())
        self.assertEqual(self.b.profile()['activity']['monday']['goods'],frozen)
        self.assertEqual(self.req(1243,index=1)[-1][0],55)

    def test_next_day_refresh_and_missed_task_pending(self):
        self.time.return_value=SUNDAY-86400
        self.task(1)
        role=self.b.profile();role['activity']['monday']['task']['finish_time']=SUNDAY-86400;self.b.save(role)
        self.data(self.req(1243,index=1),142)
        self.time.return_value=SUNDAY
        self.data(self.req(1243,index=1),142)
        d=self.data(self.call(2))
        self.assertEqual(d['add_count'],10)
        self.assertEqual(d['activity_data']['today_task']['recv_time'],0)

    def test_vip_double_only_monday_and_gift_once(self):
        self.time.return_value=MONDAY
        self.assertEqual(self.data(self.call(2))['add_count'],20)
        self.assertEqual(self.call(2)[-1][0],55)
        # A second isolated account starts with VIP, no pavilion resources.
        role=self.b.profile();role['activity'].pop('monday');role['vip_level']=1
        s=m.state(role,MONDAY,m.load_rules())
        self.assertEqual(m.available(s),40)
        data=m.settle(role,1219,dict(flag=2,level=0,op_type=0),MONDAY)
        self.assertEqual(role['activity']['monday']['jade'],40)
        self.assertTrue(data)

    def test_exchange_all_slots_achievement_and_insufficient(self):
        self.time.return_value=MONDAY
        self.data(self.call(2));role=self.b.profile()
        role['activity']['monday']['jade']=100;self.b.save(role)
        for i in range(1,5):
            self.data(self.call(3,i))
        self.assertEqual(self.b.profile()['activity']['monday']['jade'],0)
        self.assertEqual(self.b.profile()['achievements']['totals']['125'],1)
        before=self.b.profile();self.assertEqual(self.call(3,1)[-1][0],55)
        self.assertEqual(before,self.b.profile())

    def test_expiry_recycles_once_and_persists_restart(self):
        self.time.return_value=MONDAY
        self.data(self.call(2)); before=self.b.profile()
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(before,self.b.profile())
        self.time.return_value=MONDAY+86400
        self.data(self.call());role=self.b.profile()
        mails=[v for k,v in role['welfare']['mails'].items() if k.startswith('monday-recycle-')]
        self.assertEqual(len(mails),1); self.assertEqual(mails[0]['prizes'],[[12,0,20000,1]])
        self.ok(self.req(1103,mail_id=mails[0]['mail_id']))
        before=self.b.profile();self.data(self.call())
        self.assertEqual(before['silver_coin'],self.b.profile()['silver_coin'])
        self.assertEqual(self.b.profile()['activity']['monday']['jade'],0)
        self.time.return_value=MONDAY
        before=self.b.profile();self.assertEqual(self.call(2)[-1][0],55)
        self.assertEqual(before,self.b.profile())

    def test_invalid_and_disabled_rollback(self):
        for kw in [dict(flag=0),dict(flag=4),dict(flag=1,level=1),dict(flag=1,op_type=1)]:
            before=self.b.profile();self.assertEqual(self.call(**kw)[-1][0],55)
            self.assertEqual(before,self.b.profile())
        for index in (0,5,255):self.assertEqual(self.req(1243,index=index)[-1][0],55)
        with patch.object(m,'load_rules',return_value=dict(m.load_rules(),enabled=False)):
            self.assertEqual(self.call()[-1][0],55)
        self.time.return_value=MONDAY;self.data(self.call(2));before=self.b.profile()
        with patch('network_redirect.activity.attributes',side_effect=ValueError('bad encoding')):
            self.assertEqual(self.call(3,1)[-1][0],55)
        self.assertEqual(before,self.b.profile())

    def test_rules_validate_missing_or_bad_rewards(self):
        r=m.load_rules()
        for key,value in [('slots',[]),('daily_jade',0),('recycle_silver',False),('task_rotation',[1]*9)]:
            with tempfile.TemporaryDirectory() as tmp:
                p=Path(tmp)/'rules.json';p.write_text(json.dumps(dict(r,**{key:value})))
                with self.assertRaises(formation.Rejected):m.load_rules(p)
