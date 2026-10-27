"""Caishen wire rewards, random offers, calendar boundaries and atomic saves."""
import copy
import json
from pathlib import Path
from unittest.mock import patch
from test_activity import ActivityCase, NOW
from network_redirect import activity, activity_caishen as cs, formation, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode


class CaishenTests(ActivityCase):
    def count(self,tid):return sum(i['count'] for i in self.b.profile()['attachments'] if i['attach_type']==5 and i['type_id']==tid)
    def status(self):
        out=self.req(1205,flag=0);self.ok(out)
        return next(d['visit_caishen'] for e,d in out if e==47)
    def saved(self):return self.b.profile()['activity']['seasonal']['spring']
    def rich(self,n=10000):
        r=self.b.profile();summon.add_item(r,1028,n);self.b.save(r)
    def mails(self):return [v for k,v in self.b.profile().get('welfare',{}).get('mails',{}).items() if k.startswith('caishen-recycle-')]
    def restart(self):
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)

    def test_preview_and_validation(self):
        data=self.status()
        self.assertEqual(len(data['prize_list']),5);self.assertEqual(len(data['random_get_item']),7)
        self.assertAlmostEqual(sum(x['probability'] for x in data['random_get_item'].values()),1)
        self.assertEqual([v['count'] for v in data['coin_pool'].values()],[100,200,300])
        bad=[]
        for key,value in [('spring_pool',[]),('spring_pool_weights',[1]*6),('spring_coin_pool',[{}]),
                          ('spring_shop_revision',''),('spring_recycle_coins_per_peach',1),('spring_shop',[])]:
            r=copy.deepcopy(self.b.activity_rules);r[key]=value;bad.append(r)
        for field,val in [('cost',0),('limit',2),('reward',[10,99999,1,1])]:
            r=copy.deepcopy(self.b.activity_rules);r['spring_shop'][0][field]=val;bad.append(r)
        for r in bad:
            p=Path(self.tmp.name)/'bad.json';p.write_text(json.dumps(r))
            with self.assertRaises(formation.Rejected):activity.load_rules(p)

    def test_all_weight_intervals_exhaustive(self):
        r=self.b.activity_rules
        for values,weights in [([100,200,300],[60,30,10]),(r['spring_pool'],r['spring_pool_weights'])]:
            results=[]
            for n in range(sum(weights)):
                with patch.object(cs,'randbelow',return_value=n):results.append(cs.draw(values,weights))
            self.assertEqual([results.count(x) for x in values],weights)

    def test_daily_two_draws_replay_restart_and_silver(self):
        self.status();before=self.b.profile()
        with patch.object(cs,'randbelow',side_effect=[99,60]) as rng:
            out=self.req(1210,flag=1);self.ok(out);self.assertEqual(rng.call_count,2)
        prize=next(d for e,d in out if e==88)
        self.assertEqual(len(prize['prize_list']),2);self.assertEqual(self.count(1028),300)
        self.assertEqual(self.b.profile()['silver_coin']-before['silver_coin'],50000)
        self.assertEqual(self.b.profile()['gold_coin'],before['gold_coin'])
        after=self.b.profile();self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
        self.assertEqual(after,self.b.profile());self.assertEqual(self.req(1210,flag=1)[0][0],55)
        self.assertEqual(after,self.b.profile());self.restart();self.status()
        self.assertEqual(self.saved()['weekly_visits'],1);self.assertEqual(self.req(1210,flag=1)[0][0],55)

    def test_all_item_rewards_and_coin_quantities(self):
        self.status();r=self.b.activity_rules;ticket=0
        for idx,p in enumerate(r['spring_pool']):
            now=NOW+idx*86400
            with patch('network_redirect.backend.time.time',return_value=now):
                self.status();before=self.b.profile()
                with patch.object(cs,'randbelow',side_effect=[(0,60,90)[idx%3],ticket]):out=self.req(1210,flag=1)
            self.ok(out);prizes=next(d['prize_list'] for e,d in out if e==88)
            self.assertEqual(prizes[1]['attach_count'],[100,200,300][idx%3])
            self.assertEqual((prizes[2]['object_type'],prizes[2]['attach_type'],prizes[2]['attach_count']),tuple(p[:3]))
            if p[0]==5:
                old=sum(x['count'] for x in before['attachments'] if x['type_id']==p[1])
                self.assertEqual(self.count(p[1])-old,p[2])
            ticket+=r['spring_pool_weights'][idx]

    def test_shop_unique_no_reroll_and_candidates(self):
        self.status();before=self.saved()
        with patch.object(cs,'randbelow',side_effect=AssertionError('reroll')):self.status()
        self.assertEqual(before,self.saved());self.restart();self.status();self.assertEqual(before,self.saved())
        r=self.b.activity_rules
        for idx in range(8):
            role=self.b.profile();role['activity']['seasonal'].pop('spring')
            with patch.object(cs,'randbelow',side_effect=[idx,0,0,0,idx%5]):s=cs.state(role,NOW,r)
            self.assertEqual(len({x['reward'][1] for x in s['shop']}),5)
            self.assertEqual([x['tier'] for x in s['shop']],['low']*4+['high'])
            self.assertEqual(s['shop'][0],r['spring_shop'][idx]);self.assertEqual(s['shop'][4],r['spring_shop'][8+idx%5])

    def test_all_13_goods_cost_count_grant_and_limit(self):
        r=self.b.activity_rules
        for idx,row in enumerate(r['spring_shop']):
            now=NOW+idx*86400
            with patch('network_redirect.backend.time.time',return_value=now):
                with patch.object(cs,'randbelow',side_effect=[idx if idx<8 else 0,0,0,0,max(0,idx-8)]):data=self.status()
                self.rich();before=self.b.profile();typ,tid,n,_=row['reward']
                goods=next(x for x in data['prize_list'].values() if x['attach_type']==tid)
                out=self.req(1211,prize_id=goods['prize_id'],count=1);self.ok(out)
                actual=next(d for e,d in out if e==87);self.assertEqual(actual['attach_count'],n)
                self.assertEqual(sum(x['count'] for x in before['attachments'] if x['type_id']==1028)-self.count(1028),row['cost'])
                if typ==10:self.assertEqual(self.b.profile()['souls'].get(str(tid),0)-before.get('souls',{}).get(str(tid),0),n)
                else:self.assertEqual(self.count(tid)-sum(x['count'] for x in before['attachments'] if x['type_id']==tid),n)
                after=self.b.profile();self.assertEqual(self.req(1211,prize_id=goods['prize_id'],count=1)[0][0],55)
                self.assertEqual(after,self.b.profile())

    def test_invalid_absent_insufficient_locked_and_encoding_rollback(self):
        data=self.status();ident=data['prize_list'][1]['prize_id']
        for mid,args in [(1210,dict(flag=0)),(1211,dict(prize_id=ident,count=2)),(1211,dict(prize_id=ident,count=0)),
                         (1211,dict(prize_id=ident,count=1)),(1211,dict(prize_id=1,count=1))]:
            before=self.b.profile();self.assertEqual(self.req(mid,**args)[0][0],55);self.assertEqual(before,self.b.profile())
        self.rich();role=self.b.profile()
        for x in role['attachments']:
            if x['type_id']==1028:x['is_lock']=1
        self.b.save(role);before=self.b.profile()
        self.assertEqual(self.req(1211,prize_id=ident,count=1)[0][0],55);self.assertEqual(before,self.b.profile())
        real=summon.event
        def broken(event,data):
            if event==88:raise ValueError('encode failure')
            return real(event,data)
        with patch.object(summon,'event',side_effect=broken):
            self.assertEqual(self.req(1210,flag=1)[0][0],55)
        self.assertEqual(before,self.b.profile())

    def test_midnight_stale_offer_before_and_after_refresh(self):
        with patch.object(cs,'randbelow',return_value=0):data=self.status()
        self.rich();ident=data['prize_list'][1]['prize_id']
        self.ok(self.req(1210,flag=1));self.ok(self.req(1211,prize_id=ident,count=1))
        boundary=data['next_daily_refresh']
        with patch('network_redirect.backend.time.time',return_value=boundary-1):
            self.assertTrue(self.status()['visited_today']);self.assertEqual(self.req(1210,flag=1)[0][0],55)
        with patch('network_redirect.backend.time.time',return_value=boundary):
            before=self.b.profile();self.assertEqual(self.req(1211,prize_id=ident,count=1)[0][0],55);self.assertEqual(before,self.b.profile())
            with patch.object(cs,'randbelow',return_value=0):fresh=self.status()
            self.assertFalse(fresh['visited_today']);self.assertEqual(self.saved()['purchases'],{})
            self.assertNotEqual(fresh['prize_list'][1]['prize_id'],ident)
            self.assertEqual(self.req(1211,prize_id=ident,count=1)[0][0],55)
            self.ok(self.req(1210,flag=1));self.ok(self.req(1211,prize_id=fresh['prize_list'][1]['prize_id'],count=1))
        stable=self.saved();self.status();self.assertEqual(stable,self.saved());self.assertEqual(self.req(1210,flag=1)[0][0],55)

    def test_weekly_mail_even_odd_locked_stacks_claim_and_restart(self):
        data=self.status();self.ok(self.req(1210,flag=1));role=self.b.profile()
        role['attachments']=[i for i in role['attachments'] if i['type_id']!=1028]
        for n,extra in [(100,{}),(6,{'is_lock':1}),(1,{'owner_id':99})]:
            role['attachments'].append(dict(id=formation.new_id(role),attach_type=5,type_id=1028,count=n,level=1,**extra))
        self.b.save(role);peaches=self.count(1001);deadline=data['next_weekly_refresh']
        with patch('network_redirect.backend.time.time',return_value=deadline-1):self.status();self.assertEqual(self.count(1028),107)
        with patch('network_redirect.backend.time.time',return_value=deadline):
            out=self.req(1205,flag=0);self.ok(out);self.assertIn(13,[e for e,d in out])
            self.assertEqual(self.count(1028),0);self.assertEqual(self.count(1001),peaches)
            mail=self.mails()[0];self.assertEqual(mail['prizes'],[[5,1001,54,1]])
            self.assertIn('107枚',mail['mail_body']);self.assertTrue(mail['no_expiry'])
            self.assertEqual(self.saved()['weekly_visits'],0);self.assertEqual(self.saved()['weekly_coins'],0)
            self.restart();self.status();self.assertEqual(len(self.mails()),1)
            self.ok(self.req(1102,mail_id=mail['mail_id'],flag=0));self.ok(self.req(1103,mail_id=mail['mail_id']))
            self.assertEqual(self.count(1001),peaches+54);self.assertEqual(self.req(1103,mail_id=mail['mail_id'])[0][0],55)
        self.status();self.assertEqual(len(self.mails()),1)
        with patch('network_redirect.backend.time.time',return_value=deadline+28*86400):self.status()
        self.assertEqual(len(self.mails()),1);self.assertEqual(self.count(1028),0)

    def test_week_direct_visit_recycles_before_new_reward_and_mail_failure_rolls_back(self):
        data=self.status();self.rich(102);before=self.b.profile();boundary=data['next_weekly_refresh']
        with patch('network_redirect.backend.time.time',return_value=boundary),patch('network_redirect.system_mail.deliver',side_effect=formation.Rejected('mail failure')):
            self.assertEqual(self.req(1210,flag=1)[0][0],55)
            after=self.b.profile()
            for key in ('activity','attachments','welfare','gold_coin','silver_coin'):self.assertEqual(before.get(key),after.get(key))
        with patch('network_redirect.backend.time.time',return_value=boundary),patch.object(cs,'randbelow',return_value=0):
            self.ok(self.req(1210,flag=1));self.assertEqual(self.count(1028),100)
            self.assertEqual(self.mails()[0]['prizes'],[[5,1001,51,1]])
            self.assertEqual(self.saved()['weekly_visits'],1)

    def test_heartbeat_rollover_and_rollback_watermark(self):
        data=self.status();self.rich(1)
        with patch('network_redirect.backend.time.time',return_value=data['next_weekly_refresh']):
            out=self.b.respond(encode(2999,{}),self.state)
            self.assertIn(13,[d['id'] for m,_,d in map(decode,out) if m==2998])
        self.assertEqual(self.count(1028),0);self.assertEqual(self.mails()[0]['prizes'],[[5,1001,1,1]])
        self.status();self.assertGreater(self.saved()['day'],data['shop_day'])
        self.ok(self.req(1210,flag=1));stable=self.saved()
        with patch('network_redirect.backend.time.time',return_value=data['next_weekly_refresh']):
            self.status();self.assertEqual(self.req(1210,flag=1)[0][0],55)
        self.assertEqual(self.saved(),stable);self.assertEqual(len(self.mails()),1)

    def test_permanent_disabled_login_recycling_and_no_travel_coins(self):
        self.b.activity_rules['seasonal_games']['spring_money']['end_time']=NOW-1
        data=self.status();self.assertTrue(data['local_enabled']);self.ok(self.req(1210,flag=1))
        from network_redirect.activity_seasonal import travel_drop
        role=self.b.profile();before=sum(i['count'] for i in role['attachments'] if i['type_id']==1028)
        travel_drop(role,NOW,self.b.activity_rules)
        self.assertEqual(sum(i['count'] for i in role['attachments'] if i['type_id']==1028),before)
        self.b.activity_rules['seasonal_games']['spring_money']['enabled']=False
        self.assertFalse(self.status()['local_enabled']);before=self.b.profile()
        self.assertEqual(self.req(1210,flag=1)[0][0],55);self.assertEqual(before,self.b.profile())
        with patch('network_redirect.backend.time.time',return_value=data['next_weekly_refresh']):self.b.snapshot()
        self.assertEqual(self.count(1028),0);self.assertEqual(len(self.mails()),1)

    def test_old_save_migration_retains_cards_visit_and_relevant_quota(self):
        self.status();role=self.b.profile();old=role['activity']['seasonal']['spring']
        role['activity']['seasonal']['spring']=dict(day=activity.day(NOW,self.b.activity_rules),last_visit_time=NOW,
             purchases={'2':3,'4':1},cards_given=old['cards_given'])
        self.b.save(role);before=self.b.profile()
        with patch.object(cs,'randbelow',return_value=0):data=self.status()
        self.assertTrue(data['visited_today']);self.assertEqual(self.saved()['purchases']['1023'],3)
        self.assertEqual(data['prize_list'][2]['count'],0)
        self.assertEqual(before['attachments'],self.b.profile()['attachments'])
        self.assertEqual(before['activity']['seasonal']['spring']['cards_given'],self.saved()['cards_given'])
        self.assertEqual(self.req(1210,flag=1)[0][0],55)
        self.rich(200)
        with patch('network_redirect.backend.time.time',return_value=NOW+7*86400):self.status()
        self.assertEqual(len(self.mails()),1);self.assertEqual(self.mails()[0]['prizes'],[[5,1001,100,1]])

    def test_first_use_and_offline_multiweek_single_settlement(self):
        self.rich(200);self.status();self.assertEqual(self.mails(),[])
        with patch('network_redirect.backend.time.time',return_value=NOW+35*86400):self.status()
        self.assertEqual(len(self.mails()),1);self.assertEqual(self.saved()['weekly_visits'],0)
        self.assertEqual(self.mails()[0]['prizes'],[[5,1001,100,1]])

    def test_accounts_have_independent_shops_and_inventory(self):
        with patch.object(cs,'randbelow',return_value=0):first=self.status()
        other=Backend(Path(self.tmp.name)/'other',18771,lambda *a,**k:None)
        try:
            role=other.profile()
            with patch.object(cs,'randbelow',side_effect=[7,0,0,0,4]):s=cs.state(role,NOW,other.activity_rules)
            other.save(role);cs.settle(role,1210,dict(flag=1),NOW,other.activity_rules);other.save(role)
            self.assertNotEqual(first['prize_list'][1]['attach_type'],s['shop'][0]['reward'][1])
            self.assertEqual(self.count(1028),0);self.assertEqual(self.saved()['weekly_visits'],0)
        finally:other.close()
