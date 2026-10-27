"""Wire-level fishing settlement, persistent random shop and calendar boundaries."""
import copy
import json
from pathlib import Path
from unittest.mock import patch
from test_activity import ActivityCase, NOW
from network_redirect import activity, activity_fish as fish, formation, summon
from network_redirect.protocol import encode, decode
from network_redirect.backend import Backend, login_fields


class FishTests(ActivityCase):
    def count(self, tid):
        return sum(i['count'] for i in self.b.profile()['attachments'] if i['attach_type']==5 and i['type_id']==tid)

    def status(self):
        out=self.req(1205,flag=0);self.ok(out)
        return next(d['search_gold_data'] for e,d in out if e==47)

    def fishing(self):return self.b.profile()['activity']['seasonal']['fish']

    def rich(self):
        role=self.b.profile();summon.add_item(role,1027,10000);self.b.save(role)

    def test_preview_and_config_validation(self):
        data=self.status()
        self.assertEqual(len(data['random_get_item']),8)
        self.assertEqual(len(data['exchange_data']),5)
        self.assertEqual(data['cost_gold_count'],100)
        self.assertTrue(data['local_permanent'])
        for key,value in [('fish_pool_weights',[1]*7),('fish_pool',[]),('fish_gold_per_net',0),
                          ('fish_koi_pool',[dict(count=2,weight=10)]),('fish_shop',[])]:
            cfg=copy.deepcopy(self.b.activity_rules);cfg[key]=value
            path=Path(self.tmp.name)/'bad.json';path.write_text(json.dumps(cfg))
            with self.assertRaises(formation.Rejected):activity.load_rules(path)

    def test_single_free_paid_ten_and_restart(self):
        self.status();self.status();self.assertEqual(self.count(1026),3)
        gold=self.b.profile()['gold_coin']
        with patch.object(fish,'randbelow',return_value=0):
            self.ok(self.req(1208,count=1,type_id=0))
            self.assertEqual(self.count(1026),2);self.assertEqual(self.count(1027),2)
            self.assertEqual(self.b.profile()['gold_coin'],gold)
            self.ok(self.req(1208,count=10,type_id=0))
            self.assertEqual(self.count(1026),2);self.assertEqual(self.count(1027),22)
            self.assertEqual(self.b.profile()['gold_coin'],gold-1000)
            for _ in range(3):self.ok(self.req(1208,count=1,type_id=0))
        self.assertEqual(self.b.profile()['gold_coin'],gold-1100)
        before=self.fishing()
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.status();self.assertEqual(before,self.fishing());self.assertEqual(self.count(1026),0)

    def test_weighted_boundaries_exhaustive(self):
        cfg=self.b.activity_rules
        for values,weights in [([2,3,5],[60,30,10]),(cfg['fish_pool'],cfg['fish_pool_weights'])]:
            results=[]
            for ticket in range(sum(weights)):
                with patch.object(fish,'randbelow',return_value=ticket):results.append(fish.draw(values,weights))
            self.assertEqual([results.count(v) for v in values],weights)

    def test_ten_independent_draws_duplicate_and_silver(self):
        self.status();before=self.b.profile()
        with patch.object(fish,'randbelow',side_effect=[99,50]*10) as rng:
            out=self.req(1208,count=10,type_id=0);self.ok(out)
            self.assertEqual(rng.call_count,20)
        self.assertEqual(self.count(1027),50)
        self.assertEqual(self.b.profile()['silver_coin']-before['silver_coin'],500000)
        self.assertEqual(len(next(d for e,d in out if e==85)['item_list']),20)
        after=self.b.profile()
        self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
        self.assertEqual(after,self.b.profile())
        self.assertEqual(self.fishing()['weekly_casts'],10)

    def test_shop_no_duplicates_and_no_query_reroll(self):
        self.status();s=self.fishing()
        self.assertEqual(len({x['reward'][1] for x in s['shop']}),5)
        self.assertEqual([x['tier'] for x in s['shop']],['low']*4+['high'])
        with patch.object(fish,'randbelow',side_effect=AssertionError('reroll')):self.status()
        self.assertEqual(self.fishing(),s)
        # Every candidate can occupy the first low / high position.
        cfg=self.b.activity_rules
        for idx in range(6):
            role=copy.deepcopy(self.b.profile());role['activity']['seasonal'].pop('fish')
            with patch.object(fish,'randbelow',side_effect=[idx,0,0,0,idx]):s=fish.state(role,NOW,cfg)
            self.assertEqual(s['shop'][0],cfg['fish_shop'][idx])
            self.assertEqual(s['shop'][4],cfg['fish_shop'][idx+6])

    def test_batch_exchange_limit_and_atomic_rejections(self):
        with patch.object(fish,'randbelow',return_value=0):self.status()
        self.rich();row=self.fishing()['shop'][0];tid=row['reward'][1]
        before=self.count(tid);out=self.req(1208,count=2,type_id=tid);self.ok(out)
        self.assertEqual(self.count(tid)-before,row['reward'][2]*2)
        self.assertEqual(self.count(1027),10000-row['cost']*2)
        self.assertEqual(self.fishing()['purchases'][str(tid)],2)
        self.status();self.assertEqual(self.fishing()['purchases'][str(tid)],2)
        absent=next(x['reward'][1] for x in self.b.activity_rules['fish_shop'] if x not in self.fishing()['shop'])
        for n,t in [(row['limit'],tid),(1,absent),(1,999999),(2,0),(0,0),(101,tid)]:
            before=self.b.profile();self.assertEqual(self.req(1208,count=n,type_id=t)[0][0],55)
            self.assertEqual(before,self.b.profile())
        role=self.b.profile();role['gold_coin']=0;self.b.save(role);before=self.b.profile()
        self.assertEqual(self.req(1208,count=10,type_id=0)[0][0],55);self.assertEqual(before,self.b.profile())

    def test_all_high_goods_granted_once(self):
        for idx in range(6):
            with patch('network_redirect.backend.time.time',return_value=NOW+idx*86400), \
                 patch.object(fish,'randbelow',side_effect=[0,0,0,0,idx]):self.status()
            self.rich();row=self.fishing()['shop'][4];typ,tid,n,_=row['reward'];before=self.b.profile()
            self.ok(self.req(1208,count=1,type_id=tid))
            after=self.b.profile()
            self.assertEqual(row['cost'],20)
            self.assertEqual(sum(i['count'] for i in before['attachments'] if i['type_id']==1027)-self.count(1027),20)
            if typ==10:self.assertEqual(after['souls'].get(str(tid),0)-before.get('souls',{}).get(str(tid),0),5)
            else:self.assertEqual(sum(i['count'] for i in after['attachments'] if i['type_id']==tid)-sum(i['count'] for i in before['attachments'] if i['type_id']==tid),5)
            self.assertEqual(self.req(1208,count=1,type_id=tid)[0][0],55)

    def test_daily_boundary_and_stale_exchange(self):
        data=self.status();self.rich();row=self.fishing()['shop'][0]
        self.ok(self.req(1208,count=1,type_id=row['reward'][1]));old=self.fishing()
        deadline=data['next_daily_refresh']
        with patch('network_redirect.backend.time.time',return_value=deadline-1):self.status()
        self.assertEqual(old,self.fishing())
        with patch('network_redirect.backend.time.time',return_value=deadline):
            before=self.b.profile()
            self.assertEqual(self.req(1208,count=1,type_id=row['reward'][1])[0][0],55)
            self.assertEqual(before,self.b.profile())
            self.status();self.assertEqual(self.fishing()['purchases'],{})
            self.assertEqual(self.count(1026),6)
        self.assertEqual(self.fishing()['weekly_exchanges'],1)
        # Returning the clock to yesterday cannot reset quotas or gift again.
        stable=self.fishing();self.status();self.assertEqual(stable,self.fishing());self.assertEqual(self.count(1026),6)

    def test_week_boundary_offline_jump_and_inventory_preserved(self):
        data=self.status();self.rich()
        self.ok(self.req(1208,count=10,type_id=0))
        self.ok(self.req(1208,count=1,type_id=self.fishing()['shop'][0]['reward'][1]))
        deadline=data['next_weekly_refresh'];old=self.fishing()
        with patch('network_redirect.backend.time.time',return_value=deadline-1):self.status()
        self.assertEqual(self.fishing()['weekly_casts'],10)
        before=self.count(1027);nets=self.count(1026)
        with patch('network_redirect.backend.time.time',return_value=deadline):
            new=self.status();self.assertEqual(new['weekly_casts'],0)
            self.assertEqual(new['weekly_koi'],0);self.assertEqual(new['weekly_exchanges'],0)
            self.assertEqual(self.fishing()['news'],[]);self.assertEqual(self.count(1027),0)
            mails=self.recycle_mails();self.assertEqual(len(mails),1)
            self.assertEqual(mails[0]['prizes'],[[5,1001,before,1]])
            self.assertEqual(self.count(1026),nets+3)
        with patch('network_redirect.backend.time.time',return_value=deadline+28*86400):self.status()
        self.assertEqual(self.count(1026),nets+6)  # Missed days do not accumulate gifts.
        self.assertGreater(self.fishing()['week'],old['week'])
        self.assertEqual(len(self.recycle_mails()),1)

    def test_migration_preserves_inventory_and_gift(self):
        self.status();role=self.b.profile();before=self.count(1026)
        role['activity']['seasonal']['fish']={'day':activity.day(NOW,self.b.activity_rules),
           'purchases':{'1001':8},'news':[],'gift_day':activity.day(NOW,self.b.activity_rules)}
        self.b.save(role);self.status()
        self.assertEqual(self.count(1026),before);self.assertEqual(len(self.fishing()['shop']),5)
        self.assertEqual(self.fishing()['purchases'],{})

    def test_permanent_window_and_disabled_atomic(self):
        self.b.activity_rules['seasonal_games']['fish']['end_time']=NOW-1
        self.assertTrue(self.status()['local_enabled'])
        self.ok(self.req(1208,count=1,type_id=0))
        self.b.activity_rules['seasonal_games']['fish']['enabled']=False
        self.assertFalse(self.status()['local_enabled']);before=self.b.profile()
        self.assertEqual(self.req(1208,count=1,type_id=0)[0][0],55);self.assertEqual(before,self.b.profile())

    def test_new_low_shop_values_and_settlement(self):
        expected={1007:(5,3),1343:(5,1),1024:(5,3),1042:(5,1),1032:(3,3),1031:(5,1)}
        for idx,(tid,(cost,limit)) in enumerate(expected.items()):
            with patch('network_redirect.backend.time.time',return_value=NOW+idx*86400), patch.object(fish,'randbelow',side_effect=[idx,0,0,0,0]):
                data=self.status()
            row=data['exchange_data'][1]
            self.assertEqual((row['type_id'],row['attach_count'],row['cost_fish_count'],row['count']),(tid,1,cost,limit))
            self.rich();before=self.count(tid);balance=self.count(1027)
            self.ok(self.req(1208,count=limit,type_id=tid))
            self.assertEqual(self.count(tid)-before,limit)
            self.assertEqual(balance-self.count(1027),cost*limit)
            self.assertEqual(self.req(1208,count=1,type_id=tid)[0][0],55)

    def test_shop_revision_migrates_without_reroll_or_quota_reset(self):
        with patch.object(fish,'randbelow',return_value=0):self.status()
        self.rich();role=self.b.profile();s=role['activity']['seasonal']['fish']
        s.pop('shop_revision')
        for row in s['shop']:
            row['cost']=60
            if row['reward'][1]==1343:row['reward'][2]=5;row['limit']=5
        s['purchases']={'1343':3,'1007':1};s['weekly_exchanges']=4
        self.b.save(role);before=self.b.profile();ids=[x['reward'][1] for x in s['shop']]
        with patch.object(fish,'randbelow',side_effect=AssertionError('unexpected reroll')):
            data=self.status()
        after=self.fishing()
        self.assertEqual([x['reward'][1] for x in after['shop']],ids)
        self.assertEqual(after['purchases'],s['purchases'])
        self.assertEqual(after['weekly_exchanges'],4)
        self.assertEqual(self.b.profile()['attachments'],before['attachments'])
        goods={x['type_id']:x for x in data['exchange_data'].values()}
        self.assertEqual(goods[1343]['count'],0)
        self.assertEqual(goods[1007]['count'],2)
        self.assertEqual(goods[5039]['cost_fish_count'],20)
        self.assertEqual(self.req(1208,count=1,type_id=1343)[0][0],55)
        self.ok(self.req(1208,count=1,type_id=1007))
        self.assertEqual(self.count(1027),9995)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.status();self.assertEqual(self.fishing()['purchases'],{'1343':3,'1007':2})

    def recycle_mails(self):
        return [m for key,m in self.b.profile().get('welfare',{}).get('mails',{}).items() if key.startswith('fish-recycle-')]

    def test_weekly_mail_claim_restart_rollback_and_locked_stacks(self):
        data=self.status();role=self.b.profile()
        for count,extra in [(7,{}),(5,{'is_lock':1}),(3,{'owner_id':99})]:
            role['attachments'].append(dict(id=formation.new_id(role),attach_type=5,type_id=1027,level=1,count=count,**extra))
        self.b.save(role);peaches=self.count(1001);deadline=data['next_weekly_refresh']
        with patch('network_redirect.backend.time.time',return_value=deadline):
            events=self.req(1205,flag=0);self.ok(events)
            self.assertIn(13,[e for e,d in events])
            self.assertEqual(self.count(1027),0);self.assertEqual(self.count(1001),peaches)
            mail=self.recycle_mails()[0]
            self.assertEqual(mail['prizes'],[[5,1001,15,1]])
            self.assertIn('剩余锦鲤15条',mail['mail_body'])
            self.assertIn('1条锦鲤兑换1个蟠桃',mail['mail_body'])
            self.assertTrue(mail['no_expiry'])
            self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
            self.status();self.assertEqual(len(self.recycle_mails()),1)
            self.ok(self.req(1102,mail_id=mail['mail_id'],flag=0))
            self.ok(self.req(1103,mail_id=mail['mail_id']))
            self.assertEqual(self.count(1001),peaches+15)
            self.assertEqual(self.req(1103,mail_id=mail['mail_id'])[0][0],55)
        self.status();self.assertEqual(len(self.recycle_mails()),1)
        with patch('network_redirect.backend.time.time',return_value=deadline+28*86400):self.status()
        self.assertEqual(len(self.recycle_mails()),1);self.assertEqual(self.count(1001),peaches+15)

    def test_weekly_direct_draw_clears_old_only_and_failed_mail_is_atomic(self):
        data=self.status();self.rich();before=self.b.profile();deadline=data['next_weekly_refresh']
        with patch('network_redirect.backend.time.time',return_value=deadline), patch('network_redirect.system_mail.deliver',side_effect=formation.Rejected('邮件失败')):
            self.assertEqual(self.req(1208,count=10,type_id=0)[0][0],55)
            after=self.b.profile()
            for key in ('attachments','gold_coin','activity','welfare'):
                self.assertEqual(after.get(key),before.get(key))
        with patch('network_redirect.backend.time.time',return_value=deadline), patch.object(fish,'randbelow',return_value=0):
            self.ok(self.req(1208,count=10,type_id=0))
            self.assertEqual(self.count(1027),20)
            self.assertEqual(self.recycle_mails()[0]['prizes'],[[5,1001,10000,1]])
            self.assertEqual(self.fishing()['weekly_casts'],10)
            after=self.b.profile();self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
            self.assertEqual(after,self.b.profile())

    def test_weekly_heartbeat_recycles_without_open_panel(self):
        data=self.status();self.rich()
        with patch('network_redirect.backend.time.time',return_value=data['next_weekly_refresh']):
            responses=self.b.respond(encode(2999,{}),self.state)
            events=[login_fields(d['data']) for m,_,d in map(decode,responses) if m==2998 and d['id']==13]
            self.assertTrue(events)
            self.assertEqual(self.count(1027),0);self.assertEqual(len(self.recycle_mails()),1)
            self.b.respond(encode(2999,{}),self.state)
            self.assertEqual(len(self.recycle_mails()),1)

    def test_first_use_and_legacy_day_establish_correct_week(self):
        role=self.b.profile();role['activity'].setdefault('seasonal',{}).pop('fish',None)
        summon.add_item(role,1027,9)
        fish.state(role,NOW,self.b.activity_rules)
        self.assertFalse(any(k.startswith('fish-recycle-') for k in role.get('welfare',{}).get('mails',{})))
        old=role['activity']['seasonal']['fish'];old.pop('week')
        fish.state(role,NOW+7*86400,self.b.activity_rules)
        self.assertFalse(any(i['type_id']==1027 for i in role['attachments']))
        self.assertEqual(len([k for k in role['welfare']['mails'] if k.startswith('fish-recycle-')]),1)

    def test_login_snapshot_recycles_even_when_activity_disabled(self):
        data=self.status();self.rich()
        self.b.activity_rules['seasonal_games']['fish']['enabled']=False
        with patch('network_redirect.backend.time.time',return_value=data['next_weekly_refresh']):
            snapshot=self.b.snapshot()
            self.assertFalse(any(i['type_id']==1027 for i in snapshot['attachments']))
            self.assertEqual(len(self.recycle_mails()),1)
            events=[login_fields(d['data']) for m,_,d in map(decode,self.b.bootstrap()) if m==2998 and d['id']==13]
            self.assertTrue(events)
            self.assertEqual(len(self.recycle_mails()),1)
