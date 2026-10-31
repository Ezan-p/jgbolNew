import copy
import tempfile
import unittest
from pathlib import Path
from decimal import Decimal
from network_redirect import spirit_array as a, formation as f, summon, combat_power
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode


class ArrayTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **kw: None)
        self.addCleanup(self.b.close)
        self.serial = 1000
        r = self.b.profile(); summon.add_item(r, 1315, 100000); self.b.save(r)

    def request(self, op, **data):
        self.serial += 1
        self.packet = encode(1310, dict(serial_num=self.serial, id=op, data=summon.lua(data)))
        self.replies = self.b.respond(self.packet, {'authenticated': True})
        return [login_fields(d['data']) for m, _, d in map(decode, self.replies) if m == 2998 and d['id'] in (55,165)]

    def stone(self, kind, level, **kw):
        r = self.b.profile(); ident = summon.next_id(r)
        r['attachments'].append(dict(id=ident, attach_type=5, type_id=kind, count=1, level=level, **kw))
        self.b.save(r); return ident

    def ok(self, op, **data):
        result = self.request(op, **data)
        self.assertEqual(result[0].get('flag'), op, result)
        return result[0]

    def reject(self, op, **data):
        before = self.b.profile()
        result = self.request(op, **data)
        self.assertIn('op_string', result[0])
        self.assertEqual(self.b.profile(), before)

    def test_full_six_stage_progression_persistence_and_achievements(self):
        self.assertEqual(len(self.ok(5)['ling_info']), 6)
        for stage in range(1,7):
            for pos in range(1,stage+1):
                kind, lv = a.NEEDS[stage,pos]
                self.ok(1, goss_id=stage, pos=pos, id_list=[self.stone(kind,lv)])
            self.ok(2, goss_id=stage)
            for pos in range(1,stage+1):
                for lv in range(1,5): self.ok(3,goss_id=stage,pos=pos)
                self.reject(3,goss_id=stage,pos=pos)
        r = self.b.profile()
        self.assertTrue(all(x['activated'] and all(v == 5 for v in x['skill_list']) for x in r['spirit_array']))
        self.assertEqual(sum(x['count'] for x in r['attachments'] if x['type_id']==1315), 100000-sum(i*sum(v) for i,v in a.COSTS.items()))
        for ident in (461,462,463,464,465,560,561,562): self.assertGreater(r['achievements']['totals'][str(ident)],0)
        other = Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        try: self.assertEqual(other.profile()['spirit_array'],r['spirit_array'])
        finally: other.close()

    def test_refund_batch_and_replay(self):
        result=self.ok(1,goss_id=1,pos=1,id_list=[self.stone(1092,8)])
        self.assertEqual(result['ret_items'][1]['attach_count'],20)
        before=self.b.profile()
        self.assertEqual(self.b.respond(self.packet,{'authenticated':True}),self.replies)
        self.assertEqual(self.b.profile(),before)
        self.reject(1,goss_id=1,pos=1,id_list=[self.stone(1092,7)])
        result=self.ok(6,id_list=[self.stone(1090,4),self.stone(1091,11)])
        self.assertEqual(result['ret_items'][1]['attach_count'],161)

    def test_validation_atomic(self):
        self.reject(2,goss_id=1)
        self.reject(3,goss_id=1,pos=1)
        self.reject(1,goss_id=2,pos=1,id_list=[self.stone(1090,8)])
        for kind,lv,kw in [(1092,6,{}),(1090,7,{}),(1092,7,{'is_lock':True}),(1092,7,{'owner_id':1})]:
            self.reject(1,goss_id=1,pos=1,id_list=[self.stone(kind,lv,**kw)])
        ident=self.stone(1092,7)
        self.reject(6,id_list=[ident,ident]); self.reject(6,id_list=[ident,999999])
        self.reject(6,id_list=[]); self.reject(3,goss_id=True,pos=1)
        self.ok(1,goss_id=1,pos=1,id_list=[ident]); self.ok(2,goss_id=1)
        r=self.b.profile();r['attachments']=[];self.b.save(r)
        self.reject(3,goss_id=1,pos=1)

    def test_all_effect_rows_and_no_compounding(self):
        r=self.b.profile(); a.state(r)
        self.assertEqual(a.effects(r),{})
        for x in r['spirit_array']: x.update(activated=True,skill_list=[5]*len(x['skill_list']))
        effects=a.effects(r)
        self.assertEqual(set(effects), {int(x['name_index']) for x in a.EFFECTS})
        self.assertEqual(effects[1],30)
        f.recalculate(r,self.b.formation_rules); old=copy.deepcopy(r['corteges'])
        f.recalculate(r,self.b.formation_rules);self.assertEqual(old,r['corteges'])
        c=dict(order=0); v=dict(hp=Decimal(100),gongji=Decimal(100),fangyu=Decimal(100),magic=Decimal(100))
        before=v.copy();a.base_bonuses(r,c,v);a.final_bonuses(r,c,v);self.assertEqual(v,before)
        c['order']=1;a.base_bonuses(r,c,v);self.assertEqual(v['hp'],130)
        unit=dict(order=1,essences={13:(Decimal(9),),19:(Decimal(2),Decimal(4)),10:(Decimal(25),Decimal(14.5)),16:(Decimal(14),Decimal(5))})
        a.attach_combat(r,[unit]);self.assertEqual(unit['essences'][13][0],11)  # 1263: +2, formerly +7
        self.assertEqual(unit['essences'][16],(Decimal('15.5'),Decimal(5)))  # trigger, not damage
        self.assertEqual(unit['essences'][19][0],Decimal('3.5'))
        self.assertEqual(unit['training_bonuses'][0],(6,1000))
        self.assertEqual(unit['reborn_traits']['survival'],5)

    def test_battle_healing_and_training_are_applied(self):
        from network_redirect import combat_engine, journey, combat
        from tests.test_combat_engine import unit
        from unittest.mock import patch
        role = dict(spirit_array=[dict(activated=True,skill_list=[5]*i) for i in range(1,7)])
        with patch('network_redirect.combat.secrets.randbelow',return_value=999999):
            battle=combat_engine.Battle(role, ([unit(hp=100,essences={10:(100,10)})], [unit()]), journey.load_rules())
            actor=battle.sides[0][0]
            self.assertEqual(actor['essences'][10],(100,15))
            # Physical training adds 6% and 1000 flat: 100*1.06+1000.
            target=battle.sides[1][0];target['hp']=10000
            self.assertEqual(combat.damage(actor,target,1,1,battle.rules),1106)
            with patch('network_redirect.combat.secrets.randbelow',return_value=0):
                self.assertEqual(combat.damage(actor,target,1,1,battle.rules),1769)
            # Enemy never inherits the player's arrays.
            self.assertNotIn('training_bonuses',target)

    def test_invalid_serial_and_account_isolation(self):
        ident=self.stone(1092,7);self.ok(1,goss_id=1,pos=1,id_list=[ident])
        before=self.b.profile()
        packet=encode(1310,dict(serial_num=self.serial,id=6,data=summon.lua(dict(id_list=[ident]))))
        out=[decode(x) for x in self.b.respond(packet,{'authenticated':True})]
        self.assertTrue(any(m==2998 and d['id']==55 for m,_,d in out))
        self.assertEqual(before,self.b.profile())
        self.assertNotIn('spirit_array',self.b.profile('array-other'))

    def test_open_gate_and_queries(self):
        self.ok(4); self.ok(5)
        self.b.profile_rules['ling_is_open']=False;self.reject(5)
        self.b.profile_rules['ling_is_open']=True;self.b.profile_rules['ling_open_level']=10;self.reject(5)


if __name__ == '__main__': unittest.main()
