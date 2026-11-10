"""Verify the once-only grant using modules extracted from the actual new APK."""
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / '.runtime/v110-test-maps500'
PROGRAM = WORK / 'program'
EVIDENCE = ROOT / 'analysis/evidence/v110_test_maps500'
APK = WORK / '金箍棒ol测试版-v110-九幽宝图500.apk'
sys.path.insert(0, str(PROGRAM))
from offline_android import test_edition_v108 as previous, test_edition_v110 as current
from network_redirect import summon, formation, game_clock
from network_redirect.protocol import encode, decode


def counts(role):
    return {tid: sum(i['count'] for i in role['attachments'] if i['attach_type'] == 5 and i['type_id'] == tid)
            for tid in range(1431, 1441)}


class MapsGrantTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)

    def old_save(self):
        a = previous.fixed_accounts_class()(self.path, 18776, lambda *a, **k: None)
        b = a.backends[previous.ACCOUNT]
        role = b.profile()
        role['role_name'] = '宝图追加旧档'
        role['gold_coin'] -= 123
        for tid, _ in current.MAP_ITEMS:
            summon.add_item(role, tid, 7)
        b.save(role, gameplay=False)
        before = b.profile()
        b.save(dict(before, role_name='另一个账号'), account='unrelated', gameplay=False)
        unrelated = b.db.execute("SELECT data FROM roles WHERE account='unrelated'").fetchone()[0]
        a.close()
        return before, unrelated

    def open(self, factory=current.fixed_accounts_class):
        a = factory()(self.path, 18776, lambda *a, **k: None)
        self.addCleanup(a.close)
        return a, a.backends[previous.ACCOUNT]

    def test_existing_save_adds_exactly_500_and_preserves_progress_and_other_account(self):
        before, unrelated = self.old_save()
        _, b = self.open()
        after = b.profile()
        for tid in range(1431, 1441):
            self.assertEqual(counts(after)[tid], counts(before)[tid] + dict(current.MAP_ITEMS).get(tid, 0))
        self.assertEqual(sum(dict(current.MAP_ITEMS).values()), 500)
        for key in ('role_name', 'gold_coin', 'silver_coin', 'test_v108_silver_reserve', 'test_supply_revision', 'corteges'):
            self.assertEqual(before[key], after[key], key)
        nonmaps = lambda r: [i for i in r['attachments'] if i['type_id'] not in range(1431, 1441)]
        self.assertEqual(nonmaps(before), nonmaps(after))
        self.assertEqual(unrelated, b.db.execute("SELECT data FROM roles WHERE account='unrelated'").fetchone()[0])

    def test_repeated_initialization_and_restart_after_consumption_do_not_refill(self):
        self.old_save()
        a, b = self.open()
        before = b.profile()
        self.assertFalse(current.grant_maps(b))
        self.assertEqual(b.profile(), before)
        role = b.profile()
        formation.debit_item(role, current.MAP_ITEMS[0][0], 3)
        b.save(role, gameplay=False)
        saved = b.profile()
        a.close()
        _, b = self.open()
        self.assertEqual(b.profile(), saved)

    def test_new_save_receives_original_allowance_and_maps_once(self):
        a, b = self.open()
        role = b.profile()
        self.assertEqual(role['test_supply_revision'], 108)
        self.assertEqual(role['gold_coin'], 110000)
        for tid, count in current.MAP_ITEMS:
            self.assertEqual(counts(role)[tid], count)
        a.close()
        _, b = self.open()
        self.assertEqual(b.profile(), role)

    def test_save_failure_rolls_back_reward_and_marker_then_retry_grants_once(self):
        self.old_save()
        _, b = self.open(previous.fixed_accounts_class)
        before = b.profile()
        raw = b.db.execute('SELECT data FROM roles WHERE account=?', (previous.ACCOUNT,)).fetchone()[0]
        save = b.save
        def fail(role, *args, **kwargs):
            if current.MARKER not in role:
                return save(role, *args, **kwargs)
            b.db.execute('UPDATE roles SET data=? WHERE account=?', (json.dumps(role), previous.ACCOUNT))
            raise RuntimeError('simulated failure before commit')
        with patch.object(b, 'save', side_effect=fail), self.assertRaises(RuntimeError):
            current.grant_maps(b)
        self.assertEqual(raw, b.db.execute('SELECT data FROM roles WHERE account=?', (previous.ACCOUNT,)).fetchone()[0])
        self.assertTrue(current.grant_maps(b))
        self.assertFalse(current.grant_maps(b))
        self.assertEqual(sum(counts(b.profile()).values()) - sum(counts(before).values()), 500)

    def test_non_test_account_is_not_granted(self):
        _, b = self.open(previous.fixed_accounts_class)
        before = b.profile()
        with patch.object(b, 'account', 'unrelated'):
            self.assertFalse(current.grant_maps(b))
        self.assertEqual(b.profile(), before)

    def test_granted_map_is_usable_through_real_protocol_and_replay_does_not_double_spend(self):
        _, b = self.open()
        tid = current.MAP_ITEMS[0][0]
        before = counts(b.profile())[tid]
        request = encode(1329, dict(serial_num=91001, id=24,
            data=summon.lua(dict(map_type=tid, treasure_count=1, open_count=1))))
        replies = b.respond(request, {'authenticated': True})
        self.assertFalse(any(mid == 2998 and data.get('id') == 55 for mid, _, data in map(decode, replies)))
        self.assertEqual(counts(b.profile())[tid], before - 1)
        self.assertEqual(b.respond(request, {'authenticated': True}), replies)
        self.assertEqual(counts(b.profile())[tid], before - 1)
        self.assertFalse(current.grant_maps(b))


if __name__ == '__main__':
    with zipfile.ZipFile(APK) as apk:
        with zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as p:
            for name in p.namelist():
                assert p.read(name) == (PROGRAM / name).read_bytes(), name
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(MapsGrantTests))
    for name, module in list(sys.modules.items()):
        if name.startswith(('network_redirect.', 'offline_android.')) and getattr(module, '__file__', None):
            assert Path(module.__file__).resolve().is_relative_to(PROGRAM.resolve()), name
    report = dict(passed=result.wasSuccessful(), tests=result.testsRun, failures=len(result.failures),
        errors=len(result.errors), skipped=len(result.skipped), apk_sha256=hashlib.sha256(APK.read_bytes()).hexdigest())
    (EVIDENCE / 'grant-validation.json').write_text(json.dumps(report, indent=2)+'\n')
    raise SystemExit(not result.wasSuccessful())
