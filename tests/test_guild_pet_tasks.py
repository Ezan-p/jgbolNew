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

    def test_completed_targets_disappear_without_renumbering_or_paid_replay(self):
        self.req(84,task_index=2,task_type=1,pay_type=2)
        self.assertEqual([row['index'] for row in self.targets()],[1,3])
        for payment in (1,2):
            before=self.b.profile()
            self.req(84,ok=False,task_index=2,task_type=1,pay_type=payment)
            self.assertEqual(self.b.profile(),before)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual([row['index'] for row in self.targets()],[1,3])
        self.req(84,task_index=3,task_type=1,pay_type=1)
        self.req(84,task_index=1,task_type=1,pay_type=1)
        current=self.req(83)[0]
        self.assertEqual(current['union_task'],{})
        self.assertEqual((current['free_task_times'],current['pay_task_times']),(0,0))
        self.assertEqual(current['wander_times'],3)

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
        self.assertEqual([row['index'] for row in self.targets()],[1,2])
        self.now+=1
        after=self.req(83)[0]
        self.assertEqual([row['index'] for row in after['union_task'].values()],[1,2,3])
        self.assertNotEqual(before['union_task'][1]['task_info'],after['union_task'][1]['task_info'])
        state=self.b.profile()['guild']['instances']
        self.assertEqual((state['completed_tasks'],state['tasks'],state['paid_tasks'],state['task_opponents']),([],[],0,{}))
        self.assertEqual(after['task_day'],before['task_day']+1)
        self.assertEqual(after['task_last_time']-before['task_last_time'],86400)
        saved=self.b.profile()
        self.req(84,ok=False,task_index=1,task_type=1,pay_type=1,task_day=before['task_day'])
        self.assertEqual(self.b.profile(),saved)
        self.req(84,task_index=1,task_type=1,pay_type=1,task_day=after['task_day'])

    def test_old_completed_free_tasks_remain_hidden_and_resources_are_preserved(self):
        self.req(84,task_index=1,task_type=1,pay_type=1)
        role=self.b.profile();role['guild']['instances'].pop('completed_tasks');self.b.save(role)
        expected=copy.deepcopy(role)
        self.assertEqual([row['index'] for row in self.targets()],[2,3])
        after=self.b.profile()
        for key in ('gold_coin','silver_coin','attachments'):
            self.assertEqual(after[key],expected[key])
        self.assertEqual(after['guild']['instances']['reputation'],expected['guild']['instances']['reputation'])


del GuildActivityFixTests
