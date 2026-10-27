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
        if op == 4:
            state = self.sky_state()
            data.setdefault('shop_day', state['shop_day'])
            data.setdefault('shop_revision', state['shop_revision'])
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
        cfg = n.load_rules();cfg['treasure_basis_points']=0;cfg['battle_basis_points']=0
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
        cfg=n.load_rules();cfg['treasure_basis_points']=0;cfg['battle_basis_points']=0;cfg['double_basis_points']=0
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
        s.update(stars=1000,cards={'200':2,'500':2});self.b.save(role)
        self.result(self.call(3,buy_type=1,first_send=True))
        high_cost=s['shop'][5]['cost'];low_cost=s['shop'][0]['cost']
        d=self.result(self.call(4,buy_type=1,index=6,count=1,card_list={200:1}))
        balance=1000-high_cost+200
        self.assertEqual(d['stars'],balance);self.assertEqual(d['return_credits'],0)
        d=self.result(self.call(4,buy_type=1,index=1,count=1,card_list={500:1}))
        self.assertEqual((d['stars'],d['return_credits']),(balance,500-low_cost))
        self.result(self.call(3,buy_type=2,first_send=True))
        self.result(self.call(4,buy_type=2,index=1,count=1))
        self.assertEqual(self.sky_state()['credits'],500-low_cost-20)
        for args in [dict(buy_type=1,index=6,count=2,card_list={}),dict(buy_type=1,index=2,count=1,card_list={500:2}),
                     dict(buy_type=1,index=2,count=1,card_list={999:1}),dict(buy_type=2,index=1,count=0)]:
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
        cfg['treasure_basis_points']=0;cfg['battle_basis_points']=0
        for i in range(6):n.roll(role,s,dict(count=1,index=0),NOW,cfg)
        self.assertEqual((s['free_times'],s['bonus_dice']),(2,2))
        s=n.state(role,NOW+86400,cfg);self.assertEqual(s['free_times'],7)

    def test_ninth_sentinel_batch_uses_portal_and_stays_in_ninth(self):
        role=self.b.profile();cfg=n.load_rules();cfg['treasure_basis_points']=0;cfg['battle_basis_points']=0
        s=n.state(role,NOW,cfg)
        s.update(floor=9,steps=940+99998,cur_point=dict(x=0,y=99998),cur_map=2)
        d=n.roll(role,s,dict(count=10,index=1),NOW,cfg)
        self.assertTrue(d['map_event_list'][0]['is_enter_next'])
        self.assertEqual(s['floor'],9)
        second=d['map_event_list'][1]
        self.assertEqual(second['forward'],n.ROADS[0,second['rand_map']].count('1'))
        self.assertLess(s['cur_point']['y'],99999)

    def test_daily_shop_unique_tiers_saved_selection_and_quota_reset(self):
        self.result(self.call());s=self.sky_state()
        self.assertEqual([x['tier'] for x in s['shop']], ['low']*5+['high'])
        self.assertEqual(len({tuple(x['reward'][:2]) for x in s['shop']}),6)
        role=self.b.profile();role['activity']['nine_sky'].update(stars=10000,credits=100)
        self.b.save(role)
        self.result(self.call(4,buy_type=1,index=1,count=1,card_list={}))
        self.result(self.call(4,buy_type=2,index=1,count=1))
        saved=self.sky_state()
        for _ in range(3):self.result(self.call(3,buy_type=1,first_send=True))
        self.assertEqual(self.sky_state()['shop'],saved['shop'])
        self.assertEqual(self.sky_state()['purchases'],saved['purchases'])
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.sky_state(),saved)
        midnight=(s['shop_day']+1)*86400-8*3600
        with patch('network_redirect.backend.time.time',return_value=midnight):
            d=self.result(self.call(3,buy_type=1,first_send=True))
            self.assertEqual(self.sky_state()['purchases'],{'1':[0]*6,'2':[0]*2})
            self.assertEqual(d['local_snapshot']['shop_day'],s['shop_day']+1)
            self.assertEqual(self.sky_state()['stars'],saved['stars'])
        before=self.b.profile()
        self.assertEqual(self.call(4,buy_type=1,index=1,count=1,card_list={})[0][0],55)
        self.assertEqual(self.b.profile(),before)

    def test_stale_shop_token_rejected_even_after_other_request_refreshes(self):
        self.result(self.call());old=self.sky_state()
        role=self.b.profile();role['activity']['nine_sky']['stars']=10000;self.b.save(role)
        midnight=(old['shop_day']+1)*86400-8*3600
        with patch('network_redirect.backend.time.time',return_value=midnight):
            self.result(self.call())
            before=self.b.profile()
            events=self.call(4,buy_type=1,index=1,count=1,card_list={},shop_day=old['shop_day'])
            self.assertEqual(events[0][0],55);self.assertEqual(self.b.profile(),before)
            events=self.call(4,buy_type=2,index=1,count=1,shop_revision='stale')
            self.assertEqual(events[0][0],55);self.assertEqual(self.b.profile(),before)
            missing=self.req(1309,id=4,data='{buy_type=1,index=1,count=1,card_list={}}')
            self.assertEqual(missing[0][0],55);self.assertEqual(self.b.profile(),before)

    def test_week_exact_boundary_recycles_odd_stars_once_and_claims_mail(self):
        self.result(self.call());role=self.b.profile();s=role['activity']['nine_sky']
        s.update(stars=101,credits=99,cards={'50':2},bonus_dice=3,free_times=4,
                 steps=99,floor=4,battle_seen=[123],battle_count=1,battle_wins=1)
        end=s['end'];self.b.save(role)
        peach=lambda r:sum(i['count'] for i in r['attachments'] if i['attach_type']==5 and i['type_id']==1001)
        previous=peach(role)
        with patch('network_redirect.backend.time.time',return_value=end):
            events=self.call();self.result(events)
            self.assertIn(13,[e for e,_ in events])
            fresh=self.sky_state()
            for k in ('stars','credits','steps'):self.assertEqual(fresh[k],0)
            self.assertEqual(fresh['cards'],{});self.assertEqual(fresh['free_times'],5)
            self.assertNotIn('battle_seen',fresh)
            self.assertTrue(n.status(end)['local_enabled'])
            self.assertIn(9137,n.market_goods(end))
            mails=self.b.profile()['welfare']['mails']
            mail=mails[f'nine-sky-recycle-{s["start"]}']
            self.assertEqual(mail['prizes'],[[5,1001,51,1]])
            self.assertTrue(mail['no_expiry']);self.assertEqual(peach(self.b.profile()),previous)
            self.result(self.call());self.assertEqual(self.b.profile()['welfare']['mails'],mails)
            self.ok(self.req(1103,mail_id=mail['mail_id'],flag=1))
            self.assertEqual(peach(self.b.profile()),previous+51)
            self.req(1103,mail_id=mail['mail_id'],flag=1)
            self.assertEqual(peach(self.b.profile()),previous+51)

    def test_offline_multiple_weeks_and_restart_do_not_duplicate_mail(self):
        self.result(self.call());role=self.b.profile();s=role['activity']['nine_sky']
        s['stars']=100;self.b.save(role);future=s['end']+21*86400
        with patch('network_redirect.backend.time.time',return_value=future):
            self.b.snapshot()
            fresh=self.sky_state()
            self.assertEqual((fresh['stars'],fresh['free_times']),(0,5))
            self.assertEqual(fresh['start'],n.period(future,n.load_rules())[0])
            mails=self.b.profile()['welfare']['mails']
            self.assertEqual(len([k for k in mails if k.startswith('nine-sky-recycle-')]),1)
            self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
            self.result(self.call());self.assertEqual(self.b.profile()['welfare']['mails'],mails)
            with patch('network_redirect.backend.time.time',return_value=future+7*86400):
                self.result(self.call())
                self.assertEqual(self.b.profile()['welfare']['mails'],mails)

    def test_heartbeat_rollover_announces_mail_without_inventory_change(self):
        self.result(self.call());role=self.b.profile();s=role['activity']['nine_sky']
        s['stars']=2;self.b.save(role)
        with patch('network_redirect.backend.time.time',return_value=s['end']):
            replies=self.b.respond(encode(2999,dict(time=0,random_key=0,delay_time=0)),self.state)
        events=[d['id'] for mid,_,d in map(decode,replies) if mid==2998]
        self.assertIn(13,events)
        self.assertEqual(self.sky_state()['stars'],0)
        self.assertEqual(self.sky_state()['last_recycle']['peaches'],1)
        self.assertEqual(self.b.profile()['attachments'],role['attachments'])

    def test_week_mail_and_reset_rollback_together_on_encoding_failure(self):
        self.result(self.call());role=self.b.profile();s=role['activity']['nine_sky']
        s['stars']=200;self.b.save(role)
        with patch('network_redirect.backend.time.time',return_value=s['end']), \
             patch('network_redirect.backend.activity.attributes',side_effect=ValueError('encode failed')):
            self.assertEqual(self.call()[0][0],55)
        self.assertEqual(self.b.profile(),role)
        with patch('network_redirect.backend.time.time',return_value=s['end']):self.result(self.call())
        self.assertEqual(self.sky_state()['last_recycle']['peaches'],100)

    def test_treasure_weight_boundaries_and_shop_candidate_coverage(self):
        cfg=n.load_rules();ticket=0
        for row in cfg['treasure_pool']:
            for pick in (ticket,ticket+row['weight']-1):
                with patch.object(n.secrets,'randbelow',return_value=pick):
                    self.assertEqual(n.treasure(cfg),row['reward'])
            ticket+=row['weight']
        self.assertEqual(ticket,100)
        for choose_last in (False,True):
            with patch.object(n.secrets,'randbelow',side_effect=lambda size:size-1 if choose_last else 0), \
                 patch.object(n.secrets,'choice',side_effect=lambda rows:rows[-1] if choose_last else rows[0]):
                s=n.state(copy.deepcopy(self.b.profile()),NOW,cfg)
            ids=[x['reward'][1] for x in s['shop']]
            self.assertEqual(len(set(ids)),6)
            expected=[x['reward'][1] for x in cfg['star_shop'][:9]][-5:] if choose_last else [x['reward'][1] for x in cfg['star_shop'][:5]]
            self.assertEqual(ids[:5],expected)

    def test_legacy_fixed_shop_migration_keeps_resources_and_used_quotas(self):
        role=self.b.profile();cfg=n.load_rules();s=n.state(role,NOW,cfg)
        s.update(stars=123,credits=456,cards={'50':2},purchases={'1':[2,0,1,3],'2':[4,5]})
        for k in ('shop','shop_day','shop_revision'):s.pop(k)
        with patch.object(n.secrets,'choice',side_effect=lambda rows:rows[0]):
            n.state(role,NOW,cfg)
        self.assertEqual((s['stars'],s['credits'],s['cards']),(123,456,{'50':2}))
        self.assertEqual(s['purchases']['1'][5],1)
        self.assertEqual(s['purchases']['2'],[4,5])
        before=copy.deepcopy(s);n.state(role,NOW,cfg);self.assertEqual(s,before)

    def test_invalid_refresh_config_is_rejected(self):
        cases=[('battle_floor_power',[3000]*9),('recycle_stars_per_peach',3),('battle_basis_points',True),
               ('period_days',8),('timezone_offset_hours',9),('battle_pool',[])]
        for key,value in cases:
            cfg=n.load_rules();cfg[key]=value
            path=Path(self.tmp.name)/'invalid.json';path.write_text(json.dumps(cfg))
            with self.assertRaises(n.f.Rejected):n.load_rules(path)

    def test_ten_real_battles_and_reward_grants_are_atomic_and_replay_safe(self):
        from network_redirect import nine_sky_battle
        self.result(self.call());cfg=n.load_rules()
        cfg.update(battle_basis_points=10000,treasure_basis_points=0)
        before=self.b.profile();old_cards=self.sky_state()['cards'].get('100',0)
        with patch.object(n,'load_rules',return_value=cfg), \
             patch.object(nine_sky_battle,'reward',return_value=[1,-1,1,100]):
            result=self.result(self.call(2,count=10,index=1))
        s=self.sky_state();wins=s['battle_wins']
        self.assertEqual(len(result['local_battles']),10)
        self.assertEqual(len(set(s['battle_seen'])),10)
        self.assertEqual(s['battle_count'],10)
        self.assertEqual(s['cards'].get('100',0)-old_cards,wins)
        self.assertEqual(before['gold_coin']-self.b.profile()['gold_coin'],1000)
        self.assertEqual(result['local_before_snapshot']['steps'],0)
        self.assertEqual(sum(bool(x['won']) for x in result['local_battles'].values()),wins)
        for battle in result['local_battles'].values():
            self.assertEqual(bool(battle['rewards']),battle['won'])
        self.assertLess(max(map(len,self.replies)),32768)
        saved=self.b.profile()
        self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
        self.assertEqual(self.b.profile(),saved)
        with patch.object(n,'load_rules',return_value=cfg), \
             patch.object(nine_sky_battle,'encounter',side_effect=ValueError('battle unavailable')):
            self.assertEqual(self.call(2,count=10,index=1)[0][0],55)
        self.assertEqual(self.b.profile(),saved)

    def test_daily_config_revision_keeps_selection_and_limits(self):
        self.result(self.call());role=self.b.profile();s=role['activity']['nine_sky']
        s['purchases']['1'][0]=1;self.b.save(role)
        cfg=n.load_rules();cfg['revision']='nine-sky-test-price-update'
        for row in cfg['star_shop']:row['cost']+=1
        with patch.object(n,'load_rules',return_value=cfg):
            self.result(self.call(3,buy_type=1,first_send=True))
        updated=self.sky_state()
        self.assertEqual(updated['purchases'],s['purchases'])
        self.assertEqual([x['reward'] for x in updated['shop']],[x['reward'] for x in s['shop']])
        self.assertEqual(updated['shop'][0]['cost'],s['shop'][0]['cost']+1)
        self.assertEqual(updated['shop_revision'],cfg['revision'])
