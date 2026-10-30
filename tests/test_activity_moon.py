"""Exact probability intervals and real offline wire settlement for Mid-Autumn."""
import copy
import json
from collections import Counter
from pathlib import Path
from unittest.mock import patch
from test_activity import ActivityCase, NOW
from network_redirect import activity, activity_moon as moon, activity_seasonal as season, formation, summon
from network_redirect.backend import Backend


class MoonTests(ActivityCase):
    def count(self, tid, typ=5, role=None):
        role = role or self.b.profile()
        return sum((1 if typ == 6 else i['count']) for i in role['attachments']
                   if i['attach_type'] == typ and i['type_id'] == tid)

    def put(self, tid, count=1):
        r = self.b.profile();summon.add_item(r, tid, count);self.b.save(r)
        return next(i['id'] for i in r['attachments'] if i['type_id'] == tid and not i.get('is_lock'))

    def use(self, tid, ident, count=1, **kw):
        req = dict(item_type=tid, item_id=ident, item_count=count, des_type=1, des_id=0)
        req.update(kw)
        return self.req(1051, **req)

    def test_exact_all_pool_weight_tickets(self):
        for pool in moon.load_rules()['pools'].values():
            groups=pool['groups'];weights=[g['weight'] for g in groups]
            with patch.object(moon, 'randbelow', side_effect=range(10000)):
                actual=Counter(moon.weighted(list(range(len(groups))),weights) for _ in range(10000))
            self.assertEqual(actual, dict(enumerate(weights)))

    def test_material_exact_counts_independence_and_no_zero_items(self):
        r=self.b.activity_rules
        for index,tid in enumerate(moon.FILLINGS):
            counts=Counter()
            for ticket in range(100):
                rolls=[0,0,0,0,0];rolls[index+1]=ticket
                with patch.object(moon,'randbelow',side_effect=rolls):specs=moon.material_specs(r)
                counts[next((p[2] for p in specs if p[1]==tid),0)]+=1
                self.assertTrue(all(p[2]>0 for p in specs))
            self.assertEqual(counts,{0:10,1:70,2:20})
        for flour in range(3):
            with patch.object(moon,'randbelow',side_effect=[flour,0,10,79,80]):
                self.assertEqual(moon.material_specs(r),[[5,1134,flour+2,1],[5,1136,1,1],[5,1137,1,1],[5,1138,2,1]])
        with patch.object(moon,'randbelow',side_effect=[2,99,99,99,99]):
            self.assertEqual([p[2] for p in moon.material_specs(r)],[4,2,2,2,2])

    def test_all_candidates_credit_exact_quantity_via_wire(self):
        for tid,pool in moon.load_rules()['pools'].items():
            ticket=0
            for group in pool['groups']:
                for index,p in enumerate(group['candidates']):
                    ident=self.put(int(tid));before=self.b.profile()
                    rolls=[ticket]+([index] if len(group['candidates'])>1 else [])
                    with patch.object(moon,'randbelow',side_effect=rolls):out=self.use(int(tid),ident)
                    self.ok(out);after=self.b.profile()
                    data=next(d for e,d in out if e==21)
                    self.assertEqual(data['attach_list'],{1:activity.prize_spec(p)})
                    typ,target,n,_=p
                    if typ in (11,12):
                        field='gold_coin' if typ==11 else 'silver_coin'
                        self.assertEqual(after[field]-before[field],n)
                    else:
                        self.assertEqual(self.count(target,typ,after)-self.count(target,typ,before),n)
                    self.assertEqual(self.count(int(tid),role=after),self.count(int(tid),role=before)-1)
                    # Winning a card stores a card, never applies recharge automatically.
                    self.assertEqual(after.get('recharge'),before.get('recharge'))
                ticket+=group['weight']

    def test_batch_draws_independently_aggregates_and_replay_does_not_reroll(self):
        ident=self.put(1133,3);before=self.b.profile()
        with patch.object(moon,'randbelow',side_effect=[0,6500,9999]) as rng:out=self.use(1133,ident,3)
        self.ok(out);self.assertEqual(rng.call_count,3)
        self.assertEqual(self.b.profile()['silver_coin']-before['silver_coin'],50000)
        self.assertEqual(self.b.profile()['gold_coin']-before['gold_coin'],20)
        self.assertEqual(self.count(1152),self.count(1152,role=before)+1)
        saved=self.b.profile()
        with patch.object(moon,'randbelow',side_effect=AssertionError('rerolled')):
            self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
        self.assertEqual(saved,self.b.profile())
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(saved,self.b.profile())
        self.assertEqual(self.use(1133,ident)[0][0],55)

    def test_repeated_equipment_skills_and_stones_are_separate_instances(self):
        r=moon.load_rules()
        for tid,name in ((1131,'五星武器／防具成品'),(1131,'武器灵石'),(1132,'五星主动法术成品')):
            groups=r['pools'][str(tid)]['groups'];group=next(g for g in groups if name in g['name'])
            p=group['candidates'][0];ticket=sum(g['weight'] for g in groups[:groups.index(group)])
            before={i['id'] for i in self.b.profile()['attachments']};ident=self.put(tid,2)
            rolls=([ticket,0] if len(group['candidates'])>1 else [ticket])*2
            with patch.object(moon,'randbelow',side_effect=rolls):self.ok(self.use(tid,ident,2))
            gained=[i for i in self.b.profile()['attachments'] if i['id'] not in before and i['type_id']==p[1] and i['attach_type']==p[0]]
            self.assertEqual(len(gained),p[2]*2)
            self.assertEqual(len({i['id'] for i in gained}),p[2]*2)
            self.assertTrue(all(i['level']==1 and i['count']==(0 if p[0]==6 else 1) for i in gained))

    def test_selected_stack_and_invalid_use_are_atomic(self):
        first=self.put(1130,5);r=self.b.profile()
        second=dict(id=formation.new_id(r),attach_type=5,type_id=1130,count=2,level=1)
        r['attachments'].append(second);self.b.save(r)
        with patch.object(moon,'randbelow',return_value=0):self.ok(self.use(1130,second['id']))
        self.assertEqual(formation.lookup(self.b.profile(),'attachments',first)['count'],5)
        self.assertEqual(formation.lookup(self.b.profile(),'attachments',second['id'])['count'],1)
        for kw in (dict(item_count=0),dict(item_count=101),dict(item_count=2),dict(item_type=1131),dict(des_type=2),dict(des_id=999999)):
            before=self.b.profile()
            with patch.object(moon,'randbelow',side_effect=AssertionError('invalid draw')):
                self.assertEqual(self.use(1130,second['id'],**kw)[0][0],55)
            self.assertEqual(before,self.b.profile())
        for field in ('is_lock','owner_id','equip_pos','equip_order'):
            r=self.b.profile();formation.lookup(r,'attachments',second['id'])[field]=1;self.b.save(r);before=self.b.profile()
            self.assertEqual(self.use(1130,second['id'])[0][0],55);self.assertEqual(before,self.b.profile())
            r=self.b.profile();formation.lookup(r,'attachments',second['id'])[field]=0;self.b.save(r)

    def test_reward_encode_failure_and_balance_overflow_rollback(self):
        ident=self.put(1133);before=self.b.profile()
        with patch.object(moon,'randbelow',return_value=0),patch.object(moon.item_rewards,'grant',side_effect=formation.Rejected('test failure')):
            self.assertEqual(self.use(1133,ident)[0][0],55)
        self.assertEqual(before,self.b.profile())
        original=summon.event
        def fail_reward(kind,data):
            if kind==21:raise formation.Rejected('encode failure')
            return original(kind,data)
        with patch.object(moon,'randbelow',return_value=0),patch.object(moon.summon,'event',side_effect=fail_reward):
            self.assertEqual(self.use(1133,ident)[0][0],55)
        self.assertEqual(before,self.b.profile())
        r=self.b.profile();r['silver_coin']=2147483647;self.b.save(r);before=self.b.profile()
        with patch.object(moon,'randbelow',return_value=0):self.assertEqual(self.use(1133,ident)[0][0],55)
        self.assertEqual(before,self.b.profile())

    def test_permanent_crafting_starter_once_and_disabled_owned_food(self):
        self.ok(self.req(1205,flag=0));self.assertEqual(self.count(1134),60)
        rules=self.b.activity_rules;rules['seasonal_games']['moon'].update(start_time=2,end_time=3)
        self.ok(self.req(1205,flag=0));self.assertEqual(self.count(1134),60)
        rules['seasonal_games']['moon']['start_time']=1
        before=self.count(1134);self.ok(self.req(1205,flag=0));self.assertEqual(self.count(1134),before)
        self.ok(self.req(1333,flag=1,src_type=1135));self.assertEqual(self.count(1134),before-15)
        self.assertTrue(season.is_open(rules,'moon',2147483648))
        rules['seasonal_games']['moon']['enabled']=False
        self.assertEqual(moon.material_specs(rules),[])
        self.assertEqual(self.req(1333,flag=1,src_type=1135)[0][0],55)
        ident=next(i['id'] for i in self.b.profile()['attachments'] if i['type_id']==1130)
        with patch.object(moon,'randbelow',return_value=0):self.ok(self.use(1130,ident))

    def test_real_journey_sweep_independent_and_loss_no_materials(self):
        r=self.b.profile();r.update(vip_level=4,strength=100)
        r['journey']['gates']['1:101']=dict(pass_star=3,day_count=0,flush_count=0);self.b.save(r)
        before=self.count(1134)
        with patch.object(moon,'randbelow',side_effect=[0,0,0,0,0,1,10,10,10,10,2,80,80,80,80]) as rng:
            self.ok(self.req(1061,tollgate_type=1,tollgate_id=101,sweep_count=3))
        self.assertEqual(rng.call_count,15);self.assertEqual(self.count(1134)-before,9)
        for tid in moon.FILLINGS:self.assertEqual(self.count(tid),3)
        before=self.count(1134)
        with patch('network_redirect.journey.battle',return_value=(4,[],[])),patch.object(moon,'randbelow',side_effect=AssertionError('lost draw')):
            self.ok(self.req(1026,fight_type=1,des_type=1,des_id=101))
        self.assertEqual(self.count(1134),before)

    def test_duty_win_loss_and_party_actual_protocol(self):
        self.ok(self.req(1043,flag=0));self.ok(self.req(1043,plus_type=1,plus_index=1))
        with patch('network_redirect.journey.battle',return_value=(3,[],[])),patch.object(moon,'randbelow',side_effect=[2,0,10,80,99]):
            out=self.req(1026,fight_type=5,des_type=1,des_id=0,des_value=1);self.ok(out)
        self.assertEqual(self.count(1134),4);self.assertIn(22,[e for e,_ in out])
        before=self.b.profile()
        self.assertEqual(self.b.respond(self.packet,self.state),self.replies);self.assertEqual(before,self.b.profile())
        d=before['activity']['duty']
        if d['phase']=='prize':self.ok(self.req(1043,plus_type=3))
        with patch('network_redirect.journey.battle',return_value=(4,[],[])),patch.object(moon,'randbelow',side_effect=AssertionError('lost draw')):
            self.ok(self.req(1026,fight_type=5,des_type=1,des_id=0,des_value=2))
        self.assertEqual(self.count(1134),4)
        with patch('network_redirect.journey.battle',return_value=(4,[],[])),patch.object(moon,'randbelow',side_effect=[0,10,10,10,10]):
            self.ok(self.req(1026,fight_type=6))
        self.assertEqual(self.count(1134),6)

    def test_config_rejects_bad_probabilities_and_rewards(self):
        base=moon.load_rules();path=Path(self.tmp.name)/'bad-moon.json'
        for kind in ('total','negative','missing','reward','duplicate','drop','common_counts','common_weights'):
            r=copy.deepcopy(base);g=r['pools']['1130']['groups']
            if kind=='total':g[0]['weight']+=1
            if kind=='negative':g[0]['weight']=-1
            if kind=='missing':del r['pools']['1133']
            if kind=='reward':g[0]['candidates'][0][1]=1134
            if kind=='duplicate':g[1]['candidates']=copy.deepcopy(g[0]['candidates'])
            if kind=='drop':r['filling_weights']=[20,70,10]
            if kind=='common_counts':r['flour_counts']=[1,2,3]
            if kind=='common_weights':r['flour_weights']=[1,2,1]
            path.write_text(json.dumps(r))
            with self.assertRaises(formation.Rejected):moon.load_rules(path)

    def test_legacy_starter_migration_and_recipe_failure_rollback(self):
        r=self.b.profile();s=season.state(r);s['supplies']['moon:1']=True;self.b.save(r)
        self.ok(self.req(1205,flag=0));self.assertEqual(self.count(1134),0)
        self.assertTrue(self.b.profile()['activity']['seasonal']['supplies']['moon:permanent'])
        self.put(1135,15);before=self.b.profile()
        self.assertEqual(self.req(1333,flag=1,src_type=1135)[0][0],55)
        self.assertEqual(before,self.b.profile())
        self.put(1134,15);self.ok(self.req(1333,flag=1,src_type=1135))
        self.assertEqual(self.count(1130),1);self.assertEqual(self.count(1134),0)
        self.assertEqual(self.count(1135),0)

    def test_hundred_foods_aggregate_and_crafting_daily_limit(self):
        ident=self.put(1133,100);before=self.b.profile()
        with patch.object(moon,'randbelow',return_value=6500) as rng:out=self.use(1133,ident,100)
        self.ok(out);self.assertEqual(rng.call_count,100)
        self.assertEqual(self.b.profile()['gold_coin']-before['gold_coin'],2000)
        self.assertEqual(next(d for e,d in out if e==21)['attach_list'],{1:activity.prize_spec([11,0,2000,1])})
        self.put(1134,30);self.put(1135,30);r=self.b.profile()
        season.state(r)['counts'][f'moon:{activity.day(NOW,self.b.activity_rules)}']=100;self.b.save(r);before=self.b.profile()
        self.assertEqual(self.req(1333,flag=1,src_type=1135)[0][0],55);self.assertEqual(before,self.b.profile())
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):self.ok(self.req(1333,flag=1,src_type=1135))
