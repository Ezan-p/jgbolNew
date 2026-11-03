"""Promotion reset invalidates inherited eligibility before any claim can pay."""
from pathlib import Path
from unittest.mock import patch
from test_activity import ActivityCase, NOW
from network_redirect import activity, activity_rank as rank
from network_redirect.backend import Backend


class PromotionResetTests(ActivityCase):
    def legacy(self, already_reset=True, order=501):
        role=self.b.profile();state=role['activity']
        state.pop('rank_promotion_reset_version',None)
        if not already_reset:state.pop('rank_reset_version',None)
        state.update(rank_order=order,rank_origin_order=order,rank_slots={},rank_reached_order=1,
                     rank_promotions=[4,9,10],rank_score=12345,rank_count=2,rank_extra=9)
        self.b.save(role)
        return self.b.profile()

    def notice(self,events):
        return [d for e,d in events if e==80 and (d.get('local_rank_reset_notice') or d.get('local_rank_promotion_reset_notice'))]

    def test_old_claims_and_stale_challenges_blocked_before_board_but_normal_exchange_works(self):
        for already_reset in (False,True):
            before=self.legacy(already_reset)
            self.assertEqual(rank.masks(before['activity']),(0,0))
            for entry in rank.rules()['exchanges']:
                if entry['promote_order']:
                    self.assertEqual(self.req(1203,exchange_type=entry['index'])[0][0],55)
            self.assertEqual(self.req(1026,fight_type=2,des_type=2,des_id=930500,des_value=500)[0][0],55)
            self.assertEqual(self.b.profile(),before)
            self.ok(self.req(1203,exchange_type=1))
            self.assertEqual(self.b.profile()['activity']['rank_score'],12345-5000)
            self.assertNotIn('rank_promotion_reset_version',self.b.profile()['activity'])

    def test_rank_only_reset_save_clears_all_tiers_then_reearns_and_persists(self):
        before=self.legacy()
        events=self.req(1021,flag=0);self.ok(events)
        self.assertEqual(self.notice(events),[{'local_rank_promotion_reset_notice':True}])
        after=self.b.profile();state=after['activity']
        self.assertEqual((state['rank_order'],state['rank_reached_order'],state['rank_promotions']),(501,501,[]))
        self.assertEqual((state['rank_count'],state['rank_extra'],state['rank_score']),(2,9,12345))
        self.assertEqual(after['gold_coin'],before['gold_coin'])
        self.assertEqual(after['attachments'],before['attachments'])
        self.assertEqual((after['top_first_promote_time'],after['top_first_promote_prize']),(0,0))
        wire=next(d for m,_,d in self.decoded if m==1022)
        self.assertEqual((wire['promote_time'],wire['promote_prize']),(0,0))
        self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
        self.assertEqual(self.b.profile(),after)
        for entry in rank.rules()['exchanges']:
            if entry['promote_order']:self.assertEqual(self.req(1203,exchange_type=entry['index'])[0][0],55)
        # Losing does not establish eligibility; a new real win does.
        with patch('network_redirect.activity_rank.journey.battle',return_value=(4,[],[])):
            self.ok(self.req(1026,fight_type=2,des_type=2,des_id=930500,des_value=500))
        self.assertEqual(rank.masks(self.b.profile()['activity']),(0,0))
        self.ok(self.req(1026,fight_type=2,des_type=2,des_id=930500,des_value=500))
        self.assertEqual(self.b.profile()['activity']['rank_reached_order'],500)
        gold=self.b.profile()['gold_coin'];self.ok(self.req(1203,exchange_type=4))
        self.assertEqual(self.b.profile()['gold_coin']-gold,100)
        earned=self.b.profile()
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        for flag in (0,1):
            events=self.req(1021,flag=flag);self.ok(events)
            self.assertFalse(self.notice(events))
        self.assertEqual(self.b.profile(),earned)
        self.assertEqual(self.req(1203,exchange_type=4)[0][0],55)
        self.assertEqual(self.req(1203,exchange_type=10)[0][0],55)

    def test_repair_does_not_reset_rank_again_or_trust_current_rank_as_qualification(self):
        self.legacy(order=20)
        events=self.req(1021,flag=0);self.ok(events)
        state=self.b.profile()['activity']
        self.assertEqual((state['rank_order'],state['rank_reached_order']),(20,501))
        self.assertEqual(rank.masks(state),(0,0))
        self.assertEqual(self.notice(events),[{'local_rank_promotion_reset_notice':True}])
        self.assertEqual(self.req(1203,exchange_type=8)[0][0],55)

    def test_failed_reset_cannot_consume_migration_and_new_saves_are_unaffected(self):
        self.assertEqual(self.b.profile()['activity']['rank_promotion_reset_version'],1)
        events=self.req(1021,flag=0);self.ok(events);self.assertFalse(self.notice(events))
        before=self.legacy()
        with patch.object(rank,'board',side_effect=ValueError('encode failed')):
            self.assertEqual(self.req(1021,flag=0)[0][0],55)
        self.assertEqual(self.b.profile(),before)
        self.assertEqual(self.req(1203,exchange_type=5)[0][0],55)
        events=self.req(1021,flag=1);self.ok(events)
        self.assertEqual(len(self.notice(events)),1)
        self.assertEqual(self.b.profile()['activity']['rank_promotions'],[])
