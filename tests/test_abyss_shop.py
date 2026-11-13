"""Material shop selection, migration and real protocol settlement regressions."""
import copy
import json
from itertools import permutations
from collections import Counter
from pathlib import Path
from unittest.mock import patch
from tests.test_activity import ActivityCase, NOW
from network_redirect import activity, activity_abyss as abyss, summon
from network_redirect.backend import Backend


class AbyssShopTests(ActivityCase):
    def setUp(self):
        super().setUp()
        role=self.b.profile();role['level']=80;self.b.save(role)
        self.call(13)

    def call(self,op,**data):
        out=self.req(1329,id=op,data=summon.lua(data));self.ok(out)
        return next(value for ident,value in out if ident==173 and value['flag']==op)

    def test_config_rejects_non_material_duplicate_missing_and_bad_weights(self):
        rules=self.b.activity_rules
        self.assertEqual({p['reward'][1] for p in rules['abyss_shop']},
                         {1329,1330,1331,1332,1310,1311,1312,1333})
        changes=[lambda r:r['abyss_shop'][0]['reward'].__setitem__(1,1001),
                 lambda r:r['abyss_shop'][0]['reward'].__setitem__(1,1701),
                 lambda r:r['abyss_shop'][0]['reward'].__setitem__(1,10101),
                 lambda r:r['abyss_shop'][0]['reward'].__setitem__(1,10201),
                 lambda r:r['abyss_shop'][-1]['reward'].__setitem__(1,1334),
                 lambda r:r['abyss_shop'][-1]['reward'].__setitem__(1,1335),
                 lambda r:r['abyss_shop'][0]['reward'].__setitem__(1,10000),
                 lambda r:r['abyss_shop'][0].__setitem__('weight',0),
                 lambda r:r['abyss_shop'][0].__setitem__('weight',True),
                 lambda r:r['abyss_shop'][0].__setitem__('category','other'),
                 lambda r:r['abyss_shop'].pop(),
                 lambda r:r['abyss_shop'].append(copy.deepcopy(r['abyss_shop'][0])),
                 lambda r:r.__setitem__('abyss_shop_daily_count',5),
                 lambda r:r['abyss_shop'][0].__setitem__('guaranteed',True),
                 lambda r:r['abyss_shop'][5].__setitem__('guaranteed',True),
                 lambda r:r['abyss_shop'][0].__setitem__('weight',1),
                 lambda r:r['abyss_shop'][0].__setitem__('guaranteed',1)]
        path=Path(self.tmp.name)/'invalid.json'
        for change in changes:
            r=copy.deepcopy(rules);change(r);path.write_text(json.dumps(r))
            with self.assertRaises(ValueError):activity.load_rules(path)

    def test_daily_probabilities_match_six_weighted_draws(self):
        rules=self.b.activity_rules;counts=Counter();trials=12000
        for role_id in range(trials):
            offers=abyss.refresh_shop({},dict(role_id=role_id),rules,12345)
            self.assertFalse(any(p['guaranteed'] for p in offers))
            self.assertEqual(len({p['reward'][1] for p in offers}),6)
            counts.update(p['reward'][1] for p in offers)
        expected=Counter();pool=rules['abyss_shop'];total=sum(q['weight'] for q in pool)
        for order in permutations(pool,6):
            chance=1;remaining=total
            for q in order:
                chance*=q['weight']/remaining;remaining-=q['weight']
            for q in order:expected[q['reward'][1]]+=chance
        for p in pool:
            tid=p['reward'][1]
            self.assertGreater(counts[tid],0)
            self.assertLess(counts[tid],trials,'no material may be permanently listed')
            self.assertAlmostEqual(counts[tid]/trials,expected[tid],delta=.018)

    def test_all_materials_exact_cost_quantity_limit_and_replay(self):
        for product in self.b.activity_rules['abyss_shop']:
            role=self.b.profile();s=role['activity']['abyss'];s['shop'][0]=copy.deepcopy(product)
            s['purchases']={};s['crystals']=product['cost']*product['limit'];self.b.save(role)
            tid=product['reward'][1]
            def owned(r):return sum(i['count'] for i in r['attachments'] if i['attach_type']==5 and i['type_id']==tid)
            before=owned(role)
            self.call(12,index=1,count=product['limit'],shop_day=s['shop_day'],shop_revision=s['shop_revision'])
            after=self.b.profile()
            self.assertEqual(owned(after)-before,product['reward'][2]*product['limit'])
            self.assertEqual(after['activity']['abyss']['crystals'],0)
            self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
            self.assertEqual(after,self.b.profile())
            self.assertEqual(self.req(1329,id=12,data=summon.lua(dict(index=1,count=1)))[0][0],55)
            self.assertEqual(after,self.b.profile())

    def test_v15_bulk_essences_migrate_to_single_units_and_500_limit(self):
        role=self.b.profile();s=role['activity']['abyss']
        old=copy.deepcopy(s['shop']);old[0].update(reward=[5,1310,100,1],cost=1000,limit=5)
        revision='2026-11-13-no-essence-stone-v15'
        s.update(shop=old,shop_revision=revision,crystals=20000,purchases={'old':2})
        inventory=copy.deepcopy(role['attachments']);self.b.save(role)
        first=self.call(13);saved=self.b.profile()
        self.assertEqual(saved['attachments'],inventory)
        self.assertEqual(saved['activity']['abyss']['crystals'],20000)
        self.assertEqual(saved['activity']['abyss']['purchases'],{})
        self.assertEqual(self.req(1329,id=12,data=summon.lua(dict(index=1,count=1,
            shop_day=first['shop_day'],shop_revision=revision)))[0][0],55)
        self.assertEqual(saved,self.b.profile())
        # Selection is random; pin an essence to test the purchase contract.
        saved['activity']['abyss']['shop'][0]=copy.deepcopy(next(
            p for p in self.b.activity_rules['abyss_shop'] if p['reward'][1]==1310))
        self.b.save(saved)
        current=self.call(13)
        self.assertEqual(current['shop_list'][1]['attach_count'],1)
        self.assertEqual(current['shop_list'][1]['crystals'],20)
        self.assertEqual(current['shop_list'][1]['buy_times'],500)
        def owned(role):
            return sum(i['count'] for i in role['attachments'] if i['attach_type']==5 and i['type_id']==1310)
        before=owned(saved)
        self.call(12,index=1,count=1)
        self.assertEqual(self.b.profile()['activity']['abyss']['crystals'],19980)
        self.assertEqual(owned(self.b.profile())-before,1)
        self.call(12,index=1,count=499);saved=self.b.profile()
        self.assertEqual(saved['activity']['abyss']['crystals'],10000)
        self.assertEqual(owned(saved)-before,500)
        self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
        self.assertEqual(saved,self.b.profile())
        self.assertEqual(self.req(1329,id=12,data=summon.lua(dict(index=1,count=1)))[0][0],55)
        self.assertEqual(saved,self.b.profile())

    def test_five_batches_of_100_use_500_daily_quota_once(self):
        role=self.b.profile();s=role['activity']['abyss']
        s['shop'][0]=copy.deepcopy(next(p for p in self.b.activity_rules['abyss_shop'] if p['reward'][1]==1310))
        s['crystals']=20000;s['purchases']={};self.b.save(role)
        def owned(role):
            return sum(i['count'] for i in role['attachments'] if i['attach_type']==5 and i['type_id']==1310)
        before=owned(role)
        for batch in range(1,6):
            self.call(12,index=1,count=100,shop_day=s['shop_day'],shop_revision=s['shop_revision'])
            saved=self.b.profile()
            self.assertEqual(owned(saved)-before,batch*100)
            self.assertEqual(saved['activity']['abyss']['crystals'],20000-batch*2000)
            self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
            self.assertEqual(self.b.profile(),saved)
            self.assertEqual(self.call(13)['shop_list'][1]['buy_times'],500-batch*100)
        saved=self.b.profile()
        self.assertEqual(self.req(1329,id=12,data=summon.lua(dict(index=1,count=1)))[0][0],55)
        self.assertEqual(self.b.profile(),saved)

    def test_insufficient_currency_and_invalid_quantity_are_atomic(self):
        role=self.b.profile();s=role['activity']['abyss'];s['crystals']=s['shop'][0]['cost']-1;self.b.save(role)
        for count in [1,0,-1,1.5,True,10000]:
            before=self.b.profile()
            self.assertEqual(self.req(1329,id=12,data=summon.lua(dict(index=1,count=count)))[0][0],55)
            self.assertEqual(before,self.b.profile())

    def test_revision_migration_removes_old_offers_without_losing_resources(self):
        role=self.b.profile();s=role['activity']['abyss']
        summon.add_item(role,10101,3);summon.add_item(role,10201,2)
        # Seed valid essence objects, including the normal progression field.
        for item in role['attachments']:
            if item['type_id'] in (10101,10201):item.setdefault('prob_compen',0)
        s.update(shop_revision='2026-10-31-reborn-equip-v5',crystals=12345,
            shop=[dict(reward=[5,tid,1,1],cost=800,limit=2) for tid in (10101,10201)*3],purchases={'old':3})
        inventory=copy.deepcopy(role['attachments']);self.b.save(role)
        first=self.call(13);after=self.b.profile()
        self.assertEqual(after['activity']['abyss']['crystals'],12345)
        self.assertEqual(after['attachments'],inventory)
        self.assertEqual(after['activity']['abyss']['purchases'],{})
        self.assertTrue(all(not (1701<=p['attach_type']<=1726 or 10101<=p['attach_type']<=10219)
                            for p in first['shop_list'].values()))
        self.assertEqual(first,self.call(13))
        self.assertEqual(self.req(1329,id=12,data=summon.lua(dict(index=1,count=1,
            shop_day=first['shop_day'],shop_revision='2026-10-31-reborn-equip-v5')))[0][0],55)
        self.assertEqual(after,self.b.profile())

    def test_restart_preserves_purchases_and_day_refresh_resets(self):
        first=self.call(13);role=self.b.profile();role['activity']['abyss']['crystals']=10000;self.b.save(role)
        self.call(12,index=1,count=1);purchased=self.call(13)
        self.assertEqual(purchased['shop_list'][1]['buy_times'],first['shop_list'][1]['buy_times']-1)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(purchased,self.call(13))
        with patch('network_redirect.game_clock.now',return_value=NOW+86400):
            today=self.call(13)
            self.assertEqual(today['shop_day'],first['shop_day']+1)
            self.assertEqual(self.b.profile()['activity']['abyss']['purchases'],{})
            before=self.b.profile()
            self.assertEqual(self.req(1329,id=12,data=summon.lua(dict(index=1,count=1,
                shop_day=first['shop_day'],shop_revision=first['shop_revision'])))[0][0],55)
            self.assertEqual(before,self.b.profile())

    def test_v11_shelf_migrates_to_current_pool_and_new_portions(self):
        role=self.b.profile();s=role['activity']['abyss']
        old=[]
        for tid in (1329,1330,1331,1332,10000,1333):
            old.append(dict(reward=[5,tid,2,1],cost=800,limit=2,weight=10))
        s.update(shop_revision='2026-11-10-reborn-equip-v11',shop=old,
                 crystals=20000,purchases={'old':2})
        inventory=copy.deepcopy(role['attachments']);self.b.save(role)
        first=self.call(13);saved=self.b.profile();state=saved['activity']['abyss']
        self.assertEqual(state['crystals'],20000)
        self.assertEqual(saved['attachments'],inventory)
        self.assertEqual(state['purchases'],{})
        self.assertEqual(len({p['reward'][1] for p in state['shop']}),6)
        self.assertTrue(all(p in self.b.activity_rules['abyss_shop'] for p in state['shop']))
        self.assertEqual(first,self.call(13))
        self.assertEqual(self.req(1329,id=12,data=summon.lua(dict(index=1,count=1,
            shop_day=first['shop_day'],shop_revision='2026-11-10-reborn-equip-v11')))[0][0],55)
        self.assertEqual(saved,self.b.profile())

    def test_removed_casting_materials_migrate_without_losing_inventory(self):
        role=self.b.profile();s=role['activity']['abyss']
        summon.add_item(role,1334,5);summon.add_item(role,1335,7)
        old=copy.deepcopy(self.b.activity_rules['abyss_shop'][:6])
        old[-2]['reward']=[5,1334,1,1];old[-1]['reward']=[5,1335,1,1]
        revision='2026-11-13-rare-materials-v13'
        s.update(shop_revision=revision,shop=old,crystals=20000,purchases={'old':2})
        inventory=copy.deepcopy(role['attachments']);self.b.save(role)
        first=self.call(13);saved=self.b.profile();state=saved['activity']['abyss']
        self.assertEqual(saved['attachments'],inventory)
        self.assertEqual(state['crystals'],20000)
        self.assertEqual(state['purchases'],{})
        self.assertFalse({p['reward'][1] for p in state['shop']} & {1334,1335})
        self.assertEqual(first,self.call(13))
        self.assertEqual(self.req(1329,id=12,data=summon.lua(dict(index=1,count=1,
            shop_day=first['shop_day'],shop_revision=revision)))[0][0],55)
        self.assertEqual(saved,self.b.profile())

    def test_v17_fixed_shelf_migrates_to_all_random_without_losing_resources(self):
        role=self.b.profile();s=role['activity']['abyss']
        catalog={p['reward'][1]:copy.deepcopy(p) for p in self.b.activity_rules['abyss_shop']}
        old=[copy.deepcopy(catalog[tid]) for tid in (1310,1311,1312,1329,1330,1331)]
        for p in old[:3]:p.update(guaranteed=True,weight=24)
        revision='2026-11-13-butiantian-v17'
        s.update(shop=old,shop_revision=revision,crystals=12345,purchases={'old':2})
        inventory=copy.deepcopy(role['attachments']);self.b.save(role)
        first=self.call(13);saved=self.b.profile();current=saved['activity']['abyss']
        self.assertEqual(saved['attachments'],inventory)
        self.assertEqual(current['crystals'],12345)
        self.assertEqual(current['purchases'],{})
        self.assertTrue(all(not p['guaranteed'] and p==catalog[p['reward'][1]] for p in current['shop']))
        self.assertEqual(len({p['reward'][1] for p in current['shop']}),6)
        self.assertEqual(first,self.call(13))
        self.assertEqual(self.req(1329,id=12,data=summon.lua(dict(index=1,count=1,
            shop_day=first['shop_day'],shop_revision=revision)))[0][0],55)
        self.assertEqual(saved,self.b.profile())

    def test_v14_crystal_stone_removed_without_losing_owned_items(self):
        role=self.b.profile();s=role['activity']['abyss']
        summon.add_item(role,10000,777)
        old=copy.deepcopy(s['shop']);old[-1]=dict(reward=[5,10000,300,1],
            cost=1000,limit=5,weight=40,category='reborn',guaranteed=False)
        revision='2026-11-13-no-casting-v14'
        s.update(shop_revision=revision,shop=old,crystals=10000,purchases={'old':2})
        inventory=copy.deepcopy(role['attachments']);self.b.save(role)
        first=self.call(13);saved=self.b.profile();state=saved['activity']['abyss']
        self.assertEqual(saved['attachments'],inventory)
        self.assertEqual(state['crystals'],10000)
        self.assertEqual(state['purchases'],{})
        self.assertNotIn(10000,{p['reward'][1] for p in state['shop']})
        self.assertEqual(first,self.call(13))
        self.assertEqual(self.req(1329,id=12,data=summon.lua(dict(index=6,count=1,
            shop_day=first['shop_day'],shop_revision=revision)))[0][0],55)
        self.assertEqual(saved,self.b.profile())
