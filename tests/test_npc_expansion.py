"""Design generation invariants against real tables, without a player database."""
import copy
import math
import unittest
from analysis.tools import build_npc_expansion as e


class NpcExpansionTests(unittest.TestCase):
    def test_seed_reproducibility_and_stream_independence(self):
        a = e.generate(36, 'T3', 'magic', set())
        e.generate(7, 'T4', 'attack', set())
        b = e.generate(36, 'T3', 'magic', set())
        self.assertEqual(a, b)
        self.assertNotEqual(e.seed_for(36, 'T3', 'magic', 0), e.seed_for(36, 'T3', 'magic', 1))

    def test_tiers_quotas_and_realm_prerequisites_at_boundaries(self):
        seen = set()
        for level in (1, 18, 36, 60, 70, 80, 90, 99):
            for tier in e.base.TIERS:
                with self.subTest(level=level, tier=tier):
                    n = e.generate(level, tier, 'attack', seen)
                    e.base.validate(n)
                    power = n['role']['role_combat_power']
                    self.assertGreaterEqual(power, n['power_range']['minimum'])
                    self.assertLessEqual(power, n['generation_ceiling'])
                    team = [c for c in n['role']['corteges'] if c['order']]
                    self.assertGreaterEqual(sum(e.base.quality(c['type']) == 5 for c in team),
                                            math.ceil(len(team) * e.CONFIG['five_star_min_ratio'][tier]))

    def test_repeated_composition_resamples_not_just_positions(self):
        n = e.generate(24, 'T3', 'attack', set())
        newer = e.generate(24, 'T3', 'attack', {e.signature(n)})
        self.assertNotEqual(e.signature(n), e.signature(newer))
        self.assertGreater(newer['roster_attempt'], n['roster_attempt'])

    def test_scale_does_not_modify_input_or_inject_panel_boost(self):
        original = e.candidate(99, 'T1', 'magic', 0)
        snapshot = copy.deepcopy(original)
        n = e.scaled(original, 20)
        e.base.validate(n)
        self.assertEqual(original, snapshot)
        self.assertFalse(n['role'].get('combat_sources'))
        self.assertTrue(all(not c.get('combat_sources') for c in n['role']['corteges']))

    def test_bad_potential_and_duplicate_lineup_rejected(self):
        n = e.generate(36, 'T3', 'attack', set())
        altered = copy.deepcopy(n)
        altered['role']['corteges'][0]['culture_point'] += 1
        with self.assertRaises(AssertionError):
            e.base.validate(altered)
        altered = copy.deepcopy(n)
        altered['role']['corteges'][1]['type'] = altered['role']['corteges'][0]['type']
        with self.assertRaises(AssertionError):
            e.base.validate(altered)


if __name__ == '__main__':
    unittest.main()
