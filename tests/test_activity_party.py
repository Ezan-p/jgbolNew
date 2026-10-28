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
        peaches=0
        for _ in range(10):
            data=self.fight()
            peaches+=min(100,data['cur_damage']//10000)
            self.assertGreater(data['cur_damage'],0)
            self.assertTrue(data['damage_list'])
            self.assertLessEqual(data['cur_damage'],party.rules()['boss_hp'])
        before=self.b.profile()
        self.assertEqual(self.req(1026,fight_type=6)[0][0],55)
        self.assertEqual(before,self.b.profile())
        for _ in range(5):peaches+=min(100,self.fight(1)['cur_damage']//10000)
        before=self.b.profile();self.assertEqual(before['gold_coin'],initial-100)
        self.assertEqual(before['activity']['party']['week_lucky'],0)
        self.assertEqual(before['activity']['party']['peaches'],peaches)
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

    def test_lucky_disabled_including_legacy_pending_and_restart(self):
        self.fight()
        r=self.b.profile();p=r['activity']['party']
        p.update(pending=[[5,1001,1000,1]],week_lucky=100,week_history={'self_order':1})
        self.b.save(r)
        for days in (0,2,50):
            with patch('network_redirect.backend.time.time',return_value=NOW+days*86400):
                for mid,args in ((1049,dict(query_type=3)),(1201,dict(flag=1))):
                    out=self.req(mid,**args)
                    self.assertEqual(out[0][0],55)
                    self.assertIn('离线模式，暂不开启',str(out))
                self.ok(self.req(1049,query_type=1))
                saved=self.b.profile()
                self.assertFalse(saved['activity']['party']['pending'])
                self.assertEqual(saved['party_take_prize'],1)
                self.assertEqual(saved['party_order'],0)
                self.assertEqual(saved['activity']['party']['week_lucky'],0)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.b.profile()['activity']['party'],saved['activity']['party'])

    def test_damage_reward_boundaries_and_inventory(self):
        for damage,expected in ((0,0),(9999,0),(10000,1),(19999,1),(349380,34),(999999,99),(1000000,100),(10**9,100)):
            r=copy.deepcopy(self.b.profile())
            gain=party.fight_rewards(r,damage,self.b.activity_rules)
            self.assertEqual(sum(x['attach_count'] for x in gain if x['attach_type']==1001),expected)
            before=sum(x['count'] for x in self.b.profile()['attachments'] if x['type_id']==1001)
            after=sum(x['count'] for x in r['attachments'] if x['type_id']==1001)
            self.assertEqual(after-before,expected)

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
        self.assertEqual((p['count'],p['damage'],p['week_lucky']),(2,1234,0))
        before=self.b.profile()
        with patch('network_redirect.backend.time.time',return_value=NOW-86400):
            self.assertEqual(self.req(1026,fight_type=6)[0][0],55)
        self.assertEqual(before,self.b.profile())

    def test_daily_npcs_are_static_scores_and_never_reduce_hp(self):
        r=self.b.profile();day=r['activity']['party']['day']
        board=party.daily_board(r,day,0,self.b.activity_rules)
        self.assertEqual(len(board),20)
        self.assertTrue(all(x['name'] and x['damage']>0 for x in board))
        for second in (39600,43200,46799,86400):
            self.assertEqual(board,party.daily_board(r,day,second,self.b.activity_rules))
            r['activity']['party']['clock']=(day*86400-self.b.activity_rules['timezone_offset_hours']*3600)+second
            info=party.info(r,self.b.activity_rules)
            self.assertEqual(info['cur_hp'],party.rules()['boss_hp'])
            self.assertEqual(info['total_damage'],0)
        self.assertNotEqual(board,party.daily_board(r,day+1,0,self.b.activity_rules))
        self.fight();r=self.b.profile();info=party.info(r,self.b.activity_rules)
        self.assertEqual(len(info['damage_list']),21)
        self.assertEqual(info['total_damage'],r['activity']['party']['damage'])
        self.assertEqual(info['cur_hp'],party.rules()['boss_hp']-info['total_damage']%party.rules()['boss_hp'])

    def test_wave_replenishes_and_rank_achievements(self):
        r=self.b.profile();p=r['activity']['party'];p.update(count=1,damage=10**12,lucky=10000,week_lucky=10000)
        day=p['day'];rows=party.daily_board(r,day,86400,self.b.activity_rules)
        # Deterministic selection can pick the human, not only NPCs.
        with patch.object(party,'stable',side_effect=lambda *args: 0):
            party.finish_day(r,self.b.activity_rules,NOW)
        party.prepare(r,NOW+2*86400,self.b.activity_rules)
        totals=achievements.state(r)['totals']
        for ident in (218,219,320):self.assertEqual(totals[str(ident)],1)
        for ident in (220,221):self.assertEqual(totals.get(str(ident),0),0)
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

    def test_original_hours_boundaries_and_close_settlement(self):
        self.assertEqual(self.b.activity_rules['party_period'],[39600,46800])
        r=self.b.profile();r['activity']['party']['clock']=NOW-3601;self.b.save(r)
        for timestamp,allowed in ((NOW-3601,False),(NOW-3600,True),(NOW+3599,True),(NOW+3600,False)):
            with patch('network_redirect.backend.time.time',return_value=timestamp):
                result=self.req(1026,fight_type=6)
                if allowed:self.ok(result)
                else:self.assertEqual(result[0][0],55)
        with patch('network_redirect.backend.time.time',return_value=NOW+3600):
            h=dict(self.req(1049,query_type=2))[30]
            self.assertEqual(h['fight_count'],2)
            self.assertTrue(self.b.profile()['activity']['party']['closed'])
            self.assertEqual(self.req(1202,flag=1)[0][0],55)

    def test_boss_daily_stability_restart_and_actual_lineup(self):
        r=self.b.profile();p=r['activity']['party'];p['count']=1
        seen={};start=p['day']
        for offset in range(30):
            p['day']=start+offset
            expected=None
            for wave in range(5):
                p['damage']=wave*party.rules()['boss_hp']+123
                info=party.info(r,self.b.activity_rules)
                pair=(info['boss_type'],info['name'])
                if expected is None:expected=pair
                self.assertEqual(pair,expected)
                seen.setdefault(info['boss_type'],copy.deepcopy(r))
        self.assertEqual(set(seen),{4020,5025,3015})
        for tid,r in seen.items():
            timestamp=NOW+(r['activity']['party']['day']-start)*86400
            with patch('network_redirect.backend.time.time',return_value=timestamp):
                self.b.save(r)
                expected=party.info(self.b.profile(),self.b.activity_rules)
                self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
                actual=dict(self.req(1049,query_type=1))[29]
                self.assertEqual((actual['boss_type'],actual['name']),(tid,expected['name']))
                self.fight()
                lineup=next(d for m,_,d in self.decoded if m==1028)
                self.assertEqual(lineup['des_name'],expected['name'])
                self.assertEqual([x['des_type'] for x in lineup['lineup'] if x['des_type']],[tid])
