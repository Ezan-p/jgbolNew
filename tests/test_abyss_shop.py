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
                         {10000,
                          1329,1330,1331,1332,1310,1311,1312,1333,1334,1335})
        changes=[lambda r:r['abyss_shop'][0]['reward'].__setitem__(1,1001),
                 lambda r:r['abyss_shop'][0]['reward'].__setitem__(1,1701),
                 lambda r:r['abyss_shop'][0]['reward'].__setitem__(1,10101),
                 lambda r:r['abyss_shop'][0]['reward'].__setitem__(1,10201),
                 lambda r:r['abyss_shop'][0].__setitem__('weight',0),
                 lambda r:r['abyss_shop'][0].__setitem__('weight',True),
                 lambda r:r['abyss_shop'][0].__setitem__('category','other'),
                 lambda r:r['abyss_shop'].pop(),
                 lambda r:r['abyss_shop'].append(copy.deepcopy(r['abyss_shop'][0])),
                 lambda r:r['abyss_shop_category_slots'].__setitem__('reborn',2)]
        path=Path(self.tmp.name)/'invalid.json'
        for change in changes:
            r=copy.deepcopy(rules);change(r);path.write_text(json.dumps(r))
            with self.assertRaises(ValueError):activity.load_rules(path)

    def test_daily_probabilities_match_three_weighted_draws(self):
        rules=self.b.activity_rules;counts=Counter();trials=12000
        for role_id in range(trials):
            offers=abyss.refresh_shop({},dict(role_id=role_id),rules,12345)
            self.assertEqual(Counter(p['category'] for p in offers),dict(reborn=3,apotheosis=3))
            self.assertEqual(len({p['reward'][1] for p in offers}),6)
            counts.update(p['reward'][1] for p in offers)
        for p in rules['abyss_shop']:
            pool=[q for q in rules['abyss_shop'] if q['category']==p['category']]
            total=sum(q['weight'] for q in pool);expected=0
            for order in permutations(pool,3):
                if p not in order:continue
                chance=1;remaining=total
                for q in order:
                    chance*=q['weight']/remaining;remaining-=q['weight']
                expected+=chance
            self.assertAlmostEqual(counts[p['reward'][1]]/trials,expected,delta=.018)

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
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            today=self.call(13)
            self.assertEqual(today['shop_day'],first['shop_day']+1)
            self.assertEqual(self.b.profile()['activity']['abyss']['purchases'],{})
            before=self.b.profile()
            self.assertEqual(self.req(1329,id=12,data=summon.lua(dict(index=1,count=1,
                shop_day=first['shop_day'],shop_revision=first['shop_revision'])))[0][0],55)
            self.assertEqual(before,self.b.profile())
