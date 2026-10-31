"""Original wire end-to-end rank flow against an isolated SQLite save."""
import copy
import random
from pathlib import Path
from unittest.mock import patch
from test_activity import ActivityCase, NOW
from network_redirect import activity, activity_rank as rank, summon, formation
from network_redirect.backend import Backend
from network_redirect.protocol import decode, encode


class RankTests(ActivityCase):
    def test_rank_44_skill_effects_settle_persist_and_replay_once(self):
        role = self.b.profile()
        role['activity'].update(rank_order=45, rank_origin_order=100, rank_slots={})
        # A matching NPC roster survives long enough to exercise real effects.
        npc = rank.catalog()[930044]['role']
        for key in ('corteges', 'attachments'):
            role[key] = copy.deepcopy(npc[key])
        self.b.save(role)
        before = self.b.profile()
        with patch('network_redirect.combat.secrets.randbelow', side_effect=random.Random(17).randrange):
            _, events = self.fight(44)
        after = self.b.profile()
        record = after['activity']['rank_records'][-1]
        self.assertTrue(any(str(k).isdigit() for k in record['fight_events']))
        self.assertEqual(after['energy'], before['energy'] - 1)
        self.assertEqual(after['activity']['rank_count'], before['activity']['rank_count'] + 1)
        self.assertIn(44, [event for event, _ in events])
        self.assertEqual(self.b.respond(self.packet, self.state), self.replies)
        self.assertEqual(self.b.profile(), after)
        self.b.close()
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.assertEqual(self.b.profile(), after)
        self.ok(self.req(1244, fight_type=2))
        self.assertEqual(self.b.profile(), after)

    def test_daily_points_for_challenges_caps_failures_replay_and_next_day(self):
        def points(): return self.b.profile().get('daily', {}).get('points', {}).get('10', 0)
        self.board(); self.assertEqual(points(), 0)
        self.req(1026, fight_type=2, des_type=2, des_id=0, des_value=99)
        self.assertEqual(points(), 0)
        self.fight(99); self.assertEqual(points(), 10)
        before = self.b.profile()
        self.assertEqual(self.b.respond(self.packet, self.state), self.replies)
        self.assertEqual(self.b.profile(), before)
        # A valid losing challenge counts just like a win.
        role = self.b.profile(); role['activity']['rank_order'] = 2
        role['activity']['rank_slots'] = {}; self.b.save(role)
        fight, _ = self.fight(1)
        self.assertGreaterEqual(fight['final_result'], 4)
        self.assertEqual(points(), 20)
        self.fight(1); self.assertEqual(points(), 20)
        self.req(1244, fight_type=2); self.assertEqual(points(), 20)
        role = self.b.profile(); role['energy'] = 0; self.b.save(role)
        self.req(1026, fight_type=2, des_type=2, des_id=930001, des_value=1)
        self.assertEqual(points(), 20)
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        with patch('network_redirect.backend.time.time', return_value=NOW+86400):
            role = self.b.profile(); role['energy'] = 100; self.b.save(role)
            # No board query before this first new-day settlement.
            self.ok(self.req(1026, fight_type=2, des_type=2, des_id=930001, des_value=1))
            self.assertEqual(points(), 10)
            self.assertEqual(self.b.profile()['daily']['total'], 10)

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
        for ident in (930001,930002,930003,930004,930005,930050,930099):
            out=self.req(1039,des_type=2,des_id=ident);self.ok(out)
            data=next(d for e,d in out if e==11);npc=rank.catalog()[ident]['role']
            chars=list(data['cortege_list'].values());expected=[c for c in npc['corteges'] if c['order']]
            self.assertEqual(len(chars),len(expected))
            self.assertEqual(sum(c['wuligongji_show'] for c in chars),sum(c['gongji'] for c in expected))
            self.assertTrue(data['equip_list']);self.assertTrue(data['skill_list'])
            self.assertTrue(all(len(p)<=32768 for p in self.replies))

    def test_elites_stronger_with_remaining_ladder_and_sources_unchanged(self):
        from network_redirect import npc_players
        from analysis.tools import build_npc_catalog as design
        current = rank.catalog()
        original_rules = copy.deepcopy(rank.rules())
        original_rules.pop('elite_npcs')
        with patch.object(rank, 'rules', return_value=original_rules):
            original = rank.catalog.__wrapped__()
        self.assertEqual({k:v for k,v in current.items() if k > 930005},
                         {k:v for k,v in original.items() if k > 930005})
        for ident in range(930001,930006):
            npc = current[ident]
            self.assertGreater(npc['role']['role_combat_power'], original[ident]['role']['role_combat_power'])
            design.validate(copy.deepcopy(npc))
        source = npc_players.get('npc_v1_l99_t1_attack')['role']
        self.assertEqual({c['evolve_level'] for c in source['corteges'] if c['order']}, {49})
        self.assertEqual({c['evolve_level'] for c in current[930001]['role']['corteges'] if c['order']}, {99})

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

    def test_token_batch_uses_inventory_preserves_score_and_replays_once(self):
        r=self.b.profile();summon.add_item(r,1021,100);self.b.save(r)
        token=next(i for i in r['attachments'] if i['type_id']==1021)
        before=self.b.profile()
        events=self.req(1051,item_type=1021,item_id=token['id'],item_count=100,des_type=1)
        self.ok(events)
        result=next(d for e,d in events if e==21)
        self.assertEqual(result,dict(result=1,type_id=1021,count=100,effect_value=300))
        self.assertNotIn(1022,[m for m,_,d in self.decoded])
        after=self.b.profile()
        self.assertEqual(after['activity']['rank_score'],before['activity']['rank_score'])
        self.assertEqual(after['activity']['rank_extra'],300)
        self.assertFalse(any(i['id']==token['id'] for i in after['attachments']))
        self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
        self.assertEqual(after,self.b.profile())
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(after,self.b.profile())

    def test_token_invalid_batch_and_unusable_stack_are_atomic(self):
        r=self.b.profile();summon.add_item(r,1021,2);self.b.save(r)
        token=next(i for i in r['attachments'] if i['type_id']==1021)
        for override in (dict(item_count=3),dict(item_count=101),dict(des_type=2),dict(des_id=999999),dict(item_id=999999)):
            before=self.b.profile()
            request=dict(item_type=1021,item_id=token['id'],item_count=1,des_type=1)
            request.update(override)
            self.assertEqual(self.req(1051,**request)[0][0],55)
            self.assertEqual(before,self.b.profile())
        for field in ('is_lock','equip_pos','owner_id'):
            r=self.b.profile();next(i for i in r['attachments'] if i['id']==token['id'])[field]=1
            self.b.save(r);before=self.b.profile()
            self.assertEqual(self.req(1051,item_type=1021,item_id=token['id'],item_count=1,des_type=1)[0][0],55)
            self.assertEqual(before,self.b.profile())
            next(i for i in r['attachments'] if i['id']==token['id'])[field]=0;self.b.save(r)

    def test_daily_score_offline_cap_and_clock_rollback(self):
        self.board();base=self.b.profile()['activity']['rank_score']
        with patch('network_redirect.backend.time.time',return_value=NOW+1799):self.board()
        self.assertEqual(self.b.profile()['activity']['rank_score'],base)
        with patch('network_redirect.backend.time.time',return_value=NOW+1800):self.board();self.board()
        self.assertEqual(self.b.profile()['activity']['rank_score'],base)
        with patch('network_redirect.backend.time.time',return_value=NOW-86400):self.board()
        self.assertEqual(self.b.profile()['activity']['rank_score'],base)
        with patch('network_redirect.backend.time.time',return_value=NOW+40*86400):self.board()
        self.assertEqual(self.b.profile()['activity']['rank_score'],base+7*rank.score(100,'day_score'))

    def test_previous_day_best_claim_and_historical_promotions(self):
        self.fight(99);self.assertEqual(self.req(1201,flag=2)[0][0],55)
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            self.board();r=self.b.profile()
            self.assertEqual(r['activity']['rank_score'],rank.score(99)+rank.score(99,'day_score'))
            self.assertEqual(r['activity']['rank_previous_best'],99)
            self.assertEqual(self.req(1201,flag=2)[0][0],55);self.assertEqual(r,self.b.profile())
            self.ok(self.req(1203,exchange_type=5));self.assertEqual(self.req(1203,exchange_type=5)[0][0],55)
        self.assertEqual(self.req(1203,exchange_type=10)[0][0],55)

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

    def test_draw_keeps_rank_and_no_win_reward(self):
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
        self.ok(self.req(1203,exchange_type=10))

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


    def test_exchange_prices_rewards_and_insufficient_score(self):
        for index,cost,tid,count in ((1,5000,1001,100),):
            r=self.b.profile();r['activity']['rank_score']=cost-1;self.b.save(r)
            before=self.b.profile();self.assertEqual(self.req(1203,exchange_type=index)[0][0],55)
            self.assertEqual(before,self.b.profile())
            r['activity']['rank_score']=cost;self.b.save(r)
            owned=lambda r:sum(v['count'] for v in r['attachments'] if v['type_id']==tid and v['attach_type']==5)
            before=owned(r);self.ok(self.req(1203,exchange_type=index));after=self.b.profile()
            self.assertEqual(owned(after)-before,count);self.assertEqual(after['activity']['rank_score'],0)

    def test_peach_exchange_inventory_failure_replay_and_restart(self):
        owned=lambda r,tid:sum(v['count'] for v in r['attachments'] if v['type_id']==tid and v['attach_type']==5)
        r=self.b.profile();r['activity']['rank_score']=0
        r['attachments']=[v for v in r['attachments'] if v['type_id'] not in (1001,1343)]
        summon.add_item(r,1001,999);self.b.save(r)
        before=self.b.profile()
        self.assertEqual(self.req(1203,exchange_type=3)[0][0],55)
        self.assertEqual(self.b.profile(),before)
        summon.add_item(r,1001,1);self.b.save(r)
        events=self.req(1203,exchange_type=3);self.ok(events);after=self.b.profile()
        self.assertEqual((owned(after,1001),owned(after,1343)),(0,1))
        self.assertEqual(after['activity']['rank_score'],0)
        self.assertEqual(next(d for e,d in events if e==36)[1]['attach_count'],1)
        self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
        self.assertEqual(self.b.profile(),after)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.b.profile(),after)
        self.assertEqual(self.req(1203,exchange_type=3)[0][0],55)
        self.assertEqual(self.b.profile(),after)

    def test_only_two_exchanges_and_removed_offer_rejected(self):
        self.assertEqual([v['index'] for v in rank.rules()['exchanges'] if not v['promote_order']],[1,3])
        r=self.b.profile();r['activity']['rank_score']=1000000;self.b.save(r)
        for index in (2,11,255):
            before=self.b.profile()
            self.assertEqual(self.req(1203,exchange_type=index)[0][0],55)
            self.assertEqual(self.b.profile(),before)

    def test_peach_exchange_cannot_consume_locked_or_equipped_items(self):
        for field in ('is_lock','equip_pos','owner_id'):
            r=self.b.profile();r['attachments']=[v for v in r['attachments'] if v['type_id']!=1001]
            summon.add_item(r,1001,1000)
            next(v for v in r['attachments'] if v['type_id']==1001)[field]=1
            self.b.save(r);before=self.b.profile()
            self.assertEqual(self.req(1203,exchange_type=3)[0][0],55)
            self.assertEqual(self.b.profile(),before)

    def test_seven_promotion_thresholds_gold_and_duplicates(self):
        tiers=[(4,500,50),(5,100,100),(6,50,200),(7,30,300),(8,20,400),(9,10,1000),(10,1,2000)]
        self.assertEqual([v['promote_order'] for v in rank.rules()['exchanges'] if v['promote_order']],[v[1] for v in tiers])
        for index,order,gold in tiers:
            r=self.b.profile();r['activity']['rank_reached_order']=order+1;self.b.save(r)
            self.assertEqual(self.req(1203,exchange_type=index)[0][0],55)
            r['activity']['rank_reached_order']=order;self.b.save(r);before=self.b.profile()
            events=self.req(1203,exchange_type=index);self.ok(events);after=self.b.profile()
            self.assertNotIn(1022,[m for m,_,d in self.decoded])
            self.assertEqual(next(d for e,d in events if e==36)[1],dict(object_type=11,attach_type=1,attach_count=gold,attach_level=1))
            state=next(d['local_rank'] for e,d in events if e==80 and 'local_rank' in d)
            self.assertTrue(state['promote_prize'] & (1 << (index-2)))
            self.assertEqual(after['gold_coin']-before['gold_coin'],gold)
            self.assertEqual(after['attachments'],before['attachments'])
            self.assertEqual(self.req(1203,exchange_type=index)[0][0],55)
            self.assertEqual(after,self.b.profile())

    def test_legacy_claims_migrate_by_threshold_and_pending_paid_once(self):
        r=self.b.profile();s=r['activity'];s.pop('rank_reward_version',None)
        s.update(rank_promotions=[4,5,6,7,8,9],rank_pending_score=4400,rank_score=12345,rank_reached_order=1)
        self.b.save(r);self.board();s=self.b.profile()['activity']
        self.assertEqual(s['rank_promotions'],[4,5,9,10]);self.assertEqual(s['rank_score'],16745)
        self.board();self.assertEqual(self.b.profile()['activity']['rank_score'],16745)
        for index in (4,5,9,10):self.assertEqual(self.req(1203,exchange_type=index)[0][0],55)
        for index in (6,7,8):self.ok(self.req(1203,exchange_type=index))

    def test_midnight_best_rank_daily_cap_restart_and_clock_rollback(self):
        r=self.b.profile();s=r['activity'];s.update(rank_day_best=20,rank_reached_order=20)
        self.b.save(r);midnight=(s['rank_day']+1)*86400-8*3600
        with patch('network_redirect.backend.time.time',return_value=midnight-1):self.board()
        self.assertEqual(self.b.profile()['activity']['rank_score'],0)
        with patch('network_redirect.backend.time.time',return_value=midnight):
            self.board();before=self.b.profile();self.assertEqual(before['activity']['rank_score'],rank.score(20,'day_score'))
            self.board();self.assertEqual(before,self.b.profile())
            self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
            self.board();self.assertEqual(before,self.b.profile())
        with patch('network_redirect.backend.time.time',return_value=midnight-10):self.board()
        self.assertEqual(self.b.profile()['activity']['rank_score'],rank.score(20,'day_score'))
        r=self.b.profile();r['activity']['rank_score']=16777214;self.b.save(r)
        with patch('network_redirect.backend.time.time',return_value=midnight+86400):self.board()
        self.assertEqual(self.b.profile()['activity']['rank_score'],16777215)

    def test_cross_rank_disabled_and_no_mutation(self):
        before=self.b.profile()
        for mid,data in [(1232,{}),(1233,{}),(1231,{}),(1234,{}),(1235,{}),(1236,{}),(1238,{}),(1026,dict(fight_type=18)),(1244,dict(fight_type=3))]:
            result=self.req(mid,**data)
            self.assertEqual(result,[(55,{'op_string':'离线模式，暂未开启'})])
            self.assertEqual(before,self.b.profile())


    def test_heartbeat_credits_at_midnight_without_opening_board(self):
        r=self.b.profile();s=r['activity'];s.update(rank_day_best=30,rank_count=3,rank_extra=6)
        self.b.save(r);midnight=(s['rank_day']+1)*86400-8*3600
        heartbeat=encode(2999,{})
        with patch('network_redirect.backend.time.time',return_value=midnight):
            packets=self.b.respond(heartbeat,self.state);decoded=[decode(p) for p in packets]
            after=self.b.profile();self.assertEqual(after['activity']['rank_score'],rank.score(30,'day_score'))
            self.assertEqual(after['activity']['rank_count'],0);self.assertEqual(after['activity']['rank_extra'],0)
            self.assertNotIn(1022,[m for m,_,d in decoded])
            self.assertTrue(any(a['type']==131 and a['value']==rank.score(30,'day_score') for m,_,d in decoded if m==1032 for a in d['attr_list']))
            self.b.respond(heartbeat,self.state)
            self.assertEqual(self.b.profile()['activity']['rank_score'],after['activity']['rank_score'])
