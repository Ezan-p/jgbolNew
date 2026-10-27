"""Equipped essence identity and timing boundaries against real inventory data."""
import copy
import random
import unittest
from fractions import Fraction
from unittest.mock import patch

from network_redirect import combat, combat_engine, combat_power, journey


def unit(order=1, **values):
    return dict(dict(type=1001, order=order, level=1, evolve=0, reborn=0,
                     hp=1000, max_hp=1000, gongji=100, fangyu=0, magic=0,
                     skills=[]), **values)


class EssenceInventoryTests(unittest.TestCase):
    def setUp(self):
        self.role = dict(corteges=[dict(id=7, type=1001, order=1, equiped_ext_skill_limit=4)],
                         attachments=[])

    def engrave(self, kind, level=1, slot=1, **values):
        self.role['attachments'].append(dict(dict(id=len(self.role['attachments']) + 20,
            type_id=kind, level=level, ext_skill_pos=slot, count=1, attach_type=5,
            owner_id=7), **values))

    def attached(self, order=1):
        fighter = unit(order, companion_id=7)
        combat.attach_essences(self.role, [fighter])
        return fighter

    def test_inventory_or_invalid_engraving_cannot_change_damage(self):
        self.engrave(10211, count=0)
        self.engrave(10208, level=0)
        self.engrave(10219, level=6)
        self.engrave(10213, slot=5)
        self.engrave(10206, slot=0)
        self.engrave(10205, owner_id=8)
        fighter = self.attached()
        self.assertEqual(fighter['essences'], {})
        self.assertEqual(fighter['essence_ids'], {})
        with patch('network_redirect.combat.secrets.randbelow', return_value=0):
            self.assertEqual(combat.damage(fighter, unit(), 1, 1,
                                          journey.load_rules()['battle']), 100)

    def test_conflicting_families_and_slots_match_panel_selection_in_any_order(self):
        self.engrave(10111, level=5, slot=1)
        self.engrave(10211, level=5, slot=2)
        self.engrave(10213, level=5, slot=2)
        self.engrave(10105, slot=3)
        before = copy.deepcopy(self.role)
        fighter = self.attached()
        self.assertEqual(self.role, before)
        self.assertEqual(fighter['essence_ids'], {5: 10105, 11: 10211})
        self.assertEqual(combat.effect(fighter, 11), (60, Fraction('27.5')))
        panel = combat_power.essence_score(self.role, self.role['corteges'][0])
        self.assertEqual(set(fighter['essences']), {i['family'] for i in panel['selected']})
        self.role['attachments'].reverse()
        self.assertEqual(self.attached()['essences'], fighter['essences'])

    def test_formation_moves_keep_identity_and_removal_clears_cached_effect(self):
        self.engrave(10219, level=5)
        fighter = self.attached(order=9)
        self.assertEqual(combat.effect(fighter, 19), (12, 14))
        self.role['attachments'].clear()
        combat.attach_essences(self.role, [fighter])
        self.assertEqual(fighter['essences'], {})
        self.assertEqual(fighter['essence_ids'], {})

    def test_locked_slots_do_not_affect_battle(self):
        self.engrave(10211)
        self.role['corteges'][0]['equiped_ext_skill_limit'] = 0
        self.assertEqual(self.attached()['essences'], {})


class EssenceDamageBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.rules = journey.load_rules()

    def battle(self, left, right):
        return combat_engine.Battle({}, ([left], [right]), self.rules)

    def test_assault_intimidation_parry_modify_only_extra_damage(self):
        actor = unit(gongji=1000, essences={11: (100, 50), 4: (100, 50)})
        target = unit(hp=100000, max_hp=100000, essences={1: (0, 0, 40), 3: (100, 50), 6: (100, 20)})
        with patch('network_redirect.combat.secrets.randbelow', return_value=0):
            # 1000 * (1 + 0.50 * 0.60 * 1.50) * 0.80.
            self.assertEqual(combat.damage(actor, target, 1, 1, self.rules['battle']), 1160)

    def test_execute_threshold_is_strict_and_lucky_dodge_is_execute_only(self):
        with patch('network_redirect.combat.secrets.randbelow', return_value=0):
            for hp, expected in ((200, [100]), (199, [100, 0])):
                battle = self.battle(unit(essences={15: (10, 100)}),
                                     unit(hp=hp, essences={14: (0, 100)}))
                battle.round = 1
                battle.attack(battle.sides[0][0], battle.sides[1])
                self.assertEqual([row['damage_list'][0] for row in battle.actions], expected)

    def test_war_intent_uses_rounds_without_compounding_additional_actions(self):
        actor = unit(gongji=1000, essences={12: (10,)})
        seen = []
        for round_no in (1, 2, 2, 3, 4, 4):
            combat.begin_action(actor, round_no)
            seen.append(actor['gongji'])
        self.assertEqual(seen, [1000, 1100, 1100, 1100, 1200, 1200])

    def test_round_poison_resolves_both_sides_before_elimination(self):
        battle = self.battle(unit(hp=5), unit(hp=5))
        for side, units in enumerate(battle.sides, 1):
            units[0]['poison'] = dict(rate=10, source_side=3-side, logic=101162)
        battle.round = 1
        battle.upkeep()
        self.assertEqual([units[0]['hp'] for units in battle.sides], [0, 0])
        self.assertEqual(battle.actions.damage_totals, {1: 5, 2: 5})
        self.assertEqual(battle.run()[0], 0)

    def test_healing_eligibility_is_evaluated_after_poison_damage(self):
        battle = self.battle(unit(), unit(essences={10: (100, 20)}))
        target = battle.sides[1][0]
        target['poison'] = dict(rate=10, source_side=1, logic=101162)
        battle.round = 2
        with patch('network_redirect.combat.secrets.randbelow', return_value=0):
            battle.upkeep()
        self.assertEqual(target['hp'], target['max_hp'])
        self.assertEqual([change['field_plus'] for event in battle.actions.events
                          for change in event['skill_result_list']], [-100, 100])

    def test_round_thirty_finishes_final_main_action_and_its_combo(self):
        battle = combat_engine.Battle({}, (
            [unit(4, hp=200, gongji=0)],
            [unit(3, hp=100, gongji=60, essences={7: (100, 100)})]), self.rules)
        battle.round = 29
        with patch('network_redirect.combat.secrets.randbelow', return_value=0):
            result, _, actions = battle.run()
        # Attacker is still ahead after the defender's final main hit (140>100),
        # but loses after the same turn's combo (80<100).
        self.assertEqual(actions.final_hp, {1: {4: 80}, 2: {3: 100}})
        self.assertEqual((actions.rounds, actions.stop_reason), (30, 'round_limit'))
        self.assertTrue(4 <= result <= 6)
        self.assertEqual([row['cur_round'] for row in actions], [30, 30, 30])

    def test_poison_revival_resolves_before_round_result_without_second_heal(self):
        battle = self.battle(unit(hp=5), unit(hp=5, essences={10: (100, 100), 19: (100, 50)}))
        for side, units in enumerate(battle.sides, 1):
            units[0]['poison'] = dict(rate=10, source_side=3-side, logic=101162)
        battle.round = 29
        with patch('network_redirect.combat.secrets.randbelow', return_value=0):
            result, _, actions = battle.run()
        self.assertEqual(actions.final_hp, {1: {1: 0}, 2: {1: 500}})
        self.assertEqual((actions.rounds, actions.stop_reason), (30, 'elimination'))
        self.assertTrue(4 <= result <= 6)
        self.assertEqual(battle.sides[1][0]['revive_count'], 1)
        self.assertEqual(actions.damage_totals, {1: 5, 2: 5})

    def test_seeded_all_essence_families_preserve_hp_and_damage_attribution(self):
        for seed in range(12):
            rng = random.Random(91000 + seed)
            slots = 8 if seed % 2 == 0 else 9
            sides = []
            for _side in (1, 2):
                team = []
                for order in range(1, slots + 1):
                    effects, identities = {}, {}
                    for family in rng.sample(range(1, 20), 4):
                        tid = 10200 + family
                        effects[family] = tuple(Fraction(part.split('|')[4].rstrip('%'))
                            for part in combat.ESSENCES[tid]['parameter'].split('/'))
                        identities[family] = tid
                    team.append(unit(order, hp=rng.randrange(50, 1000), max_hp=1000,
                                     gongji=rng.randrange(20, 300), magic=rng.randrange(50, 400),
                                     fangyu=rng.randrange(50), skills=[(101, 1), (21, 10)],
                                     skill_probabilities={101: 100},
                                     essences=effects, essence_ids=identities))
                sides.append(team)
            before = copy.deepcopy(sides)
            with self.subTest(seed=seed), patch('network_redirect.combat.secrets.randbelow', side_effect=rng.randrange):
                battle = combat_engine.Battle({}, sides, self.rules, slots=slots)
                _, _, actions = battle.run()
                hp = {(side, u['order']): u['hp'] for side, team in enumerate(battle.initial, 1) for u in team}
                maximum = {(side, u['order']): u['max_hp'] for side, team in enumerate(battle.initial, 1) for u in team}
                damage = {1: 0, 2: 0}
                for index, row in enumerate(actions, 1):
                    source_side = 1 if row['is_src'] else 2
                    for order, hit in enumerate(row['damage_list'], 1):
                        hp[3-source_side, order] -= hit
                        damage[source_side] += hit
                    for event in actions.events:
                        if event['cur_action'] != index:
                            continue
                        for change in event['skill_result_list']:
                            key = event['who_use'], change['des_order']
                            if change['field'] == 65:
                                hp[key] += change['field_plus']
                                damage[3-event['who_use']] += max(0, -change['field_plus'])
                            elif change['field'] == 9999:
                                hp[key] += change.get('hp_add', 0)
                                maximum[key] += change.get('hp_max_add', 0)
                    self.assertTrue(all(0 <= value <= maximum[key] for key, value in hp.items()))
                self.assertEqual(damage, actions.damage_totals)
                self.assertEqual(hp, {(side, order): value for side, values in actions.final_hp.items()
                                      for order, value in values.items()})
                self.assertEqual(sides, before)


