"""Original binary equipment requests against a disposable database."""
import copy
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch
from network_redirect import formation as f, equipment as e, summon, reborn
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode


class EquipmentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **kw: None)
        self.addCleanup(lambda: self.b.close())
        self.serial = 10000
        role = self.b.profile(); role.update(level=99, silver_coin=1000000000, reborn_layer=4)
        for t in (1093, 1333, 1369, 1310, 1311, 1312, 1313, 1314, 1320, 1321, 1322, 1323, 1334, 1335):
            summon.add_item(role, t, 100000)
        self.b.save(role)

    def add(self, tid, **kw):
        role = self.b.profile(); ident = f.new_id(role)
        item = dict(id=ident, attach_type=5, type_id=tid, count=1, level=1)
        item.update(kw); role['attachments'].append(item); self.b.save(role)
        return ident

    def gear(self, main=1, quality=5, **kw):
        tid = next(t for t, r in f.ITEMS.items() if int(r['main_type']) == main and int(r['quality']) == quality)
        return self.add(tid, **kw)

    def get(self, ident):
        return next(i for i in self.b.profile()['attachments'] if i['id'] == ident)

    def req(self, mid, **kw):
        self.serial += 1; self.packet = encode(mid, dict(serial_num=self.serial, **kw))
        self.replies = self.b.respond(self.packet, {'authenticated': True})
        self.decoded = [decode(p) for p in self.replies]
        self.assertEqual(self.decoded[-1][0], 1106)
        return [(d['id'], login_fields(d['data'])) for m, _, d in self.decoded if m == 2998]

    def stone(self, op, target, ids=(), pos=0, order=0):
        return self.req(1054, flag=op, des_id=target, stone_pos=pos, equip_order=order,
                        src_count=len(ids), src_list=[dict(id=i) for i in ids])

    def test_drill_mosaic_upgrade_remove_all_types_and_persistence(self):
        for main in (1, 2, 3):
            gear = self.gear(main, level=80, equip_order=1, equip_pos=main)
            stone = self.add(1089 + main)
            self.assertEqual(self.stone(1, gear, order=1)[-1][0], 83)
            before = self.b.profile()['corteges'][0][{1:'gongji',2:'fangyu',3:'hp'}[main]]
            self.assertEqual(self.stone(2, gear, [stone], 1, 1)[-1][1]['result'], 1)
            self.assertEqual(self.get(stone)['owner_id'], gear)
            self.assertEqual(self.get(gear)['stone1_level'], 1)
            self.assertGreater(self.b.profile()['corteges'][0][{1:'gongji',2:'fangyu',3:'hp'}[main]], before)
            mats = [self.add(1090) for _ in range(3)]
            self.assertEqual(self.stone(3, stone, mats, 1, 1)[-1][1]['result'], 1)
            self.assertEqual(self.get(gear)['stone1_level'], 2)
            self.assertFalse(any(m == 1035 and d['first_send'] for m, _, d in self.decoded))
            self.assertEqual(self.stone(4, gear, [stone], 1, 1)[-1][1]['result'], 1)
            self.assertEqual(self.get(gear)['stone1_level'], 0)
            self.assertEqual(self.get(stone)['level'], 2)
            self.assertEqual(self.get(stone)['owner_id'], 0)
        expected = self.b.profile(); self.b.close()
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **kw: None)
        self.assertEqual(expected, self.b.profile())

    def test_failure_compensation_replay_and_success_reset(self):
        stone = self.add(1090); mat = self.add(1091)
        with patch.object(e.secrets, 'randbelow', return_value=999999):
            self.assertEqual(self.stone(3, stone, [mat])[-1][1]['result'], 6)
        self.assertEqual(self.get(stone)['prob_compen'], 5)
        role = self.b.profile()
        self.assertEqual(self.b.respond(self.packet, {'authenticated': True}), self.replies)
        self.assertEqual(role, self.b.profile())
        mats = [self.add(1092) for _ in range(3)]
        self.assertEqual(self.stone(3, stone, mats)[-1][1]['result'], 1)
        self.assertEqual(self.get(stone)['prob_compen'], 0)

    def test_invalid_operations_roll_back(self):
        gear = self.gear(); stone = self.add(1090); locked = self.add(1090, is_lock=1)
        for op, target, ids, pos in [(2, gear, [stone], 1), (3, stone, [stone], 0),
                                    (3, stone, [locked], 0), (3, stone, [locked, locked], 0),
                                    (5, stone, [], 0), (4, gear, [stone], 1)]:
            before = self.b.profile()
            self.assertEqual(self.stone(op, target, ids, pos)[-1][0], 55)
            self.assertEqual(before, self.b.profile())
        self.stone(1, gear)
        wrong = self.add(1091)
        before = self.b.profile(); self.assertEqual(self.stone(2, gear, [wrong], 1)[-1][0], 55)
        self.assertEqual(before, self.b.profile())

    def test_every_socket_limit_and_stale_owner(self):
        for quality in sorted({int(r["quality"]) for r in f.ITEMS.values() if int(r["main_type"]) == 1}):
            gear = self.gear(quality=quality)
            for _ in range({1:1,2:1,3:1,4:2,5:3}[quality]):
                self.assertEqual(self.stone(1, gear)[-1][0], 83)
            before = self.b.profile(); self.assertEqual(self.stone(1, gear)[-1][0], 55)
            self.assertEqual(before, self.b.profile())
        stone = self.add(1090); self.stone(2, gear, [stone], 1)
        before = self.b.profile(); self.assertEqual(self.stone(3, stone, [self.add(1091)], 1, 2)[-1][0], 55)
        self.assertEqual(self.get(stone), next(i for i in before['attachments'] if i['id'] == stone))

    def test_reborn_and_refine_exact_level_costs(self):
        for main in (1,2,3):
            tid = main + 1089; gear = self.gear(main, drill_count=1)
            stone = self.add(tid, level=10); self.stone(2, gear, [stone], 1)
            before = self.b.profile(); self.assertEqual(self.stone(5, stone, pos=1)[-1][0], 55)
            self.assertEqual(before, self.b.profile())
            self.add(tid, level=10)
            self.assertEqual(self.stone(5, stone, pos=1)[-1][1]['result'], 1)
            self.assertEqual(self.get(gear)['stone1_level'], 11)
            self.add(tid, level=11)
            self.assertEqual(self.stone(5, stone, pos=1)[-1][1]['result'], 1)
            self.assertEqual(self.get(gear)['stone1_level'], 12)
            self.assertEqual(self.stone(5, stone, pos=1)[-1][0], 55)

    def test_all_normal_stone_levels_and_prices(self):
        for kind in (1,2,3):
            for level in range(1,10):
                stone = self.add(kind + 1089, level=level)
                mat = self.add(1090, level=10)
                before = self.b.profile()['silver_coin']
                self.assertEqual(self.stone(3, stone, [mat])[-1][1]['result'], 1)
                self.assertEqual(self.get(stone)['level'], level + 1)
                self.assertEqual(before-self.b.profile()['silver_coin'], int(e.STONE_VALUES[kind,level]['silver_cost']))

    def test_original_equipment_components_exhaustive(self):
        for tid, cfg in f.ITEMS.items():
            main = int(cfg['main_type'])
            if main not in (1,2,3): continue
            for level in (1, 37, int(cfg['top_level'])):
                item = dict(type_id=tid, level=level)
                basic = sum(Decimal(cfg[k]) for k in ('gongji_plus','fangyu_plus','maxhp_plus'))
                growth = Decimal(cfg['upgrade_plus']) * (level-1)
                self.assertEqual(e.effect(item), int(basic+growth))
                if int(cfg['quality']) != 5: continue
                item.update(reborn_bit=1, cast_level=4, advance_level=10, star_count=0)
                base = basic + growth * Decimal('1.12')
                flat = {1:525,2:259,3:1260}[main]
                advance_flat = {1:791,2:355,3:1646}[main]
                for sl in range(1,13):
                    item['stone1_level'] = sl
                    expected = int(base)+int(base*e.stone_rate(main,sl))+int(base*Decimal('1.05')+advance_flat)+int(base*Decimal('.5')+flat)
                    self.assertEqual(e.effect(item), expected, (tid, level, sl))

    def test_companion_rebirth_does_not_reapply_equipment_multipliers(self):
        gear = self.gear(level=1, reborn_bit=1, cast_level=4)
        values = {s:Decimal(1000) for s in f.STATS}
        reborn.bonuses({}, {}, values, [self.get(gear)])
        self.assertEqual(values, {s:Decimal(1000) for s in f.STATS})

    def test_split_legacy_stack_and_individual_rewards(self):
        gear = self.gear(drill_count=1); stone = self.add(1090, count=5)
        self.assertEqual(self.stone(2, gear, [stone], 1)[-1][0], 83)
        self.assertEqual(self.get(stone)['count'], 1)
        self.assertTrue(any(m == 1035 and not d['first_send'] for m,_,d in self.decoded))
        role = self.b.profile(); self.assertEqual(sum(i['count'] for i in role['attachments'] if i['type_id'] == 1090), 5)
        summon.add_item(role, 1091, 3)
        self.assertEqual([i['count'] for i in role['attachments'] if i['type_id'] == 1091], [1,1,1])

    def test_full_advance_and_enhancement_limits(self):
        for main in (1,2,3):
            gear = self.gear(main)
            for tier in range(10):
                for star in range(1,8):
                    self.assertEqual(self.req(1073, flag=1, equip_order=0, is_one_key=True, equip_id=gear)[-1][0], 115)
                    self.assertEqual(self.get(gear)['star_count'], star)
                self.assertEqual(self.req(1073, flag=2, equip_order=0, is_one_key=False, equip_id=gear)[-1][0], 115)
                self.assertEqual(self.get(gear)['advance_level'], tier+1)
            before = self.b.profile()
            self.assertEqual(self.req(1073, flag=1, equip_order=0, is_one_key=True, equip_id=gear)[-1][0], 55)
            self.assertEqual(before, self.b.profile())
        role = self.b.profile(); role.update(level=2, vip_level=3)
        item = next(i for i in role['attachments'] if i['id'] == gear); item['level'] = 3
        self.b.save(role)
        with patch.object(summon, 'weighted_choice', return_value=5):
            self.assertEqual(self.req(1052, equip_order=0, inbatch=True, equip_id=gear)[-1][0], 2)
        self.assertEqual(self.get(gear)['level'], 4)

    def test_successive_enhancement_batches_stop_below_cap_and_can_continue(self):
        gear = self.gear(main=1)
        role = self.b.profile()
        role['vip_level'] = 3
        self.b.save(role)
        for start in (1, 11):
            before = self.b.profile()
            with patch.object(summon, 'weighted_choice', return_value=1):
                events = dict(self.req(1052, equip_order=0, inbatch=True, equip_id=gear))
            self.assertNotIn(55, events)
            steps = events[2]['upgrade_list']
            self.assertEqual(len(steps), 10)
            self.assertEqual(steps[1]['old_level'], start)
            self.assertEqual(steps[10]['new_level'], start+10)
            after = self.b.profile()
            item = self.get(gear)
            self.assertEqual(item['level'], start+10)
            quality = int(f.ITEMS[item['type_id']]['quality'])
            cost = sum(int(f.EQUIP_COST[lv][f'star{quality}_money']) for lv in range(start, start+10))
            self.assertEqual(after['silver_coin'], before['silver_coin']-cost)
            self.assertLess(item['level'], min(int(f.ITEMS[item['type_id']]['top_level']), after['level']*2))
            self.assertEqual(self.b.respond(self.packet, {'authenticated': True}), self.replies)
            self.assertEqual(self.b.profile(), after)

    def test_realm_level_and_currency_gates_are_atomic(self):
        stone = self.add(1090); mat = self.add(1091)
        role = self.b.profile(); role['silver_coin']=0; self.b.save(role)
        before = self.b.profile(); self.assertEqual(self.stone(3,stone,[mat])[-1][0],55)
        self.assertEqual(before,self.b.profile())
        role['level']=9; self.b.save(role); gear=self.gear()
        before=self.b.profile();self.assertEqual(self.stone(1,gear)[-1][0],55)
        self.assertEqual(before,self.b.profile())
        role=self.b.profile();role.update(level=99,reborn_layer=0);self.b.save(role)
        stone=self.add(1090,level=10);self.add(1090,level=10)
        before=self.b.profile();self.assertEqual(self.stone(5,stone)[-1][0],55)
        self.assertEqual(before,self.b.profile())
        config=login_fields(decode(self.b.bootstrap()[0])[2]['data'])
        self.assertTrue(config[11]['open_flag'])
        self.assertFalse(config[31][0]['rights']['open_stone_sys'])
        self.assertTrue(config[31][1]['rights']['open_stone_sys'])

    def test_stack_and_locked_materials_are_not_debited_on_late_failure(self):
        stone=self.add(1090,level=10,count=3)
        role=self.b.profile()
        for i in role['attachments']:
            if i['type_id']==1333:i['is_lock']=1
        self.b.save(role)
        before=self.b.profile();self.assertEqual(self.stone(5,stone)[-1][0],55)
        self.assertEqual(before,self.b.profile())

    def test_unworn_equipment_refreshes_and_recalculation_is_idempotent(self):
        gear=self.gear(level=50,advance_level=10)
        self.assertEqual(self.req(1328,reborn_type=3,id=5,data=summon.lua(dict(equip_id=gear,equip_order=0)))[-1][0],172)
        item=self.get(gear);self.assertEqual(item['effect_value'],e.effect(item))
        role=self.b.profile();again=copy.deepcopy(role)
        for _ in range(3):f.prepare(again,self.b.formation_rules)
        self.assertEqual(role,again)
