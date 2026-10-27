"""Thirty complete rounds, simultaneous upkeep and authoritative outcome boundaries."""
import copy
import unittest
from unittest.mock import patch

from network_redirect import combat_engine as engine, journey


def unit(order=1, **values):
    return dict(dict(type=1001, order=order, level=1, evolve=0, reborn=0,
                     hp=1000, max_hp=1000, gongji=0, fangyu=0, magic=0, skills=[]), **values)


class RoundLimitTests(unittest.TestCase):
    def setUp(self):
        self.rules = journey.load_rules()
        rng = patch('network_redirect.combat.secrets.randbelow', return_value=0)
        rng.start()
        self.addCleanup(rng.stop)

    def battle(self, sides, **kwargs):
        battle = engine.Battle({}, sides, self.rules, **kwargs)
        return battle, battle.run()

    def test_exact_current_hp_comparison_including_one_point_and_ties(self):
        for left, right, expected in ((1000, 999, 3), (999, 1000, 4), (1000, 1000, 0)):
            with self.subTest(left=left, right=right):
                b, (result, _, actions) = self.battle(([unit(hp=left)], [unit(hp=right)]))
                self.assertEqual(result, expected)
                self.assertEqual((b.round, actions.rounds, len(actions)), (30, 30, 60))
                self.assertEqual(actions.stop_reason, 'round_limit')
                self.assertEqual(max(row['cur_round'] for row in actions), 30)

    def test_compare_absolute_hp_not_ratio_and_include_living_reserves(self):
        _, (result, _, actions) = self.battle(
            ([unit(hp=800, max_hp=10000), unit(5, hp=800, max_hp=10000)], [unit(hp=1500, max_hp=1500)]))
        self.assertEqual(result, 1)  # 1600 > 1500 despite lower HP percentage.
        self.assertEqual(actions.final_hp[1][5], 800)
        self.assertTrue(all(row['src_order'] != 5 for row in actions))

    def test_finish_every_position_and_additional_action_in_round_thirty(self):
        effects = {3: (100, 100), 7: (100, 100)}
        sides = [[unit(i, essences=effects) for i in range(1, 5)] for _ in (1, 2)]
        _, (result, _, actions) = self.battle(sides)
        self.assertEqual(result, 0)
        self.assertEqual(len(actions), 30 * 8 * 3)
        self.assertEqual(sum(row['cur_round'] == 30 for row in actions), 24)
        self.assertEqual((actions[-1]['is_src'], actions[-1]['src_order']), (False, 3))

    def test_nine_grid_runs_540_main_actions_independent_of_old_limits(self):
        self.rules['battle']['max_actions'] = 16
        _, (result, _, actions) = self.battle(
            [[unit(i) for i in range(1, 10)] for _ in (1, 2)], slots=9)
        self.assertEqual((result, len(actions), actions.rounds), (0, 540, 30))

    def test_both_sides_poisoned_to_death_finish_upkeep_before_result(self):
        b = engine.Battle({}, ([unit(hp=10)], [unit(hp=10)]), self.rules)
        for side in (1, 2):
            b.sides[side - 1][0]['poison'] = dict(rate=1, source_side=3-side, logic=101162)
        result, _, actions = b.run()
        self.assertEqual((result, actions.rounds, actions.stop_reason), (0, 1, 'elimination'))
        self.assertEqual(actions.final_hp, {1: {1: 0}, 2: {1: 0}})
        self.assertEqual(len(actions), 2)
        self.assertEqual(actions.damage_totals, {1: 10, 2: 10})

    def test_poison_revive_is_resolved_before_comparing_sides(self):
        b = engine.Battle({}, ([unit(hp=10, essences={19: (100, 50)})], [unit(hp=10)]), self.rules)
        for side in (1, 2):
            b.sides[side - 1][0]['poison'] = dict(rate=1, source_side=3-side, logic=101162)
        result, _, actions = b.run()
        self.assertEqual(result, 2)
        self.assertEqual(actions.final_hp, {1: {1: 500}, 2: {1: 0}})

    def test_elimination_on_last_round_is_resolved_before_round_limit(self):
        _, (result, _, actions) = self.battle(([unit(gongji=1)], [unit(hp=30)]))
        self.assertEqual((result, actions.rounds, actions.stop_reason), (3, 30, 'elimination'))

    def test_opening_passives_are_display_metadata_not_extra_combat_turns(self):
        sides = ([unit(skills=[(2, 1)]), unit(5, skills=[(2, 2)])], [unit()])
        original = copy.deepcopy(sides)
        _, (_, _, actions) = self.battle(sides)
        self.assertEqual(len(actions), 60)
        opening = engine.event_data(actions, 9)['opening_passives']
        self.assertEqual([row['src_order'] for row in opening], [1, 5])
        self.assertTrue(all(row['cur_round'] == 0 and row['self_use'] and not any(row['damage_list']) for row in opening))
        self.assertEqual(sides, original)


if __name__ == '__main__':
    unittest.main()
