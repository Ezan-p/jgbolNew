"""Fight completion is independent of transport size and victory labels."""
import copy
import random
import unittest
from unittest.mock import patch

from network_redirect import combat_engine as engine, formation, journey


def unit(order=1, **values):
    return dict(dict(type=1001, order=order, level=1, evolve=0, reborn=0,
                     hp=1000, max_hp=1000, gongji=100, fangyu=0, magic=0, skills=[]), **values)


class CombatTerminationTests(unittest.TestCase):
    def setUp(self):
        self.rules = journey.load_rules()
        random = patch('network_redirect.combat.secrets.randbelow', return_value=0)
        random.start()
        self.addCleanup(random.stop)

    def battle(self, sides, budget=1000, **options):
        rules = copy.deepcopy(self.rules)
        rules['battle']['mechanics']['event_budget_bytes'] = budget
        battle = engine.Battle({}, sides, rules, **options)
        return battle, battle.run()

    def assert_hp_replay(self, battle):
        hp = {(side, u['order']): u['hp'] for side, units in enumerate(battle.initial, 1) for u in units}
        events = {}
        for event in battle.actions.events:
            self.assertTrue(1 <= event['cur_action'] <= len(battle.actions))
            events.setdefault(event['cur_action'], []).append(event)
        for index, action in enumerate(battle.actions, 1):
            target_side = 2 if action['is_src'] else 1
            single = int(formation.SKILLS[action['skill_type']]['effect_target(1-single，2-multi)']) == 1
            for order, hit in enumerate(action['damage_list'], 1):
                if single and order != action['des_order']:
                    self.assertEqual(hit, 0, 'native single-target playback ignores off-target damage slots')
                    continue
                if hit:
                    hp[target_side, order] -= hit
                    self.assertGreaterEqual(hp[target_side, order], 0)
            for event in events.get(index, []):
                for change in event['skill_result_list']:
                    if change['field'] == 65:
                        hp[event['who_use'], change['des_order']] += change['field_plus']
                    elif change['field'] == 9999:
                        hp[event['who_use'], change['des_order']] += change.get('hp_add', 0)
        self.assertEqual(hp, {(side, order): value for side, units in battle.actions.final_hp.items()
                              for order, value in units.items()})

    def test_lifesteal_reaches_round_cap_independent_of_event_budgets(self):
        sides = ([unit(hp=10000, max_hp=10000, gongji=150, essences={5: (50,)})],
                 [unit(hp=10000, max_hp=10000, essences={5: (50,)})])
        outcomes = []
        for budget in (1000, 12000):
            battle, (result, _, actions) = self.battle(sides, budget)
            self.assertGreater(battle.event_bytes, 1000)
            self.assertEqual(actions.stop_reason, 'round_limit')
            self.assertGreater(sum(actions.final_hp[1].values()), sum(actions.final_hp[2].values()))
            self.assertEqual(result, 3)
            self.assert_hp_replay(battle)
            outcomes.append((result, actions, actions.events, actions.final_hp))
        self.assertEqual(outcomes[0], outcomes[1])

    def test_round_healing_keeps_all_events_through_round_cap(self):
        sides = ([unit(hp=10000, max_hp=10000, gongji=150, essences={10: (100, 10)})],
                 [unit(hp=10000, max_hp=10000)])
        battle, (result, _, actions) = self.battle(sides)
        self.assertGreater(battle.event_bytes, 1000)
        self.assertEqual(actions.stop_reason, 'round_limit')
        self.assertEqual(result, 3)
        self.assertGreater(actions.final_hp[1][1], actions.final_hp[2][1])
        self.assert_hp_replay(battle)

    def test_endless_sustain_finishes_at_round_limit_by_remaining_hp(self):
        sides = ([unit(essences={5: (100,)})], [unit(essences={5: (100,)})])
        battle, (result, _, actions) = self.battle(sides)
        self.assertEqual(actions.rounds, 30)
        self.assertEqual(len(actions), 60)
        self.assertEqual(actions.stop_reason, 'round_limit')
        self.assertEqual(result, 4)
        self.assertTrue(all(hp > 0 for side in actions.final_hp.values() for hp in side.values()))
        self.assert_hp_replay(battle)

    def test_zero_action_limit_is_respected_without_guessing_a_winner(self):
        _, (result, _, actions) = self.battle(([unit()], [unit()]), max_actions=0)
        self.assertEqual((result, len(actions), actions.stop_reason), (0, 0, 'debug_action_limit'))
        self.assertEqual(actions.final_hp, {1: {1: 1000}, 2: {1: 1000}})

    def test_empty_rosters_take_precedence_over_zero_action_limit(self):
        for sides, expected in ((([unit()], []), 3), (([], [unit()]), 4), (([], []), 0)):
            with self.subTest(expected=expected):
                _, (result, _, actions) = self.battle(sides, max_actions=0)
                self.assertEqual((result, len(actions), actions.stop_reason), (expected, 0, 'elimination'))

    def test_winning_stars_require_elimination_and_use_exact_hp_boundaries(self):
        for hp, expected in ((1, 1), (399, 1), (400, 2), (699, 2), (700, 3), (1000, 3)):
            with self.subTest(hp=hp):
                battle, (result, _, actions) = self.battle(([unit(hp=hp, gongji=10000)], [unit()]))
                self.assertEqual(result, expected)
                self.assertEqual(actions.stop_reason, 'elimination')
                self.assertEqual(actions.final_hp[2][1], 0)
                self.assert_hp_replay(battle)

    def test_single_target_sharing_reaches_protector_via_hp_event(self):
        battle, (_, _, actions) = self.battle(
            ([unit(gongji=1000)], [unit(skills=[(21, 10)]), unit(2, hp=500)]), max_actions=1)
        self.assertEqual(actions[0]['des_order'], 2)
        self.assertEqual(actions[0]['damage_list'][:2], [0, 500])
        self.assertEqual(actions.final_hp[2], {1: 880, 2: 0})
        self.assertEqual(engine.total_damage(actions), 620)
        self.assert_hp_replay(battle)

    def test_aoe_sharing_and_revival_are_not_double_counted_in_native_replay(self):
        battle, (_, _, actions) = self.battle(
            ([unit(gongji=10000, magic=10000, skills=[(101, 1)], skill_probabilities={101: 100})],
             [unit(), unit(2, hp=10, skills=[(21, 10)], essences={19: (100, 50)})]), max_actions=1)
        self.assertEqual(actions[0]['damage_list'][1], 0)
        self.assertEqual(actions.final_hp[2][2], 500)
        self.assertEqual([event['logic_type'] for event in actions.events], [101201, 101191])
        self.assertEqual(engine.total_damage(actions), 1010)
        self.assert_hp_replay(battle)

    def test_seeded_mixed_effects_preserve_hp_inputs_and_outcome_invariants(self):
        rng = random.Random(4567)
        effects = {3: (60, 50), 5: (50,), 7: (50, 50), 10: (40, 10),
                   13: (20,), 16: (30, 5), 18: (40, 10), 19: (40, 20)}
        for case in range(24):
            slots = 8 if case % 2 == 0 else 9
            sides = []
            for _ in (1, 2):
                army = []
                for order in range(1, slots + 1):
                    if rng.randrange(5) == 0:
                        continue
                    hp = rng.randrange(500, 5000)
                    chosen = {kind: values for kind, values in effects.items() if rng.randrange(3) == 0}
                    army.append(unit(order, hp=hp, max_hp=hp, gongji=rng.randrange(30, 500),
                                     fangyu=rng.randrange(200), magic=rng.randrange(500),
                                     skills=[(101, 1), (21, 10)], essences=chosen))
                sides.append(army)
            original = copy.deepcopy(sides)
            with self.subTest(case=case, slots=slots), patch('network_redirect.combat.secrets.randbelow', side_effect=rng.randrange):
                battle, (result, _, actions) = self.battle(sides, slots=slots)
                self.assertEqual(sides, original)
                self.assertLessEqual(actions.rounds, 30)
                self.assert_hp_replay(battle)
                if 1 <= result <= 3:
                    self.assertGreater(sum(actions.final_hp[1].values()), sum(actions.final_hp[2].values()))
                elif 4 <= result <= 6:
                    self.assertLess(sum(actions.final_hp[1].values()), sum(actions.final_hp[2].values()))
