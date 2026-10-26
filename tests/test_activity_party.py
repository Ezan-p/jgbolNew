"""Original packets through detached DB settlement; no live save touched."""
import copy
from unittest.mock import patch
from tests.test_activity import ActivityCase, NOW
from network_redirect import activity, activity_party as party, achievements
from network_redirect.backend import Backend
from network_redirect.protocol import decode
from pathlib import Path

class PartyTests(ActivityCase):
    def fight(self, paid=0):
        out=self.req(1026,fight_type=6,des_value=paid)
        self.ok(out)
        return dict(out)[29]

    def test_full_free_paid_cycle_and_replay(self):
        initial=self.b.profile()['gold_coin']
        for _ in range(10):
            data=self.fight()
            self.assertGreater(data['cur_damage'],0)
            self.assertTrue(data['damage_list'])
            self.assertLessEqual(data['cur_damage'],party.rules()['boss_hp'])
        before=self.b.profile()
        self.assertEqual(self.req(1026,fight_type=6)[0][0],55)
        self.assertEqual(before,self.b.profile())
        for _ in range(5):self.fight(1)
        before=self.b.profile();self.assertEqual(before['gold_coin'],initial-100)
        self.assertEqual(before['activity']['party']['week_lucky'],150)
        self.assertEqual(before['activity']['party']['peaches'],75)
        self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
        self.assertEqual(before,self.b.profile())
        self.assertEqual(self.req(1026,fight_type=6,des_value=1)[0][0],55)
        self.assertEqual(before,self.b.profile())

    def test_daily_history_felstar_and_no_double_award(self):
        self.fight();before=self.b.profile();gold=before['gold_coin']
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            h=dict(self.req(1049,query_type=2))[30];self.assertEqual(h['fight_count'],1)
            self.assertEqual(len(h['damage_list']),10);self.assertIn('id',h['felstar_info'])
            self.assertGreater(self.b.profile()['gold_coin'],gold)
            snapshot=self.b.profile();self.ok(self.req(1049,query_type=2));self.assertEqual(snapshot,self.b.profile())
            self.assertEqual(snapshot['activity']['party_count'],0)
            self.ok(self.req(1049,query_type=5,flag=2))
            self.assertEqual(self.req(1049,query_type=5,flag=2)[0][0],55)
            self.assertEqual(self.b.profile()['activity']['party']['history']['top_list'][1]['liked_times'],1)
        with patch('network_redirect.backend.time.time',return_value=NOW):
            self.ok(self.req(1049,query_type=1))
            self.assertEqual(self.req(1049,query_type=5,flag=2)[0][0],55)

    def test_monday_weekly_claim_and_restart(self):
        self.fight()
        with patch('network_redirect.backend.time.time',return_value=NOW+2*86400):
            h=dict(self.req(1049,query_type=3))[28]
            self.assertEqual(h['self_lucky_his'],10);self.assertGreater(h['self_order'],0)
            self.assertTrue(self.b.profile()['activity']['party']['pending'])
            self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
            self.ok(self.req(1201,flag=1));saved=self.b.profile()
            self.assertEqual(self.req(1201,flag=1)[0][0],55);self.assertEqual(saved,self.b.profile())
            self.assertEqual(saved['party_take_prize'],1)
            self.assertEqual(saved['activity']['party']['week_lucky'],0)

    def test_long_absence_keeps_week_prize(self):
        self.fight()
        with patch('network_redirect.backend.time.time',return_value=NOW+50*86400):
            self.ok(self.req(1049,query_type=3));self.assertTrue(self.b.profile()['activity']['party']['pending'])
            self.ok(self.req(1201,flag=1))

    def test_npcs_deterministic_and_inspectable(self):
        r=self.b.profile();day=activity.day(NOW,self.b.activity_rules)
        board=party.daily_board(r,day,86400,self.b.activity_rules)
        other=copy.deepcopy(r);other['role_combat_power']=99999999
        self.assertEqual(board,party.daily_board(other,day,86400,self.b.activity_rules))
        for ident in (next(iter(party.catalog())),next(reversed(party.catalog()))):
            self.ok(self.req(1039,des_type=1,des_id=ident,flag=3))
        self.assertTrue(all(n['role']['level']>=13 for n in party.catalog().values()))

    def test_bonus_cost_cap_and_atomic_failure(self):
        gold=self.b.profile()['gold_coin']
        for _ in range(10):self.ok(self.req(1202,flag=1))
        self.assertEqual(self.b.profile()['gold_coin'],gold-275)
        before=self.b.profile();self.assertEqual(self.req(1202,flag=1)[0][0],55);self.assertEqual(before,self.b.profile())
        r=self.b.profile();r['gold_coin']=0;self.b.save(r);before=self.b.profile()
        self.assertEqual(self.req(1026,fight_type=6,des_value=1)[0][0],55);self.assertEqual(before,self.b.profile())

    def test_restricted_period_level_and_no_lineup(self):
        self.b.activity_rules['party_period']=[39600,46800]
        with patch('network_redirect.backend.time.time',return_value=NOW+7200):
            self.assertEqual(self.req(1026,fight_type=6)[0][0],55)
            self.assertEqual(self.req(1202,flag=1)[0][0],55)
        r=self.b.profile();r['level']=12;self.b.save(r)
        self.assertEqual(self.req(1026,fight_type=6)[0][0],55)
        r=self.b.profile();r['level']=60
        for c in r['corteges']:c['order']=0
        self.b.save(r);before=self.b.profile()
        self.assertEqual(self.req(1026,fight_type=6)[0][0],55);self.assertEqual(before,self.b.profile())

    def test_legacy_migration_and_backwards_clock(self):
        r=self.b.profile();r['activity'].pop('party');r['activity'].update(party_count=2,party_damage=1234)
        self.b.save(r);self.ok(self.req(1049,query_type=1));p=self.b.profile()['activity']['party']
        self.assertEqual((p['count'],p['damage'],p['week_lucky']),(2,1234,20))
        before=self.b.profile()
        with patch('network_redirect.backend.time.time',return_value=NOW-86400):
            self.assertEqual(self.req(1026,fight_type=6)[0][0],55)
        self.assertEqual(before,self.b.profile())

    def test_week_boundaries_and_unparticipated(self):
        day=activity.day(NOW,self.b.activity_rules)
        self.assertEqual(party.week(day),party.week(day+1));self.assertEqual(party.week(day)+1,party.week(day+2))
        with patch('network_redirect.backend.time.time',return_value=NOW+2*86400):
            self.ok(self.req(1049,query_type=3));self.assertEqual(self.req(1201,flag=1)[0][0],55)
            self.assertFalse(self.b.profile()['activity']['party']['pending'])

    def test_wave_replenishes_and_rank_achievements(self):
        r=self.b.profile();p=r['activity']['party'];p.update(count=1,damage=10**12,lucky=10000,week_lucky=10000)
        day=p['day'];rows=party.daily_board(r,day,86400,self.b.activity_rules)
        # Deterministic selection can pick the human, not only NPCs.
        with patch.object(party,'stable',side_effect=lambda *args: 0):
            party.finish_day(r,self.b.activity_rules,NOW)
        party.prepare(r,NOW+2*86400,self.b.activity_rules)
        totals=achievements.state(r)['totals']
        for ident in (218,219,220,221,320):self.assertEqual(totals[str(ident)],1)
        self.assertGreater(party.info(r,self.b.activity_rules)['cur_hp'],0)

    def test_query_on_backwards_clock_cannot_restore_chances(self):
        self.fight();self.ok(self.req(1202,flag=1))
        before=self.b.profile()['activity']['party']
        with patch('network_redirect.backend.time.time',return_value=NOW-86400):
            self.ok(self.req(1049,query_type=1))
            self.assertEqual(self.req(1202,flag=1)[0][0],55)
        after=self.b.profile()['activity']
        self.assertEqual(after['party_count'],before['free'])
        self.assertEqual(after['party_bonus'],before['bonus'])
        self.fight();self.assertEqual(self.b.profile()['activity']['party_count'],2)

    def test_materials_tasks_and_entry_usage(self):
        data=self.fight()
        self.assertGreater(len(data['fight_prize']),1)
        status=dict(self.req(1205,flag=1))[48]
        self.assertEqual((status['party_free_count'],status['party_pay_count']),(1,0))
        for _ in range(9):self.fight()
        r=self.b.profile()
        self.assertEqual(r['welfare']['task_progress'][str(activity.day(NOW,self.b.activity_rules))]['2'],10)

    def test_unclaimed_week_survives_another_empty_week(self):
        self.fight()
        for days in (2,9):
            with patch('network_redirect.backend.time.time',return_value=NOW+days*86400):
                h=dict(self.req(1049,query_type=3))[28]
                self.assertGreater(h['self_order'],0)
                self.assertEqual(self.b.profile()['party_take_prize'],0)
        with patch('network_redirect.backend.time.time',return_value=NOW+9*86400):self.ok(self.req(1201,flag=1))
