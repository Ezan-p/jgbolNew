"""Hunting weekly settlement and native mailbox delivery on temporary saves."""
import copy
from pathlib import Path
from unittest.mock import patch

from tests.test_activity import ActivityCase
from network_redirect import activity, activity_land_rewards as rewards
from network_redirect import activity_land_npc as npc, summon, daily
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode, encode


class LandWeekMailTests(ActivityCase):
    def seed(self, soul=999999):
        self.ok(self.req(1302,id=1,data='{}'))
        role=self.b.profile();s=role['activity']['land']
        s['week_soul']=soul;self.b.save(role)
        self.week=s['week']
        self.monday=((self.week+1)*7+4)*86400-self.b.activity_rules['timezone_offset_hours']*3600
        return role

    def mails(self):
        return {k:m for k,m in self.b.profile()['welfare'].get('mails',{}).items()
                if k.startswith('land-week-')}

    def events(self, packets):
        return [(d['id'],login_fields(d['data'])) for mid,_,d in map(decode,packets) if mid==2998]

    def assert_announced(self, events):
        ids={m['mail_id'] for m in self.mails().values()}
        self.assertTrue(ids)
        self.assertTrue(any(event==13 and ids<=set(data.values()) for event,data in events))

    def test_bootstrap_settles_without_entering_land_and_reconnect_does_not_repeat(self):
        before=self.seed()
        with patch('network_redirect.backend.time.time',return_value=self.monday):
            self.assert_announced(self.events(self.b.bootstrap()))
            mails=self.mails();self.assertEqual(len(mails),1)
            mail=mails[f'land-week-{self.week}']
            self.assertEqual(mail['prizes'],[[5,10000,1200,1],[5,1325,50,1],
                                              [5,10001,12,1],[11,1,500,1]])
            self.assertFalse(mail['claimed']);self.assertTrue(mail['no_expiry'])
            self.assertEqual(self.b.profile()['gold_coin'],before['gold_coin'])
            self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
            self.assert_announced(self.events(self.b.bootstrap(reconnect=True)))
            self.assertEqual(self.mails(),mails)

    def test_heartbeat_boundary_and_last_sunday_tower_income(self):
        self.seed(0)
        sunday=self.monday-600
        with patch('network_redirect.backend.time.time',return_value=sunday):
            self.ok(self.req(1302,id=1,data='{}'))
            self.ok(self.req(1302,id=4,data=summon.lua(dict(flag=1,des_type=2,des_id=14))))
        with patch('network_redirect.backend.time.time',return_value=self.monday-1):
            self.b.respond(encode(2999,{}),self.state)
            self.assertFalse(self.mails())
        with patch('network_redirect.backend.time.time',return_value=self.monday+600):
            # Other activities may already have advanced their daily marker.
            role=self.b.profile();role['activity']['rank_day']=activity.day(self.monday,self.b.activity_rules)
            role['activity']['rank_reward_version']=2
            daily.prepare(role,self.monday+600,self.b.daily_rules);self.b.save(role)
            self.assert_announced(self.events(self.b.respond(encode(2999,{}),self.state)))
            s=self.b.profile()['activity']['land']
            self.assertEqual(s['last_week_result']['soul'],100)
            self.assertEqual(s['week_soul'],0)
            self.assertEqual(s['soul_count'],100)
            self.assertEqual(s['last_week_result']['rank'],61)
            mails=self.mails()
            self.b.respond(encode(2999,{}),self.state)
            self.assertEqual(self.mails(),mails)

    def test_all_reward_tiers_native_read_claim_and_duplicate(self):
        original=self.seed()
        tiers=((1,1200,50,12,500),(3,900,38,9,350),(6,750,32,8,250),
               (10,600,25,6,200),(20,400,20,4,100),(50,200,15,2,80),(61,100,10,0,50))
        for rank,stone,chest,shard,gold in tiers:
            with self.subTest(rank=rank), patch('network_redirect.backend.time.time',return_value=self.monday):
                self.b.save(copy.deepcopy(original))
                with patch.object(npc,'ranking',return_value=([],dict(order=rank))):
                    events=self.req(1302,id=1,data='{}');self.ok(events);self.assert_announced(events)
                mail=next(iter(self.mails().values()))
                read=self.b.respond(encode(1102,dict(serial_num=0,mail_id=mail['mail_id'],flag=0)),self.state)
                detail=next(data for event,data in self.events(read) if event==14)
                self.assertEqual(detail['attach_count'],4 if shard else 3)
                before=self.b.profile()
                result=self.req(1103,mail_id=mail['mail_id'],flag=1);self.ok(result)
                self.assertTrue(any(e==15 and d['result']==1 for e,d in result))
                after=self.b.profile()
                self.assertEqual(after['gold_coin']-before['gold_coin'],gold)
                for tid,count in ((10000,stone),(1325,chest),(10001,shard)):
                    total=lambda r:sum(x['count'] for x in r['attachments'] if x['attach_type']==5 and x['type_id']==tid)
                    self.assertEqual(total(after)-total(before),count)
                self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
                self.assertEqual(self.b.profile(),after)
                self.assertEqual(self.req(1103,mail_id=mail['mail_id'],flag=1)[0][0],55)
                self.assertEqual(self.b.profile(),after)
                read=self.req(1102,mail_id=mail['mail_id'],flag=0)
                self.assertEqual(next(d for e,d in read if e==14)['attach_count'],0)

    def test_claim_failure_rolls_back_and_late_claim_survives_restart(self):
        self.seed()
        with patch('network_redirect.backend.time.time',return_value=self.monday):
            self.ok(self.req(1302,id=1,data='{}'))
            mail=next(iter(self.mails().values()));before=self.b.profile()
            with patch('network_redirect.backend.welfare_attributes',side_effect=ValueError('encoding')):
                self.assertEqual(self.req(1103,mail_id=mail['mail_id'],flag=1)[0][0],55)
            self.assertEqual(self.b.profile(),before)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        with patch('network_redirect.backend.time.time',return_value=self.monday+365*86400):
            self.ok(self.req(1103,mail_id=mail['mail_id'],flag=1))
            self.assertEqual(self.b.profile()['gold_coin'],before['gold_coin']+500)
            self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
            self.assertEqual(self.req(1103,mail_id=mail['mail_id'],flag=1)[0][0],55)
            self.assertEqual(len(self.mails()),1)

    def test_unplayed_weeks_are_not_rewarded_and_spending_does_not_reduce_rank(self):
        role=self.seed(0)
        with patch('network_redirect.backend.time.time',return_value=self.monday):
            self.b.bootstrap();self.assertFalse(self.mails())
        s=role['activity']['land'];rewards.gain(s,999999)
        activity.spend(s,'soul_count',s['soul_count']);self.b.save(role)
        with patch('network_redirect.backend.time.time',return_value=self.monday+28*86400):
            self.b.bootstrap()
            self.assertEqual(set(self.mails()),{f'land-week-{self.week}'})
            self.assertEqual(self.b.profile()['activity']['land']['last_week_result']['rank'],1)
            self.b.bootstrap();self.assertEqual(len(self.mails()),1)
