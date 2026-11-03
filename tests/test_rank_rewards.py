"""Rank reward boundaries, atomic settlement and stable promotion identities."""
import copy
from pathlib import Path
from unittest.mock import patch
from test_activity import ActivityCase, NOW
from network_redirect import activity_rank as rank
from network_redirect.backend import Backend


class RankRewardTests(ActivityCase):
    def owned(self, role, tid):
        return sum(i['count'] for i in role['attachments'] if i['attach_type']==5 and i['type_id']==tid)

    def arrange(self, target, source=None):
        role=self.b.profile(); source=source or target+1
        role['energy']=100
        role['activity'].update(rank_order=source,rank_origin_order=source,rank_slots={},rank_count=0,
                                rank_day_best=source,rank_reset_version=1,rank_records=[])
        # Lower opponents are available through the existing revenge route.
        ident=rank.identity(role['activity'],target)
        role['activity']['rank_revenge']=ident
        self.b.save(role)
        return self.b.profile(),ident

    def fight(self,target,ident,result=1):
        with patch('network_redirect.activity_rank.journey.battle',return_value=(result,[],[])), \
             patch('network_redirect.activity_rank.secrets.randbelow',return_value=0):
            events=self.req(1026,fight_type=2,des_type=2,des_value=target,des_id=ident)
        self.ok(events)
        return events

    def test_all_bonus_boundaries_retries_restarts_and_repeated_wins(self):
        for target,tid,count in ((1,1152,2),(10,1152,2),(11,1152,1),(50,1152,1),
                                 (51,1156,1),(100,1156,1),(101,1001,50),(500,1001,50)):
            with self.subTest(target=target):
                for repeat in range(2):
                    before,ident=self.arrange(target)
                    events=self.fight(target,ident);after=self.b.profile()
                    expected={1001:5,1152:0,1156:0};expected[tid]+=count
                    for item,amount in expected.items():
                        self.assertEqual(self.owned(after,item)-self.owned(before,item),amount)
                    bonus=next(d['local_rank_battle_bonus'] for e,d in events if e==80 and 'local_rank_battle_bonus' in d)
                    self.assertEqual(bonus['target_order'],target)
                    self.assertEqual(bonus['prizes'][1],dict(object_type=5,attach_type=tid,attach_count=count,attach_level=1))
                    self.assertEqual(len(next(d for e,d in events if e==33)),5)
                    self.assertEqual(after['energy'],before['energy']-1)
                    self.assertEqual(after['activity']['rank_count'],1)
                    self.assertEqual(after.get('recharge'),before.get('recharge'))
                    self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
                    self.assertEqual(self.b.profile(),after)
                    self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
                    self.assertEqual(self.b.profile(),after)
                    events=self.req(1244,fight_type=2);self.ok(events)
                    self.assertFalse(any(e==80 and 'local_rank_battle_bonus' in d for e,d in events))
                    self.assertEqual(self.b.profile(),after)

    def test_bonus_uses_opponent_rank_before_swap_not_winner_rank(self):
        before,ident=self.arrange(11,source=10)
        self.fight(11,ident);after=self.b.profile()
        self.assertEqual(after['activity']['rank_order'],10)
        self.assertEqual(self.owned(after,1152)-self.owned(before,1152),1)

    def test_loss_draw_and_rank_501_have_no_bonus(self):
        for target,source,result in ((1,2,4),(1,2,0),(501,500,1)):
            before,ident=self.arrange(target,source)
            events=self.fight(target,ident,result);after=self.b.profile()
            bonus=next(d['local_rank_battle_bonus'] for e,d in events if e==80 and 'local_rank_battle_bonus' in d)
            self.assertFalse(bonus['prizes'])
            for tid in (1152,1156):self.assertEqual(self.owned(after,tid),self.owned(before,tid))
            self.assertEqual(self.owned(after,1001)-self.owned(before,1001),5 if result==1 else 0)

    def test_defence_has_no_bonus(self):
        before,ident=self.arrange(11,source=10)
        role=copy.deepcopy(before)
        with patch('network_redirect.activity_rank.journey.battle',return_value=(1,[],[])):
            win,replay=rank.simulate(role,11,NOW,self.b.journey_rules,defence=True)
        self.assertTrue(win)
        self.assertNotIn('challenge_bonus',replay)
        self.assertEqual(role['attachments'],before['attachments'])

    def test_bonus_failure_rolls_back_cards_costs_rank_and_retries(self):
        before,ident=self.arrange(10)
        with patch('network_redirect.activity_rank.journey.battle',return_value=(1,[],[])), \
             patch('network_redirect.activity.prizes',side_effect=ValueError('bonus cannot be encoded')):
            self.assertEqual(self.req(1026,fight_type=2,des_type=2,des_value=10,des_id=ident)[0][0],55)
        self.assertEqual(self.b.profile(),before)
        self.fight(10,ident)
        self.assertEqual(self.owned(self.b.profile(),1152)-self.owned(before,1152),2)

    def test_old_claims_keep_ids_and_new_thresholds_remain_claimable(self):
        role=self.b.profile();state=role['activity']
        state.update(rank_reward_version=2,rank_reached_order=1,rank_promotions=list(range(4,11)))
        self.b.save(role);before=self.b.profile()
        for ident in range(4,11):self.assertEqual(self.req(1203,exchange_type=ident)[0][0],55)
        self.assertEqual(self.b.profile(),before)
        for ident in (11,12,13):self.ok(self.req(1203,exchange_type=ident))
        after=self.b.profile()
        self.assertEqual(after['gold_coin']-before['gold_coin'],1000)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        for ident in (11,12,13):self.assertEqual(self.req(1203,exchange_type=ident)[0][0],55)
        self.assertEqual(self.b.profile(),after)
