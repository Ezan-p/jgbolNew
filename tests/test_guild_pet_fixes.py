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
        fake=(1,[],dict(fight_result_msg=dict(fight_result=[]),damage_total=1000000))
        for floor in range(1,5):
            with patch('network_redirect.guild_instances.simulate',return_value=fake):data=self.req(80)[0]
            self.assertEqual(len(data['fight_result_list']),1)
            info=self.req(79)[0];self.assertEqual(info['result'],58)
            self.assertEqual(info['cleared_layer'],floor);self.assertEqual(info['boss_layer'],min(4,floor+1))
            claim=self.req(82)[0]
            self.assertEqual(claim['add_catch_count'],1)
            self.assertEqual(claim['trial_state'],self.req(79)[0])
            self.assertEqual(claim['trial_state']['result'],54 if floor==4 else 1)
            before=self.b.profile();self.req(82,ok=False);self.assertEqual(self.b.profile(),before)
        self.assertEqual(self.req(79)[0]['result'],54)
        before=self.b.profile();self.req(80,ok=False);self.assertEqual(self.b.profile(),before)
        self.assertEqual(self.b.profile()['guild']['instances']['lucky_bonus'],4)

    def test_floor_attempt_limit_damage_and_no_partial_clear_reward(self):
        fake=(4,[],dict(fight_result_msg=dict(fight_result=[]),damage_total=1000))
        with patch('network_redirect.guild_instances.simulate',return_value=fake):
            for _ in range(3):self.req(80)
        info=self.req(79)[0]
        self.assertEqual(info['boss_info']['boss_hp'],7000);self.assertEqual(info['remaining_attempts'],0)
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
        guild_trial.prepare(a,dict(random_serial=0),self.b.guild_rules)
        self.assertEqual((a['train_cleared'],a['train_floor'],a['train_hp'],a['train_end'],a['train_floor_attempts']),(1,2,6000,123,2))

    def test_healing_boss_uses_final_hp_instead_of_total_damage(self):
        fake=(4,[],dict(fight_result_msg=dict(fight_result=[]),damage_total=15000,boss_remaining_hp=3000))
        with patch('network_redirect.guild_instances.simulate',return_value=fake):self.req(80)
        info=self.req(79)[0]
        self.assertEqual((info['boss_layer'],info['cleared_layer'],info['boss_info']['boss_hp']),(1,0,3000))
        self.req(82,ok=False)


del GuildActivityFixTests
