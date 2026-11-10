"""Duplicate rewards, legacy stacks and independent formation equipment IDs."""
import copy
import unittest
from pathlib import Path
from unittest.mock import patch

from network_redirect import formation as f, summon, journey, equipment_crafting, market
from network_redirect.backend import Backend
from network_redirect.protocol import decode
from tests import test_formation as original


class EquipmentGrantTests(unittest.TestCase):
    def test_every_equipment_type_stays_individual_across_reward_paths(self):
        grants = (
            lambda r, t, n: summon.add_item(r, t, n),
            lambda r, t, n: journey.grant(r, (5, t, n, 1)),
            lambda r, t, n: equipment_crafting.grant(r, [(5, t, 1, n)]),
            lambda r, t, n: market.grant(r, t, n),
        )
        for tid, cfg in f.ITEMS.items():
            if int(cfg['main_type']) not in (1, 2, 3):
                continue
            for index, grant in enumerate(grants):
                with self.subTest(tid=tid, path=index):
                    role = dict(attachments=[], summon={})
                    grant(role, tid, 1)
                    equipped = role['attachments'][0]
                    equipped.update(equip_order=1, equip_pos=int(cfg['main_type']))
                    before = copy.deepcopy(equipped)
                    grant(role, tid, 2)
                    self.assertEqual(equipped, before)
                    self.assertEqual(len(role['attachments']), 3)
                    self.assertEqual(len({i['id'] for i in role['attachments']}), 3)
                    self.assertTrue(all(i['count'] == 1 for i in role['attachments']))

    def test_materials_still_stack_and_stones_remain_individual(self):
        role = dict(attachments=[], summon={})
        for tid in (1001, 1090, 1091, 1092):
            summon.add_item(role, tid, 2)
            summon.add_item(role, tid, 3)
            items = [i for i in role['attachments'] if i['type_id'] == tid]
            self.assertEqual(sum(i['count'] for i in items), 5)
            self.assertEqual(len(items), 1 if tid == 1001 else 5)


class EquipmentInstanceTests(unittest.TestCase):
    setUp = original.FormationTests.setUp
    request = original.FormationTests.request
    events = original.FormationTests.events
    ok = original.FormationTests.ok
    change = original.FormationTests.change

    def gear(self, role, tid=2001):
        return [i for i in role['attachments'] if i['attach_type'] == 5 and i['type_id'] == tid]

    def test_duplicate_rewards_can_equip_two_companions_and_upgrade_independently(self):
        role = self.backend.profile()
        journey.grant(role, (5, 2001, 1, 1))
        journey.grant(role, (5, 2001, 2, 1))
        self.backend.save(role)
        first, second, spare = self.gear(self.backend.profile())
        self.change(self.ids[1], 2)
        for item, order in ((first, 1), (second, 2)):
            self.ok(1037, flag=3, obj_type=5, src_id=item['id'], src_order=0,
                    des_order=order, des_equip_pos=1)
        with patch('network_redirect.summon.secrets.randbelow', return_value=0):
            self.ok(1052, equip_id=first['id'], equip_order=1, inbatch=False)
        gear = self.gear(self.backend.profile())
        self.assertEqual([(i['equip_order'], i['level']) for i in gear[:2]], [(1, 2), (2, 1)])
        self.assertEqual(gear[2].get('equip_order', 0), 0)
        self.assertEqual(gear[2]['level'], 1)
        self.ok(1037, flag=3, obj_type=5, src_id=first['id'], src_order=1,
                des_order=0, des_equip_pos=0)
        self.assertEqual(self.gear(self.backend.profile())[1]['equip_order'], 2)

    def test_legacy_stack_preserves_original_growth_links_and_lock_after_restart(self):
        role = self.backend.profile()
        original_item = dict(id=f.new_id(role), attach_type=5, type_id=2001, count=3,
                             level=10, equip_order=1, equip_pos=1, is_lock=1,
                             advance_level=1, star_count=2, cur_spirit_count=1,
                             drill_count=1, stone1_level=5, reborn_bit=1, cast_level=1)
        role['attachments'].append(original_item)
        stone = dict(id=f.new_id(role), attach_type=5, type_id=1090, count=1,
                     level=5, owner_id=original_item['id'], equip_pos=1)
        role['attachments'].append(stone)
        summon.add_item(role, 1001, 17)
        self.backend.save(role)
        migrated = self.backend.profile()
        gear = self.gear(migrated)
        self.assertEqual(len(gear), 3)
        for key, value in original_item.items():
            self.assertEqual(gear[0][key], 1 if key == 'count' else value)
        self.assertEqual(f.lookup(migrated, 'attachments', stone['id'])['owner_id'], original_item['id'])
        for item in gear[1:]:
            self.assertEqual((item['count'], item['level'], item['is_lock']), (1, 1, 1))
            self.assertTrue(all(not item.get(k) for k in (
                'equip_order', 'equip_pos', 'owner_id', 'advance_level', 'star_count',
                'cur_spirit_count', 'drill_count', 'stone1_level', 'reborn_bit', 'cast_level')))
        self.assertEqual(sum(i['count'] for i in migrated['attachments'] if i['type_id'] == 1001), 17)
        self.assertFalse(f.prepare(migrated, self.backend.formation_rules))
        self.assertEqual(migrated, self.backend.profile())
        self.backend.close()
        self.backend = Backend(Path(self.directory.name), 18770, lambda *a, **k: None)
        self.assertEqual(self.gear(self.backend.profile()), gear)

    def test_legacy_duplicates_reach_client_in_multiple_inventory_packets(self):
        role = self.backend.profile()
        for main in (1, 2, 3):
            tid = next(t for t, cfg in f.ITEMS.items() if int(cfg['main_type']) == main)
            role['attachments'].append(dict(id=f.new_id(role), attach_type=5,
                                            type_id=tid, count=90, level=1))
        self.backend.save(role)
        migrated = self.backend.profile()
        packets = [decode(p)[2] for p in self.backend.inventory(migrated, changed={'attachments'})]
        self.assertEqual([p['first_send'] for p in packets], [True, False, False])
        items = [i for packet in packets for i in packet['attach_list']]
        gear = [i for i in items if i['attach_type'] == 5]
        self.assertEqual(len(gear), 270)
        self.assertEqual(len({i['id'] for i in items}), len(items))
        self.assertTrue(all(i['count'] == 1 for i in gear))


if __name__ == '__main__':
    unittest.main()
