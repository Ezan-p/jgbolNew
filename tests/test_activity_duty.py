"""Original 1043/1026 round contract, persistence, ranking and settlement."""
import copy
from unittest.mock import patch
from test_activity import ActivityCase, NOW
from network_redirect import activity, activity_duty as duty, achievements, duty_balance as balance
from network_redirect.backend import Backend
from network_redirect.protocol import decode, encode
from pathlib import Path


class DutyTests(ActivityCase):
    def setUp(self):
        super().setUp()
        # Stable baseline: reward on difficulty 2, 5% / 9-soul offers. Separate tests
        # below exercise every weighted outcome and saved random state.
        picker = patch('network_redirect.duty_balance.weighted', side_effect=lambda rows: rows[0])
        picker.start(); self.addCleanup(picker.stop)
        guard_picker = patch.object(balance, 'guard_reward', side_effect=lambda number:
            dict(round=number, difficulty=2, reward=[12, 0, 3000, 1]))
        guard_picker.start(); self.addCleanup(guard_picker.stop)

    def set_guard_reward(self, reward, difficulty=3):
        role = self.b.profile(); d = role['activity']['duty']
        d['guard_reward'] = dict(round=d['round'], difficulty=difficulty, reward=reward)
        self.b.save(role)

    def test_one_visible_reward_per_layer_persists_across_backend_restart(self):
        self.start()
        first = self.info(flag=1)['lineup_list']
        self.assertEqual([i for i, row in first.items() if 'reward' in row], [2])
        self.assertTrue(all('gold' not in row for row in first.values()))
        self.assertEqual(len({row['type'] for row in first.values()}), 3)
        with patch.object(balance, 'guard_reward', side_effect=AssertionError('rerolled')):
            self.assertEqual(first, self.info(flag=1)['lineup_list'])
            self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
            self.assertEqual(first, self.info(flag=1)['lineup_list'])

    def test_guard_selection_passes_corresponding_difficulty_to_actual_battle(self):
        self.start()
        saved = self.b.profile()
        group = saved['activity']['duty']['group']
        for difficulty in (1, 2, 3):
            self.b.save(copy.deepcopy(saved))
            with patch.object(duty.journey, 'battle', return_value=(4, [], [])) as battle:
                self.ok(self.req(1026, fight_type=5, des_value=1, des_type=difficulty))
            self.assertEqual(battle.call_args.kwargs['units'][1], balance.enemies(group, 1, difficulty))

    def test_unrewarded_guard_and_loss_never_grant_displayed_reward(self):
        self.start(); self.set_guard_reward([5, 1031, 1, 1], 2)
        self.fight(difficulty=1)
        self.assertFalse(duty.pending(self.b.profile()['activity']['duty']))
        self.assertEqual(self.info(flag=1)['result'], 3)
        self.set_guard_reward([5, 1031, 1, 1], 3)
        self.fight(4)
        self.assertFalse(duty.pending(self.b.profile()['activity']['duty']))

    def test_silver_guard_and_third_stage_silver_stack(self):
        self.start(); self.pass_stages(2)
        self.set_guard_reward([12, 0, 3000, 1])
        self.fight()
        self.assertEqual(duty.pending(self.b.profile()['activity']['duty']), [[12, 0, 3000, 1]]*2)
        before = self.b.profile()['silver_coin']
        self.info(plus_type=3)
        self.assertEqual(self.b.profile()['silver_coin'], before+6000)

    def test_legacy_fight_migrates_once_and_preserves_old_pending_reward(self):
        self.start()
        role = self.b.profile(); role['activity']['duty'].pop('guard_reward'); self.b.save(role)
        self.assertEqual(sum('reward' in row for row in self.info(flag=1)['lineup_list'].values()), 1)
        role = self.b.profile(); d = role['activity']['duty']
        d.update(phase='prize', pending_rewards=[[11, 0, 30, 1]], after_prize='fight')
        d.pop('guard_reward'); self.b.save(role)
        before = self.b.profile()['gold_coin']
        self.info(plus_type=3)
        self.assertEqual(self.b.profile()['gold_coin'], before+30)
        self.assertEqual(sum('reward' in row for row in self.info(flag=1)['lineup_list'].values()), 1)

    def test_half_snapshot_preserves_visible_guard_without_pending_prize(self):
        self.start(); self.pass_stages(12)
        before = duty.half(self.b.profile()['activity']['duty'])
        self.fight(4); self.info(plus_type=4, plus_index=1)
        d = self.b.profile()['activity']['duty']
        self.assertEqual(d['guard_reward'], before['guard_reward'])
        self.assertFalse(duty.pending(d))

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
            if self.b.profile()['activity']['duty']['phase'] == 'exchange':
                self.info(plus_type=2, plus_index=3)

    def test_original_client_round_plus_one_and_vs(self):
        self.assertEqual(self.info(flag=1)['cur_round'], 0)
        self.assertIsNone(self.b.profile()['activity']['duty'])
        self.start(); d = self.info(flag=1)
        self.assertEqual(d['cur_round'], 0)
        self.assertEqual([x['vs'][2] for x in d['lineup_list'].values()], [self.b.profile()['activity']['duty']['group']]*3)
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
        self.assertEqual(self.info(flag=1)['cur_used_star'], 9)
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

    def test_low_grade_souls_accumulate_without_exchange_softlock(self):
        self.start()
        for stage in range(1, 10):
            self.fight(1, 1)
            if stage % 3 == 0:
                info = self.info(plus_type=3)
                self.assertEqual(info['result'], 5 if stage == 9 else 3)
        self.assertEqual(info['cur_get_star'], 9)
        self.info(plus_type=2, plus_index=1)
        self.assertEqual(self.info(flag=1)['cur_used_star'], 9)

    def test_random_prize_ack_resumes_fight_and_preserves_reconnect(self):
        self.start()
        self.set_guard_reward([5, 1032, 1, 1])
        self.fight()
        before = self.info(flag=1)
        self.assertEqual(before['silver_prize'][1]['attach_type'], 1032)
        self.assertEqual(before['result'], 6)
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.assertEqual(self.info(flag=1), before)
        before_count = sum(i['count'] for i in self.b.profile()['attachments'] if i['type_id'] == 1032)
        self.assertEqual(self.info(plus_type=3)['result'], 3)
        after_count = sum(i['count'] for i in self.b.profile()['attachments'] if i['type_id'] == 1032)
        self.assertEqual(after_count, before_count+1)
        saved = self.b.profile()
        self.assertEqual(self.req(1043, plus_type=3)[0][0], 55)
        self.assertEqual(self.b.profile(), saved)

    def test_all_random_prizes_settle_once_and_loss_has_no_roll(self):
        self.start()
        for row in balance.rules()['drops']:
            prize = row['reward']
            self.set_guard_reward(prize)
            with patch.object(balance, 'drop') as roll:
                result = self.fight()
                roll.assert_not_called()
            self.assertIn(prize, duty.pending(self.b.profile()['activity']['duty']))
            before = self.b.profile()
            self.info(plus_type=3)
            after = self.b.profile()
            if prize[0] == 11:
                self.assertEqual(after['gold_coin']-before['gold_coin'], prize[2])
            elif prize[0] == 12:
                self.assertEqual(after['silver_coin']-before['silver_coin'], prize[2])
            else:
                count = lambda r: sum(i['count'] for i in r['attachments'] if i['type_id'] == prize[1])
                self.assertEqual(count(after)-count(before), prize[2])
            if after['activity']['duty']['phase'] == 'exchange':
                self.info(plus_type=2, plus_index=1)
        with patch.object(balance, 'drop') as roll:
            self.fight(4)
            roll.assert_not_called()

    def test_random_drop_encoder_failure_rolls_back_entire_win(self):
        self.start(); self.set_guard_reward([11, 0, 20, 1]); before = self.b.profile()
        with patch.object(duty.journey, 'battle', return_value=(3, [], [])), \
             patch('network_redirect.backend.activity.attributes', side_effect=ValueError('encode')):
            self.assertEqual(self.req(1026, fight_type=5, des_type=3, des_value=1)[0][0], 55)
        self.assertEqual(before, self.b.profile())

    def test_pending_random_prizes_cross_day_and_half_never_duplicates(self):
        self.start(); self.pass_stages(6)
        self.set_guard_reward([11, 0, 20, 1])
        self.fight()
        before = self.b.profile()['gold_coin']
        g = self.b.profile()['activity']['duty']['group']
        with patch('network_redirect.backend.time.time', return_value=NOW+86400):
            self.info(flag=1); self.info(flag=1)
            self.assertEqual(self.b.profile()['gold_coin'], before+20+duty.rank_reward(g, 1))
            self.info(plus_type=5, plus_index=1)
            self.assertFalse(duty.pending(self.b.profile()['activity']['duty']))

    def test_affordable_fallback_and_saved_random_offers(self):
        self.start(); self.fight(); self.fight()
        with patch.object(balance, 'weighted', side_effect=lambda rows: rows[-1]), \
             patch.object(balance.secrets, 'randbelow', return_value=2):
            self.fight()
        d = self.b.profile()['activity']['duty']
        self.assertEqual([o['value'] for o in d['offers']], [20, 20, 5, 20])
        self.assertEqual(d['offers'][2]['star'], 9)
        offers = copy.deepcopy(d['offers'])
        self.info(flag=1); self.info(plus_type=3); self.info(flag=1)
        self.assertEqual(self.b.profile()['activity']['duty']['offers'], offers)
        before = self.b.profile()
        self.assertEqual(self.req(1043, plus_type=2, plus_index=1)[0][0], 55)
        self.assertEqual(self.b.profile(), before)
        self.info(plus_type=2, plus_index=3)
        self.assertEqual(self.b.profile()['activity']['duty']['bonus'][2], 5)

    def test_half_keeps_group_and_saved_offers(self):
        self.start(); self.pass_stages(12)
        r = self.b.profile(); d = r['activity']['duty']
        saved = d['checkpoints']['6']
        saved.update(phase='exchange', offers=[dict(field=177, value=15, star=27)], stars=54, used=9)
        original_group = d['group']
        d['phase'] = 'finished'; r['cortege_count'] = 4; self.b.save(r)
        self.info(plus_type=4, plus_index=1)
        d = self.b.profile()['activity']['duty']
        self.assertEqual(d['group'], original_group)
        self.assertEqual(d['offers'], saved['offers'])
        self.assertFalse(duty.pending(d))

    def test_each_bonus_tier_debits_its_saved_cost_and_value(self):
        self.start()
        for index, tier in enumerate(balance.rules()['bonus_tiers']):
            r = self.b.profile(); d = r['activity']['duty']
            d.update(phase='exchange', stars=108, used=0, bonus=[0]*4)
            with patch.object(balance, 'weighted', return_value=tier):
                d['offers'] = balance.offers(108)
            self.b.save(r)
            self.info(plus_type=2, plus_index=index+1)
            d = self.b.profile()['activity']['duty']
            self.assertEqual(d['used'], tier['star'])
            self.assertEqual(d['bonus'][index], tier['value'])
            self.assertEqual(sum(d['bonus']), tier['value'])

