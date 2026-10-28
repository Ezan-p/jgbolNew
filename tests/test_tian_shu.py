"""Novice book wire integration, real settlement triggers and restart receipts."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from network_redirect import tian_shu as ts, summon, formation, activity, journey
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode
from tests.test_activity import ActivityCase, NOW


class TianShuTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.serial = 0
        self.addCleanup(self.tmp.cleanup)
        self.addCleanup(lambda: self.b.close())

    def send(self, stage, serial=None):
        self.serial += 1
        packet = encode(1201, dict(serial_num=self.serial if serial is None else serial, flag=4, id=stage))
        replies = self.b.respond(packet, {'authenticated': True})
        events = [(d['id'], login_fields(d['data'])) for m, _, d in map(decode, replies) if m == 2998]
        return packet, replies, events

    def ready(self):
        role = self.b.profile()
        role['task_progress'] = sum(1 << s for s in ts.ORDER)
        self.b.save(role)
        return role

    def test_bootstrap_configuration_and_bit_layout(self):
        packets = list(map(decode, self.b.bootstrap()))
        cfg = next(login_fields(d['data']) for m, _, d in packets if m == 2998 and d['id'] == 80)
        self.assertEqual(set(cfg[2]), set(ts.ORDER))
        self.assertEqual(cfg[2][1][1]['attach_count'], 20)
        self.assertEqual(cfg[2][7][1]['attach_count'], 100)
        self.assertEqual(cfg[2][13][1]['attach_type'], 3019)
        self.assertEqual(cfg[2][12][1]['attach_count'], 50)
        self.assertFalse(ts.has(self.b.profile(), 'task_prize', 1))
        self.assertFalse(ts.has(self.b.profile(), 'task_progress', 1))

    def test_full_order_rewards_restart_and_duplicate(self):
        self.ready()
        start = self.b.profile()['gold_coin']
        for stage in ts.ORDER:
            packet, replies, events = self.send(stage)
            self.assertNotIn(55, dict(events), events)
            self.assertEqual(dict(events)[57]['task_stage'], stage)
            self.assertEqual(replies, self.b.respond(packet, {'authenticated': True}))
            role = self.b.profile()
            self.assertTrue(ts.has(role, 'task_prize', stage))
            self.assertIn(80, dict(events))
            self.b.close()
            self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
            _, _, duplicate = self.send(stage)
            self.assertIn(55, dict(duplicate))
            self.assertEqual(role, self.b.profile())
        role = self.b.profile()
        self.assertEqual(role['gold_coin'] - start, 750)
        self.assertEqual(sum(i.get('count', 0) for i in role['attachments'] if i['type_id'] == 3019), 1)
        self.assertEqual(role['task_prize'], sum(1 << s for s in ts.ORDER))

    def test_early_unknown_out_of_order_and_serial_collision(self):
        for stage in (0, 99, 1, 10):
            before = self.b.profile()
            self.assertIn(55, dict(self.send(stage)[2]))
            self.assertEqual(before, self.b.profile())
        self.ready()
        self.assertIn(55, dict(self.send(10)[2]))
        packet, replies, _ = self.send(1)
        before = self.b.profile()
        self.assertIn(55, dict(self.send(10, serial=self.serial)[2]))
        self.assertEqual(before, self.b.profile())

    def test_level9_gold_does_not_change_month_card_or_charge(self):
        self.ready()
        role = self.b.profile()
        role['task_prize'] = sum(1 << s for s in ts.ORDER[:ts.ORDER.index(12)])
        role['month_card_time'] = NOW + 86400
        role['month_card_record'] = NOW
        self.b.save(role)
        old = self.b.profile()
        self.assertNotIn(55, dict(self.send(12)[2]))
        role = self.b.profile()
        self.assertEqual(role['gold_coin'], old['gold_coin'] + 50)
        for key in ('month_card_time', 'month_card_record', 'vip_level', 'charge_gold'):
            self.assertEqual(role.get(key, 0), old.get(key, 0))
        self.assertIn(55, dict(self.send(12)[2]))
        self.assertEqual(self.b.profile()['gold_coin'], old['gold_coin'] + 50)

    def test_migration_preserves_paid_tutorial_but_not_bootstrap_sentinel(self):
        for guide, expected in ((0x7fffffff, False), (0x3ffe, True), (0x1ffe, False)):
            role = self.b.profile()
            role.pop('tian_shu', None)
            role.update(task_progress=0, task_prize=0, guide_progress=guide)
            ts.refresh(role)
            self.assertEqual(ts.has(role, 'task_prize', 1), expected)

    def test_saved_facts_monotonic_and_no_fake_wins(self):
        role = self.b.profile()
        role.update(level=99, top_order=1)
        ts.refresh(role)
        for stage in (10, 2, 13, 12, 6):
            self.assertTrue(ts.has(role, 'task_progress', stage))
        for stage in (1, 3, 4, 5, 7, 8, 9, 11):
            self.assertFalse(ts.has(role, 'task_progress', stage), stage)
        role['journey']['gates']['1:103'] = dict(pass_star=3)
        ts.refresh(role)
        self.assertFalse(ts.has(role, 'task_progress', 1))
        role['journey']['gates']['1:105'] = dict(pass_star=3)
        role['rule_index'] = 1
        role.setdefault('activity', {})['duty_best'] = 10
        summon.add_item(role, 3019, 1)
        next(i for i in role['attachments'] if i['type_id'] == 3019)['level'] = 2
        role['attachments'].append(dict(id=999, attach_type=6, type_id=215, level=3))
        ts.refresh(role)
        for stage in (1, 3, 7, 8, 11):
            self.assertTrue(ts.has(role, 'task_progress', stage))
        mask = role['task_progress']
        role['attachments'] = [];role['rule_index'] = 0;role['activity']['duty_best'] = 0
        ts.refresh(role)
        self.assertEqual(mask, role['task_progress'])

    def test_party_cross_day_restart_and_clock_rollback(self):
        role = self.b.profile()
        role.setdefault('activity', {})['party'] = dict(day=100, count=15)
        for _ in range(3): ts.refresh(role)
        self.assertEqual(role['tian_shu']['party_count'], 15)
        role['activity']['party'] = dict(day=101, count=4)
        ts.refresh(role)
        self.assertFalse(ts.has(role, 'task_progress', 9))
        role['activity']['party'] = dict(day=100, count=15)
        ts.refresh(role)
        self.assertEqual(role['tian_shu']['party_count'], 19)
        role['activity']['party'] = dict(day=101, count=5)
        ts.refresh(role)
        self.assertTrue(ts.has(role, 'task_progress', 9))

    def test_tutorial_and_ordinary_claim_share_one_receipt(self):
        role = self.b.profile()
        role['guide_progress'] = 0x1ffe
        role['journey']['gates']['1:105'] = dict(pass_star=3, day_count=1, flush_count=0)
        self.b.save(role)
        before = self.b.profile()['gold_coin']
        self.assertNotIn(55, dict(self.send(1)[2]))
        replies = self.b.respond(encode(1204, dict(serial_num=90, stage=13)), {'authenticated': True})
        events = [(d['id'], login_fields(d['data'])) for m, _, d in map(decode, replies) if m == 2998]
        self.assertNotIn(55, dict(events), events)
        self.assertEqual(dict(events)[35]['stage'], 13)
        self.assertEqual(self.b.profile()['gold_coin'], before + 20)
        self.assertIn(55, dict(self.send(1)[2]))

    def test_reward_variant_and_encoding_failure_atomicity(self):
        self.assertEqual(ts.reward_specs(7, dict(reward_variant=2)), [(11, 1, 50, 1)])
        self.ready();before = self.b.profile()
        with patch('network_redirect.backend.recharge.attrs', side_effect=ValueError('bad wire')):
            self.assertIn(55, dict(self.send(1)[2]))
        self.assertEqual(self.b.profile(), before)


class TianShuGameplayTests(ActivityCase):
    def test_rank_and_practice_outcome_hooks(self):
        for ft, stage in ((2, 4), (4, 3), (3, 5), (12, 5)):
            role = self.b.profile();role['task_progress'] &= ~(1 << stage)
            for result in (0, 4, 6):
                ts.record_events(role, [encode(1027, dict(fight_type=ft, final_result=result))])
                self.assertFalse(ts.has(role, 'task_progress', stage))
            ts.record_events(role, [encode(1027, dict(fight_type=ft, final_result=3))])
            self.assertTrue(ts.has(role, 'task_progress', stage))
        out = self.req(1026, fight_type=4, des_type=1, des_id=0, des_value=0)
        self.ok(out)
        self.assertTrue(ts.has(self.b.profile(), 'task_progress', 3))
        self.assertIn(80, dict(out))

    def test_actual_party_fights_accumulate_across_days(self):
        for i in range(20):
            with patch('network_redirect.backend.time.time', return_value=NOW+(i//10)*86400):
                self.ok(self.req(1026, fight_type=6, des_value=0))
                role = self.b.profile()
                self.assertEqual(role['tian_shu']['party_count'], min(i+1, 20))
                self.assertEqual(ts.has(role, 'task_progress', 9), i == 19)
                self.assertEqual(self.b.respond(self.packet, self.state), self.replies)

    def test_rank_and_rape_requests_drive_real_book_state(self):
        self.ok(self.req(1021, flag=0))
        self.ok(self.req(1026, fight_type=2, des_type=2, des_value=99, des_id=930099))
        self.assertTrue(ts.has(self.b.profile(), 'task_progress', 4))
        with patch('network_redirect.activity_rape.roll_forms', return_value=[1,3,5]):
            self.ok(self.req(1029, flag=1))
        ident = int(next(iter(self.b.profile()['activity']['rape_boards'][0]['form_list']['2'])))
        with patch('network_redirect.activity_rape.journey.battle', return_value=(4, [], [])):
            self.ok(self.req(1026, fight_type=3, des_type=2, des_value=1, des_id=ident))
        self.assertFalse(ts.has(self.b.profile(), 'task_progress', 5))
        with patch('network_redirect.activity_rape.journey.battle', return_value=(1, [], [])):
            self.ok(self.req(1026, fight_type=3, des_type=2, des_value=1, des_id=ident))
        self.assertTrue(ts.has(self.b.profile(), 'task_progress', 5))
