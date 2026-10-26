"""Native protocol, complete nine-floor travel, economy and persistence."""
import copy
import json
from pathlib import Path
from unittest.mock import patch

from test_activity import ActivityCase, NOW
from network_redirect import activity_nine_sky as n, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode, encode


class NineSkyTests(ActivityCase):
    def call(self, op=1, **data):
        return self.req(1309, id=op, data=summon.lua(data))

    def result(self, events):
        self.ok(events)
        return next(d for e, d in events if e == 164)

    def test_entry_status_and_original_constants(self):
        d = self.result(self.call())
        self.assertEqual(d['role_sky_data']['steps'], 0)
        self.assertEqual(d['const_data']['one_rock_money'], 100)
        status = next(d for e,d in self.req(1205,flag=0) if e==47)['nine_sky_data']
        self.assertLess(status['begin_time'], NOW)
        self.assertGreater(status['end_time'], NOW)
        self.assertEqual(n.LEVELS, [10,20,40,70,100,160,220,320,99999])
        self.assertEqual(len(n.ROADS), 42)

    def test_free_paid_ten_rolls_original_cost_and_replay(self):
        self.result(self.call())
        cfg = n.load_rules();cfg['treasure_basis_points']=0
        with patch.object(n,'load_rules',return_value=cfg):
            for i in range(5):
                d=self.result(self.call(2,count=1,index=0))
                self.assertEqual(d['free_times'],4-i)
            before=self.b.profile();self.assertEqual(self.call(2,count=1,index=0)[0][0],55)
            self.assertEqual(before,self.b.profile())
            d=self.result(self.call(2,count=10,index=1))
            self.assertEqual(len(d['map_event_list']),10)
            self.assertEqual(before['gold_coin']-self.b.profile()['gold_coin'],1000)
            self.assertEqual(self.sky_state()['rolls'],15)
            after=self.b.profile()
            self.assertEqual(self.b.respond(self.packet,self.__dict__['state']),self.replies)
            self.assertEqual(after,self.b.profile())

    def test_all_nine_floors_and_42_routes_match_client(self):
        # Use a disposable role; no mock victory or state increments.
        role=self.b.profile();role['gold_coin']=1000000
        cfg=n.load_rules();cfg['treasure_basis_points']=0;cfg['double_basis_points']=0
        s=n.state(role,NOW,cfg);seen={1};cross=[]
        for i in range(120):
            before=copy.deepcopy(s)
            d=n.roll(role,s,dict(count=10,index=1),NOW+i,cfg)
            for ev in d['map_event_list']:
                road=n.ROADS[before['cur_map'],ev['rand_map']]
                self.assertEqual(ev['forward'],road.count('1'))
                before['steps']+=ev['forward']
                before['stars']+=ev['forward']*5
                for direction in road:
                    dx,dy=n.DIRECTIONS[direction]
                    before['cur_point']['x']+=dx;before['cur_point']['y']+=dy
                if ev['is_enter_next']:
                    self.assertEqual(before['cur_point']['y'],n.LEVELS[before['floor']-1])
                    cross.append(before['steps']);before['floor']+=1;seen.add(before['floor'])
                    before['cur_map']=0;before['cur_point']=dict(x=0,y=0)
                else:before['cur_map']=ev['rand_map']
            for key in ('steps','stars','floor','cur_point','cur_map'):
                self.assertEqual(s[key],before[key],key)
            if s['floor']==9:break
        self.assertEqual(seen,set(range(1,10)))
        self.assertEqual(cross,[10,30,70,140,240,400,620,940])
        self.assertGreaterEqual(s['steps'],940)

    def test_double_adds_only_five_and_all_treasure_kinds(self):
        role=self.b.profile();cfg=n.load_rules();cfg['double_basis_points']=10000;cfg['treasure_basis_points']=10000
        s=n.state(role,NOW,cfg)
        for reward in [row['reward'] for row in cfg['treasure_pool']]:
            stars=s['stars'];dice=s['free_times'];gold=role['gold_coin']
            with patch.object(n,'treasure',return_value=reward):
                d=n.roll(role,s,dict(count=1,index=1),NOW,cfg)
            ev=d['map_event_list'][0]
            self.assertEqual(s['stars']-stars,5*ev['forward']+5)
            self.assertEqual(gold-role['gold_coin'],100)
            self.assertEqual(ev['meet_rand_list'][0],n.a.prize_spec(reward))
            if reward[0:2]==[1,-1]:self.assertEqual(s['cards']['50'],1)
            if reward[0:2]==[1,-2]:self.assertEqual(s['free_times'],dice+1)

    def test_cards_mixed_payment_overflow_credit_and_limits(self):
        self.result(self.call());role=self.b.profile();s=role['activity']['nine_sky']
        s.update(stars=400,cards={'200':2,'500':2});self.b.save(role)
        self.result(self.call(3,buy_type=1,first_send=True))
        d=self.result(self.call(4,buy_type=1,index=1,count=1,card_list={200:1}))
        self.assertEqual(d['stars'],100);self.assertEqual(d['return_credits'],0)
        d=self.result(self.call(4,buy_type=1,index=2,count=1,card_list={500:1}))
        self.assertEqual((d['stars'],d['return_credits']),(100,350))
        self.result(self.call(3,buy_type=2,first_send=True))
        self.result(self.call(4,buy_type=2,index=1,count=1))
        self.assertEqual(self.sky_state()['credits'],330)
        for args in [dict(buy_type=1,index=1,count=9,card_list={}),dict(buy_type=1,index=1,count=1,card_list={500:2}),
                     dict(buy_type=1,index=1,count=1,card_list={999:1}),dict(buy_type=2,index=1,count=0)]:
            before=self.b.profile();self.assertEqual(self.call(4,**args)[0][0],55);self.assertEqual(before,self.b.profile())

    def test_palace_resume_purchase_and_stale_encounter(self):
        d=self.result(self.call(2,count=10,index=1))
        p=d['map_event_list'][10]['tina_shop'];idx=p['shop_index']
        self.assertEqual(len(p['right_shop']),2);self.assertEqual(len(p['predit_shop']),2)
        self.assertEqual(self.result(self.call())['tina_shop']['shop_index'],idx)
        gold=self.b.profile()['gold_coin']
        self.result(self.call(5,buy_type=1,index=1,count=1,shop_index=idx))
        self.assertEqual(gold-self.b.profile()['gold_coin'],300)
        self.result(self.call(5,buy_type=2,index=1,count=1,shop_index=idx))
        self.assertGreater(self.sky_state()['cards']['50'],0)
        before=self.b.profile();self.assertEqual(self.call(5,buy_type=1,index=1,count=1,shop_index=idx)[0][0],55)
        self.assertEqual(before,self.b.profile())
        self.result(self.call(2,count=1,index=1))
        self.assertEqual(self.call(5,buy_type=2,index=1,count=1,shop_index=idx)[0][0],55)

    def test_day_season_restart_clock_and_disabled(self):
        self.result(self.call(2,count=1,index=0));before=self.b.profile()
        with patch('network_redirect.backend.time.time',return_value=NOW-1):
            self.assertEqual(self.call(2,count=1,index=0)[0][0],55)
        self.assertEqual(before,self.b.profile())
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(before,self.b.profile())
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            d=self.result(self.call())['role_sky_data'];self.assertEqual(d['free_times'],5+before['activity']['nine_sky'].get('bonus_dice',0))
            self.assertEqual(d['steps'],before['activity']['nine_sky']['steps'])
        end=self.sky_state()['end']
        with patch('network_redirect.backend.time.time',return_value=end+1):
            d=self.result(self.call())['role_sky_data'];self.assertEqual(d['steps'],0)
        cfg=n.load_rules();cfg['enabled']=False
        with patch.object(n,'load_rules',return_value=cfg):self.assertEqual(self.call()[0][0],55)

    def test_bad_requests_atomicity_and_account_isolation(self):
        for op,text in [(0,'{}'),(1,'{bad}'),(2,'{count=10,index=0}'),(2,'{count=-1,index=1}'),
                        (2,'{count=1,index=1,stars=999}'),(4,'{buy_type=1,index=1,count=-1}'),(3,'{buy_type=true}')]:
            before=self.b.profile();self.assertEqual(self.req(1309,id=op,data=text)[0][0],55);self.assertEqual(before,self.b.profile())
        self.result(self.call());before=self.b.profile()
        with patch('network_redirect.backend.activity.attributes',side_effect=ValueError('encode failed')):
            self.assertEqual(self.call(2,count=10,index=1)[0][0],55)
        self.assertEqual(before,self.b.profile())
        other=Backend(Path(self.tmp.name),18770,lambda *a,**k:None,account='other');self.addCleanup(other.close)
        self.assertNotIn('nine_sky',other.profile().get('activity',{}))

    def test_bad_config(self):
        for key,value in [('mode','official'),('daily_free',True),('one_rock_money',50),('card_values',[0]),('palace_cards',[])]:
            cfg=n.load_rules();cfg[key]=value
            path=Path(self.tmp.name)/'invalid.json';path.write_text(json.dumps(cfg))
            with self.assertRaises(n.f.Rejected):n.load_rules(path)

    def sky_state(self):
        return self.b.profile()['activity']['nine_sky']

    def test_market_bag_original_souls_and_selected_stack(self):
        from network_redirect import market
        role=self.b.profile();cfg=n.load_rules()
        goods=market.catalog(role,NOW,self.b.market_rules)['rich_item_list'][9137]
        self.assertEqual((goods['type_id'],goods['buy_price']),(1243,300))
        market.buy(role,dict(page_id=2,index=9137,type_id=1243,count=2),NOW,self.b.market_rules)
        self.b.save(role)
        item=next(i for i in role['attachments'] if i['type_id']==1243)
        before=role.get('souls',{}).get('5027',0)
        req=dict(item_type=1243,item_id=item['id'],item_count=2,des_type=1,des_id=role['role_id'])
        self.ok(self.req(1051,**req))
        self.assertEqual(self.b.profile()['souls']['5027']-before,10)
        before=self.b.profile();self.assertEqual(self.req(1051,**req)[0][0],55)
        self.assertEqual(before,self.b.profile())
        cfg['enabled']=False
        with patch.object(n,'load_rules',return_value=cfg):
            self.assertEqual(n.market_goods(NOW),{})

    def test_real_local_leader_and_stale_week_exclusion(self):
        role=self.b.profile();cfg=n.load_rules();s=n.state(role,NOW,cfg)
        peer=copy.deepcopy(role);peer.update(role_id=777,role_name='本地同行')
        ps=peer['activity']['nine_sky'];ps['steps']=100
        self.assertEqual(n.top(role,s,[peer])['name'],'本地同行')
        ps['start']-=7*86400
        self.assertEqual(n.top(role,s,[peer])['name'],'')

    def test_daily_allowance_expires_but_earned_dice_survive(self):
        role=self.b.profile();cfg=n.load_rules();s=n.state(role,NOW,cfg)
        n.grant(role,s,[1,-2,3,1]);self.assertEqual(s['free_times'],8)
        cfg['treasure_basis_points']=0
        for i in range(6):n.roll(role,s,dict(count=1,index=0),NOW,cfg)
        self.assertEqual((s['free_times'],s['bonus_dice']),(2,2))
        s=n.state(role,NOW+86400,cfg);self.assertEqual(s['free_times'],7)

    def test_ninth_sentinel_batch_uses_portal_and_stays_in_ninth(self):
        role=self.b.profile();cfg=n.load_rules();cfg['treasure_basis_points']=0
        s=n.state(role,NOW,cfg)
        s.update(floor=9,steps=940+99998,cur_point=dict(x=0,y=99998),cur_map=2)
        d=n.roll(role,s,dict(count=10,index=1),NOW,cfg)
        self.assertTrue(d['map_event_list'][0]['is_enter_next'])
        self.assertEqual(s['floor'],9)
        second=d['map_event_list'][1]
        self.assertEqual(second['forward'],n.ROADS[0,second['rand_map']].count('1'))
        self.assertLess(s['cur_point']['y'],99999)
