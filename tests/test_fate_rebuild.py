"""Real packet integration: nine rebirths -> package -> box -> fate activation."""
import copy
import tempfile
from pathlib import Path
from unittest.mock import patch
from test_activity import ActivityCase, NOW
from network_redirect import fate_rebuild as fr, reborn, summon, formation, combat_power, combat, combat_loadout
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode, encode


class FateTests(ActivityCase):
    def setUp(self):
        super().setUp()
        role=self.b.profile();role.update(level=99,reborn_layer=4)
        role['corteges']=[summon.companion(role,5022)]
        c=role['corteges'][0];c.update(reborn_layer=9,level=100,order=1)
        self.cid=c['id'];self.b.save(role)

    def c(self): return self.b.profile()['corteges'][0]
    def stock(self,tid,n):
        role=self.b.profile();summon.add_item(role,tid,n);self.b.save(role)
    def count(self,tid): return sum(i['count'] for i in self.b.profile()['attachments'] if i['attach_type']==5 and i['type_id']==tid)
    def fate(self,op=3,**kw): return self.req(1357,id=op,data=summon.lua(dict(cortege_id=self.cid,**kw)))
    def activate(self): self.stock(1371,20);self.ok(self.fate())
    def node(self,part):
        c=self.c();level,stars=fr.progress(c,part)
        tokens=list(map(int,fr.COSTS[part,level,stars+1].split('|')))
        if tokens[0]==3: materials=dict(zip(tokens[1::2],tokens[2::2]))
        else: materials={tokens[1]:tokens[-1]}
        role=self.b.profile()
        for tid,n in materials.items():
            if tokens[0]==2:
                for _ in range(n): role['attachments'].append(dict(id=formation.new_id(role),attach_type=6,type_id=tid,count=1,level=1))
            else: summon.add_item(role,tid,n)
        self.b.save(role)
        self.ok(self.fate(0,soul_part=part,material_list=materials))
        return materials

    def test_package_box_activation_and_restart(self):
        self.stock(1141,75)
        self.ok(self.req(1227,flag=2,index=2,count=3,five_card=0,ten_card=0))
        self.assertEqual((self.count(1141),self.count(1370),self.count(1371)),(0,48,24))
        role=self.b.profile();mail=next(m for k,m in role['welfare']['mails'].items() if k.startswith('pavilion-first-') and k.endswith('-2'))
        self.ok(self.req(1103,mail_id=mail['mail_id']));self.assertEqual(self.count(1375),1000)
        box=next(i for i in self.b.profile()['attachments'] if i['type_id']==1370)
        self.ok(self.req(1051,item_type=1370,item_id=box['id'],item_count=5,des_type=1,des_id=0))
        self.assertEqual(self.count(1370),43)
        self.assertEqual(sum(self.count(t) for t in (1372,1373,1374)),5)
        self.ok(self.fate());self.assertEqual(self.count(1371),4)
        self.assertEqual(self.c()['fate_rebullding_state'],1)
        packet,replies,before=self.packet,self.replies,self.b.profile()
        self.assertEqual(self.b.respond(packet,self.state),replies);self.assertEqual(self.b.profile(),before)
        self.assertEqual(self.fate()[0][0],55);self.assertEqual(self.b.profile(),before)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.c()['fate_rebullding_state'],1)
        configs=[login_fields(d['data']) for mid,_,d in map(decode,self.b.bootstrap()) if mid==2998 and d['id']==80]
        config=next(x for x in configs if 'local_fate_rebuild' in x)
        self.assertEqual(config['local_fate_rebuild'][self.cid]['fate_rebullding_state'],1)

    def test_activation_guards_locked_materials_and_rollback(self):
        self.stock(1371,20)
        for changes in ({'reborn_layer':8},{'type':5004}):
            role=self.b.profile();old=copy.deepcopy(role);role['corteges'][0].update(changes);self.b.save(role)
            before=self.b.profile();self.assertEqual(self.fate()[0][0],55);self.assertEqual(before,self.b.profile());self.b.save(old)
        role=self.b.profile();role['reborn_layer']=3;self.b.save(role);before=self.b.profile()
        self.assertEqual(self.fate()[0][0],55);self.assertEqual(before,self.b.profile())
        role['reborn_layer']=4
        next(i for i in role['attachments'] if i['type_id']==1371)['is_lock']=1
        self.b.save(role);before=self.b.profile();self.assertEqual(self.fate()[0][0],55);self.assertEqual(before,self.b.profile())
        role=copy.deepcopy(before);next(i for i in role['attachments'] if i['type_id']==1371)['is_lock']=0;self.b.save(role)
        before=self.b.profile()
        with patch('network_redirect.fate_rebuild.sync',side_effect=ValueError('encode failure')):
            self.assertEqual(self.fate()[0][0],55)
        self.assertEqual(self.b.profile(),before)

    def test_all_ten_soul_paths_real_costs_stats_and_potential(self):
        self.activate();base=self.c()
        for part in range(1,11):
            for _ in range(fr.star_count(part)): self.node(part)
            self.assertEqual(fr.progress(self.c(),part),(1,0))
        c=self.c();self.assertGreater(c['gongji'],base['gongji']);self.assertGreater(c['hp'],base['hp'])
        self.assertEqual(c['culture_point']-base['culture_point'],170)
        self.assertEqual(c['fate_rebuilding_culture_point'],170)
        self.assertEqual(c['fate_rebuilding_achive_rate'],4.3)
        self.assertEqual(c['fate_rebuilding_fangyu_rate_zs'],1.6)
        role=self.b.profile();before=copy.deepcopy(role);formation.recalculate(role,self.b.formation_rules)
        self.assertEqual(role,before)

    def test_invalid_forged_costs_limits_and_equipped_skill_protection(self):
        self.activate()
        for kw in ({'soul_part':1,'material_list':{1375:1}}, {'soul_part':11,'material_list':{1375:30}},
                   {'soul_part':True,'material_list':{1375:30}}, {'soul_part':1,'material_list':{1375:-30}}):
            before=self.b.profile();self.assertEqual(self.fate(0,**kw)[0][0],55);self.assertEqual(before,self.b.profile())
        role=self.b.profile();role['corteges'][0]['physic_yp_level']=10;self.b.save(role)
        before=self.b.profile();self.assertEqual(self.fate(0,soul_part=10,material_list={1329:100,1330:50})[0][0],55);self.assertEqual(before,self.b.profile())
        role=self.b.profile();role['attachments'].append(dict(id=formation.new_id(role),attach_type=6,type_id=25,count=1,level=1,is_lock=1));self.b.save(role)
        before=self.b.profile();self.assertEqual(self.fate(0,soul_part=8,material_list={25:1})[0][0],55);self.assertEqual(before,self.b.profile())

    def test_choice_unlock_switch_combat_and_exact_reset(self):
        self.activate();before=self.b.profile()
        self.assertEqual(self.fate(2,soul_part=1,effect_type=378)[0][0],55);self.assertEqual(before,self.b.profile())
        # Exercise actual costs through ten complete layers, including stone nodes.
        for _ in range(90):self.node(1)
        gold=self.b.profile()['gold_coin'];self.ok(self.fate(2,soul_part=1,effect_type=378))
        self.assertEqual(self.b.profile()['gold_coin'],gold);self.assertEqual(self.c()['fate_rebuilding_damage_train_rate'],2)
        self.ok(self.fate(2,soul_part=1,effect_type=379));self.assertEqual(self.b.profile()['gold_coin'],gold-50)
        self.assertEqual(self.c()['fate_rebuilding_damage_train_rate'],0);self.assertEqual(self.c()['fate_rebuilding_absorb_train_rate'],2)
        role=self.b.profile();units=combat_loadout.player_units(role)
        self.assertEqual(units[0]['reborn_traits']['fate_absorb'],2)
        ledger=copy.deepcopy(self.c()['fate_materials']['1']);counts={t:self.count(int(t)) for t in ledger}
        self.ok(self.fate(4));self.assertEqual(fr.progress(self.c(),1),(0,0));self.assertEqual(self.c()['fate_rebuilding_absorb_train_rate'],0)
        for t,n in ledger.items():self.assertEqual(self.count(int(t)),counts[t]+n)
        before=self.b.profile();self.assertEqual(self.fate(4)[0][0],55);self.assertEqual(before,self.b.profile())

    def test_nine_turn_progression_then_activate(self):
        role=self.b.profile();c=role['corteges'][0];c.update(reborn_layer=0,reborn_vein_level=0)
        for t in (1329,1330,1331,1332,10000,10300):summon.add_item(role,t,100000)
        for t in (*range(10101,10120),*range(10201,10220)):summon.add_item(role,t,1000)
        self.b.save(role)
        for layer in range(1,10):
            role=self.b.profile();role['corteges'][0]['level']=int(reborn.LAYERS[layer]['min_level']);self.b.save(role)
            for vein in range(1,10):
                row=reborn.VEINS[layer,vein];materials={int(p.split('|')[1]):int(p.split('|')[3]) for p in row['consume_list'].split('/')}
                count=int(row['fixed_count(fix>0|unfix=0)'])
                if count:materials={next(iter(materials)):count}
                self.ok(self.req(1328,reborn_type=2,id=1,data=summon.lua(dict(cortege_id=self.cid,material_list=materials))))
            self.ok(self.req(1328,reborn_type=2,id=2,data=summon.lua(dict(cortege_id=self.cid))))
            self.assertEqual(self.c()['reborn_layer'],layer)
        self.activate();self.assertEqual(self.c()['fate_rebullding_state'],1)

    def test_fifth_essence_slot_engraving_and_battle(self):
        self.activate();role=self.b.profile();c=role['corteges'][0]
        c.update(spirit_earth_level=50,equiped_ext_skill_limit=4)
        for pos in range(1,5):
            role['attachments'].append(dict(id=formation.new_id(role),attach_type=5,type_id=10100+pos,
                count=1,level=1,owner_id=self.cid,ext_skill_pos=pos))
        item=summon.add_item(role,10105,1);self.b.save(role)
        source=next(i for i in self.b.profile()['attachments'] if i['type_id']==10105)
        self.ok(self.req(1311,ext_skill_id=source['id'],des_cortege_id=self.cid,lock_list='{}'))
        role=self.b.profile();c=role['corteges'][0]
        engraved=next(i for i in role['attachments'] if i['id']==source['id'])
        self.assertEqual(engraved['ext_skill_pos'],5)
        self.assertEqual(len(combat_power.essence_score(role,c)['selected']),5)
        self.assertIn(5,combat_loadout.player_units(role)[0]['essences'])
        c['spirit_earth_level']=49
        self.assertEqual(len(combat_power.essence_score(role,c)['selected']),4)

    def test_enabled_character_traits_and_essence_bonuses(self):
        from fractions import Fraction
        for tid in fr.ACTIVE:
            c=dict(type=tid,fate_rebullding_state=1,spirit_heaven_level=100,spirit_fortune_level=100)
            fr.refresh(c);family=fr.ESSENCE_FAMILY[tid]
            u=dict(essences={family:(Fraction(1),)*3})
            fr.special_bonuses(c,u)
            self.assertTrue(u['fate_traits'],tid)
            self.assertTrue(any(v>1 for v in u['essences'][family]),tid)
        c=dict(type=5013,fate_rebullding_state=1,spirit_heaven_level=100);fr.refresh(c)
        u=dict(essences={16:(10,5)});fr.special_bonuses(c,u)
        self.assertEqual(u['essences'][16],(10,40))  # curse HP, not proc chance
        u={};fr.special_bonuses(c,u);self.assertNotIn('essences',u)

    def test_fate_battle_damage_heal_reflect_and_round_growth(self):
        from test_combat_engine import unit
        from network_redirect import combat_engine,journey
        def battle(a,b):return combat_engine.Battle({},([unit(**a)],[unit(**b)]),journey.load_rules())
        a=battle({'fate_traits':{'target_hp_damage':[4]}},{})
        a.round=1;a.attack(a.sides[0][0],a.sides[1]);self.assertEqual(a.sides[1][0]['hp'],860)
        b=battle({}, {'fate_traits':{'reflect':[40]}})
        b.round=1;b.attack(b.sides[0][0],b.sides[1]);self.assertEqual(b.sides[0][0]['hp'],960)
        self.assertEqual(combat_engine.total_damage(b.actions,2),40)
        b=battle({'hp':500,'fate_traits':{'round_heal':[15],'round_defense':[3]}},{})
        b.round=2;b.upkeep();self.assertEqual(b.sides[0][0]['hp'],650)
        actor=unit(fate_traits={'round_attack':[9]});combat.begin_action(actor,3)
        self.assertEqual(actor['gongji'],118);combat.begin_action(actor,3);self.assertEqual(actor['gongji'],118)
        b=battle({}, {'hp':50,'magic':100,'fate_traits':{'death_spell':[100,40]}})
        b.round=1;b.attack(b.sides[0][0],b.sides[1]);self.assertEqual(b.sides[0][0]['hp'],960)

    def test_large_roster_login_uses_bounded_fate_packets(self):
        role=self.b.profile()
        for _ in range(149):
            c=summon.companion(role,5022);c.update(fate_rebullding_state=1,reborn_layer=9)
            role['corteges'].append(c)
        self.b.save(role)
        packets=self.b.bootstrap();self.assertTrue(all(len(p)<65536 for p in packets))
        states=[login_fields(d['data']) for mid,_,d in map(decode,packets) if mid==2998 and d['id']==80]
        chunks=[s for s in states if 'local_fate_rebuild' in s]
        self.assertEqual(len(chunks),15)
        self.assertFalse(chunks[0]['local_fate_append'])
        self.assertTrue(all(s['local_fate_append'] for s in chunks[1:]))
        self.assertEqual(sum(len(s['local_fate_rebuild']) for s in chunks),149)
        self.assertNotIn('local_fate_rebuild',states[0])
