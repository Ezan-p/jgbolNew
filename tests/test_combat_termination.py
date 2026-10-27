"""Fight completion is independent of transport size and victory labels."""
import copy
import unittest
from unittest.mock import patch

from network_redirect import combat_engine as engine, journey


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
            for order, hit in enumerate(action['damage_list'], 1):
                if hit:
                    hp[target_side, order] -= hit
                    self.assertGreaterEqual(hp[target_side, order], 0)
            for event in events.get(index, []):
                for change in event['skill_result_list']:
                    if change['field'] == 65:
                        hp[event['who_use'], change['des_order']] += change['field_plus']
        self.assertEqual(hp, {(side, order): value for side, units in battle.actions.final_hp.items()
                              for order, value in units.items()})

    def test_lifesteal_can_finish_beyond_both_old_event_budgets(self):
        sides = ([unit(hp=10000, max_hp=10000, gongji=150, essences={5: (50,)})],
                 [unit(hp=10000, max_hp=10000, essences={5: (50,)})])
        outcomes = []
        for budget in (1000, 12000):
            battle, (result, _, actions) = self.battle(sides, budget)
            self.assertGreater(battle.event_bytes, 12000)
            self.assertEqual(actions.stop_reason, 'elimination')
            self.assertEqual(actions.final_hp[2][1], 0)
            self.assertEqual(result, 3)
            self.assert_hp_replay(battle)
            outcomes.append((result, actions, actions.events, actions.final_hp))
        self.assertEqual(outcomes[0], outcomes[1])

    def test_round_healing_finishes_with_all_events_past_12000_bytes(self):
        sides = ([unit(hp=10000, max_hp=10000, gongji=150, essences={10: (100, 10)})],
                 [unit(hp=10000, max_hp=10000)])
        battle, (result, _, actions) = self.battle(sides)
        self.assertGreater(battle.event_bytes, 12000)
        self.assertEqual(actions.stop_reason, 'elimination')
        self.assertEqual(result, 3)
        self.assertEqual(actions.final_hp[2][1], 0)
        self.assert_hp_replay(battle)

    def test_endless_sustain_stops_at_action_limit_as_unresolved(self):
        sides = ([unit(essences={5: (100,)})], [unit(essences={5: (100,)})])
        battle, (result, _, actions) = self.battle(sides)
        self.assertEqual(len(actions), self.rules['battle']['max_actions'])
        self.assertEqual(actions.stop_reason, 'action_limit')
        self.assertEqual(result, 0)
        self.assertTrue(all(hp > 0 for side in actions.final_hp.values() for hp in side.values()))
        self.assert_hp_replay(battle)

    def test_zero_action_limit_is_respected_without_guessing_a_winner(self):
        _, (result, _, actions) = self.battle(([unit()], [unit()]), max_actions=0)
        self.assertEqual((result, len(actions), actions.stop_reason), (0, 0, 'action_limit'))
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
