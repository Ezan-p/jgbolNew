"""Store clock regression: exercise real packets and daily stock settlement."""
import unittest
from unittest.mock import patch
from network_redirect import daily
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
        self.assertEqual(after['gold_coin'],before['gold_coin']-self.b.guild_rules['store_flush_gold'])
        self.assertEqual(after['union_store_flush_time'],before['union_store_flush_time'])
        self.assertGreater(after['union_store_flush_time'],NOW)
        self.assertNotEqual(before['guild']['store_stock'],after['guild']['store_stock'])
        self.assertEqual(self.b.respond(self.packet,{'authenticated':True}),self.replies)
        self.assertEqual(self.role(),after)
        self.assertEqual(self.ok(38)[-1][2]['flush_flag'],0)

    def test_midnight_restocks_once_and_advances_before_store_response(self):
        self.create();self.ok(36,count=100);self.ok(40,item_id=1,buy_count=5)
        before=self.role();deadline=before['union_store_flush_time']
        self.assertEqual(self.ok(38)[-1][2]['item_list'][1]['buy_times'],0)
        with patch('network_redirect.backend.time.time',return_value=deadline-1):
            self.assertEqual(self.ok(38)[-1][2]['item_list'][1]['buy_times'],0)
        with patch('network_redirect.backend.time.time',return_value=deadline):
            data=next(d for mid,op,d in self.ok(38) if mid==1301 and op==38);after=self.role()
            self.assertEqual(data['item_list'][1]['buy_times'],5)
            self.assertEqual(after['union_store_flush_time'],deadline+86400)
            self.assertEqual(after['gold_coin'],before['gold_coin'])
            self.assertNotEqual(after['guild']['store_stock'],before['guild']['store_stock'])
            self.assertEqual(after['guild']['day'],daily.day(deadline,self.b.guild_rules))
            self.ok(38);self.assertEqual(self.role(),after)
            mids=[decode(p)[0] for p in self.replies]
            self.assertLess(mids.index(1032),mids.index(1301))

    def test_failed_refresh_and_purchase_are_atomic(self):
        self.create()
        role=self.role();role['gold_coin']=0;role['cur_union_contrib']=0;self.b.save(role)
        before=self.role()
        self.assertEqual(self.req(39)[-1][1],55)
        self.assertEqual(self.role(),before)
        self.assertEqual(self.req(40,item_id=1,buy_count=1)[-1][1],55)
        self.assertEqual(self.role(),before)


if __name__=='__main__':unittest.main()
