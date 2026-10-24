import copy
import tempfile
import unittest
import struct
from datetime import datetime, timezone, timedelta
from pathlib import Path
from unittest.mock import patch
from network_redirect import xianling, summon
from network_redirect.backend import Backend,login_fields
from network_redirect.protocol import encode,decode

NOW=int(datetime(2026,10,24,12,tzinfo=timezone(timedelta(hours=8))).timestamp())
class XianlingTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.b=Backend(Path(self.tmp.name),18790,lambda *a,**k:None);self.addCleanup(lambda:self.b.close())
        self.serial=1000
        c=patch('network_redirect.backend.time.time',return_value=NOW);c.start();self.addCleanup(c.stop)
    def req(self,flag=4,index=0,count=0,mid=1336,**kw):
        self.serial+=1
        self.packet=encode(mid,dict(serial_num=self.serial,flag=flag,index=index,count=count,**kw))
        self.replies=self.b.respond(self.packet,dict(authenticated=True))
        self.assertEqual(decode(self.replies[-1])[0],1106)
        return [(d['id'],login_fields(d['data'])) for m,_,d in map(decode,self.replies) if m==2998]
    def charge(self,order='order-0001',product=1):
        return self.req(mid=1111,event_id=250,data=summon.lua(dict(item_id=product,order_id=order)))
    def item(self,tid):return sum(a['count'] for a in self.b.profile()['attachments'] if a['type_id']==tid)
    def fixture(self,tid=1140,n=1000):
        r=self.b.profile();r['gold_coin']=10000;summon.add_item(r,tid,n);self.b.save(r);return self.b.profile()
    def test_enter_and_bootstrap(self):
        d=self.req()[-1][1];self.assertEqual(len(d['exchange_list']),7);self.assertEqual(d['take_list'],{1:1,2:1,3:1,4:1})
        self.assertEqual(d['shop_data']['attach_list'][1]['attach_type'],1249);self.assertEqual(d['shop_data']['need_gold'],10);self.assertEqual(d['canbuy_count'],1)
        cfg=login_fields(decode(self.b.bootstrap()[0])[2]['data']);self.assertFalse(cfg[24]['vip_shop']['had_gift'])
    def test_batch_exchange_exact_cost_and_replay(self):
        self.fixture();before=self.item(1001)
        out=self.req(1,1,3);self.assertEqual(out[-1][0],185)
        self.assertEqual(self.item(1140),985);self.assertEqual(self.item(1001)-before,30)
        self.assertEqual(self.b.respond(self.packet,dict(authenticated=True)),self.replies)
        self.assertEqual(self.item(1140),985)
    def test_insufficient_locked_invalid_and_expired(self):
        self.fixture(n=1)
        for kw in [dict(flag=1,index=1,count=1),dict(flag=1,index=0,count=1),dict(flag=1,index=255,count=1),dict(flag=1,index=1,count=0),dict(flag=1,index=1,count=2**32-1),dict(flag=9)]:
            before=self.b.profile();self.assertEqual(self.req(**kw)[-1][0],55);self.assertEqual(before,self.b.profile())
        self.fixture();r=self.b.profile()
        for a in r['attachments']:
            if a['type_id']==1140:a['is_lock']=True
        self.b.save(r);self.assertEqual(self.req(1,1,1)[-1][0],55)
    def test_daily_buy_cap_upgrade_and_rollover(self):
        self.fixture();before=self.item(1249)
        self.req(3,1,1);self.assertEqual(self.item(1249)-before,1);self.assertEqual(self.b.profile()['gold_coin'],9990)
        self.assertEqual(self.req(3,1,1)[-1][0],55)
        self.charge();self.assertEqual(self.req()[-1][1]['canbuy_count'],1)
        self.req(3,1,1);self.assertEqual(self.req(3,1,1)[-1][0],55)
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):self.assertEqual(self.req()[-1][1]['canbuy_count'],2)
    def test_monthly_charge_claim_all_and_restart(self):
        self.charge(product=4)
        d=self.req()[-1][1];self.assertEqual(d['month_charge'],5000);self.assertEqual(list(d['take_list'].values()),[2]*4)
        for i in range(1,5):
            self.req(2,i,1);self.assertEqual(self.req(2,i,1)[-1][0],55)
        self.assertEqual(self.item(1140),1020)
        self.b.close();self.b=Backend(Path(self.tmp.name),18790,lambda *a,**k:None)
        self.charge(product=4)
        self.assertEqual(self.req()[-1][1]['month_charge'],5000);self.assertEqual(self.item(1140),1020)
        self.assertEqual(list(self.req()[-1][1]['take_list'].values()),[3]*4)
    def test_month_boundaries_and_replayed_old_order(self):
        self.charge(product=4);self.req(2,1,1)
        nov=int(datetime(2026,11,1,tzinfo=timezone(timedelta(hours=8))).timestamp())
        with patch('network_redirect.backend.time.time',return_value=nov-1):self.assertEqual(self.req()[-1][1]['month_charge'],5000)
        with patch('network_redirect.backend.time.time',return_value=nov):
            self.charge(product=4);d=self.req()[-1][1];self.assertEqual(d['month_charge'],0);self.assertEqual(list(d['take_list'].values()),[1]*4)
            self.charge('nov-order-01');self.assertEqual(self.req()[-1][1]['month_charge'],100)
            self.req(2,1,1);self.assertEqual(self.item(1140),40)
    def test_charge_thresholds_not_spending_or_daily_gold(self):
        self.fixture();self.assertEqual(self.req(2,1,1)[-1][0],55)
        self.charge();self.assertEqual(list(self.req()[-1][1]['take_list'].values()),[2,1,1,1])
        self.req(3,1,1);self.assertEqual(self.req()[-1][1]['month_charge'],100)
        self.charge('charge-second',2);self.assertEqual(list(self.req()[-1][1]['take_list'].values()),[2,2,1,1])
    def test_box_targets_cost_and_rejection(self):
        self.fixture(1249,90)
        for tid in (5001,5004,5005):
            item=next(a for a in self.b.profile()['attachments'] if a['type_id']==1249);before=self.item(tid)
            out=self.req(mid=1051,item_type=1249,item_id=item['id'],item_count=30,des_type=5,des_id=tid)
            self.assertEqual(out[-1][0],21);self.assertEqual(self.item(tid)-before,1)
        self.assertEqual(self.item(1249),0)
        self.fixture(1249,60);item=next(a for a in self.b.profile()['attachments'] if a['type_id']==1249)
        for tid,n in [(5002,30),(5001,1),(5001,60)]:
            before=self.b.profile();self.assertEqual(self.req(mid=1051,item_type=1249,item_id=item['id'],item_count=n,des_type=5,des_id=tid)[-1][0],55);self.assertEqual(before,self.b.profile())
    def test_encoding_failure_atomic(self):
        self.fixture();before=self.b.profile()
        with patch.object(self.b,'inventory',side_effect=struct.error('fixture failure')):self.assertEqual(self.req(1,1,1)[-1][0],55)
        self.assertEqual(before,self.b.profile())
    def test_calendar_tip_and_login_hint(self):
        self.charge();cfg=login_fields(decode(self.b.bootstrap()[0])[2]['data']);self.assertTrue(cfg[24]['vip_shop']['had_gift'])
        self.req(2,1,1)
        tip=next(d for m,_,d in map(decode,self.replies) if m==2995);self.assertFalse(login_fields(tip['tip_info'])['had_gift'])
