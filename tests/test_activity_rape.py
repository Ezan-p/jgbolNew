"""Real wire-level offline 渡劫 lifecycle and NPC consistency checks."""
import copy
from unittest.mock import patch
from tests.test_activity import ActivityCase, NOW
from network_redirect import activity_rape as rape, activity_land_npc as npcs, activity_rank
from network_redirect.protocol import decode


class RapeTests(ActivityCase):
    def setUp(self):
        super().setUp()
        p=patch('network_redirect.activity_rape.roll_forms',return_value=[1,3,5])
        p.start();self.addCleanup(p.stop)

    def board(self):
        self.ok(self.req(1029,flag=1))
        return self.b.profile()['activity']['rape_boards']

    def fight(self,idx,ident,ft=3,value=None):
        return self.req(1026,fight_type=ft,des_type=1 if ft==12 else 2,des_value=idx if value is None else value,des_id=int(ident))

    def test_actual_battle_matches_inspection_and_persists(self):
        boards=self.board();ident,target=next(iter(boards[0]['form_list']['2'].items()))
        self.ok(self.req(1039,des_type=2,des_id=int(ident)))
        view=next(d for e,d in self.req(1039,des_type=2,des_id=int(ident)) if e==11)
        self.assertEqual(view['level'],target['level'])
        before=self.b.profile()
        self.ok(self.fight(1,ident))
        fight=next(d for m,_,d in self.decoded if m==1027)
        self.assertIn(fight['final_result'],range(7))
        self.assertEqual(self.b.profile()['energy'],before['energy']-1)
        self.assertEqual(self.b.profile()['activity']['rape_boards'][0]['form_list']['2'][ident]['has_win'],1<=fight['final_result']<=3)
        self.b.close()
        from network_redirect.backend import Backend
        self.b=Backend(__import__('pathlib').Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.b.profile()['activity']['rape_boards'],self.board())

    def test_full_clear_exact_rewards_duplicate_and_sweep_cost(self):
        boards=self.board();before=self.b.profile()
        with patch('network_redirect.activity_rape.journey.battle',return_value=(1,[],[])):
            self.ok(self.req(1072))
        after=self.b.profile()
        self.assertEqual(after['energy'],before['energy']-9)
        self.assertEqual(after['gold_coin'],before['gold_coin']-9)
        self.assertEqual(len(after['attachments']),len(before['attachments'])+12)
        self.assertTrue(all(b['reward_claimed'] for b in after['activity']['rape_boards']))
        self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
        self.assertEqual(after,self.b.profile())
        self.assertIn(55,[e for e,d in self.req(1072)])

    def test_refresh_changes_npc_invalidates_old_target_and_preserves_slot(self):
        b=self.board()[0];ident,old=next(iter(b['form_list']['2'].items()))
        self.ok(self.req(1041,form_index=1,object_type=2,object_id=int(ident)))
        rows=self.b.profile()['activity']['rape_boards'][0]['form_list']['2'];new=next(iter(rows.values()))
        self.assertNotEqual(new['npc_id'],old['npc_id']);self.assertEqual(new['rand'],old['rand'])
        before=self.b.profile();self.assertIn(55,[e for e,d in self.fight(1,ident)]);self.assertEqual(before,self.b.profile())
        self.ok(self.req(1029,flag=2));self.assertTrue(set(rows).isdisjoint(self.b.profile()['activity']['rape_boards'][0]['form_list']['2']))

    def test_revenge_win_ignore_expiry_and_forgery(self):
        ident=next(iter(self.board()[0]['form_list']['2']))
        with patch('network_redirect.activity_rape.journey.battle',return_value=(4,[],[])):
            self.ok(self.fight(1,ident))
        key,target=next(iter(self.b.profile()['activity']['rape_revenge'].items()))
        before=self.b.profile()
        self.assertIn(55,[e for e,d in self.fight(0,key,12,9999)]);self.assertEqual(before,self.b.profile())
        self.ok(self.req(1039,des_type=1,des_id=target['id']))
        with patch('network_redirect.activity_rape.journey.battle',return_value=(1,[],[])):
            self.ok(self.fight(0,key,12,target['skill_type']))
        after=self.b.profile();self.assertEqual(len(after['attachments']),len(before['attachments'])+1)
        self.assertIn(55,[e for e,d in self.fight(0,key,12,target['skill_type'])]);self.assertEqual(after,self.b.profile())
        self.ok(self.req(1060,request_id=int(key)))
        self.assertFalse(self.b.profile()['activity']['rape_revenge'])

    def test_special_dice_and_query_idempotence(self):
        for dice,count,claimed in (([1,2,3],2,False),([2,2,2],1,True)):
            r=self.b.profile();r['activity']['rape_boards']=None;self.b.save(r)
            with patch('network_redirect.activity_rape.roll_forms',return_value=dice):boards=self.board()
            self.assertTrue(all(b['skill_count']==count and b['reward_claimed']==claimed for b in boards))
            before=self.b.profile();self.board();self.assertEqual(before,self.b.profile())

    def test_thresholds_atomic_failure_rollover_and_match_range(self):
        self.board();r=self.b.profile();r.update(gold_coin=0,energy=0);self.b.save(r);before=self.b.profile()
        self.assertIn(55,[e for e,d in self.req(1029,flag=3)]);self.assertEqual(before,self.b.profile())
        self.assertIn(55,[e for e,d in self.req(1072)]);self.assertEqual(before,self.b.profile())
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            self.board();self.assertEqual(self.b.profile()['activity']['rape_refreshes'],0)
        for level in (8,25,60,99):
            r['level']=level
            for i in range(3):
                n=npcs.catalog()[rape.choose(r,i)]
                self.assertLessEqual(n['role']['level'],level)
                self.assertNotEqual(n['battle_validation']['status'],'replay_limit_observed')

    def test_old_board_migration_preserves_progress_and_no_regrant(self):
        r=self.b.profile()
        r['activity']['rape_boards']=[dict(skill_type=101,skill_count=1,form_list={'2':{str(i*10+j):dict(has_win=i==1 or j==1) for j in (1,2,3)}}) for i in (1,2,3)]
        self.b.save(r);before=len(r['attachments']);boards=self.board()
        self.assertTrue(boards[0]['reward_claimed']);self.assertFalse(boards[1]['reward_claimed'])
        self.assertEqual(len(self.b.profile()['attachments']),before)
        self.assertEqual(set(boards[0]['form_list']),{'1','2'})
        self.assertTrue(all('npc_id' in t for b in boards for t in b['form_list']['2'].values()))

    def test_expired_revenge_and_level_gates_are_atomic(self):
        ident=next(iter(self.board()[0]['form_list']['2']))
        with patch('network_redirect.activity_rape.journey.battle',return_value=(4,[],[])):
            self.ok(self.fight(1,ident))
        key,target=next(iter(self.b.profile()['activity']['rape_revenge'].items()))
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            self.board();before=self.b.profile()
            self.assertIn(55,[e for e,d in self.fight(0,key,12,target['skill_type'])]);self.assertEqual(before,self.b.profile())
        r=self.b.profile();r.update(level=7,vip_level=5);self.b.save(r);before=self.b.profile()
        self.assertIn(55,[e for e,d in self.req(1029,flag=1)])
        self.assertIn(55,[e for e,d in self.req(1072)]);self.assertEqual(before,self.b.profile())

    def test_partial_sweep_vip_cost_and_loss_keeps_target(self):
        self.board();r=self.b.profile();r.update(energy=2,vip_level=5);self.b.save(r);before=self.b.profile()
        with patch('network_redirect.activity_rape.journey.battle',return_value=(4,[],[])):
            out=self.req(1072);self.ok(out)
        result=next(d for e,d in out if e==114)
        self.assertEqual(len([k for k in result if isinstance(k,int)]),2)
        after=self.b.profile();self.assertEqual(after['energy'],0);self.assertEqual(after['gold_coin'],before['gold_coin'])
        self.assertFalse(any(t['has_win'] for b in after['activity']['rape_boards'] for t in b['form_list']['2'].values()))
