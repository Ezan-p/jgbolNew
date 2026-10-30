"""Store clock regression: exercise real packets and daily stock settlement."""
import copy
import unittest
from unittest.mock import patch
from network_redirect import daily, guild_offline
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
        row=next(x for x in self.ok(38)[-1][2]['item_list'].values() if x['cost_contrib']==20)
        self.ok(40,item_id=row['id'],buy_count=row['buy_times'])
        before=self.role();deadline=before['union_store_flush_time']
        self.assertEqual(self.ok(38)[-1][2]['item_list'][row['id']]['buy_times'],0)
        with patch('network_redirect.backend.time.time',return_value=deadline-1):
            self.assertEqual(self.ok(38)[-1][2]['item_list'][row['id']]['buy_times'],0)
        with patch('network_redirect.backend.time.time',return_value=deadline):
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
        expected={(5,tid,20 if tid==1001 else 5,1) for tid in
                  (1001,1022,1023,1006,1007,1034,1033,1032,1031,10000,1310,1311,1312)}
        expected.add((12,0,5,1))
        expected.add((5,1015,20,1))
        self.assertEqual({tuple(x['prize']) for x in self.b.guild_rules['store']},expected)
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
                role['guild'].update(store_stock=stock,store_pool_version=1,purchases={})
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

    def test_saved_limits_update_without_reroll_or_quota_reset(self):
        self.create()
        role=self.role();role['cur_union_contrib']=10000
        targets=(1007,1031,1032,1033,1034)
        stock=copy.deepcopy([x for x in self.b.guild_rules['store'] if x['prize'][1] in targets]
                            +self.b.guild_rules['store'][:3])
        for i,row in enumerate(stock,1):
            row['id']=i
            if row['prize'][1] in targets:
                row['limit']=1 if row['prize'][1]==1007 else 5
        spent={'1':1,'2':1,'3':2,'4':3,'5':5}
        role['guild'].update(store_stock=stock,store_pool_version=1,purchases=spent,flushes=2)
        self.b.save(role)
        # Buying directly must use the new limit even before opening the shop.
        self.ok(40,item_id=1,buy_count=1)
        data=self.ok(38)[-1][2];after=self.role()
        self.assertEqual([data['item_list'][i]['buy_times'] for i in range(1,6)],[0,1,0,0,0])
        self.assertEqual([x['prize'] for x in after['guild']['store_stock']],[x['prize'] for x in stock])
        self.assertEqual(after['guild']['purchases'],dict(spent,**{'1':2}))
        self.assertEqual(after['guild']['flushes'],2)
        self.assertEqual(after['gold_coin'],role['gold_coin'])
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
