"""Dragon Boat protocol rewards, independent rolls, persistence and parity."""
import copy
from collections import Counter
from pathlib import Path
from unittest.mock import patch
from test_activity import ActivityCase, NOW
from network_redirect import activity, activity_moon as moon, activity_rice as rice
from network_redirect import activity_food as food, activity_seasonal as season, formation, summon
from network_redirect.backend import Backend


class RiceTests(ActivityCase):
    def count(self, tid, typ=5, role=None):
        r=role or self.b.profile()
        return sum(1 if typ==6 else i['count'] for i in r['attachments'] if i['attach_type']==typ and i['type_id']==tid)

    def put(self, tid, count=1):
        r=self.b.profile();summon.add_item(r,tid,count);self.b.save(r)
        return next(i['id'] for i in r['attachments'] if i['type_id']==tid and not i.get('is_lock'))

    def use(self, tid, ident, count=1, **changes):
        req=dict(item_type=tid,item_id=ident,item_count=count,des_type=1,des_id=0);req.update(changes)
        return self.req(1051,**req)

    def craft(self, index=1, ids=None):
        if ids is None:
            r=self.b.profile()
            ids=[next(i['id'] for i in r['attachments'] if i['type_id']==tid and i['attach_type']==5 and not i.get('is_lock')) for tid in (1208,1208+index)]
        return self.req(1126,compose_type=index,material_count=len(ids),material_list=[dict(id=i) for i in ids])

    def test_shared_pools_all_tickets_and_every_concrete_reward(self):
        self.assertEqual(rice.FOOD_POOLS,{1213:1130,1214:1131,1215:1132,1216:1133})
        outcomes=0
        for tid,moon_id in rice.FOOD_POOLS.items():
            pool=self.b.activity_rules['moon_rules']['pools'][str(moon_id)]
            groups=pool['groups'];weights=[g['weight'] for g in groups]
            with patch.object(rice,'randbelow',side_effect=range(10000)):
                counts=Counter(food.weighted(list(range(len(groups))),weights,rice.randbelow) for _ in range(10000))
            self.assertEqual(counts,dict(enumerate(weights)))
            ticket=0
            for g in groups:
                for index,p in enumerate(g['candidates']):
                    ident=self.put(tid);before=self.b.profile()
                    rolls=[ticket]+([index] if len(g['candidates'])>1 else [])
                    with patch.object(rice,'randbelow',side_effect=rolls),patch.object(moon,'randbelow',side_effect=AssertionError('shared moon roll')):
                        out=self.use(tid,ident)
                    self.ok(out);outcomes+=1;after=self.b.profile()
                    self.assertEqual(next(d for e,d in out if e==21)['attach_list'],{1:activity.prize_spec(p)})
                    typ,target,n,level=p
                    if typ in (11,12):
                        key='gold_coin' if typ==11 else 'silver_coin';self.assertEqual(after[key]-before[key],n)
                    else:
                        self.assertEqual(self.count(target,typ,after)-self.count(target,typ,before),n)
                        if typ==6 or formation.ITEMS[target]['can_stack']=='0':
                            oldids={i['id'] for i in before['attachments']}
                            gained=[i for i in after['attachments'] if i['id'] not in oldids and i['type_id']==target and i['attach_type']==typ]
                            self.assertEqual(len(gained),n)
                            self.assertTrue(all(i['level']==level and i['count']==(0 if typ==6 else 1) for i in gained))
                    self.assertEqual(self.count(tid,role=after),self.count(tid,role=before)-1)
                    self.assertEqual(before.get('recharge'),after.get('recharge'))
                ticket+=g['weight']
        self.assertEqual(outcomes,108)

    def test_material_probability_boundaries_and_independent_events(self):
        shared=self.b.activity_rules
        for index,tid in enumerate(rice.FILLINGS):
            counts=Counter()
            for ticket in range(100):
                rolls=[0,0,0,0,0];rolls[index+1]=ticket
                with patch.object(rice,'randbelow',side_effect=rolls):specs=rice.material_specs(shared)
                counts[next((p[2] for p in specs if p[1]==tid),0)]+=1
                self.assertTrue(all(p[2]>0 for p in specs))
            self.assertEqual(counts,{0:10,1:70,2:20})
        for leaf in range(3):
            with patch.object(rice,'randbelow',side_effect=[leaf,0,10,79,80]):
                self.assertEqual(rice.material_specs(shared),[[5,1208,leaf+2,1],[5,1210,1,1],[5,1211,1,1],[5,1212,2,1]])
        with patch.object(rice,'randbelow',side_effect=[2,80,80,80,80]) as rr,patch.object(moon,'randbelow',side_effect=[0,0,0,0,0]) as mr:
            specs=season.material_specs(shared)
        self.assertEqual((rr.call_count,mr.call_count),(5,5))
        self.assertEqual(specs,[[5,1208,4,1]]+[[5,t,2,1] for t in rice.FILLINGS]+[[5,1134,2,1]])
        shared['seasonal_games']['rice']['enabled']=False
        with patch.object(rice,'randbelow',side_effect=AssertionError('disabled roll')),patch.object(moon,'randbelow',side_effect=[1,10,10,10,10]):
            self.assertEqual([p[1] for p in season.material_specs(shared)],[1134,1135,1136,1137,1138])
        shared['seasonal_games']['rice']['enabled']=True;shared['seasonal_games']['moon']['enabled']=False
        with patch.object(moon,'randbelow',side_effect=AssertionError('disabled roll')),patch.object(rice,'randbelow',side_effect=[0,0,0,0,0]):
            self.assertEqual(season.material_specs(shared),[[5,1208,2,1]])

    def test_batch_one_hundred_independent_and_moon_opening_not_shared(self):
        ident=self.put(1216,100);mid=self.put(1133);before=self.b.profile()
        with patch.object(rice,'randbelow',side_effect=[0,6500]*50) as rr,patch.object(moon,'randbelow',return_value=9999) as mr:
            out=self.use(1216,ident,100);self.ok(out);self.ok(self.use(1133,mid))
        self.assertEqual((rr.call_count,mr.call_count),(100,1))
        after=self.b.profile();self.assertEqual(after['silver_coin']-before['silver_coin'],2500000)
        self.assertEqual(after['gold_coin']-before['gold_coin'],1000)
        self.assertEqual(self.count(1152)-self.count(1152,role=before),1)
        self.assertEqual(len(next(d for e,d in out if e==21)['attach_list']),2)

    def test_replay_restart_and_consumed_id(self):
        ident=self.put(1216,3)
        with patch.object(rice,'randbelow',side_effect=[0,6500,9999]):self.ok(self.use(1216,ident,3))
        before=self.b.profile()
        with patch.object(rice,'randbelow',side_effect=AssertionError('reroll')):
            self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
        self.assertEqual(before,self.b.profile())
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(before,self.b.profile());self.assertEqual(self.use(1216,ident)[0][0],55)

    def test_invalid_requests_selected_stack_and_rollback(self):
        first=self.put(1213,5);r=self.b.profile()
        second=dict(id=formation.new_id(r),attach_type=5,type_id=1213,count=2,level=1);r['attachments'].append(second);self.b.save(r)
        with patch.object(rice,'randbelow',return_value=0):self.ok(self.use(1213,second['id']))
        self.assertEqual(formation.lookup(self.b.profile(),'attachments',first)['count'],5)
        self.assertEqual(formation.lookup(self.b.profile(),'attachments',second['id'])['count'],1)
        for changes in (dict(item_count=0),dict(item_count=101),dict(item_count=2),dict(item_type=1214),dict(des_type=2),dict(des_id=999999)):
            before=self.b.profile()
            with patch.object(rice,'randbelow',side_effect=AssertionError('invalid roll')):
                self.assertEqual(self.use(1213,second['id'],**changes)[0][0],55)
            self.assertEqual(before,self.b.profile())
        for key in ('is_lock','owner_id','equip_pos','equip_order'):
            r=self.b.profile();formation.lookup(r,'attachments',second['id'])[key]=1;self.b.save(r);before=self.b.profile()
            self.assertEqual(self.use(1213,second['id'])[0][0],55);self.assertEqual(before,self.b.profile())
            r=self.b.profile();formation.lookup(r,'attachments',second['id'])[key]=0;self.b.save(r)

    def test_grant_encoding_and_balance_failures_atomic(self):
        ident=self.put(1216);before=self.b.profile()
        with patch.object(rice,'randbelow',return_value=0),patch.object(food.item_rewards,'grant',side_effect=formation.Rejected('test grant')):
            self.assertEqual(self.use(1216,ident)[0][0],55)
        self.assertEqual(before,self.b.profile())
        original=summon.event
        def fail(kind,data):
            if kind==21:raise formation.Rejected('test encode')
            return original(kind,data)
        with patch.object(rice,'randbelow',return_value=0),patch.object(summon,'event',side_effect=fail):
            self.assertEqual(self.use(1216,ident)[0][0],55)
        self.assertEqual(before,self.b.profile())
        r=self.b.profile();r['silver_coin']=2147483647;self.b.save(r);before=self.b.profile()
        with patch.object(rice,'randbelow',return_value=0):self.assertEqual(self.use(1216,ident)[0][0],55)
        self.assertEqual(before,self.b.profile())

    def test_starter_once_permanent_migration_and_closed_food(self):
        self.ok(self.req(1205,flag=0));self.assertEqual(self.count(1208),60)
        for tid in rice.FILLINGS:self.assertEqual(self.count(tid),15)
        r=self.b.activity_rules;r['seasonal_games']['rice'].update(start_time=2,end_time=3)
        self.assertTrue(season.is_open(r,'rice',2147483648))
        self.ok(self.req(1205,flag=0));self.assertEqual(self.count(1208),60)
        for index in range(1,5):self.ok(self.craft(index))
        self.assertEqual(self.count(1208),0);self.assertEqual(self.count(1217),0)
        r['seasonal_games']['rice']['enabled']=False
        self.assertEqual(self.craft(1,[1,2])[0][0],55)
        ident=next(i['id'] for i in self.b.profile()['attachments'] if i['type_id']==1213)
        with patch.object(rice,'randbelow',return_value=0):self.ok(self.use(1213,ident))

    def test_legacy_claim_preserved_and_counters_start_without_invented_history(self):
        r=self.b.profile();s=season.state(r);s.pop('rice_count');s['supplies']['rice:1']=True
        s['rice_news']=[dict(name='旧记录',data=[1213])];s['moon_count']=9;self.b.save(r)
        self.ok(self.req(1205,flag=0));self.assertEqual(self.count(1208),0)
        s=self.b.profile()['activity']['seasonal'];self.assertEqual(s['rice_count'],0);self.assertEqual(s['moon_count'],9)
        self.assertTrue(s['supplies']['rice:permanent'])
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.ok(self.req(1205,flag=0));self.assertEqual(self.count(1208),0)

    def test_crafting_bonus_daily_limit_and_moon_progress_are_independent(self):
        self.put(1208,180);self.put(1209,180);self.put(1134,30);self.put(1135,30)
        r=self.b.profile();s=season.state(r);s['moon_count']=9;self.b.save(r)
        before=self.count(1001)
        for _ in range(10):self.ok(self.craft())
        s=self.b.profile()['activity']['seasonal'];self.assertEqual((s['rice_count'],s['moon_count']),(10,9))
        self.assertEqual(self.count(1001)-before,10)
        self.ok(self.req(1333,flag=1,src_type=1135));self.assertEqual(self.count(1001)-before,20)
        r=self.b.profile();season.state(r)['counts'][f'rice:{activity.day(NOW,self.b.activity_rules)}']=100;self.b.save(r);before=self.b.profile()
        self.assertEqual(self.craft()[0][0],55);self.assertEqual(before,self.b.profile())
        self.ok(self.req(1333,flag=1,src_type=1135))
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):self.ok(self.craft())
        self.assertEqual(self.b.profile()['activity']['seasonal']['rice_count'],11)

    def test_recipe_ids_consumed_exactly_and_bad_sources_rejected(self):
        first=[self.put(t,30) for t in (1208,1209)];r=self.b.profile();chosen=[]
        for tid in (1208,1209):
            i=dict(id=formation.new_id(r),attach_type=5,type_id=tid,count=15,level=1);chosen.append(i['id']);r['attachments'].append(i)
        self.b.save(r);self.ok(self.craft(ids=chosen))
        self.assertTrue(all(formation.lookup(self.b.profile(),'attachments',i)['count']==30 for i in first))
        for ids in ([first[0],first[0]],[first[1],first[0],first[1]],chosen,[first[1],999999]):
            before=self.b.profile();self.assertEqual(self.craft(ids=ids)[0][0],55);self.assertEqual(before,self.b.profile())
        r=self.b.profile();formation.lookup(r,'attachments',first[0])['is_lock']=1;self.b.save(r);before=self.b.profile()
        self.assertEqual(self.craft(ids=first)[0][0],55);self.assertEqual(before,self.b.profile())

    def test_journey_sweep_and_defeat_separate_random_results(self):
        r=self.b.profile();r.update(vip_level=4,strength=100)
        r['journey']['gates']['1:101']=dict(pass_star=3,day_count=0,flush_count=0);self.b.save(r)
        with patch.object(rice,'randbelow',side_effect=[2,80,80,80,80]*3) as rr,patch.object(moon,'randbelow',side_effect=[0,0,0,0,0]*3) as mr:
            self.ok(self.req(1061,tollgate_type=1,tollgate_id=101,sweep_count=3))
        self.assertEqual((rr.call_count,mr.call_count),(15,15))
        self.assertEqual(self.count(1208),12);self.assertEqual(self.count(1134),6)
        self.assertEqual([self.count(t) for t in rice.FILLINGS],[6]*4)
        self.assertEqual([self.count(t) for t in moon.FILLINGS],[0]*4)
        before=self.b.profile()
        with patch('network_redirect.journey.battle',return_value=(4,[],[])),patch.object(rice,'randbelow',side_effect=AssertionError('lost drop')):
            self.ok(self.req(1026,fight_type=1,des_type=1,des_id=101))
        self.assertEqual(self.count(1208),self.count(1208,role=before))

    def test_duty_and_party_both_events_rolled_once_per_settlement(self):
        self.ok(self.req(1043,flag=0));self.ok(self.req(1043,plus_type=1,plus_index=1))
        with patch('network_redirect.journey.battle',return_value=(3,[],[])),patch.object(rice,'randbelow',side_effect=[2,80,80,80,80]) as rr,patch.object(moon,'randbelow',side_effect=[0,0,0,0,0]) as mr:
            out=self.req(1026,fight_type=5,des_type=1,des_id=0,des_value=1);self.ok(out)
        self.assertEqual((rr.call_count,mr.call_count),(5,5));self.assertEqual(self.count(1208),4)
        self.assertEqual(self.count(1134),2);self.assertIn(22,[e for e,d in out])
        before=self.b.profile();self.assertEqual(self.b.respond(self.packet,self.state),self.replies);self.assertEqual(before,self.b.profile())
        if before['activity']['duty']['phase']=='prize':self.ok(self.req(1043,plus_type=3))
        with patch('network_redirect.journey.battle',return_value=(4,[],[])),patch.object(rice,'randbelow',side_effect=AssertionError('lost drop')):
            self.ok(self.req(1026,fight_type=5,des_type=1,des_id=0,des_value=2))
        with patch('network_redirect.journey.battle',return_value=(4,[],[])),patch.object(rice,'randbelow',side_effect=[0,0,0,0,0]) as rr,patch.object(moon,'randbelow',side_effect=[2,80,80,80,80]) as mr:
            self.ok(self.req(1026,fight_type=6))
        self.assertEqual((rr.call_count,mr.call_count),(5,5));self.assertEqual((self.count(1208),self.count(1134)),(6,6))

    def test_legacy_five_star_inventory_can_still_be_opened(self):
        ident=self.put(1217);before=self.count(1343)
        self.ok(self.use(1217,ident));self.assertEqual(self.count(1343),before+1)
