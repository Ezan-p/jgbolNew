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

    def test_screenshot_catalog_and_all_variants_deliver(self):
        rules = m.load_rules()
        self.assertEqual([r['cost'] for r in rules['slots']], [10, 20, 30, 40])
        self.assertEqual([len(r['pool']) for r in rules['slots']], [7, 6, 4, 4])
        expected = [
            [(1001,20),(1034,5),(1024,1),(1022,2),(1023,1),(1006,1),(1002,1)],
            [(1333,3),(1323,10),(1032,5),(1031,1),(1033,5)],
            [(10001,5),(1249,3),(1343,3)],
            [(6005,5),(6002,5),(6003,5),(1031,5)],
        ]
        for row, items in zip(rules['slots'], expected):
            self.assertEqual([p for p in row['pool'] if isinstance(p,list)],
                             [[5,t,n,1] for t,n in items])
        groups = [p for row in rules['slots'] for p in row['pool'] if isinstance(p,dict)]
        self.assertEqual(groups[0]['choices'], [[5,t,40,1] for t in (1310,1311,1312)])
        self.assertEqual(groups[1]['choices'], [[5,t,3,1] for t in range(1042,1081,2)])
        self.assertEqual(len(groups),2)
        for row in rules['slots']:
            for entry in row['pool']:
                for kind,tid,_,_ in m.candidates(entry):
                    self.assertEqual(kind,5)
                    self.assertNotIn(formation.ITEMS[tid]['main_type'],('1','2'))
        self.time.return_value = MONDAY
        self.data(self.call())
        # Force every configured concrete preview, then buy via the real wire.
        for index, row in enumerate(rules['slots'], 1):
            for entry in row['pool']:
                for spec in m.candidates(entry):
                    with self.subTest(slot=index, spec=spec):
                        role=self.b.profile();s=role['activity']['monday']
                        s['goods'][index-1]=spec;s['jade']=row['cost'];self.b.save(role)
                        kind,tid,count,_=spec
                        def owned(r):
                            return sum((1 if kind==6 else p['count']) for p in r['attachments']
                                       if p['attach_type']==kind and p['type_id']==tid)
                        before=owned(role)
                        d=self.data(self.call(3,index))
                        self.assertEqual(d['attach_data'],dict(object_type=kind,attach_type=tid,attach_count=count,attach_level=1))
                        after=self.b.profile()
                        self.assertEqual(owned(after)-before,count)
                        self.assertEqual(after['activity']['monday']['jade'],0)

    def test_every_closed_weekday_and_exact_midnight_boundaries(self):
        monday_midnight=MONDAY-43200
        tuesday_midnight=monday_midnight-6*86400
        self.time.return_value=tuesday_midnight
        self.data(self.call())
        role=self.b.profile();role['activity']['monday']['jade']=100;self.b.save(role)
        for day in range(6):
            self.time.return_value=tuesday_midnight+day*86400
            self.assertEqual(m.calendar(int(self.time.return_value),m.load_rules())[1],day+2)
            for index in range(1,5):
                before=self.b.profile()
                self.assertEqual(self.call(3,index)[-1][0],55)
                self.assertEqual(self.b.profile(),before)
                self.data(self.req(1243,index=index),142)
                self.assertEqual(self.req(1243,index=index)[-1][0],55)
        self.time.return_value=monday_midnight-1
        self.assertEqual(self.call(3,1)[-1][0],55)
        frozen=self.b.profile()['activity']['monday']['goods']
        self.time.return_value=monday_midnight
        self.data(self.call(3,1))
        self.assertEqual(self.b.profile()['activity']['monday']['goods'],frozen)
        for index in range(1,5):self.assertEqual(self.req(1243,index=index)[-1][0],55)
        self.time.return_value=monday_midnight+86400-1
        self.data(self.call(3,1))
        self.time.return_value=monday_midnight+86400
        self.data(self.call())
        self.assertEqual(self.b.profile()['activity']['monday']['jade'],0)
        self.assertEqual(self.call(3,1)[-1][0],55)
        self.data(self.req(1243,index=1),142)
        mails=[v for k,v in self.b.profile()['welfare']['mails'].items() if k.startswith('monday-recycle-')]
        self.assertEqual(len(mails),1)
        self.assertEqual(mails[0]['prizes'],[[12,0,80000,1]])

    def test_weekly_draw_once_offline_skip_and_unclaimed_expiry(self):
        self.time.return_value=MONDAY
        self.data(self.call(2))
        old=self.b.profile()['activity']['monday']
        tuesday=MONDAY+43200
        self.time.return_value=tuesday
        with patch.object(m,'draw',wraps=m.draw) as draw:
            self.data(self.call())
            self.assertEqual(draw.call_count,4)
            for day in range(7):
                self.time.return_value=tuesday+day*86400
                self.data(self.call())
            self.assertEqual(draw.call_count,4)
            role=self.b.profile();role['activity']['monday']['pending']=10;self.b.save(role)
            self.time.return_value=tuesday+28*86400
            self.data(self.call())
            self.assertEqual(draw.call_count,8)
        s=self.b.profile()['activity']['monday']
        self.assertEqual(s['start']-old['start'],35)
        self.assertEqual((s['jade'],s['pending'],s['random_time']),(0,0,[0]*4))
        mails=[v for k,v in self.b.profile()['welfare']['mails'].items() if k.startswith('monday-recycle-')]
        self.assertEqual(len(mails),1)  # Unclaimed Monday gifts do not become jade.
        before=self.b.profile();self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.data(self.call())
        self.assertEqual(before['activity']['monday'],self.b.profile()['activity']['monday'])

    def test_catalog_migration_preserves_progress_and_valid_goods(self):
        self.data(self.call())
        role=self.b.profile();s=role['activity']['monday'];s.pop('catalog_revision')
        s.update(goods=[[5,1001,10,1],[5,1323,5,1],[5,1032,5,1],[5,6005,5,1]],
                 jade=17,pending=10,random_time=[SUNDAY]*4)
        self.b.save(role);before=copy.deepcopy(s)
        with patch.object(m,'draw',wraps=m.draw) as draw:
            self.data(self.call());self.assertEqual(draw.call_count,3)
            self.data(self.call());self.assertEqual(draw.call_count,3)
        s=self.b.profile()['activity']['monday']
        for key in ('start','jade','pending','random_time','task'):
            self.assertEqual(s[key],before[key])
        self.assertEqual(s['goods'][3],before['goods'][3])
        self.assertEqual(s['catalog_revision'],m.load_rules()['revision'])
        self.assertEqual(self.req(1243,index=1)[-1][0],55)

    def test_group_refresh_excludes_current_category_and_rejects_bad_groups(self):
        row=m.load_rules()['slots'][2];group=row['pool'][2]
        with patch.object(m.secrets,'choice',side_effect=lambda options: options[0]) as choose:
            prize=m.draw(row,group['choices'][0])
            self.assertEqual(prize,row['pool'][0])
            self.assertNotIn(group,choose.call_args_list[0].args[0])
        for bad in ({'choices':[]},{'choices':[[6,999999,1,1]]}, {'choices':[[5,1001,1,1]]}):
            rules=copy.deepcopy(m.load_rules())
            rules['slots'][0]['pool']=[[5,1001,1,1],bad]
            with tempfile.TemporaryDirectory() as tmp:
                path=Path(tmp)/'rules.json';path.write_text(json.dumps(rules))
                with self.assertRaises(formation.Rejected):m.load_rules(path)

    def test_removed_four_star_previews_migrate_out_of_existing_saves(self):
        self.data(self.call())
        for removed in ([5,2010,1,1],[5,3009,1,1],[6,207,1,1]):
            role=self.b.profile();s=role['activity']['monday']
            s['catalog_revision']='2026-10-27.1';s['goods'][2]=removed
            s['jade']=17;s['random_time'][2]=SUNDAY;self.b.save(role)
            self.data(self.call());s=self.b.profile()['activity']['monday']
            self.assertTrue(any(s['goods'][2] in m.candidates(e) for e in m.load_rules()['slots'][2]['pool']))
            self.assertEqual((s['jade'],s['random_time'][2]),(17,SUNDAY))

    def test_login_heartbeat_and_mail_read_recycle_without_opening_shop(self):
        for week,route in enumerate(('login','heartbeat','mail')):
            with self.subTest(route=route):
                self.time.return_value=MONDAY+week*7*86400
                self.data(self.call(2))
                role=self.b.profile();start=role['activity']['monday']['start']
                from network_redirect import system_mail, welfare
                system_mail.deliver(role,key='read-test-'+route,title='测试',body='测试',
                                    prizes=[[12,0,1,1]],now=int(self.time.return_value),rules=welfare.load_rules())
                mail_id=role['welfare']['mails']['read-test-'+route]['mail_id'];self.b.save(role)
                self.time.return_value+=43200
                if route=='login':
                    self.b.bootstrap(reconnect=True)
                elif route=='heartbeat':
                    replies=self.b.respond(encode(2999,{}),self.state)
                    self.assertEqual(decode(replies[0])[0],2999)
                else:
                    self.ok(self.req(1102,mail_id=mail_id,flag=0))
                role=self.b.profile()
                self.assertEqual(role['activity']['monday']['jade'],0)
                mails=[v for k,v in role['welfare']['mails'].items() if k=='monday-recycle-'+str(start)]
                self.assertEqual(len(mails),1)
                self.assertEqual(mails[0]['prizes'],[[12,0,20000,1]])
                before=role['silver_coin']
                self.ok(self.req(1103,mail_id=mails[0]['mail_id']))
                self.assertEqual(self.b.profile()['silver_coin']-before,20000)
                self.assertEqual(self.req(1103,mail_id=mails[0]['mail_id'])[-1][0],55)

    def test_recycle_mail_failure_preserves_old_balance_for_retry(self):
        self.time.return_value=MONDAY;self.data(self.call(2))
        self.time.return_value=MONDAY+43200
        before=self.b.profile()
        with patch('network_redirect.system_mail.deliver',side_effect=formation.Rejected('mail failed')):
            self.assertEqual(self.call()[-1][0],55)
        self.assertEqual(before,self.b.profile())
        self.data(self.call())
        mails=[v for k,v in self.b.profile()['welfare']['mails'].items() if k.startswith('monday-recycle-')]
        self.assertEqual(len(mails),1)
        self.assertEqual(mails[0]['prizes'],[[12,0,20000,1]])
