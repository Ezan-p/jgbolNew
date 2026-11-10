"""Original map wire semantics, odds, debit/replay and legacy-board continuity."""
import copy
from pathlib import Path
from unittest.mock import patch
from tests.test_activity import ActivityCase, NOW
from network_redirect import activity, activity_abyss, activity_treasure as treasure, formation, summon
from network_redirect.backend import Backend


class TreasureTests(ActivityCase):
    def setUp(self):
        super().setUp()
        role = self.b.profile(); role['level'] = 80
        activity_abyss.state(role, NOW, self.b.activity_rules)
        for tid in range(1431, 1441):
            summon.add_item(role, tid, 110)
        self.b.save(role)

    def call(self, op=3, **data):
        out = self.req(1329, id=op, data=summon.lua(data)); self.ok(out)
        result = next(v for ident, v in out if ident == 173)
        return result['event_data'] if op == 3 else result

    def count(self, tid):
        return sum(i['count'] for i in self.b.profile()['attachments'] if i['attach_type'] == 5 and i['type_id'] == tid)

    def reject(self, op=3, **data):
        before = self.b.profile()
        self.assertEqual(self.req(1329, id=op, data=summon.lua(data))[0][0], 55)
        self.assertEqual(before, self.b.profile())

    def test_native_batch_field_order_and_99_maps_one_draw_free(self):
        gold = self.b.profile()['gold_coin']
        with patch.object(treasure.secrets, 'randbelow', return_value=0):
            out = self.call(24, map_type=1431, treasure_count=1, open_count=99)
        self.assertEqual(self.count(1431), 11)
        self.assertEqual(self.b.profile()['gold_coin'], gold)
        self.assertEqual(len(out['prize_list']), 1)
        self.assertEqual(out['prize_list'][1]['attach_type'], 1310)
        self.assertEqual(out['prize_list'][1]['attach_count'], 99)

    def test_five_draw_batch_cost_aggregation_and_no_replacement(self):
        before = self.count(1431); gold = self.b.profile()['gold_coin']
        with patch.object(treasure.secrets, 'randbelow', return_value=0):
            out = self.call(24, map_type=1431, treasure_count=5, open_count=3)
        self.assertEqual(self.count(1431), before - 3)
        self.assertEqual(self.b.profile()['gold_coin'], gold - 240)
        expected = {p[1]: p[2] * 3 for p in self.b.activity_rules['abyss_map_rewards'][:5]}
        self.assertEqual({p['attach_type']: p['attach_count'] for p in out['prize_list'].values()}, expected)

    def test_batch_replay_and_restart_no_double_award(self):
        self.call(24, map_type=1431, treasure_count=2, open_count=7)
        before = self.b.profile(); replies = self.replies
        self.assertEqual(self.b.respond(self.packet, self.state), replies)
        self.assertEqual(self.b.profile(), before)
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.assertEqual(self.b.profile(), before)

    def test_batch_invalid_counts_types_resources_and_level_are_atomic(self):
        for draws, maps in ((0, 1), (6, 1), (1, 0), (1, 100), (True, 2), (1, True), (1.5, 2), ('2', 3)):
            self.reject(24, map_type=1431, treasure_count=draws, open_count=maps)
        self.reject(24, map_type=1430, treasure_count=1, open_count=1)
        role = self.b.profile(); role['gold_coin'] = 19; self.b.save(role)
        self.reject(24, map_type=1431, treasure_count=2, open_count=1)
        role = self.b.profile(); role['level'] = 69; self.b.save(role)
        self.reject(24, map_type=1431, treasure_count=1, open_count=1)
        role = self.b.profile(); role['level'] = 80
        for i in role['attachments']:
            if i['type_id'] == 1431: i['is_lock'] = True
        self.b.save(role)
        self.reject(24, map_type=1431, treasure_count=1, open_count=1)
        self.reject(op_type=1, type_id=1431)

    def test_no_partial_commit_when_grant_or_encoding_fails(self):
        with patch.object(treasure, 'grant', side_effect=formation.Rejected('奖品失败')):
            self.reject(24, map_type=1431, treasure_count=2, open_count=7)
        with patch.object(activity_abyss, 'response', side_effect=formation.Rejected('编码失败')):
            self.reject(24, map_type=1431, treasure_count=2, open_count=7)

    def test_single_open_free_draw_paid_continuation_exhaustion(self):
        count = self.count(1431); gold = self.b.profile()['gold_coin']
        out = self.call(op_type=1, type_id=1431)
        self.assertEqual(out['max_pay_times'], 4)
        self.assertEqual(self.count(1431), count)
        indices = []
        with patch.object(treasure.secrets, 'randbelow', return_value=0):
            for n in range(5):
                out = self.call(op_type=2, type_id=1431, **({'index_list': [1, 2]} if n == 0 else {}))
                indices.append(out['des_index'])
                self.assertEqual(self.b.profile()['gold_coin'], gold - n * 20)
        self.assertEqual(indices, [3, 4, 5, 6, 7])
        self.assertEqual(self.count(1431), count - 1)
        self.reject(op_type=2, type_id=1431)
        self.call(op_type=1, type_id=1431)
        self.assertEqual(self.count(1431), count - 1)

    def test_pending_map_blocks_batch_but_abandon_keeps_rewards(self):
        count = self.count(1431)
        self.call(op_type=1, type_id=1431)
        self.call(op_type=3, type_id=1431)
        self.assertEqual(self.count(1431), count)
        self.call(op_type=1, type_id=1431); self.call(op_type=2, type_id=1431)
        self.reject(24, map_type=1431, treasure_count=1, open_count=2)
        self.reject(op_type=2, type_id=1431, index_list=[2])
        self.call(op_type=3, type_id=1431)
        self.assertEqual(self.count(1431), count - 1)
        self.call(24, map_type=1431, treasure_count=1, open_count=2)
        self.assertEqual(self.count(1431), count - 3)

    def test_legacy_board_preserves_four_draw_limit_uniform_odds_and_goods(self):
        role = self.b.profile(); board = self.old_board(1)
        board['goods'][0]['got'] = True; board['goods'][1]['rm'] = True
        role['activity']['abyss']['maps'] = {'1431': board}; self.b.save(role)
        self.assertEqual(self.call(op_type=1, type_id=1431)['max_pay_times'], 3)
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        stored = self.b.profile()['activity']['abyss']['maps']['1431']
        self.assertEqual(stored['goods'], board['goods']); self.assertEqual(stored['weights'], [1] * 12)
        for _ in range(3): self.call(op_type=2, type_id=1431)
        self.reject(op_type=2, type_id=1431)
        self.assertEqual(self.call(op_type=1, type_id=1431)['max_pay_times'], 4)

    def test_policy_snapshot_and_month_card_expires_during_draw(self):
        role = self.b.profile(); role['month_card_time'] = NOW + 1; self.b.save(role)
        self.call(op_type=1, type_id=1431); self.call(op_type=5, type_id=1431)
        with patch('network_redirect.game_clock.now', return_value=NOW + 2):
            out = self.call(op_type=2, type_id=1431)
        self.assertFalse(out['mark_flag'])
        with patch.dict(self.b.activity_rules, abyss_map_gold=123):
            gold = self.b.profile()['gold_coin']
            out = self.call(op_type=2, type_id=1431)
            self.assertEqual(out['pay_gold_count'], 20)
            self.assertEqual(self.b.profile()['gold_coin'], gold - 20)

    def test_all_ten_tiers_and_twelve_rewards_reach_inventory(self):
        for tid in range(1431, 1441):
            for index, spec in enumerate(self.b.activity_rules['abyss_map_rewards']):
                before = self.count(spec[1])
                ticket = sum(self.b.activity_rules['abyss_map_weights'][:index])
                with patch.object(treasure.secrets, 'randbelow', return_value=ticket):
                    out = self.call(24, map_type=tid, treasure_count=1, open_count=1)
                self.assertEqual(self.count(spec[1]) - before, spec[2] * (tid - 1430))
                self.assertEqual(out['prize_list'][1]['attach_type'], spec[1])

    def test_weight_boundaries_removal_and_probability_mass(self):
        board = treasure.new_board(1431, self.b.activity_rules)
        hits = [0] * 12
        for ticket in range(sum(board['weights'])):
            with patch.object(treasure.secrets, 'randbelow', return_value=ticket):
                hits[treasure.draw(copy.deepcopy(board))] += 1
        self.assertEqual(hits, [17,17,17,2,2,2,10,10,2,2,9,10])
        board['goods'][0]['rm'] = True; board['goods'][1]['got'] = True
        board['weights'] = list(range(1, 13))
        start = 0
        for index in range(2, 12):
            for ticket in (start, start + board['weights'][index] - 1):
                with patch.object(treasure.secrets, 'randbelow', return_value=ticket) as rand:
                    self.assertEqual(treasure.draw(copy.deepcopy(board)), index)
                    rand.assert_called_once_with(sum(range(3, 13)))
            start += board['weights'][index]

    def test_maximum_batch_result_bounded(self):
        with patch.object(treasure.secrets, 'randbelow', return_value=0):
            out = self.call(24, map_type=1440, treasure_count=5, open_count=99)
        self.assertEqual(len(out['prize_list']), 5)
        self.assertEqual(self.count(1440), 11)
        self.assertLess(max(map(len, self.replies)), 65535)

    def test_config_validation(self):
        for key, value in (('abyss_map_weights', [1] * 11), ('abyss_map_weights', [0] + [1] * 11),
                           ('abyss_map_weights', [True] * 12), ('abyss_map_batch_limit', 100),
                           ('abyss_map_paid_draws', 3), ('abyss_map_revision', '')):
            rules = copy.deepcopy(self.b.activity_rules); rules[key] = value
            with self.assertRaises(formation.Rejected): treasure.validate(rules)

    def old_board(self, draws=0):
        old = [(1001,10),(1022,1),(1023,1),(1034,1),(1343,1),(1442,1),
               (1701,10),(1702,2),(1330,5),(1006,1),(1366,50),(1361,50)]
        return dict(draws=draws, quick=False,
                    goods=[activity.prize_spec([5, tid, n, 1]) for tid, n in old])

    def test_user_pool_quantities_and_category_probabilities(self):
        rules = self.b.activity_rules
        old_ids = {p['attach_type'] for p in self.old_board()['goods']}
        new_ids = {p[1] for p in rules['abyss_map_rewards']}
        self.assertEqual(old_ids & new_ids, {1343})
        self.assertNotIn(1060, new_ids); self.assertNotIn(1246, new_ids)
        self.assertEqual([p[2] for p in rules['abyss_map_rewards']], [1] * 12)
        groups = ({1310,1311,1312}, {1313,1314,1323}, {1333}, {1343}, {1329,1331,1332}, {1249})
        for group, weight in zip(groups, (51,14,2,10,14,9)):
            self.assertTrue(group <= new_ids)
            self.assertEqual(sum(w for p,w in zip(rules['abyss_map_rewards'], rules['abyss_map_weights'])
                                 if p[1] in group), weight)
        for bad in (1001,1330,1442,1310,1343):
            invalid = copy.deepcopy(rules); invalid['abyss_map_rewards'][-1][1] = bad
            with self.assertRaises(formation.Rejected): treasure.validate(invalid)

    def test_unpaid_old_preview_requires_reopen_then_refreshes_without_debit(self):
        for revision in (None, '2026-11-07-native-batch-v2'):
            role = self.b.profile(); board = self.old_board()
            if revision:
                board.update(revision=revision, weights=[1]*12, paid_draws=4, gold=20, remove_count=2)
            role['activity']['abyss']['maps'] = {'1431': board}; self.b.save(role)
            self.reject(op_type=2, type_id=1431)
            before = self.count(1431); gold = self.b.profile()['gold_coin']
            out = self.call(op_type=1, type_id=1431)
            self.assertEqual(out['shop_list'][1]['attach_type'], 1310)
            self.assertEqual(self.count(1431), before)
            self.assertEqual(self.b.profile()['gold_coin'], gold)
            self.assertEqual(out['max_pay_times'], 4)

    def test_started_v2_board_preserves_old_rewards_weights_and_paid_opportunities(self):
        role = self.b.profile(); board = self.old_board(1)
        board.update(revision='2026-11-07-native-batch-v2', weights=[1]*12, paid_draws=4, gold=20, remove_count=2)
        board['goods'][0]['got'] = True; board['goods'][1]['rm'] = True
        role['activity']['abyss']['maps'] = {'1431': board}; self.b.save(role)
        self.call(op_type=1, type_id=1431)
        self.assertEqual(self.b.profile()['activity']['abyss']['maps']['1431'], board)
        before = self.count(1023)
        with patch.object(treasure.secrets, 'randbelow', return_value=0):
            self.call(op_type=2, type_id=1431)
        self.assertEqual(self.count(1023), before + 1)
        for _ in range(3): self.call(op_type=2, type_id=1431)
        self.reject(op_type=2, type_id=1431)
        self.assertEqual(self.call(op_type=1, type_id=1431)['shop_list'][1]['attach_type'], 1310)

    def test_new_peach_and_four_star_vessel_are_distinct_and_merge_across_maps(self):
        with patch.object(treasure.secrets, 'randbelow', side_effect=[57,80,57,80]):
            out = self.call(24, map_type=1440, treasure_count=2, open_count=2)
        self.assertEqual({p['attach_type']: p['attach_count'] for p in out['prize_list'].values()},
                         {1343: 20, 1313: 20})
        self.call(op_type=1, type_id=1431)
        with patch.object(treasure.secrets, 'randbelow', side_effect=[57,80]):
            first = self.call(op_type=2, type_id=1431)
            second = self.call(op_type=2, type_id=1431)
        self.assertEqual((first['des_index'], second['des_index']), (7,12))
        self.assertEqual(second['shop_list'][12]['attach_type'], 1313)
        self.assertTrue(second['shop_list'][7]['got'] and second['shop_list'][12]['got'])

    def test_v4_preview_refreshes_but_started_board_keeps_both_peach_slots(self):
        for draws in (0,1):
            role = self.b.profile()
            board = dict(draws=draws, quick=False, revision='2026-11-09-user-pool-v4',
                         paid_draws=4, gold=20, remove_count=2,
                         weights=[10,10,10,10,10,6,9,10,7,4,7,7],
                         goods=[activity.prize_spec([5,tid,n,1]) for tid,n in
                                [(1310,10),(1311,10),(1312,10),(1314,2),(1323,2),(1333,1),
                                 (1343,1),(1329,2),(1331,1),(1332,1),(1249,1),(1343,1)]])
            if draws: board['goods'][0]['got'] = True
            role['activity']['abyss']['maps'] = {'1431': copy.deepcopy(board)}; self.b.save(role)
            if not draws: self.reject(op_type=2, type_id=1431)
            before = self.count(1431)
            self.call(op_type=1, type_id=1431)
            stored = self.b.profile()['activity']['abyss']['maps']['1431']
            self.assertEqual(self.count(1431), before)
            if draws:
                self.assertEqual(stored, board)
                with patch.object(treasure.secrets, 'randbelow', side_effect=[46,74]):
                    self.assertEqual(self.call(op_type=2, type_id=1431)['des_index'], 7)
                    result = self.call(op_type=2, type_id=1431)
                self.assertEqual(result['des_index'], 12)
                self.assertEqual(result['prize_list'][1]['attach_type'], 1343)
            else:
                self.assertEqual(stored['revision'], self.b.activity_rules['abyss_map_revision'])
                self.assertEqual(stored['weights'], [17,17,17,2,2,2,10,10,2,2,9,10])
                self.assertEqual(stored['goods'][11]['attach_type'], 1313)
                self.assertTrue(all(p['attach_count']==1 for p in stored['goods']))

    def test_peach_reward_can_be_used_for_targeted_training(self):
        with patch.object(treasure.secrets, 'randbelow', return_value=57):
            self.call(24, map_type=1431, treasure_count=1, open_count=1)
        role = self.b.profile(); c = role['corteges'][0]
        c['culture_point'] = 5; self.b.save(role)
        old = self.count(1343); attack = c['gongji_plus']
        self.ok(self.req(1089, cortege_id=c['id'], train_field=2, train_point=5))
        self.assertEqual(self.count(1343), old - 1)
        updated = next(x for x in self.b.profile()['corteges'] if x['id'] == c['id'])
        self.assertEqual(updated['culture_point'], 0)
        self.assertGreater(updated['gongji_plus'], attack)

    def test_awarded_realm_boxes_can_be_exchanged_for_owned_companion_souls(self):
        with patch.object(treasure.secrets, 'randbelow', return_value=86):
            self.call(24, map_type=1431, treasure_count=1, open_count=5)
        role = self.b.profile(); box = next(i for i in role['attachments'] if i['type_id'] == 1249)
        self.ok(self.req(1051, item_type=1249, item_id=box['id'], item_count=5, des_type=5, des_id=5005))
        role = self.b.profile(); realm = next(i for i in role['attachments'] if i['type_id'] == 5005)
        souls = role.get('souls', {}).get('5004', 0); silver = role['silver_coin']
        self.ok(self.req(1051, item_type=5005, item_id=realm['id'], item_count=5, des_type=4, des_id=5004))
        self.assertEqual(self.b.profile()['souls']['5004'], souls + 5)
        self.assertEqual(self.b.profile()['silver_coin'], silver - 25000)
