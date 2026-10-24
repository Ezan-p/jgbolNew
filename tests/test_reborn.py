"""Full binary requests against isolated persistent stores, original CSV costs."""
import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from network_redirect import reborn as r, reborn_stars as stars, formation as f, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode

class RebornTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.addCleanup(lambda: self.b.close())
        self.serial = 10000
        role = self.b.profile()
        role.update(level=99, silver_coin=100000000, gold_coin=100000)
        role['corteges'] = [summon.companion(role, 5022)]
        role['corteges'][0].update(order=1, level=200)
        self.cid = role['corteges'][0]['id']
        for t in [1329,1330,1331,1332,1333,1334,1335,1310,1311,1312,10000,10300]:
            summon.add_item(role, t, 100000)
        for t in range(10101,10120): summon.add_item(role,t,100)
        for t in range(10201,10220): summon.add_item(role,t,100)
        self.b.save(role)

    def req(self, mid=1328, **kw):
        self.serial += 1
        self.packet = encode(mid, dict(serial_num=self.serial, **kw))
        self.replies = self.b.respond(self.packet, dict(authenticated=True))
        self.decoded = [decode(p) for p in self.replies]
        self.assertEqual(self.decoded[-1][0], 1106)
        return [(d['id'],login_fields(d['data'])) for m,_,d in self.decoded if m==2998]

    def op(self, kind, op, **data):
        return self.req(reborn_type=kind,id=op,data=summon.lua(data))

    def role(self): return self.b.profile()
    def cort(self): return self.role()['corteges'][0]
    def add(self,t,kind=5,**kw):
        role=self.role(); ident=f.new_id(role)
        role['attachments'].append(dict(id=ident,type_id=t,attach_type=kind,count=1,level=1,**kw))
        self.b.save(role);return ident
    def get(self,ident):return next(x for x in self.role()['attachments'] if x['id']==ident)
    def veins(self, layer):
        for p in range(1,10):
            row=r.VEINS[layer,p]; allowed={int(x.split('|')[1]):int(x.split('|')[3]) for x in row['consume_list'].split('/')}
            count=int(row['fixed_count(fix>0|unfix=0)'])
            materials={next(iter(allowed)):count} if count else allowed
            self.assertEqual(self.op(2,1,cortege_id=self.cid,material_list=materials)[-1],(172,{'flag':1}))
            self.assertEqual(self.cort()['reborn_vein_level'],p)
    def ready(self):
        role=self.role();role['reborn_layer']=4;role['corteges'][0].update(reborn_layer=1)
        self.b.save(role)
        return next(x['id'] for x in self.role()['attachments'] if x.get('innate_owner_id')==self.cid)
    def awake(self):
        sid=self.ready();role=self.role();next(x for x in role['attachments'] if x['id']==sid).update(level=10)
        self.b.save(role)
        a,b=self.add(42,6),self.add(43,6)
        self.assertEqual(self.req(1332,des_id=sid,awaken_type=1,material_count=2,material_list=[dict(id=a),dict(id=b)])[-1],(183,{'result':0}))
        return sid

    def test_bootstrap_complete_configs(self):
        cfg=login_fields(decode(self.b.bootstrap()[0])[2]['data'])
        self.assertEqual(len(cfg[31]),5);self.assertTrue(cfg[32]['is_open'])
        for i,x in cfg[31].items():
            self.assertIn('consume_list',x['condiction']);self.assertIn('boss_layer',x['rights'])

    def test_all_nine_layers_and_81_veins(self):
        role=self.role();role['reborn_layer']=4;self.b.save(role)
        for layer in range(1,10):
            role=self.role();role['corteges'][0]['level']=int(r.LAYERS[layer]['min_level']);self.b.save(role)
            self.veins(layer)
            self.assertEqual(self.op(2,2,cortege_id=self.cid)[-1],(172,{'flag':2}))
            c=self.cort();self.assertEqual(c['reborn_layer'],layer);self.assertEqual(c['reborn_vein_level'],0)
            self.assertEqual(c['level'],int(r.LAYERS[layer]['reset_level']))
            self.assertEqual(c['culture_point'],150*layer)
        before=self.role();self.assertEqual(self.op(2,2,cortege_id=self.cid)[-1][0],55);self.assertEqual(before,self.role())

    def test_four_realms_require_server_conditions(self):
        self.assertEqual(self.op(1,4)[-1][0],172)
        before=self.role();self.assertEqual(self.op(1,4)[-1][0],55);self.assertEqual(before,self.role())
        for target in (2,3,4):
            role=self.role(); need=self.b.reborn_rules['realms'][target-1]['required_layer']
            while len(role['corteges'])<3:role['corteges'].append(summon.companion(role,5022))
            for c in role['corteges']:c['reborn_layer']=need
            self.b.save(role)
            self.assertEqual(self.op(1,4)[-1][0],172);self.assertEqual(self.role()['reborn_layer'],target)
        self.assertEqual(self.op(1,4)[-1][0],55)

    def test_invalid_material_rolls_back_and_replay(self):
        self.op(1,4)
        before=self.role()
        for materials in ({10000:1},{10000:-300},{1329:300},{10000:300,1329:1}):
            self.assertEqual(self.op(2,1,cortege_id=self.cid,material_list=materials)[-1][0],55)
            self.assertEqual(before,self.role())
        self.op(2,1,cortege_id=self.cid,material_list={10000:300})
        once=self.role(); self.assertEqual(self.b.respond(self.packet,dict(authenticated=True)),self.replies)
        self.assertEqual(once,self.role())
        collision=encode(1328,dict(serial_num=self.serial,reborn_type=1,id=4,data='{}'))
        self.b.respond(collision,dict(authenticated=True));self.assertEqual(once,self.role())

    def test_premature_rebirth_and_unknown_target(self):
        self.op(1,4)
        for kind,op,data in [(2,2,dict(cortege_id=self.cid)),(2,1,dict(cortege_id=-1)),(2,4,{}),(3,3,{})]:
            before=self.role();self.assertEqual(self.op(kind,op,**data)[-1][0],55);self.assertEqual(before,self.role())

    def test_change_attributes_cost_and_deltas(self):
        self.ready();before=self.role();old=before['corteges'][0]['gongji']
        self.assertEqual(self.op(2,3,cortege_id=self.cid,des_type=1)[-1][0],172)
        self.assertEqual(self.role()['gold_coin'],before['gold_coin']-50)
        self.assertNotEqual(self.cort()['gongji'],old)
        self.assertTrue(any(a['type']==226 for m,_,d in self.decoded if m==1032 for a in d['attr_list']))
        before=self.role();self.assertEqual(self.op(2,3,cortege_id=self.cid,des_type=1)[-1][0],55);self.assertEqual(before,self.role())

    def test_equipment_all_three_types_and_four_casts(self):
        self.ready()
        for main in (1,2,3):
            t=next(t for t,x in f.ITEMS.items() if int(x['main_type'])==main and int(x['quality'])==5)
            ident=self.add(t,advance_level=10,equip_order=0)
            self.assertEqual(self.op(3,5,equip_id=ident,equip_order=0)[-1][0],172)
            self.assertEqual(self.get(ident)['reborn_bit'],1)
            self.assertEqual(self.get(ident)['cast_level'],1)
            for level in range(2,5):
                self.assertEqual(self.op(3,6,equip_id=ident,equip_order=0)[-1][0],172)
                self.assertEqual(self.get(ident)['cast_level'],level)
            before=self.role();self.assertEqual(self.op(3,6,equip_id=ident,equip_order=0)[-1][0],55);self.assertEqual(before,self.role())

    def test_divination_query_draw_quick_collect_reset_buy(self):
        role=self.role();role['vip_level']=3;self.b.save(role)
        self.assertEqual(self.req(1337,event_type=1,data='{}')[-1][0],190)
        self.req(1337,event_type=2,data='{}');self.assertEqual(len(self.role()['divination']['star_list']),1)
        self.req(1337,event_type=3,data='{}');self.assertEqual(len(self.role()['divination']['star_list']),20)
        before=self.role();self.assertEqual(self.req(1337,event_type=2,data='{}')[-1][0],55);self.assertEqual(before,self.role())
        self.req(1337,event_type=5,data='{}');self.assertEqual(self.role()['divination']['star_list'],[])
        self.assertEqual(sum(x['count'] for x in self.role()['attachments'] if x['type_id'] in stars.STARS),20)
        before=self.role();self.assertEqual(self.req(1337,event_type=5,data='{}')[-1][0],55);self.assertEqual(before,self.role())
        self.req(1337,event_type=6,data='{count=10}');self.assertEqual(self.role()['gold_coin'],before['gold_coin']-50)
        self.req(1337,event_type=6,data='{count=10}');self.assertEqual(self.role()['gold_coin'],before['gold_coin']-150)
        self.req(1337,event_type=4,data='{}');self.assertEqual(self.role()['divination']['cur_pos'],1)

    def test_daily_reset_keeps_pending_rewards(self):
        role=self.role();rules=self.b.reborn_rules
        stars.divination(role,dict(event_type=2,data='{}'),rules,login_fields,now=100000)
        pending=copy.deepcopy(role['divination']['star_list'])
        stars.divination(role,dict(event_type=1,data='{}'),rules,login_fields,now=200000)
        self.assertEqual(role['divination']['divi_count'],rules['daily_divinations']);self.assertEqual(role['divination']['star_list'],pending)

    def test_awaken_star_equip_upgrade_unload_decompose_restore(self):
        sid=self.awake(); self.assertEqual(self.get(sid)['awaken'],1)
        ident=self.add(10301)
        self.assertEqual(self.req(1338,des_cortege_id=self.cid,ext_star_id=ident,element_id=1,replace=0)[-1][0],186)
        self.assertEqual(self.get(ident)['owner_id'],self.cid)
        self.assertEqual(self.req(1341,count=1,star_list=[dict(id=ident)])[-1][0],55)
        self.assertEqual(self.req(1340,ext_star_id=ident,cost_count=5)[-1][0],188);self.assertEqual(self.get(ident)['level'],2)
        self.assertEqual(self.req(1339,des_cortege_id=self.cid,element_id=1)[-1][0],187)
        self.assertEqual(self.req(1341,count=1,star_list=[dict(id=ident)])[-1][0],189)
        self.assertEqual(self.req(1342,des_id=sid)[-1],(191,{'result':1}));self.assertEqual(self.get(sid)['awaken'],0)
        self.assertEqual(sorted(x['type_id'] for x in self.role()['attachments'] if x['attach_type']==6 and not x.get('protogenic')),[42,43])

    def test_all_star_qualities_upgrade_to_ten(self):
        for quality in range(1,6):
            ident=self.add(10301+(quality-1)*1000)
            for n in stars.EXP[quality]:
                self.assertEqual(self.req(1340,ext_star_id=ident,cost_count=n)[-1][0],188)
            self.assertEqual(self.get(ident)['level'],10)
            before=self.role();self.assertEqual(self.req(1340,ext_star_id=ident,cost_count=1)[-1][0],55);self.assertEqual(before,self.role())

    def test_invalid_star_operations_are_atomic(self):
        self.awake();ident=self.add(10301,is_lock=1)
        for mid,kw in [(1341,dict(count=2,star_list=[dict(id=ident),dict(id=ident)])),(1341,dict(count=1,star_list=[dict(id=ident)])),(1340,dict(ext_star_id=ident,cost_count=0)),(1338,dict(des_cortege_id=self.cid,ext_star_id=ident,element_id=6,replace=0))]:
            before=self.role();self.assertEqual(self.req(mid,**kw)[-1][0],55);self.assertEqual(before,self.role())

    def test_persistence_and_stat_recalculation_idempotent(self):
        self.ready();self.op(2,3,cortege_id=self.cid,des_type=1)
        before=self.role();self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(before,self.role())
        for _ in range(3):self.b.save(self.role())
        self.assertEqual(before,self.role())

    def test_every_star_type_equip_and_combat_traits(self):
        self.awake()
        for tid in stars.STARS:
            with self.subTest(star=tid):
                ident=self.add(tid)
                self.assertEqual(self.req(1338,des_cortege_id=self.cid,ext_star_id=ident,element_id=1,replace=1)[-1][0],192)
                role=self.role()
                traits=stars.combat_traits(role,role['corteges'][0])
                self.assertGreaterEqual(stars.spell_power(100,202,traits),100)
                self.assertGreaterEqual(stars.combat_hit(10,100,True,traits,{}),10)

    def test_star_combat_critical_resistance_survival_and_spell(self):
        with patch.object(stars.secrets,'randbelow',return_value=0):
            self.assertEqual(stars.combat_hit(100,1000,True,dict(crit=10,crit_damage=20),{}),170)
            self.assertEqual(stars.combat_hit(100,1000,True,dict(crit=10),dict(resist=10)),100)
            defender=dict(survival=100,survival_count=1)
            self.assertEqual(stars.combat_hit(200,100,False,{},defender),99)
            self.assertEqual(stars.combat_hit(200,100,False,{},defender),100)
        self.assertEqual(stars.spell_power(1000,202,dict(awake_skills={202:10},spell_rate=10,spell_flat=2)),1212)

    def test_rebirth_preserves_experience_above_minimum(self):
        role=self.role();role['reborn_layer']=4;c=role['corteges'][0]
        c.update(level=168,cur_exp=123,reborn_vein_level=9)
        quality=int(f.BASES[c['type']]['quality'])
        expected=123+sum(f.EXPERIENCE[quality,lv] for lv in range(165,168))
        self.b.save(role)
        self.assertEqual(self.op(2,2,cortege_id=self.cid)[-1][0],172)
        c=self.cort()
        self.assertEqual(sum(f.EXPERIENCE[quality,lv] for lv in range(155,c['level']))+c['cur_exp'],expected)

    def test_vein_material_preserves_equipped_and_locked_essences(self):
        role=self.role()
        role['attachments']=[x for x in role['attachments'] if x['type_id']!=10101]
        role['attachments'] += [dict(id=90001,attach_type=5,type_id=10101,count=10,level=1,owner_id=self.cid),
                                dict(id=90002,attach_type=5,type_id=10101,count=10,level=1,is_lock=1),
                                dict(id=90003,attach_type=5,type_id=10101,count=3,level=1)]
        r.debit_material(role,10101,3)
        self.assertEqual([x['count'] for x in role['attachments'] if x['type_id']==10101],[10,10])
        with self.assertRaises(f.Rejected):r.debit_material(role,10101,1)

if __name__=='__main__':unittest.main()