class NpcPassiveBoundaryTests(unittest.TestCase):
    def test_same_stat_passives_are_additive_and_match_player_rounding(self):
        npc = unit(gongji=1000, fangyu=800, magic=500,
                   skills=[(42, 1), (46, 1), (22, 2), (31, 3), (51, 2), (202, 10), (21, 10)])
        combat.apply_npc_passives(npc)
        # Player skill_effect floors each displayed passive percentage first:
        # 22 at level 2 is 12%; 51 at level 2 is 23%. Rulai is trigger-only.
        self.assertEqual([npc[s] for s in ('gongji', 'fangyu', 'magic', 'hp')],
                         [1160, 896, 575, 1230])

    def test_journey_csv_enemy_gets_passive_once_and_player_panel_is_preserved(self):
        role = dict(corteges=[dict(id=7, type=1001, order=1, level=1,
                                  gongji=1234, fangyu=567, hp=890, magic=321)],
                    attachments=[dict(id=8, type_id=42, level=10, attach_type=6,
                                      equip_order=1, equip_pos=1)])
        before = copy.deepcopy(role)
        ours, enemies = journey.fighters(role, dict(cortege_list='5022|1', skill_level=1))
        # Sun Wukong: CSV attack 271, innate skill 45 gives displayed 6%.
        self.assertEqual(enemies[0]['gongji'], 287)
        self.assertEqual(enemies[0]['hp'], enemies[0]['max_hp'])
        self.assertEqual(ours[0]['gongji'], 1234)
        self.assertEqual(role, before)
        self.assertEqual(journey.fighters(role, dict(cortege_list='5022|1', skill_level=1)),
                         (ours, enemies))

    def test_prepared_units_skip_csv_passive_settlement(self):
        prepared = ([unit(skills=[(42, 10)])], [unit(skills=[(42, 10)])])
        with patch('network_redirect.combat.apply_npc_passives', side_effect=AssertionError('already settled')):
            journey.battle({}, {}, journey.load_rules(), units=prepared)
