"""Deterministic interactions, actual HP accounting and native replay contracts."""
import copy
import unittest
from unittest.mock import patch
from network_redirect import combat, combat_engine as e, journey, summon
from network_redirect.protocol import encode, decode
from network_redirect.backend import login_fields


def unit(order=1, **kw):
    return dict(dict(type=1001, order=order, level=1, evolve=0, reborn=0,
                     hp=1000, max_hp=1000, gongji=100, fangyu=0, magic=0, skills=[]), **kw)


class EngineTests(unittest.TestCase):
    def setUp(self):
        self.rules = journey.load_rules()
        self.rules['battle']['mechanics']['rulai_shield_probability'] = 0
        self.rng = patch('network_redirect.combat.secrets.randbelow', return_value=0)
        self.rng.start()
        self.addCleanup(self.rng.stop)

    def battle(self, left=None, right=None, **kw):
        return e.Battle({}, (left or [unit()], right or [unit()]), self.rules, **kw)

    def test_nine_grid_sparse_positions_alternate_occupied_units(self):
        b = self.battle([unit(9)], [unit(1), unit(2)], slots=9)
        self.assertEqual(b.schedule(), ((2, 1), (1, 9), (2, 2)))
        b = self.battle([unit(1), unit(9)], [unit(1), unit(2)], slots=9)
        self.assertEqual(b.schedule(), ((1, 1), (2, 1), (1, 9), (2, 2)))

    def test_counter_never_recurses_and_parry_blocks(self):
        b = self.battle([unit(essences={3: (100, 50)})], [unit(essences={3: (100, 50)})])
        b.round = 1
        b.attack(b.sides[0][0], b.sides[1])
        self.assertEqual([a['damage_list'][0] for a in b.actions], [100, 50])
        b = self.battle([unit(essences={4: (100, 20)})], [unit(essences={3: (100, 50)})])
        b.attack(b.sides[0][0], b.sides[1])
        self.assertEqual(len(b.actions), 1)

    def test_combo_precedes_execute_and_cannot_chain(self):
        b = self.battle([unit(essences={7: (100, 50), 15: (99, 100)})])
        b.attack(b.sides[0][0], b.sides[1])
        self.assertEqual([a['damage_list'][0] for a in b.actions], [100, 50])

    def test_execute_lucky_dodge(self):
        b = self.battle([unit(essences={15: (99, 100)})], [unit(essences={14: (30, 100)})])
        b.attack(b.sides[0][0], b.sides[1])
        self.assertEqual([a['damage_list'][0] for a in b.actions], [100, 0])

    def test_lifesteal_uses_actual_loss_and_never_revives_attacker(self):
        b = self.battle([unit(hp=100, gongji=5000, essences={5: (50,)})], [unit(hp=30)])
        b.attack(b.sides[0][0], b.sides[1])
        self.assertEqual(b.sides[0][0]['hp'], 115)
        self.assertEqual(e.total_damage(b.actions), 30)
        self.assertEqual(b.actions.events[0]['skill_result_list'][0]['field_plus'], 15)

    def test_advanced_revive_twice_and_clear_debuffs(self):
        b = self.battle([unit(gongji=1000)], [unit(hp=10, essences={19: (100, 50)}, essence_ids={19: 10219})])
        target = b.sides[1][0]
        for i in range(3):
            target['poison'] = dict(rate=10, source_side=1, logic=101162)
            target['armor_break'] = 20
            target['attack_reduction'] = 20
            b.attack(b.sides[0][0], [target])
            self.assertNotIn('poison', target)
            self.assertNotIn('attack_reduction', target)
            self.assertEqual(target['armor_break'], 0)
        self.assertEqual(target['hp'], 0)
        self.assertEqual(target['revive_count'], 2)
        self.assertEqual([v['logic_type'] for v in b.actions.events], [102191, 102191])

    def test_survival_before_resurrection(self):
        b = self.battle([unit(gongji=10000)], [unit(essences={19: (100, 50)},
            reborn_traits=dict(survival=100, survival_count=1))])
        target = b.sides[1][0]
        b.attack(b.sides[0][0], [target])
        self.assertEqual(target['hp'], 1)
        self.assertEqual(target['revive_count'], 0)
        b.attack(b.sides[0][0], [target])
        self.assertEqual(target['hp'], 500)
        self.assertEqual(target['revive_count'], 1)

    def test_poison_ticks_at_round_start_cap_and_clear(self):
        b = self.battle([unit(gongji=0)], [unit(hp=1000000, max_hp=1000000)])
        target = b.sides[1][0]
        target['poison'] = dict(rate=90, source_side=1, logic=101162)
        b.round = 2
        b.upkeep()
        self.assertEqual(target['hp'], 800000)
        self.assertEqual(e.total_damage(b.actions), 200000)
        self.assertTrue(b.actions[0]['self_use'])
        self.assertEqual(b.actions[0]['damage_list'][0], 0)
        self.assertEqual(b.actions.events[0]['skill_result_list'][0]['field_plus'], -200000)
        target['essences'] = {17: (100,)}
        b.upkeep()
        self.assertNotIn('poison', target)
        self.assertEqual(target['hp'], 800000)

    def test_poison_death_has_valid_event_anchor_and_no_heal(self):
        b = self.battle(right=[unit(hp=5, essences={10: (100, 100)})])
        target = b.sides[1][0]
        target['poison'] = dict(rate=10, source_side=1, logic=101162)
        b.round = 2
        b.upkeep()
        self.assertEqual(target['hp'], 0)
        self.assertEqual(len(b.actions), 1)
        self.assertEqual(len(b.actions.events), 1)
        self.assertEqual(b.actions.events[0]['cur_action'], 1)

    def test_heal_starts_round_two_lucky_multiplier_and_cap(self):
        b = self.battle(left=[unit(hp=100, essences={10: (100, 20), 14: (50, 0)})])
        b.round = 1
        b.upkeep()
        self.assertEqual(b.sides[0][0]['hp'], 100)
        b.round = 2
        b.upkeep()
        self.assertEqual(b.sides[0][0]['hp'], 400)
        b.sides[0][0]['hp'] = 999
        b.upkeep()
        self.assertEqual(b.sides[0][0]['hp'], 1000)

    def test_blessing_strongest_and_strengthen_additive_base(self):
        units = [unit(essences={18: (100, 10), 13: (50,)}), unit(2, essences={18: (100, 20)})]
        before = copy.deepcopy(units)
        b = self.battle(left=units)
        target = b.sides[0][0]
        self.assertEqual(target['gongji'], 120)
        self.assertEqual(target['max_hp'], 1700)
        self.assertEqual(target['hp'], 1700)
        self.assertEqual(units, before)

    def test_rulai_shares_raw_damage_before_hp_cap_without_recursion(self):
        b = self.battle([unit(gongji=1000)], [unit(hp=500, skills=[(21, 10)]), unit(2, skills=[(21, 10)])])
        b.attack(b.sides[0][0], [b.sides[1][0]])
        self.assertEqual(b.actions[0]['damage_list'][:2], [500, 0])
        self.assertEqual(b.actions.events[0]['logic_type'], 101201)
        self.assertEqual(b.actions.events[0]['skill_result_list'], [dict(field=65, field_plus=-120, des_order=2)])
        self.assertEqual(e.total_damage(b.actions), 620)

    def test_shield_absorbs_before_hp_and_lifesteal(self):
        b = self.battle([unit(hp=100, essences={5: (100,)})])
        b.sides[1][0]['shield'] = 70
        b.attack(b.sides[0][0], b.sides[1])
        self.assertEqual(b.actions[0]['damage_list'][0], 30)
        self.assertEqual(b.sides[0][0]['hp'], 130)
        self.assertEqual(b.sides[1][0]['shield'], 0)

    def test_shield_grant_lowest_ratio_refresh_and_no_health_creation(self):
        self.rules['battle']['mechanics']['rulai_shield_probability'] = 100
        b = self.battle(right=[unit(skills=[(21, 10)]), unit(2, hp=100)])
        b.attack(b.sides[0][0], [b.sides[1][0]])
        weak = b.sides[1][1]
        self.assertEqual((weak['hp'], weak['shield']), (100, 350))
        b.attack(b.sides[0][0], [b.sides[1][0]])
        self.assertEqual(weak['shield'], 350)
        self.assertTrue(any(v['logic_type'] == 101200 and v['skill_result_list'][0]['field'] == 0 for v in b.actions.events))

    def test_break_armor_affects_current_hit_and_is_not_stacked(self):
        b = self.battle([unit(essences={2: (100, 50)})], [unit(fangyu=100)])
        for _ in range(2):
            b.attack(b.sides[0][0], b.sides[1])
        self.assertEqual([a['damage_list'][0] for a in b.actions], [50, 50])

    def test_penetration_probability_bonus_is_configured_not_damage(self):
        actor = unit(skills=[(202, 1)], skill_probabilities={202: 10}, essences={9: (25,)})
        with patch('network_redirect.combat.secrets.randbelow', return_value=120000):
            self.assertEqual(combat.select_skill(actor, self.rules['battle']), (202, 1))
            self.assertEqual(combat.select_skill(actor), (1, 1))

    def test_reordered_identity_preserves_engraved_effects(self):
        role = dict(corteges=[dict(id=7, type=1001, order=1, equiped_ext_skill_limit=1)], attachments=[
            dict(id=1, type_id=10219, level=5, attach_type=5, count=1, owner_id=7, ext_skill_pos=1)])
        fighter = unit(9, companion_id=7)
        b = e.Battle(role, ([fighter], [unit()]), self.rules, slots=9)
        self.assertEqual(combat.effect(b.sides[0][0], 19), (12, 14))

    def test_wire_replay_conserves_hp_with_poison_heal_and_revive(self):
        b = self.battle([unit(essences={5: (50,), 16: (100, 10)})],
                        [unit(essences={10: (100, 10), 19: (100, 10)})], max_actions=30)
        result, lineup, actions = b.run()
        replay = decode(encode(1027, dict(fight_id=7, fight_type=1, final_result=result,
                         fight_round=len(actions), fight_result=actions)))[2]
        payload = login_fields(decode(e.event_packets(actions, 7)[0])[2]['data'])
        hp = {(1, 1): lineup[0]['src_hp'], (2, 1): lineup[0]['des_hp']}
        for index, row in enumerate(replay['fight_result'], 1):
            side = 2 if row['is_src'] else 1
            for order, hit in enumerate(row['damage_list'], 1):
                if hit:
                    hp[side, order] -= hit
                    self.assertGreaterEqual(hp[side, order], 0)
            for event in payload.values():
                if isinstance(event, dict) and event.get('cur_action') == index:
                    for v in event['skill_result_list'].values():
                        if v['field'] == 65:
                            hp[event['who_use'], v['des_order']] += v['field_plus']
        self.assertEqual(hp, {(side, order): value for side, units in actions.final_hp.items() for order, value in units.items()})
        self.assertTrue(all(1 <= v['cur_action'] <= len(actions) for v in actions.events))

    def test_event_budget_does_not_end_an_unfinished_battle(self):
        self.rules['battle']['mechanics']['event_budget_bytes'] = 1000
        b = self.battle([unit(gongji=150, essences={5: (50,)})], [unit(essences={5: (50,)})])
        result, _, actions = b.run()
        self.assertEqual(actions.stop_reason, 'elimination')
        self.assertGreater(b.event_bytes, 1000)
        self.assertEqual(actions.final_hp, {1: {1: 750}, 2: {1: 0}})
        self.assertEqual(result, 3)

    def test_policy_invalid_values_rejected(self):
        for key, bad in [('poison_max_damage', 0), ('rulai_shield_probability', 101),
                         ('advanced_revive_limit', 3), ('event_budget_bytes', 32768)]:
            rules = copy.deepcopy(self.rules['battle'])
            rules['mechanics'][key] = bad
            with self.assertRaises(ValueError):
                combat.validate_rules(rules)

    def test_aoe_defers_shared_death_revival_until_action_end(self):
        b = self.battle([unit(gongji=10000, magic=10000)],
            [unit(), unit(2, hp=10, max_hp=1000, skills=[(21, 10)], essences={19: (100, 50)})])
        b.attack(b.sides[0][0], b.sides[1], skill=101)
        self.assertEqual(b.actions[0]['damage_list'][1], 0)
        self.assertEqual([(event['logic_type'], event['skill_result_list'][0]['field_plus'])
                          for event in b.actions.events], [(101201, -10), (101191, 500)])
        self.assertEqual(b.sides[1][1]['hp'], 500)
        self.assertEqual(b.sides[1][1]['revive_count'], 1)

    def test_counter_consumes_intimidation_once(self):
        b = self.battle([unit(essences={1: (100, 50, 0)})], [unit(essences={3: (100, 100)})])
        b.attack(b.sides[0][0], b.sides[1])
        self.assertEqual(b.actions[1]['damage_list'][0], 50)
        self.assertNotIn('attack_reduction', b.sides[1][0])

    def test_revived_attacker_cannot_resume_combo_after_counter(self):
        b = self.battle([unit(hp=1, essences={7: (100, 100), 19: (100, 50)})],
                        [unit(essences={3: (100, 100)})])
        b.attack(b.sides[0][0], b.sides[1])
        self.assertEqual(len(b.actions), 2)
        self.assertEqual(b.sides[0][0]['revive_count'], 1)

    def test_empty_opposition_is_victory(self):
        b = e.Battle({}, ([unit()], []), self.rules)
        self.assertEqual(b.run()[0], 3)

    def test_fractional_training_csv_levels_are_supported(self):
        role = dict(activity=dict(home=dict(train={'1': {'level': 6}})))
        b = e.Battle(role, ([unit()], [unit(hp=100000, max_hp=100000)]), self.rules)
        b.attack(b.sides[0][0], b.sides[1])
        self.assertEqual(b.actions[0]['damage_list'][0], 3106)

    def test_spell_training_does_not_amplify_attack_component(self):
        actor, target = unit(magic=0, skills=[(202, 1)]), unit()
        baseline = combat.damage(actor, target, 202, 1, self.rules['battle'])
        actor['training_bonuses'] = [(0, 0), (0, 0), (100, 0), (0, 0)]
        self.assertEqual(combat.damage(actor, target, 202, 1, self.rules['battle']), baseline)

    def test_nine_slot_aoe_reaches_ninth_and_uses_configured_cap(self):
        b = self.battle([unit(magic=1000)], [unit(i) for i in range(1, 10)], slots=9)
        b.attack(b.sides[0][0], b.sides[1], skill=101)
        hits = b.actions[0]['damage_list']
        self.assertEqual(len(hits), 9)
        self.assertTrue(all(v == hits[0] > 0 for v in hits))
        self.assertEqual(combat.target_count(101, b.rules), 9)

    def test_healing_formula_targets_allies_and_cannot_resurrect(self):
        b = self.battle([unit(hp=100, magic=1000, skills=[(6, 1)], skill_probabilities={6: 100}),
                         unit(2, hp=0), unit(3, hp=200)], max_actions=1)
        b.run()
        self.assertTrue(b.actions[0]['self_use'])
        self.assertEqual(b.actions[0]['skill_type'], 6)
        self.assertGreater(b.sides[0][0]['hp'], 100)
        self.assertEqual(b.sides[0][1]['hp'], 0)
        self.assertGreater(b.sides[0][2]['hp'], 200)
        self.assertEqual(b.sides[1][0]['hp'], 1000)
        self.assertEqual(e.total_damage(b.actions), 0)
        self.assertTrue(b.actions.events)
        self.assertTrue(all(event['logic_type'] == 101101 for event in b.actions.events))
        self.assertTrue(all(change['field'] == 65 and change['field_plus'] > 0
                            for event in b.actions.events for change in event['skill_result_list']))
        self.assertEqual([u['max_hp'] for u in b.sides[0]], [1000, 1000, 1000])

    def test_placeholder_projectile_uses_physical_formula(self):
        actor, target = unit(magic=100000), unit()
        self.assertEqual(combat.damage(actor, target, 8, 1, self.rules['battle']), 100)

    def test_penetration_does_not_enable_disabled_placeholder(self):
        actor = unit(skills=[(6, 1)], essences={9: (100,)})
        self.assertEqual(combat.select_skill(actor, self.rules['battle']), (1, 1))

    def test_dead_unit_cannot_bless_on_entry(self):
        b = self.battle([unit(hp=0, essences={18: (100, 100)}), unit(2)])
        self.assertEqual(b.sides[0][1]['gongji'], 100)
        self.assertEqual(b.sides[0][1]['hp'], 1000)

    def test_full_rosters_with_effects_fit_wire_limits(self):
        effects = {3: (100, 50), 5: (50,), 7: (100, 50), 10: (100, 20),
                   16: (100, 10), 19: (100, 50)}
        self.rules['battle']['mechanics']['rulai_shield_probability'] = 100
        sides = [[unit(i, hp=10000, max_hp=10000, gongji=1000, magic=300,
                       skills=[(101, 1), (21, 10)], skill_probabilities={101: 100}, essences=effects)
                  for i in range(1, 10)] for _ in range(2)]
        b = e.Battle({}, sides, self.rules, slots=9)
        result, lineup, actions = b.run()
        event_packets = e.event_packets(actions, 123)
        for packet in event_packets + e.result_packets(1140, dict(fight_id=123,
                fight_type=30, final_result=result, fight_round=len(actions), fight_result=actions)):
            self.assertLessEqual(len(packet), 32768)
        # Full transport reassembly is covered by test_battle_replay. Here
        # verify every authoritative HP event for the actual heavy battle.
        payload = e.event_data(actions, 123)
        hp = {(side, u['order']): u['hp'] for side, team in enumerate(b.initial, 1) for u in team}
        for index, row in enumerate(actions, 1):
            side = 2 if row['is_src'] else 1
            for order, hit in enumerate(row['damage_list'], 1):
                hp[side, order] -= hit
                self.assertGreaterEqual(hp[side, order], 0)
            for event in payload.values():
                if isinstance(event, dict) and event.get('cur_action') == index:
                    for v in event['skill_result_list']:
                        if v['field'] == 65:
                            hp[event['who_use'], v['des_order']] += v['field_plus']
        self.assertEqual(hp, {(side, order): value for side, units in actions.final_hp.items() for order, value in units.items()})
