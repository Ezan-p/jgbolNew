"""Validate the signed v112 test APK, including actual v111 save migration."""
import argparse
import collections
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools import build_v112_test as build
from analysis.tools import verify_v112 as verify

for name in ('WORK', 'EVIDENCE', 'OUTPUT', 'BASE', 'digest', 'report'):
    setattr(verify, name, getattr(build, name))
# Backend bootstrap tests assert the formal account interface. Test-edition
# initialization is covered by the real v111 migration and grant tests below.
verify.SUITES = [n for n in verify.SUITES if not n.startswith('test_android_offline_backend')
                 and n != 'test_network_time_runtime']


def scope():
    program = verify.setup()
    meta = json.loads((build.EVIDENCE / 'build-validation.json').read_text())
    import io
    import zipfile
    from offline_android.pack_payload import verify_payload
    assert verify_payload(program)['loopback_port'] == 18776
    with zipfile.ZipFile(build.OUTPUT) as apk, \
            zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as p:
        assert all(p.read(n) == (program / n).read_bytes() for n in p.namelist())
    for name, sha in meta['source_hashes'].items():
        if name not in ('offline_android/backend.py', 'network_redirect/login.html'):
            assert build.digest((program / name).read_bytes()) == sha, name
    # Every gameplay file equals the current source snapshot; the two deliberate
    # exceptions are the fixed-account boot adapter and the retained test login.
    backend = (program / 'offline_android/backend.py').read_text()
    assert 'PORT = 18776' in backend and "self.files_dir / 'test-save-v106'" in backend
    assert 'from offline_android.test_edition_v112 import fixed_accounts_class' in backend
    expected_backend = (build.WORK / 'source/offline_android/backend.py').read_text()
    expected_backend = expected_backend.replace('PORT = 18770', 'PORT = 18776')
    expected_backend = expected_backend.replace("self.files_dir / 'save'", "self.files_dir / 'test-save-v106'")
    expected_backend = expected_backend.replace('from network_redirect.accounts import Accounts',
        'from offline_android.test_edition_v112 import fixed_accounts_class\n        Accounts = fixed_accounts_class()')
    assert backend == expected_backend
    for name in ('offline_android/test_edition_seed.py', 'offline_android/test_edition_v108.py',
                 'offline_android/test_edition_v110.py', 'network_redirect/login.html'):
        assert (program / name).read_bytes() == (build.WORK / 'payload-old' / name).read_bytes()
    config = lambda n: json.loads((program / f'server_config/{n}_rules.json').read_text())
    assert config('activity')['abyss_map_revision'] == '2026-11-13-user-pool-v9'
    assert config('activity')['undergo_shop_revision'] == 'taixu-shop-2026-11-13-v5'
    assert config('rice')['normal_five_star_weight'] == 25
    assert config('taixu')['revision'] == 'offline-taixu-8'
    assert config('taixu')['arena_win_prize_crystals'] == 100
    assert 'local_forfeit' in (program / 'network_redirect/taixu_client.lua').read_text()
    assert not any(p.suffix in ('.db', '.sqlite3') for p in program.rglob('*'))
    build.report('scope-validation', dict(passed=True, apk_sha256=meta['apk_sha256'],
        frozen_gameplay_verified=True, test_save_identity_preserved=True,
        latest_twelve_update_groups=True, contains_player_database=False))
    print('Frozen gameplay and isolated test identity verified')


OLD_WORKER = r'''
import json,sys
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from offline_android import test_edition_v110 as old
from network_redirect import summon,formation
a=old.fixed_accounts_class()(Path(sys.argv[2]),18776,lambda *a,**k:None)
b=a.backends[old.ACCOUNT]
r=b.profile();r['role_name']='v112旧档验证';r['gold_coin']-=1234
r['test_v112_preserve']={'progress':[1,2,3]}
formation.debit_item(r,1431,7)
for tid in list(range(1431,1441))+list(range(1213,1218)):
 summon.add_item(r,tid,7)
b.save(r,gameplay=False)
b.save(dict(r,role_name='其他账号'),account='unrelated',gameplay=False)
(Path(sys.argv[2])/'before.json').write_text(json.dumps(b.profile()))
a.close()
'''


