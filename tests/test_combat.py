import copy
import unittest
from unittest.mock import patch
from network_redirect import combat, journey, formation


class DamageTests(unittest.TestCase):
    def setUp(self):
        self.rules = journey.load_rules()['battle']
        self.actor = dict(gongji=10000, magic=3000, skills=[(202, 1)])
        self.target = dict(fangyu=5000, hp=100000)

    def hit(self, skill=202):
        with patch.dict(formation.SKILLS[202], intensity='300', upgrade_plus='0'):
            return combat.damage(self.actor, self.target, skill, 1, self.rules)

    def test_document_examples(self):
        self.assertEqual(self.hit(1), 5000)
        self.assertEqual(self.hit(), 10307)
        self.target['extras'] = {10108: 30}
        self.assertEqual(self.hit(), 7215)
        self.actor['extras'] = {10109: 42}
        self.assertEqual(self.hit(), 8513)
        self.target['extras'] = {}
        self.assertEqual(self.hit(), 10307)

    def test_floor_and_hp_clamp(self):
        self.actor['gongji'] = 19
        self.target['fangyu'] = 10000
        self.assertEqual(self.hit(1), 0)
        self.actor['gongji'] = 10000
        self.target.update(fangyu=0, hp=7)
        self.assertEqual(self.hit(), 7)

    def test_normal_effects_do_not_affect_spells(self):
        self.actor['extras'] = {10111: 50}
        self.target['extras'] = {10106: 30, 10108: 30}
        self.assertEqual(self.hit(1), 5250)
        self.assertEqual(self.hit(), 7215)

    def test_configured_targets_not_survivor_count(self):
        self.rules['skill_target_limits']['202'] = 3
        self.assertEqual(self.hit(), 5153)

    def test_probability_only_selects_action(self):
        self.actor['skill_probabilities'] = {202: 30}
        with patch('network_redirect.combat.secrets.randbelow', return_value=299999):
            self.assertEqual(combat.select_skill(self.actor), (202, 1))
        with patch('network_redirect.combat.secrets.randbelow', return_value=300000):
            self.assertEqual(combat.select_skill(self.actor), (1, 1))
        self.assertEqual(self.hit(), 10307)

    def test_invalid_curve_rejected(self):
        self.rules['intensity_curve']['high'] = 30
        with self.assertRaises(formation.Rejected):
            combat.validate_rules(self.rules)

    def test_engraved_essence_parameters(self):
        unit = dict(type=5004, order=1)
        role = dict(corteges=[dict(id=7, type=5004, order=1, equiped_ext_skill_limit=1)], attachments=[
            dict(id=8, type_id=10211, attach_type=5, owner_id=7, level=5, count=1, ext_skill_pos=1)])
        combat.attach_essences(role, [unit])
        self.assertEqual(combat.effect(unit, 11), (60, 27.5))

    def test_debuffs_and_effective_stats(self):
        self.actor['essences'] = {1: (100, 20, 30), 2: (100, 50)}
        self.target['gongji'] = 1000
        combat.after_hit(self.actor, self.target)
        combat.begin_action(self.target, 1)
        self.assertEqual(self.target['gongji'], 800)
        self.assertEqual(self.target['fangyu'], 2500)
        combat.begin_action(self.target, 2)
        self.assertEqual(self.target['gongji'], 1000)
        combat.after_hit(self.actor, self.target)
        self.assertEqual(self.target['fangyu'], 2500)

    def test_both_engines_use_same_spell_damage_and_preserve_input(self):
        from network_redirect import activity_abyss_combat
        actor = dict(self.actor, type=5004, order=1, level=1, evolve=0, reborn=0,
                     hp=100000, max_hp=100000, fangyu=5000, skill_probabilities={202: 100})
        enemy = dict(actor, type=5005, skills=[], gongji=0, magic=0)
        units = ([actor], [enemy])
        before = copy.deepcopy(units)
        rules = dict(battle=self.rules)
        with patch.dict(formation.SKILLS[202], intensity='300', upgrade_plus='0'):
            normal = journey.battle({}, {}, rules, units=units)[2]
            abyss = activity_abyss_combat.battle({}, units, rules, {}, max_actions=80)[2]
        self.assertEqual(normal[0]['damage_list'][0], 10307)
        self.assertEqual(abyss[0]['damage_list'], normal[0]['damage_list'])
        self.assertEqual(units, before)
