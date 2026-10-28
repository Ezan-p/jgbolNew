import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from network_redirect.backend import Backend, login_fields
from network_redirect import new_role_guide as guide
from network_redirect.protocol import encode, decode


class NewRoleGuideTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.backend = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None, account='new-guide')
        self.serial = 1

    def tearDown(self):
        self.backend.close()
        self.tmp.cleanup()

    def send(self, stage, name='', head_type=0, serial=None):
        serial = self.serial if serial is None else serial
        self.serial += 1
        packet = encode(1204, dict(serial_num=serial, stage=stage, name=name, head_type=head_type))
        replies = self.backend.respond(packet, {'authenticated': True})
        return packet, replies

    def step(self, stage, **kwargs):
        packet, replies = self.send(stage, **kwargs)
        decoded = [decode(p) for p in replies]
        errors = [r[2] for r in decoded if r[0] == 2998 and r[2]['id'] == 55]
        self.assertFalse(errors, errors)
        self.assertTrue(guide.done(self.backend.profile(), stage))
        return decoded

    def test_full_native_protocol_flow_and_replays(self):
        role = self.backend.profile()
        self.assertEqual(role['guide_progress'], 0)
        self.assertEqual(role['corteges'], [])
        self.step(1, name='新手行者', head_type=101)
        self.assertEqual(self.backend.profile()['guide_progress'], 2)
        self.step(2, name='1')
        for stage in range(3, 14):
            role = self.backend.profile()
            kwargs = {}
            if stage == 6:
                kwargs['name'] = str(int(role['corteges'][1]['id']))
            if stage == 9:
                kwargs['name'] = str(int(next(i['id'] for i in role['attachments'] if i['type_id'] == 2041)))
            replies = self.step(stage, **kwargs)
            if stage in guide.GATES:
                battle = next(r[2] for r in replies if r[0] == 1027)
                self.assertEqual(battle['fight_type'], 7)
                self.assertEqual(battle['guide_stage'], stage)
                self.assertGreater(battle['fight_round'], 0)
                self.assertEqual(battle['final_result'], 4 if stage == 4 else 3)
            if stage == 5:
                before = copy.deepcopy(self.backend.profile())
                self.send(5)  # A new serial must never grant a second copy.
                self.assertEqual(self.backend.profile(), before)
        self.assertEqual(self.backend.profile()['guide_progress'], 0x3ffe)
        self.assertEqual(len(self.backend.profile()['corteges']), 2)
        self.assertEqual(self.backend.profile()['gold_coin'], 20)
        for stage in range(21, 31):
            self.step(stage, serial=0)  # Original activity entry sends can be unnumbered.
        self.backend.close()
        self.backend = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None, account='new-guide')
        role = self.backend.profile()
        self.assertTrue(guide.done(role, 13))
        self.assertTrue(guide.done(role, 30))
        self.assertEqual(role['role_name'], '新手行者')

    def test_invalid_order_name_and_exact_replay(self):
        before = self.backend.profile()
        self.send(2, name='1')
        self.assertEqual(self.backend.profile(), before)
        self.send(1, name='a', head_type=101)
        self.assertFalse(guide.done(self.backend.profile(), 1))
        packet, replies = self.send(1, name='测试行者', head_type=101)
        self.assertEqual(replies, self.backend.respond(packet, {'authenticated': True}))
        event = next(login_fields(decode(p)[2]['data']) for p in replies
                     if decode(p)[0] == 2998 and decode(p)[2]['id'] == 35)
        self.assertNotIn('result', event)
        self.assertEqual(event['new_name'], '测试行者')
        self.send(2, name='999')
        self.assertEqual(self.backend.profile()['corteges'], [])
        self.step(2, name='2')
        self.assertEqual(self.backend.profile()['corteges'][0]['type'], 4053)

    def test_fresh_login_snapshot_and_restart_each_stage(self):
        snapshot = next(decode(p)[2] for p in self.backend.bootstrap() if decode(p)[0] == 1017)
        self.assertEqual(snapshot['guide_progress'], 0)
        self.step(1, name='断线行者', head_type=201)
        self.step(2, name='1')
        for stage in range(3, 14):
            self.backend.close()
            self.backend = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None, account='new-guide')
            snapshot = next(decode(p)[2] for p in self.backend.bootstrap(True) if decode(p)[0] == 1017)
            self.assertEqual(snapshot['guide_progress'], (1 << stage) - 2)
            role = self.backend.profile()
            name = (str(int(role['corteges'][1]['id'])) if stage == 6 else
                    str(int(next(i['id'] for i in role['attachments'] if i['type_id'] == 2041))) if stage == 9 else '')
            self.step(stage, name=name)

    def test_encoding_failure_rolls_back_selection(self):
        self.step(1, name='回滚行者', head_type=101)
        before = self.backend.profile()
        with patch.object(self.backend, 'inventory', side_effect=ValueError('encode failure')):
            self.send(2, name='1')
        self.assertEqual(self.backend.profile(), before)
        self.step(2, name='1')

    def test_foreign_object_cannot_complete_formation(self):
        self.step(1, name='校验行者', head_type=101)
        self.step(2, name='1')
        for stage in (3, 4, 5):
            self.step(stage)
        before = self.backend.profile()
        self.send(6, name='99999999')
        self.assertEqual(self.backend.profile(), before)

    def test_existing_save_is_preserved_and_new_accounts_isolated(self):
        role = self.backend.profile()
        role.update(guide_progress=guide.LEGACY_COMPLETE, level=12, gold_coin=123)
        self.backend.save(role)
        self.send(1, name='不能覆盖', head_type=101)
        self.assertEqual(self.backend.profile()['gold_coin'], 123)
        self.assertEqual(self.backend.profile()['guide_progress'], guide.LEGACY_COMPLETE)
        self.assertEqual(self.backend.profile('another-new')['guide_progress'], 0)
        self.assertEqual(self.backend.profile('local-player')['corteges'][0]['type'], 5004)


if __name__ == '__main__':
    unittest.main()
