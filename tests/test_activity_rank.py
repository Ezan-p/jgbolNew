"""Original wire end-to-end rank flow against an isolated SQLite save."""
import copy
from pathlib import Path
from unittest.mock import patch
from test_activity import ActivityCase, NOW
from network_redirect import activity, activity_rank as rank, summon, formation
from network_redirect.backend import Backend
from network_redirect.protocol import decode


class RankTests(ActivityCase):
    def board(self):
        self.ok(self.req(1021,flag=0))
        return next(d for m,_,d in self.decoded if m==1022)

    def fight(self,order=None):
        rows=self.board()['show_list']
        row=next(v for v in rows if v['order']==order) if order else max((v for v in rows if v['top_relation']==2),key=lambda v:v['order'])
        out=self.req(1026,fight_type=2,des_type=2,des_id=row['id'],des_value=row['order'])
        self.ok(out)
        return next(d for m,_,d in self.decoded if m==1027),out

    def test_catalog_fixed_monotonic_and_no_shared_mutation(self):
        rows=list(rank.catalog().values());powers=[v['role']['role_combat_power'] for v in rows]
        self.assertEqual(powers,sorted(powers,reverse=True));self.assertEqual(len({v['npc_id'] for v in rows}),99)
        before=copy.deepcopy(rank.catalog());self.fight();self.assertEqual(rank.catalog(),before)
        ids=[v['id'] for v in self.board()['show_list']]
        r=self.b.profile();r['level']=99;self.b.save(r)
        self.assertEqual(ids,[v['id'] for v in self.board()['show_list']])

    def test_inspection_matches_full_fighting_roster_and_skills(self):
        self.board()
        for ident in (930001,930050,930099):
            out=self.req(1039,des_type=2,des_id=ident);self.ok(out)
            data=next(d for e,d in out if e==11);npc=rank.catalog()[ident]['role']
            chars=list(data['cortege_list'].values());expected=[c for c in npc['corteges'] if c['order']]
            self.assertEqual(len(chars),len(expected))
            self.assertEqual(sum(c['wuligongji_show'] for c in chars),sum(c['gongji'] for c in expected))
            self.assertTrue(data['equip_list']);self.assertTrue(data['skill_list'])
            self.assertTrue(all(len(p)<=32768 for p in self.replies))

    def test_win_rewards_five_cards_one_actual_award(self):
        before=self.b.profile();fight,events=self.fight(99);after=self.b.profile()
        self.assertIn(fight['final_result'],(1,2,3));self.assertEqual(after['activity']['rank_order'],99)
        self.assertEqual(after['energy'],before['energy']-1)
        self.assertEqual(after['activity']['rank_score'],rank.score(99))
        cards=next(d for e,d in events if e==33);self.assertEqual(len(cards),5)
        chosen=[c for c in cards.values() if c['flag']];self.assertEqual(len(chosen),1)
        tid=chosen[0]['attach_type'];count=lambda r:sum(i['count'] for i in r['attachments'] if i['type_id']==tid and i['attach_type']==5)
        self.assertEqual(count(after)-count(before),chosen[0]['attach_count'])
        self.assertEqual(after['silver_coin']-before['silver_coin'],self.b.activity_rules['battle_silver'])
        self.assertEqual(rank.identity(after['activity'],100),930099)

    def test_repeat_packet_and_restart_no_duplicate_rewards(self):
        self.fight();before=self.b.profile()
        self.assertEqual(self.b.respond(self.packet,self.state),self.replies);self.assertEqual(before,self.b.profile())
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(before,self.b.profile());events=self.req(1244,fight_type=2);self.ok(events);self.assertEqual(before,self.b.profile())
        self.assertIn(152,[e for e,d in events]);self.assertNotIn(44,[e for e,d in events])
        meta=next(d['local_rank_records'] for e,d in events if e==80 and 'local_rank_records' in d)
        self.assertEqual(meta[1]['label'],'攻胜·'+rank.catalog()[930099]['role']['role_name'])
        self.assertEqual(meta[1]['power'],rank.catalog()[930099]['role']['role_combat_power'])
        self.assertTrue(any(e==80 and d.get('local_rank_show_records') for e,d in events))

    def test_loss_no_prize_or_promotion(self):
        r=self.b.profile();r['activity']['rank_order']=2;r['activity']['rank_slots']={};self.b.save(r)
        fight,events=self.fight(1)
        self.assertGreaterEqual(fight['final_result'],4);self.assertNotIn(33,[e for e,d in events])
        self.assertEqual(self.b.profile()['activity']['rank_order'],2)
        self.assertEqual(self.b.profile()['activity']['rank_score'],0)

    def test_token_consume_cap_validation_and_rollover(self):
        r=self.b.profile();summon.add_item(r,1021,102);r['activity']['rank_count']=r['top_fight_limit'];self.b.save(r)
        self.assertEqual(self.board()['fight_count'],0)
        self.ok(self.req(1051,item_type=1021,item_count=2,des_type=1))
        self.assertEqual(self.board()['fight_count'],6)
        self.assertTrue(any(a['type']==134 and a['value']==6 for m,_,d in self.decoded if m==1032 for a in d['attr_list']))
        before=self.b.profile();self.assertEqual(self.req(1051,item_type=1021,item_count=100,des_type=1)[0][0],55);self.assertEqual(before,self.b.profile())
        self.assertEqual(self.req(1051,item_type=1021,item_count=1,item_id=999999,des_type=1)[0][0],55)
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            self.assertEqual(self.board()['fight_count'],self.b.profile()['top_fight_limit'])
            self.assertEqual(self.b.profile()['activity']['rank_extra'],0)

    def test_half_hour_offline_cap_and_clock_rollback(self):
        self.board();base=self.b.profile()['activity']['rank_score']
        with patch('network_redirect.backend.time.time',return_value=NOW+1799):self.board()
        self.assertEqual(self.b.profile()['activity']['rank_score'],base)
        with patch('network_redirect.backend.time.time',return_value=NOW+1800):self.board();self.board()
        self.assertEqual(self.b.profile()['activity']['rank_score'],base+rank.score(100))
        with patch('network_redirect.backend.time.time',return_value=NOW-86400):self.board()
        self.assertEqual(self.b.profile()['activity']['rank_score'],base+rank.score(100))
        with patch('network_redirect.backend.time.time',return_value=NOW+40*86400):self.board()
        self.assertEqual(self.b.profile()['activity']['rank_score'],base+337*rank.score(100))

    def test_previous_day_best_claim_and_historical_promotions(self):
        self.fight(99);self.assertEqual(self.req(1201,flag=2)[0][0],55)
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            self.ok(self.req(1201,flag=2));r=self.b.profile()
            self.assertEqual(r['activity']['rank_previous_best'],99)
            self.assertEqual(self.req(1201,flag=2)[0][0],55);self.assertEqual(r,self.b.profile())
            self.ok(self.req(1203,exchange_type=7));self.assertEqual(self.req(1203,exchange_type=7)[0][0],55)
        self.assertEqual(self.req(1203,exchange_type=9)[0][0],55)

    def test_defence_once_daily_and_revenge_uses_same_npc(self):
        self.fight(99)
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            self.board();r=self.b.profile();n=len(r['activity']['rank_records']);self.board()
            self.assertEqual(len(self.b.profile()['activity']['rank_records']),n)
            self.assertEqual(self.b.profile()['energy'],r['energy'])
            self.assertTrue(r['activity']['rank_records'][-1]['defence'])

    def test_defensive_loss_produces_revenge_without_charging(self):
        r=self.b.profile();s=r['activity'];s.update(rank_order=1,rank_origin_order=1,rank_slots={},rank_reached_order=1);self.b.save(r)
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            rows=self.board()['show_list'];after=self.b.profile();state=after['activity']
            self.assertEqual(state['rank_order'],2)
            self.assertEqual(state['rank_revenge'],930002)
            self.assertTrue(any(v['id']==930002 and v['order']==1 and v['top_relation']==3 for v in rows))
            self.assertEqual(state['rank_count'],0)
            self.assertEqual(after['energy'],r['energy'])
            self.assertEqual(after['silver_coin'],r['silver_coin'])
            record=state['rank_records'][-1]
            self.assertTrue(record['defence']);self.assertGreaterEqual(record['fight_result_msg']['final_result'],4)

    def test_unresolved_battle_keeps_rank_and_no_win_reward(self):
        self.board();r=self.b.profile();r['activity'].update(rank_order=1,rank_origin_order=1,rank_slots={},rank_reached_order=1);self.b.save(r)
        with patch('network_redirect.activity_rank.journey.battle',return_value=(0,[],[])):
            fight,events=self.fight(2)
        after=self.b.profile();self.assertEqual(fight['final_result'],0)
        self.assertEqual(after['activity']['rank_order'],1)
        self.assertEqual(after['activity']['rank_score'],r['activity']['rank_score'])
        self.assertEqual(after['silver_coin'],r['silver_coin'])
        self.assertNotIn(33,[e for e,d in events]);self.assertEqual(after['activity']['rank_count'],1)

    def test_invalid_and_exhausted_are_atomic(self):
        self.board();before=self.b.profile()
        for d in [dict(des_type=2,des_value=1,des_id=930001),dict(des_type=1,des_value=99,des_id=930099),dict(des_type=2,des_value=99,des_id=10099)]:
            self.assertEqual(self.req(1026,fight_type=2,**d)[0][0],55);self.assertEqual(before,self.b.profile())
        r=self.b.profile();r['energy']=0;self.b.save(r);before=self.b.profile()
        self.assertEqual(self.req(1026,fight_type=2,des_type=2,des_value=99,des_id=930099)[0][0],55);self.assertEqual(before,self.b.profile())

    def test_top_rank_has_targets_and_loss_swaps_positions(self):
        r=self.b.profile();s=r['activity'];s.update(rank_order=1,rank_origin_order=1,rank_slots={},rank_reached_order=1);self.b.save(r)
        rows=self.board()['show_list'];self.assertEqual(sum(v['top_relation']==2 for v in rows),5)
        fight,_=self.fight(2);self.assertGreaterEqual(fight['final_result'],4)
        s=self.b.profile()['activity'];self.assertEqual(s['rank_order'],2);self.assertEqual(rank.identity(s,1),930002)
        self.ok(self.req(1203,exchange_type=9))

    def test_ladder_permutation_and_migration_preserve_balances(self):
        r=self.b.profile();s=r['activity'];s.update(rank_order=40,rank_score=54321,rank_count=3,rank_promotions=[4,5]);s.pop('rank_version');self.b.save(r)
        self.board();s=self.b.profile()['activity'];self.assertEqual(s['rank_score'],54321);self.assertEqual(s['rank_count'],3)
        for target in (20,1,2,50,99,100,1):
            rank.swap(s,target)
            ids=[rank.identity(s,o) for o in range(1,101) if o!=s['rank_order']]
            self.assertEqual(set(ids),set(rank.catalog()));self.assertEqual(len(ids),len(set(ids)))

    def test_all_inspection_packets_fit_protocol(self):
        r=self.b.profile()
        for ident in rank.catalog(): self.assertLessEqual(len(rank.inspection(r,ident)),32768)