def grants():
    program = verify.setup()
    from offline_android import test_edition_v112 as current, test_edition_v110 as previous
    from network_redirect import summon, formation
    from network_redirect.protocol import encode, decode
    baseline = build.WORK / 'v111-save-fixture'
    assert not baseline.exists(), 'Do not replace save evidence'
    baseline.mkdir()
    subprocess.run([sys.executable, '-I', '-c', OLD_WORKER,
                    str(build.WORK / 'payload-old'), str(baseline)], check=True, timeout=180)

    def counts(role):
        out = collections.Counter()
        for i in role['attachments']:
            if i['attach_type'] == 5:
                out[i['type_id']] += i['count']
        return out

    class GrantTests(unittest.TestCase):
        def setUp(self):
            self.temp = tempfile.TemporaryDirectory(prefix='v112-grant-')
            self.addCleanup(self.temp.cleanup)
            self.path = Path(self.temp.name)
            shutil.copytree(baseline, self.path, dirs_exist_ok=True)
            self.before = json.loads((self.path / 'before.json').read_text())

        def open(self, factory=current.fixed_accounts_class):
            a = factory()(self.path, 18776, lambda *a, **k: None)
            self.addCleanup(a.close)
            return a, a.backends[current.ACCOUNT]

        def test_actual_v111_save_adds_all_14_items_and_preserves_progress(self):
            _, b = self.open()
            after = b.profile()
            self.assertEqual(counts(after) - counts(self.before), dict(current.ITEMS))
            self.assertFalse(counts(self.before) - counts(after))
            for key in ('role_name','gold_coin','silver_coin','test_v108_silver_reserve',
                        'test_supply_revision','test_v112_preserve',previous.MARKER):
                self.assertEqual(after[key], self.before[key], key)
            for companion in self.before['corteges']:
                other = next(c for c in after['corteges'] if c['id'] == companion['id'])
                for key in ('type','level','evolve_level','reborn_layer','order'):
                    self.assertEqual(other.get(key), companion.get(key), key)
            non_supply = lambda r: [i for i in r['attachments'] if i['type_id'] not in dict(current.ITEMS)]
            self.assertEqual(non_supply(after), non_supply(self.before))
            self.assertEqual(counts(after)[1217], 7)

        def test_restart_after_consuming_every_supply_does_not_refill(self):
            a, b = self.open()
            role = b.profile()
            for tid, _ in current.ITEMS:
                formation.debit_item(role, tid, 3)
            b.save(role, gameplay=False)
            saved = b.profile()
            a.close()
            _, b = self.open()
            self.assertEqual(b.profile(), saved)
            self.assertFalse(current.grant_supplies(b))

        def test_new_save_gets_legacy_supplies_and_new_grant_once(self):
            shutil.rmtree(self.path)
            self.path.mkdir()
            a, b = self.open()
            role = b.profile()
            self.assertEqual(role['test_supply_revision'], 108)
            self.assertIn(previous.MARKER, role)
            for tid, n in current.ITEMS:
                self.assertEqual(counts(role)[tid], n + (500 if tid == 1431 else 0))
            a.close()
            _, b = self.open()
            self.assertEqual(b.profile(), role)

        def test_save_failure_rolls_back_items_and_receipt_then_retry(self):
            _, b = self.open(previous.fixed_accounts_class)
            before = b.profile()
            raw = b.db.execute('SELECT data FROM roles WHERE account=?', (current.ACCOUNT,)).fetchone()[0]
            def fail(role, *args, **kwargs):
                b.db.execute('UPDATE roles SET data=? WHERE account=?', (json.dumps(role), current.ACCOUNT))
                raise RuntimeError('injected failure before commit')
            with patch.object(b, 'save', side_effect=fail), self.assertRaises(RuntimeError):
                current.grant_supplies(b)
            self.assertEqual(raw, b.db.execute('SELECT data FROM roles WHERE account=?', (current.ACCOUNT,)).fetchone()[0])
            self.assertTrue(current.grant_supplies(b))
            self.assertFalse(current.grant_supplies(b))
            self.assertEqual(counts(b.profile()) - counts(before), dict(current.ITEMS))

        def test_partial_item_failure_never_persists_and_retry_is_exact(self):
            _, b = self.open(previous.fixed_accounts_class)
            before = b.profile()
            add = summon.add_item
            def fail(role, tid, n):
                if tid == 1435:
                    raise RuntimeError('injected partial grant failure')
                return add(role, tid, n)
            with patch.object(summon, 'add_item', side_effect=fail), self.assertRaises(RuntimeError):
                current.grant_supplies(b)
            self.assertEqual(b.profile(), before)
            self.assertTrue(current.grant_supplies(b))
            self.assertEqual(counts(b.profile()) - counts(before), dict(current.ITEMS))

        def test_other_account_unchanged_and_ineligible(self):
            _, b = self.open(previous.fixed_accounts_class)
            raw = b.db.execute("SELECT data FROM roles WHERE account='unrelated'").fetchone()[0]
            self.assertTrue(current.grant_supplies(b))
            self.assertEqual(raw, b.db.execute("SELECT data FROM roles WHERE account='unrelated'").fetchone()[0])
            with patch.object(b, 'account', 'unrelated'):
                self.assertFalse(current.grant_supplies(b))

        def test_all_ten_map_tiers_usable_and_replay_does_not_double_spend(self):
            _, b = self.open()
            for serial, (tid, _) in enumerate(current.MAP_ITEMS, 91000):
                before = counts(b.profile())[tid]
                request = encode(1329, dict(serial_num=serial, id=24,
                    data=summon.lua(dict(map_type=tid, treasure_count=1, open_count=1))))
                replies = b.respond(request, {'authenticated': True})
                self.assertFalse(any(mid == 2998 and data.get('id') == 55 for mid, _, data in map(decode, replies)))
                self.assertEqual(counts(b.profile())[tid], before - 1)
                self.assertEqual(b.respond(request, {'authenticated': True}), replies)
                self.assertEqual(counts(b.profile())[tid], before - 1)

        def test_all_four_rice_supplies_usable_in_batches(self):
            _, b = self.open()
            for serial, (tid, _) in enumerate(current.RICE_ITEMS, 92000):
                role = b.profile()
                item = next(i for i in role['attachments'] if i['type_id'] == tid and not i.get('is_lock'))
                before = counts(role)[tid]
                request = encode(1051, dict(serial_num=serial, item_type=tid, item_id=item['id'],
                    item_count=10, des_type=1, des_id=0))
                replies = b.respond(request, {'authenticated': True})
                self.assertFalse(any(mid == 2998 and data.get('id') == 55 for mid, _, data in map(decode, replies)))
                self.assertEqual(counts(b.profile())[tid], before - 10)
                self.assertEqual(b.respond(request, {'authenticated': True}), replies)
                self.assertEqual(counts(b.profile())[tid], before - 10)

    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(GrantTests))
    for name, module in list(sys.modules.items()):
        runtime_module = name.startswith('network_redirect.') or name.startswith('offline_android.test_edition') or name == 'offline_android.backend'
        if runtime_module and getattr(module, '__file__', None):
            assert Path(module.__file__).resolve().is_relative_to(program.resolve()), name
    build.report('grant-validation', dict(passed=result.wasSuccessful() and not result.skipped,
        tests=result.testsRun, failures=len(result.failures), errors=len(result.errors), skipped=len(result.skipped),
        apk_sha256=build.digest(build.OUTPUT.read_bytes()), actual_v111_save_migration=True,
        additive_maps_each=500, additive_rice_each=300))
    raise SystemExit(not result.wasSuccessful() or bool(result.skipped))


