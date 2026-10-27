"""Growth response contracts consumed by the original 3.87 item preview.

Each test uses binary requests and a disposable backend. The cached-item reader
below models lineupUI.updateItemInfo:617-723: property 209 is ignored, while
201/202/203 update effect_value only for the corresponding equipment category.
It deliberately does not repair the selected object from a later snapshot.
"""
import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from network_redirect import formation, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode, encode


class RealtimeEquipmentRefreshTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.backend = Backend(Path(self.directory.name), 18770, lambda *a, **k: None)
        self.addCleanup(self.backend.close)
        self.serial = 10000
        role = self.backend.profile()
        role.update(level=99, reborn_layer=4, vip_level=3,
                    silver_coin=1000000000, gold_coin=100000)
        for type_id in (1093, 1310, 1311, 1312, 1313, 1314,
                        1320, 1321, 1322, 1323, 1333, 1334, 1335, 1369):
            summon.add_item(role, type_id, 100000)
        self.backend.save(role)

    def add(self, type_id, **values):
        role = self.backend.profile()
        item = dict(id=formation.new_id(role), attach_type=5, type_id=type_id,
                    count=1, level=1, equip_order=0, equip_pos=0)
        item.update(values)
        role['attachments'].append(item)
        self.backend.save(role)
        return item['id']

    def gear(self, main_type, **values):
        type_id = next(t for t, row in formation.ITEMS.items()
                       if int(row['main_type']) == main_type and int(row['quality']) == 5)
        return self.add(type_id, **values)

    def get(self, identity):
        return next(item for item in self.backend.profile()['attachments'] if item['id'] == identity)

    def request(self, mid, **values):
        self.serial += 1
        packet = encode(mid, dict(serial_num=self.serial, **values))
        rows = [decode(reply) for reply in self.backend.respond(packet, {'authenticated': True})]
        self.assertEqual(rows[-1][0], 1106)
        errors = [login_fields(data['data']) for m, _, data in rows if m == 2998 and data['id'] == 55]
        self.assertEqual(errors, [])
        return rows

    def assert_refresh(self, selected, main_type, rows, event, *, effect_changed=True):
        authoritative = self.get(selected['id'])
        old_effect = selected['effect_value']
        callback = next(i for i, (mid, _, data) in enumerate(rows)
                        if mid == 2998 and data['id'] == event)
        changed = False
        properties = {102: 'count', 103: 'level', 105: 'equip_order', 10: 'equip_pos',
                      109: 'advance_level', 110: 'star_count', 111: 'cur_spirit_count',
                      113: 'reborn_bit', 115: 'cast_level', 117: 'star_level',
                      301: 'drill_count', 302: 'stone1_level', 303: 'stone2_level',
                      304: 'stone3_level', 305: 'stone4_level'}
        accepted_effect = {1: 201, 2: 202, 3: 203}[main_type]
        for index, (mid, _, data) in enumerate(rows):
            if mid != 1032 or data['unit_type'] != 5 or data['id'] != selected['id']:
                continue
            self.assertLess(index, callback, 'the original result callback must see updated values')
            for attr in data['attr_list']:
                if attr['type'] == accepted_effect:
                    selected['effect_value'] = attr['value']
                    changed = True
                elif attr['type'] in properties:
                    selected[properties[attr['type']]] = attr['value']
        if effect_changed:
            self.assertNotEqual(old_effect, authoritative['effect_value'])
            self.assertTrue(changed, 'the response only sent the ignored generic effect property')
        self.assertEqual(selected['effect_value'], authoritative['effect_value'])
        for key in properties.values():
            self.assertEqual(selected.get(key, 0), authoritative.get(key, 0), key)

    def test_single_consecutive_and_batch_enhancement_all_slots(self):
        for main_type in (1, 2, 3):
            with self.subTest(main_type=main_type):
                identity = self.gear(main_type, level=20, equip_order=1, equip_pos=main_type)
                selected = copy.deepcopy(self.get(identity))
                for batch in (False, False, True):
                    with patch.object(summon, 'weighted_choice', return_value=1):
                        rows = self.request(1052, equip_id=identity, equip_order=1, inbatch=batch)
                    self.assert_refresh(selected, main_type, rows, 2)
                    self.assertFalse(any(mid == 1035 and data['first_send'] for mid, _, data in rows))

    def test_pour_progress_seven_stars_and_advancement_all_slots(self):
        for main_type in (1, 2, 3):
            with self.subTest(main_type=main_type):
                identity = self.gear(main_type, level=40)
                selected = copy.deepcopy(self.get(identity))
                rows = self.request(1073, flag=1, equip_id=identity, equip_order=0, is_one_key=False)
                self.assert_refresh(selected, main_type, rows, 115, effect_changed=False)
                self.assertEqual(selected['cur_spirit_count'], 5)
                for star in range(1, 8):
                    rows = self.request(1073, flag=1, equip_id=identity, equip_order=0, is_one_key=True)
                    self.assert_refresh(selected, main_type, rows, 115)
                    self.assertEqual(selected['star_count'], star)
                rows = self.request(1073, flag=2, equip_id=identity, equip_order=0, is_one_key=False)
                self.assert_refresh(selected, main_type, rows, 115)
                self.assertEqual(selected['advance_level'], 1)

    def test_socket_upgrade_and_unload_update_equipment_all_slots(self):
        for main_type in (1, 2, 3):
            with self.subTest(main_type=main_type):
                identity = self.gear(main_type, level=50, drill_count=1)
                stone = self.add(1089 + main_type, level=5)
                material = self.add(1090, level=10)
                selected = copy.deepcopy(self.get(identity))
                for operation, target, materials in ((2, identity, [stone]),
                                                     (3, stone, [material]),
                                                     (4, identity, [stone])):
                    rows = self.request(1054, flag=operation, des_id=target, equip_order=0,
                                        stone_pos=1, src_count=len(materials),
                                        src_list=[dict(id=value) for value in materials])
                    self.assert_refresh(selected, main_type, rows, 83)
                self.assertEqual(selected['stone1_level'], 0)

    def test_rebirth_and_repeated_casts_update_equipment_all_slots(self):
        for main_type in (1, 2, 3):
            with self.subTest(main_type=main_type):
                identity = self.gear(main_type, level=50, advance_level=10)
                selected = copy.deepcopy(self.get(identity))
                for operation in (5, 6, 6, 6):
                    rows = self.request(1328, reborn_type=3, id=operation,
                                        data=summon.lua(dict(equip_id=identity, equip_order=0)))
                    self.assert_refresh(selected, main_type, rows, 172)
                self.assertEqual(selected['cast_level'], 4)

    def test_non_equipment_deltas_keep_generic_property(self):
        before = {'attachments': [dict(id=10, attach_type=5, type_id=1001, effect_value=3)]}
        after = copy.deepcopy(before)
        after['attachments'][0]['effect_value'] = 4
        rows = [decode(packet) for packet in self.backend.item_deltas(before, after)]
        self.assertEqual(rows[0][2]['attr_list'], [dict(type=209, value=4)])


if __name__ == '__main__':
    unittest.main()
