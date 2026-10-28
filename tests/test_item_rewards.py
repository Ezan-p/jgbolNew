"""All inventory containers/fragments, real wire requests, disposable accounts."""
import copy
from collections import Counter
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from tests import test_equipment as original
from network_redirect import item_rewards as r, equipment_crafting as c, formation as f, summon
from network_redirect.backend import Backend


class ItemRewardTests(unittest.TestCase):
    setUp = original.EquipmentTests.setUp
    add = original.EquipmentTests.add
    get = original.EquipmentTests.get
    req = original.EquipmentTests.req

    def use(self, tid, ident, count=1, **kw):
        args = dict(item_type=tid, item_id=ident, item_count=count, des_type=1, des_id=0)
        args.update(kw)
        return self.req(1051, **args)

    def test_every_missing_container_real_wire_and_exact_fixed_contents(self):
        baseline = self.b.profile()
        rules = r.load_rules()
        for tid in sorted(r.HANDLED):
            with self.subTest(tid=tid):
                self.b.save(copy.deepcopy(baseline))
                ident = self.add(tid, count=3)
                events = self.use(tid, ident, 2)
                self.assertEqual(events[-1][0], 21, events)
                event = events[-1][1]
                self.assertEqual((event['type_id'], event['count'], self.get(ident)['count']), (tid, 2, 1))
                got = {(p['object_type'], p['attach_type'], p['attach_level']): p['attach_count']
                       for p in event['attach_list'].values()}
                rule = rules['items'][str(tid)]
                if rule['mode'] == 'fixed':
                    self.assertEqual(got, {(k,t,lv):n*2 for k,t,n,lv in rule['prizes']})
                else:
                    allowed = {(k,t,lv) for g in rules['pools'][rule['pool']] for k,t,n,lv in g['candidates']}
                    if rule['mode'] == 'fixed_random':
                        allowed.update((k,t,lv) for k,t,n,lv in rule['prizes'])
                        for k,t,n,lv in rule['prizes']:
                            self.assertGreaterEqual(got[k,t,lv], n*2)
                    self.assertTrue(set(got) <= allowed)
                for (kind, target, level), count in got.items():
                    profile = self.b.profile()
                    if kind in (5, 6):
                        inventory = [i for i in profile['attachments'] if i['attach_type']==kind and i['type_id']==target]
                        self.assertTrue(inventory, got)
                        if kind == 6 or f.ITEMS[target]['can_stack']=='0':
                            self.assertTrue(all(i.get('count') == (0 if kind==6 else 1) for i in inventory))
                before = self.b.profile()
                self.assertEqual(self.b.respond(self.packet, {'authenticated': True}), self.replies)
                self.assertEqual(before, self.b.profile())

    def test_market_qiankun_gifts_purchase_and_open_give_full_quantities(self):
        role = self.b.profile()
        role['gold_coin'] = 1000
        self.b.save(role)
        def amount(tid):
            return sum(i['count'] for i in self.b.profile()['attachments']
                       if i['attach_type'] == 5 and i['type_id'] == tid)
        goods = self.req(1057, first_send=1, page_id=2)[0][1]['rich_item_list'][204]
        self.assertEqual((goods['type_id'], goods['count'], goods['buy_price']), (1206, 1, 100))
        for purchase_count in (1, 2):
            before = amount(1206)
            gold = self.b.profile()['gold_coin']
            result = self.req(1057, first_send=0, page_id=2, index=204,
                              type_id=1206, count=purchase_count)[0][1]
            self.assertEqual(result['result'], 1)
            self.assertEqual(result['attach_list'][1]['attach_count'], purchase_count)
            self.assertEqual(amount(1206)-before, purchase_count)
            self.assertEqual(self.b.profile()['gold_coin'], gold-100*purchase_count)
            packet, replies = self.packet, self.replies
            self.assertEqual(self.b.respond(packet, {'authenticated': True}), replies)
            self.assertEqual(amount(1206)-before, purchase_count)
        gifts = [i for i in self.b.profile()['attachments'] if i['type_id'] == 1206]
        self.assertEqual(len(gifts), 3)
        for gift in gifts:
            self.assertEqual(gift['count'], 1)
            before = amount(1015)
            result = self.use(1206, gift['id'])[-1]
            self.assertEqual(result[0], 21)
            prize = result[1]['attach_list'][1]
            self.assertEqual((prize['attach_type'], prize['attach_count']), (1015, 100))
            self.assertEqual(amount(1015)-before, 100)
            packet, replies = self.packet, self.replies
            self.assertEqual(self.b.respond(packet, {'authenticated': True}), replies)
            self.assertEqual(amount(1015)-before, 100)
        self.assertEqual(amount(1206), 0)

    def test_seven_gifts_every_bonus_exact_fixed_inventory_and_replay(self):
        rules = r.load_rules()
        baseline = self.b.profile()
        for tid in (1247, 1084, 1085, 1086, 1098, 1099, 1205):
            rule = rules['items'][str(tid)]
            self.assertEqual(rule['mode'], 'fixed_random')
            for group in rules['pools'][rule['pool']]:
                for prize in group['candidates']:
                    with self.subTest(tid=tid, prize=prize):
                        self.b.save(copy.deepcopy(baseline))
                        ident = self.add(tid)
                        before = self.b.profile()
                        with patch.object(r, 'draw', return_value=prize) as draw:
                            event = self.use(tid, ident)[-1]
                        self.assertEqual(event[0], 21, event)
                        draw.assert_called_once()
                        expected = Counter()
                        for k,t,n,lv in rule['prizes'] + [prize]:
                            expected[k,t,lv] += n
                        got = {(p['object_type'],p['attach_type'],p['attach_level']):p['attach_count']
                               for p in event[1]['attach_list'].values()}
                        self.assertEqual(got, dict(expected))
                        after = self.b.profile()
                        self.assertFalse(any(x['id']==ident for x in after['attachments']))
                        for (kind,target,level),count in expected.items():
                            if kind in (11,12):
                                field = 'gold_coin' if kind==11 else 'silver_coin'
                                self.assertEqual(after[field]-before[field],count)
                            else:
                                def amount(role):
                                    return sum(x['count'] for x in role['attachments']
                                               if (x['attach_type'],x['type_id'],x.get('level',1))
                                               ==(kind,target,level))
                                self.assertEqual(amount(after)-amount(before),count)
                                if target in (1090,1091,1092):
                                    stones = [x for x in after['attachments']
                                              if x['type_id']==target and x.get('level',1)==level]
                                    self.assertTrue(all(x['count']==1 for x in stones))
                        # Acquiring a gold card does not redeem it or recharge.
                        self.assertEqual(after.get('vip_level'),before.get('vip_level'))
                        self.assertEqual(after.get('charge_gold'),before.get('charge_gold'))
                        self.assertEqual(after.get('recharge'),before.get('recharge'))
                        self.assertEqual(self.b.respond(self.packet, {'authenticated':True}),self.replies)
                        self.assertEqual(after,self.b.profile())

    def test_seven_gifts_batch_draws_and_same_level_stone_merge(self):
        ident = self.add(1247,count=3)
        with patch.object(r,'draw',side_effect=[[11,1,400,1],[5,1156,2,1],[11,1,500,1]]) as draw:
            event = self.use(1247,ident,3)[-1]
        self.assertEqual(event[0],21,event)
        self.assertEqual(draw.call_count,3)
        got = {(p['object_type'],p['attach_type'],p['attach_level']):p['attach_count']
               for p in event[1]['attach_list'].values()}
        self.assertEqual(got,{(12,1,1):300000,(5,1001,1):300,(11,1,1):900,(5,1156,1):2})
        ident = self.add(1205,count=2)
        with patch.object(r,'draw',side_effect=[[5,1090,1,1],[5,1090,1,4]]):
            event = self.use(1205,ident,2)[-1]
        got = {(p['attach_type'],p['attach_level']):p['attach_count']
               for p in event[1]['attach_list'].values()}
        self.assertEqual(got,{(1090,1):3,(1090,4):1,(1091,1):2,(1092,1):2})

    def test_seven_gifts_allowlist_and_level_scope(self):
        for source,target in ((1085,1249),(1086,1031),(1086,1032),(1086,1033),(1086,1034)):
            r.valid_prize([5,target,1,1],source)
        for source,target,level in ((1084,1032,1),(1085,1085,1),(1086,1247,1),
                                    (1081,1249,1),(1205,1090,5),(1085,1090,2),(1205,1001,2)):
            with self.assertRaises(ValueError):
                r.valid_prize([5,target,1,level],source)
        # Sharing a whitelisted pool must not grant that permission to other gifts.
        rules = r.load_rules()
        rules['items']['1081'] = dict(mode='random',pool='seasonal_1085',reason='test')
        with patch.object(r.json,'loads',return_value=rules), self.assertRaises(ValueError):
            r.load_rules()

    def test_seven_gifts_currency_overflow_and_encoding_failure_are_atomic(self):
        ident = self.add(1247)
        role = self.b.profile(); role['gold_coin']=2147483647; self.b.save(role)
        before = self.b.profile()
        with patch.object(r,'draw',return_value=[11,1,400,1]):
            self.assertEqual(self.use(1247,ident)[-1][0],55)
        self.assertEqual(before,self.b.profile())
        role['gold_coin']=1000; self.b.save(role)
        before = self.b.profile()
        with patch.object(r,'draw',return_value=[5,1152,1,1]), \
                patch.object(self.b,'inventory',side_effect=ValueError('wire failure')):
            self.assertEqual(self.use(1247,ident)[-1][0],55)
        self.assertEqual(before,self.b.profile())

    def test_all_weight_tickets_exact_and_all_candidates_reachable(self):
        # Exhausting integer tickets verifies precise mass and both ends of every interval.
        for name, groups in r.load_rules()['pools'].items():
            weights = {i:g['weight'] for i,g in enumerate(groups)}
            counts = Counter()
            with patch.object(summon.secrets, 'randbelow', side_effect=range(sum(weights.values()))):
                for _ in range(sum(weights.values())):
                    counts[summon.weighted_choice(weights)] += 1
            self.assertEqual(dict(counts), weights, name)
            for idx, group in enumerate(groups):
                for prize in group['candidates']:
                    with patch.object(summon, 'weighted_choice', return_value=idx), patch.object(r.secrets, 'choice', return_value=prize):
                        self.assertEqual(r.draw(groups), prize)

    def test_every_special_container_keeps_native_route(self):
        baseline=self.b.profile();baseline['vip_level']=10
        for tid in sorted(r.SPECIAL):
            with self.subTest(tid=tid):
                self.b.save(copy.deepcopy(baseline))
                count=30 if tid==1249 else 1
                ident=self.add(tid,count=count*2)
                target=dict(des_type=5,des_id=5001) if tid==1249 else (
                    dict(des_type=10,des_id=5053) if tid in (1367,1368) else {})
                events=self.use(tid,ident,count,**target)
                result=next((d for e,d in events if e==21),None)
                self.assertIsNotNone(result,events)
                self.assertEqual(self.get(ident)['count'],count)
                self.assertEqual(result['result'],1)

    def test_choice_box_consumes_only_selected_stack(self):
        first=self.add(1249,count=60);second=self.add(1249,count=30)
        event=self.use(1249,second,30,des_type=5,des_id=5001)[-1]
        self.assertEqual(event[0],21)
        self.assertEqual(self.get(first)['count'],60)
        self.assertFalse(any(i['id']==second for i in self.b.profile()['attachments']))
        small=self.add(1249,count=1);before=self.b.profile()
        self.assertEqual(self.use(1249,small,30,des_type=5,des_id=5001)[-1][0],55)
        self.assertEqual(before,self.b.profile())

    def test_vip_gift_equipment_instances_are_independent(self):
        role=self.b.profile();role['vip_level']=10;self.b.save(role)
        ident=self.add(1110,count=2)
        self.assertEqual(self.use(1110,ident,2)[-1][0],21)
        for tid in (2008,3002,4004):
            items=[i for i in self.b.profile()['attachments'] if i['type_id']==tid and i['attach_type']==5]
            self.assertEqual(len(items),2)
            self.assertTrue(all(i['count']==1 for i in items))

    def test_batch_independent_draws_and_typed_skill_prizes(self):
        ident = self.add(1240, count=15)
        with patch.object(r, 'draw', side_effect=[[6,51,1,1],[6,52,1,1]]*7+[[6,51,1,1]]) as choose:
            event = self.use(1240, ident, 15)[-1]
        self.assertEqual(event[0], 21)
        self.assertEqual(choose.call_count, 15)
        self.assertEqual({p['attach_type']:p['attach_count'] for p in event[1]['attach_list'].values()}, {51:8,52:7})

    def test_pool_semantic_constraints(self):
        rules = r.load_rules()
        for tid in (1326,1328):
            actual = {p[1] for g in rules['pools'][str(tid)] for p in g['candidates']}
            rows = summon.rows('item_receive_config.csv')
            excluded = {p[1] for row in (rows if tid==1326 else rows[-1:]) for p in c.parts(row['attach_data']) if p[0]==5}
            expected = {t for t,row in f.ITEMS.items() if row['quality']=='5' and row['main_type'] in ('1','2')} - excluded
            self.assertEqual(actual, expected)
            self.assertTrue(actual)
        self.assertEqual(rules['items']['1806']['prizes'], [[5,5001,1,1]])
        from network_redirect import qiankun_bags as bags
        for tid in ('1032','1033','1034'):
            targets = {target for tier in bags.load_rules()['bags'][tid]['tiers'].values()
                       for g in tier['groups'] for kind,target in bags.CATALOG[g['pool']] if kind==5}
            expected_books = {t for kind,t in bags.CATALOG['manual']}
            if tid != '1034':
                expected_books |= {t for kind,t in bags.CATALOG['manual_advanced']}
            self.assertEqual(targets & f.EXPERIENCE_BOOKS, expected_books)
        from network_redirect import activity_hunt
        self.assertTrue(set(activity_hunt.load_rules()['upgrade_box_pool']) <= {1310,1311,1312,1313,1314,1320,1321,1322,1323})

    def test_wrong_source_lock_target_quantity_and_level_atomic(self):
        ident = self.add(1326, count=16)
        for changes in ({'item_count':0}, {'item_count':17}, {'item_count':16}, {'item_type':1328},
                        {'item_id':99999999}, {'des_type':4}, {'des_id':9999}):
            before = self.b.profile()
            args=dict(item_type=1326,item_id=ident,item_count=1,des_type=1,des_id=0);args.update(changes)
            self.assertEqual(self.req(1051, **args)[-1][0], 55)
            self.assertEqual(before, self.b.profile())
        for field in ('is_lock','owner_id','equip_pos','equip_order','level'):
            value = 2 if field=='level' else 1
            bad = self.add(1326, **{field:value})
            before = self.b.profile()
            self.assertEqual(self.use(1326,bad)[-1][0],55)
            self.assertEqual(before,self.b.profile())

    def test_currency_overflow_and_encoding_failure_rollback(self):
        ident=self.add(1081)
        role=self.b.profile();role['silver_coin']=2147483647;self.b.save(role)
        before=self.b.profile()
        self.assertEqual(self.use(1081,ident)[-1][0],55)
        self.assertEqual(before,self.b.profile())
        role=self.b.profile();role['silver_coin']=1000;self.b.save(role)
        before=self.b.profile()
        with patch.object(self.b,'inventory',side_effect=ValueError('wire failure')):
            self.assertEqual(self.use(1081,ident)[-1][0],55)
        self.assertEqual(before,self.b.profile())

    def test_selected_stack_exhaustion_and_restart(self):
        first=self.add(1327,count=4);second=self.add(1327,count=2)
        self.assertEqual(self.use(1327,second,2)[-1][0],21)
        self.assertEqual(self.get(first)['count'],4)
        self.assertFalse(any(i['id']==second for i in self.b.profile()['attachments']))
        before=self.b.profile();self.b.close()
        self.b=Backend(Path(self.tmp.name),18770,lambda *a,**kw:None)
        self.assertEqual(before,self.b.profile())

    def test_every_fragment_recipe_real_wire(self):
        fragments={t for t,row in r.NAMES.items() if '碎片' in row['name']}
        checked=set();baseline=self.b.profile()
        for row in c.RECIPES:
            for kind,tid,level,count in c.parts(row[c.SRC]):
                if kind!=5 or tid not in fragments:continue
                with self.subTest(tid=tid):
                    self.b.save(copy.deepcopy(baseline))
                    ident=self.add(tid,count=count*2,level=level)
                    before=self.b.profile()
                    event=self.req(1074,flag=2,num=2,des_type=1,count=1,id_list=[dict(id=ident)])[-1]
                    self.assertEqual(event[0],116,event)
                    self.assertFalse(any(i['id']==ident for i in self.b.profile()['attachments']))
                    dest=r.recipe_destinations(row,tid)
                    allowed={p[:3] for p in dest}
                    got=event[1]['item_list'].values()
                    self.assertTrue(all((p['object_type'],p['attach_type'],p['attach_level']) in allowed for p in got))
                    self.assertEqual(sum(p['attach_count'] for p in event[1]['item_list'].values()),2)
                    self.assertEqual(before['silver_coin']-self.b.profile()['silver_coin'],2*sum(p[3] for p in c.parts(row[c.COST]) if p[0]==12))
                    checked.add(tid)
        self.assertEqual(checked,fragments)

    def test_every_random_fragment_weight_and_output(self):
        baseline=self.b.profile()
        for row in c.RECIPES:
            src=c.parts(row[c.SRC])[0]
            if '碎片' not in r.NAMES.get(src[1],{}).get('name','') or row['is_random']!='1':continue
            dest=r.recipe_destinations(row,src[1])
            weights={i:p[4] for i,p in enumerate(dest)}
            counts=Counter()
            with patch.object(summon.secrets,'randbelow',side_effect=range(sum(weights.values()))):
                for _ in range(sum(weights.values())):counts[summon.weighted_choice(weights)]+=1
            self.assertEqual(dict(counts),weights)
            for i,prize in enumerate(dest):
                self.b.save(copy.deepcopy(baseline));ident=self.add(src[1],count=src[3])
                with patch.object(summon,'weighted_choice',return_value=i):
                    event=self.req(1074,flag=2,num=1,des_type=1,count=1,id_list=[dict(id=ident)])[-1]
                self.assertEqual(event[0],116)
                got=event[1]['item_list'][1]
                self.assertEqual((got['object_type'],got['attach_type'],got['attach_level'],got['attach_count']),prize[:4])

    def test_passive_fragment_native_1053_and_query_98(self):
        entries=self.req(1055,flag=1)[0][1].values()
        self.assertIn(dict(compose_quality=5,compose_maintype=4,material_count=40),entries)
        ident=self.add(6005,count=40)
        event=self.req(1053,compose_type=1,equip_type=4,equip_quality=5,material_quality=5,
                       material_count=1,material_list=[dict(id=ident)])[-1]
        self.assertEqual(event[0],6,event)
        self.assertEqual((event[1]['object_type'],event[1]['count']),(6,1))
        self.assertEqual(event[1]['attach_list'][1]['object_type'],6)

    def test_fragment_override_is_narrow_and_keeps_original_evidence(self):
        row,src=c.recipe_for(dict(attach_type=5,type_id=10001,level=1),2)
        original=c.parts(row[c.DEST]);effective=r.recipe_destinations(row,10001)
        self.assertEqual(sum(p[4] for p in effective),1550)
        self.assertEqual([p[1] for p in effective],list(range(10201,10220)))
        self.assertEqual(sum(a!=b for a,b in zip(original,effective)),1)
        self.assertEqual(sum(p[1]==10204 for p in original),2)

    def test_fragments_invalid_inputs_fail_without_consumption(self):
        ident=self.add(10001,count=40)
        for changes in ({'num':3},{'num':0},{'des_type':10203},
                        {'count':2,'id_list':[dict(id=ident),dict(id=ident)]}):
            args=dict(flag=2,num=1,des_type=1,count=1,id_list=[dict(id=ident)]);args.update(changes)
            before=self.b.profile()
            self.assertEqual(self.req(1074,**args)[-1][0],55)
            self.assertEqual(before,self.b.profile())
        for field,value in (('silver_coin',0),('level',4)):
            before=self.b.profile();changed=copy.deepcopy(before);changed[field]=value;self.b.save(changed)
            state=self.b.profile()
            self.assertEqual(self.req(1074,flag=2,num=1,des_type=1,count=1,id_list=[dict(id=ident)])[-1][0],55)
            self.assertEqual(state,self.b.profile());self.b.save(before)

    def test_bad_config_fails_closed(self):
        rules=r.load_rules()
        variants=[]
        bad=copy.deepcopy(rules);del bad['items']['1326'];variants.append(bad)
        bad=copy.deepcopy(rules);bad['pools']['1326'][0]['weight']=0;variants.append(bad)
        bad=copy.deepcopy(rules);bad['pools']['1326'][0]['candidates']=[[5,1326,1,1]];variants.append(bad)
        for bad in variants:
            with patch.object(Path,'read_text',return_value=json.dumps(bad)),self.assertRaises(f.Rejected):r.load_rules()


if __name__=='__main__':
    unittest.main()
