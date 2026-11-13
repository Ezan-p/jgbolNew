"""Bagua original binary requests: settlement, failure atomicity and reconnect."""
import copy
import json
import tempfile
import unittest
from unittest.mock import patch
from decimal import Decimal
from pathlib import Path
from network_redirect import cheer, formation as f, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode


class CheerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.addCleanup(self.b.close)
        self.serial = 1000
        role = self.b.profile()
        role.update(level=99, reborn_layer=4, gold_coin=10000)
        for t in (1015, 1016, 1017):
            summon.add_item(role, t, 100000)
        # Legacy material stacks are supported; avoid creating 100,000 separate
        # non-stackable gift instances just to exercise Bagua settlement.
        role['attachments'].append(dict(id=f.new_id(role), attach_type=5, type_id=1206,
                                        count=100000, level=1))
        for t in (5002, 5003):
            role['corteges'].append(summon.companion(role, t))
        f.prepare(role, self.b.formation_rules)
        self.ids = [c['id'] for c in role['corteges']]
        self.b.save(role)

    def req(self, flag, order=1, identity=0, pos=9, fail=False):
        if flag == 8 and order in (1, 2) and not fail:
            return {}  # Original first two positive positions open automatically.
        self.serial += 1
        before = self.b.profile()
        self.packet = encode(1087, dict(serial_num=self.serial, flag=flag, order=order, id=identity, client_flag=pos))
        self.replies = self.b.respond(self.packet, {'authenticated': True})
        rows = [decode(x) for x in self.replies]
        events = [(d['id'], login_fields(d['data'])) for m, _, d in rows if m == 2998]
        self.assertEqual(rows[-1][0], 1106)
        self.assertEqual(rows[-1][2]['req_serial_num'], self.serial)
        if fail:
            self.assertEqual(events[0][0], 55)
            self.assertEqual(self.b.profile(), before)
        else:
            self.assertNotIn(55, [i for i, _ in events], events)
            self.assertEqual(events[-1][0], 95)
        return events[-1][1]

    def full(self, order=1):
        self.req(8, order)
        for _ in range(9):
            self.req(3, order)

    def open_positives(self):
        for order, name in enumerate(cheer.NAMES[:8], 1):
            if not self.b.profile()['cheer_' + name + '_level']:
                self.req(8, order)

    def move(self, flag, *changes):
        self.serial += 1
        packet = encode(1024, dict(serial_num=self.serial, flag=flag, count=len(changes),
                                  change_info=[dict(id=i, new_order=p) for i, p in changes]))
        rows = [decode(p) for p in self.b.respond(packet, {'authenticated': True})]
        self.assertFalse(any(m == 2998 and d['id'] == 55 for m, _, d in rows), rows)
        self.assertEqual(rows[-1][0], 1106)
        return rows

    def cheer_gain(self, role, identity):
        trace = role['combat_power_breakdown']['companions'][str(identity)]
        return {s: Decimal(trace['cheer'][s]) - Decimal(trace['pet'][s]) for s in cheer.STATS}

    def test_config_original_types_and_realm(self):
        cfg = login_fields(decode(self.b.bootstrap()[0])[2]['data'])
        self.assertIs(cfg[14]['is_open'], True)
        self.assertEqual(cfg[14]['is_open_ni'], 2)
        self.assertIsInstance(cfg[14]['cost_item_count'], int)
        self.assertEqual(list(cfg[14]['cheer_level_limit'].values()),
                         [40, 40] + [60] * 14)
        self.assertTrue(cfg[31][4]['rights']['open_cheer_skill'])

    def test_all_sixteen_positions_and_level_cap(self):
        role = self.b.profile(); role['level'] = 39; self.b.save(role)
        for order in range(1, 17):
            self.req(3, order, fail=True)
        role = self.b.profile(); role['level'] = 40; self.b.save(role)
        for order, name in enumerate(cheer.NAMES, 1):
            if 3 <= order <= 8:
                role = self.b.profile(); role['level'] = 60; self.b.save(role)
            if order == 9:
                for level in (40, 59):
                    role = self.b.profile(); role['level'] = level; self.b.save(role)
                    for reverse in range(9, 17):
                        self.req(8, reverse, fail=True)
                role = self.b.profile(); role['level'] = 60; self.b.save(role)
            self.full(order)
            self.req(3, order, fail=True)
            self.assertEqual(self.b.profile()['cheer_' + name + '_level'], 10)
        self.assertEqual(self.b.profile()['cheer_count'], 16)

    def test_first_two_positions_auto_unlock_at_40_without_materials(self):
        role = self.b.profile()
        role['level'] = 39
        role['cheer_heaven_level'] = role['cheer_earth_level'] = 0
        role['attachments'] = [i for i in role['attachments'] if i['type_id'] not in (1016, 1017)]
        self.b.save(role)
        self.assertEqual(self.b.profile()['cheer_count'], 0)
        self.req(8, 1, fail=True)
        self.req(8, 2, fail=True)
        role = self.b.profile()
        before_items = copy.deepcopy(role['attachments'])
        role['level'] = 40
        self.b.save(role)
        role = self.b.profile()
        self.assertEqual([role['cheer_' + n + '_level'] for n in cheer.NAMES], [1, 1] + [0] * 14)
        self.assertEqual(role['attachments'], before_items)
        for order in range(3, 9):
            self.req(8, order, fail=True)
        other = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        try:
            self.assertEqual(other.profile()['cheer_count'], 2)
            self.assertEqual(other.profile()['attachments'], before_items)
        finally:
            other.close()

    def test_positive_unlock_level_boundaries_cost_replay_and_reconnect(self):
        def token_counts(role):
            return {tid: sum(i['count'] for i in role['attachments'] if i['type_id'] == tid)
                    for tid in (1016, 1017)}

        for order, required_level in enumerate((60,) * 6, 3):
            with self.subTest(order=order, required_level=required_level):
                key = 'cheer_' + cheer.NAMES[order - 1] + '_level'
                role = self.b.profile()
                role['level'] = required_level - 1
                self.b.save(role)
                self.req(8, order, fail=True)  # Even with enough tokens, reject early.
                role = self.b.profile()
                role['level'] = required_level
                self.b.save(role)
                role = self.b.profile()
                self.assertEqual(role[key], 0)  # Level alone must not unlock paid slots.
                before = token_counts(role)
                tid = 1016 if order == 3 else 1017
                self.req(8, order)
                after = self.b.profile()
                self.assertEqual(after[key], 1)
                expected = dict(before)
                expected[tid] -= 1
                self.assertEqual(token_counts(after), expected)
                self.assertEqual(self.b.respond(self.packet, {'authenticated': True}), self.replies)
                self.assertEqual(self.b.profile(), after)
                self.req(8, order, fail=True)  # New requests cannot pay twice either.
        other = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        try:
            role = other.profile()
            self.assertEqual([role['cheer_' + n + '_level'] for n in cheer.NAMES], [1] * 8 + [0] * 8)
            self.assertEqual(token_counts(role), expected)
        finally:
            other.close()

    def test_all_paid_positive_positions_reject_old_level_thresholds(self):
        for level in (40, 42, 44, 46, 48, 50, 52, 59):
            role = self.b.profile(); role['level'] = level; self.b.save(role)
            for order in range(3, 9):
                with self.subTest(level=level, order=order):
                    self.req(8, order, fail=True)
            self.assertEqual(self.b.profile()['cheer_count'], 2)

    def test_unlock_gate_update_preserves_legacy_open_positions(self):
        role = self.b.profile()
        role['level'] = 50
        role.update(cheer_shake_level=7, shake_skill_level=100)
        self.b.save(role)
        before = self.b.profile()
        other = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        try:
            restored = other.profile()
            self.assertEqual(restored['cheer_shake_level'], 7)
            self.assertEqual(restored['shake_skill_level'], 100)
            self.assertEqual(restored['attachments'], before['attachments'])
            self.assertEqual(restored['cheer_targets'], before['cheer_targets'])
        finally:
            other.close()

    def test_paid_positive_positions_stay_locked_without_tokens(self):
        role = self.b.profile()
        role['attachments'] = [i for i in role['attachments'] if i['type_id'] not in (1016, 1017)]
        self.b.save(role)
        self.assertEqual(self.b.profile()['cheer_count'], 2)
        for order in range(3, 9):
            with self.subTest(order=order):
                # Earlier slots have been opened so this exercises missing materials.
                self.req(8, order, fail=True)
                role = self.b.profile()
                summon.add_item(role, 1016 if order == 3 else 1017, 1)
                self.b.save(role)
                self.req(8, order)
                self.assertFalse(any(i['type_id'] in (1016, 1017) and i['count'] > 0
                                     for i in self.b.profile()['attachments']))

    def test_explicit_target_switch_and_remove(self):
        self.req(8)
        base = self.b.profile()['corteges'][0]['gongji']
        self.req(1, identity=self.ids[1])
        self.assertEqual(self.b.profile()['corteges'][0]['gongji'], base)
        self.req(2, identity=self.ids[0])
        self.assertGreater(self.b.profile()['corteges'][0]['gongji'], base)
        self.req(2)
        self.assertEqual(self.b.profile()['corteges'][0]['gongji'], base)
        self.req(1)
        self.assertEqual(self.b.profile()['corteges'][1]['cheer_order'], 0)

    def test_reverse_target_conflicts_and_innate_uses_separate_inventory(self):
        self.open_positives()
        self.req(8); self.req(8, 9)
        self.req(1, identity=self.ids[1]); self.req(2, identity=self.ids[0])
        self.req(1, 9, self.ids[2]); self.req(2, 9, self.ids[0], fail=True)
        self.req(2)
        self.req(2, 9, self.ids[0])
        role = self.b.profile()
        self.assertEqual(role['cheer_heaven_effect'], 0)
        self.assertEqual(role['cheer_targets']['unheaven'], self.ids[0])
        self.assertTrue(all(v > 0 for v in self.cheer_gain(role, self.ids[0]).values()))
        innate = next(i for i in role['attachments'] if i.get('innate_owner_id') == self.ids[2])
        self.assertEqual(innate['equip_order'], 17)
        self.assertEqual(self.req(12, 9, self.ids[2])['skill_id'], innate['id'])
        self.req(12, 9, self.ids[1], fail=True)

    def test_wash_preview_cancel_confirm_and_reconnect(self):
        self.full()
        before = self.b.profile()['heaven_gongji_plus']
        result = self.req(4)
        self.assertEqual(self.req(7)['modify_value'], result['modify_value'])
        self.assertEqual(self.b.profile()['heaven_gongji_plus'], before)
        other = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.addCleanup(other.close)
        self.assertIn('1', other.profile()['cheer_pending'])
        self.req(5)
        self.assertEqual(self.req(7)['result'], 2)
        self.req(6, fail=True)
        self.req(4)
        before = self.b.profile()
        p = before['cheer_pending']['1']
        self.req(6)
        after = self.b.profile()
        self.assertEqual(after['heaven_' + cheer.STATS[p['src_index'] - 1] + '_plus'], before['heaven_' + cheer.STATS[p['src_index'] - 1] + '_plus'] - p['modify_value'])
        self.req(6, fail=True)

    def test_skill_slots_equip_upgrade_and_unload(self):
        self.req(8); self.req(1, identity=self.ids[1]); self.req(2, identity=self.ids[0])
        self.req(9, pos=2); self.req(9, pos=3)
        self.req(9, pos=2, fail=True)
        role = self.b.profile()
        item = dict(id=f.new_id(role), type_id=22, attach_type=6, count=1, level=1, equip_order=0, equip_pos=0)
        role['attachments'].append(item); self.b.save(role)
        before = self.b.profile()['role_combat_power']
        self.req(11, identity=item['id'], pos=2)
        self.assertGreater(self.b.profile()['role_combat_power'], before)
        self.req(11, identity=item['id'], pos=3, fail=True)
        self.req(10)
        self.assertEqual(self.b.profile()['heaven_skill_level'], 1)
        self.req(11, pos=2)
        self.assertEqual(self.b.profile()['role_combat_power'], before)

    def test_skill_wash_cancel_confirm_and_type_guard(self):
        self.full(); self.req(9, pos=2)
        self.req(13, pos=2)
        self.req(6, fail=True)
        self.req(14)
        self.req(13, pos=2)
        n = self.b.profile()['cheer_pending']['1']['plus_level']
        self.req(15)
        self.assertEqual(self.b.profile()['heaven_skill_level'], n)
        self.req(15, fail=True)

    def test_failed_cost_and_locked_material_atomic(self):
        role = self.b.profile()
        for i in role['attachments']:
            if i['type_id'] in (1016,1017): i['is_lock'] = 1
        self.b.save(role)
        self.req(8, 3, fail=True)
        self.req(8, 9, fail=True)

    def test_invalid_and_occupied_inputs(self):
        for flag, order in ((0,1), (16,1), (8,0), (8,17), (1,3)):
            self.req(flag, order, fail=True)
        self.req(8)
        self.req(8, fail=True)
        self.req(1, identity=self.ids[0], fail=True)
        self.req(2, identity=self.ids[1], fail=True)
        self.req(4, fail=True)
        self.req(9, pos=1, fail=True)

    def test_duplicate_serial_is_replayed_without_payment(self):
        self.req(8,3)
        before = self.b.profile()
        self.assertEqual(self.b.respond(self.packet, {'authenticated': True}), self.replies)
        self.assertEqual(self.b.profile(), before)
        old = encode(1087, dict(serial_num=self.serial, flag=3, order=1, client_flag=9))
        self.assertEqual(decode(self.b.respond(old, {'authenticated':True})[0])[2]['id'], 55)
        self.assertEqual(self.b.profile(), before)

    def test_reverse_skill_byte_cap(self):
        self.open_positives()
        self.full(); self.full(9); self.req(9, 9, pos=2)
        role = self.b.profile(); role['unheaven_skill_level'] = 500; self.b.save(role)
        self.req(10, 9, fail=True); self.req(13, 9, pos=2, fail=True)
        packets = [decode(packet) for packet in self.b.bootstrap()]
        self.assertEqual(next(d for m,_,d in packets if m == 1017)['unheaven_skill_level'], 255)
        self.assertTrue(any(a['type'] == 621 and a['value'] == 500 for m,_,d in packets if m == 1032 and d['unit_type'] == 1 for a in d['attr_list']))
        self.assertEqual(self.b.profile()['unheaven_skill_level'], 500)

    def test_free_initial_positions_and_sequential_unlock(self):
        role = self.b.profile()
        self.assertEqual((role['cheer_heaven_level'],role['cheer_earth_level']), (1,1))
        self.req(8,4,fail=True)
        self.req(8,3);self.req(8,4)
        self.req(8,11,fail=True)
        self.open_positives()
        self.req(8,9);self.req(8,10);self.req(8,11)

    def test_materials_purchase_and_inspection(self):
        from network_redirect import market, activity
        role = self.b.profile()
        goods = market.catalog(role, 1700000000, self.b.market_rules)['rich_item_list']
        for index in range(201,205):
            row = goods[index]
            before = sum(i['count'] for i in role['attachments'] if i['type_id'] == row['type_id'])
            market.buy(role, dict(page_id=2,index=index,count=2,type_id=row['type_id']),1700000000,self.b.market_rules)
            self.assertEqual(sum(i['count'] for i in role['attachments'] if i['type_id'] == row['type_id']),before+2*row['count'])
        self.b.save(role)
        self.req(1,identity=self.ids[1]);self.req(2,identity=self.ids[0])
        role = self.b.profile();activity.prepare(role,1700000000,self.b.activity_rules)
        packet = activity.query_lineup(role,dict(des_id=role['role_id'],des_type=1),self.b.activity_rules)[0]
        data = login_fields(decode(packet)[2]['data'])
        self.assertEqual(data['owner_cheer_info'][171],1)
        self.assertEqual(data['cheer_cortege'][1]['id'],self.ids[1])
        self.assertTrue(any(i['order']==9 for i in data['skill_list'].values()))
        role['level']=39
        self.assertFalse(cheer.market_goods(role))
        role['level']=40
        self.assertEqual(len(cheer.market_goods(role)), 4)

    def test_target_moves_to_empty_slot_without_losing_binding(self):
        self.req(1,identity=self.ids[1]);self.req(2,identity=self.ids[0])
        role=self.b.profile()
        f.change_order(role,dict(flag=5,count=1,change_info=[dict(id=self.ids[0],new_order=2)]))
        f.prepare(role,self.b.formation_rules)
        self.assertEqual(role['cheer_heaven_effect'],2)
        self.assertEqual(role['cheer_targets']['heaven'], self.ids[0])

    def test_all_sixteen_slots_share_one_target_occupancy(self):
        self.open_positives()
        for order in range(9, 17):
            self.req(8, order)
        for order, name in enumerate(cheer.NAMES, 1):
            with self.subTest(order=order):
                self.req(1, order, self.ids[1])
                self.req(2, order, self.ids[0])
                self.req(2, order, self.ids[0])  # Re-selecting the same binding is valid.
                for other in (1, 2, 9, 16):
                    if other != order:
                        self.req(2, other, self.ids[0], fail=True)
                self.assertEqual(self.b.profile()['cheer_targets'][name], self.ids[0])
                self.req(1, order)  # Removing a supporter also releases its target.
                self.assertEqual(self.b.profile()['cheer_targets'][name], 0)

    def test_distinct_targets_and_retargeting_release_previous_target(self):
        self.move(5, (self.ids[2], 2))
        self.req(1, identity=self.ids[1])
        self.req(2, identity=self.ids[0])
        self.req(2, identity=self.ids[2])
        self.req(2, 2, self.ids[0])
        role = self.b.profile()
        self.assertEqual((role['cheer_targets']['heaven'], role['cheer_targets']['earth']),
                         (self.ids[2], self.ids[0]))
        self.req(2, 2, self.ids[2], fail=True)

    def test_swap_keeps_each_support_and_spell_bonus_with_companion(self):
        self.move(5, (self.ids[2], 2))
        self.req(1, identity=self.ids[1]); self.req(2, identity=self.ids[0])
        self.req(9, pos=2)
        role = self.b.profile()
        item = dict(id=f.new_id(role), type_id=22, attach_type=6, count=1,
                    level=1, equip_order=0, equip_pos=0)
        role['attachments'].append(item); self.b.save(role)
        self.req(11, identity=item['id'], pos=2)
        before = self.cheer_gain(self.b.profile(), self.ids[0])
        self.assertTrue(any(before.values()))
        for flag, changes in ((5, ((self.ids[0], 2), (self.ids[2], 1))),
                              (4, ((self.ids[0], 1),)),
                              (0, ((self.ids[0], 2), (self.ids[2], 1)))):
            with self.subTest(flag=flag):
                rows = self.move(flag, *changes)
                role = self.b.profile()
                target = f.lookup(role, 'corteges', self.ids[0])
                self.assertEqual(self.cheer_gain(role, self.ids[0]), before)
                self.assertFalse(any(self.cheer_gain(role, self.ids[2]).values()))
                self.assertEqual(role['cheer_heaven_effect'], target['order'])
                self.assertTrue(any(a == dict(type=171, value=target['order'])
                                    for m, _, d in rows if m == 1032 and d['unit_type'] == 1
                                    for a in d['attr_list']))
                self.assertEqual(cheer.inspection(role)['owner_cheer_info'][171], target['order'])

    def test_replacement_suspends_binding_and_return_restores_after_restart(self):
        self.req(1, identity=self.ids[1]); self.req(2, identity=self.ids[0])
        gain = self.cheer_gain(self.b.profile(), self.ids[0])
        self.move(4, (self.ids[2], 1))
        role = self.b.profile()
        self.assertEqual(role['cheer_heaven_effect'], 0)
        self.assertEqual(role['cheer_targets']['heaven'], self.ids[0])
        self.assertFalse(any(self.cheer_gain(role, self.ids[2]).values()))
        other = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        try:
            self.assertEqual(other.profile()['cheer_targets'], role['cheer_targets'])
        finally:
            other.close()
        self.move(4, (self.ids[0], 1))
        self.assertEqual(self.cheer_gain(self.b.profile(), self.ids[0]), gain)
        self.req(2, 2, self.ids[0], fail=True)

    def test_two_supported_companions_swap_without_exchanging_bonuses(self):
        self.move(5, (self.ids[2], 2))
        role = self.b.profile()
        second = summon.companion(role, 5005)
        role['corteges'].append(second); self.b.save(role)
        self.req(1, identity=self.ids[1]); self.req(2, identity=self.ids[0])
        self.req(1, 2, second['id']); self.req(2, 2, self.ids[2])
        before = self.b.profile()
        gains = {i: self.cheer_gain(before, i) for i in (self.ids[0], self.ids[2])}
        self.assertTrue(all(any(v.values()) for v in gains.values()))
        self.move(5, (self.ids[0], 2), (self.ids[2], 1))
        after = self.b.profile()
        for identity, gain in gains.items():
            self.assertEqual(self.cheer_gain(after, identity), gain)
        self.assertEqual((after['cheer_heaven_effect'], after['cheer_earth_effect']), (2, 1))

    def test_legacy_slot_bindings_migrate_once_and_remove_duplicates(self):
        self.open_positives(); self.req(8, 9)
        role = self.b.profile()
        role.pop('cheer_targets')
        role.update(cheer_heaven_effect=1, cheer_earth_effect=1,
                    cheer_unheaven_effect=1, cheer_pool_effect=8)
        original_items = copy.deepcopy(role['attachments'])
        peak = role['max_combat_power'] = 9999999
        self.b.db.execute('UPDATE roles SET data=? WHERE account=?',
                          (json.dumps(role), self.b.account))
        self.b.db.commit()
        role = self.b.profile()
        self.assertEqual(role['cheer_targets']['heaven'], self.ids[0])
        for name in ('earth', 'unheaven', 'pool'):
            self.assertEqual(role['cheer_targets'][name], 0)
            self.assertEqual(role['cheer_' + name + '_effect'], 0)
        self.assertEqual(role['attachments'], original_items)
        self.assertEqual(role['max_combat_power'], peak)
        self.move(5, (self.ids[0], 2))
        other = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        try:
            restored = other.profile()
            self.assertEqual(restored['cheer_targets']['heaven'], self.ids[0])
            self.assertEqual(restored['cheer_heaven_effect'], 2)
            wire = [decode(p) for p in other.bootstrap(reconnect=True)]
            self.assertTrue(any(a == dict(type=171, value=2)
                                for m, _, d in wire if m == 1032 and d['unit_type'] == 1
                                for a in d['attr_list']))
        finally:
            other.close()

    def test_deleted_target_does_not_rebind_to_new_occupant(self):
        self.req(1, identity=self.ids[1]); self.req(2, identity=self.ids[0])
        role = self.b.profile()
        role['corteges'] = [c for c in role['corteges'] if c['id'] != self.ids[0]]
        f.lookup(role, 'corteges', self.ids[2])['order'] = 1
        cheer.prepare(role)
        self.assertEqual(role['cheer_targets']['heaven'], 0)
        self.assertEqual(role['cheer_heaven_effect'], 0)
        # Wire fields are derived after migration, never a new binding source.
        role['cheer_heaven_effect'] = 1
        cheer.prepare(role)
        self.assertEqual(role['cheer_heaven_effect'], 0)

    def test_no_recalculation_feedback(self):
        self.req(8); self.req(1, identity=self.ids[1]); self.req(2, identity=self.ids[0])
        role = self.b.profile(); power = role['role_combat_power']
        for _ in range(4):
            self.b.save(role); role = self.b.profile()
            self.assertEqual(role['role_combat_power'], power)

    def test_reverse_entry_requires_all_positive_positions_and_first_reverse(self):
        # An open corresponding positive position alone was incorrectly sufficient.
        self.req(8, 9, fail=True)
        self.open_positives()
        self.req(8, 10, fail=True)
        self.req(8, 9)
        self.req(8, 11, fail=True)
        self.req(8, 10)
        self.req(8, 11)

    def test_reverse_level_and_feature_switches_are_atomic(self):
        self.open_positives()
        role = self.b.profile(); role['level'] = 59; self.b.save(role)
        self.req(8, 9, fail=True)
        role = self.b.profile(); role['level'] = 60; self.b.save(role)
        self.b.cheer_rules['is_open_ni'] = 0
        self.req(8, 9, fail=True)
        self.b.cheer_rules['is_open_ni'] = 1
        self.req(8, 9)
        self.req(1, 9, self.ids[1]); self.req(2, 9, self.ids[0])
        for flag in (3, 4, 7, 9, 10, 11, 13):
            self.req(flag, 9, pos=2, fail=True)
        self.b.cheer_rules['is_open_ni'] = 2
        self.req(3, 9)
        self.req(9, 9, pos=2)

    def test_reverse_full_upgrade_cost_and_rates(self):
        self.open_positives()
        before = self.b.profile()
        for order in range(9, 17):
            self.full(order)
        after = self.b.profile()
        def count(role, tid):
            return sum(i['count'] for i in role['attachments'] if i['type_id'] == tid)
        self.assertEqual(count(before, 1015) - count(after, 1015), 8 * 1300)
        self.assertEqual(count(before, 1017) - count(after, 1017), 8 * 2)
        for name in cheer.NAMES[8:]:
            self.assertEqual([after[name + '_' + s + '_plus'] for s in cheer.STATS], [175, 175, 275, 175])

    def test_all_reverse_skill_bits_and_equipment_positions_are_independent(self):
        self.open_positives()
        for order in range(9, 17):
            self.req(8, order)
            for pos in (2, 3):
                self.req(9, order, pos=pos)
                role = self.b.profile()
                item = dict(id=f.new_id(role), type_id=22, attach_type=6, count=1,
                            level=1, equip_order=0, equip_pos=0)
                role['attachments'].append(item); self.b.save(role)
                self.req(11, order, item['id'], pos)
                self.assertEqual(next(i for i in self.b.profile()['attachments'] if i['id'] == item['id'])['equip_order'], order + 8)
                self.req(11, order, pos=pos)
        self.assertEqual(self.b.profile()['cheer_skill_ni_open'], 131070)
        self.assertEqual(self.b.profile()['cheer_skill_open'], 0)

    def test_reverse_wash_reconnect_and_skill_500_cap(self):
        self.open_positives(); self.full(9); self.req(9, 9, pos=2)
        with patch.object(cheer.secrets, 'randbelow', return_value=0), patch.object(cheer.secrets, 'choice', return_value=3):
            self.req(4, 9)
        self.req(6, 1, fail=True)
        self.req(15, 9, fail=True)
        saved = self.b.profile()
        other = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        try:
            self.assertEqual(other.profile()['cheer_pending'], saved['cheer_pending'])
        finally:
            other.close()
        self.req(6, 9)
        role = self.b.profile()
        self.assertEqual((role['unheaven_gongji_plus'], role['unheaven_hp_plus']), (170, 280))
        role['unheaven_skill_level'] = 499; self.b.save(role)
        with patch.object(cheer.secrets, 'randbelow', return_value=4):
            self.assertEqual(self.req(13, 9, pos=2)['plus_level'], 1)
        self.req(10, 9, fail=True)
        self.req(15, 9)
        self.assertEqual(self.b.profile()['unheaven_skill_level'], 500)
        self.req(15, 9, fail=True)
        self.req(13, 9, pos=2, fail=True)

    def test_legacy_skill_mask_migration_is_persistent_and_idempotent(self):
        role = self.b.profile()
        role.pop('cheer_skill_mask_version')
        role.update(cheer_skill_open=1, cheer_skill_ni_open=32769)
        self.b.save(role)
        for _ in range(3):
            role = self.b.profile()
            self.assertEqual((role['cheer_skill_open'], role['cheer_skill_ni_open']), (2, 65538))
            self.assertTrue(cheer.skill_open(role, 9, 2))
            self.assertTrue(cheer.skill_open(role, 16, 3))
            self.assertFalse(cheer.skill_open(role, 9, 3))
            self.assertEqual(role['cheer_skill_mask_version'], 2)
            self.b.save(role)
        other = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        try:
            self.assertEqual(other.profile()['cheer_skill_ni_open'], 65538)
        finally:
            other.close()

    def test_closed_reverse_position_and_skill_slot_cannot_grant_stale_bonuses(self):
        role = self.b.profile()
        target, supporter = role['corteges'][:2]
        supporter.update(order=0, cheer_order=9)
        role.update(cheer_unheaven_effect=target['order'], unheaven_gongji_plus=175)
        role['cheer_targets']['unheaven'] = target['id']
        role['attachments'].append(dict(type_id=22, equip_order=17, equip_pos=2, level=1))
        pending = {c['id']: dict.fromkeys(cheer.STATS, Decimal(1000)) for c in (target, supporter)}
        values = dict.fromkeys(cheer.STATS, Decimal(0))
        cheer.bonuses(role, target, values, pending)
        self.assertEqual(sum(values.values()), 0)
        role['cheer_unheaven_level'] = 1
        cheer.bonuses(role, target, values, pending)
        self.assertEqual(values['gongji'], 175)
        role['cheer_skill_ni_open'] = 2
        opened = dict.fromkeys(cheer.STATS, Decimal(0))
        cheer.bonuses(role, target, opened, pending)
        self.assertGreater(sum(opened.values()), sum(values.values()))

if __name__ == '__main__': unittest.main()
