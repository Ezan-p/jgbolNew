"""Crafting binary protocol, original table pricing, rollback and replay."""
import copy
import unittest
from unittest.mock import patch
from decimal import Decimal
from tests import test_equipment as original
from network_redirect import equipment_crafting as c, formation as f, equipment, summon
from network_redirect.protocol import decode


class CraftingTests(unittest.TestCase):
    setUp = original.EquipmentTests.setUp
    add = original.EquipmentTests.add
    gear = original.EquipmentTests.gear
    get = original.EquipmentTests.get
    req = original.EquipmentTests.req

    def convert(self, flag, ids, num=1, des=1):
        return self.req(1074, flag=flag, num=num, des_type=des, count=len(ids), id_list=[dict(id=i) for i in ids])

    def compose(self, item, op=1, target=None, ids=None):
        cfg = f.ITEMS[self.get(item)['type_id']]
        return self.req(1053, compose_type=op, equip_type=int(cfg['sub_type']) if target is None else target,
            equip_quality=int(cfg['quality']) if target is None else int(f.ITEMS[target]['quality']),
            material_quality=int(cfg['quality']), material_count=len(ids or [item]), material_list=[dict(id=i) for i in (ids or [item])])

    def test_query_and_random_and_named_fragments(self):
        for flag in (0, 1):
            events = self.req(1055, flag=flag)
            self.assertEqual([x[0] for x in events], [98, 7])
            self.assertEqual(events[-1][1]['show'], flag == 0)
        for tid in (6001, 6002, 6003, 6004):
            source = self.add(tid, count=80)
            before = self.b.profile()
            event = self.compose(source)[-1]
            self.assertEqual(event[0], 6)
            self.assertEqual(self.get(source)['count'], 40)
            cfg, src = c.recipe_for(self.get(source), 2)
            self.assertIn(event[1]['equip_type'], [x[1] for x in c.parts(cfg[c.DEST])])
            expected = int(c.parts(cfg[c.COST])[0][3])
            self.assertEqual(before['silver_coin'] - self.b.profile()['silver_coin'], expected)
            self.assertEqual(self.compose(source)[-1][0], 6)
            self.assertFalse(any(i['id'] == source for i in self.b.profile()['attachments']))
        self.assertTrue(all(i['count'] == 1 for i in self.b.profile()['attachments'] if i['attach_type']==5 and int(f.ITEMS[i['type_id']]['main_type']) in (1,2,3)))

    def test_appoint_exchange_and_limits(self):
        self.add(1008, count=2)
        ids = [self.gear(quality=4) for _ in range(5)]
        event = self.compose(ids[0], 2, 2001, ids)
        self.assertEqual(event[-1][0], 6)
        ids = [self.gear(quality=4) for _ in range(5)]
        before = self.b.profile()
        self.assertEqual(self.compose(ids[0], 2, 2001, ids)[-1][0], 55)
        self.assertEqual(before, self.b.profile())
        self.assertEqual(self.compose(ids[0], 3, 6002, ids)[-1][0], 6)
        self.assertEqual(self.b.profile()['equipment_forge']['exchanged'], 1)
        self.assertEqual(sum(i['count'] for i in self.b.profile()['attachments'] if i['type_id']==6002), 40)

    def test_convert_every_original_material_recipe_both_directions(self):
        # Every progression/shard/essence recipe, not a hand-picked happy path.
        checked = 0
        for row in c.RECIPES:
            src = c.parts(row[c.SRC])[0]
            ident = self.add(src[1], level=src[2], count=src[3]*2)
            flag = 3 if int(row['category']) >= 100 else 2
            event = self.convert(flag, [ident], 2)[-1]
            self.assertEqual(event[0], 116, (src, event))
            from network_redirect import item_rewards
            allowed = {x[:3] for x in item_rewards.recipe_destinations(row, src[1])}
            self.assertTrue(all((x['object_type'], x['attach_type'], x['attach_level']) in allowed for x in event[1]['item_list'].values()))
            checked += 1
        self.assertGreater(checked, 60)

    def test_recycle_original_base_and_investment_rate(self):
        for main in (1, 2, 3):
            for quality in (4, 5):
                item = self.gear(main, quality, level=3, advance_level=1, star_count=1, cur_spirit_count=1)
                original = self.get(item)
                totals, silver = c.invested(original)
                row = c.RECYCLE[quality]
                expected = [(5, t, 1, f.floor(n * Decimal('.8'))) for t,n in totals.items() if f.floor(n * Decimal('.8'))]
                expected += c.parts(row['is_fabao']) if main==3 else [(5,int(row['des_type']),1,int(row['des_count']))]+c.parts(row['attach_list'])
                event = self.convert(1,[item])[-1]
                self.assertEqual(event[0],116)
                got = event[1]['item_list'].values()
                for tid in {x[1] for x in expected}:
                    self.assertEqual(sum(x['attach_count'] for x in got if x['object_type']==5 and x['attach_type']==tid), sum(x[3] for x in expected if x[1]==tid))

    def test_transform_preserves_growth_and_returns_stones(self):
        for state in (1, 2):
            gear = self.add(2001, level=50, advance_level=3, star_count=2, cur_spirit_count=1, drill_count=2, stone1_level=10)
            stone = self.add(1090, level=10, owner_id=gear, equip_pos=1)
            self.add(1100)
            with patch.object(c.secrets, 'choice', side_effect=lambda candidates:candidates[-1]):
                event = self.req(1225, state=state, item_id=gear)[-1]
            self.assertEqual(event[0],124)
            new = self.get(event[1]['item_id'])
            self.assertEqual(int(f.ITEMS[new['type_id']]['main_type']), state)
            self.assertEqual((new['level'],new['advance_level'],new['star_count'],new['drill_count']), (50,3,2,2))
            self.assertEqual(new['stone1_level'],0)
            self.assertEqual(self.get(stone)['owner_id'],0)
            self.assertEqual(new['effect_value'],equipment.effect(new))

    def test_six_star_doubles_base_refunds_and_updates_worn_stats(self):
        target = self.add(2001, level=20, equip_order=1, equip_pos=1)
        material = self.add(2001, level=5, advance_level=2, star_count=3, cur_spirit_count=1, drill_count=1, stone1_level=5)
        stone = self.add(1090, level=5, owner_id=material, equip_pos=1)
        before = self.b.profile()
        base = equipment.base_effect(self.get(target))
        events = self.req(1079, equipid=target, equip_order=1, material_equipid=material)
        self.assertEqual(events[-1][0],201)
        self.assertEqual(self.get(target)['star_level'],1)
        self.assertEqual(equipment.base_effect(self.get(target)),base*2)
        self.assertEqual(self.get(stone)['owner_id'],0)
        self.assertGreater(self.b.profile()['corteges'][0]['gongji'],before['corteges'][0]['gongji'])
        attrs = [a for m,_,d in self.decoded if m==1032 and d['id']==target for a in d['attr_list']]
        self.assertIn(dict(type=117,value=1),attrs)
        self.assertTrue(events[-1][1]['attach_list'])
        self.assertEqual(self.b.respond(self.packet,{'authenticated':True}),self.replies)
        other = self.add(2001)
        before = self.b.profile()
        self.assertEqual(self.req(1079,equipid=target,equip_order=1,material_equipid=other)[-1][0],55)
        self.assertEqual(before,self.b.profile())

    def test_batch_sale_price_and_atomic_validation(self):
        ids = [self.gear(quality=q,level=10) for q in (2,3)]
        expected = sum(f.floor(Decimal(c.SELL[c.gear(self.get(i))[1]]['base_sell_price'])+Decimal('.45')*c.invested(self.get(i))[1]) for i in ids)
        before = self.b.profile()['silver_coin']
        self.assertEqual(self.req(1056,data=summon.lua(dict(equip_list=ids)))[-1][0],16)
        self.assertEqual(self.b.profile()['silver_coin']-before,expected)
        good = self.gear(quality=3); locked = self.gear(quality=3,is_lock=1)
        for selected in ([good,locked],[good,good],[99999999],[]):
            before = self.b.profile()
            self.assertEqual(self.req(1056,data=summon.lua(dict(equip_list=selected)))[-1][0],55)
            self.assertEqual(before,self.b.profile())

    def test_insufficient_currency_bad_ids_and_level_are_atomic(self):
        source = self.add(1313,count=10)
        for flag, ids, num, des in ((2,[source,source],1,1),(2,[source],0,1),(2,[source],2,1),(3,[source],1,1),(2,[source],1,1314)):
            before = self.b.profile()
            self.assertEqual(self.convert(flag,ids,num,des)[-1][0],55)
            self.assertEqual(before,self.b.profile())
        role = self.b.profile(); role['silver_coin']=0;self.b.save(role)
        before = self.b.profile()
        self.assertEqual(self.convert(2,[source])[-1][0],55)
        self.assertEqual(before,self.b.profile())
        role=self.b.profile();role.update(level=1,silver_coin=100000);self.b.save(role)
        before=self.b.profile()
        self.assertEqual(self.convert(2,[source])[-1][0],55)
        self.assertEqual(before,self.b.profile())

    def test_policy_in_report_and_initial_cast_config(self):
        role=self.b.profile()
        report=role['combat_power_breakdown']
        self.assertEqual(report['attribute_policy']['advance_extra_base'],'pre_fate_panel')
        self.assertEqual(f.load_rules()['equipment_batch_count'],10)
        for values in report['companions'].values():
            self.assertIn('advance_extra_base',values)
            self.assertIn('advance_extra_rates',values)

    def test_six_star_chain_replaces_cast_chain_and_realm_gate(self):
        from network_redirect import reborn
        items = [dict(id=n, attach_type=5, type_id=t, star_level=1, reborn_bit=1, cast_level=4)
                 for n,t in enumerate((2002,3003,4006),1)]
        values={k:Decimal(0) for k in f.STATS}
        reborn.bonuses({}, {}, values, items)
        self.assertEqual(values,dict(hp=4500,magic=0,gongji=4500,fangyu=3000))
        items[0]['star_level']=0
        values={k:Decimal(0) for k in f.STATS}
        reborn.bonuses({}, {}, values, items)
        self.assertEqual(values,dict(hp=1600,magic=0,gongji=2000,fangyu=1600))
        target=self.add(2001);material=self.add(2001)
        role=self.b.profile();role['reborn_layer']=3;self.b.save(role);before=self.b.profile()
        self.assertEqual(self.req(1079,equipid=target,equip_order=0,material_equipid=material)[-1][0],55)
        self.assertEqual(before,self.b.profile())
        role=self.b.profile();role['reborn_layer']=4
        next(i for i in role['attachments'] if i['id']==target)['count']=2
        self.b.save(role);before=self.b.profile()
        self.assertEqual(self.req(1079,equipid=target,equip_order=0,material_equipid=material)[-1][0],55)
        self.assertEqual(before,self.b.profile())

    def test_skill_recipe_and_reopen_crafting_state(self):
        role=self.b.profile();role['gold_coin']=1000
        ident=f.new_id(role);role['attachments'].append(dict(id=ident,attach_type=6,type_id=22,level=1,count=0));self.b.save(role)
        event=self.convert(5,[ident])[-1]
        self.assertEqual(event[0],116)
        self.assertEqual({x['attach_type'] for x in event[1]['item_list'].values()},{22,206})
        self.assertEqual(self.b.profile()['gold_coin'],900)
        before=self.b.profile();self.b.close()
        from network_redirect.backend import Backend
        from pathlib import Path
        self.b=Backend(Path(self.tmp.name),18770,lambda *a,**kw:None)
        self.assertEqual(before,self.b.profile())

    def test_advance_extra_uses_pre_fate_panel_once(self):
        from network_redirect import combat_power
        self.add(2001,level=20,advance_level=10,equip_order=1,equip_pos=1)
        role=self.b.profile();target=role['corteges'][0]['id'];rules=f.load_rules()
        with_extra=combat_power.explain(role,rules)['companions'][str(target)]
        real=f.advance_worth
        with patch.object(f,'advance_worth',side_effect=lambda item:(*real(item)[:2],Decimal(0))):
            without_extra=combat_power.explain(role,rules)['companions'][str(target)]
        basis=Decimal(with_extra['advance_extra_base']['gongji'])
        gain=Decimal(with_extra['fates_and_advance']['gongji'])-Decimal(without_extra['fates_and_advance']['gongji'])
        self.assertEqual(gain,basis*Decimal('.25'))
        self.assertEqual(with_extra['advance_extra_rates']['gongji'],'0.25')

    def test_consuming_items_preserves_zero_compensation_skills(self):
        role=self.b.profile();ident=f.new_id(role)
        role['attachments'].append(dict(id=ident,attach_type=6,type_id=22,level=1,count=0));self.b.save(role)
        source=self.add(1313,count=10)
        self.assertEqual(self.convert(2,[source])[-1][0],116)
        self.assertEqual(self.get(ident)['count'],0)
        sale=self.gear(quality=3)
        self.assertEqual(self.req(1056,data=summon.lua(dict(equip_list=[sale])))[-1][0],16)
        self.assertEqual(self.get(ident)['type_id'],22)
