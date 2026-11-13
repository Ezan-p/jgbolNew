"""Playable progression contracts, resource conservation and authoritative medicine gates."""
import copy
import json
from pathlib import Path
import tempfile
from unittest.mock import patch
from tests.test_activity import ActivityCase, NOW
from network_redirect import activity, activity_abyss as ab, activity_drug as drug
from network_redirect import abyss_balance as balance, activity_abyss_combat as essence, formation, summon
from network_redirect.backend import Backend


class AbyssBalanceTests(ActivityCase):
    def setUp(self):
        super().setUp()
        role=self.b.profile();role['level']=80;self.b.save(role)

    def call(self,op,**data):
        result=self.req(1329,id=op,data=summon.lua(data));self.ok(result)
        return next(d for i,d in result if i==173 and d['flag']==op)

    def test_all_160_drugs_at_legal_levels_and_mastery(self):
        seen=set()
        for idx,row in drug.RECIPES.items():
            for grade,roll in enumerate((0,60,85,95)):
                role=self.b.profile();role.update(drug_level=int(row['min_level']),drug_exp=0)
                for token in row['study_material(attach_type|attach_count|need_silver)'].split('/'):
                    tid,n,_=map(int,token.split('|'));summon.add_item(role,tid,n)
                with patch.object(drug.secrets,'randbelow',return_value=roll):
                    drug.settle(role,dict(recipes=[idx]),21,dict(index=idx),self.b.activity_rules)
                tid=int(row['attach_type'])+grade*(20 if int(row['type'])==5 else 1)
                self.assertTrue(any(x['type_id']==tid for x in role['attachments']))
                seen.add(tid)
            for level in range(int(row['min_level']),37):
                self.assertEqual(sum(drug.quality_weights(level,row)),100)
            self.assertEqual(drug.quality_weights(36,row),[0,0,0,100])
            with self.assertRaises(formation.Rejected):drug.quality_weights(37,row)
        self.assertEqual(seen,set(ab.PILLS)|set(essence.DRUGS))

    def test_starter_once_restart_and_old_balances_preserved(self):
        before=self.b.profile();self.call(1);after=self.b.profile()
        self.assertEqual(after['silver_coin']-before['silver_coin'],100000)
        self.assertEqual(after['gold_coin']-before['gold_coin'],50)
        self.assertEqual(sum(x['count'] for x in after['attachments'] if x['type_id']==1442),40)
        self.call(1);self.assertEqual(after,self.b.profile())
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.call(1);self.assertEqual(after,self.b.profile())

    def test_no_effect_downgrade_and_wrong_slot_do_not_consume(self):
        self.call(1)
        role=self.b.profile()
        for tid in (1501,1502,1503,1521):summon.add_item(role,tid,2)
        self.b.save(role);self.call(17,index=1,type_id=1502)
        for tid in (1501,1503,1521):
            before=self.b.profile();out=self.req(1329,id=17,data=summon.lua(dict(index=1,type_id=tid)))
            self.assertEqual(out[0][0],55);self.assertEqual(before,self.b.profile())
        # A stronger useful replacement is allowed without compounding reductions.
        role=self.b.profile();role['activity']['abyss'].update(boss=80,pills={},reductions=[0]*4);self.b.save(role)
        self.call(17,index=1,type_id=1501);self.call(17,index=1,type_id=1502)
        self.assertEqual(self.b.profile()['activity']['abyss']['reductions'][0],20000)

    def test_stacked_bag_full_identity_gate_migration_and_claim(self):
        self.call(1);role=self.b.profile();s=role['activity']['abyss']
        s['bag']=[activity.prize_spec([5,1442,2,1]),activity.prize_spec([5,1442,3,1])]
        self.b.save(role);self.call(10);s=self.b.profile()['activity']['abyss']
        self.assertEqual(len(s['bag']),1);self.assertEqual(s['bag'][0]['attach_count'],5)
        tiny=dict(bag=[activity.prize_spec([5,1442,1,1])],grid_count=1)
        self.assertTrue(ab.store_drop(tiny,activity.prize_spec([5,1442,2,1])))
        self.assertFalse(ab.store_drop(tiny,activity.prize_spec([5,1443,1,1])))
        self.assertEqual(tiny['bag'][0]['attach_count'],3)
        self.call(5)
        self.assertEqual(sum(i['count'] for i in self.b.profile()['attachments'] if i['type_id']==1442),45)
        before=self.b.profile();self.assertEqual(self.req(1329,id=5,data='{}')[0][0],55)
        self.assertEqual(before,self.b.profile())

    def test_starter_training_and_victory_course_use_real_rewards(self):
        self.call(1)
        self.ok(self.req(1059,first_send=True,flag=3,cortege_id=0,roll_count=1,roll_list=[dict(type_id=1442,count=40)]))
        role=self.b.profile();self.assertEqual(role['drug_level'],4)
        # A real victory using only the existing test account and a legal HP pill.
        summon.add_item(role,1544,1);self.b.save(role);self.call(17,index=3,type_id=1544)
        before=self.b.profile();out=self.call(6);after=self.b.profile()
        self.assertTrue(out['is_win'])
        self.assertEqual(after['activity']['abyss']['crystals']-before['activity']['abyss']['crystals'],1208)
        self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
        self.assertEqual(after,self.b.profile())
        self.assertEqual(after['silver_coin']-before['silver_coin'],120000)
        self.assertTrue(set((1,6,11,16))<=set(after['activity']['abyss']['recipes']))
        self.assertEqual(after['drug_exp']-before['drug_exp'],balance.course_total(1))
        self.assertEqual(after['activity']['abyss']['pills'],{})

    def test_original_enemy_attributes_skills_and_panels_all_floors(self):
        original=copy.deepcopy(ab.NPCS)
        for floor in range(1,82):
            with self.subTest(floor=floor):
                state=dict(boss=floor,reductions=[0]*4)
                units=ab.enemies(state)
                tokens=next(v for k,v in ab.BOSSES[floor].items() if k and k.startswith('cortege_list')).split('/')
                self.assertEqual(len(units),len(tokens))
                for order,(unit,token) in enumerate(zip(units,tokens),1):
                    tid,_=map(int,token.split('|'));row=original[tid]
                    self.assertEqual((unit['type'],unit['order']),(tid,order))
                    for key,column in (('gongji','base_gongji'),('fangyu','base_fangyu'),
                                       ('hp','base_max_hp'),('magic','base_max_magic')):
                        self.assertEqual(unit[key],int(row[column]))
                    self.assertEqual(unit['max_hp'],int(row['base_max_hp']))
                    self.assertEqual((unit['level'],unit['evolve'],unit['reborn']),(1,0,0))
                    self.assertEqual(int(row['chushijineng']),0)
                    self.assertEqual(unit['skills'],[])
                role=self.b.profile();saved=ab.state(role,NOW,self.b.activity_rules)
                saved.update(boss=floor,reductions=[0]*4,pills={})
                panel=ab.boss(role,saved,NOW)['boss_data']
                totals=[sum(u[k] for u in units) for k in ('gongji','fangyu','hp','magic')]
                self.assertEqual(panel['boss_info'],totals)
                self.assertEqual(panel['max_list'],[v-len(units) for v in totals])
        self.assertEqual(ab.NPCS,original)
        self.assertEqual(ab.enemies(dict(boss=81,reductions=[0]*4))[0]['magic'],36000100)

    def test_original_magic_pill_panel_replay_and_restart(self):
        self.call(1);role=self.b.profile();state=role['activity']['abyss']
        state.update(boss=81,pills={'4':1656},reductions=[0,0,0,71921])
        before=copy.deepcopy(role['attachments']);self.b.save(role)
        panel=self.call(16)['boss_data']
        self.assertEqual(panel['boss_info'],dict(enumerate([1002599,45875,6002435,26852400],1)))
        self.assertEqual(panel['pill_list'],dict(enumerate([0,0,0,9148000],1)))
        self.assertEqual(self.b.profile()['attachments'],before)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.call(16)['boss_data'],panel)
        self.call(6)
        lineup=next(d for mid,_,d in self.decoded if mid==1028)['lineup']
        self.assertEqual(sum(u['des_magic'] for u in lineup if 'des_magic' in u),26852400)
        actions=[a for mid,_,d in self.decoded if mid==1027 for a in d['fight_result']]
        enemy_actions=[a for a in actions if not a['is_src']]
        self.assertTrue(enemy_actions)
        self.assertTrue(all(a['skill_type']==1 for a in enemy_actions))

    def test_essence_only_leader(self):
        units=ab.enemies(dict(boss=81,reductions=[0]*4))
        with patch('network_redirect.combat_engine.Battle') as engine:
            engine.return_value.run.return_value=(0,[],type('Actions',(list,),{'events':[]})())
            essence.battle({},([],units),self.b.journey_rules,{10113:50})
            passed=engine.call_args.args[1][1]
            self.assertEqual(passed[0]['extras'],{10113:50})
            self.assertTrue(all('extras' not in u for u in passed[1:]))
        self.assertTrue(all('extras' not in u for u in units))

    def test_economy_course_and_config_bounds(self):
        self.assertEqual(sum(next(p[2] for p in balance.victory_rewards(i) if p[1]==1441) for i in range(1,82)),180010)
        self.assertEqual(balance.course_total(72),sum(drug.LEVELS[i] for i in range(4,36)))
        self.assertEqual(balance.course_total(81),balance.course_total(72))
        self.assertEqual([balance.crystal_tick(dict(role_combat_power=10**9),dict(layer=i),self.b.activity_rules) for i in range(1,82,9)],[18,24,30,36,42,48,54,60,66])
        bad=copy.deepcopy(balance.rules());bad['quality_weights'][0][0]=-1
        path=Path(self.tmp.name)/'bad.json';path.write_text(json.dumps(bad))
        with self.assertRaises(formation.Rejected):balance.load_rules(path)
        for key,value in (('enemy_config_mode','scaled'),('region_stat_percent',[100]*9),
                          ('magic_attack_cap_percent',200),('leader_fallback_skill',101)):
            bad=copy.deepcopy(balance.rules());bad[key]=value
            path.write_text(json.dumps(bad))
            with self.assertRaises(formation.Rejected):balance.load_rules(path)

    def test_idle_multiplier_applies_below_cap_and_rejects_invalid_config(self):
        for floor in range(1,82):
            for power in (0,999,1000,1999,2000,2999,5000,11000,10**9):
                with self.subTest(floor=floor,power=power):
                    old_gain=min(3+(floor-1)//9,max(1,power//1000))
                    self.assertEqual(balance.crystal_tick(dict(role_combat_power=power),
                        dict(layer=floor),self.b.activity_rules),old_gain*6)
        path=Path(self.tmp.name)/'bad-multiplier.json'
        for value in (0,-1,True,1.5,None):
            cfg=copy.deepcopy(balance.rules());cfg['idle_crystal_multiplier']=value
            path.write_text(json.dumps(cfg))
            with self.assertRaises(formation.Rejected):balance.load_rules(path)

    def test_all_boss_crystals_double_after_rounding(self):
        for floor,row in ab.BOSSES.items():
            expected=[]
            for token in row['prirze_list'].split('/'):
                typ,tid,lv,n=map(int,token.split('|'))
                expected.append([typ,tid,2*max(1,n//100) if (typ,tid)==(5,1441) else n,lv])
            expected.append([12,0,100000+20000*floor,1])
            self.assertEqual(balance.victory_rewards(floor),expected)
        path=Path(self.tmp.name)/'bad-boss-multiplier.json'
        for value in (0,-1,True,1.5,None):
            cfg=copy.deepcopy(balance.rules());cfg['boss_crystal_multiplier']=value
            path.write_text(json.dumps(cfg))
            with self.assertRaises(formation.Rejected):balance.load_rules(path)

    def test_all_recipe_flags_fit_real_wire_and_persist(self):
        self.call(1);role=self.b.profile()
        state=role['activity']['abyss'];state['recipes']=list(range(1,41))
        self.assertEqual(drug.flags(role,state),dict(drug_study_flag=-2,drug_study_flag2=1022))
        self.b.save(role)
        self.call(22,client_flag=1)  # Includes actual 1032 encoding after the mutation.
        self.assertEqual(self.b.profile()['drug_study_flag'],-2)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.b.profile()['activity']['abyss']['recipes'],list(range(1,41)))

    def test_old_progress_training_catchup_once_without_replaying_money(self):
        self.call(1);role=self.b.profile();s=role['activity']['abyss']
        s.update(boss=73,layer=70,crystals=987654)
        del s['training_course_received'];role.update(drug_level=4,drug_exp=0)
        self.b.save(role);gold,silver=role['gold_coin'],role['silver_coin']
        self.call(1);after=self.b.profile()
        self.assertEqual(after['drug_level'],36)
        self.assertEqual(len(after['activity']['abyss']['recipes']),40)
        self.assertEqual((after['gold_coin'],after['silver_coin'],after['activity']['abyss']['crystals']),
                         (gold,silver,987654))
        self.assertEqual((after['activity']['abyss']['boss'],after['activity']['abyss']['layer']),(73,70))
        self.call(1);self.assertEqual(after,self.b.profile())
