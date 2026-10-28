import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from network_redirect import welfare,summon
from network_redirect.backend import Backend,login_fields
from network_redirect.protocol import encode,decode

NOW=1792857600
class WelfareTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.b=Backend(Path(self.tmp.name),1,lambda *a,**k:None);self.serial=0
  # Retain coverage of the optional legacy branches; shipping defaults are
  # covered separately by test_welfare_disabled.py.
  self.b.welfare_rules['order']=sorted(welfare.TYPES)
 def tearDown(self):self.b.close();self.tmp.cleanup()
 def req(self,mid=1127,**kw):
  self.serial+=1
  with patch('network_redirect.backend.time.time',return_value=NOW):
   packets=self.b.respond(encode(mid,dict(serial_num=self.serial,**kw)),dict(authenticated=True))
  return [(m,login_fields(d['data']) if m==2998 else d) for m,_,d in map(decode,packets)]
 def claim(self,a,i=0):return self.req(act_type=a,index=i,flag=2)
 def ready(self):
  role=self.b.profile();role.update(level=60,vip_level=10,gold_coin=100000,silver_coin=10000000,buy_growup=1)
  welfare.record_charge(role,10000,NOW,self.b.welfare_rules)
  summon.add_item(role,1001,1000);self.b.save(role);return role
 def error(self,replies):return any(m==2998 and 'op_string' in d for m,d in replies)
 def test_catalog_and_bootstrap(self):
  role=self.b.profile();data=login_fields(decode(welfare.query(role,NOW,self.b.welfare_rules))[2]['data'])
  self.assertEqual(set(data['all_activity']),welfare.TYPES)
  self.assertLess(len(welfare.query(role,NOW,self.b.welfare_rules)),32768)
  self.assertTrue(self.b.bootstrap())
 def test_every_manual_reward_and_double_claim(self):
  for a,i in [(16,0),(22,0),(23,0),(21,0),(21,10),(32,1),(32,2),(33,1),(35,1),(35,2),(36,1),(60,1),(71,1),(71,100)]:
   with self.subTest(a=a,i=i):
    self.ready();self.assertFalse(self.error(self.claim(a,i)))
    before=self.b.profile();self.assertTrue(self.error(self.claim(a,i)));self.assertEqual(before,self.b.profile())
 def test_turn_result_persisted_and_cannot_forge(self):
  role=self.ready();c=welfare.catalog(role,NOW,self.b.welfare_rules);chosen=c[33]['step_list'][0];self.b.save(role)
  self.assertEqual(chosen,welfare.catalog(self.b.profile(),NOW,self.b.welfare_rules)[33]['step_list'][0])
  before=self.b.profile();self.assertTrue(self.error(self.claim(33,10+(chosen%8+1))));self.assertEqual(before,self.b.profile())
  self.assertFalse(self.error(self.claim(33,10+chosen)));self.assertTrue(self.error(self.claim(33,10+chosen)))
 def test_group_rebate_limit_and_replay(self):
  self.ready();start=self.b.profile()['gold_coin']
  self.assertFalse(self.error(self.req(1239,buy_count=4)))
  self.assertFalse(self.error(self.req(1239,buy_count=1)))
  self.assertEqual(start-self.b.profile()['gold_coin'],450)
  self.assertTrue(self.error(self.req(1239,buy_count=6)))
  self.assertFalse(self.error(self.req(1239,buy_count=5)))
  self.assertEqual(start-self.b.profile()['gold_coin'],800)
 def test_daily_pay_and_monday_weekly_reset(self):
  self.ready()
  for op in (2,3):
   self.assertFalse(self.error(self.req(1352,id=op,data='{index=1}')))
   self.assertTrue(self.error(self.req(1352,id=op,data='{index=1}')))
  role=self.b.profile();nextday=NOW+86400;welfare.record_charge(role,1000,nextday,self.b.welfare_rules)
  cat=welfare.catalog(role,nextday,self.b.welfare_rules)[74]['data']
  self.assertEqual(cat['charge_data'][0]['status'],2);self.assertEqual(cat['total_charge_data'][0]['status'],2)
  self.assertEqual(cat['total_charge'],100)
 def test_fund_cards_first_gift_not_double(self):
  before=self.b.profile();self.assertTrue(self.error(self.req(1112,event_id=3,data='{item_id=8}')));self.assertEqual(before,self.b.profile())
  role=self.b.profile();summon.add_item(role,1156,9);self.b.save(role)
  self.req(1111,event_id=251,data='{item_id=202,order_id="welfare-fund-001",large_count=0,small_count=9}')
  r=self.b.profile();self.assertEqual(r['buy_growup'],1);self.assertEqual(r['gold_coin'],60);self.assertEqual(r['first_charge'],0);self.assertEqual(r['first_charge_gift'],1)
  self.assertFalse(self.error(self.req(1201,flag=6,id=0)));self.assertTrue(self.error(self.req(1201,flag=6,id=0)))
  self.assertTrue(self.error(self.req(1112,event_id=3,data='{item_id=8}')))
 def test_first_charge_double_only_once(self):
  role=self.b.profile();summon.add_item(role,1156,4);self.b.save(role)
  self.req(1111,event_id=251,data='{item_id=101,order_id="welfare-order-001",large_count=0,small_count=2}')
  r=self.b.profile();self.assertEqual(r['gold_coin'],260);self.assertEqual(r['charge_gold'],100)
  self.req(1111,event_id=251,data='{item_id=101,order_id="welfare-order-001",large_count=0,small_count=2}')
  self.assertEqual(r,self.b.profile())
  self.req(1111,event_id=251,data='{item_id=101,order_id="welfare-order-002",large_count=0,small_count=2}')
  self.assertEqual(self.b.profile()['gold_coin'],360)
 def test_upgrade_after_old_deadline_uses_current_level(self):
  self.ready()
  role=self.b.profile();role['welfare']['start']=NOW-31*86400;role['welfare']['last_level']=20;role['welfare']['end_level']=20;self.b.save(role)
  before=self.b.profile()['gold_coin'];self.assertFalse(self.error(self.claim(7)))
  self.assertEqual(self.b.profile()['gold_coin']-before,1500)
 def test_permanent_growth_level_boundaries_and_lifetime_claim(self):
  for level,amount in [(9,0),(10,100),(19,100),(20,300),(29,300),(30,600),(39,600),(40,1000),(49,1000),(50,1500),(99,1500)]:
   with self.subTest(level=level):
    role=self.b.profile();role['level']=level
    role.pop('welfare',None);self.b.save(role)
    before=self.b.profile()['gold_coin']
    catalog=welfare.catalog(role,NOW,self.b.welfare_rules)[7]
    self.assertTrue(catalog['permanent']);self.assertEqual(catalog['end_time'],0)
    self.assertEqual(catalog['can_take'],amount>0)
    self.assertEqual(self.error(self.claim(7)),amount==0)
    self.assertEqual(self.b.profile()['gold_coin']-before,amount)
    if amount:
     role=self.b.profile();role['level']=99;self.b.save(role)
     self.assertTrue(self.error(self.claim(7)))
     self.assertFalse(welfare.catalog(role,NOW+400*86400,self.b.welfare_rules)[7]['can_take'])
 def test_growth_replay_restart_and_legacy_claim(self):
  self.ready();packet=encode(1127,dict(serial_num=500,act_type=7,index=0,flag=2));auth=dict(authenticated=True)
  with patch('network_redirect.backend.time.time',return_value=NOW):
   first=self.b.respond(packet,auth);saved=self.b.profile()
   self.assertEqual(first,self.b.respond(packet,auth));self.assertEqual(saved,self.b.profile())
  self.b.close();self.b=Backend(Path(self.tmp.name),1,lambda *a,**k:None)
  before=self.b.profile();self.assertTrue(self.error(self.claim(7)));self.assertEqual(before,self.b.profile())
  self.assertEqual(saved['gold_coin'],before['gold_coin'])
  self.assertIn('7:0',before['welfare']['claims'])
 def test_growth_invalid_index_and_red_dot(self):
  self.ready();before=self.b.profile()
  self.assertTrue(self.error(self.claim(7,1)));self.assertEqual(before,self.b.profile())
  def flag():
   data=login_fields(decode(welfare.hint(self.b.profile(),NOW,self.b.welfare_rules))[2]['data'])
   return data[24]['activity_info']['had_prize_flag'][7]
  self.assertTrue(flag());self.claim(7);self.assertFalse(flag())
 def test_atomic_exchange_and_invalid_requests(self):
  for a,i in [(0,0),(255,1),(32,255),(33,255),(35,255),(71,101),(74,255),(48,0)]:
   before=self.b.profile();self.assertTrue(self.error(self.claim(a,i)));self.assertEqual(before,self.b.profile())
  self.ready();role=self.b.profile();role['silver_coin']=0;self.b.save(role);before=self.b.profile()
  self.assertTrue(self.error(self.claim(32,1)));self.assertEqual(before,self.b.profile())
 def test_replay_restart_persistent_claim(self):
  self.ready();pkt=encode(1127,dict(serial_num=20,act_type=16,index=0,flag=2));auth=dict(authenticated=True)
  with patch('network_redirect.backend.time.time',return_value=NOW):
   result=self.b.respond(pkt,auth);role=self.b.profile();self.assertEqual(result,self.b.respond(pkt,auth));self.assertEqual(role,self.b.profile())
  self.b.close();self.b=Backend(Path(self.tmp.name),1,lambda *a,**k:None)
  self.assertTrue(self.error(self.claim(16)))
 def test_original_friend_rules_and_progress(self):
  r=self.ready();rules=welfare.friend_rules();self.assertEqual(len(rules),6);self.assertEqual(rules[0]['prizes'],[[11,1,80,1],[12,1,600000,1]])
  win=encode(1027,dict(fight_type=1,final_result=1,fight_round=0,fight_result=[]))
  lose=encode(1027,dict(fight_type=1,final_result=4,fight_round=0,fight_result=[]))
  welfare.track(r,1026,{},[lose],NOW,self.b.welfare_rules)
  self.assertFalse(welfare.catalog(r,NOW,self.b.welfare_rules)[36]['day_tasks'][6]['can_take'])
  for _ in range(10):welfare.track(r,1026,{},[win],NOW,self.b.welfare_rules)
  self.assertTrue(welfare.catalog(r,NOW,self.b.welfare_rules)[36]['day_tasks'][6]['can_take'])
 def test_anniversary_claim_window_and_original_multiplier(self):
  self.ready();self.assertTrue(self.error(self.claim(34)))
  role=self.b.profile();role['welfare']['start']=NOW-29*86400;self.b.save(role)
  before=role['gold_coin'];self.assertFalse(self.error(self.claim(34)))
  self.assertEqual(self.b.profile()['gold_coin']-before,10000)
  self.assertTrue(self.error(self.claim(34)))
 def test_anniversary_mail_and_claim_once(self):
  role=self.ready();role['welfare']['start']=NOW-29*86400;self.b.save(role)
  self.req(act_type=0,index=0,flag=1)
  mail=self.b.profile()['welfare']['mails']['anniversary']
  out=self.req(1102,mail_id=mail['mail_id'],flag=1)
  content=next(d for m,d in out if m==2998 and 'mail_body' in d)
  self.assertEqual(content['attach_count'],2)
  before=self.b.profile()['gold_coin'];self.assertFalse(self.error(self.req(1103,mail_id=mail['mail_id'],flag=1)))
  self.assertEqual(self.b.profile()['gold_coin']-before,600)
  self.assertTrue(self.error(self.req(1103,mail_id=mail['mail_id'],flag=1)))
 def test_consecutive_charge_days_break(self):
  role=self.ready();s=role['welfare'];day=NOW//86400
  s['charge_days']={str(day):100,str(day-2):100,str(day-3):100}
  self.assertEqual(welfare.charge_streak(s,day),1)
  s['charge_days'][str(day-1)]=100
  self.assertEqual(welfare.charge_streak(s,day),4)
 def test_season_and_crossday(self):
  r=self.ready();s=r['welfare'];welfare.prepare(r,NOW,self.b.welfare_rules);self.assertEqual(len(s['login_days']),1)
  welfare.prepare(r,NOW+86400,self.b.welfare_rules);self.assertEqual(len(s['login_days']),2)
  r['welfare']['start']=NOW-31*86400;self.b.save(r);self.assertTrue(self.error(self.claim(35,1)))

if __name__=='__main__':unittest.main()
