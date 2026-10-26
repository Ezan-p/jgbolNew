"""Original 1043/1026 round contract, persistence, ranking and settlement."""
import copy
from unittest.mock import patch
from test_activity import ActivityCase, NOW
from network_redirect import activity, activity_duty as duty, achievements
from network_redirect.backend import Backend
from network_redirect.protocol import decode, encode
from pathlib import Path


class DutyTests(ActivityCase):
    def info(self, **req):
        out = self.req(1043, **req); self.ok(out)
        return next(data for ident, data in out if ident == 19)

    def start(self):
        self.info(flag=0)
        self.info(plus_type=1, plus_index=3)

    def fight(self, grade=3, difficulty=3):
        current = self.info(flag=1)['cur_round']
        with patch('network_redirect.activity_duty.journey.battle', return_value=(grade, [], [])):
            out = self.req(1026, fight_type=5, des_value=current+1, des_type=difficulty)
        self.ok(out)
        return next(data for ident, data in out if ident == 19)

    def pass_stages(self, count):
        for _ in range(count):
            self.fight()
            if self.b.profile()['activity']['duty']['phase'] == 'prize':
                self.info(plus_type=3, plus_index=1)
                self.info(plus_type=2, plus_index=3)

    def test_original_client_round_plus_one_and_vs(self):
        self.assertEqual(self.info(flag=1)['cur_round'], 0)
        self.assertIsNone(self.b.profile()['activity']['duty'])
        self.start(); d = self.info(flag=1)
        self.assertEqual(d['cur_round'], 0)
        self.assertEqual([x['vs'][2] for x in d['lineup_list'].values()], [1]*3)
        self.assertEqual(self.fight()['cur_round'], 1)

    def test_all_nine_grade_and_difficulty_combinations(self):
        for grade in (1, 2, 3):
            for difficulty in (1, 2, 3):
                r = self.b.profile(); r['activity']['duty'] = None; r['activity']['duty_runs'] = 0; self.b.save(r)
                self.start()
                self.assertEqual(self.fight(grade, difficulty)['cur_get_star'], grade*difficulty)

    def test_prize_reentry_exchange_and_single_claim(self):
        self.start(); self.fight(); self.fight(); self.fight()
        before = self.b.profile()['silver_coin']
        for _ in range(2):
            d = self.info(flag=1); self.assertEqual(d['result'], 6)
            self.assertEqual(d['silver_prize'][1]['attach_count'], 3000)
        d = self.info(plus_type=3, plus_index=1)
        self.assertEqual(self.b.profile()['silver_coin'], before+3000)
        self.assertEqual(d['result'], 5)
        self.assertEqual(self.req(1043, plus_type=3)[0][0], 55)
        self.assertEqual(self.info(flag=1)['star_exchange'], d['star_exchange'])
        self.info(plus_type=2, plus_index=3)
        self.assertEqual(self.info(flag=1)['cur_used_star'], 3)
        self.assertEqual(self.req(1043, plus_type=2, plus_index=3)[0][0], 55)

    def test_invalid_stage_target_phase_and_flags_are_atomic(self):
        self.info(flag=0)
        attempts = [(1026, dict(fight_type=5, des_type=3, des_value=1)),
                    (1043, dict(plus_type=2, plus_index=1)),
                    (1043, dict(plus_type=1, plus_index=5)),
                    (1043, dict(plus_type=1, plus_index=1, flag=1)),
                    (1043, dict(flag=2))]
        for mid, req in attempts:
            before = self.b.profile()
            self.assertEqual(self.req(mid, **req)[0][0], 55)
            self.assertEqual(before, self.b.profile())
        self.info(plus_type=1, plus_index=1)
        for req in (dict(des_value=2), dict(des_value=1, des_id=77), dict(des_value=1, des_type=4)):
            before = self.b.profile()
            self.assertEqual(self.req(1026, **dict(dict(fight_type=5, des_type=3), **req))[0][0], 55)
            self.assertEqual(before, self.b.profile())

    def test_105_stages_no_30_100_cap_and_achievement(self):
        self.start(); self.pass_stages(105)
        r = self.b.profile()
        self.assertEqual(r['activity']['duty']['round'], 106)
        self.assertEqual(r['activity']['duty_best'], 105)
        self.assertEqual(self.info(flag=1)['max_get_star'], 945)
        for ident in range(426, 431):
            self.assertGreaterEqual(achievements.state(r)['totals'][str(ident)], 1)
        self.assertEqual(r['activity']['duty_runs'], 1)

    def test_failure_and_three_attempt_limit(self):
        self.start()
        for attempt in range(3):
            self.fight(4)
            if attempt < 2:
                self.assertEqual(self.info(flag=1)['result'], 11)
                self.info(plus_type=4, plus_index=0)
                self.info(plus_type=1, plus_index=1)
        self.assertEqual(self.info(flag=1)['result'], 7)
        self.assertEqual(self.req(1043, plus_type=4, plus_index=0)[0][0], 55)
        self.assertEqual(self.b.profile()['activity']['duty_runs'], 3)

    def test_half_resume_uses_snapshot_not_zero_bonus(self):
        self.start(); self.pass_stages(15)
        old = self.b.profile()['activity']['duty']; saved = duty.half(old)
        self.fight(4)
        preview = self.info(flag=1)
        self.assertEqual(preview['revert_begin_round'], saved['round'])
        d = self.info(plus_type=4, plus_index=1)
        self.assertEqual(d['cur_round'], saved['round']-1)
        self.assertEqual(d['cur_get_star'], saved['stars'])
        self.assertEqual(d['cur_used_star'], saved['used'])
        self.assertEqual(self.b.profile()['activity']['duty']['bonus'], saved['bonus'])
        self.assertEqual(self.b.profile()['activity']['duty_runs'], 2)

    def test_restart_zeroes_bonuses_keeps_daily_best(self):
        self.start(); self.pass_stages(6); self.fight(4)
        best = self.info(flag=1)['max_get_star']
        d = self.info(plus_type=4, plus_index=0)
        self.assertEqual(d['result'], 1)
        self.assertEqual(d['cur_round'], 0)
        self.assertEqual(d['cur_get_star'], 0)
        self.assertEqual(d['max_get_star'], best)
        self.assertEqual(sum(d['plus_list'][2].values())+sum(d['plus_list'][1].values()), 0)

    def test_yesterday_half_and_first_day_does_not_consume_query(self):
        self.start(); self.pass_stages(15)
        with patch('network_redirect.backend.time.time', return_value=NOW+86400):
            for _ in range(2):
                d = self.info(flag=1)
                self.assertEqual(d['result'], 12); self.assertEqual(d['fight_count'], 3)
            self.assertEqual(self.req(1043, plus_type=4, plus_index=1)[0][0], 55)
            d = self.info(plus_type=5, plus_index=1)
            self.assertEqual(d['fight_count'], 2)
            self.assertEqual(d['cur_round'], 6)
            self.assertEqual(self.req(1043, plus_type=5, plus_index=1)[0][0], 55)

    def test_yesterday_restart_option(self):
        self.start(); self.pass_stages(9)
        with patch('network_redirect.backend.time.time', return_value=NOW+86400):
            d = self.info(plus_type=5, plus_index=0)
            self.assertEqual(d['result'], 1); self.assertEqual(d['cur_round'], 0)

    def test_cross_day_pending_silver_and_rank_reward_exactly_once(self):
        self.start(); self.fight(); self.fight(); self.fight()
        r = self.b.profile(); gold = r['gold_coin']; silver = r['silver_coin']
        g = r['activity']['duty']['group']
        with patch('network_redirect.backend.time.time', return_value=NOW+86400):
            self.info(flag=1); self.info(flag=1)
            r = self.b.profile()
            self.assertEqual(r['silver_coin'], silver+3000)
            self.assertEqual(r['gold_coin'], gold+duty.rank_reward(g, 1))
            self.assertIsNone(r['activity']['duty'])
            self.assertIn('113', r['profile_titles'])
            self.assertGreaterEqual(achievements.state(r)['totals']['216'], 1)

    def test_backward_time_does_not_reset_or_grant(self):
        self.start(); before = self.b.profile()
        with patch('network_redirect.backend.time.time', return_value=NOW-86400):
            self.assertEqual(self.req(1043, flag=0)[0][0], 55)
        self.assertEqual(self.b.profile()['activity'], before['activity'])

    def test_reconnect_restores_all_stages_and_pending(self):
        self.start(); self.fight(); self.fight(); self.fight()
        before = self.info(flag=1)
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.assertEqual(self.info(flag=1), before)
        self.info(plus_type=3)

    def test_replay_and_encoder_failure_no_double_rewards(self):
        self.start(); self.fight(); self.fight(); self.fight()
        self.info(plus_type=3); packet, replies = self.packet, self.replies
        before = self.b.profile()
        self.assertEqual(self.b.respond(packet, self.state), replies)
        self.assertEqual(self.b.profile(), before)
        with patch('network_redirect.backend.activity.attributes', side_effect=ValueError('encoder')):
            self.assertEqual(self.req(1043, plus_type=2, plus_index=3)[0][0], 55)
        self.assertEqual(self.b.profile(), before)

    def test_best_score_is_not_lifetime_times_three(self):
        self.start(); self.fight(1, 1); self.fight(4)
        self.assertEqual(self.info(flag=1)['max_get_star'], 1)
        self.info(plus_type=4, plus_index=0); self.info(plus_type=1, plus_index=1)
        self.fight(3, 3)
        self.assertEqual(self.info(flag=1)['max_get_star'], 9)

    def test_legacy_migration_no_fabricated_snapshots(self):
        r = self.b.profile(); r['activity'].pop('duty_meta', None)
        r['activity']['duty'] = dict(round=16, stars=45, used=12, bonus=[10,0,40,0], phase='exchange')
        r['activity']['duty_runs'] = 1; self.b.save(r)
        self.assertEqual(self.info(flag=1)['cur_round'], 15)
        self.info(plus_type=2, plus_index=3); self.fight(4)
        self.assertEqual(self.req(1043, plus_type=4, plus_index=1)[0][0], 55)
        self.info(plus_type=4, plus_index=0)

    def test_actual_account_ranking_and_inspection(self):
        self.start(); self.pass_stages(3)
        r = copy.deepcopy(self.b.profile()); r.update(role_name='第二玩家', register_account='peer')
        rec = r['activity']['duty_meta']['records'][str(duty.day(NOW, self.b.activity_rules))]
        rec['stars'] += 3
        self.b.save(r, 'peer')
        out = self.req(1049, query_type=4); self.ok(out)
        board = next(d for e,d in out if e == 39)
        self.assertEqual(board['expect_order'], 2)
        rows = board['all_top_list'][board['duty_group']]
        self.assertEqual(rows[1]['name'], '第二玩家')
        out = self.req(1039, des_type=1, des_id=rows[1]['id'], flag=3)
        self.ok(out)
        self.assertEqual(next(d for e,d in out if e == 11)['role_name'], '第二玩家')
        self.assertEqual(self.req(1039, des_type=1, des_id=2**40, flag=3)[0][0], 55)

    def test_ranking_all_five_groups_csv_boundaries(self):
        for g in range(4, 9):
            self.assertGreater(duty.rank_reward(g, 20), 0)
            self.assertEqual(duty.rank_reward(g, 51), 0)
            self.assertEqual(duty.rank_reward(g, 21)>0, g == 8)
        self.assertEqual(duty.rank_reward(4, 1), 250)
        self.assertEqual(duty.rank_reward(8, 1), 700)

    def test_two_day_streak_and_gap_break(self):
        self.start(); self.pass_stages(3)
        with patch('network_redirect.backend.time.time', return_value=NOW+86400):
            self.info(plus_type=5, plus_index=0); self.info(plus_type=1, plus_index=3)
            self.pass_stages(3)
        with patch('network_redirect.backend.time.time', return_value=NOW+2*86400):
            self.info(flag=1)
            self.assertEqual(self.b.profile()['activity']['duty_meta']['streak'], 2)
            self.assertEqual(achievements.state(self.b.profile())['totals']['431'], 2)
        with patch('network_redirect.backend.time.time', return_value=NOW+4*86400):
            self.start(); self.pass_stages(3)
        with patch('network_redirect.backend.time.time', return_value=NOW+5*86400):
            self.info(flag=1)
            self.assertEqual(self.b.profile()['activity']['duty_meta']['streak'], 1)

    def test_no_participation_no_rank_no_reward(self):
        before = self.b.profile()['gold_coin']
        for offset in (0, 86400, 7*86400):
            with patch('network_redirect.backend.time.time', return_value=NOW+offset):
                self.assertEqual(self.info(flag=1)['expect_order'], 0)
                self.assertEqual(self.b.profile()['gold_coin'], before)

    def test_bonus_only_affects_battle_units_and_preview_matches(self):
        self.start(); before = self.b.profile()
        seen = []
        def run(role, cfg, rules, **kw):
            seen.append(copy.deepcopy(kw['units']))
            return 3, [], []
        with patch('network_redirect.activity_duty.journey.battle', side_effect=run):
            self.ok(self.req(1026, fight_type=5, des_type=3, des_value=1))
        original, _ = duty.journey.fighters(before, dict(cortege_list='1001|1'))
        self.assertEqual(seen[0][0][0]['gongji'], original[0]['gongji']*110//100)
        self.assertEqual(self.b.profile()['corteges'], before['corteges'])

    def test_unresolved_battle_does_not_award_win(self):
        self.start(); d = self.fight(0)
        self.assertEqual(d['cur_round'], 0); self.assertEqual(d['cur_get_star'], 0)
        self.assertEqual(self.b.profile()['activity']['duty']['phase'], 'finished')

    def test_level_gate(self):
        r = self.b.profile(); r['level'] = 11; self.b.save(r)
        self.assertEqual(self.req(1043, flag=0)[0][0], 55)
        self.assertEqual(self.req(1049, query_type=4)[0][0], 55)

    def test_rank_payment_uses_other_accounts_and_isolation(self):
        self.start(); self.pass_stages(3)
        peer = copy.deepcopy(self.b.profile()); peer.update(register_account='peer', role_name='第二玩家')
        key = str(duty.day(NOW, self.b.activity_rules))
        peer['activity']['duty_meta']['records'][key]['stars'] += 1
        self.b.save(peer, 'peer')
        old_peer = self.b.profile('peer'); before = self.b.profile()['gold_coin']
        g = peer['activity']['duty']['group']
        with patch('network_redirect.backend.time.time', return_value=NOW+86400):
            self.info(flag=1)
            self.assertEqual(self.b.profile()['gold_coin'], before+duty.rank_reward(g, 2))
        # Querying another account never settles or grants it anything.
        self.assertEqual(self.b.profile('peer')['activity'], old_peer['activity'])
        self.assertEqual(self.b.profile('peer')['gold_coin'], old_peer['gold_coin'])

    def test_late_settlement_title_does_not_restart_expiry(self):
        self.start(); self.pass_stages(3)
        with patch('network_redirect.backend.time.time', return_value=NOW+7*86400):
            self.info(flag=1)
            title = self.b.profile()['profile_titles']['113']
            self.assertLess(title['endtime'], NOW+7*86400)
            before = self.b.profile()['gold_coin']
            self.info(flag=1)
            self.assertEqual(self.b.profile()['gold_coin'], before)

    def test_rank_settlement_encoding_failure_rolls_back(self):
        self.start(); self.pass_stages(3)
        before = self.b.profile()
        with patch('network_redirect.backend.time.time', return_value=NOW+86400):
            with patch('network_redirect.backend.activity.attributes', side_effect=ValueError('encoding')):
                self.assertEqual(self.req(1043, flag=1)[0][0], 55)
        self.assertEqual(self.b.profile()['activity'], before['activity'])
        self.assertEqual(self.b.profile()['gold_coin'], before['gold_coin'])

    def test_failed_run_daily_task_exactly_once(self):
        self.start(); before = copy.deepcopy(self.b.profile().get('daily'))
        self.fight(4)
        after = self.b.profile().get('daily')
        self.assertNotEqual(before, after)
        self.info(flag=1); self.info(flag=0)
        self.assertEqual(self.b.profile().get('daily'), after)

    def test_exchange_uses_saved_offer_not_client_index_as_stat(self):
        self.start(); self.fight(); self.fight(); self.fight(); self.info(plus_type=3)
        r = self.b.profile(); d = r['activity']['duty']; d['offers'] = [dict(star=9, field=177, value=15)]
        self.b.save(r)
        self.info(plus_type=2, plus_index=1)
        d = self.b.profile()['activity']['duty']
        self.assertEqual(d['bonus'][3], 15); self.assertEqual(d['used'], 9)

    def test_insufficient_stars_preserves_offer_and_state(self):
        self.start(); self.fight(); self.fight(); self.fight(); self.info(plus_type=3)
        r = self.b.profile(); r['activity']['duty']['used'] = 27; self.b.save(r)
        before = self.b.profile()['activity']
        self.assertEqual(self.req(1043, plus_type=2, plus_index=1)[0][0], 55)
        self.assertEqual(self.b.profile()['activity'], before)

