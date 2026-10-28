import copy
import random
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from network_redirect.backend import Backend, login_fields
from network_redirect import new_role_guide as guide, progression, journey, combat, formation, tian_shu
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

    def test_full_legacy_schedule_flow_and_replays(self):
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
                self.assertIn(battle['final_result'], range(7) if stage == 4 else (1, 2, 3))
                lineup = next(r[2]['lineup'] for r in replies if r[0] == 1028)
                original = journey.fighters(role, journey.GATES[1][guide.GATES[stage]])
                self.assertEqual([r['des_hp'] for r in lineup if r.get('des_type')],
                                 [u['hp'] for u in original[1]])
                self.assertTrue(all(r['src_hp'] > 1 for r in lineup if r.get('src_type')))
            if stage == 5:
                before = copy.deepcopy(self.backend.profile())
                self.send(5)  # A new serial must never grant a second copy.
                self.assertEqual(self.backend.profile(), before)
        self.assertEqual(self.backend.profile()['guide_progress'], 0x3ffe)
        self.assertEqual(len(self.backend.profile()['corteges']), 2)
        self.assertEqual(self.backend.profile()['gold_coin'], 40)  # Level 2 plus task 1.
        for stage in range(21, 31):
            self.step(stage, serial=0)  # Original activity entry sends can be unnumbered.
        self.backend.close()
        self.backend = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None, account='new-guide')
        role = self.backend.profile()
        self.assertTrue(guide.done(role, 13))
        self.assertTrue(guide.done(role, 30))
        self.assertEqual(role['role_name'], '新手行者')

    def test_native_summon_after_first_fight_and_resume(self):
        self.step(1, name='召唤行者', head_type=101)
        self.step(2, name='2')
        self.step(3)
        # Existing stuck saves have only stages 1..3, and the original client
        # resumes them directly at summon as well.
        self.backend.close()
        self.backend = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None, account='new-guide')
        before = self.backend.profile()
        self.assertEqual(before['guide_progress'], 14)
        with patch.object(self.backend, 'inventory', side_effect=ValueError('encode failure')):
            self.send(5)
        self.assertEqual(self.backend.profile(), before)
        packet, replies = self.send(5)
        after = self.backend.profile()
        self.assertEqual(after['guide_progress'], 62)
        self.assertEqual([c['type'] for c in after['corteges']], [4053, 4061])
        # A skipped lesson must not run battle settlement or charge resources.
        for key in ('journey', 'strength', 'cur_exp', 'silver_coin', 'gold_coin'):
            self.assertEqual(after[key], before[key], key)
        events = [decode(p) for p in replies]
        self.assertFalse(any(mid in (1027, 1028) for mid, _, _ in events))
        event = next(login_fields(data['data']) for mid, _, data in events
                     if mid == 2998 and data['id'] == 35)
        self.assertEqual(event['stage'], 5)
        self.assertEqual(event['cortege_type'], 4061)
        self.assertEqual(self.backend.respond(packet, {'authenticated': True}), replies)
        self.send(5)
        self.send(4)
        self.assertEqual(self.backend.profile(), after)
        for stage in range(6, 14):
            self.backend.close()
            self.backend = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None, account='new-guide')
            snapshot = next(decode(p)[2] for p in self.backend.bootstrap(True) if decode(p)[0] == 1017)
            self.assertEqual(snapshot['guide_progress'], (1 << stage) - 2)
            role = self.backend.profile()
            name = (str(int(role['corteges'][1]['id'])) if stage == 6 else
                    str(int(next(i['id'] for i in role['attachments'] if i['type_id'] == 2041))) if stage == 9 else '')
            before = self.backend.profile()
            if stage == 10:
                with patch.object(self.backend, 'inventory', side_effect=ValueError('encode failure')):
                    self.send(stage)
                self.assertEqual(self.backend.profile(), before)
            replies = self.step(stage, name=name)
            if stage == 10:
                role = self.backend.profile()
                self.assertEqual((role['level'], role['cur_exp']), (2, 0))
                events = [(data['id'], login_fields(data['data'])) for mid, _, data in replies if mid == 2998]
                upgrade = next(data for eid, data in events if eid == 2)
                self.assertEqual((upgrade['old_level'], upgrade['new_level']), (1, 2))
                gain = next(data['exp_plus'] for eid, data in events if eid == 45 and data['obj_type'] == 1)
                self.assertEqual(gain, before['next_exp'] - before['cur_exp'])
                self.assertLess(next(i for i, (eid, _) in enumerate(events) if eid == 2),
                                next(i for i, (eid, _) in enumerate(events) if eid == 44))
        self.assertEqual(self.backend.profile()['guide_progress'], 0x3ffe)
        self.assertEqual(self.backend.profile()['gold_coin'], 40)

    @patch.object(progression, 'strength_bonus', return_value=(0, 100))
    def test_stuck_upgrade_save_recovers_once_without_replaying_battle(self, _bonus):
        # Recreate an old save from before the level-1 XP bonus was enabled.
        self.step(1, name='升级行者', head_type=101)
        self.step(2, name='1')
        for stage in (3, 5, 6, 7, 8, 9):
            role = self.backend.profile()
            name = (str(int(role['corteges'][1]['id'])) if stage == 6 else
                    str(int(next(i['id'] for i in role['attachments'] if i['type_id'] == 2041))) if stage == 9 else '')
            self.step(stage, name=name)
        # Reproduce the previously shipped stage-10 settlement exactly.
        with patch.object(guide, 'ensure_tutorial_level', return_value=0):
            self.step(10)
            before = self.backend.profile()
        self.assertEqual((before['level'], before['cur_exp'], before['guide_progress']), (1, 20, 2046))
        snapshot = next(decode(p)[2] for p in self.backend.bootstrap() if decode(p)[0] == 1017)
        after = self.backend.profile()
        self.assertEqual((snapshot['level'], snapshot['cur_exp'], snapshot['guide_progress']), (2, 0, 2046))
        self.assertEqual(after['gold_coin'] - before['gold_coin'], 20)
        buns = [i for i in after['attachments'] if i['type_id'] == 1020]
        self.assertEqual(sum(i['count'] for i in buns), 1)
        for key in ('journey', 'strength', 'silver_coin', 'corteges'):
            self.assertEqual(after[key], before[key], key)
        self.backend.close()
        self.backend = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None, account='new-guide')
        self.backend.bootstrap(True)
        reloaded = self.backend.profile()
        for key in ('level', 'cur_exp', 'guide_progress', 'gold_coin', 'attachments', 'progression',
                    'journey', 'strength', 'silver_coin', 'corteges'):
            self.assertEqual(reloaded[key], after[key], key)

    def test_upgrade_recovery_does_not_change_unrelated_or_leveled_saves(self):
        for progress, level in ((0, 1), (1022, 1), (guide.LEGACY_COMPLETE, 1), (2046, 2)):
            with self.subTest(progress=progress, level=level):
                role = self.backend.profile()
                role.update(guide_progress=progress, level=level, cur_exp=0)
                progression.prepare(role)
                self.backend.save(role)
                self.assertEqual(self.backend.profile(), role)

    def test_native_summon_still_requires_first_fight(self):
        for stage in range(3):
            if stage == 1:
                self.step(1, name='前置行者', head_type=101)
            elif stage == 2:
                self.step(2, name='1')
            before = self.backend.profile()
            _, replies = self.send(5)
            self.assertEqual(self.backend.profile(), before)
            errors = [login_fields(decode(p)[2]['data']) for p in replies
                      if decode(p)[0] == 2998 and decode(p)[2]['id'] == 55]
            self.assertEqual(errors, [dict(op_string='请先完成前置引导')])

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

    def test_original_enemy_stats_and_both_starting_lineups_complete_tutorial(self):
        expected_hp = {3: [200], 7: [250, 220], 8: [280, 280], 10: [300, 300], 12: [500, 300]}
        for choice in ('1', '2'):
            role = self.backend.profile('balance-' + choice)
            for stage in (1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13):
                name = ('教学行者' if stage == 1 else choice if stage == 2 else
                        str(int(role['corteges'][1]['id'])) if stage == 6 else
                        str(int(next(i['id'] for i in role['attachments'] if i['type_id'] == 2041))) if stage == 9 else '')
                if stage in guide.GATES:
                    cfg = journey.GATES[1][guide.GATES[stage]]
                    original = journey.fighters(role, cfg)
                    units = guide.fighters(role, cfg)
                    self.assertEqual(units[0], original[0])
                    self.assertEqual([u['hp'] for u in units[1]], expected_hp[stage])
                    for enemy, normal in zip(units[1], original[1]):
                        self.assertEqual({k: v for k, v in enemy.items() if k != 'skill_probabilities'}, normal)
                    before = copy.deepcopy(role)
                    for seed in range(100):
                        with patch.object(combat.secrets, 'randbelow', side_effect=random.Random(seed).randrange):
                            result, lineup, actions = journey.battle(role, cfg, self.backend.journey_rules, units=units)
                        self.assertEqual(result, 3, (choice, stage, seed))
                        self.assertLessEqual(actions.rounds, 5)
                        self.assertTrue(actions)
                        self.assertTrue(all(a['skill_type'] == 1 for a in actions if not a['is_src']))
                        self.assertEqual([r['des_max_hp'] for r in lineup if r.get('des_type')], expected_hp[stage])
                    self.assertEqual(role, before)
                    # Include both extremes: no random player spells, and every spell proc.
                    for draw in (lambda n: n - 1, lambda n: 0):
                        with patch.object(combat.secrets, 'randbelow', side_effect=draw):
                            result, _, _ = journey.battle(role, cfg, self.backend.journey_rules, units=units)
                        self.assertEqual(result, 3, (choice, stage))
                guide.settle(role, dict(stage=stage, name=name, head_type=101), 1793181600, self.backend)
                formation.prepare(role, self.backend.formation_rules)
                formation.recalculate(role, self.backend.formation_rules)
                tian_shu.refresh(role)
            self.assertEqual(role['guide_progress'], 0x3ffe)
            self.assertEqual(role['gold_coin'], 40)


if __name__ == '__main__':
    unittest.main()
