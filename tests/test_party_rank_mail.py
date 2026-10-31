"""Party daily awards use permanent mail and the real protocol/transaction path."""
from pathlib import Path
from unittest.mock import patch

from tests.test_activity import ActivityCase, NOW
from network_redirect import activity_party as party
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode, encode


class PartyRankMailTests(ActivityCase):
    def seed(self):
        role=self.b.profile()
        role['activity']['party'].update(count=1,damage=100000000)
        self.b.save(role)
        return role['activity']['party']['day']

    def mails(self):
        return {k:m for k,m in self.b.profile().get('welfare',{}).get('mails',{}).items()
                if k.startswith('party-rank-')}

    def peaches(self,tid):
        return sum(a['count'] for a in self.b.profile()['attachments'] if a['type_id']==tid)

    def test_rank_boundaries(self):
        for rank,expected in ((0,[]),(1,[[5,1343,100,1]]),(5,[[5,1343,100,1]]),
                              (6,[[5,1343,50,1]]),(10,[[5,1343,50,1]]),
                              (11,[[5,1001,200,1]]),(50,[[5,1001,200,1]]),(51,[])):
            self.assertEqual(party.rewards('daily',rank),expected)
            role=self.b.profile();role['activity']['party'].update(count=1,damage=100000000)
            with patch.object(party,'placement',return_value=rank):
                party.finish_day(role,self.b.activity_rules,NOW+3600)
            mails={k:m for k,m in role.get('welfare',{}).get('mails',{}).items() if k.startswith('party-rank-')}
            self.assertEqual(len(mails),int(bool(expected)))
            if expected:self.assertEqual(next(iter(mails.values()))['prizes'],expected)

    def test_close_mail_announced_and_claimed_once_after_restart(self):
        day=self.seed();before=self.peaches(1343)
        with patch('network_redirect.backend.time.time',return_value=NOW+3599):
            self.ok(self.req(1049,query_type=1));self.assertFalse(self.mails())
        with patch('network_redirect.backend.time.time',return_value=NOW+3600):
            events=self.req(1049,query_type=2);self.ok(events)
            mail=self.mails()[f'party-rank-{day}']
            self.assertTrue(any(e==13 and mail['mail_id'] in data.values() for e,data in events))
            self.assertEqual(mail['prizes'],[[5,1343,100,1]])
            self.assertIn('2026-10-24',mail['mail_body']);self.assertIn('第1名',mail['mail_body'])
            self.assertTrue(mail['no_expiry']);self.assertIsNone(mail['expires_at'])
            self.assertFalse(mail['claimed']);self.assertEqual(self.peaches(1343),before)
            self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
            self.ok(self.req(1049,query_type=2));self.assertEqual(len(self.mails()),1)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        with patch('network_redirect.backend.time.time',return_value=NOW+365*86400):
            content=dict(self.req(1102,mail_id=mail['mail_id'],flag=0))[14]
            self.assertEqual(content['attach_list'][1]['attach_type'],1343)
            self.assertEqual(content['attach_list'][1]['attach_count'],100)
            self.ok(self.req(1103,mail_id=mail['mail_id'],flag=1))
            self.assertEqual(self.peaches(1343),before+100)
            self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
            self.assertEqual(self.req(1103,mail_id=mail['mail_id'],flag=1)[0][0],55)
            self.assertEqual(self.peaches(1343),before+100)
            self.assertEqual(len(self.mails()),1)

    def test_heartbeat_cross_day_and_backwards_clock_do_not_repeat(self):
        self.seed()
        for elapsed in (86400,2*86400,0):
            with patch('network_redirect.backend.time.time',return_value=NOW+elapsed):
                packets=self.b.respond(encode(2999,{}),self.state)
                self.assertEqual(len(self.mails()),1)
                if elapsed==86400:
                    events=[(d['id'],login_fields(d['data'])) for mid,_,d in map(decode,packets) if mid==2998]
                    self.assertIn(13,[e for e,_ in events])

    def test_bootstrap_settles_missed_day_and_no_unplayed_mail(self):
        with patch('network_redirect.backend.time.time',return_value=NOW+3600):
            self.b.bootstrap();self.assertFalse(self.mails())
        role=self.b.profile();role['activity']['party'].update(closed=False,count=1,damage=100000000)
        self.b.save(role)
        with patch('network_redirect.backend.time.time',return_value=NOW+7*86400):
            self.b.bootstrap();self.assertEqual(len(self.mails()),1)
            self.b.bootstrap(reconnect=True);self.assertEqual(len(self.mails()),1)

    def test_failed_delivery_rolls_back_and_retries(self):
        self.seed()
        with patch('network_redirect.backend.time.time',return_value=NOW+3600):
            before=self.b.profile()
            with patch('network_redirect.system_mail.deliver',side_effect=ValueError('mail encoding')):
                self.assertEqual(self.req(1049,query_type=2)[0][0],55)
            self.assertEqual(self.b.profile(),before)
            self.ok(self.req(1049,query_type=2));self.assertEqual(len(self.mails()),1)

    def test_failed_claim_keeps_mail_claimable(self):
        self.seed()
        with patch('network_redirect.backend.time.time',return_value=NOW+3600):
            self.ok(self.req(1049,query_type=2));mail=next(iter(self.mails().values()))
            before=self.peaches(1343)
            with patch('network_redirect.backend.welfare_attributes',side_effect=ValueError('encoding')):
                self.assertEqual(self.req(1103,mail_id=mail['mail_id'],flag=1)[0][0],55)
            self.assertEqual(self.peaches(1343),before)
            self.assertFalse(next(iter(self.mails().values()))['claimed'])
            self.ok(self.req(1103,mail_id=mail['mail_id'],flag=1))
            self.assertEqual(self.peaches(1343),before+100)

    def test_legacy_settled_rewards_are_not_reissued_as_mail(self):
        self.seed();role=self.b.profile();before=self.peaches(1343)
        role['activity']['party'].update(closed=True,daily_pending=[[5,1343,7,1]])
        self.b.save(role)
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            self.ok(self.req(1049,query_type=2))
            self.assertFalse(self.mails());self.assertEqual(self.peaches(1343),before+7)
            self.ok(self.req(1049,query_type=2));self.assertEqual(self.peaches(1343),before+7)
