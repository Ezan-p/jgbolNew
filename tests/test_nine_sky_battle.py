"""Real encounter combat, NPC rotation, scaling and reward boundaries."""
import copy
import unittest
from unittest.mock import patch

from network_redirect import nine_sky_battle as battle, npc_players


RULES = dict(
    battle_floor_power=[3000, 6000, 12000, 22000, 38000, 65000, 105000, 160000, 240000],
    battle_pool=[
        dict(weight=25, reward=[5, 1031, 5, 1]),
        dict(weight=20, reward=[5, 6002, 5, 1]),
        dict(weight=20, reward=[5, 6003, 5, 1]),
        dict(weight=15, reward=[5, 6004, 5, 1]),
        dict(weight=15, reward=[1, -1, 1, 100]),
        dict(weight=5, reward=[5, 1246, 1, 1]),
    ],
)


class NineSkyBattleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.key = min(battle.catalog(), key=lambda k: battle.catalog()[k]['profile']['role_combat_power'])

    def role(self, stat):
        role = npc_players.get(self.key)['role']
        role['attachments'] = []
        role['activity'] = {}
        role['spirit_array'] = {}
        for companion in role['corteges']:
            for name in battle.formation.STATS:
                companion[name] = stat
        return role

    def test_all_weekly_opponents_are_used_before_any_repeat(self):
        state = {}
        # Choosing alone exercises the complete rotation without expensive
        # combat or loading 1700 full loadouts.
        size = len(battle.catalog())
        with patch.object(battle.secrets, 'choice', side_effect=lambda rows: rows[0]):
            selected = [battle.choose(state, RULES['battle_floor_power'][i % 9])
                        for i in range(size)]
            self.assertEqual(len(set(selected)), size)
            last = selected[-1]
            following = battle.choose(state, 3000)
        self.assertNotEqual(following, last)
        self.assertEqual(state['battle_cycles'], 1)
        self.assertEqual(state['battle_seen'], [following])

    def test_restart_history_and_account_isolation(self):
        first = {}
        with patch.object(battle.secrets, 'choice', side_effect=lambda rows: rows[0]):
            key = battle.choose(first, 3000)
            restored = copy.deepcopy(first)
            second = battle.choose(restored, 3000)
            unrelated = battle.choose({}, 3000)
        self.assertNotEqual(key, second)
        self.assertEqual(unrelated, key)
        self.assertEqual(first['battle_seen'], [key])

    def test_every_sky_scales_all_stats_without_mutating_template(self):
        original = copy.deepcopy(battle.template(self.key))
        previous = None
        for floor, target in enumerate(RULES['battle_floor_power'], 1):
            units, power = battle.enemies(self.key, floor, RULES)
            self.assertLess(abs(power - target), target // 100 + 32)
            self.assertEqual([u['type'] for u in units], [u['type'] for u in original])
            self.assertEqual([u['skills'] for u in units], [u['skills'] for u in original])
            for index, unit in enumerate(units):
                self.assertEqual(unit['hp'], unit['max_hp'])
                if previous:
                    for stat in battle.formation.STATS:
                        self.assertGreater(unit[stat], previous[index][stat])
            previous = units
        self.assertEqual(battle.template(self.key), original)
        previous[0]['hp'] = 0
        self.assertEqual(battle.template(self.key), original)

    def test_real_victory_selects_one_reward_without_granting_it(self):
        role = self.role(1000000)
        original = copy.deepcopy(role)
        state = dict(floor=1)
        with patch.object(battle.secrets, 'choice', side_effect=lambda rows: rows[0]), \
                patch.object(battle.secrets, 'randbelow', return_value=99):
            record, reward = battle.encounter(role, state, RULES)
        self.assertTrue(record['won'])
        self.assertIn(record['result'], (1, 2, 3))
        self.assertGreater(record['rounds'], 0)
        self.assertEqual(reward, [5, 1246, 1, 1])
        self.assertEqual(state['battle_count'], 1)
        self.assertEqual(state['battle_wins'], 1)
        self.assertEqual(record['enemy_count'], len(record['enemy_types']))
        self.assertEqual(role, original)

    def test_real_defeat_has_no_reward_and_does_not_mutate_progress(self):
        role = self.role(1)
        original = copy.deepcopy(role)
        state = dict(floor=9, steps=1000, stars=321, cur_point=dict(x=0, y=60))
        with patch.object(battle.secrets, 'choice', side_effect=lambda rows: rows[0]):
            record, reward = battle.encounter(role, state, RULES)
        self.assertFalse(record['won'])
        self.assertIsNone(reward)
        self.assertEqual((state['floor'], state['steps'], state['stars']), (9, 1000, 321))
        self.assertEqual(state['cur_point'], dict(x=0, y=60))
        self.assertEqual(state['battle_wins'], 0)
        self.assertEqual(role, original)

    def test_encounter_uses_supplied_pre_portal_floor(self):
        role = self.role(1)
        state = dict(floor=2)
        with patch.object(battle.secrets, 'choice', side_effect=lambda rows: rows[0]):
            record, _ = battle.encounter(role, state, RULES, floor=1)
        self.assertEqual((record['floor'], record['target_power']), (1, 3000))
        self.assertEqual(state['floor'], 2)

    def test_empty_player_formation_settles_as_defeat(self):
        role = dict(corteges=[], attachments=[], activity={}, level=1)
        with patch.object(battle.secrets, 'choice', side_effect=lambda rows: rows[0]):
            record, reward = battle.encounter(role, dict(floor=1), RULES)
        self.assertFalse(record['won'])
        self.assertEqual(record['rounds'], 0)
        self.assertIsNone(reward)

    def test_reward_probability_boundaries_cover_each_bucket(self):
        start = 0
        for row in RULES['battle_pool']:
            for pick in (start, start + row['weight'] - 1):
                with patch.object(battle.secrets, 'randbelow', return_value=pick):
                    self.assertEqual(battle.reward(RULES), row['reward'])
            start += row['weight']
        self.assertEqual(start, 100)


if __name__ == '__main__':
    unittest.main()
