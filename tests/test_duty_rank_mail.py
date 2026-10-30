"""Daily duty rewards through the native mailbox, using isolated account saves."""
import copy
from pathlib import Path
from unittest.mock import patch

from test_activity import ActivityCase, NOW
from network_redirect import activity_duty as duty, daily, welfare
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode, encode


class DutyRankMailTests(ActivityCase):
    def seed(self, dates=None, group=8):
        role = self.b.profile()
        today = duty.day(NOW, self.b.activity_rules)
        for date in dates if dates is not None else [today]:
            role['activity']['duty_meta']['records'][str(date)] = dict(
                stars=27, rounds=3, group=group)
        self.b.save(role)
        return today

    def mails(self):
        return {k: m for k, m in self.b.profile().get('welfare', {}).get('mails', {}).items()
                if k.startswith('duty-rank-')}

    def events(self, packets):
        return [(d['id'], login_fields(d['data'])) for mid, _, d in map(decode, packets) if mid == 2998]

    def assert_announced(self, events):
        mail_ids = {m['mail_id'] for m in self.mails().values()}
        self.assertTrue(mail_ids)
        self.assertTrue(any(event == 13 and mail_ids <= set(data.values()) for event, data in events))

    def test_activity_rollover_announces_mail_without_crediting_gold(self):
        today = self.seed()
        before = self.b.profile()['gold_coin']
        with patch('network_redirect.backend.time.time', return_value=NOW+86400):
            events = self.req(1049, query_type=4)
            self.ok(events); self.assert_announced(events)
            mail = self.mails()[f'duty-rank-{today}']
            self.assertEqual(mail['prizes'], [[11, 1, 700, 1]])
            self.assertIn('2026-10-24', mail['mail_body'])
            self.assertIn('8人组第1名', mail['mail_body'])
            self.assertFalse(mail['claimed'])
            self.assertTrue(mail['no_expiry']); self.assertIsNone(mail['expires_at'])
            self.assertEqual(self.b.profile()['gold_coin'], before)
            packet, replies = self.packet, self.replies
            self.assertEqual(self.b.respond(packet, self.state), replies)
            self.ok(self.req(1043, flag=1))
            self.assertEqual(len(self.mails()), 1)

    def test_heartbeat_announces_even_if_daily_hint_already_rolled_over(self):
        self.seed()
        with patch('network_redirect.backend.time.time', return_value=NOW+86400):
            role = self.b.profile(); daily.prepare(role, NOW+86400, self.b.daily_rules); self.b.save(role)
            packets = self.b.respond(encode(2999, {}), self.state)
            self.assert_announced(self.events(packets))
            before = self.mails()
            self.b.respond(encode(2999, {}), self.state)
            self.assertEqual(self.mails(), before)

    def test_bootstrap_delivers_all_played_days_and_reconnect_keeps_mail_ids(self):
        today = duty.day(NOW, self.b.activity_rules)
        self.seed([today-4, today-2, today])
        with patch('network_redirect.backend.time.time', return_value=NOW+7*86400):
            self.assert_announced(self.events(self.b.bootstrap()))
            before = self.mails()
            self.assertEqual(set(before), {f'duty-rank-{d}' for d in (today-4, today-2, today)})
            self.assertEqual(len({m['mail_id'] for m in before.values()}), 3)
            self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
            self.assert_announced(self.events(self.b.bootstrap(reconnect=True)))
            self.assertEqual(self.mails(), before)

    def test_native_read_claim_persist_replay_and_late_claim(self):
        self.seed()
        with patch('network_redirect.backend.time.time', return_value=NOW+86400):
            self.ok(self.req(1043, flag=1))
        mail = next(iter(self.mails().values()))
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        with patch('network_redirect.backend.time.time', return_value=NOW+365*86400):
            packets = self.b.respond(encode(1102, dict(serial_num=0, mail_id=mail['mail_id'], flag=0)), self.state)
            content = next(data for event, data in self.events(packets) if event == 14)
            self.assertEqual(content['attach_count'], 1)
            self.assertEqual(content['attach_list'][1]['attach_count'], 700)
            before = self.b.profile()['gold_coin']
            events = self.req(1103, mail_id=mail['mail_id'], flag=1); self.ok(events)
            self.assertTrue(any(event == 15 and data['result'] == 1 for event, data in events))
            self.assertEqual(self.b.profile()['gold_coin'], before+700)
            self.assertTrue(any(a['type'] == 8 and a['value'] == before+700
                for mid, _, data in self.decoded if mid == 1032 for a in data['attr_list']))
            self.assertEqual(self.b.respond(self.packet, self.state), self.replies)
            self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
            self.assertEqual(self.req(1103, mail_id=mail['mail_id'], flag=1)[0][0], 55)
            self.assertEqual(self.b.profile()['gold_coin'], before+700)
            content = next(data for event, data in self.req(1102, mail_id=mail['mail_id'], flag=0) if event == 14)
            self.assertEqual(content['attach_count'], 0)

    def test_claim_encoder_failure_keeps_attachment_claimable(self):
        self.seed()
        with patch('network_redirect.backend.time.time', return_value=NOW+86400):
            self.ok(self.req(1043, flag=1))
            mail = next(iter(self.mails().values()))
            before = self.b.profile()['gold_coin']
            with patch('network_redirect.backend.welfare_attributes', side_effect=ValueError('encoding')):
                self.assertEqual(self.req(1103, mail_id=mail['mail_id'], flag=1)[0][0], 55)
            self.assertEqual(self.b.profile()['gold_coin'], before)
            self.assertFalse(next(iter(self.mails().values()))['claimed'])
            self.ok(self.req(1103, mail_id=mail['mail_id'], flag=1))
            self.assertEqual(self.b.profile()['gold_coin'], before+700)

    def test_legacy_paid_dates_are_not_paid_again(self):
        today = self.seed()
        role = self.b.profile()
        role['activity']['duty_meta']['settled'][str(today)] = dict(group=8, rank=1, gold=700)
        role['gold_coin'] += 700
        self.b.save(role)
        with patch('network_redirect.backend.time.time', return_value=NOW+86400):
            self.ok(self.req(1043, flag=1))
        self.assertFalse(self.mails())
        self.assertEqual(self.b.profile()['gold_coin'], role['gold_coin'])

    def test_later_anniversary_mail_does_not_shadow_duty_attachment(self):
        self.seed()
        with patch('network_redirect.backend.time.time', return_value=NOW+86400):
            self.ok(self.req(1043, flag=1))
            role = self.b.profile(); state = role['welfare']
            mail = next(iter(self.mails().values()))
            rules = copy.deepcopy(self.b.welfare_rules)
            rules['order'] = list(set(rules['order']) | {34})
            state['charge_days'] = {'test': rules['anniversary']['min_rmb'] * rules['gold_per_rmb']}
            state['start'] = NOW+86400-rules['season_days']*86400
            welfare.prepare(role, NOW+86400, rules)
            self.assertNotEqual(state['mails']['anniversary']['mail_id'], mail['mail_id'])
            before = role['gold_coin']
            welfare.mail_request(role, 1103, dict(mail_id=mail['mail_id'], flag=1), NOW+86400, rules, state)
            self.assertEqual(role['gold_coin'], before+700)
            self.assertFalse(state['mails']['anniversary']['claimed'])

    def test_unplayed_and_unrewarded_dates_have_no_mail(self):
        today = self.seed(group=4)
        role = self.b.profile()
        peers = []
        for index in range(20):
            peer = copy.deepcopy(role); peer['register_account'] = f'peer-{index}'
            peer['activity']['duty_meta']['records'][str(today)]['stars'] = 100
            peers.append(peer)
        duty.prepare(role, NOW+86400, self.b.activity_rules, peers)
        self.assertEqual(role['activity']['duty_meta']['settled'][str(today)]['rank'], 21)
        self.assertFalse(any(k.startswith('duty-rank-') for k in role.get('welfare', {}).get('mails', {})))
        self.b.save(role)
        with patch('network_redirect.backend.time.time', return_value=NOW+3*86400):
            self.ok(self.req(1043, flag=1))
        self.assertFalse(self.mails())
