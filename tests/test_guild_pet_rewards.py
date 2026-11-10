"""Native reward contracts and task -> inventory box -> training-pill flow."""
import copy
import unittest
from pathlib import Path
from unittest.mock import patch

from network_redirect import guild, pets, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode
from tests.test_guild_activity_fixes import GuildActivityFixTests


class GuildPetRewardTests(unittest.TestCase):
    setUp = GuildActivityFixTests.setUp
    req = GuildActivityFixTests.req

    def win(self, index, typ, payment=1):
        with patch('network_redirect.guild_hunt.simulate', return_value=(1, [], dict(fight_result_msg=dict(fight_result=[])))):
            return self.req(84, task_index=index, task_type=typ, pay_type=payment)[0]

    def quantity(self, tid):
        return sum(row['count'] for row in self.b.profile()['attachments'] if row['attach_type']==5 and row['type_id']==tid)

    def open_box(self, item_id, count=1, ok=True):
        self.serial += 1
        self.packet = encode(1051, dict(serial_num=self.serial, item_type=1346, item_id=item_id,
                                       item_count=count, des_type=1, des_id=0))
        self.replies = self.b.respond(self.packet, {'authenticated':True})
        self.decoded = [decode(p) for p in self.replies]
        events = [(d['id'], login_fields(d['data'])) for m,_,d in self.decoded if m==2998]
        self.assertEqual(any(op==55 for op,_ in events), not ok, events)
        return events

    def test_each_native_offer_drives_its_own_settlement(self):
        self.b.guild_rules['hunt_task_rewards'][0] = dict(reputation=7, union_funds=11, items=[[5,1001,2,1]])
        self.b.guild_rules['hunt_task_rewards'][1] = dict(reputation=13, union_funds=17, items=[[5,1338,3,1]])
        preview = self.req(83)[0]['union_task'][2]['prize_info']
        self.assertNotEqual(preview[1], preview[2])
        for typ in (1,2):
            before = self.b.profile()
            result = self.win(2,typ)
            after = self.b.profile()
            offer = preview[typ]
            self.assertEqual(result['prize_list'],offer['prize_list'])
            self.assertEqual(result['prize_reputation'],offer['add_reputation'])
            self.assertEqual(result['prize_union_gold'],offer['add_union_gold'])
            self.assertEqual(after['guild']['instances']['reputation']-before['guild']['instances']['reputation'],offer['add_reputation'])
            self.assertEqual(sum(row['attach_count'] for row in result['animal_info'].values()),1)
            self.assertEqual(result['task_state']['wander_times'],typ)
        self.assertEqual(self.quantity(1346),2)

    def test_recent_box_display_tracks_actual_success_failure_and_rollover(self):
        self.assertEqual(self.req(83)[0]['drop_baoxiang_item']['attach_count'],0)
        rules=pets.load_rules();rules['task_training_boxes']=2
        with patch('network_redirect.pets.load_rules',return_value=rules):
            result=self.win(1,1)
        self.assertEqual(result['task_state']['drop_baoxiang_item']['attach_count'],2)
        self.assertEqual(self.quantity(1346),2)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.req(83)[0]['drop_baoxiang_item']['attach_count'],2)
        with patch('network_redirect.guild_hunt.simulate',return_value=(4,[],dict(fight_result_msg=dict(fight_result=[])))):
            failure=self.req(84,task_index=1,task_type=2,pay_type=1)[0]
        self.assertEqual(failure['task_state']['drop_baoxiang_item']['attach_count'],0)
        self.assertEqual((failure['prize_reputation'],failure['prize_union_gold'],failure['prize_list'],failure['animal_info']),(0,0,{},{}))
        self.win(2,1)
        self.now=result['task_state']['task_last_time']
        self.assertEqual(self.req(83)[0]['drop_baoxiang_item']['attach_count'],0)

    def test_fund_settlement_reports_actual_amount_at_cap(self):
        role=self.b.profile();g=role['guild']['unions'][str(role['union_id'])]
        g['money']=self.b.guild_rules['money_cap']-5;self.b.save(role)
        self.assertEqual(self.win(1,1)['prize_union_gold'],5)
        self.assertEqual(self.win(1,2)['prize_union_gold'],0)

    def test_six_task_boxes_open_into_pills_with_native_events_and_replay_guard(self):
        for typ in (1,2):
            for index in (1,2,3):self.win(index,typ,typ)
        self.assertEqual(self.quantity(1346),6)
        item=next(i for i in self.b.profile()['attachments'] if i['type_id']==1346)
        before_pills=self.quantity(1345)
        with patch('network_redirect.activity.prepare',side_effect=AssertionError('box must not settle activities')), \
                patch('network_redirect.pets.summon.weighted_choice',return_value=15):
            events=self.open_box(item['id'])
        result=next(data for op,data in events if op==21)
        self.assertEqual((result['result'],result['type_id'],result['count']),(1,1346,1))
        self.assertEqual(result['attach_list'][1],dict(object_type=5,attach_type=1345,attach_count=15,attach_level=1))
        self.assertTrue(any(mid==1035 for mid,_,_ in self.decoded),'native inventory snapshot missing')
        saved=self.b.profile()
        with patch('network_redirect.pets.summon.weighted_choice',side_effect=AssertionError('replay must not reroll')):
            self.assertEqual(self.b.respond(self.packet,{'authenticated':True}),self.replies)
        self.assertEqual(self.b.profile(),saved)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        with patch('network_redirect.pets.summon.weighted_choice',side_effect=[10,15,20,10,20]) as draw:
            self.open_box(item['id'],5)
            self.assertEqual(draw.call_count,5)
        self.assertEqual(self.quantity(1346),0)
        self.assertEqual(self.quantity(1345)-before_pills,90)
        before=self.b.profile();self.open_box(item['id'],ok=False)
        self.assertEqual(self.b.profile(),before)

    def test_box_batch_limit_selected_stack_and_atomic_failure(self):
        role=self.b.profile();summon.add_item(role,1346,20)
        item=next(i for i in role['attachments'] if i['type_id']==1346)
        locked=copy.deepcopy(item);locked.update(id=summon.next_id(role),count=4,is_lock=True)
        role['attachments'].append(locked);self.b.save(role)
        for item_id,count in ((item['id'],0),(item['id'],16),(item['id'],21),(locked['id'],1)):
            before=self.b.profile();self.open_box(item_id,count,ok=False)
            self.assertEqual(self.b.profile(),before)
        before=self.b.profile()
        with patch('network_redirect.journey.grant',side_effect=ValueError('reward failure')):
            self.open_box(item['id'],ok=False)
        self.assertEqual(self.b.profile(),before,'failed grant consumed box')
        with patch('network_redirect.pets.summon.weighted_choice',side_effect=[10,15,20]*5) as draw:
            self.open_box(item['id'],15)
            self.assertEqual(draw.call_count,15)
        self.assertEqual(self.quantity(1345),225)
        rows={i['id']:i for i in self.b.profile()['attachments']}
        self.assertEqual(rows[item['id']]['count'],5)
        self.assertEqual(rows[locked['id']]['count'],4)

    def test_reward_configuration_rejects_duplicate_box_append(self):
        rules=copy.deepcopy(self.b.guild_rules)
        rules['hunt_task_rewards'][0]['items'].append([5,1346,1,1])
        with patch('network_redirect.guild.json.loads',return_value=rules),self.assertRaises(ValueError):
            guild.load_rules()

    def test_box_probability_intervals_cover_exactly_30_50_20_percent(self):
        role=self.b.profile();summon.add_item(role,1346,1)
        item=next(i for i in role['attachments'] if i['type_id']==1346)
        request=dict(item_type=1346,item_id=item['id'],item_count=1,des_type=1,des_id=0)
        counts={10:0,15:0,20:0}
        for roll in range(100):
            candidate=copy.deepcopy(role)
            with patch('network_redirect.summon.secrets.randbelow',return_value=roll) as rng:
                packets=pets.use_box(candidate,request)
            rng.assert_called_once_with(100)
            result=login_fields(decode(packets[0])[2]['data'])
            amount=result['attach_list'][1]['attach_count']
            self.assertEqual(amount,10 if roll<30 else 15 if roll<80 else 20)
            counts[amount]+=1
        self.assertEqual(counts,{10:30,15:50,20:20})

    def test_box_pool_validation_rejects_bad_counts_and_probabilities(self):
        for pool in ([], [{'count':15,'weight':100}],
                     [{'count':10,'weight':30},{'count':10,'weight':50},{'count':20,'weight':20}],
                     [{'count':10,'weight':30},{'count':15,'weight':50},{'count':20,'weight':19}],
                     [{'count':10,'weight':0},{'count':15,'weight':80},{'count':20,'weight':20}],
                     [{'count':10,'weight':30.0},{'count':15,'weight':50},{'count':20,'weight':20}]):
            with self.subTest(pool=pool):
                rules=pets.load_rules();rules['training_box_pool']=pool
                with patch('network_redirect.pets.json.loads',return_value=rules),self.assertRaises(ValueError):
                    pets.load_rules()


del GuildActivityFixTests
