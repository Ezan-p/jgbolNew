"""Original acquisition invariants from the in-game help and item descriptions."""
from tests.test_guild import GuildTests
from network_redirect import guild, summon
from unittest.mock import patch
import unittest

class AcquisitionTests(unittest.TestCase):
    req=GuildTests.req
    ok=GuildTests.ok
    role=GuildTests.role
    create=GuildTests.create
    legacy_setup=GuildTests.setUp
    # Do not inherit the legacy suite's test cases.
    def setUp(self):
        self.legacy_setup()
        self.create()
        self.b.guild_rules.update(pet_role_level=50,pet_union_level=5,wander_daily=0)
        r=self.role();r['level']=50
        g=r['guild']['unions'][str(r['union_id'])]
        g['popularity']=4*self.b.guild_rules['level_popularity'];self.b.save(r)

    def test_entry_gates(self):
        self.ok(83)
        for level,popularity in ((49,4),(50,3)):
            r=self.role();r['level']=level;r['guild']['unions'][str(r['union_id'])]['popularity']=popularity*self.b.guild_rules['level_popularity'];self.b.save(r)
            before=self.role();self.assertEqual(self.req(83)[-1][1],55);self.assertEqual(before,self.role())

    def test_paid_and_free_tasks_add_residents_and_one_encounter(self):
        self.ok(88);r=self.role();g=r['guild']['unions'][str(r['union_id'])];before=sum(g['resident_pets'].values())
        self.assertEqual(self.req(86,two_type=2)[-1][1],55)
        for payment in (1,2):self.ok(84,task_index=1,task_type=1,pay_type=payment)
        r=self.role();g=r['guild']['unions'][str(r['union_id'])]
        self.assertEqual(sum(g['resident_pets'].values()),before+2)
        self.assertEqual(self.ok(83)[-1][2]['wander_times'],2)
        for _ in range(2):self.ok(86,two_type=2);self.ok(87,two_type=1)
        self.assertEqual(self.req(86,two_type=2)[-1][1],55)

    def test_god_charm_guarantees_capture_and_missing_item_is_atomic(self):
        self.ok(84,task_index=1,task_type=1)
        self.ok(86,two_type=2)
        before=self.role();self.assertEqual(self.req(87,two_type=2,catch_type=1341)[-1][1],55);self.assertEqual(before,self.role())
        r=self.role();summon.add_item(r,1341,1);self.b.save(r)
        with patch('network_redirect.guild_offline.roll',side_effect=lambda s,n:n-1):result=self.ok(87,two_type=2,catch_type=1341)
        self.assertEqual(next(d for _,op,d in result if op==87)['flag'],1)
        self.assertEqual(len(self.role()['activity']['home']['pets']),1)
        self.assertEqual(set(guild.load_rules()['catch_prop_rates']),{'1338','1339','1340','1341'})
        items=self.ok(91,two_type=1)[-1][2]['item_list']
        self.assertEqual(len(items),6)

    def test_failed_task_does_not_spend_attempt_or_grant_pet(self):
        self.ok(88);before=self.role()
        replay=dict(fight_result_msg=dict(fight_result=[]))
        with patch('network_redirect.guild_hunt.simulate',return_value=(4,[],replay)):
            self.ok(84,task_index=1,task_type=2)
        r=self.role();a=r['guild']['instances']
        self.assertEqual(a['tasks'],[])
        self.assertEqual(a['paid_tasks'],0)
        self.assertEqual(self.ok(83)[-1][2]['wander_times'],0)
        self.assertEqual(r['guild']['unions'][str(r['union_id'])]['resident_pets'],before['guild']['unions'][str(before['union_id'])]['resident_pets'])

    def test_all_members_have_base_adoption_quota_without_week_score(self):
        from network_redirect.guild_instances import lucky_limit
        self.assertEqual(lucky_limit({'week_score':0},self.b.guild_rules),3)
        self.assertEqual(lucky_limit({'week_score':0,'lucky_bonus':2},self.b.guild_rules),5)

    def test_support_is_not_a_battle_and_does_not_deal_damage(self):
        self.ok(79);r=self.role();a=r['guild']['instances']
        a.update(train_open=True,train_hp=9000,train_end=1792818000,train_attempts=1)
        self.b.save(r)
        with patch('network_redirect.guild_instances.simulate',side_effect=AssertionError('support cannot fight')):
            result=self.ok(78)
        self.assertEqual([op for mid,op,_ in result if mid==1301],[78])
        a=self.role()['guild']['instances']
        self.assertEqual((a['train_hp'],a['train_attempts'],a['train_support']),(9000,1,1))

del GuildTests