def lua():
    verify.lua()
    from lupa.lua51 import LuaRuntime
    LuaRuntime().execute((build.WORK / 'tests/taixu_client_regression.lua').read_text())
    record = json.loads((build.EVIDENCE / 'lua-validation.json').read_text())
    record['taixu_forfeit_and_rewards'] = True
    build.report('lua-validation', record)


def runtime():
    verify.setup()
    # Reuse the established test-edition HTTP/login/restart and trusted-clock
    # checks with the current APK, rather than formal-account expectations.
    source = (ROOT / 'analysis/tools/verify_v111_test_runtime.py').read_text()
    source = source.replace('.runtime/v111-test/program', '.runtime/v112-test-20261113/payload-new')
    source = source.replace('analysis/evidence/v111_test', 'analysis/evidence/v112-test-20261113')
    source = source.replace('.runtime/v111-test/金箍棒ol测试版-v111.apk',
                            '.runtime/v112-test-20261113/金箍棒ol测试版-v112.apk')
    source = source.replace("name.startswith(('network_redirect.','offline_android.'))",
        "(name.startswith('network_redirect.') or name.startswith('offline_android.test_edition') or name=='offline_android.backend')")
    source = source.replace("self.assertEqual(role['test_supply_revision'],108)",
        "self.assertEqual(role['test_supply_revision'],108)\n"
        "                    self.assertEqual(role['test_v112_maps500_rice300_v1']['maps_total'],5000)\n"
        "                    self.assertEqual(role['test_v112_maps500_rice300_v1']['rice_total'],1200)")
    namespace = dict(__name__='__main__', __file__=str(ROOT / 'analysis/tools/verify_v112_test_runtime.py'))
    exec(compile(source, namespace['__file__'], 'exec'), namespace)


