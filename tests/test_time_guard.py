import copy
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

from network_redirect import time_guard, activity, activity_babel, welfare, formation
from network_redirect.backend import Backend, login_fields
from network_redirect import game_clock
from tests.test_game_clock import Source, NOW


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)
        self.db = sqlite3.connect(self.path / 'game.sqlite3')
        self.addCleanup(self.db.close)
        self.db.execute('CREATE TABLE roles(account TEXT PRIMARY KEY, data TEXT)')
        self.guard = time_guard.Guard(self.db, self.path)
        self.role = {'level': 40, 'activity': {'babel': {'clock': NOW + 864000}}}
        self.db.execute('INSERT INTO roles VALUES (?,?)', ('a', json.dumps(self.role)))
        self.db.commit()

    def test_future_legacy_kept_and_confirm_persists(self):
        original = copy.deepcopy(self.role)
        info = self.guard.load('a', self.role, NOW)
        self.assertEqual(info['blocked'], [])
        self.assertEqual(original['activity'], self.role['activity'])
        self.guard.confirm('a', ['activity_babel'], '复核记录：重复发放流水1和2', NOW)
        restored = json.loads(self.db.execute('SELECT data FROM roles').fetchone()[0])
        guard = time_guard.Guard(self.db, self.path)
        guard.load('a', restored, NOW + 86400)
        self.assertTrue(time_guard.blocked(restored, 'activity_babel'))
        self.assertFalse(time_guard.blocked(restored, 'activity_hunt'))
        self.assertEqual(restored['time_guard']['since'], NOW)
        other = copy.deepcopy(original)
        guard.load('b', other, NOW)
        self.assertFalse(time_guard.blocked(other, 'activity_babel'))

    def test_sealed_time_mutation_quarantines_before_gameplay(self):
        self.guard.load('a', self.role, NOW)
        self.role['activity']['babel']['clock'] += 100
        self.guard.load('a', self.role, NOW + 1)
        self.assertEqual(self.role['time_guard']['blocked'], ['*'])
        self.role['time_guard'] = {'blocked': []}
        self.guard.load('a', self.role, NOW + 2)
        self.assertEqual(self.role['time_guard']['blocked'], ['*'])

    def test_forged_guard_record_and_normal_checkpoint(self):
        self.guard.load('a', self.role, NOW)
        self.role['activity']['babel']['clock'] += 100
        with self.db:
            self.guard.checkpoint('a', self.role)
        self.guard.load('a', self.role, NOW)
        self.assertFalse(self.role['time_guard']['blocked'])
        with self.db:
            self.db.execute("UPDATE time_guard SET data='{}'")
        self.guard.load('a', self.role, NOW)
        self.assertEqual(self.role['time_guard']['blocked'], ['*'])

    def test_blocked_tower_no_recovery_week_reset_or_mail(self):
        source = Source()
        clock = game_clock.GameClock(self.path, source=source)
        self.addCleanup(clock.close)
        backend = Backend(self.path, 0, lambda *a, **k: None, account='player', clock=clock)
        self.addCleanup(backend.close)
        role = backend.profile()
        role['level'] = 40
        activity.prepare(role, NOW, backend.activity_rules, [])
        activity_babel.state(role, NOW, backend.activity_rules)
        role['activity']['babel'].update(energy=0, life=20)
        backend.save(role)
        backend.time_guard.confirm('player', ['activity_babel'], '人工复核异常获利流水', NOW)
        role = backend.profile()
        original = copy.deepcopy(role)
        activity_babel.state(role, NOW + 14 * 86400, backend.activity_rules)
        self.assertEqual(role, original)
        with self.assertRaisesRegex(formation.Rejected, 'TIME-001'):
            activity.settle(role, 1353, {'op': 1}, NOW, backend.activity_rules,
                            backend.journey_rules, backend.formation_rules, login_fields)
        # Login and heartbeat-like shared maintenance cannot settle the tower.
        source.seconds += 14 * 86400
        backend.bootstrap()
        loaded = backend.profile()
        self.assertEqual(loaded['activity']['babel'], original['activity']['babel'])
        self.assertFalse(any(k.startswith('babel-') for k in loaded.get('welfare', {}).get('mails', {})))

    def test_clock_edit_restores_anchor_and_blocks_login_rewards(self):
        source = Source()
        clock = game_clock.GameClock(self.path, source=source)
        self.addCleanup(clock.close)
        backend = Backend(self.path, 0, lambda *a, **k: None, account='clock-test', clock=clock)
        self.addCleanup(backend.close)
        backend.bootstrap()
        from network_redirect import system_mail
        role = backend.profile()
        system_mail.deliver(role, 'operator-test', '测试', '正常奖励', [[12, 0, 10, 1]],
                            NOW, backend.welfare_rules, mail_id=800000999)
        backend.save(role)
        raw = json.loads(clock.db.execute('SELECT data FROM clock').fetchone()[0])
        raw['game'] += 365 * 86400
        with clock.db:
            clock.db.execute('UPDATE clock SET data=?', (json.dumps(raw),))
        self.assertEqual(clock.sample(), NOW)
        self.assertTrue(clock.quarantined)
        backend.bootstrap()
        self.assertEqual(backend.profile()['time_guard']['blocked'], ['*'])
        from network_redirect.protocol import encode, decode
        replies = backend.respond(encode(1353, dict(serial_num=901, id=1, data='{}')),
                                  {'authenticated': True})
        self.assertTrue(any(mid == 2998 and data['id'] == 55 and
                            'TIME-001' in login_fields(data['data'])['op_string']
                            for mid, _, data in map(decode, replies)))
        balance = backend.profile()['silver_coin']
        for serial in (902, 903):
            backend.respond(encode(1103, dict(serial_num=serial, mail_id=800000999)),
                            {'authenticated': True})
        self.assertEqual(backend.profile()['silver_coin'], balance + 10)
        heartbeat = backend.respond(encode(2999, {}), {'authenticated': True})
        self.assertEqual(decode(heartbeat[0])[0], 2999)
        source.wall_seconds += 100 * 86400
        source.seconds += 60
        self.assertEqual(clock.sample(), NOW + 60)

    def test_global_block_keeps_normal_item_grants_and_mail_receipt(self):
        from network_redirect import summon
        role = {'level': 1, 'silver_coin': 0, 'attachments': [], 'summon': {},
                'time_guard': {'blocked': ['*'], 'since': NOW}}
        summon.add_item(role, 20000, 7)
        self.assertEqual(sum(x['count'] for x in role['attachments']), 7)
        role['welfare'] = {'mails': {'operator-gift': dict(
            mail_id=2, claimed=False, prizes=[[12, 0, 10, 1]])}}
        welfare.mail_request(role, 1103, {'mail_id': 2}, NOW, {}, copy.deepcopy(role['welfare']))
        self.assertEqual(role['silver_coin'], 10)
        with self.assertRaises(formation.Rejected):
            welfare.mail_request(role, 1103, {'mail_id': 2}, NOW, {}, role['welfare'])

    def test_missing_clock_integrity_fails_closed(self):
        clock = game_clock.GameClock(self.path, source=Source())
        self.addCleanup(clock.close)
        with clock.db:
            clock.db.execute('DELETE FROM clock_integrity')
        with self.assertRaisesRegex(RuntimeError, '缺失'):
            clock.sample()

    def test_admin_preview_and_backed_up_apply(self):
        command = [sys.executable, '-m', 'network_redirect.time_guard_admin',
                   '--directory', str(self.path), '--account', 'a',
                   '--scope', 'activity_babel', '--evidence', '复核流水编号test-1']
        before = self.db.execute('SELECT data FROM roles').fetchone()[0]
        preview = json.loads(subprocess.check_output(command, text=True))
        self.assertFalse(preview['applied'])
        self.assertEqual(self.db.execute('SELECT data FROM roles').fetchone()[0], before)
        result = json.loads(subprocess.check_output(command + ['--apply'], text=True))
        self.assertTrue(result['applied'])
        with sqlite3.connect(Path(result['backup']) / 'game.sqlite3') as backup:
            self.assertEqual(backup.execute('SELECT data FROM roles').fetchone()[0], before)
        self.assertEqual(result['result']['blocked'], ['activity_babel'])

    def test_related_mail_rejected_normal_mail_allowed(self):
        role = {'level': 1, 'silver_coin': 0, 'time_guard': {
            'blocked': ['activity_babel'], 'since': NOW}}
        mails = {'babel-rank-1': dict(mail_id=1, claimed=False, prizes=[[12, 0, 10, 1]]),
                 'operator-gift': dict(mail_id=2, claimed=False, prizes=[[12, 0, 10, 1]])}
        role['welfare'] = {'mails': mails}
        with self.assertRaisesRegex(formation.Rejected, 'TIME-001'):
            welfare.mail_request(role, 1103, {'mail_id': 1}, NOW, {}, role['welfare'])
        welfare.mail_request(role, 1103, {'mail_id': 2}, NOW, {}, role['welfare'])
        self.assertEqual(role['silver_coin'], 10)
        self.assertTrue(mails['operator-gift']['claimed'])
        self.assertFalse(mails['babel-rank-1']['claimed'])


if __name__ == '__main__':
    unittest.main()
