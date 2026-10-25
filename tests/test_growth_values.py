"""Exhaustive growth boundaries and original coefficient arithmetic."""
import copy
from decimal import Decimal
import unittest

from network_redirect import formation as f, reborn, summon


class GrowthValueTests(unittest.TestCase):
    def test_all_evolution_levels_and_qualities(self):
        rules = f.load_rules()
        for quality in range(1, 6):
            tid = next(t for t, row in f.BASES.items() if int(row['quality']) == quality)
            role = dict(level=99, summon={}, attachments=[], corteges=[], souls={str(tid): sum(f.EVOLVE_COST.values())})
            c = summon.companion(role, tid)
            c['culture_point'] = 0
            role['corteges'] = [c]
            f.recalculate(role, rules)
            base = {s: c[s] for s in f.STATS}
            gain = {s: int(Decimal(f.BASES[tid][g]) * 3) for s, g in zip(f.STATS, f.GROWTH_COLUMNS)}
            potential = c['culture_point']
            for level in range(1, 300):
                with self.subTest(quality=quality, evolution=level):
                    f.evolve(role, dict(flag=0, cortege_id=c['id']))
                    f.recalculate(role, rules)
                    potential += f.EVOLVE_POINTS[quality, level]
                    self.assertEqual(c['culture_point'], potential)
                    self.assertEqual({s: c[s] for s in f.STATS}, {s: base[s] + gain[s] * level for s in f.STATS})
            self.assertEqual(role['souls'][str(tid)], 0)
            before = copy.deepcopy(role)
            with self.assertRaises(f.Rejected):
                f.evolve(role, dict(flag=0, cortege_id=c['id']))
            self.assertEqual(role, before)

    def test_every_companion_uses_floor_before_multiplication(self):
        rules = f.load_rules()
        for tid, row in f.BASES.items():
            role = dict(level=99, summon={}, attachments=[], corteges=[])
            c = summon.companion(role, tid)
            c.update(evolve_level=7, level=17)
            role['corteges'] = [c]
            f.recalculate(role, rules)
            for s, b, g in zip(f.STATS, f.BASE_COLUMNS, f.GROWTH_COLUMNS):
                expected = int(Decimal(row[b]) + Decimal(row[g]) * 16 + int(Decimal(row[g]) * 3) * 7)
                self.assertEqual(c[s], expected, (tid, s))
            before = copy.deepcopy(role)
            f.recalculate(role, rules)
            self.assertEqual(role, before)

    def test_all_rebirth_directions_layers_and_veins(self):
        # Independent arithmetic from the original tables: percentages add,
        # completed veins and direction entries accumulate exactly once.
        for direction in (1, 2, 3):
            for layer in range(10):
                for vein in range(10 if layer < 9 else 1):
                    c = dict(reborn_layer=layer, reborn_vein_level=vein, reborn_plus_type=direction)
                    values = {s: Decimal(1000) for s in f.STATS}
                    expected = {s: Decimal(1000) + 25 * layer for s in f.STATS}
                    texts = [row['plus_list'] for row in summon.rows('cortege_reborn_effect.csv')
                             if int(row['effect_type']) == direction and int(row['layer']) <= layer]
                    texts += [row['effect_list(1=gongji|2=fangyu|3=hp|4=fa)']
                              for row in summon.rows('cortege_reborn_vein.csv')
                              if int(row['layer']) <= layer or
                              (int(row['layer']) == layer + 1 and int(row['pulse']) <= vein)]
                    for text in texts:
                        for part in text.split('/'):
                            stat, amount = part.split('|')
                            expected[{1:'gongji', 2:'fangyu', 3:'hp', 4:'magic'}[int(stat)]] += Decimal(amount)
                    reborn.bonuses({}, c, values, [])
                    self.assertEqual(values, expected, (direction, layer, vein))

    def test_evolution_survives_rebirth_and_direction_round_trip(self):
        role = dict(level=99, summon={}, attachments=[], corteges=[])
        c = summon.companion(role, 5022)
        c.update(level=170, evolve_level=12, reborn_layer=3, reborn_plus_type=1)
        role['corteges'] = [c]
        rules = f.load_rules()
        f.recalculate(role, rules)
        initial = {s: c[s] for s in f.STATS}
        c['reborn_plus_type'] = 2
        f.recalculate(role, rules)
        self.assertNotEqual({s: c[s] for s in f.STATS}, initial)
        c['reborn_plus_type'] = 1
        f.recalculate(role, rules)
        self.assertEqual({s: c[s] for s in f.STATS}, initial)
        c['evolve_level'] = 0
        f.recalculate(role, rules)
        self.assertTrue(all(c[s] < initial[s] for s in f.STATS))
