import copy
import unittest
from collections import Counter
from unittest.mock import patch
from network_redirect import duty_balance as b, npc_players, formation


class BalanceTests(unittest.TestCase):
    def test_exact_weighted_distribution_and_boundaries(self):
        for key in ('bonus_tiers', 'drops'):
            rows = b.rules()[key]
            total = sum(row['weight'] for row in rows)
            with patch.object(b.secrets, 'randbelow', side_effect=range(total)):
                actual = Counter(rows.index(b.weighted(rows)) for _ in range(total))
            self.assertEqual(actual, {i: row['weight'] for i, row in enumerate(rows)})

    def test_guard_positions_and_reward_pool(self):
        with patch.object(b.secrets, 'randbelow', side_effect=[0, 0, 1, 600, 2, 999]):
            results = [b.guard_reward(7) for _ in range(3)]
        self.assertEqual([r['difficulty'] for r in results], [1, 2, 3])
        self.assertEqual([r['round'] for r in results], [7]*3)
        self.assertEqual([r['reward'] for r in results], [[12, 0, 3000, 1], [11, 0, 20, 1], [5, 1031, 1, 1]])
        self.assertEqual([r['reward'] for r in b.rules()['drops']], [
            [12, 0, 3000, 1], [11, 0, 20, 1], [5, 1034, 1, 1],
            [5, 1033, 1, 1], [5, 1032, 1, 1], [5, 1031, 1, 1]])

    def test_every_group_and_stage_difficulty_and_stable_schedule(self):
        for group in range(4, 9):
            previous = [0, 0, 0]
            selected = set()
            for stage in range(1, 121):
                p = b.stage(group, stage)
                selected.add(p['npc_id'])
                self.assertEqual(p['targets'], sorted(set(p['targets'])))
                self.assertTrue(all(a < c for a, c in zip(previous, p['targets'])))
                previous = p['targets']
                self.assertIn(p['npc_id'], npc_players.catalog())
                self.assertEqual(b.stage(group, stage), p)
                self.assertEqual(len(set(p['guard_types'])), 3)
                resources = [int(formation.BASES[t]['resource']) for t in p['guard_types']]
                self.assertEqual(len(set(resources)), 3)
                armies = [b.enemies(group, stage, d) for d in (1, 2, 3)]
                self.assertTrue(set(p['guard_types']).issubset({u['type'] for u in armies[0]}))
                for easy, normal, hard in zip(*armies):
                    self.assertEqual(easy['type'], normal['type'])
                    self.assertEqual(normal['type'], hard['type'])
                    self.assertTrue(all(easy[s] < normal[s] < hard[s] for s in formation.STATS),
                                    (group, stage, easy['type']))
            self.assertGreater(len(selected), 20)

    def test_complete_lineups_scaling_traits_and_no_source_mutation(self):
        for group in range(4, 9):
            for number in (1, 30, 60, 100, 120):
                plan = b.stage(group, number)
                original = copy.deepcopy(b.template(plan['npc_id']))
                enemies = [b.enemies(group, number, difficulty) for difficulty in (1, 2, 3)]
                for army in enemies:
                    self.assertEqual(len(army), group)
                    self.assertEqual(sorted(u['order'] for u in army), list(range(1, group+1)))
                    for u, template in zip(army, original):
                        self.assertEqual(u['skills'], template['skills'])
                        self.assertEqual(u['max_hp'], u['hp'])
                        for key in set(template)-set(formation.STATS)-{'max_hp'}:
                            self.assertEqual(u[key], template[key])
                for easy, normal, hard in zip(*enemies):
                    self.assertTrue(all(easy[s] < normal[s] < hard[s] for s in formation.STATS))
                enemies[0][0]['hp'] = 1
                self.assertEqual(b.template(plan['npc_id']), original)

    def test_three_sets_distinct_complete_equal_curve_and_immutable(self):
        for group in range(4, 9):
            for number in range(1, 121):
                plans = [b.stage(group, number, variant) for variant in range(3)]
                self.assertEqual(len({p['npc_id'] for p in plans}), 3)
                self.assertEqual(len({p['archetype'] for p in plans}), 1)
                self.assertTrue(all(p['targets'] == plans[0]['targets'] for p in plans))
                signatures = []
                for variant, plan in enumerate(plans):
                    original = copy.deepcopy(b.template(plan['npc_id']))
                    signatures.append(tuple(u['type'] for u in original))
                    armies = [b.enemies(group, number, diff, variant) for diff in (1, 2, 3)]
                    for army in armies:
                        self.assertEqual(len(army), group)
                        self.assertEqual(sorted(u['order'] for u in army), list(range(1, group+1)))
                        self.assertTrue(set(plan['guard_types']).issubset({u['type'] for u in army}))
                        for unit, source in zip(army, original):
                            for key in set(source)-set(formation.STATS)-{'max_hp'}:
                                self.assertEqual(unit[key], source[key])
                            self.assertEqual(unit['hp'], unit['max_hp'])
                    for easy, normal, hard in zip(*armies):
                        self.assertTrue(all(easy[k] < normal[k] < hard[k] for k in formation.STATS))
                    armies[0][0]['hp'] = 1
                    self.assertEqual(b.template(plan['npc_id']), original)
                self.assertEqual(len(set(signatures)), 3)

    def test_enemy_set_draw_and_no_consecutive_repeat(self):
        with patch.object(b.secrets, 'randbelow', side_effect=[0, 1, 2]):
            self.assertEqual([b.choose_enemy_set() for _ in range(3)], [0, 1, 2])
        for previous in range(3):
            with patch.object(b.secrets, 'randbelow', side_effect=[0, 1]):
                self.assertEqual({b.choose_enemy_set(previous) for _ in range(2)}, set(range(3))-{previous})

    def test_high_round_is_bounded_without_numeric_overflow(self):
        self.assertEqual(b.stage(8, 1000000)['base_power'], b.rules()['power_ceiling'])
