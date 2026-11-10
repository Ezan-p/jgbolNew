"""Independent trial attempts, authoritative timeout defeat and weekly adoption."""
import copy
import unittest
from pathlib import Path
from unittest.mock import patch

from network_redirect import combat_engine, guild, guild_combat, guild_trial
from network_redirect.backend import Backend
from network_redirect.protocol import decode
from tests.test_combat_round_limit import unit
from tests.test_guild_activity_fixes import GuildActivityFixTests


class GuildTrialTests(unittest.TestCase):
    setUp=GuildActivityFixTests.setUp
    req=GuildActivityFixTests.req

    def test_each_attempt_and_reconnect_start_with_full_hp(self):
        self.req(79)
        fake=(4,[],dict(fight_result_msg=dict(fight_result=[]),damage_total=149999,boss_remaining_hp=1))
        with patch('network_redirect.guild_instances.simulate',return_value=fake) as simulate:
            for _ in range(2):
                self.req(80)
                self.assertEqual(simulate.call_args.args[6],150000)
                self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
                info=self.req(79)[0]
                self.assertEqual((info['cleared_layer'],info['boss_info']['boss_hp']),(0,150000))
                self.req(82,ok=False)
        a=self.b.profile()['guild']['instances']
        self.assertEqual([r['boss_remaining_hp'] for r in a['train_record']],[1,1])
        self.assertEqual(a['lucky_bonus'],0)

    def test_thirtieth_round_requires_boss_kill_in_packets_and_replay(self):
        role=self.b.profile();s,_=guild.prepare(role,self.now,self.b.guild_rules)
        rules=copy.deepcopy(self.b.guild_rules)
        rules['train_floors'][0].update(hp=30,attack=0,defense=0,magic=0)
        # Run the real 30-round engine with deterministic loadouts. The generic
        # HP comparison would award victory in all three timeout cases.
        def battle(owner,cfg,jrules,*,units,slots):
            return combat_engine.Battle({},units,jrules,slots).run()
        for hp,attack,won in ((30,0,False),(31,1,False),(30,1,True),(29,1,True)):
            with self.subTest(hp=hp,attack=attack):
                rules['train_floors'][0]['hp']=hp
                armies=([unit(hp=1000,gongji=attack)],[unit()])
                with patch('network_redirect.journey.fighters',return_value=armies),patch('network_redirect.journey.battle',side_effect=battle):
                    result,packets,replay=guild_combat.simulate(role,s,rules,self.b.journey_rules,27,'试炼',1)
                self.assertEqual(1<=result<=3,won)
                self.assertEqual(replay['fight_result_msg']['final_result'],result)
                wire=[data for mid,_,data in map(decode,packets) if mid==1027]
                self.assertEqual(wire[0]['final_result'],result)
                self.assertEqual(replay['battle_rounds'],29 if hp==29 else 30)
                self.assertEqual(replay['stop_reason'],'elimination' if won else 'round_limit')
                self.assertEqual(replay['boss_remaining_hp']==0,won)
                self.assertEqual(replay['line_up_msg']['lineup'][0]['des_hp'],hp)

    def test_legacy_partial_damage_does_not_unlock_floors(self):
        a=dict(train_done=False,train_hp=1,train_claimed_stage=0)
        guild_trial.prepare(a,dict(random_serial=0),self.b.guild_rules,50)
        self.assertEqual((a['train_cleared'],a['train_floor'],a['train_hp']),(0,1,150000))

    def test_earned_adoptions_persist_until_weekly_reset(self):
        self.req(79);role=self.b.profile()
        role['guild']['instances'].update(train_cleared=3,train_floor=4)
        self.b.save(role)
        claim=self.req(82)[0]
        self.assertEqual((claim['add_catch_count'],claim['total_catch_times'],claim['left_catch_times']),(9,12,12))
        self.req(82,ok=False)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.req(88)[0]['total_catch_times'],12)
        self.now+=86400  # Saturday, daily trial reset retains this week's bonus.
        for _ in range(12):self.req(89)
        before=self.b.profile();self.req(89,ok=False);self.assertEqual(self.b.profile(),before)
        self.now+=86400
        self.assertEqual(self.req(88)[0]['left_catch_times'],0)
        self.now+=86400  # Monday clears used quota and earned bonus together.
        home=self.req(88)[0]
        self.assertEqual((home['total_catch_times'],home['left_catch_times']),(3,3))
        self.req(89,ok=False)

    def test_adoption_weekend_midnight_boundaries(self):
        day=self.b.profile()['guild']['day'];offset=self.b.guild_rules['timezone_offset_hours']*3600
        self.now=(day+1)*86400-offset-1
        self.req(89,ok=False)
        self.now+=1;self.req(89)
        self.now+=2*86400-1;self.req(89)
        self.now+=1;self.req(89,ok=False)

    def test_support_limit_bonus_persist_across_floors_and_reconnect(self):
        self.req(79);before=self.b.profile();self.req(78,ok=False)
        self.assertEqual(self.b.profile(),before)
        fake=(4,[],dict(fight_result_msg=dict(fight_result=[]),boss_remaining_hp=100))
        with patch('network_redirect.guild_instances.simulate',return_value=fake):self.req(80)
        for used in range(1,4):
            before=self.b.profile()['guild']['instances']
            gold=self.b.profile()['gold_coin']
            with patch('network_redirect.guild_instances.simulate') as battle:
                data=self.req(78)[0];battle.assert_not_called()
            self.assertEqual((data['support'],data['support_remaining'],data['support_bonus_percent']),(used,3-used,used*5))
            self.assertEqual(data['can_support'],used<3)
            self.assertEqual((data['support_gold'],data['gold_cost']),(20,20))
            self.assertEqual(self.b.profile()['gold_coin'],gold-20)
            for key in ('train_hp','train_record','train_floor_attempts','train_damage'):
                self.assertEqual(self.b.profile()['guild']['instances'][key],before[key])
            self.assertEqual(self.req(79)[0]['support_bonus_percent'],used*5)
        before=self.b.profile();self.req(78,ok=False);self.assertEqual(self.b.profile(),before)
        self.req(81,appoint_role=int(before['role_id']))
        win=(1,[],dict(fight_result_msg=dict(fight_result=[]),boss_remaining_hp=0))
        with patch('network_redirect.guild_instances.simulate',return_value=win):self.req(80)
        self.req(82)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        info=self.req(79)[0]
        self.assertEqual((info['boss_layer'],info['support'],info['support_bonus_percent']),(2,3,15))
        self.assertFalse(info['can_support']);self.req(78,ok=False)
        self.now+=86400
        info=self.req(79)[0]
        self.assertEqual((info['support'],info['support_remaining'],info['support_bonus_percent']),(0,3,0))
        self.assertFalse(info['can_support'])

    def test_expired_or_finished_trial_cannot_receive_support(self):
        self.req(79);role=self.b.profile();a=role['guild']['instances']
        a.update(train_open=True,train_end=self.now,train_support=1);self.b.save(role)
        self.assertFalse(self.req(79)[0]['can_support'])
        before=self.b.profile();self.req(78,ok=False);self.assertEqual(self.b.profile(),before)
        role['guild']['instances'].update(train_end=self.now+3600,train_done=True,train_cleared=4)
        self.b.save(role);self.assertFalse(self.req(79)[0]['can_support'])
        before=self.b.profile();self.req(78,ok=False);self.assertEqual(self.b.profile(),before)

    def test_support_insufficient_gold_does_not_change_state(self):
        self.req(79);role=self.b.profile()
        role['guild']['instances'].update(train_open=True,train_end=self.now+3600)
        role['gold_coin']=19;self.b.save(role)
        before=self.b.profile();self.req(78,ok=False);self.assertEqual(self.b.profile(),before)
        role['gold_coin']=20;self.b.save(role)
        data=self.req(78)[0]
        self.assertEqual((data['support'],data['support_bonus_percent']),(1,5))
        self.assertEqual(self.b.profile()['gold_coin'],0)
        before=self.b.profile();self.req(78,ok=False);self.assertEqual(self.b.profile(),before)

    def test_support_scales_only_challenger_snapshot_and_caps_legacy_counts(self):
        role=self.b.profile();s,_=guild.prepare(role,self.now,self.b.guild_rules)
        actor=copy.deepcopy(role);actor['role_id']+=100;actor['role_name']='指定队员'
        original=copy.deepcopy(actor)
        for count,percent in ((0,0),(1,5),(3,15),(999,15),(-1,0)):
            s.setdefault('instances',{})['train_support']=count
            captured=[]
            def battle(owner,cfg,rules,*,units,slots):
                captured.append(copy.deepcopy(units))
                return combat_engine.Battle({},units,rules,slots).run()
            with patch('network_redirect.journey.fighters',side_effect=lambda *args:([unit(hp=1000,max_hp=1000,gongji=100,fangyu=100,magic=100)],[unit()])),patch('network_redirect.journey.battle',side_effect=battle):
                _,_,replay=guild_combat.simulate(role,s,self.b.guild_rules,self.b.journey_rules,27,'试炼',actor_role=actor)
            ally,boss=captured[0][0][0],captured[0][1][0]
            for key in ('hp','max_hp'):self.assertEqual(ally[key],1000*(100+percent)//100)
            for key in ('gongji','fangyu','magic'):self.assertEqual(ally[key],100+percent)
            self.assertEqual(boss['hp'],150000)
            self.assertEqual(replay['trial_support']['support_bonus_percent'],percent)
            self.assertEqual(actor,original)


del GuildActivityFixTests
