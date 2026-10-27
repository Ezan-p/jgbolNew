"""Spell acquisition/growth and inventory retention through unrelated spending."""
import copy
from pathlib import Path
from unittest.mock import patch
import unittest

from tests import test_formation as helpers
from network_redirect import formation as f, summon, equipment_crafting
from network_redirect import spirit_array, welfare, activity_visit
from network_redirect.backend import Backend


class SkillTests(unittest.TestCase):
    setUp = helpers.FormationTests.setUp
    request = helpers.FormationTests.request
    events = helpers.FormationTests.events
    ok = helpers.FormationTests.ok
    rejected = helpers.FormationTests.rejected
    add_item = helpers.FormationTests.add_item

    def spell(self, tid=22, level=1, **kw):
        ident = self.add_item(tid, count=0, attach_type=6)
        r = self.backend.profile()
        f.lookup(r, 'attachments', ident).update(level=level, **kw)
        self.backend.save(r)
        return ident

    def skills(self, r):
        return [copy.deepcopy(i) for i in r['attachments'] if i['attach_type'] == 6]

    def test_card_payment_preserves_all_spell_states_and_ids(self):
        for flags in ({}, {'equip_order':1,'equip_pos':2}, {'is_lock':1}, {'upgrade_level':1}, {'awaken':1}):
            self.spell(**flags)
        self.add_item(1156, 2)
        before = self.skills(self.backend.profile())
        self.request(1111, event_id=251, data=summon.lua(dict(item_id=101, order_id='spell-payment-001', large_count=0, small_count=2)))
        self.assertEqual(self.backend.profile()['charge_gold'],100)
        self.assertEqual(before, self.skills(self.backend.profile()))
        self.assertEqual(self.backend.respond(self.packet, self.state), self.replies)
        with BackendContext(self.directory.name) as b:
            self.assertEqual(before, self.skills(b.profile()))

    def test_array_embed_activate_upgrade_and_exchange_keep_spells(self):
        self.spell(203, 10)
        r = self.backend.profile();r['level']=99
        summon.add_item(r,1315,1000);self.backend.save(r)
        kind, lv = spirit_array.NEEDS[1,1]
        stone=self.add_item(kind)
        r=self.backend.profile();f.lookup(r,'attachments',stone)['level']=lv;self.backend.save(r)
        before=self.skills(self.backend.profile())
        for op, data in [(1,dict(goss_id=1,pos=1,id_list=[stone])),(2,dict(goss_id=1)),(3,dict(goss_id=1,pos=1))]:
            self.ok(1310,id=op,data=summon.lua(data))
            self.assertEqual(before,self.skills(self.backend.profile()))
        stone=self.add_item(kind)
        r=self.backend.profile();f.lookup(r,'attachments',stone)['level']=lv;self.backend.save(r)
        self.ok(1310,id=6,data=summon.lua(dict(id_list=[stone])))
        self.assertEqual(before,self.skills(self.backend.profile()))

    def test_optional_welfare_exchange_only_removes_paid_stacks(self):
        self.spell(203,10)
        r=self.backend.profile();r.update(level=99,gold_coin=100000)
        summon.add_item(r,1001,1000);self.backend.save(r)
        self.backend.welfare_rules['order']=sorted(welfare.TYPES)
        before=self.skills(self.backend.profile())
        self.ok(1127,act_type=32,index=2,flag=2)
        self.assertEqual(before,self.skills(self.backend.profile()))

    def test_all_54_spells_have_values_before_equipping_and_on_reconnect(self):
        r=self.backend.profile()
        tids=sorted(t for ids in activity_visit.SKILLS.values() for t in ids)
        self.assertEqual(len(tids),54)
        prizes=equipment_crafting.grant(r,[(6,t,1,1) for t in tids])
        self.assertEqual(len(prizes),54)
        for item in self.skills(r):
            self.assertEqual(item['effect_value'],f.skill_effect(item))
        # Legacy idle spells missing display fields are repaired idempotently.
        for item in r['attachments']:
            if item['attach_type']==6:item.pop('effect_value',None)
        self.backend.save(r);r=self.backend.profile()
        for item in self.skills(r):self.assertEqual(item['effect_value'],f.skill_effect(item))
        d=next(i for i in r['attachments'] if i['type_id']==21 and i['attach_type']==6)
        self.assertEqual((d['absorb_rate'],d['shield_rate']),(3,8))
        before=copy.deepcopy(r);f.prepare(r,self.backend.formation_rules);self.assertEqual(r,before)

    def test_bag_acquire_upgrade_equip_pay_unequip_reconnect(self):
        bag=self.add_item(1034)
        with patch('network_redirect.qiankun_bags.draw',return_value=[6,22,1,1]):
            self.ok(1051,item_type=1034,item_id=bag,item_count=1,des_type=1,des_id=0)
        target=next(i['id'] for i in self.backend.profile()['attachments'] if i['attach_type']==6 and i['type_id']==22)
        for roll in (99,0):
            fodder=self.spell(212)
            with patch('network_redirect.formation.secrets.randbelow',return_value=roll):
                self.ok(1071,data=summon.lua(dict(des_skill_id=target,src_skill_list=[fodder])))
        self.ok(1037,flag=3,obj_type=6,src_id=target,src_order=0,des_order=1,des_equip_pos=2)
        self.add_item(1156,2)
        self.request(1111,event_id=251,data=summon.lua(dict(item_id=101,order_id='skill-chain-order',large_count=0,small_count=2)))
        self.assertEqual(self.backend.profile()['charge_gold'],100)
        self.ok(1037,flag=3,obj_type=6,src_id=target,src_order=1,des_order=0,des_equip_pos=0)
        item=f.lookup(self.backend.profile(),'attachments',target)
        self.assertEqual((item['level'],item['count'],item['equip_order']),(2,0,0))
        with BackendContext(self.directory.name) as b:self.assertEqual(item,f.lookup(b.profile(),'attachments',target))

    def test_material_validation_and_max_level_are_atomic(self):
        target=self.spell(22,10);fodder=self.spell(212)
        self.rejected(1071,data=summon.lua(dict(des_skill_id=target,src_skill_list=[fodder])))
        target=self.spell(22)
        for ids in ([True],[{}],[-1],[1.5],[fodder,fodder]):
            self.rejected(1071,data=summon.lua(dict(des_skill_id=target,src_skill_list=ids)))


class BackendContext:
    def __init__(self,path):self.path=Path(path)
    def __enter__(self):self.b=Backend(self.path,18770,lambda *a,**k:None);return self.b
    def __exit__(self,*args):self.b.close()
