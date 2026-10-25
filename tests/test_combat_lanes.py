"""User-specified lane formation, reserve deployment and four-field-target AOE."""
import copy
import unittest
from unittest.mock import patch
from network_redirect import combat, combat_engine as engine, journey


def unit(order, **kw):
    return dict(dict(type=1001, order=order, level=1, evolve=0, reborn=0,
                     hp=1000, max_hp=1000, gongji=10, fangyu=0, magic=0, skills=[]), **kw)


class LaneTests(unittest.TestCase):
    def setUp(self):
        self.rules = journey.load_rules()
        self.rng = patch('network_redirect.combat.secrets.randbelow', return_value=0)
        self.rng.start()
        self.addCleanup(self.rng.stop)

    def battle(self, left=None, right=None, **kw):
        return engine.Battle({}, (left if left is not None else [unit(i) for i in range(1, 9)],
                                 right if right is not None else [unit(i) for i in range(1, 9)]), self.rules, **kw)

    def test_exact_eight_step_order(self):
        b = self.battle(max_actions=8)
        actions = b.run()[2]
        self.assertEqual([(a['is_src'], a['src_order']) for a in actions],
                         [(True, 1), (False, 2), (True, 2), (False, 1),
                          (True, 3), (False, 4), (True, 4), (False, 3)])
        self.assertEqual([a['des_order'] for a in actions], [2, 2, 2, 2, 3, 4, 4, 3])

    def test_target_routes_and_front_reserve_before_rear(self):
        b = self.battle()
        rear, front, upper, lower = b.sides[0][:4]
        for actor in (rear, front):
            self.assertEqual(b.targets(actor)[0]['order'], 2)
        b.sides[1][1]['hp'] = 0
        b.deploy()
        self.assertEqual(b.targets(rear)[0]['order'], 6)
        b.sides[1][5]['hp'] = 0
        b.deploy()
        self.assertEqual(b.targets(rear)[0]['order'], 1)
        for index in (0, 4):
            b.sides[1][index]['hp'] = 0
        b.deploy()
        self.assertEqual(b.targets(front)[0]['order'], 3)
        for index in (2, 6):
            b.sides[1][index]['hp'] = 0
        b.deploy()
        self.assertEqual(b.targets(front)[0]['order'], 4)

    def test_side_lane_fallback_middle_then_opposite_lane(self):
        for actor_order, lane in ((3, (3, 7)), (4, (4, 8))):
            b = self.battle()
            actor = b.sides[0][actor_order - 1]
            self.assertEqual(b.targets(actor)[0]['order'], actor_order)
            for order in lane:
                b.sides[1][order - 1]['hp'] = 0
            b.deploy()
            self.assertEqual(b.targets(actor)[0]['order'], 2)
            for order in (1, 2, 5, 6):
                b.sides[1][order - 1]['hp'] = 0
            b.deploy()
            self.assertEqual(b.targets(actor)[0]['order'], 4 if actor_order == 3 else 3)

    def test_aoe_locks_only_initial_field_and_reserves_do_not_take_damage(self):
        b = self.battle([unit(1, gongji=100000, magic=100000)])
        actor = b.sides[0][0]
        targets = b.targets(actor, 101)
        self.assertEqual([u['order'] for u in targets], [1, 2, 3, 4])
        b.attack(actor, targets, 101)
        self.assertEqual(b.actions[0]['damage_list'], [1000] * 4 + [0] * 4)
        self.assertEqual([u['order'] for u in b.fielded(2)], [5, 6, 7, 8])
        self.assertEqual([u['hp'] for u in b.sides[1][4:]], [1000] * 4)
        self.assertEqual([u['order'] for u in b.targets(actor, 101)], [5, 6, 7, 8])

    def test_aoe_multiplier_is_four_slot_cap_not_roster_or_live_count(self):
        actor = unit(1, gongji=10000, magic=3000)
        target = unit(2, hp=100000, max_hp=100000, fangyu=5000)
        b = self.battle([actor], [target])
        from network_redirect import formation
        with patch.dict(formation.SKILLS[101], intensity='300', upgrade_plus='0'):
            self.assertEqual(combat.target_count(101, b.rules), 4)
            self.assertEqual(combat.damage(b.sides[0][0], b.sides[1][0], 101, 1, b.rules), 4122)
        self.assertEqual(len(b.targets(b.sides[0][0], 101)), 1)

    def test_reserve_inherits_unspent_turn_without_extra_action(self):
        b = self.battle([unit(1, gongji=2000)], [unit(2), unit(6)], max_actions=4)
        actions = b.run()[2]
        self.assertEqual([(a['is_src'], a['src_order'], a['cur_round']) for a in actions],
                         [(True, 1, 1), (False, 6, 1), (True, 1, 2)])
        self.assertEqual(b.actions.final_hp[2], {2: 0, 6: 0})

    def test_reserve_waits_if_position_turn_already_spent(self):
        b = self.battle([unit(2, gongji=2000)], [unit(2), unit(6)], max_actions=3)
        actions = b.run()[2]
        self.assertEqual([(a['is_src'], a['src_order'], a['cur_round']) for a in actions],
                         [(False, 2, 1), (True, 2, 1), (False, 6, 2)])

    def test_revival_keeps_reserve_off_field(self):
        b = self.battle([unit(1, gongji=2000)], [unit(2, essences={19: (100, 50)}), unit(6)])
        b.attack(b.sides[0][0], b.targets(b.sides[0][0]))
        self.assertEqual([u['order'] for u in b.fielded(2)], [2])
        self.assertFalse(b.sides[1][1].get('entered', False))

    def test_reserve_cannot_bless_heal_or_share_until_entry(self):
        reserve = unit(6, skills=[(21, 10)], essences={18: (100, 100), 10: (100, 50)})
        b = self.battle([unit(1, gongji=100)], [unit(2), reserve])
        b.round = 2
        b.sides[1][1]['hp'] = 100
        b.upkeep()
        self.assertEqual(b.sides[1][1]['hp'], 100)
        self.assertEqual(b.sides[1][0]['gongji'], 10)
        b.attack(b.sides[0][0], b.targets(b.sides[0][0]))
        self.assertEqual(b.actions[-1]['damage_list'][1], 100)
        self.assertEqual(b.actions[-1]['damage_list'][5], 0)
        b.sides[0][0]['base_gongji'] = 2000
        b.attack(b.sides[0][0], b.targets(b.sides[0][0]))
        self.assertTrue(b.sides[1][1]['entered'])
        self.assertEqual(b.sides[1][1]['gongji'], 20)
        self.assertTrue(any(event['skill_result_list'][0]['field'] == 9999 for event in b.actions.events))

    def test_reserve_only_lineup_deploys_and_battle_runs_to_elimination(self):
        b = self.battle([unit(5, gongji=2000)], [unit(6)])
        result, _, actions = b.run()
        self.assertTrue(1 <= result <= 3)
        self.assertEqual(actions[0]['src_order'], 5)
        self.assertEqual(actions[0]['des_order'], 6)
        self.assertEqual(actions.final_hp[2][6], 0)
        self.assertEqual(actions.stop_reason, 'elimination')

    def test_nine_grid_is_not_treated_as_four_starters_plus_reserves(self):
        b = self.battle([unit(i) for i in range(1, 10)], [unit(i) for i in range(1, 10)], slots=9)
        self.assertEqual(len(b.fielded(1)), 9)
        self.assertEqual(len(b.targets(b.sides[0][0], 101)), 9)

    def test_old_skill_override_cannot_restore_eight_field_targets(self):
        self.rules['battle']['skill_target_limits']['101'] = 8
        b = self.battle()
        self.assertEqual(combat.target_count(101, b.rules), 4)
        self.assertEqual(len(b.targets(b.sides[0][0], 101)), 4)
