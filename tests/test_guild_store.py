"""Store clock regression: exercise real packets and daily stock settlement."""
import copy
from collections import Counter
import json
import unittest
from unittest.mock import patch
from network_redirect import daily, guild, guild_offline
from network_redirect.backend import Backend
from pathlib import Path
from network_redirect.protocol import decode
from tests import test_guild as base
NOW=base.NOW


class GuildStoreTests(unittest.TestCase):
    setUp = base.GuildTests.setUp
    req = base.GuildTests.req
    role = base.GuildTests.role
    create = base.GuildTests.create
    ok = base.GuildTests.ok

    def test_open_repairs_legacy_clock_and_does_not_reroll(self):
        self.create()
        role=self.role();role['union_store_flush_time']=0;self.b.save(role)
        first=self.ok(38)[-1][2]
        attrs=next(d['attr_list'] for mid,_,d in map(decode,self.replies) if mid==1032)
        deadline=next(v['value'] for v in attrs if v['type']==147)
        self.assertGreater(deadline,NOW)
        self.assertLessEqual(deadline,NOW+86400)
        self.assertEqual(type(first['flush_flag']),int)
        self.assertEqual(first['flush_flag'],0)
        before=self.role()
        for _ in range(4):self.assertEqual(self.ok(38)[-1][2],first)
        self.assertEqual(self.role(),before)

    def test_paid_refresh_keeps_future_clock_and_charges_once(self):
        self.create();self.ok(38)
        before=self.role()
        result=self.ok(39)[-1][2]
        after=self.role()
        self.assertEqual(result['flush_flag'],1)
        self.assertEqual(result['flush_cost'],100)
        self.assertEqual(after['gold_coin'],before['gold_coin']-100)
        self.assertEqual(after['union_store_flush_time'],before['union_store_flush_time'])
        self.assertGreater(after['union_store_flush_time'],NOW)
        self.assertNotEqual(before['guild']['store_stock'],after['guild']['store_stock'])
        self.assertEqual(self.b.respond(self.packet,{'authenticated':True}),self.replies)
        self.assertEqual(self.role(),after)
        self.assertEqual(self.ok(38)[-1][2]['flush_flag'],0)

    def test_midnight_restocks_once_and_advances_before_store_response(self):
        self.create();self.ok(36,count=100)
        row=next(iter(self.ok(38)[-1][2]['item_list'].values()))
        role=self.role();role['cur_union_contrib']=row['cost_contrib']*row['buy_times'];self.b.save(role)
        self.ok(40,item_id=row['id'],buy_count=row['buy_times'])
        before=self.role();deadline=before['union_store_flush_time']
        self.assertEqual(self.ok(38)[-1][2]['item_list'][row['id']]['buy_times'],0)
        with patch('network_redirect.game_clock.now',return_value=deadline-1):
            self.assertEqual(self.ok(38)[-1][2]['item_list'][row['id']]['buy_times'],0)
        with patch('network_redirect.game_clock.now',return_value=deadline):
            data=next(d for mid,op,d in self.ok(38) if mid==1301 and op==38);after=self.role()
            self.assertEqual(after['guild']['purchases'],{})
            for item in after['guild']['store_stock']:
                self.assertEqual(data['item_list'][item['id']]['buy_times'],item['limit'])
            self.assertEqual(after['union_store_flush_time'],deadline+86400)
            self.assertEqual(after['gold_coin'],before['gold_coin'])
            self.assertNotEqual(after['guild']['store_stock'],before['guild']['store_stock'])
            self.assertEqual(after['guild']['day'],daily.day(deadline,self.b.guild_rules))
            self.ok(38);self.assertEqual(self.role(),after)
            mids=[decode(p)[0] for p in self.replies]
            self.assertLess(mids.index(1032),mids.index(1301))

    def test_pool_sample_is_exact_unique_and_persistent(self):
        self.create()
        expected_offers={
            (5,1001,100,1):(100,5), (5,1015,20,1):(100,5),
            (5,1022,5,1):(200,2), (5,1023,5,1):(200,2),
            (5,1006,5,1):(200,2), (5,1007,5,1):(300,2),
            (12,0,100000,1):(100,5), (12,0,500000,1):(200,5),
            (5,1034,5,1):(50,2), (5,1033,5,1):(100,2),
            (5,1032,5,1):(100,2), (5,1031,5,1):(300,2),
            (5,1327,1,1):(200,3), (5,1346,1,1):(200,1),
            (5,1206,1,1):(100,1), (5,1343,1,1):(100,10),
        }
        expected=set(expected_offers)
        self.assertEqual({tuple(x['prize']):(x['cost'],x['limit'])
                          for x in self.b.guild_rules['store']},expected_offers)
        seen=set();selections=set()
        for day in range(100):
            state={'day':day}
            stock=guild_offline.store(state,self.b.guild_rules)
            prizes={tuple(x['prize']) for x in stock}
            self.assertEqual(len(stock),8);self.assertEqual(len(prizes),8)
            self.assertTrue(prizes<=expected)
            self.assertEqual([x['id'] for x in stock],list(range(1,9)))
            saved=copy.deepcopy(state)
            self.assertEqual(guild_offline.store(state,self.b.guild_rules),stock)
            self.assertEqual(state,saved)
            seen.update(prizes);selections.add(frozenset(prizes))
        self.assertEqual(seen,expected);self.assertGreater(len(selections),1)
        first=self.ok(38)[-1][2]
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.ok(38)[-1][2],first)

    def test_refresh_uses_exact_weights_without_replacement(self):
        rules=self.b.guild_rules
        weights={tuple(row['prize']):row['weight'] for row in rules['store']}
        for prize,weight in weights.items():
            self.assertEqual(weight,1 if prize[:2] in ((5,1007),(5,1031),(5,1343)) else 5)
        first_counts=Counter()
        original=copy.deepcopy(rules)
        for ticket in range(sum(weights.values())):
            state={}
            with patch.object(guild_offline,'roll',side_effect=[ticket]+[0]*7) as rng:
                guild_offline.refresh_store(state,rules)
            stock=state['store_stock']
            first_counts[tuple(stock[0]['prize'])]+=1
            remaining=dict(weights)
            self.assertEqual(len(stock),8)
            for row,call in zip(stock,rng.call_args_list):
                self.assertEqual(call.args[1],sum(remaining.values()))
                remaining.pop(tuple(row['prize']))
            with patch.object(guild_offline,'roll',side_effect=AssertionError('saved stock rerolled')):
                self.assertEqual(guild_offline.store(state,rules),stock)
        self.assertEqual(dict(first_counts),weights)
        self.assertEqual(rules,original)

    def test_invalid_refresh_weights_rejected_and_legacy_config_supported(self):
        path=Path(self.tmp.name)/'guild_rules.json'
        original=guild.load_rules()
        for value in (0,-1,True,1.5,'1',100001):
            rules=copy.deepcopy(original)
            rules['store'][0]['weight']=value
            path.write_text(json.dumps(rules))
            with self.subTest(weight=value),self.assertRaises(guild.formation.Rejected):
                guild.load_rules(path)
        rules=copy.deepcopy(original)
        for row in rules['store']:row.pop('weight')
        path.write_text(json.dumps(rules))
        guild.load_rules(path)
        with patch.object(guild_offline,'roll',return_value=0) as rng:
            state={};guild_offline.refresh_store(state,rules)
        self.assertEqual([call.args[1] for call in rng.call_args_list],list(range(16,8,-1)))

    def test_legacy_stock_migrates_once_without_resetting_spent_quota(self):
        self.create()
        role=self.role();state=role['guild']
        state['store_stock']=[dict(id=i,prize=[5,1003,5,1],cost=20,limit=5) for i in range(1,7)]
        state.pop('store_pool_version',None)
        state['purchases']={'1':1};state['flushes']=2
        self.b.save(role)
        first=self.ok(38)[-1][2]
        after=self.role()
        self.assertEqual(len(first['item_list']),8)
        self.assertNotIn(1003,[x['item']['attach_type'] for x in first['item_list'].values()])
        self.assertEqual(after['guild']['purchases'],{'1':1})
        self.assertEqual(after['guild']['flushes'],2)
        self.assertEqual(after['gold_coin'],role['gold_coin'])
        self.assertEqual(self.ok(38)[-1][2],first)
        self.assertEqual(self.role(),after)

    def test_every_candidate_grants_advertised_quantity(self):
        self.create()
        for candidate in self.b.guild_rules['store']:
            with self.subTest(prize=candidate['prize']):
                role=self.role();role['cur_union_contrib']=10000
                stock=copy.deepcopy(self.b.guild_rules['store'][:8]);stock[7]=copy.deepcopy(candidate)
                for i,row in enumerate(stock,1):row['id']=i
                role['guild'].update(store_stock=stock,store_pool_version=self.b.guild_rules['store_pool_version'],purchases={})
                self.b.save(role)
                kind,tid,count,_=candidate['prize']
                def amount(r):
                    if kind==12:return r['silver_coin']
                    return sum(x['count'] for x in r['attachments'] if x['attach_type']==5 and x['type_id']==tid)
                offer=self.ok(38)[-1][2]['item_list'][8]
                self.assertEqual(offer['item'],daily.spec(candidate['prize']))
                if tid in (1007,1031,1032,1033,1034):
                    self.assertEqual(offer['buy_times'],2)
                self.ok(40,item_id=8,buy_count=candidate['limit'])
                after=self.role()
                self.assertEqual(amount(after)-amount(role),count*candidate['limit'])
                self.assertEqual(after['cur_union_contrib'],10000-candidate['cost']*candidate['limit'])
                self.assertEqual(self.req(40,item_id=8,buy_count=1)[-1][1],55)
                self.assertEqual(self.role(),after)

    def test_previous_eight_slot_pool_migrates_once(self):
        self.create()
        role=self.role();state=role['guild']
        state.update(store_pool_version=1,flushes=3,purchases={'1':2,'8':5},
                     store_stock=[dict(id=i,prize=[5,1310,5,1],cost=20,limit=5)
                                  for i in range(1,9)])
        self.b.save(role)
        first=self.ok(38)[-1][2];after=self.role()
        expected={tuple(row['prize']) for row in self.b.guild_rules['store']}
        self.assertEqual(after['guild']['store_pool_version'],2)
        self.assertTrue(all(tuple(row['prize']) in expected for row in after['guild']['store_stock']))
        self.assertEqual(after['guild']['purchases'],state['purchases'])
        self.assertEqual(after['guild']['flushes'],3)
        self.assertEqual(after['gold_coin'],role['gold_coin'])
        for row in after['guild']['store_stock']:
            self.assertEqual(first['item_list'][row['id']]['buy_times'],
                             max(0,row['limit']-state['purchases'].get(str(row['id']),0)))
        self.assertEqual(self.ok(38)[-1][2],first)
        self.assertEqual(self.role(),after)

    def test_silver_tiers_have_independent_limits_and_purchases(self):
        self.create()
        rules=self.b.guild_rules
        silver=[row for row in rules['store'] if row['prize'][0]==12]
        # Different limits expose accidental matching by currency type alone.
        silver[0]['limit']=2;silver[1]['limit']=3
        stock=copy.deepcopy(silver+rules['store'][:6])
        for slot,row in enumerate(stock,1):
            row['id']=slot;row['limit']=9;row['cost']=500
        role=self.role();role['cur_union_contrib']=10000
        role['guild'].update(store_stock=stock,store_pool_version=rules['store_pool_version'],purchases={})
        self.b.save(role)
        offers=self.ok(38)[-1][2]['item_list']
        self.assertEqual([offers[i]['buy_times'] for i in (1,2)],[2,3])
        self.assertEqual([offers[i]['cost_contrib'] for i in (1,2)],[100,200])
        self.ok(40,item_id=1,buy_count=2)
        self.assertEqual(self.ok(38)[-1][2]['item_list'][2]['buy_times'],3)
        self.ok(40,item_id=2,buy_count=3)
        after=self.role()
        self.assertEqual(after['silver_coin']-role['silver_coin'],1700000)
        self.assertEqual(after['cur_union_contrib'],9200)
        for slot in (1,2):
            self.assertEqual(self.req(40,item_id=slot,buy_count=1)[-1][1],55)
            self.assertEqual(self.role(),after)

    def test_duplicate_reward_tier_is_rejected(self):
        rules=guild.load_rules()
        rules['store'][-1]['prize']=list(rules['store'][0]['prize'])
        path=Path(self.tmp.name)/'guild_rules.json'
        path.write_text(json.dumps(rules))
        with self.assertRaises(guild.formation.Rejected):guild.load_rules(path)

    def test_saved_prices_and_limits_update_without_reroll_or_quota_reset(self):
        self.create()
        role=self.role();role['cur_union_contrib']=10000
        targets=(1007,1031,1032,1033,1034)
        stock=copy.deepcopy([x for x in self.b.guild_rules['store'] if x['prize'][1] in targets]
                            +self.b.guild_rules['store'][:3])
        for i,row in enumerate(stock,1):
            row['id']=i
            row['cost']=500
            if row['prize'][1] in targets:
                row['limit']=1 if row['prize'][1]==1007 else 5
        spent={'1':1,'2':1,'3':2,'4':3,'5':5}
        role['guild'].update(store_stock=stock,store_pool_version=self.b.guild_rules['store_pool_version'],purchases=spent,flushes=2)
        self.b.save(role)
        # Buying directly must use the new price/limit before opening the shop.
        self.ok(40,item_id=1,buy_count=1)
        data=self.ok(38)[-1][2];after=self.role()
        self.assertEqual([data['item_list'][i]['buy_times'] for i in range(1,6)],[0,1,0,0,0])
        self.assertEqual([x['prize'] for x in after['guild']['store_stock']],[x['prize'] for x in stock])
        self.assertEqual(after['guild']['purchases'],dict(spent,**{'1':2}))
        self.assertEqual(after['guild']['flushes'],2)
        self.assertEqual(after['gold_coin'],role['gold_coin'])
        self.assertEqual(after['cur_union_contrib'],9700)
        expected={tuple(row['prize']):row['cost'] for row in self.b.guild_rules['store']}
        for row in stock:
            self.assertEqual(data['item_list'][row['id']]['cost_contrib'],expected[tuple(row['prize'])])
        for slot in (1,3,4,5):
            self.assertEqual(self.req(40,item_id=slot,buy_count=1)[-1][1],55)
            self.assertEqual(self.role(),after)
        self.assertEqual(self.ok(38)[-1][2],data)

    def test_failed_refresh_and_purchase_are_atomic(self):
        self.create()
        role=self.role();role['gold_coin']=99;role['cur_union_contrib']=0;self.b.save(role)
        before=self.role()
        self.assertEqual(self.req(39)[-1][1],55)
        self.assertEqual(self.role(),before)
        self.assertEqual(self.req(40,item_id=1,buy_count=1)[-1][1],55)
        self.assertEqual(self.role(),before)


if __name__=='__main__':unittest.main()
