"""Real protocol, local randomness, migration, weekly mail and restart coverage."""
import copy
import json
from collections import Counter
from pathlib import Path
from unittest.mock import patch
from test_activity import ActivityCase, NOW
from network_redirect import activity, activity_tangwang as tw, formation, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode


class TangwangTests(ActivityCase):
    def status(self):
        out=self.req(1205,flag=0);self.ok(out)
        return next(d['tangwang_info'] for e,d in out if e==47)

    def cards(self):
        return [i for i in self.b.profile()['attachments'] if tw.is_card(i)]

    def twstate(self):
        return self.b.profile()['activity']['seasonal']['tangwang']

    def count(self,tid):
        return sum(i['count'] for i in self.b.profile()['attachments'] if i['attach_type']==5 and i['type_id']==tid)

    def put(self,levels):
        role=self.b.profile();ids=[tw.card(role,v)['id'] for v in levels];self.b.save(role)
        return ids

    def exchange(self,ids):
        return self.req(1213,count=len(ids),card_list=[dict(id=i) for i in ids])

    def mails(self):
        return [m for k,m in self.b.profile().get('welfare',{}).get('mails',{}).items() if k.startswith('tangwang-recycle-')]

    def test_daily_random_gift_no_repeat_restart_or_clock_rollback(self):
        with patch.object(tw,'randbelow',side_effect=[0,20,40,52]) as rng:
            status=self.status();self.assertEqual(rng.call_count,4)
        self.assertEqual([c['level'] for c in self.cards()],[1,2,3,4])
        self.assertEqual(self.twstate()['weekly_cards'],4)
        self.status();self.assertEqual(len(self.cards()),4)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        with patch.object(tw,'randbelow',side_effect=AssertionError('rerolled')):self.status()
        with patch('network_redirect.backend.time.time',return_value=status['next_daily_refresh']):self.status()
        self.assertEqual(len(self.cards()),8);self.status();self.assertEqual(len(self.cards()),8)

    def test_every_letter_and_reward_ticket_exact_weights(self):
        rules=tw.load_rules()
        pools=[(list(range(1,9)),rules['letter_weights'])]
        for p in rules['pools']:
            rows=p['rewards'];pools.append(([tuple(x['reward']) for x in rows],[x['weight'] for x in rows]))
        for values,weights in pools:
            actual=Counter()
            for ticket in range(sum(weights)):
                with patch.object(tw,'randbelow',return_value=ticket):actual[tw.draw(values,weights)]+=1
            self.assertEqual(actual,Counter(dict(zip(values,weights))))
            self.assertEqual(sum(weights),100)

    def test_all_pool_entries_credit_one_reward_and_consume_four(self):
        self.status()
        for index,pool in enumerate(self.b.activity_rules['tangwang_rules']['pools']):
            ticket=0
            for row in pool['rewards']:
                ids=self.put(tw.COMBINATIONS[index] if index<3 else [1,1,1,1])
                before=self.b.profile();count=len(self.cards())
                with patch.object(tw,'randbelow',return_value=ticket):out=self.exchange(ids)
                self.ok(out);data=next(d for e,d in out if e==90)
                self.assertEqual(data['pool_index'],index+1)
                self.assertEqual(len(data['prize_list']),1)
                self.assertEqual(data['prize_list'][1],activity.prize_spec(row['reward']))
                typ,tid,n,_=row['reward'];after=self.b.profile()
                if typ in (11,12):
                    key='gold_coin' if typ==11 else 'silver_coin';self.assertEqual(after[key]-before[key],n)
                else:
                    self.assertEqual(self.count(tid)-sum(i['count'] for i in before['attachments'] if i['attach_type']==5 and i['type_id']==tid),n)
                    if tid in (1090,1091,1092):
                        old_ids={i['id'] for i in before['attachments']}
                        stones=[i for i in after['attachments'] if i['type_id']==tid and i['id'] not in old_ids]
                        self.assertEqual(len(stones),n)
                        self.assertEqual(len({i['id'] for i in stones}),n)
                        self.assertTrue(all(i['level']==1 and i['count']==1 for i in stones))
                self.assertEqual(len(self.cards()),count-4)
                ticket+=row['weight']

    def test_reordered_letters_fallback_and_duplicate_request_cached(self):
        self.status();ids=self.put([4,3,2,1])
        with patch.object(tw,'randbelow',return_value=99):out=self.exchange(ids)
        self.ok(out);self.assertEqual(next(d['pool_index'] for e,d in out if e==90),4)
        before=self.b.profile();reply=self.b.respond(self.packet,self.state_auth())
        self.assertEqual(reply,self.replies);self.assertEqual(before,self.b.profile())
        self.assertEqual(self.exchange(ids)[0][0],55);self.assertEqual(before,self.b.profile())

    def state_auth(self):return {'authenticated':True}

    def test_bad_selection_lock_owner_and_type_all_atomic(self):
        self.status();ids=self.put([1,2,3,4]);baseline=self.b.profile()
        for chosen in (ids[:3],ids+[ids[0]],[ids[0]]*4,ids[:3]+[99999999]):
            self.assertEqual(self.exchange(chosen)[0][0],55);self.assertEqual(baseline,self.b.profile())
        for key,value in [('is_lock',1),('owner_id',2),('equip_pos',1),('equip_order',1),('level',9),('type_id',1001),('count',0)]:
            role=copy.deepcopy(baseline);next(i for i in role['attachments'] if i['id']==ids[0])[key]=value
            self.b.save(role);before=self.b.profile()
            self.assertEqual(self.exchange(ids)[0][0],55);self.assertEqual(before,self.b.profile())

    def test_travel_30_percent_and_each_letter_conditional_probability(self):
        role=self.b.profile();r=self.b.activity_rules
        for ticket in range(100):
            with patch.object(tw,'randbelow',side_effect=[ticket,99] if ticket<30 else [ticket]):
                result=tw.travel_drop(role,NOW,r)
            self.assertEqual(bool(result),ticket<30)
            if result:self.assertEqual(result[0],activity.prize_spec([5,1094,1,8]))
        s=role['activity']['seasonal']['tangwang']
        self.assertEqual((s['weekly_travel_wins'],s['weekly_travel_cards']),(100,30))
        self.assertEqual(len([c for c in role['attachments'] if tw.is_card(c)]),30)

    def test_journey_win_sweep_and_defeat_hook(self):
        from network_redirect import journey
        self.status();r=self.b.profile();r['strength']=1000;self.b.save(r)
        with patch('network_redirect.journey.battle',return_value=(1,[],[])), patch.object(tw,'randbelow',return_value=0):
            out=self.req(1026,fight_type=1,des_type=1,des_id=101);self.ok(out)
        self.assertEqual(self.twstate()['weekly_travel_cards'],1)
        with patch('network_redirect.journey.battle',return_value=(0,[],[])), patch.object(tw,'randbelow',side_effect=AssertionError('defeat dropped card')):
            self.ok(self.req(1026,fight_type=1,des_type=1,des_id=101))
        self.assertEqual(self.twstate()['weekly_travel_cards'],1)
        with patch.object(tw,'randbelow',side_effect=[0,0]*3) as rng:
            self.ok(self.req(1061,tollgate_type=1,tollgate_id=101,sweep_count=3))
            self.assertEqual(rng.call_count,6)
        self.assertEqual(self.twstate()['weekly_travel_cards'],4)

    def test_week_boundary_locked_cards_mail_claim_and_restart(self):
        status=self.status();role=self.b.profile()
        for c in role['attachments']:
            if tw.is_card(c):c['is_lock']=1
        role['activity']['seasonal']['tangwang']['exchanges']=[3,2,1,4]
        self.b.save(role);peaches=self.count(1001);deadline=status['next_weekly_refresh']
        with patch('network_redirect.backend.time.time',return_value=deadline-1):self.status()
        count=self.count(1094)
        with patch('network_redirect.backend.time.time',return_value=deadline):
            self.status();self.assertEqual(self.count(1094),4)
            self.assertEqual(self.twstate()['exchanges'],[0]*4)
            self.assertEqual(self.twstate()['weekly_cards'],4)
            mail=self.mails()[0];self.assertEqual(mail['prizes'],[[5,1001,count,1]])
            self.assertTrue(mail['no_expiry']);self.assertIn('1枚金牌兑换1个蟠桃',mail['mail_body'])
            self.assertEqual(self.count(1001),peaches)
            self.ok(self.req(1103,mail_id=mail['mail_id']));self.assertEqual(self.count(1001),peaches+count)
            self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
            self.status();self.assertEqual(len(self.mails()),1)
            self.req(1103,mail_id=mail['mail_id']);self.assertEqual(self.count(1001),peaches+count)
        self.status();self.assertEqual(len(self.mails()),1);self.assertEqual(self.count(1094),4)

    def test_offline_many_weeks_only_recycles_actual_cards_once(self):
        status=self.status();count=self.count(1094)
        with patch('network_redirect.backend.time.time',return_value=status['next_weekly_refresh']+28*86400):
            self.status();self.status()
        self.assertEqual(len(self.mails()),1);self.assertEqual(self.mails()[0]['prizes'],[[5,1001,count,1]])
        self.assertEqual(self.count(1094),4)

    def test_heartbeat_without_panel_recycles_no_gift_and_refreshes_ui(self):
        status=self.status();deadline=status['next_weekly_refresh']
        with patch('network_redirect.backend.time.time',return_value=deadline):
            replies=self.b.respond(encode(2999,dict(time=deadline)),self.state_auth())
            decoded=list(map(decode,replies))
            events=[(d['id'],login_fields(d['data'])) for m,_,d in decoded if m==2998]
            inventory_index=next(i for i,(m,_,d) in enumerate(decoded) if m==1035)
            card_status_index=next(i for i,(m,_,d) in enumerate(decoded) if m==2998 and d['id']==47)
            self.assertLess(inventory_index,card_status_index)
            self.assertIn(13,[e for e,d in events]);self.assertIn(47,[e for e,d in events])
            self.assertTrue(next(d['tangwang_info']['daily_gift_pending'] for e,d in events if e==47))
            self.assertEqual(self.count(1094),0);self.assertEqual(self.twstate()['exchanges'],[0]*4)
            self.b.respond(encode(2999,dict(time=deadline)),self.state_auth())
        self.assertEqual(len(self.mails()),1)

    def test_empty_week_no_mail_and_stacked_cards_recycle_by_count(self):
        role=self.b.profile();r=self.b.activity_rules['tangwang_rules']
        deadline=tw.payload(self.twstate(),r,True)['next_weekly_refresh']
        tw.state(role,deadline,r)
        self.assertFalse(any(k.startswith('tangwang-recycle-') for k in role.get('welfare',{}).get('mails',{})))
        item=tw.card(role,1);item.update(count=7,is_lock=1)
        tw.card(role,8)
        tw.state(role,deadline+7*86400,r)
        mail=next(m for k,m in role['welfare']['mails'].items() if k.startswith('tangwang-recycle-'))
        self.assertEqual(mail['prizes'],[[5,1001,8,1]])
        self.assertFalse(any(tw.is_card(i) for i in role['attachments']))

    def test_daily_gift_after_heartbeat_snapshot(self):
        status=self.status();deadline=status['next_daily_refresh']
        with patch('network_redirect.backend.time.time',return_value=deadline):
            self.b.respond(encode(2999,dict(time=deadline)),self.state_auth())
            self.assertEqual(self.count(1094),4)
            r=self.b.activity_rules['tangwang_rules']
            self.assertTrue(tw.payload(self.twstate(),r,True)['daily_gift_pending'])
            self.assertFalse(self.status()['daily_gift_pending'])
            self.assertEqual(self.count(1094),8)

    def test_expired_ids_rejected_and_failed_mail_atomic_retry(self):
        status=self.status();ids=self.put([1,2,3,4]);baseline=self.b.profile()
        with patch('network_redirect.backend.time.time',return_value=status['next_weekly_refresh']):
            baseline=self.b.profile()  # Unrelated daily profile migration precedes activity transactions.
            self.assertEqual(self.exchange(ids)[0][0],55);self.assertEqual(baseline,self.b.profile())
            with patch('network_redirect.system_mail.deliver',side_effect=formation.Rejected('mail unavailable')):
                self.assertEqual(self.req(1205,flag=0)[0][0],55);self.assertEqual(baseline,self.b.profile())
            self.status();self.assertEqual(len(self.mails()),1)
            self.assertEqual(self.exchange(ids)[0][0],55)

    def test_first_new_week_travel_preserves_only_new_card(self):
        status=self.status();role=self.b.profile();old=self.count(1094)
        with patch.object(tw,'randbelow',side_effect=[0,99]):
            tw.travel_drop(role,status['next_weekly_refresh'],self.b.activity_rules)
        self.assertEqual([c['level'] for c in role['attachments'] if tw.is_card(c)],[8])
        self.assertEqual(role['activity']['seasonal']['tangwang']['weekly_travel_cards'],1)
        mails=role['welfare']['mails'];mail=next(v for k,v in mails.items() if k.startswith('tangwang-recycle-'))
        self.assertEqual(mail['prizes'],[[5,1001,old,1]])

    def test_legacy_letters_migrate_once_and_old_week_recycles(self):
        for old in (False,True):
            role=self.b.profile();role['activity']['seasonal'].pop('tangwang',None)
            role['attachments']=[i for i in role['attachments'] if not tw.is_card(i)]
            for lv in range(1,11):
                role['attachments'].append(dict(id=formation.new_id(role),attach_type=5,type_id=1094,level=lv,count=1))
            role['activity']['day']=activity.day(NOW-7*86400 if old else NOW,self.b.activity_rules)
            role['activity']['seasonal']['spring']={'day':role['activity']['day']}
            s=tw.state(role,NOW,self.b.activity_rules['tangwang_rules'])
            cards=[i['level'] for i in role['attachments'] if tw.is_card(i)]
            self.assertEqual(cards,[] if old else list(tw.LEGACY_LEVELS.values()))
            before=copy.deepcopy(role);tw.state(role,NOW,self.b.activity_rules['tangwang_rules']);self.assertEqual(role,before)
            if old:self.assertEqual(s['last_recycle']['cards'],10)

    def test_permanent_ignores_window_and_disabled_rejects_without_grants(self):
        cfg=self.b.activity_rules['seasonal_games']['spring_cards'];cfg['end_time']=NOW-1
        self.assertTrue(self.status()['local_enabled']);ids=self.put([1,2,3,4])
        self.ok(self.exchange(ids));cfg['enabled']=False
        before=self.count(1094)
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):self.assertFalse(self.status()['local_enabled'])
        self.assertEqual(self.count(1094),before)
        baseline=self.b.profile();self.assertEqual(self.exchange(self.put([1,2,3,4]))[0][0],55)
        with patch.object(tw,'randbelow',side_effect=AssertionError('disabled draw')):
            self.assertEqual(tw.travel_drop(baseline,NOW,self.b.activity_rules),[])

    def test_bad_config_rejected_and_client_source_included(self):
        rules=tw.load_rules();path=Path(self.tmp.name)/'rules.json'
        for key,value in [('daily_cards',True),('letter_weights',[1]*7),('travel_drop_percent',101),('letters',list('鸡年大吉'))]:
            invalid=copy.deepcopy(rules);invalid[key]=value;path.write_text(json.dumps(invalid))
            with self.assertRaises(formation.Rejected):tw.load_rules(path)
        source=(Path(__file__).resolve().parents[1]/'network_redirect/summon.py').read_text()
        self.assertIn('tangwang_client.lua',source)
