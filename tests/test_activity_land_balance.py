"""Weekly progression and tiered hunting economy through real backend requests."""
import copy
from unittest.mock import patch

from tests.test_activity import ActivityCase, NOW
from network_redirect import activity, activity_land as land, activity_land_npc as npc
from network_redirect import activity_land_rewards as rewards, summon, journey
from network_redirect.formation import Rejected


def strong_party(case):
    """A real endgame loadout for capture flow tests, without faking victory."""
    role=case.b.profile();ident=role['role_id']
    model=next(n for n in npc.catalog().values() if n['role']['level']==99 and n['tier']=='T1')
    role.update(copy.deepcopy(model['role']));role['role_id']=ident
    role['activity']['land']['grid_count']=8
    case.b.save(role)


class LandBalanceTests(ActivityCase):
    def land(self,op,**data):return self.req(1302,id=op,data=summon.lua(data))

    def test_balance_configuration_rejects_missing_or_unordered_tiers(self):
        for key,value in (('land_travel_soul_by_map',[100,200,350]),
                          ('land_travel_soul_by_map',[True,200,350,500]),
                          ('land_travel_soul_by_map',[100,100,100,100]),
                          ('land_tower_soul_by_type',[10,20,40,80]),
                          ('land_guard_tier_by_type',['T4','T3','T2','T1'])):
            rules=dict(self.b.activity_rules);rules[key]=value
            with self.assertRaises(Rejected):land.validate_balance(rules)

    def test_week_reset_closes_old_income_and_keeps_growth_and_mail_once(self):
        self.ok(self.land(1));role=self.b.profile();s=role['activity']['land'];r=self.b.activity_rules
        monday=((s['week']+1)*7+4)*86400-r['timezone_offset_hours']*3600
        with patch('network_redirect.game_clock.now',return_value=monday-600):
            self.ok(self.land(1));role=self.b.profile();s=role['activity']['land']
            s.update(boss_layer=64,inv_boss_layer=64,map_level=4,grid_count=8,soul_count=77,
                     week_soul=0,history={'64':dict(score=3000,cur_num=1)},
                     inv_history={'64':dict(score=3000,cur_num=1)},total_score=6000,
                     boss=dict(layer=64,cards=[],rewards=[[5,10000,20,1]]*5),
                     hell=dict(layer=64,cards=[],rewards=[[5,10000,10,1]]*3),
                     unlocked=list(range(1,65)),bag={'1':{'5':2}},
                     charms={'1':dict(key=1,value=30,unlock=True,is_open=True)},
                     towers={},auto_tower=0,travel=[dict(id=942001)],swept=True)
            land.towers(s,monday-600,r);s['tower_id']=41
            s['towers']['41'].update(owner_type=1,last_tick=monday-600,expire=monday+3000)
            self.b.save(role);old_week=s['week'];growth=copy.deepcopy(s['charms'])
        with patch('network_redirect.game_clock.now',return_value=monday+600):
            self.b.bootstrap();s=self.b.profile()['activity']['land']
            self.assertEqual(s['last_week_result']['soul'],800)
            self.assertEqual((s['soul_count'],s['week_soul']),(877,0))
            self.assertEqual((s['map_level'],s['boss_layer'],s['inv_boss_layer'],s['total_score']),(1,0,0,0))
            self.assertEqual(s['grid_count'],8);self.assertEqual(s['charms']['1'],growth['1'])
            self.assertEqual(s['bag'],{'1':{'5':2}})
            for key in ('history','inv_history','hell_counts','towers'):self.assertEqual(s[key],{})
            for key in ('boss','hell','travel'):self.assertIsNone(s[key])
            self.assertEqual(s['unlocked'],[]);self.assertEqual(s['tower_id'],0)
            self.assertEqual(s['travel_count'],0);self.assertEqual(s['attack_count'],0)
            self.assertEqual(s['title_layers'],list(range(120,125)))
            mails={k:v for k,v in self.b.profile()['welfare']['mails'].items() if k.startswith('land-week-')}
            self.assertEqual(list(mails),[f'land-week-{old_week}'])
            self.b.bootstrap();self.assertEqual(self.b.profile()['activity']['land'],s)
            self.assertEqual(self.land(14,index=1)[0][0],55)
            self.assertEqual(self.land(25)[0][0],55)
            self.assertEqual(self.land(2,des_level=4)[0][0],55)
            # New week gets a fresh first-win reward and map gate after reset.
            self.ok(self.land(4,flag=1,des_type=3,des_id=1,cur_num=1))
            self.assertIsNotNone(self.b.profile()['activity']['land']['boss'])
            self.ok(self.land(15));self.assertEqual(self.b.profile()['activity']['land']['boss_layer'],1)

    def test_no_income_week_still_resets_progress_and_failed_encoding_rolls_back(self):
        self.ok(self.land(1));role=self.b.profile();s=role['activity']['land']
        s.update(boss_layer=48,inv_boss_layer=20,map_level=4,week_soul=0)
        self.b.save(role);monday=((s['week']+1)*7+4)*86400-self.b.activity_rules['timezone_offset_hours']*3600
        with patch('network_redirect.game_clock.now',return_value=monday):
            with patch.object(land,'response',side_effect=ValueError('encoding failed')):
                self.assertEqual(self.land(1)[0][0],55)
            self.assertEqual(self.b.profile()['activity']['land'],s)
            self.ok(self.land(1));current=self.b.profile()
            self.assertEqual(current['activity']['land']['boss_layer'],0)
            self.assertFalse(any(k.startswith('land-week-') for k in current['welfare'].get('mails',{})))

    def test_travel_display_single_batch_and_loss_share_map_tiers(self):
        self.ok(self.land(1))
        # Isolate reward accounting; existing playthrough tests use real battles.
        for level,amount in enumerate((100,200,350,500),1):
            role=self.b.profile();s=role['activity']['land'];s.update(map_level=level,travel_count=0,travel=None)
            self.b.save(role);out=self.land(3);self.ok(out)
            self.assertTrue(all(x['expect_soul']==amount for x in out[-1][1]['enemy_list'].values()))
            before=self.b.profile()['activity']['land']['week_soul']
            with patch.object(land,'simulate',return_value=(1,{})),patch.object(land,'replay_response',side_effect=lambda op,s,r,replay,**kw:[land.response(op,s,r,**kw)]):
                out=self.land(4,flag=1,des_type=1,des_id=1);self.ok(out)
                self.assertEqual(out[-1][1]['soul_count'],amount)
                out=self.land(22);self.ok(out);self.assertEqual(out[-1][1]['reward_soul'],5*amount)
            self.assertEqual(self.b.profile()['activity']['land']['week_soul']-before,6*amount)
            with patch.object(land,'simulate',return_value=(4,{})):
                out=self.land(22);self.ok(out);self.assertEqual(out[-1][1]['reward_soul'],0)
            self.assertEqual(self.b.profile()['activity']['land']['week_soul']-before,6*amount)

    def test_all_tower_tiers_display_and_credit_the_same_rate_with_caps(self):
        when=NOW+8*3600
        with patch('network_redirect.game_clock.now',return_value=when):
            self.ok(self.land(1));original=self.b.profile()
        for typ,rate in enumerate((80,40,20,10),1):
            role=copy.deepcopy(original);s=role['activity']['land'];tid=10+typ;t=s['towers'][str(tid)]
            view=land.tower_view(role,s,t,when,self.b.activity_rules)
            self.assertEqual((view['soul_speed'],view['fps_count'],view['all_soul']),(rate,rate,rate*60))
            s['tower_id']=tid;t.update(owner_type=1,last_tick=when,expire=when+3600)
            self.b.save(role)
            with patch('network_redirect.game_clock.now',return_value=when+600):
                self.ok(self.land(1));self.assertEqual(self.b.profile()['activity']['land']['soul_count'],rate*10)
                self.ok(self.land(1));self.assertEqual(self.b.profile()['activity']['land']['soul_count'],rate*10)
            with patch('network_redirect.game_clock.now',return_value=when+7200):
                self.ok(self.land(1));s=self.b.profile()['activity']['land']
                self.assertEqual(s['soul_count'],rate*60);self.assertEqual(s['week_soul'],rate*60)
                self.assertEqual(s['tower_id'],0);self.assertEqual(s['towers'][str(tid)]['left_soul'],0)

    def test_guard_tiers_are_strictly_ordered_and_inspection_matches_actual_battle(self):
        self.ok(self.land(1));role=self.b.profile();s=role['activity']['land'];rules=self.b.activity_rules
        for map_level in range(1,5):
            for day in range(12):
                s.update(map_level=map_level,day=day,towers={})
                rows=land.towers(s,NOW,rules)
                powers=[npc.power(npc.catalog()[t['npc_id']],t['defender_count']) for t in rows]
                self.assertTrue(all(x>y for x,y in zip(powers,powers[1:])),(map_level,day,powers))
                self.assertTrue(all(npc.catalog()[t['npc_id']]['role']['level']==(50,70,90,99)[map_level-1] for t in rows))
        when=NOW+8*3600
        with patch('network_redirect.game_clock.now',return_value=when):
            self.ok(self.land(1));detail=self.land(11,tower_id=13)[-1][1]['tower_info']
            inspected=self.req(1039,des_id=940113,des_type=1,flag=10,fight_id=0);self.ok(inspected)
            data=next(d for e,d in inspected if e==11)
            self.assertEqual(data['role_combat_power'],detail['fight_power'])
            self.assertEqual(len(data['cortege_list']),detail['cortege_count'])
            role=self.b.profile();s=role['activity']['land'];key=s['towers']['13']['npc_id']
            baseline=copy.deepcopy(npc.catalog()[key]);expected=npc.units(key,8);captured=[]
            real=journey.battle
            def battle(role,cfg,rules,**kwargs):
                captured.extend(copy.deepcopy(kwargs['units'][1]));return real(role,cfg,rules,**kwargs)
            with patch.object(journey,'battle',side_effect=battle):
                out=self.land(4,flag=1,des_type=2,des_id=13);self.ok(out)
            self.assertEqual(captured,expected);self.assertEqual(npc.catalog()[key],baseline)
            self.assertEqual(self.b.profile()['activity']['land']['attack_count'],1)

    def test_entry_guards_drop_over_sixty_percent_and_top_pools_stay_identical(self):
        rules=self.b.activity_rules
        previous=dict(rules,land_guard_tier_by_type=['T1','T1','T2','T3'])
        for map_level in range(1,5):
            for typ in (1,2):
                self.assertEqual(npc.guard_pool(map_level,typ,rules),npc.guard_pool(map_level,typ,previous))
            for typ in (3,4):
                before=[npc.power(npc.catalog()[key],8) for key in npc.guard_pool(map_level,typ,previous)]
                after=[npc.power(npc.catalog()[key],8) for key in npc.guard_pool(map_level,typ,rules)]
                self.assertLess(max(after),min(before)*0.4)

    def test_saved_entry_guards_refresh_without_resetting_resources_or_occupation(self):
        when=NOW+8*3600
        with patch('network_redirect.game_clock.now',return_value=when):
            self.ok(self.land(1));role=self.b.profile();s=role['activity']['land']
            previous=dict(self.b.activity_rules,land_guard_tier_by_type=['T1','T1','T2','T3'])
            for typ in (3,4):
                key=npc.guard(s,typ,previous)
                s['towers'][str(10+typ)].update(npc_id=key,owner_name=npc.catalog()[key]['role']['name'],left_soul=123)
            s['tower_id']=14;s['towers']['14']['owner_type']=1
            self.b.save(role);before=copy.deepcopy(s['towers'])
            self.ok(self.land(1));current=self.b.profile()['activity']['land']
            for tid in ('11','12','14'):self.assertEqual(current['towers'][tid],before[tid])
            t=current['towers']['13']
            self.assertEqual(npc.catalog()[t['npc_id']]['tier'],'T4')
            for field in ('all_soul','left_soul','soul_per_tick','last_tick','expire','create_time'):
                self.assertEqual(t[field],before['13'][field])
            self.assertEqual(current['tower_id'],14)
            self.ok(self.land(5,tower_id=14));self.ok(self.land(1))
            current=self.b.profile()['activity']['land']
            self.assertEqual(npc.catalog()[current['towers']['14']['npc_id']]['tier'],'T5')
            self.assertEqual(current['towers']['14']['left_soul'],123)
            self.ok(self.land(1));self.assertEqual(self.b.profile()['activity']['land'],current)

    def test_stone_cards_credit_both_quantities_in_both_worlds(self):
        self.ok(self.land(1))
        for key,flip,count in (('boss',14,5),('hell',23,3)):
            for quantity in (10,20):
                role=self.b.profile();role['activity']['land'][key]=dict(layer=1,cards=[],rewards=[[5,10000,quantity,1]]*count)
                self.b.save(role)
                total=lambda r:sum(x['count'] for x in r['attachments'] if x['attach_type']==5 and x['type_id']==10000)
                before=total(role);self.ok(self.land(flip,index=1))
                self.assertEqual(total(self.b.profile())-before,quantity)
                self.assertEqual(self.land(flip,index=1)[0][0],55)
                self.assertEqual(total(self.b.profile())-before,quantity)

    def test_legacy_occupied_tower_keeps_saved_budget_until_daily_refresh(self):
        when=NOW+8*3600
        with patch('network_redirect.game_clock.now',return_value=when):
            self.ok(self.land(1));role=self.b.profile();s=role['activity']['land'];t=s['towers']['11']
            for k in ('soul_per_tick','defender_count'):t.pop(k)
            t.update(all_soul=600,left_soul=600,last_tick=when,expire=when+3600,owner_type=1)
            s['tower_id']=11;self.b.save(role)
        with patch('network_redirect.game_clock.now',return_value=when+600):
            self.ok(self.land(1));self.assertEqual(self.b.profile()['activity']['land']['soul_count'],100)
        with patch('network_redirect.game_clock.now',return_value=when+86400):
            self.ok(self.land(1));self.assertEqual(self.b.profile()['activity']['land']['towers']['11']['soul_per_tick'],80)
