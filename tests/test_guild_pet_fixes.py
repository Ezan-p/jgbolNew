import copy
import unittest
from unittest.mock import patch

from tests.test_guild_activity_fixes import GuildActivityFixTests
from network_redirect import guild_trial, guild, guild_combat, summon
from network_redirect.backend import Backend
from pathlib import Path


class SpiritLandTests(unittest.TestCase):
    setUp=GuildActivityFixTests.setUp
    req=GuildActivityFixTests.req

    def test_task_settlement_precedes_replay_and_updates_counts(self):
        replay=dict(fight_result_msg=dict(fight_result=[]),damage_total=0)
        with patch('network_redirect.guild_hunt.simulate',return_value=(1,[],replay)):
            rows=self.req(84,task_index=1,task_type=2,pay_type=1)
        self.assertEqual(rows[0]['task_state']['free_task_times'],2)
        self.assertEqual(rows[0]['task_state']['wander_times'],1)
        self.assertTrue(rows[0]['fight_result'])
        self.assertIn('fight_result_list',rows[1])
        self.assertEqual(rows[0]['task_state'],self.req(83)[0])
        self.req(84,task_index=2,task_type=1,pay_type=1)
        self.assertEqual(self.req(84,task_index=3,task_type=1,pay_type=1)[0]['task_state']['free_task_times'],0)
        before=self.b.profile();self.req(84,ok=False,task_index=1,task_type=2,pay_type=1)
        self.assertEqual(self.b.profile(),before)

    def test_task_loss_keeps_free_count_and_no_rewards(self):
        fake=(4,[],dict(fight_result_msg=dict(fight_result=[])))
        with patch('network_redirect.guild_hunt.simulate',return_value=fake):
            data=self.req(84,task_index=1,task_type=2,pay_type=1)[0]
        self.assertFalse(data['fight_result']);self.assertEqual(data['prize_list'],{})
        self.assertEqual(data['task_state']['free_task_times'],3)
        self.assertEqual(data['task_state']['wander_times'],0)

    def encounter(self):
        self.req(84,task_index=1,task_type=1,pay_type=1)
        return self.req(86,two_type=2)[0]

    def test_capture_returns_real_pet_and_repeated_exit_is_safe(self):
        encounter=self.encounter();role=self.b.profile();summon.add_item(role,1341,1);self.b.save(role)
        data=self.req(87,two_type=2,catch_type=1341)[0]
        pet=data['animal_list'][1];self.assertEqual(pet['type_id'],encounter['boss_info']['type_id'])
        self.assertGreater(pet['id'],0)
        for key in ('quality','level','star_level','grow_values','train_levels','cur_exp'):self.assertIn(key,pet)
        count=len(self.b.profile()['activity']['home']['pets'])
        for _ in range(2):self.req(87,two_type=1)
        self.assertEqual(len(self.b.profile()['activity']['home']['pets']),count)
        self.assertNotIn('boss_info',self.req(86,two_type=1)[0])

    def test_pending_encounter_survives_query_reconnect_and_can_abandon(self):
        encounter=self.encounter()
        with patch('network_redirect.guild_offline.roll',side_effect=lambda s,n:n-1):
            failure=self.req(87,two_type=2,catch_type=1338)[0]
        self.assertEqual(failure['flag'],2)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        data=self.req(86,two_type=1)[0]
        self.assertEqual(data['boss_info'],encounter['boss_info']);self.assertEqual(data['left_times'],2)
        before=self.b.profile();self.req(86,ok=False,two_type=2);self.assertEqual(self.b.profile(),before)
        self.req(87,two_type=1);self.assertIsNone(self.b.profile()['guild']['instances']['field'])

    def test_four_random_floors_persist_and_difficulty_increases(self):
        first=self.req(79)[0];role=self.b.profile();a=role['guild']['instances'];bosses=copy.deepcopy(a['train_bosses'])
        self.assertEqual(len({row['type_id'] for row in bosses}),4)
        for row in bosses:
            self.assertTrue(5000<=row['type_id']<6000);self.assertEqual(int(summon.BASES[row['type_id']]['quality']),5)
        for left,right in zip(bosses,bosses[1:]):
            for key in ('hp','level','attack','defense','magic'):self.assertLess(left[key],right[key])
        serial=role['guild']['random_serial'];self.req(79)
        self.assertEqual(self.b.profile()['guild']['random_serial'],serial)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.req(79)[0]['boss_type'],first['boss_type'])
        self.assertEqual(self.b.profile()['guild']['instances']['train_bosses'],bosses)

    def test_floor_kills_advance_rewards_and_only_play_latest_battle(self):
        self.req(79)
        fake=(1,[],dict(fight_result_msg=dict(fight_result=[]),damage_total=1000000000))
        for floor in range(1,5):
            with patch('network_redirect.guild_instances.simulate',return_value=fake):data=self.req(80)[0]
            self.assertEqual(len(data['fight_result_list']),1)
            info=self.req(79)[0];self.assertEqual(info['result'],58)
            self.assertEqual(info['cleared_layer'],floor);self.assertEqual(info['boss_layer'],min(4,floor+1))
            claim=self.req(82)[0]
            self.assertEqual(claim['add_catch_count'],0)
            self.assertEqual(claim['trial_state'],self.req(79)[0])
            self.assertEqual(claim['trial_state']['result'],54 if floor==4 else 1)
            before=self.b.profile();self.req(82,ok=False);self.assertEqual(self.b.profile(),before)
        self.assertEqual(self.req(79)[0]['result'],54)
        before=self.b.profile();self.req(80,ok=False);self.assertEqual(self.b.profile(),before)
        self.assertEqual(self.b.profile()['guild']['instances']['lucky_bonus'],0)

    def test_floor_attempt_limit_damage_and_no_partial_clear_reward(self):
        fake=(4,[],dict(fight_result_msg=dict(fight_result=[]),damage_total=1000))
        with patch('network_redirect.guild_instances.simulate',return_value=fake):
            for _ in range(3):self.req(80)
        info=self.req(79)[0]
        self.assertEqual(info['boss_info']['boss_hp'],147000);self.assertEqual(info['remaining_attempts'],0)
        self.req(82,ok=False)
        before=self.b.profile();self.req(80,ok=False);self.assertEqual(self.b.profile(),before)
        self.now+=86400
        info=self.req(79)[0];self.assertEqual(info['remaining_attempts'],3)
        self.assertEqual((info['boss_layer'],info['cleared_layer']),(1,0))

    def test_real_replay_uses_preview_boss_and_floor_stats(self):
        info=self.req(79)[0];role=self.b.profile();s,g=guild.prepare(role,self.now,self.b.guild_rules)
        _,_,replay=guild_combat.simulate(role,s,self.b.guild_rules,self.b.journey_rules,27,'试炼',9000)
        self.assertEqual(replay['line_up_msg']['lineup'][0]['des_type'],info['boss_type'])
        self.assertEqual(replay['trial_boss']['hp'],info['boss_info']['boss_full_hp'])
        self.assertTrue(replay['fight_result_msg']['fight_result'])

    def test_old_save_migration_preserves_claims_damage_deadline(self):
        a=dict(train_open=True,train_done=False,train_hp=6000,train_claimed_stage=1,train_end=123,train_attempts=2)
        guild_trial.prepare(a,dict(random_serial=0),self.b.guild_rules,50)
        self.assertEqual((a['train_cleared'],a['train_floor'],a['train_hp'],a['train_end'],a['train_floor_attempts']),(1,2,225000,123,2))

    def test_healing_boss_uses_final_hp_instead_of_total_damage(self):
        fake=(4,[],dict(fight_result_msg=dict(fight_result=[]),damage_total=15000,boss_remaining_hp=3000))
        with patch('network_redirect.guild_instances.simulate',return_value=fake):self.req(80)
        info=self.req(79)[0]
        self.assertEqual((info['boss_layer'],info['cleared_layer'],info['boss_info']['boss_hp']),(1,0,3000))
        self.req(82,ok=False)

    def test_level_scaling_preserves_damage_progress_and_reconnect(self):
        self.req(79)
        role=self.b.profile();a=role['guild']['instances']
        types=[v['type_id'] for v in a['train_bosses']]
        a.update(train_floor=2,train_cleared=1,train_claimed_stage=1,
                 train_open=True,train_hp=187500,train_floor_attempts=2,train_end=self.now+123)
        role['level']=80;self.b.save(role)
        info=self.req(79)[0]
        self.assertEqual(info['boss_info']['boss_full_hp'],960000)
        self.assertEqual(info['boss_info']['boss_hp'],480000)
        self.assertEqual(info['boss_info']['level'],95)
        role=self.b.profile();a=role['guild']['instances']
        self.assertEqual([v['type_id'] for v in a['train_bosses']],types)
        self.assertEqual((a['train_cleared'],a['train_claimed_stage'],a['train_floor_attempts'],a['train_end']),
                         (1,1,2,self.now+123))
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.req(79)[0],info)

    def test_existing_four_floor_save_scales_without_resetting_progress(self):
        self.req(79);role=self.b.profile();a=role['guild']['instances']
        for boss,hp in zip(a['train_bosses'],(10000,20000,35000,55000)):boss['hp']=hp
        a.update(train_floor=2,train_cleared=1,train_hp=5000,train_floor_attempts=2,
                 train_claimed_stage=1,train_end=self.now+200)
        self.b.save(role)
        info=self.req(79)[0]
        self.assertEqual(info['boss_info']['boss_hp'],93750)
        self.assertEqual(info['remaining_attempts'],1)
        self.assertEqual(self.b.profile()['guild']['instances']['train_claimed_stage'],1)
        self.assertEqual(self.req(79)[0],info)

    def test_base_strength_growth_and_level_scaling(self):
        self.req(79);role=self.b.profile();base=copy.deepcopy(role['guild']['instances']['train_bosses'])
        self.assertEqual(base[0]['hp'],150000)
        self.assertEqual(base[0]['attack'],9000)
        for left,right in zip(base,base[1:]):
            for key in ('hp','attack','defense','magic'):self.assertEqual(right[key]*2,left[key]*5)
        for level in (60,80,99):
            role=self.b.profile();role['level']=level;self.b.save(role);self.req(79)
            for first,boss in zip(base,self.b.profile()['guild']['instances']['train_bosses']):
                for key in ('hp','attack','defense','magic'):
                    self.assertEqual(boss[key],first[key]*level*level//2500)

    def test_cumulative_rewards_are_only_silver_and_peaches_and_cannot_repeat(self):
        preview=self.req(79)[0]['train_prize']
        role=self.b.profile();a=role['guild']['instances']
        a.update(train_cleared=3,train_floor=4)
        self.b.save(role);before=self.b.profile()
        def peaches(r):return sum(v.get('count',0) for v in r['attachments'] if v['attach_type']==5 and v['type_id']==1001)
        claim=self.req(82)[0];after=self.b.profile()
        self.assertEqual(claim['prize_list'],preview[3]['prize_list'])
        self.assertEqual(after['silver_coin']-before['silver_coin'],150000)
        self.assertEqual(peaches(after)-peaches(before),15)
        self.assertEqual(after['guild']['unions'],before['guild']['unions'])
        for key in ('reputation','week_score','total_reputation','lucky_bonus'):
            self.assertEqual(after['guild']['instances'].get(key),before['guild']['instances'].get(key))
        self.assertEqual((claim['add_reputation'],claim['add_union_gold'],claim['add_catch_count']),(0,0,0))
        self.req(82,ok=False);self.assertEqual(self.b.profile(),after)
        after['guild']['instances'].update(train_cleared=4,train_done=True);self.b.save(after)
        claim=self.req(82)[0]
        self.assertEqual(claim['prize_list'],preview[1]['prize_list'])
        self.assertEqual(self.b.profile()['silver_coin']-before['silver_coin'],200000)
        self.assertEqual(peaches(self.b.profile())-peaches(before),20)


del GuildActivityFixTests
