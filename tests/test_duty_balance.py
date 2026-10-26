import copy
import unittest
from collections import Counter
from unittest.mock import patch
from network_redirect import duty_balance as b, npc_players, formation


class BalanceTests(unittest.TestCase):
    def test_exact_weighted_distribution_and_boundaries(self):
        for key in ('bonus_tiers', 'drops'):
            rows = b.rules()[key]
            with patch.object(b.secrets, 'randbelow', side_effect=range(100)):
                actual = Counter(rows.index(b.weighted(rows)) for _ in range(100))
            self.assertEqual(actual, {i: row['weight'] for i, row in enumerate(rows)})

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

    def test_high_round_is_bounded_without_numeric_overflow(self):
        self.assertEqual(b.stage(8, 1000000)['base_power'], b.rules()['power_ceiling'])
