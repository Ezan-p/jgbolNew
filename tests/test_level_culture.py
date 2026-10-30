"""Configured level potential across acquisition paths and legacy persistence."""
import copy
import unittest
from unittest.mock import patch

from network_redirect import formation as f, journey, summon
from network_redirect.protocol import decode
from tests import test_formation

RATES = {1: (1, 2), 2: (3, 4), 3: (5, 7), 4: (7, 10), 5: (10, 15)}


def earned(quality, old, new):
    early, late = RATES[quality]
    return sum(early if level <= 40 else late for level in range(old + 1, new + 1))


class LevelCultureTests(unittest.TestCase):
    def setUp(self):
        self.rules = f.load_rules()
        self.role = dict(level=80, summon={}, attachments=[], corteges=[])
        self.c = summon.companion(self.role, 5004)
        self.c.update(culture_point=0, cur_exp=0, order=1)
        self.role['corteges'] = [self.c]
        f.prepare(self.role, self.rules)

    def test_quality_rates_and_level_40_boundary(self):
        for quality, (early, late) in RATES.items():
            self.assertEqual(f.level_culture_points(quality, 1, 1), 0)
            self.assertEqual(f.level_culture_points(quality, 1, 4), 3 * early)
            self.assertEqual(f.level_culture_points(quality, 39, 40), early)
            self.assertEqual(f.level_culture_points(quality, 40, 41), late)
            self.assertEqual(f.level_culture_points(quality, 39, 42), early + 2 * late)
            self.assertEqual(f.level_culture_points(quality, 119, 121), 2 * late)
            self.assertEqual(f.level_culture_points(quality, 1, 200), 39 * early + 160 * late)
            self.assertEqual(f.level_culture_points(quality, 41, 1), 0)

    def test_books_and_pills_award_each_reached_level(self):
        for quality in range(1, 6):
            for flag, subtype in ((1, 99), (2, 100)):
                with self.subTest(quality=quality, flag=flag):
                    role = copy.deepcopy(self.role)
                    c = role['corteges'][0]
                    c['type'] = next(t for t, row in f.BASES.items() if int(row['quality']) == quality)
                    tid = next(t for t, row in f.ITEMS.items() if int(row['main_type']) == 5
                               and int(row['sub_type']) == subtype and int(row['experience_plus']) > 0)
                    summon.add_item(role, tid, 1)
                    f.feed(role, dict(flag=flag, first_send=True, cortege_id=c['id'], roll_count=1,
                                     roll_list=[dict(type_id=tid, count=1)]), self.rules)
                    self.assertGreater(c['level'], 1)
                    self.assertEqual(c['culture_point'], earned(quality, 1, c['level']))

    def test_battle_and_inheritance_match_book_rewards(self):
        xp = sum(f.EXPERIENCE[5, n] for n in range(1, 4))
        self.role['silver_coin'] = 0
        with patch('network_redirect.progression.add_exp'), patch('network_redirect.progression.strength_bonus', return_value=(0, 0)):
            journey.experience(self.role, dict(strenth_consume='0', exp=str(xp), money='0'), True,
                               journey.load_rules(), self.rules)
        self.assertEqual((self.c['level'], self.c['culture_point']), (4, 30))
        dst = summon.companion(self.role, 5002)
        dst.update(culture_point=0, cur_exp=0)
        self.role['corteges'].append(dst)
        f.prepare(self.role, self.rules)
        summon.add_item(self.role, 1002, 1)
        f.impart(self.role, dict(src_id=self.c['id'], des_id=dst['id']), self.rules)
        self.assertEqual((dst['level'], dst['culture_point']), (4, 30))
        self.assertEqual((self.c['level'], self.c['culture_point']), (1, 0))
        f.prepare(self.role, self.rules)
        self.assertEqual(self.c['culture_point'], 0)

    def test_old_save_topup_preserves_training_and_other_rewards_once(self):
        self.c.pop('level_culture_version')
        self.c.update(level=4, culture_point=15 - 7 + 30, hp_plus=7,
                      evolve_level=1, reborn_layer=0, cur_exp=12)
        before = copy.deepcopy(self.c)
        f.migrate_level_culture(self.c)
        self.assertEqual(self.c['culture_point'], 30 - 7 + 30)
        for key in ('hp_plus', 'cur_exp', 'evolve_level', 'reborn_layer', 'id'):
            self.assertEqual(self.c[key], before[key])
        migrated = copy.deepcopy(self.c)
        f.migrate_level_culture(self.c)
        self.assertEqual(self.c, migrated)

    def test_all_old_versions_normalize_budget_once(self):
        for version in (0, 1, 2):
            for quality in range(1, 6):
                for level in (1, 39, 40, 41, 200):
                    for available, trained in ((20000, 7), (3, 20000), (0, 0)):
                        with self.subTest(version=version, quality=quality, level=level,
                                          available=available, trained=trained):
                            c = copy.deepcopy(self.c)
                            c.update(type=next(t for t, row in f.BASES.items() if int(row['quality']) == quality),
                                     level=level, level_culture_version=version,
                                     culture_point=available, hp_plus=trained, cur_exp=12,
                                     pending_training=dict(points=3), evolve_level=0, reborn_layer=0)
                            f.migrate_level_culture(c)
                            expected = earned(quality, 1, level)
                            self.assertEqual(c['level_culture_version'], 3)
                            self.assertEqual(c['culture_point'], max(0, expected - trained))
                            self.assertEqual(c['hp_plus'], min(expected, trained))
                            self.assertEqual(c['pending_training'], dict(points=3))
                            self.assertEqual(c['cur_exp'], 12)
                            audit = c['level_culture_migration']
                            self.assertEqual(audit['previous_available'], available)
                            self.assertEqual(audit['previous_training']['hp'], trained)
                            self.assertEqual(audit['total_adjustment'], expected - available - trained)
                            migrated = copy.deepcopy(c)
                            f.migrate_level_culture(c)
                            self.assertEqual(c, migrated)

    def test_proportional_training_reduction_and_integer_remainders(self):
        self.c.update(level=5, level_culture_version=2, culture_point=10,
                      hp_plus=100, gongji_plus=60, fangyu_plus=30, magic_plus=10)
        f.migrate_level_culture(self.c)
        self.assertEqual(self.c['culture_point'], 0)
        self.assertEqual([self.c[s + '_plus'] for s in f.STATS], [20, 12, 6, 2])
        self.c.update(type=next(t for t, row in f.BASES.items() if int(row['quality']) == 1),
                      level=4, level_culture_version=1,
                      hp_plus=1, gongji_plus=1, fangyu_plus=1, magic_plus=1)
        f.migrate_level_culture(self.c)
        self.assertEqual([self.c[s + '_plus'] for s in f.STATS], [1, 1, 1, 0])

    def test_rebirth_and_evolution_budget_is_preserved(self):
        self.c.update(level=155, level_culture_version=1, culture_point=10000,
                      hp_plus=1000, gongji_plus=500, fangyu_plus=300, magic_plus=200,
                      evolve_level=2, reborn_layer=1, reborn_vein_level=4)
        f.migrate_level_culture(self.c)
        # 39*10 + 115*15 current level, 10*15 previous cycle, 150 rebirth, 30+40 evolution.
        self.assertEqual(self.c['level_culture_migration']['budget'],
                         dict(ordinary=2115, rebirth_cycles=150, evolution=70, rebirth=150))
        self.assertEqual(self.c['culture_point'], 485)
        self.assertEqual([self.c[s + '_plus'] for s in f.STATS], [1000, 500, 300, 200])
        self.assertEqual((self.c['evolve_level'], self.c['reborn_layer'], self.c['reborn_vein_level']), (2, 1, 4))

    def test_current_version_is_not_rebalanced_on_each_load(self):
        self.c.update(level=4, culture_point=999, hp_plus=30)
        before = copy.deepcopy(self.c)
        f.migrate_level_culture(self.c)
        self.assertEqual(self.c, before)

    def test_books_and_pills_cross_level_40_for_every_quality(self):
        for quality in RATES:
            for flag, subtype in ((1, 99), (2, 100)):
                with self.subTest(quality=quality, flag=flag):
                    role = copy.deepcopy(self.role)
                    c = role['corteges'][0]
                    c.update(type=next(t for t, row in f.BASES.items() if int(row['quality']) == quality),
                             level=39, culture_point=17)
                    tid = next(t for t, row in f.ITEMS.items() if int(row['main_type']) == 5
                               and int(row['sub_type']) == subtype and int(row['experience_plus']) > 0)
                    xp = sum(f.EXPERIENCE[quality, n] for n in (39, 40, 41))
                    value = int(f.ITEMS[tid]['experience_plus'])
                    count = (xp + value - 1) // value
                    summon.add_item(role, tid, count)
                    f.feed(role, dict(flag=flag, first_send=True, cortege_id=c['id'], roll_count=1,
                                     roll_list=[dict(type_id=tid, count=count)]), self.rules)
                    self.assertGreaterEqual(c['level'], 42)
                    self.assertEqual(c['culture_point'], 17 + earned(quality, 39, c['level']))

    def test_battle_crosses_level_40_for_every_quality(self):
        for quality in RATES:
            with self.subTest(quality=quality):
                role = copy.deepcopy(self.role)
                role['silver_coin'] = 0
                c = role['corteges'][0]
                c.update(type=next(t for t, row in f.BASES.items() if int(row['quality']) == quality),
                         level=39, culture_point=17)
                xp = sum(f.EXPERIENCE[quality, n] for n in (39, 40, 41))
                with patch('network_redirect.progression.add_exp'), patch(
                        'network_redirect.progression.strength_bonus', return_value=(0, 0)):
                    journey.experience(role, dict(strenth_consume='0', exp=str(xp), money='0'),
                                       True, journey.load_rules(), self.rules)
                self.assertEqual((c['level'], c['culture_point']), (42, 17 + earned(quality, 39, 42)))

    def test_inheritance_uses_recipient_quality_across_level_40(self):
        for quality in RATES:
            with self.subTest(quality=quality):
                role = copy.deepcopy(self.role)
                src = role['corteges'][0]
                src.update(level=50, culture_point=900)
                tid = next(t for t, row in f.BASES.items() if int(row['quality']) == quality)
                dst = summon.companion(role, tid)
                dst.update(level=39, culture_point=17, cur_exp=0)
                role['corteges'].append(dst)
                f.prepare(role, self.rules)
                summon.add_item(role, 1002, 1)
                f.impart(role, dict(src_id=src['id'], des_id=dst['id']), self.rules)
                self.assertGreater(dst['level'], 40)
                self.assertEqual(dst['culture_point'], 17 + earned(quality, 39, dst['level']))
                self.assertEqual((src['level'], src['culture_point']), (1, 0))


