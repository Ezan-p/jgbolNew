"""Owner identity, re-slotting and one-time attachment of battle-only bonuses."""
import copy
import unittest
from unittest.mock import patch

from network_redirect import combat, combat_engine, combat_loadout, journey
from network_redirect import activity_rank, activity_land_npc, activity_undergo, guild_combat


def role(ident=1, train_level=1, arrays=False):
    return dict(role_id=ident, level=80, attachments=[],
                corteges=[dict(id=1, type=1001, order=1, level=1, hp=10000,
                               gongji=1000, fangyu=100, magic=100)],
                activity=dict(home=dict(train={'1': dict(level=train_level)})),
                spirit_array=[dict(activated=arrays, skill_list=[5]*i) for i in range(1, 7)])


class CombatLoadoutTests(unittest.TestCase):
    def test_defender_has_same_cultivation_and_arrays_as_attacker(self):
        owner = role(arrays=True)
        original = copy.deepcopy(owner)
        left = combat_loadout.player_units(owner)
        right = activity_rank.units(owner)
        battle = combat_engine.Battle(owner, (left, right), journey.load_rules())
        self.assertEqual(battle.sides[0][0]['training_bonuses'][0], (7, 1500))
        self.assertEqual(battle.sides[0][0]['training_bonuses'], battle.sides[1][0]['training_bonuses'])
        self.assertEqual(battle.sides[0][0]['reborn_traits'], battle.sides[1][0]['reborn_traits'])
        self.assertEqual(owner, original)

    def test_prepared_snapshot_is_idempotent_without_home_training(self):
        owner = role(train_level=0, arrays=True)
        owner['activity']['home']['train'] = {}
        army = combat_loadout.player_units(owner)
        saved = copy.deepcopy(army)
        combat_loadout.attach_owned_bonuses(owner, army)
        self.assertEqual(army, saved)
        battle = combat_engine.Battle(owner, (army, []), journey.load_rules())
        self.assertEqual(battle.sides[0][0]['training_bonuses'][0], (6, 1000))
        self.assertEqual(battle.sides[0][0]['reborn_traits'], saved[0]['reborn_traits'])

    def test_joint_formation_keeps_each_owners_cultivation(self):
        first, second = role(1, 1, True), role(2, 2, False)
        ours = combat_loadout.player_units(first)
        other = combat_loadout.player_units(second)
        other[0].update(order=2, companion_id=-2)
        expected = copy.deepcopy(other[0])
        battle = combat_engine.Battle(first, (ours+other, []), journey.load_rules())
        self.assertEqual(battle.sides[0][1]['training_bonuses'], expected['training_bonuses'])
        self.assertEqual(battle.sides[0][1]['reborn_traits'], expected['reborn_traits'])
        self.assertNotEqual(battle.sides[0][0]['training_bonuses'], battle.sides[0][1]['training_bonuses'])

    def test_ninth_grid_receives_owned_arrays_and_cultivation(self):
        owner = role(arrays=True)
        army = activity_undergo.player_units(owner, {9: 1})
        battle = combat_engine.Battle(owner, (army, []), journey.load_rules(), slots=9)
        self.assertEqual(battle.sides[0][0]['training_bonuses'][0], (7, 1500))
        self.assertEqual(battle.sides[0][0]['reborn_traits']['survival'], 5)
        self.assertEqual(owner['corteges'][0]['order'], 1)

    def test_grid_selection_of_benched_god_keeps_owned_innate_spell(self):
        owner = role()
        owner['corteges'][0]['order'] = 0
        owner['attachments'] = [dict(id=9, attach_type=6, type_id=102, level=2,
                                    equip_order=0, equip_pos=1, innate_owner_id=1),
                                dict(id=8, attach_type=6, type_id=101, level=1,
                                    equip_order=0, equip_pos=1, innate_owner_id=2)]
        self.assertEqual(activity_undergo.player_units(owner, {9: 1})[0]['skills'], [(102, 2)])

    def test_benched_god_star_strength_array_activates_on_grid_entry(self):
        from network_redirect import reborn_stars
        owner = role(arrays=True)
        owner['corteges'][0]['order'] = 0
        owner['attachments'] = [dict(id=9, attach_type=5, type_id=14309, level=10,
                                    count=1, owner_id=1, ext_awaken_pos=1)]
        self.assertEqual(reborn_stars.combat_traits(owner, owner['corteges'][0])['spell_rate'], 5)
        original = copy.deepcopy(owner)
        army = activity_undergo.player_units(owner, {9: 1})
        battle = combat_engine.Battle(owner, (army, []), journey.load_rules(), slots=9)
        self.assertAlmostEqual(battle.sides[0][0]['reborn_traits']['spell_rate'], 5.15)
        self.assertEqual(owner, original)

    def test_unmatched_companion_never_inherits_owner_effects(self):
        owner = role(arrays=True)
        army = journey.fighters(owner, dict(cortege_list='1001|1'))[0]
        army[0]['companion_id'] = -1
        before = copy.deepcopy(army)
        combat_loadout.attach_owned_bonuses(owner, army)
        self.assertEqual(army, before)

    def test_skill_slots_control_priority_independent_of_inventory(self):
        owner = role()
        owner['attachments'] = [dict(id=8, attach_type=6, type_id=101, level=1, equip_order=1, equip_pos=3),
                                dict(id=9, attach_type=6, type_id=102, level=2, equip_order=1, equip_pos=1),
                                dict(id=7, attach_type=6, type_id=103, level=3, equip_order=1, equip_pos=2)]
        for _ in range(2):
            self.assertEqual(combat_loadout.equipped_skills(owner, 1), [(102, 2), (103, 3), (101, 1)])
            army = activity_rank.units(owner)
            self.assertEqual(army[0]['skills'], [(102, 2), (103, 3), (101, 1)])
            with patch('network_redirect.combat.roll', return_value=True):
                self.assertEqual(combat.select_skill(army[0]), (102, 2))
            owner['attachments'].reverse()

    def test_every_player_snapshot_entry_preserves_owner_traits(self):
        owner = role(arrays=True)
        expected = combat_loadout.player_units(owner)
        self.assertEqual(activity_rank.units(owner), expected)
        self.assertEqual(guild_combat.player_units(owner), expected)
        with patch.object(activity_land_npc, 'catalog', return_value={'fixture': dict(role=owner)}):
            self.assertEqual(activity_land_npc.units('fixture', 1), expected)

    def test_long_guild_result_preserves_all_actions_in_saved_replay(self):
        from network_redirect import guild, battle_replay
        from network_redirect.protocol import decode, MAX_PACKET
        owner = role(); owner['role_name'] = '测试'
        actions = combat_engine.Actions()
        actions.extend(dict(self_use=False, skill_type=1, is_src=True, result=0,
                            src_order=1, des_order=1, cur_round=i//10+1,
                            damage_count=8, damage_list=[0]*8) for i in range(300))
        with patch('network_redirect.journey.battle', return_value=(0, [], actions)):
            result, packets, replay = guild_combat.simulate(owner, {}, guild.load_rules(),
                                                           journey.load_rules(), 28, '守卫')
        self.assertEqual(result, 0)
        self.assertEqual(replay['fight_result_msg']['fight_round'], 300)
        self.assertEqual(len(replay['fight_result_msg']['fight_result']), 300)
        self.assertTrue(all(len(packet) <= MAX_PACKET for packet in packets))
        notice = next(data for mid, _, data in map(decode, packets) if mid == 1027)
        self.assertEqual(notice['guide_stage'], battle_replay.RESULT_MARKER)
        self.assertEqual(notice['final_result'], 0)

    def test_cultivation_is_only_applied_to_physical_damage_once(self):
        owner = role()
        ours = combat_loadout.player_units(owner)
        target = dict(ours[0], companion_id=99, training_bonuses=[(0, 0)]*4)
        target.pop('_combat_loadout_attached')
        battle = combat_engine.Battle(owner, (ours, [target]), journey.load_rules())
        actor, enemy = battle.sides[0][0], battle.sides[1][0]
        self.assertEqual(actor['gongji'], 1000)
        self.assertEqual(combat.damage(actor, enemy, 1, 1, battle.rules), 1409)
        plain = dict(actor, training_bonuses=[(0, 0)]*4)
        self.assertEqual(combat.damage(actor, enemy, 101, 1, battle.rules),
                         combat.damage(plain, enemy, 101, 1, battle.rules))


if __name__ == '__main__':
    unittest.main()
