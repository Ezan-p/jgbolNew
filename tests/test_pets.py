"""Real 1330 -> 2998/174 packets and persistence, not direct fake success."""
import copy
from pathlib import Path
from unittest.mock import patch
from test_activity import ActivityCase
from network_redirect import pets, activity_home, summon, journey, combat_power
from network_redirect.backend import Backend

class PetTests(ActivityCase):
    def call(self, op, **data):
        result = self.req(1330, flag=1, id=op, data=summon.lua(data))
        self.ok(result)
        return next(d for e,d in result if e == 174)

    def seed(self, specs):
        r = self.b.profile()
        h = activity_home.state(r, 1792814400, self.b.activity_rules)
        h['pets'] = []; h['independent_pet_initialized'] = True
        for t,q in specs: pets.add(h,t,q)
        self.b.save(r)
        return [p['id'] for p in h['pets']]

    def home(self): return self.b.profile()['activity']['home']

    def test_entry_wire_and_starter_once(self):
        d = self.call(4)
        self.assertEqual(d['const_config']['min_train_quality'],3)
        p = next(iter(d['update_list'].values()))
        self.assertNotIn('main_type',p)
        self.assertEqual(p['prob_compen'],0)
        before = self.home()['pets']; self.call(4)
        self.assertEqual(before,self.home()['pets'])
        self.ok(self.req(1127,flag=1,act_type=0))
        self.assertTrue(next(d for e,d in self.req(1127,flag=1,act_type=0) if e==127)['animal_open'])

    def test_feed_exact_exp_repeat_and_restart(self):
        target, food = self.seed([(102,1),(101,1)])
        d = self.call(1,des_id=target,src_list=[food])
        self.assertEqual(pets.sequence(d['del_list']),[food])
        p = self.home()['pets'][0]
        self.assertEqual((p['level'],p['cur_exp']),(7,5600))
        before=self.b.profile()
        self.assertEqual(self.b.respond(self.packet,self.state), self.replies)
        self.assertEqual(before,self.b.profile())
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(before,self.b.profile())

    def test_select_toggle_and_protect_material(self):
        first, second=self.seed([(102,1),(103,2)])
        self.call(3,des_id=first); self.call(3,des_id=second)
        self.assertEqual([p['order'] for p in self.home()['pets']],[0,1])
        before=self.b.profile()
        self.assertEqual(self.req(1330,flag=1,id=1,data=summon.lua(dict(des_id=first,src_list=[second])))[0][0],55)
        self.assertEqual(before,self.b.profile())
        self.call(3,des_id=second)
        self.assertEqual([p['order'] for p in self.home()['pets']],[0,0])

    def test_fusion_three_materials_and_compensation(self):
        target,*sources=self.seed([(102,1)]*4)
        with patch('network_redirect.pets.secrets.randbelow',return_value=0):
            self.call(2,des_id=target,src_list=sources)
        p=self.home()['pets'][0]
        self.assertEqual(p['quality'],1);self.assertEqual(p['prob_compen'],3)
        self.assertEqual(len(self.home()['pets']),1)
        for k,v in zip(pets.hp.ATTR,p['grow_values']):
            lo,hi=pets.growth_range(102,k,1);self.assertTrue(lo<=v<=hi)

    def test_star_and_train_full_cycle(self):
        target,*sources=self.seed([(102,3)]+[(102,1)]*5)
        r=self.b.profile()
        for tid in (1347,1345):summon.add_item(r,tid,100)
        self.b.save(r)
        self.call(6,des_id=target,src_list=sources,order_list=[999]*5)
        self.assertEqual(self.home()['pets'][0]['star_level'],1)
        for pos in range(1,5):
            for _ in range(4):
                r=self.b.profile();summon.add_item(r,1345,15);self.b.save(r)
                self.call(5,des_id=target,pos=pos)
        self.assertEqual(self.home()['pets'][0]['train_levels'],[4]*4)
        before=self.b.profile()
        self.assertEqual(self.req(1330,flag=1,id=5,data=summon.lua(dict(des_id=target,pos=1)))[0][0],55)
        self.assertEqual(before,self.b.profile())

    def test_invalid_and_insufficient_are_atomic(self):
        target,food=self.seed([(102,3),(102,1)])
        for op,data in [(1,dict(des_id=target,src_list=[food,food])),(1,dict(des_id=target,src_list=[target])),
                        (2,dict(des_id=target,src_list=[food])),(5,dict(des_id=target,pos=5)),
                        (6,dict(des_id=target,src_list=[food])),(3,dict(des_id=True))]:
            before=self.b.profile()
            self.assertEqual(self.req(1330,flag=1,id=op,data=summon.lua(data))[0][0],55)
            self.assertEqual(before,self.b.profile())
        r=self.b.profile();r['level']=49;self.b.save(r)
        self.assertEqual(self.req(1330,flag=1,id=4,data='{}')[0][0],55)

    def test_reward_ids_never_reused_and_home_starter_no_collision(self):
        target,food=self.seed([(102,1),(101,1)])
        self.call(1,des_id=target,src_list=[food])
        r=self.b.profile();journey.grant(r,[15,201,1,2]);self.b.save(r)
        self.assertGreater(self.home()['pets'][-1]['id'],food)
        r=self.b.profile();h=r['activity']['home'];h['build']['5']=1
        pets.hp.initialize(h,self.b.activity_rules)
        self.assertEqual(len({p['id'] for p in h['pets']}),len(h['pets']))

    def test_panel_original_level_rate_special_and_quality_gates(self):
        r={'activity':{'home':{'pets':[dict(type_id=201,order=1,quality=2,level=10,
            grow_values=[20,20,20,20],star_level=0,train_levels=[0]*4)]}}}
        values={s:0 for s in combat_power.STATS}
        combat_power.add_pet(r,{'order':1},values)
        self.assertEqual(values['gongji'],80)
        r['activity']['home']['pets'][0]['quality']=3
        values={s:0 for s in combat_power.STATS}
        combat_power.add_pet(r,{'order':1},values)
        self.assertEqual(values['gongji'],88) # 80 + magic(40)/5

    def test_fusion_probability_distribution(self):
        for main in (1,2):
            for quality in range(1,5):
                for value in (0,1,3,24,210,1200,45000):
                    p=pets.fusion_probabilities(main,quality,value)
                    self.assertAlmostEqual(sum(p.values()),1)
                    self.assertTrue(all(0<=v<=1 for v in p.values()))

    def test_all_stars_exact_cost_and_stage_limits(self):
        target, = self.seed([(201,4)])
        for star in range(9):
            r=self.b.profile();h=r['activity']['home'];p=h['pets'][0]
            if star:p['train_levels']=[4]*4
            sources=[]
            for token in pets.STAR[star]['star_consume2'].split('/'):
                typ,q,n=map(int,token.split('|'))
                tid=typ if typ>3 else 102 if typ==1 else 201
                sources += [pets.add(h,tid,q)['id'] for _ in range(n)]
            _,tid,_,n=map(int,pets.STAR[star]['star_consume1'].split('|'))
            summon.add_item(r,tid,n);self.b.save(r)
            self.call(6,des_id=target,src_list=sources)
            self.assertEqual(self.home()['pets'][0]['star_level'],star+1)
            self.assertEqual(self.home()['pets'][0]['train_levels'],[0]*4)
        before=self.b.profile()
        self.assertEqual(self.req(1330,flag=1,id=6,data=summon.lua(dict(des_id=target,src_list=[])))[0][0],55)
        self.assertEqual(before,self.b.profile())

    def test_missing_star_item_rolls_back_all_materials(self):
        target,*sources=self.seed([(201,3)]+[(102,1)]*5)
        before=self.b.profile()
        self.assertEqual(self.req(1330,flag=1,id=6,data=summon.lua(dict(des_id=target,src_list=sources)))[0][0],55)
        self.assertEqual(before,self.b.profile())

    def test_max_level_rejects_without_consuming(self):
        target,food=self.seed([(102,1),(101,1)])
        r=self.b.profile();p=r['activity']['home']['pets'][0];p['level']=200;self.b.save(r)
        before=self.b.profile()
        self.assertEqual(self.req(1330,flag=1,id=1,data=summon.lua(dict(des_id=target,src_list=[food])))[0][0],55)
        self.assertEqual(before,self.b.profile())

    def test_star_stones_have_purchasable_source(self):
        r=self.b.profile();summon.add_item(r,1361,10000);self.b.save(r)
        for tid in (1347,1348,1349):
            index=next(i for i,row in enumerate(self.b.activity_rules['home_shop'],1) if row['reward'][1]==tid)
            self.ok(self.req(1348,id=15,data=summon.lua(dict(shop_page=1,item_index=index,buy_count=1))))
            self.assertEqual(sum(p['count'] for p in self.b.profile()['attachments'] if p['type_id']==tid),5)

    def test_full_capacity_query_fits_native_packet(self):
        self.seed([(201,4)]*pets.load_rules()['capacity'])
        d=self.call(4)
        self.assertEqual(len(d['update_list']),pets.load_rules()['capacity'])
        r=self.b.profile();r['activity']['home']['build']['5']=1;self.b.save(r)
        self.call(4)  # a pending home starter must not lock a full pet bag
        r=self.b.profile();before=copy.deepcopy(r)
        with self.assertRaises(ValueError):journey.grant(r,[15,201,1,4])
        self.assertEqual(before,r)

    def test_training_box_use_replay_and_locked_rejection(self):
        r=self.b.profile();summon.add_item(r,1346,3);self.b.save(r)
        item=next(p for p in r['attachments'] if p['type_id']==1346)
        self.ok(self.req(1051,item_type=1346,item_id=item['id'],item_count=2,des_type=1,des_id=0))
        r=self.b.profile()
        self.assertEqual(sum(p['count'] for p in r['attachments'] if p['type_id']==1345),30)
        self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
        self.assertEqual(r,self.b.profile())
        next(p for p in r['attachments'] if p['type_id']==1346)['is_lock']=True
        self.b.save(r);before=self.b.profile()
        self.assertEqual(self.req(1051,item_type=1346,item_id=item['id'],item_count=1,des_type=1,des_id=0)[0][0],55)
        self.assertEqual(before,self.b.profile())

    def test_experience_pet_cannot_train_or_star(self):
        target,*sources=self.seed([(101,3)]+[(102,1)]*5)
        r=self.b.profile();summon.add_item(r,1347,100);summon.add_item(r,1345,100);self.b.save(r)
        for op in (3,5,6):
            before=self.b.profile()
            self.assertEqual(self.req(1330,flag=1,id=op,data=summon.lua(dict(des_id=target,pos=1,src_list=sources)))[0][0],55)
            self.assertEqual(before,self.b.profile())

    def test_client_entry_adapter_is_packaged(self):
        source=summon.client_source(summon.load_rules())
        self.assertIn('profile.showPlayerInfoLayer=function',source)
        self.assertIn('pet.pet_is_open=true',source)
        self.assertIn('_localPetRestore',Path('network_redirect/summon_client.js').read_text())