class LevelCultureWireTests(unittest.TestCase):
    setUp = test_formation.FormationTests.setUp
    request = test_formation.FormationTests.request
    events = test_formation.FormationTests.events
    ok = test_formation.FormationTests.ok

    def test_large_potential_snapshot_and_training_keep_full_balance(self):
        role = self.backend.profile()
        c = role['corteges'][0]
        c.update(level=200, culture_point=80000)
        summon.add_item(role, 1343, 1)
        self.backend.save(role)
        packets = [decode(p) for p in self.backend.inventory(role)]
        roster = next(d for mid, _, d in packets if mid == 1034)
        self.assertEqual(roster['cortege_list'][0]['culture_point'], 65535)
        full = next(d for mid, _, d in packets if mid == 1032 and d['id'] == c['id'])
        self.assertEqual(full['attr_list'], [dict(type=90, value=80000)])
        self.assertEqual(self.backend.profile()['corteges'][0]['culture_point'], 80000)
        self.ok(1089, cortege_id=c['id'], train_point=5, train_field=1)
        self.assertEqual(self.backend.profile()['corteges'][0]['culture_point'], 79995)

    def test_legacy_migration_persists_without_double_credit(self):
        role = self.backend.profile()
        c = role['corteges'][0]
        c.pop('level_culture_version')
        c.update(level=4, culture_point=8, hp_plus=7)
        self.backend.save(role)
        first = self.backend.profile()['corteges'][0]
        self.assertEqual(first['culture_point'], 23)
        second = self.backend.profile()['corteges'][0]
        self.assertEqual(second, first)

    def test_version_one_migration_debits_and_recalculates_on_repeated_loads(self):
        role = self.backend.profile()
        c = role['corteges'][0]
        c.update(level=41, culture_point=6000, hp_plus=500, level_culture_version=1)
        self.backend.save(role)
        first = self.backend.profile()['corteges'][0]
        self.assertEqual((first['culture_point'], first['hp_plus'], first['level_culture_version']),
                         (0, 405, 3))
        before_hp = first['hp']
        f.recalculate(role, self.backend.formation_rules)
        self.assertEqual(role['corteges'][0]['hp'] - before_hp, 95)
        self.assertEqual(self.backend.profile()['corteges'][0], first)

    def test_pending_training_cannot_spend_clawed_back_points(self):
        role = self.backend.profile()
        c = role['corteges'][0]
        c.update(level=4, level_culture_version=2, culture_point=500, hp_plus=100,
                 pending_training=dict(points=3, deltas=dict(hp=3, gongji=0, fangyu=0, magic=0)),
                 train_increase_field=86, train_decrease_field=90, train_change_value=3)
        self.backend.save(role)
        migrated = self.backend.profile()['corteges'][0]
        self.assertEqual((migrated['culture_point'], migrated['hp_plus']), (0, 30))
        response = self.request(1082, cortege_id=c['id'], confirm=True)
        self.assertIn(55, [event for event, _ in self.events(response)])
        self.assertEqual(self.backend.profile()['corteges'][0], migrated)
        self.ok(1082, cortege_id=c['id'], confirm=False)
        self.assertNotIn('pending_training', self.backend.profile()['corteges'][0])