def recheck():
    verify.setup()
    names = sorted({name for record in build.EVIDENCE.glob('protocol-shard-*.json')
        for name in json.loads(record.read_text())['failed_test_ids']
        if not name.startswith(('test_android_offline_backend.', 'test_network_time_runtime.'))})
    assert names
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names))
    build.report('protocol-environment-recheck', dict(apk_sha256=build.digest(build.OUTPUT.read_bytes()),
        passed=result.wasSuccessful() and not result.skipped, tests=result.testsRun,
        failures=len(result.failures), errors=len(result.errors), skipped=len(result.skipped),
        test_ids=names, failed_test_ids=[c.id() for c, _ in result.failures + result.errors]))
    raise SystemExit(not result.wasSuccessful() or bool(result.skipped))


def merge():
    verify.setup()
    expected = {c.id().removeprefix('tests.') for c in verify.cases(
        unittest.defaultTestLoader.loadTestsFromNames(verify.SUITES))}
    recheck_path = build.EVIDENCE / 'protocol-environment-recheck.json'
    rerun = json.loads(recheck_path.read_text()) if recheck_path.exists() else None
    ids, excluded, failures = set(), set(), set()
    sha = build.digest(build.OUTPUT.read_bytes())
    for shard in range(3):
        record = json.loads((build.EVIDENCE / f'protocol-shard-{shard}.json').read_text())
        assert record['apk_sha256'] == sha and record['skipped'] == 0
        chosen = set(record['test_ids']) & expected
        assert not ids & chosen
        ids.update(chosen)
        excluded.update(set(record['test_ids']) - expected)
        failures.update(set(record['failed_test_ids']) & expected)
    assert ids == expected
    if failures:
        assert rerun and rerun['passed'] and rerun['apk_sha256'] == sha
        assert failures <= set(rerun['test_ids']) and rerun['skipped'] == 0
    runtime_report = json.loads((build.EVIDENCE / 'runtime-validation.json').read_text())
    assert runtime_report['passed'] and runtime_report['apk_sha256'] == sha
    assert all(n.startswith(('test_android_offline_backend.', 'test_network_time_runtime.')) for n in excluded)
    build.report('protocol-validation', dict(passed=True, apk_sha256=sha, tests=len(ids),
        failures=0, errors=0, skipped=0, test_ids=sorted(ids), suites=verify.SUITES,
        environment_recheck_test_ids=sorted(failures),
        formal_contract_test_ids_replaced_by_test_runtime=sorted(excluded),
        replacement_evidence='runtime-validation.json'))
    print('Passed packaged gameplay tests:', len(ids))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['scope','grants','lua','runtime','protocol','merge','recheck'])
    parser.add_argument('--shard', type=int, choices=range(3))
    args = parser.parse_args()
    if args.mode == 'protocol':
        verify.protocol(args.shard)
    else:
        globals()[args.mode]()
