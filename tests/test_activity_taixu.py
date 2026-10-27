"""Native packet tests for Taixu progression, NPC tournament and atomic rewards."""
import copy
import unittest
from pathlib import Path
from unittest.mock import patch
from test_activity import ActivityCase, NOW
from network_redirect import activity_undergo as u, activity_arena as arena, npc_players, summon
from network_redirect.backend import Backend
from network_redirect.protocol import decode


class TaixuCase(ActivityCase):
    def call(self, op, data=None, mid=1349):
        return self.req(mid, id=op, data=summon.lua(data or {}))

    def save_undergo(self, **kwargs):
        role = self.b.profile(); u.state(role, NOW, self.b.activity_rules).update(kwargs); self.b.save(role)

    def fight(self, mode=1, gid=101, positions=None):
        if positions is None:
            positions = {self.b.profile()['corteges'][0]['id']:9}
        return self.call(4, dict(mode=mode, map_id=gid, cortege_list=positions))

    def arena_enter(self):
        self.ok(self.call(1, mid=1350)); self.ok(self.call(2, mid=1350))
        return self.b.profile()['activity']['arena']

    def arena_fight(self, **overrides):
        role = self.b.profile(); s = role['activity']['arena']; order = arena.ranking(s)
        # Lowest available opponent within native rank window.
        own = order.index('self')+1
        key = next(k for k in reversed(order[:((own+4)//5)*5]) if k != 'self' and s['competitors'][k]['hp'] > 0)
        req = dict(fight_type=arena.rank_type(s), des_type=1,
                   des_id=npc_players.catalog()[key]['profile']['role_id'], des_order=order.index(key)+1,
                   is_charge=0, bet_fight=0, self_order=own)
        req.update(overrides)
        return self.call(5, req, mid=1350)


class UndergoCompleteTests(TaixuCase):
    def test_long_nine_grid_result_uses_preload_without_losing_actions(self):
        from network_redirect import combat_engine, battle_replay
        actions = combat_engine.Actions()
        actions.extend(dict(self_use=False,skill_type=1,is_src=True,result=0,src_order=9,
                            des_order=1,cur_round=i//10+1,damage_count=9,damage_list=[0]*9)
                       for i in range(300))
        with patch('network_redirect.activity_undergo.journey.battle',return_value=(0,[],actions)):
            self.ok(self.fight())
        notice = next(data for mid,_,data in self.decoded if mid==1140)
        self.assertEqual(notice['guide_stage'],battle_replay.RESULT_MARKER)
        self.assertEqual(notice['final_result'],0)
        from tests.test_battle_replay import decoded_packets
        from network_redirect.backend import login_fields
        restored = decoded_packets(self.replies)
        payloads = [login_fields(data['data']) for mid,_,data in restored if mid==2998 and data['id']==121]
        result = next(data['offline_battle_result'] for data in payloads if 'offline_battle_result' in data)
        self.assertEqual(result['fight_round'],300)
        self.assertEqual(len(result['fight_result']),300)

    @patch('network_redirect.activity_undergo.journey.battle', return_value=(1, [], []))
    def test_mode_rewards_costs_first_and_daily_prize(self, _):
        self.ok(self.call(1)); role = self.b.profile(); before = role['strength']; silver = role['silver_coin']
        self.ok(self.fight())
        role = self.b.profile(); self.assertEqual(role['strength'], before-2)
        self.assertEqual(role['silver_coin']-silver, int(u.GATES[101]['money']))
        self.assertNotIn(1, u.day_prize(role['activity']['undergo']))
        self.save_undergo(passed=list(range(101, 110)), gate=201, challenge=109)
        before = self.b.profile(); self.ok(self.fight(2, 109))
        after = self.b.profile(); s = after['activity']['undergo']
        self.assertEqual(after['strength'], before['strength']); self.assertEqual(s['challenge'], 201)
        self.assertEqual(s['first_claimed'], [109]); self.assertEqual(s['used'][str(int(before['corteges'][0]['id']))], 1)
        end = next(d for m,_,d in self.decoded if m==2998 and d['id']==44)
        from network_redirect.backend import login_fields
        self.assertEqual(login_fields(end['data'])['first_win_prize'][1]['attach_count'], 8000)
        self.save_undergo(challenge=109, challenge_passed=list(range(101, 110)))
        self.ok(self.fight(2, 109)); end = next(d for m,_,d in self.decoded if m==2998 and d['id']==44)
        self.assertEqual(login_fields(end['data'])['first_win_prize'], {})
        self.ok(self.call(7, dict(index=1))); before=self.b.profile()
        self.assertEqual(self.call(7, dict(index=1))[0][0], 55); self.assertEqual(self.b.profile(), before)

    @patch('network_redirect.activity_undergo.journey.battle', return_value=(1, [], []))
    def test_big_map_interlock_and_full_map_required(self, _):
        self.save_undergo(gate=201, passed=list(range(101, 110)))
        self.assertEqual(self.fight(1, 201)[0][0], 55)
        self.save_undergo(passed=[101], gate=102)
        self.assertEqual(self.fight(2, 101)[0][0], 55)
        self.save_undergo(passed=list(range(101, 110)), gate=201, challenge=109)
        self.ok(self.fight(2, 109)); self.ok(self.fight(1, 201))

    def test_midnight_only_resets_current_map_and_fatigue(self):
        self.save_undergo(gate=401, challenge=305, used={'1': 4}, count=10, started=NOW-1000,
                          challenge_passed=list(range(101,110)), purchases={'1': 20}, claims=[1])
        with patch('network_redirect.backend.time.time', return_value=NOW+86400):
            self.ok(self.call(1))
        s=self.b.profile()['activity']['undergo']
        self.assertEqual((s['gate'],s['challenge'],s['started']), (401,301,NOW-1000))
        self.assertEqual(s['used'], {}); self.assertEqual(s['count'],0);self.assertEqual(s['claims'],[])
        self.assertIn(1,u.day_prize(s))

    def test_timeout_rollback_clock_and_restart(self):
        self.save_undergo(challenge=305, gate=401, started=NOW-259200, top_big_id=4)
        self.ok(self.call(1)); s=self.b.profile()['activity']['undergo']
        self.assertEqual((s['challenge'],s['gate'],s['top_big_id']), (201,401,4))
        before=self.b.profile()
        self.b.close(); self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.b.profile(),before)
        with patch('network_redirect.backend.time.time', return_value=NOW-1):
            self.assertEqual(self.call(1)[0][0],55)
        self.assertEqual(self.b.profile(),before)

    @patch('network_redirect.activity_undergo.journey.battle', return_value=(4, [], []))
    def test_defeat_uses_fatigue_without_progress(self, _):
        self.save_undergo(gate=201, passed=list(range(101,110)))
        for _ in range(4): self.ok(self.fight(2))
        before=self.b.profile(); self.assertEqual(self.fight(2)[0][0],55);self.assertEqual(self.b.profile(),before)
        self.assertEqual(before['activity']['undergo']['challenge'],101)
        self.assertEqual(before['activity']['undergo']['challenge_passed'],[])

    def test_bad_positions_and_ids_are_atomic(self):
        self.ok(self.call(1));before=self.b.profile();cid=before['corteges'][0]['id']
        for positions in ({cid:0},{cid:10},{cid:1,999999:1},{999999:1},{cid:True},{cid:{'id':cid}}):
            self.assertEqual(self.fight(positions=positions)[0][0],55)
            self.assertEqual(self.b.profile(),before)

    @patch('network_redirect.activity_undergo.journey.battle', return_value=(1, [], []))
    def test_final_gate_has_completion_sentinel(self, _):
        self.save_undergo(gate=909, challenge=901, passed=[g for g in u.GATES if g<909])
        self.ok(self.fight(1,909));self.assertEqual(self.b.profile()['activity']['undergo']['gate'],u.END)
        self.save_undergo(challenge=909, challenge_passed=[g for g in u.GATES if g<909])
        self.ok(self.fight(2,909));s=self.b.profile()['activity']['undergo']
        self.assertEqual(s['challenge'],u.END);self.assertEqual(len(u.day_prize(s)),9)
        self.assertEqual(self.fight(2,909)[0][0],55)
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):self.ok(self.call(1))
        self.assertEqual(self.b.profile()['activity']['undergo']['challenge'],u.END)

    def test_shop_bounds_rollover_and_insufficient_balance(self):
        self.ok(self.call(1)); before=self.b.profile()
        self.assertEqual(self.call(5,dict(index=1,count=1))[0][0],55);self.assertEqual(before,self.b.profile())
        role=self.b.profile();summon.add_item(role,1366,100000);self.b.save(role)
        self.ok(self.call(5,dict(index=1,count=20)))
        self.assertEqual(self.call(5,dict(index=1,count=1))[0][0],55)
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):self.ok(self.call(5,dict(index=1,count=1)))

    def test_legacy_rewards_are_not_reissued(self):
        role=self.b.profile();role['activity']['undergo']=dict(gate=201,challenge=101,lineup={},passed=list(range(101,110)),day=-1)
        self.b.save(role);self.ok(self.call(1));s=self.b.profile()['activity']['undergo']
        self.assertIn(109,s['first_claimed']);self.assertIn(1,u.day_prize(s));self.ok(self.call(7,dict(index=1)))

    def test_all_original_guardians_and_training_load(self):
        self.assertEqual(len(u.GATES),81)
        units=[unit for gid in u.GATES for unit in u.enemy_units(gid)]
        self.assertTrue(any(any(v!=(0,0) for v in unit['training_bonuses']) for unit in units))
        self.assertTrue(all(1<=unit['order']<=9 and unit['hp']>0 for unit in units))

    def test_real_nine_position_battle_and_packet_replay(self):
        self.ok(self.fight());before=self.b.profile();replies=self.replies
        self.assertEqual(self.b.respond(self.packet,self.state),replies);self.assertEqual(before,self.b.profile())
        replay=next(d for m,_,d in self.decoded if m==1140)
        self.assertTrue(replay['fight_result']);self.assertTrue(all(len(x['damage_list'])==9 for x in replay['fight_result']))

    def test_encoding_failure_rolls_back(self):
        self.ok(self.call(1));before=self.b.profile()
        with patch('network_redirect.activity_undergo.encode',side_effect=ValueError('bad replay')):
            self.assertEqual(self.fight()[0][0],55)
        self.assertEqual(self.b.profile(),before)


class ArenaTests(TaixuCase):
    @patch('network_redirect.activity_arena.journey.battle',return_value=(0,[],[]))
    def test_draw_in_final_stage_awards_no_score_or_life_damage(self,_):
        self.arena_enter();role=self.b.profile();s=role['activity']['arena']
        s.update(stage=5,stage_fights=0);self.b.save(role)
        before=copy.deepcopy(s['competitors']);self.ok(self.arena_fight())
        after=self.b.profile()['activity']['arena']
        self.assertEqual(after['competitors'],before)
        self.assertEqual(after['records'][-1]['final_result'],0)
        self.assertEqual(after['stage_fights'],1)

    def test_original_level_50_gate_and_existing_low_level_save(self):
        # Previously created low-level seasons survive the restored entry gate.
        role=self.b.profile();role['level']=50
        role['activity']['arena']=arena.new_season(role,self.b.activity_rules.get('day',0),NOW)
        role['activity']['arena'].update(version=1,group=1,viewing=1)
        role['level']=12
        self.b.save(role)
        for level in (12,49):
            role=self.b.profile();role['level']=level;self.b.save(role);before=self.b.profile()
            for mid in (1349,1350):
                self.assertEqual(self.call(1,mid=mid)[0][0],55)
                self.assertEqual(before,self.b.profile())
        role=self.b.profile();role['level']=50;self.b.save(role)
        self.ok(self.call(1));self.ok(self.call(1,mid=1350))
        self.assertEqual(self.b.profile()['activity']['arena']['group'],4)

    def test_four_groups_preserve_existing_season_and_reject_removed_groups(self):
        self.arena_enter();self.ok(self.arena_fight())
        role=self.b.profile();s=role['activity']['arena']
        s.update(version=1,viewing=2);self.b.save(role)
        before=copy.deepcopy(s)
        events=self.call(1,mid=1350);self.ok(events)
        entry=next(d for e,d in events if e==199)
        self.assertEqual(set(entry['group_type_level']),{4,5,6,7})
        self.assertEqual([(g['min_level'],g['max_level']) for g in entry['group_type_level'].values()],
                         [(50,59),(60,69),(70,79),(80,99)])
        after=self.b.profile()['activity']['arena']
        expected=dict(before,version=2,viewing=before['group'])
        self.assertEqual(after,expected)
        for group in (1,2,3,8):
            with self.subTest(group=group):
                saved=self.b.profile()
                self.assertEqual(self.call(2,dict(enter_group=group),mid=1350)[0][0],55)
                self.assertEqual(self.b.profile(),saved)

    def test_advance_button_eligibility(self):
        self.arena_enter();role=self.b.profile();s=role['activity']['arena']
        self.assertFalse(arena.board(role,s)['local_arena']['can_advance'])
        s['stage_fights']=1
        self.assertTrue(arena.board(role,s)['local_arena']['can_advance'])
        s['stage_fights']=0;s['competitors']['self']['hp']=0
        self.assertTrue(arena.board(role,s)['local_arena']['can_advance'])
        s['settled']=True
        self.assertFalse(arena.board(role,s)['local_arena']['can_advance'])
        s['settled']=False;s['viewing']=4
        self.assertFalse(arena.board(role,s)['local_arena']['can_advance'])

    def test_rank_preview_matches_gold_and_holy_peaches_for_every_tier(self):
        self.arena_enter()
        for expected in arena.rules()['arena_rank_prizes']:
            role=self.b.profile();s=role['activity']['arena'];s['stage']=5
            keys=[k for k in s['competitors'] if k!='self']
            keys.insert(expected['front']-1,'self')
            for i,key in enumerate(keys):s['competitors'][key].update(hp=1000-i,score=0)
            before=copy.deepcopy(role)
            gain=arena.settle_prizes(role,s)
            preview=next(p for p in arena.prize_info() if p['front']==expected['front'])
            self.assertEqual(gain,preview['prize_list'])
            self.assertEqual(role['gold_coin']-before['gold_coin'],expected['gold'])
            def count(r,tid):return sum(x['count'] for x in r['attachments'] if x['type_id']==tid and x['attach_type']==5)
            self.assertEqual(count(role,1343)-count(before,1343),expected['holy_peach'])
            for tid in (1001,1029,1366):self.assertEqual(count(role,tid),count(before,tid))

    @patch('network_redirect.activity_arena.journey.battle',return_value=(1,[],[]))
    def test_first_defeat_still_grants_only_twenty_crystals_once(self,_):
        self.arena_enter();role=self.b.profile();s=role['activity']['arena']
        key=arena.ranking(s)[-2];target=npc_players.catalog()[key]['profile']['role_id']
        def count(r):return sum(x['count'] for x in r['attachments'] if x['type_id']==1366 and x['attach_type']==5)
        before=self.b.profile();self.ok(self.arena_fight(des_id=target))
        after=self.b.profile();self.assertEqual(count(after)-count(before),20)
        self.assertEqual(after['gold_coin'],before['gold_coin'])
        s=after['activity']['arena'];order=arena.ranking(s).index(key)+1
        self.ok(self.arena_fight(des_id=target,des_order=order))
        self.assertEqual(count(self.b.profile()),count(after))

    @patch('network_redirect.activity_arena.journey.battle',return_value=(4,[],[]))
    def test_practice_transition_is_one_board_with_future_formal_start(self,_):
        self.arena_enter();self.ok(self.arena_fight())
        events=self.call(7,dict(stage=1),mid=1350);self.ok(events)
        boards=[d for e,d in events if e==199]
        self.assertEqual(len(boards),1);data=boards[0]
        self.assertEqual(data['id'],2);self.assertEqual(data['rank_type'],2)
        schedule=data['local_entry']['schedule_list']['match_time_list']
        self.assertLess(schedule[2]['start_time'],NOW)
        self.assertGreater(schedule[2]['end_time'],NOW)
        self.assertGreater(schedule[3]['start_time'],NOW)
        self.assertEqual(data['event_info']['cur_fight_count'],5)
        for _ in range(5):self.ok(self.arena_fight())
        role=self.b.profile();self.assertEqual(arena.board(role,role['activity']['arena'])['event_info']['cur_fight_count'],0)
        self.assertEqual(self.arena_fight()[0][0],55)

    def test_all_groups_npc_identity_inspection_and_no_cross_group_attack(self):
        s=self.arena_enter();self.assertEqual(len(s['competitors']),20)
        for group in range(4,8):
            self.ok(self.call(2,dict(enter_group=group),mid=1350))
            role=self.b.profile();s=role['activity']['arena'];rows=arena.board(role,s)['rank_data']
            self.assertTrue(all(r['area_name']=='' for r in rows))
            npc=next(r for r in rows if not r['is_me'])
            self.assertIsNotNone(npc_players.resolve(npc['obj_id']))
            out=self.call(4,dict(des_id=npc['obj_id'],des_type=1),mid=1350);self.ok(out)
            self.assertEqual(next(v for e,v in out if e==11)['role_name'],npc['name'])
        before=self.b.profile();self.assertEqual(self.arena_fight()[0][0],55);self.assertEqual(before,self.b.profile())

    def test_real_fight_and_record_is_read_only_after_restart(self):
        self.arena_enter();self.ok(self.arena_fight());before=self.b.profile();s=before['activity']['arena'];rec=s['records'][-1]
        self.assertIn(1027,[m for m,_,_ in self.decoded])
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.ok(self.req(1244,fight_type=4,log_time=rec['log_time'],src_id=rec['src_id'],match_type=rec['match_type']))
        self.assertEqual(self.b.profile(),before)
        self.assertEqual(self.req(1244,fight_type=4,log_time=1,src_id=rec['src_id'],match_type=1)[0][0],55)

    def test_effect_battles_persist_and_replay_in_every_stage(self):
        from network_redirect import combat_engine
        effects = combat_engine.Actions()
        effects.events = [dict(cur_action=1, logic_type=101051, who_use=1, self_use=True,
                              src_order=1, des_order=1, speak='',
                              skill_result_list=[dict(field=65, field_plus=10, des_order=1)])]
        self.arena_enter()
        with patch('network_redirect.activity_arena.journey.battle', return_value=(1, [], effects)):
            for stage in range(1, 6):
                with self.subTest(stage=stage):
                    events = self.arena_fight(); self.ok(events)
                    original = next(d for e,d in events if e == 121)
                    self.assertIn(1, original)
                    saved = self.b.profile()
                    s = saved['activity']['arena']; rec = s['records'][-1]
                    self.assertEqual(s['replays'][str(rec['fight_id'])]['fight_events']['1'], effects.events[0])
                    self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
                    replay = self.req(1244, fight_type=4, log_time=rec['log_time'],
                                      src_id=rec['src_id'], match_type=rec['match_type'])
                    self.ok(replay)
                    self.assertEqual(next(d for e,d in replay if e == 121), original)
                    self.assertEqual(self.b.profile(), saved)
                    self.ok(self.call(7, dict(stage=stage), mid=1350))

    @patch('network_redirect.activity_arena.journey.battle',return_value=(1,[],[]))
    def test_complete_tournament_settles_once_then_next_day(self,_):
        self.arena_enter()
        for stage in range(1,6):
            self.ok(self.arena_fight());events=self.call(7,dict(stage=stage),mid=1350);self.ok(events)
            board=next(d for e,d in events if e==199)
            if stage<5:
                self.assertNotIn('local_prizes',board)
            else:
                self.assertEqual(board['local_prizes'],next(d for e,d in events if e==33))
                self.assertEqual(len(board['local_prizes']),2)
        role=self.b.profile();s=role['activity']['arena'];self.assertTrue(s['settled'])
        self.assertGreater(len(s['settlement']['attach_list']),0)
        before=self.b.profile();self.assertEqual(self.call(7,dict(stage=5),mid=1350)[0][0],55)
        self.assertEqual(before,self.b.profile());self.ok(self.call(1,mid=1350));self.assertEqual(s['day'],self.b.profile()['activity']['arena']['day'])
        events=self.call(2,mid=1350);self.ok(events)
        self.assertNotIn('local_prizes',next(d for e,d in events if e==199))
        self.assertFalse(any(e==33 for e,d in events))
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):self.ok(self.call(1,mid=1350))
        new=self.b.profile()['activity']['arena'];self.assertEqual(new['stage'],1);self.assertFalse(new['settled'])

    @patch('network_redirect.activity_arena.journey.battle',return_value=(4,[],[]))
    def test_stage_loss_and_practice_do_not_invent_victory(self,_):
        self.arena_enter();self.ok(self.arena_fight());self.ok(self.call(7,dict(stage=1),mid=1350))
        role=self.b.profile();before=copy.deepcopy(role['activity']['arena']['competitors'])
        self.ok(self.arena_fight());self.assertEqual(self.b.profile()['activity']['arena']['competitors'],before)
        self.ok(self.call(7,dict(stage=2),mid=1350))
        for stage in (3,4,5):
            hp=self.b.profile()['activity']['arena']['competitors']['self']['hp']
            self.ok(self.arena_fight())
            self.assertEqual(self.b.profile()['activity']['arena']['competitors']['self']['hp'],hp-(20 if stage==5 else 0))
            if stage<5:self.ok(self.call(7,dict(stage=stage),mid=1350))

    @patch('network_redirect.activity_arena.journey.battle',return_value=(4,[],[]))
    def test_paid_limit_and_no_charge_when_free(self,_):
        self.arena_enter();gold=self.b.profile()['gold_coin'];self.ok(self.arena_fight(is_charge=1))
        self.assertEqual(self.b.profile()['gold_coin'],gold)
        for _ in range(9):self.ok(self.arena_fight())
        before=self.b.profile();self.assertEqual(self.arena_fight()[0][0],55);self.assertEqual(before,self.b.profile())
        for _ in range(5):self.ok(self.arena_fight(is_charge=1))
        self.assertEqual(self.b.profile()['gold_coin'],gold-100)
        before=self.b.profile();self.assertEqual(self.arena_fight(is_charge=1)[0][0],55);self.assertEqual(before,self.b.profile())
        self.assertEqual(len(before['activity']['arena']['records']),10)

    def test_forged_stage_target_result_and_clock(self):
        self.arena_enter();before=self.b.profile()
        for data in (dict(stage=2),dict(stage=1)):
            self.assertEqual(self.call(7,data,mid=1350)[0][0],55);self.assertEqual(before,self.b.profile())
        for data in (dict(des_id=999),dict(des_order=100),dict(fight_type=3),dict(bet_fight=1)):
            self.assertEqual(self.arena_fight(**data)[0][0],55);self.assertEqual(before,self.b.profile())
        with patch('network_redirect.backend.time.time',return_value=NOW-1):self.assertEqual(self.call(1,mid=1350)[0][0],55)
        self.assertEqual(before,self.b.profile())

    def test_encode_failure_and_request_replay(self):
        self.arena_enter();before=self.b.profile()
        with patch('network_redirect.activity_arena.encode',side_effect=ValueError('bad packet')):
            self.assertEqual(self.arena_fight()[0][0],55)
        self.assertEqual(before,self.b.profile())
        self.ok(self.arena_fight());before=self.b.profile();replies=self.replies
        self.assertEqual(self.b.respond(self.packet,self.state),replies);self.assertEqual(before,self.b.profile())

    def test_unfinished_season_persists_across_midnight(self):
        s=self.arena_enter();roster=copy.deepcopy(s['competitors'])
        with patch('network_redirect.backend.time.time',return_value=NOW+86400*10):self.ok(self.call(1,mid=1350))
        after=self.b.profile()['activity']['arena'];self.assertEqual(after['competitors'],roster);self.assertEqual(after['day'],s['day'])

if __name__=='__main__':unittest.main()
