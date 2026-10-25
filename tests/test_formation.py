"""Original wire requests, atomic settlement, migration and reconnect regressions."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from network_redirect.backend import Backend, login_fields
from network_redirect import formation, summon
from network_redirect.protocol import encode, decode


class FormationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.backend = Backend(Path(self.directory.name), 18770, lambda *a, **k: None)
        self.addCleanup(lambda: self.backend.close())
        self.state = {'authenticated': True}
        self.serial = 100000
        role = self.backend.profile()
        role.update(level=20, gold_coin=1000, silver_coin=10000)
        role['corteges'].append(summon.companion(role, 5002))
        role['corteges'].append(summon.companion(role, 5003))
        formation.prepare(role, self.backend.formation_rules)
        role['corteges'][0]['culture_point'] = 100
        self.backend.save(role)
        self.ids = [c['id'] for c in role['corteges']]

    def request(self, mid, **req):
        self.serial += 1
        self.packet = encode(mid, dict(serial_num=self.serial, **req))
        self.replies = self.backend.respond(self.packet, self.state)
        rows = [decode(p) for p in self.replies]
        self.assertEqual(rows[-1][0], 1106)
        self.assertEqual(rows[-1][2]['req_serial_num'], self.serial)
        return rows

    def events(self, rows):
        return [(r[2]['id'], login_fields(r[2]['data'])) for r in rows if r[0] == 2998]

    def ok(self, mid, **req):
        rows = self.request(mid, **req)
        self.assertNotIn(55, [t for t, _ in self.events(rows)], self.events(rows))
        return rows

    def rejected(self, mid, **req):
        before = self.backend.profile()
        rows = self.request(mid, **req)
        self.assertEqual(self.events(rows)[0][0], 55)
        self.assertEqual(self.backend.profile(), before)

    def add_item(self, type_id, count=1, attach_type=5, **extra):
        role = self.backend.profile()
        item = dict(id=formation.new_id(role), type_id=type_id, count=count,
                    attach_type=attach_type, level=1, equip_order=0, equip_pos=0, **extra)
        role['attachments'].append(item)
        self.backend.save(role)
        return item['id']

    def change(self, identity, order, flag=4):
        return self.ok(1024, flag=flag, count=1, change_info=[dict(id=identity, new_order=order)])

    def test_original_replacement_updates_innate_and_keeps_slot_equipment(self):
        weapon = self.add_item(2001)
        self.ok(1037, flag=3, obj_type=5, src_id=weapon, src_order=0, des_order=1, des_equip_pos=1)
        rows = self.change(self.ids[1], 1)
        role = self.backend.profile()
        self.assertEqual([c['order'] for c in role['corteges']], [0, 1, 0])
        skills = {i['innate_owner_id']: i for i in role['attachments'] if i.get('protogenic')}
        self.assertEqual(skills[self.ids[0]]['equip_order'], 0)
        self.assertEqual(skills[self.ids[1]]['equip_order'], 1)
        self.assertEqual(formation.lookup(role, 'attachments', weapon)['equip_order'], 1)
        self.assertEqual(self.events(rows), [(1, {'flag': 4})])
        self.assertTrue(role['corteges'][1]['gongji'] > int(formation.BASES[5002]['base_gongji']))

    def test_atomic_swap_moves_equipment_and_innate(self):
        self.change(self.ids[1], 2)
        weapon = self.add_item(2001)
        self.ok(1037, flag=3, obj_type=5, src_id=weapon, src_order=0, des_order=1, des_equip_pos=1)
        rows = self.ok(1024, flag=5, count=2, change_info=[dict(id=self.ids[0], new_order=2), dict(id=self.ids[1], new_order=1)])
        role = self.backend.profile()
        self.assertEqual([c['order'] for c in role['corteges']], [2, 1, 0])
        self.assertEqual(formation.lookup(role, 'attachments', weapon)['equip_order'], 2)
        self.assertEqual(self.events(rows), [(1, {'flag': 5})])

    def test_order_validation_preserves_entire_save(self):
        for changes in ([dict(id=999, new_order=1)], [dict(id=self.ids[0], new_order=8)],
                        [dict(id=self.ids[0], new_order=1)] * 2,
                        [dict(id=self.ids[1], new_order=1)], [dict(id=self.ids[0], new_order=0)]):
            with self.subTest(changes=changes):
                self.rejected(1024, flag=5, count=len(changes), change_info=changes)
        self.rejected(1024, flag=99, count=1, change_info=[dict(id=self.ids[1], new_order=1)])

    def test_replay_exact_bytes_and_conflicting_serial(self):
        self.change(self.ids[1], 1)
        before = self.backend.profile()
        self.assertEqual(self.backend.respond(self.packet, self.state), self.replies)
        conflicting = encode(1024, dict(serial_num=self.serial, flag=4, count=1,
                                       change_info=[dict(id=self.ids[2], new_order=1)]))
        self.assertEqual(self.events([decode(p) for p in self.backend.respond(conflicting, self.state)])[0][0], 55)
        self.assertEqual(self.backend.profile(), before)
        replay = self.backend.respond(encode(1105, dict(req_serial_num=200000)), self.state)
        self.assertEqual(replay[:len(self.replies)], self.replies)

    def test_zero_serial_and_unauthenticated(self):
        before = self.backend.profile()
        packet = encode(1024, dict(flag=4, count=1, change_info=[dict(id=self.ids[1], new_order=1)]))
        with self.assertRaises(ValueError):
            self.backend.respond(packet, {})
        self.assertEqual(decode(self.backend.respond(packet, self.state)[0])[2]['id'], 55)
        self.assertEqual(self.backend.profile(), before)

    def test_migration_keeps_skill_id_and_level_without_duplicates(self):
        role = self.backend.profile()
        skill = next(i for i in role['attachments'] if i.get('innate_owner_id') == self.ids[0])
        skill['level'] = 5
        del skill['innate_owner_id']
        self.backend.save(role)
        migrated = self.backend.profile()
        self.assertEqual(len(migrated['attachments']), 3)
        self.assertEqual(formation.lookup(migrated, 'attachments', skill['id'])['level'], 5)
        self.assertEqual(self.backend.profile(), migrated)

    def test_missing_innate_repaired_for_all_summoned_companions(self):
        role = self.backend.profile()
        role['attachments'] = []
        self.backend.save(role)
        repaired = self.backend.profile()
        self.assertEqual(len(repaired['attachments']), len(repaired['corteges']))
        for c in repaired['corteges']:
            skill = next(i for i in repaired['attachments'] if i['innate_owner_id'] == c['id'])
            self.assertEqual(skill['type_id'], int(formation.BASES[c['type']]['chushijineng']))
            self.assertEqual(skill['effect_value'], formation.skill_effect(skill))

    def test_equipment_replace_unload_and_invalid_slot(self):
        first, second = self.add_item(2001), self.add_item(2002)
        self.ok(1037, flag=3, obj_type=5, src_id=first, src_order=0, des_order=1, des_equip_pos=1)
        self.ok(1037, flag=3, obj_type=5, src_id=second, src_order=0, des_order=1, des_equip_pos=1)
        self.assertEqual(formation.lookup(self.backend.profile(), 'attachments', first)['equip_order'], 0)
        self.rejected(1037, flag=3, obj_type=5, src_id=first, src_order=0, des_order=1, des_equip_pos=2)
        self.ok(1037, flag=3, obj_type=5, src_id=second, src_order=1, des_order=0, des_equip_pos=0)
        self.assertEqual(formation.lookup(self.backend.profile(), 'attachments', second)['equip_order'], 0)

    def test_innate_cannot_be_removed_or_consumed_or_replaced(self):
        innate = self.backend.profile()['attachments'][0]['id']
        self.rejected(1037, flag=3, obj_type=6, src_id=innate, src_order=1, des_order=0, des_equip_pos=0)
        free = self.add_item(212, count=0, attach_type=6)
        self.rejected(1037, flag=3, obj_type=6, src_id=free, src_order=0, des_order=1, des_equip_pos=1)
        self.rejected(1071, data=summon.lua(dict(des_skill_id=free, src_skill_list=[innate])))

    def test_secondary_skill_equips_and_duplicate_rejected(self):
        first = self.add_item(212, count=0, attach_type=6)
        second = self.add_item(212, count=0, attach_type=6)
        self.ok(1037, flag=3, obj_type=6, src_id=first, src_order=0, des_order=1, des_equip_pos=2)
        self.rejected(1037, flag=3, obj_type=6, src_id=second, src_order=0, des_order=1, des_equip_pos=3)

    def test_strengthening_cost_cap_and_replay(self):
        item = self.add_item(2001)
        before = self.backend.profile()
        with patch('network_redirect.summon.secrets.randbelow', return_value=0):
            rows = self.ok(1052, equip_id=item, equip_order=0, inbatch=False)
        after = self.backend.profile()
        self.assertEqual(after['silver_coin'], before['silver_coin'] - 50)
        self.assertEqual(formation.lookup(after, 'attachments', item)['level'], 2)
        self.assertEqual(self.events(rows)[0][1]['upgrade_list'][1]['new_level'], 2)
        self.assertEqual(self.backend.respond(self.packet, self.state), self.replies)
        self.assertEqual(self.backend.profile(), after)
        after['level'] = 1
        self.backend.save(after)
        self.rejected(1052, equip_id=item, equip_order=0, inbatch=False)

    def test_skill_success_and_failure_consume_only_valid_materials(self):
        target = self.backend.profile()['attachments'][0]['id']
        material = self.add_item(212, count=0, attach_type=6)
        with patch('network_redirect.formation.secrets.randbelow', return_value=99):
            self.ok(1071, data=summon.lua(dict(des_skill_id=target, src_skill_list=[material])))
        role = self.backend.profile()
        item = formation.lookup(role, 'attachments', target)
        self.assertEqual(item['level'], 1)
        self.assertEqual(item['count'], 1)
        self.assertNotIn(material, [i['id'] for i in role['attachments']])
        material = self.add_item(212, count=0, attach_type=6)
        with patch('network_redirect.formation.secrets.randbelow', return_value=0):
            self.ok(1071, data=summon.lua(dict(des_skill_id=target, src_skill_list=[material])))
        item = formation.lookup(self.backend.profile(), 'attachments', target)
        self.assertEqual((item['level'], item['count'], item['effect_value']), (2, 0, 133))

    def test_skill_duplicate_material_and_lua_injection_are_rejected(self):
        target = self.backend.profile()['attachments'][0]['id']
        material = self.add_item(212, count=0, attach_type=6)
        for payload in (dict(des_skill_id=target, src_skill_list=[material, material]),
                        dict(des_skill_id=target, src_skill_list=[target]),
                        dict(des_skill_id=target, src_skill_list=[])):
            self.rejected(1071, data=summon.lua(payload))
        self.rejected(1071, data='{des_skill_id=os.execute("false")}')

    def test_training_preview_giveup_save_and_reconnect(self):
        self.add_item(1001, 100)
        role = self.backend.profile()
        role['corteges'][0]['level'] = 2
        self.backend.save(role)
        before = self.backend.profile()
        with patch('network_redirect.formation.secrets.choice', return_value='gongji'):
            rows = self.ok(1081, cortege_id=self.ids[0], train_type=2, intensive=True)
        role = self.backend.profile()
        self.assertEqual(role['corteges'][0]['gongji'], before['corteges'][0]['gongji'])
        self.assertEqual(role['gold_coin'], before['gold_coin'] - 10)
        self.assertEqual(self.events(rows)[0], (4, dict(cortege_id=self.ids[0], train_result=1, increase_field=88, decrease_field=90, train_point=30)))
        self.rejected(1081, cortege_id=self.ids[0], train_type=1, intensive=False)
        self.backend.close()
        self.backend = Backend(Path(self.directory.name), 18770, lambda *a, **k: None)
        self.ok(1082, cortege_id=self.ids[0], confirm=True)
        after = self.backend.profile()
        self.assertEqual(after['corteges'][0]['gongji'], before['corteges'][0]['gongji'] + 30)
        self.assertEqual(after['corteges'][0]['culture_point'], 70)
        self.rejected(1082, cortege_id=self.ids[0], confirm=True)
        self.ok(1081, cortege_id=self.ids[0], train_type=1, intensive=False)
        self.ok(1082, cortege_id=self.ids[0], confirm=False)
        self.assertEqual(self.backend.profile()['corteges'][0]['culture_point'], 70)

    def test_training_insufficient_gold_does_not_consume_peaches(self):
        self.add_item(1001, 50)
        role = self.backend.profile()
        role['corteges'][0]['level'] = 2
        role['gold_coin'] = 0
        self.backend.save(role)
        self.rejected(1081, cortege_id=self.ids[0], train_type=2, intensive=True)

    def test_training_level_one_with_evolution_potential_is_disabled(self):
        self.add_item(1001, 100)
        role = self.backend.profile()
        role['corteges'][0].update(level=1, evolve_level=1, culture_point=30)
        self.backend.save(role)
        for train_type in (1, 2):
            for intensive in (False, True):
                self.rejected(1081, cortege_id=self.ids[0],
                              train_type=train_type, intensive=intensive)
                self.assertIn('2级', str(self.events([decode(p) for p in self.replies])))

    def test_training_level_two_all_four_modes(self):
        self.add_item(1001, 200)
        role = self.backend.profile()
        role['corteges'][0]['level'] = 2
        self.backend.save(role)
        for train_type in (1, 2):
            for intensive in (False, True):
                with self.subTest(train_type=train_type, intensive=intensive):
                    before = self.backend.profile()
                    points = (10 if train_type == 2 else 1) * (3 if intensive else 1)
                    with patch('network_redirect.formation.secrets.choice', return_value='gongji'):
                        rows = self.ok(1081, cortege_id=self.ids[0],
                                       train_type=train_type, intensive=intensive)
                    self.assertEqual(self.events(rows)[0][1]['train_point'], points)
                    self.assertEqual(self.backend.profile()['corteges'][0]['culture_point'],
                                     before['corteges'][0]['culture_point'])
                    self.ok(1082, cortege_id=self.ids[0], confirm=True)
                    after = self.backend.profile()['corteges'][0]
                    self.assertEqual(after['gongji_plus'], before['corteges'][0]['gongji_plus'] + points)
                    self.assertEqual(after['culture_point'], before['corteges'][0]['culture_point'] - points)

    def test_legacy_level_one_training_can_still_be_resolved(self):
        for confirm in (False, True):
            role = self.backend.profile()
            c = role['corteges'][0]
            c.update(level=1, pending_training=dict(points=1, deltas={'gongji': 1}),
                     train_increase_field=88, train_decrease_field=90, train_change_value=1)
            self.backend.save(role)
            self.ok(1082, cortege_id=self.ids[0], confirm=confirm)
            self.assertNotIn('pending_training', self.backend.profile()['corteges'][0])

    def test_evolve_and_compose_use_original_csv(self):
        role = self.backend.profile()
        role['souls'] = {'5004': 30, '5005': 40}
        self.backend.save(role)
        self.ok(1084, flag=0, cortege_id=self.ids[0])
        c = self.backend.profile()['corteges'][0]
        self.assertEqual(c['evolve_level'], 1)
        self.assertEqual(c['culture_point'], 100 + formation.EVOLVE_POINTS[5, 1])
        self.ok(1083, type_id=5005)
        role = self.backend.profile()
        c = next(c for c in role['corteges'] if c['type'] == 5005)
        self.assertTrue(any(i.get('innate_owner_id') == c['id'] for i in role['attachments']))
        self.rejected(1083, type_id=5005)

    def test_evolution_direct_stats_wire_recycle_and_reconnect(self):
        self.add_item(1002, 1)
        role = self.backend.profile()
        role['souls'] = {'5004': 75}
        self.backend.save(role)
        before = self.backend.profile()['corteges'][0]
        # Original 5004 growth: HP 36.58, attack 14.06, defense 9.03,
        # magic 9.88. The UI floors each growth * 3 BEFORE accumulation.
        gains = dict(hp=109, gongji=42, fangyu=27, magic=29)
        for n in (1, 2):
            rows = self.ok(1084, flag=0, cortege_id=self.ids[0])
            c = self.backend.profile()['corteges'][0]
            for stat, gain in gains.items():
                self.assertEqual(c[stat], before[stat] + gain * n)
            delta = next(d for m, _, d in rows if m == 1032 and d['unit_type'] == 4 and d['id'] == c['id'])
            self.assertIn(dict(type=61, value=c['hp']), delta['attr_list'])
            self.assertEqual(self.backend.respond(self.packet, self.state), self.replies)
            self.assertEqual(self.backend.profile()['corteges'][0], c)
        self.backend.close()
        self.backend = Backend(Path(self.directory.name), 18770, lambda *a, **k: None)
        self.assertEqual(self.backend.profile()['corteges'][0], c)
        self.ok(1084, flag=1, cortege_id=self.ids[0])
        c = self.backend.profile()['corteges'][0]
        for stat in gains:
            self.assertEqual(c[stat], before[stat])
        self.assertEqual(c['culture_point'], before['culture_point'])

    def test_large_inventory_is_chunked_and_complete(self):
        role = self.backend.profile()
        for _ in range(300):
            role['attachments'].append(dict(id=formation.new_id(role), attach_type=5, type_id=1001, count=1))
        self.backend.save(role)
        rows = [decode(p) for p in self.backend.bootstrap()]
        chunks = [r[2] for r in rows if r[0] == 1035]
        self.assertEqual([r['first_send'] for r in chunks], [True, False, False])
        self.assertEqual(sum(r['attach_count'] for r in chunks), 303)
        self.assertEqual(len({i['id'] for r in chunks for i in r['attach_list']}), 303)

    def test_lock_material_prevents_skill_consumption(self):
        material = self.add_item(212, count=0, attach_type=6)
        self.ok(1343, des_id=material, flag=1)
        self.rejected(1071, data=summon.lua(dict(des_skill_id=self.backend.profile()['attachments'][0]['id'], src_skill_list=[material])))

    def test_summon_payment_does_not_delete_zero_count_skills(self):
        self.add_item(1006, 1)
        before = {i['id'] for i in self.backend.profile()['attachments'] if i['attach_type'] == 6}
        self.ok(1042, pick_grade=2, pick_type=2, ten_pick=0)
        after = {i['id'] for i in self.backend.profile()['attachments'] if i['attach_type'] == 6}
        self.assertTrue(before <= after)


    def test_experience_book_levels_and_grants_potential(self):
        self.add_item(1041, 2)
        before = self.backend.profile()['corteges'][0]
        rows = self.ok(1059, first_send=True, flag=1, cortege_id=self.ids[0], roll_count=1,
                       roll_list=[dict(type_id=1041, count=1)])
        after = self.backend.profile()['corteges'][0]
        total = sum(formation.EXPERIENCE[5, n] for n in range(1, after['level'])) + after['cur_exp']
        self.assertEqual(total, 1200)
        self.assertEqual(after['culture_point'], before['culture_point'] + (after['level'] - 1) * 5)
        self.assertEqual(self.events(rows)[0][0], 65)
        self.rejected(1059, first_send=True, flag=1, cortege_id=self.ids[0], roll_count=1,
                      roll_list=[dict(type_id=1041, count=2)])

    def test_experience_discount_cap_and_pill_gate(self):
        self.add_item(1041, 3)
        self.add_item(1401, 2)
        role = self.backend.profile()
        role['corteges'][0].update(level=50, cur_exp=0)
        self.backend.save(role)
        self.ok(1059, first_send=True, flag=1, cortege_id=self.ids[0], roll_count=1,
                roll_list=[dict(type_id=1041, count=1)])
        self.assertEqual(self.backend.profile()['corteges'][0]['cur_exp'], 240)
        self.rejected(1059, first_send=True, flag=2, cortege_id=self.ids[0], roll_count=1,
                      roll_list=[dict(type_id=1401, count=1)])
        role = self.backend.profile()
        role['corteges'][0].update(level=60, cur_exp=0)
        self.backend.save(role)
        self.rejected(1059, first_send=True, flag=1, cortege_id=self.ids[0], roll_count=1,
                      roll_list=[dict(type_id=1041, count=1)])
        role['level'] = 80
        self.backend.save(role)
        self.ok(1059, first_send=True, flag=1, cortege_id=self.ids[0], roll_count=1,
                roll_list=[dict(type_id=1041, count=1)])
        self.assertEqual(self.backend.profile()['corteges'][0]['cur_exp'], 1200)
        self.ok(1059, first_send=True, flag=2, cortege_id=self.ids[0], roll_count=1,
                roll_list=[dict(type_id=1401, count=1)])

    def test_direct_training_and_invalid_points(self):
        self.add_item(1343, 2)
        role = self.backend.profile()
        role['corteges'][0]['level'] = 2
        self.backend.save(role)
        self.rejected(1089, cortege_id=self.ids[0], train_field=2, train_point=6)
        rows = self.ok(1089, cortege_id=self.ids[0], train_field=2, train_point=10)
        delta = rows[0]
        self.assertEqual((delta[0], delta[2]['unit_type']), (1032, 4))
        self.assertIn(dict(type=90, value=90), delta[2]['attr_list'])
        self.assertLess(next(i for i, r in enumerate(rows) if r[0] == 1032), next(i for i, r in enumerate(rows) if r[0] == 1034))
        c = self.backend.profile()['corteges'][0]
        self.assertEqual((c['gongji_plus'], c['culture_point']), (10, 90))
        self.rejected(1089, cortege_id=self.ids[0], train_field=2, train_point=5)

    def test_impart_conserves_experience_and_refunds_training(self):
        self.add_item(1002, 1)
        role = self.backend.profile()
        src, dst = role['corteges'][:2]
        src.update(level=3, cur_exp=7, gongji_plus=10)
        total = 7 + formation.EXPERIENCE[5, 1] + formation.EXPERIENCE[5, 2]
        original_skill = next(i['id'] for i in role['attachments'] if i.get('innate_owner_id') == src['id'])
        self.backend.save(role)
        self.ok(1025, src_id=src['id'], des_id=dst['id'])
        role = self.backend.profile()
        src, dst = role['corteges'][:2]
        self.assertEqual((src['level'], src['cur_exp'], src['gongji_plus']), (1, 0, 0))
        self.assertEqual(sum(formation.EXPERIENCE[5, n] for n in range(1, dst['level'])) + dst['cur_exp'], total)
        self.assertEqual(next(i['count'] for i in role['attachments'] if i['type_id'] == 1001), 10)
        self.assertIn(original_skill, [i['id'] for i in role['attachments']])
        self.rejected(1025, src_id=src['id'], des_id=dst['id'])

    def test_devolve_refunds_original_category_and_removes_evolution_points(self):
        self.add_item(1002, 1)
        role = self.backend.profile()
        role['souls'] = {'5004': 30}
        self.backend.save(role)
        self.ok(1084, flag=0, cortege_id=self.ids[0])
        rows = self.ok(1084, flag=1, cortege_id=self.ids[0])
        c = self.backend.profile()['corteges'][0]
        self.assertEqual((c['evolve_level'], c['culture_point']), (0, 100))
        self.assertEqual(self.events(rows)[0][0], 123)
        self.assertEqual(self.events(rows)[0][1]['attach_list'][1]['attach_count'], 9)
        self.rejected(1084, flag=1, cortege_id=self.ids[0])

    def test_equipment_critical_upgrade_and_batch_vip_gate(self):
        item = self.add_item(2001)
        self.rejected(1052, equip_id=item, equip_order=0, inbatch=True)
        with patch('network_redirect.summon.secrets.randbelow', return_value=99):
            self.ok(1052, equip_id=item, equip_order=0, inbatch=False)
        self.assertEqual(formation.lookup(self.backend.profile(), 'attachments', item)['level'], 6)
        role = self.backend.profile()
        role.update(vip_level=3, silver_coin=1000000)
        self.backend.save(role)
        with patch('network_redirect.summon.secrets.randbelow', return_value=0):
            rows = self.ok(1052, equip_id=item, equip_order=0, inbatch=True)
        self.assertEqual(len(self.events(rows)[0][1]['upgrade_list']), 10)

    def test_unlock_allows_material_consumption(self):
        material = self.add_item(212, count=0, attach_type=6)
        self.ok(1343, des_id=material, flag=1)
        self.ok(1343, des_id=material, flag=2)
        self.ok(1071, data=summon.lua(dict(des_skill_id=self.backend.profile()['attachments'][0]['id'], src_skill_list=[material])))


    def test_equipment_pouring_advance_and_atomic_costs(self):
        item = self.add_item(2001)
        self.add_item(1310, 1000)
        self.add_item(1313, 100)
        self.add_item(1320, 100)
        args = dict(equip_id=item, equip_order=0, is_one_key=False)
        self.rejected(1073, flag=1, **args)
        role = self.backend.profile()
        role['level'] = 60
        self.backend.save(role)
        self.ok(1073, flag=1, **args)
        equip = formation.lookup(self.backend.profile(), 'attachments', item)
        self.assertEqual((equip['cur_spirit_count'], equip['star_count']), (5, 0))
        self.rejected(1073, flag=2, **args)
        args['is_one_key'] = True
        for _ in range(7):
            self.ok(1073, flag=1, **args)
        equip = formation.lookup(self.backend.profile(), 'attachments', item)
        self.assertEqual((equip['star_count'], equip['effect_value']), (7, 274))
        self.rejected(1073, flag=1, **args)
        rows = self.ok(1073, flag=2, **args)
        equip = formation.lookup(self.backend.profile(), 'attachments', item)
        self.assertEqual((equip['advance_level'], equip['star_count'], equip['effect_value']), (1, 0, 283))
        self.assertEqual(self.events(rows)[0], (115, dict(flag=2, result=1, equip_id=item)))
        self.assertNotIn(1035, [r[0] for r in rows])  # Preserve the panel's selected object across repeated requests.
        delta = next(r[2] for r in rows if r[0] == 1032 and r[2]['unit_type'] == 5)
        self.assertIn(dict(type=109, value=1), delta['attr_list'])

    def test_advance_cost_failure_preserves_all_materials(self):
        item = self.add_item(2001, advance_level=0, star_count=7)
        self.add_item(1313, 100)
        role = self.backend.profile()
        role['level'] = 60
        self.backend.save(role)
        self.rejected(1073, flag=2, equip_id=item, equip_order=0, is_one_key=False)

    def test_advance_configuration_reaches_original_client(self):
        config = login_fields(decode(self.backend.bootstrap()[0])[2]['data'])
        self.assertEqual(config[23], self.backend.formation_rules['equipment_advance'])


if __name__ == '__main__':
    unittest.main()
