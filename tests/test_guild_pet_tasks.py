"""Spirit-land task rewards, stable target identities and UTC+8 daily resets."""
import copy
import unittest
from pathlib import Path
from unittest.mock import patch

from network_redirect.backend import Backend
from tests.test_guild_activity_fixes import GuildActivityFixTests


class SpiritLandTaskTests(unittest.TestCase):
    setUp=GuildActivityFixTests.setUp
    req=GuildActivityFixTests.req

    def targets(self):
        return list(self.req(83)[0]['union_task'].values())

    def test_awarded_items_and_reputation_match_preview_for_every_target_and_mode(self):
        replay=dict(fight_result_msg=dict(fight_result=[]))
        for task_type in (1,2):
            self.now+=86400
            previews=self.targets()
            for row in previews:
                with self.subTest(task_type=task_type,index=row['index']):
                    before=self.b.profile()
                    with patch('network_redirect.guild_hunt.simulate',return_value=(1,[],replay)):
                        result=self.req(84,task_index=row['index'],task_type=task_type,pay_type=1)[0]
                    expected=row['prize_info'][task_type]
                    self.assertEqual(result['prize_list'],expected['prize_list'])
                    self.assertEqual(result['prize_reputation'],expected['add_reputation'])
                    silver=sum(p['attach_count'] for p in expected['prize_list'].values() if p['object_type']==12)
                    self.assertEqual(silver,1000*row['index'])
                    after=self.b.profile()
                    self.assertEqual(after['silver_coin']-before['silver_coin'],silver-self.b.guild_rules['hunt_silver'])
                    for prize in expected['prize_list'].values():
                        if prize['object_type']!=5:continue
                        def quantity(role):
                            return sum(item['count'] for item in role['attachments'] if item['attach_type']==5 and item['type_id']==prize['attach_type'])
                        self.assertEqual(quantity(after)-quantity(before),prize['attach_count'])

    def win(self,index,typ,payment):
        replay=dict(fight_result_msg=dict(fight_result=[]))
        with patch('network_redirect.guild_hunt.simulate',return_value=(1,[],replay)):
            return self.req(84,task_index=index,task_type=typ,pay_type=payment)[0]

    def test_six_independent_challenges_use_three_free_then_three_paid(self):
        initial=self.req(83)[0]
        self.assertEqual((initial['free_task_times'],initial['pay_task_times'],initial['pay_task_gold']),(3,3,100))
        gold=self.b.profile()['gold_coin']
        # Interleave types and targets: each type is independent, not a fixed
        # assignment of leisure=free and advanced=paid.
        sequence=[(2,2),(2,1),(1,1),(3,2),(1,2),(3,1)]
        for n,(index,typ) in enumerate(sequence,1):
            result=self.win(index,typ,1 if n<=3 else 2)
            state=result['task_state']
            self.assertEqual((state['free_task_times'],state['pay_task_times']),(max(0,3-n),3-max(0,n-3)))
            self.assertEqual(self.b.profile()['gold_coin'],gold-100*max(0,n-3))
            self.assertTrue(state['union_task'][index]['completed_modes'][typ])
            self.assertEqual(state['union_task'][index]['completed'],all(state['union_task'][index]['completed_modes'].values()))
            for op in (84,85):
                for payment in (1,2):
                    before=self.b.profile()
                    self.req(op,ok=False,task_index=index,task_type=typ,pay_type=payment)
                    self.assertEqual(self.b.profile(),before)
            if n==1:
                self.assertFalse(state['union_task'][index]['completed_modes'][1])
                self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
                self.assertEqual(self.req(83)[0],state)
        self.assertEqual([row['index'] for row in self.targets()],[1,2,3])
        self.assertTrue(all(row['completed'] for row in self.targets()))
        self.assertEqual(state['wander_times'],6)
        self.assertEqual(self.b.profile()['guild']['instances']['reputation'],120)
        self.now=state['task_last_time']
        refreshed=self.req(83)[0]
        self.assertEqual((refreshed['free_task_times'],refreshed['pay_task_times']),(3,3))
        self.assertTrue(all(row['completed_modes']=={1:False,2:False} for row in refreshed['union_task'].values()))
        self.assertEqual(self.b.profile()['guild']['instances']['task_modes'],{})

    def test_legacy_paid_completions_preserve_used_quotas_and_resources(self):
        self.req(83)
        role=self.b.profile();state=role['guild']['instances']
        state.update(tasks=[1,2],paid_tasks=1,completed_tasks=[1,2,3])
        state.pop('task_modes');self.b.save(role)
        result=self.req(83)[0]
        self.assertEqual((result['free_task_times'],result['pay_task_times']),(1,2))
        self.assertTrue(all(row['completed_modes']=={1:True,2:False} for row in result['union_task'].values()))
        after=self.b.profile()
        for key in ('gold_coin','silver_coin','attachments'):
            self.assertEqual(after[key],role[key])
        self.win(1,2,1)
        self.assertEqual(self.b.profile()['guild']['instances']['tasks'],[1,2,1])

    def test_payment_guards_do_not_charge_or_complete_tasks(self):
        before=self.b.profile()
        self.req(84,ok=False,task_index=1,task_type=1,pay_type=2)
        self.assertEqual(self.b.profile(),before)
        for index in (1,2,3):self.win(index,1,1)
        before=self.b.profile()
        self.req(84,ok=False,task_index=1,task_type=2,pay_type=1)
        self.assertEqual(self.b.profile(),before)
        role=self.b.profile();role['gold_coin']=99;self.b.save(role)
        self.req(84,ok=False,task_index=1,task_type=2,pay_type=2)
        self.assertEqual(self.b.profile(),role)
        role['gold_coin']=100;self.b.save(role)
        state=self.win(1,2,2)['task_state']
        self.assertEqual(self.b.profile()['gold_coin'],0)
        self.assertEqual(state['pay_task_times'],2)

    def test_paid_failure_can_retry_without_completing_other_mode(self):
        for index in (1,2,3):self.win(index,1,1)
        before=self.b.profile()
        with patch('network_redirect.guild_hunt.simulate',return_value=(4,[],dict(fight_result_msg=dict(fight_result=[])))):
            result=self.req(84,task_index=2,task_type=2,pay_type=2)[0]
        self.assertFalse(result['fight_result'])
        self.assertEqual(result['prize_list'],{})
        self.assertEqual(result['task_state']['pay_task_times'],3)
        self.assertEqual(self.b.profile()['gold_coin'],before['gold_coin']-100)
        self.assertEqual(result['task_state']['union_task'][2]['completed_modes'],{1:True,2:False})
        self.assertTrue(self.win(2,2,2)['task_state']['union_task'][2]['completed'])

    def test_failed_challenge_stays_available_then_refreshes_at_midnight(self):
        before=self.req(83)[0]
        fake=(4,[],dict(fight_result_msg=dict(fight_result=[])))
        with patch('network_redirect.guild_hunt.simulate',return_value=fake):
            result=self.req(84,task_index=2,task_type=2,pay_type=1)[0]
        self.assertFalse(result['fight_result'])
        self.assertEqual(result['task_state']['union_task'],before['union_task'])
        self.assertIn('2',self.b.profile()['guild']['instances']['task_opponents'])
        self.req(84,task_index=3,task_type=1,pay_type=1)
        self.now=before['task_last_time']-1
        self.assertEqual([row['index'] for row in self.targets()],[1,2,3])
        self.assertEqual(self.targets()[2]['completed_modes'],{1:True,2:False})
        self.now+=1
        after=self.req(83)[0]
        self.assertEqual([row['index'] for row in after['union_task'].values()],[1,2,3])
        self.assertFalse(any(done for row in after['union_task'].values() for done in row['completed_modes'].values()))
        self.assertEqual((after['free_task_times'],after['pay_task_times']),(3,3))
        self.assertNotEqual(before['union_task'][1]['task_info'],after['union_task'][1]['task_info'])
        state=self.b.profile()['guild']['instances']
        self.assertEqual((state['completed_tasks'],state['tasks'],state['paid_tasks'],state['task_opponents']),([],[],0,{}))
        self.assertEqual(after['task_day'],before['task_day']+1)
        self.assertEqual(after['task_last_time']-before['task_last_time'],86400)
        saved=self.b.profile()
        self.req(84,ok=False,task_index=1,task_type=1,pay_type=1,task_day=before['task_day'])
        self.assertEqual(self.b.profile(),saved)
        self.req(84,task_index=1,task_type=1,pay_type=1,task_day=after['task_day'])

    def test_old_completed_free_tasks_remain_visible_and_resources_are_preserved(self):
        self.req(84,task_index=1,task_type=1,pay_type=1)
        role=self.b.profile();role['guild']['instances'].pop('completed_tasks');role['guild']['instances'].pop('task_modes');self.b.save(role)
        expected=copy.deepcopy(role)
        self.assertEqual([row['index'] for row in self.targets()],[1,2,3])
        self.assertEqual(self.targets()[0]['completed_modes'],{1:True,2:False})
        self.assertEqual((self.req(83)[0]['free_task_times'],self.req(83)[0]['pay_task_times']),(2,3))
        after=self.b.profile()
        for key in ('gold_coin','silver_coin','attachments'):
            self.assertEqual(after[key],expected[key])
        self.assertEqual(after['guild']['instances']['reputation'],expected['guild']['instances']['reputation'])


del GuildActivityFixTests
