"""Real-wire tests against detached SQLite saves; never use a live account."""
import copy
from pathlib import Path
from unittest.mock import patch
from test_activity import ActivityCase, NOW
from network_redirect import activity_save_monkey as m, activity, summon, daily, welfare, recharge
from network_redirect.backend import Backend


class SaveMonkeyTests(ActivityCase):
    def saved(self): return self.b.profile()['activity']['save_monkey']

    def call(self,op=1,**data):
        if op not in (1,4,6): data.setdefault('local_token',self.saved()['token'])
        events=self.req(1346,id=op,data=summon.lua(data));self.ok(events)
        return next(v for e,v in events if e==197)

    def reject(self,op,data):
        before=self.b.profile();out=self.req(1346,id=op,data=summon.lua(data))
        self.assertEqual(out[0][0],55,out);self.assertEqual(self.b.profile(),before)

    def grid(self, entries=()):
        role=self.b.profile();s=role['activity']['save_monkey']
        s['grid']=[[dict(strength=1,stone_type=1,content=0) for _ in range(6)] for _ in range(8)]
        for col in s['grid']: col[0]['strength']=0
        for x,y,content,stone,hp in entries:
            s['grid'][x][y]=dict(strength=hp,stone_type=stone,content=content)
        self.b.save(role)

    def use(self,tid=1350,x=2,y=1): return self.call(2,item_type=tid,pos_info=dict(x=x,y=y))

    def count(self,tid): return recharge.count(self.b.profile(),tid)

    def test_entry_starter_daily_supply_wire_status_and_restart(self):
        before=self.count(1350);out=self.call();self.assertEqual(self.count(1350)-before,17)
        self.assertEqual((len(out['grid_conf']),len(out['grid_conf'][1])),(8,6))
        self.assertEqual(len(out['point_data']),11)
        self.assertEqual(len(out['local_assist']),4)
        saved=self.saved();self.call();self.assertEqual(saved,self.saved())
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.call();self.assertEqual(saved,self.saved());self.assertEqual(self.count(1350)-before,17)
        self.assertTrue(next(v for e,v in self.req(1205,flag=0) if e==47)['local_save_monkey']['local_enabled'])
        with patch('network_redirect.game_clock.now',return_value=NOW+86400):
            self.call();self.assertEqual(self.count(1350)-before,22)
            self.assertEqual(self.saved()['grid'],saved['grid'])

    def test_original_monkey_prizes_and_coordinate_transposition(self):
        self.call();self.grid([(0,1,1355,1,1),(1,1,1356,1,1)])
        gold=self.b.profile()['gold_coin'];stone=self.count(10000)
        self.use();self.use(x=2,y=2)
        self.assertEqual(self.saved()['score'],3);self.assertEqual(self.saved()['piece'],2)
        self.assertEqual(self.b.profile()['gold_coin']-gold,8);self.assertEqual(self.count(10000)-stone,10)
        self.assertEqual(self.count(1355),0);self.assertEqual(self.count(1356),0)

    def test_fire_empty_center_and_thunder_two_by_two_clipped(self):
        self.call();self.grid();self.use(1351,x=1,y=4)
        self.assertEqual(self.saved()['piece'],3)
        self.grid();self.use(1352,x=3,y=4)
        self.assertEqual(self.saved()['piece'],7)
        for x,y in ((3,2),(4,2),(3,3),(4,3)):
            self.assertEqual(self.saved()['grid'][x][y]['strength'],0)
        self.use(1352,x=6,y=8);self.assertEqual(self.saved()['piece'],8)

    def test_granite_hard_stone_and_chain_bombs_once(self):
        self.call();self.grid([(0,1,1355,3,1),(1,1,1356,2,2)])
        self.reject(2,dict(item_type=1350,pos_info=dict(x=2,y=1),local_token=self.saved()['token']))
        self.use(x=2,y=2);self.assertEqual(self.saved()['grid'][1][1]['strength'],1)
        self.assertEqual(self.saved()['piece'],0);self.use(x=2,y=2);self.assertEqual(self.saved()['score'],1)
        self.grid([(2,2,1353,1,1),(3,2,1353,1,1),(4,2,1355,1,1),(0,1,0,3,1)])
        out=self.use(1352,x=3,y=3)
        self.assertEqual(len(out['qibaofu_list']),2);self.assertEqual(self.saved()['score'],3)
        self.assertEqual(self.saved()['grid'][0][1]['strength'],1)
        self.assertEqual(self.count(1353),0)

    def test_invalid_stale_forged_and_locked_requests_atomic(self):
        self.call();self.grid();token=self.saved()['token']
        for data in ({'item_type':1353},{'item_type':True},{'item_type':1350,'pos_info':{'x':0,'y':1}},
                     {'item_type':1350,'pos_info':{'x':True,'y':1}},
                     {'item_type':1350,'pos_info':{'x':2,'y':9}},
                     {'item_type':1350,'pos_info':{'x':5,'y':5}},
                     {'item_type':1351,'pos_info':{'x':2,'y':1}},
                     {'item_type':1350,'pos_info':{'x':2,'y':1},'score':1000}):
            self.reject(2,dict(data,local_token=token))
        self.reject(8,{})
        self.use();before=self.b.profile();self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
        self.assertEqual(self.b.profile(),before)
        self.reject(2,dict(item_type=1352,pos_info=dict(x=3,y=4),local_token=token))
        role=self.b.profile()
        for i in role['attachments']:
            if i['type_id']==1350:i['is_lock']=True
        self.b.save(role)
        self.reject(2,dict(item_type=1350,pos_info=dict(x=2,y=2),local_token=self.saved()['token']))

    def test_eye_visibility_expiry_and_scroll(self):
        self.call();self.grid([(3,4,1355,1,1)])
        self.assertNotIn('item',self.call()['grid_conf'][4][5])
        out=self.call(2,item_type=1354);self.assertEqual(out['show_deep'],29)
        self.assertEqual(out['grid_conf'][4][5]['item']['attach_type'],1355)
        self.reject(2,dict(item_type=1354,local_token=self.saved()['token']))
        role=self.b.profile();s=role['activity']['save_monkey']
        for col in s['grid']:col[1]['strength']=0
        s['grid'][0][1]=dict(strength=1,stone_type=1,content=0);self.b.save(role)
        self.use();self.assertEqual(self.saved()['deep'],1)
        self.assertEqual(self.saved()['grid'][3][3]['content'],1355)
        role=self.b.profile();role['activity']['save_monkey']['deep']=30;self.b.save(role)
        self.assertNotIn('item',self.call()['grid_conf'][4][4])

    def test_score_and_daily_claim_shop_and_period_isolation(self):
        self.call();self.reject(3,dict(prize_id=1,local_token=self.saved()['token']))
        role=self.b.profile();s=role['activity']['save_monkey'];s.update(score=10,piece=30)
        daily.record(role,1,1,NOW,daily.load_rules());self.b.save(role)
        self.assertEqual(self.call(3,prize_id=1)['status'],3)
        self.assertEqual(self.call(7,prize_id=1)['status'],3)
        self.reject(7,dict(prize_id=1,local_token=self.saved()['token']))
        n=self.count(1350);self.call(5,index=1,count=2);self.assertEqual(self.count(1350)-n,6)
        self.assertEqual(self.saved()['piece'],10)
        self.reject(5,dict(index=1,count=2,local_token=self.saved()['token']))
        end=self.saved()['end'];token=self.saved()['token'];inventory=self.b.profile()['attachments']
        with patch('network_redirect.game_clock.now',return_value=end):
            self.reject(5,dict(index=1,count=1,local_token=token))
            self.call(4);self.assertEqual(self.saved()['piece'],0);self.assertEqual(self.saved()['score'],0)
            self.assertEqual(self.b.profile()['attachments'],inventory)
        self.reject(1,{})

    def test_assist_original_all_four_rows_and_insufficient_atomic(self):
        self.call();role=self.b.profile()
        activity.prizes(role,[[5,t,1000,1] for t in (1350,1351,1352)]);self.b.save(role)
        expected=[(300,20,30),(100,0,0),(0,10,0),(0,0,15)]
        for i,row in m.ASSIST.items():
            self.assertEqual(tuple(row['consume']),expected[i-1]);gold=self.b.profile()['gold_coin']
            counts=[self.count(t) for t in (1350,1351,1352)]
            self.call(9,index=i,count=2)
            self.assertEqual([counts[j]-self.count(t) for j,t in enumerate((1350,1351,1352))],[2*n for n in expected[i-1]])
            self.assertEqual(self.b.profile()['gold_coin']-gold,2*row['prizes'][0][2])
        self.reject(9,dict(index=1,count=15,local_token=self.saved()['token']))

    def test_recharge_before_unlock_mail_once_and_card_exclusion(self):
        role=self.b.profile();m.record_charge(role,500,NOW);self.b.save(role)
        self.call();self.assertEqual(self.saved()['charge_gold'],500)
        self.assertEqual(self.saved()['charge_claimed'],[])
        role=self.b.profile();role['activity']['save_monkey']['score']=10;self.b.save(role)
        self.call();role=self.b.profile();mails=[v for k,v in role['welfare']['mails'].items() if k.startswith('save-monkey:')]
        self.assertEqual(len(mails),1);self.assertEqual(mails[0]['prizes'],[[5,1151,1,1]])
        before=copy.deepcopy(role);m.record_charge(role,500,NOW,source_item=1151);self.assertEqual(role,before)
        self.call();self.assertEqual(self.saved()['charge_claimed'],[1])
        self.assertEqual(self.count(1151),0)
        self.ok(self.req(1103,mail_id=mails[0]['mail_id']))
        self.assertEqual(self.count(1151),1)
        role=self.b.profile();card=next(i for i in role['attachments'] if i['type_id']==1151)
        gold=role['gold_coin'];charge=role['charge_gold'];monkey=copy.deepcopy(self.saved())
        self.ok(self.req(1051,item_id=card['id'],item_type=1151,item_count=1,des_type=1,des_id=0))
        self.assertEqual(self.count(1151),0)
        self.assertGreaterEqual(self.b.profile()['gold_coin']-gold,50)
        self.assertEqual(self.b.profile()['charge_gold']-charge,50)
        self.assertEqual(self.saved(),monkey)

    def test_recharge_actual_redemption_fanout(self):
        role=self.b.profile();activity.prizes(role,[[5,1152,1,1]]);self.b.save(role)
        card=next(i for i in role['attachments'] if i['type_id']==1152)
        self.ok(self.req(1051,item_id=card['id'],item_type=1152,item_count=1,des_type=1,des_id=0))
        self.assertEqual(self.saved()['charge_gold'],500)
        self.assertEqual(self.saved()['charge_tool_batches'],1)
        self.assertEqual(self.count(1350),5)

    def test_disabled(self):
        self.call()
        with patch.object(m,'load_rules',return_value=dict(m.load_rules(),enabled=False)):
            self.reject(1,{})
            role=self.b.profile();before=copy.deepcopy(role);m.record_charge(role,100,NOW)
            self.assertEqual(role,before)

    def test_daozun_order_replay_restart_and_invalid_inventory(self):
        role=self.b.profile();activity.prizes(role,[[5,1151,2,1]])
        m.record_charge(role,500,NOW);self.b.save(role)
        card=next(i for i in role['attachments'] if i['type_id']==1151)
        data=dict(order_id='monkey-card-order-1',item_id=card['id'],item_type=1151,item_count=1,des_type=1,des_id=0)
        out=self.req(1111,event_id=253,data=summon.lua(data));self.ok(out)
        charge=self.b.profile()['charge_gold'];gold=self.b.profile()['gold_coin'];monkey=self.saved()
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.req(1111,event_id=253,data=summon.lua(data))
        self.assertEqual(self.count(1151),1);self.assertEqual(self.b.profile()['charge_gold'],charge)
        self.assertEqual(self.b.profile()['gold_coin'],gold);self.assertEqual(self.saved(),monkey)
        role=self.b.profile()
        for item in role['attachments']:
            if item['type_id']==1151:item['is_lock']=True
        self.b.save(role);before=self.b.profile()
        data['order_id']='monkey-card-order-2'
        out=self.req(1111,event_id=253,data=summon.lua(data))
        self.assertIn(55,[e for e,v in out]);self.assertEqual(self.b.profile(),before)
