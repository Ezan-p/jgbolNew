"""Run gameplay regressions against the actual signed v110 refresh payload."""
import argparse
import ast
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / '.runtime/v110-test-refresh-20261110/program'
EVIDENCE = ROOT / 'analysis/evidence/v110-test-refresh-20261110'
APK = PROGRAM.parent / '金箍棒ol测试版-v110-20261110整合更新.apk'


def suites():
    # Read the existing release's suite list without importing its build modules.
    tree = ast.parse((ROOT / 'analysis/tools/verify_v111.py').read_text())
    base = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == 'SUITES' for t in n.targets))
    return sorted(set(base + [p.stem for p in (ROOT / 'tests').glob('test_guild*.py')] + [
        'test_level_card', 'test_level_card_sources', 'test_activity_hunt', 'test_gift_codes',
        'test_network_time', 'test_trusted_game_clock', 'test_seasonal_weekly',
        'test_activity_moon', 'test_activity_rice', 'test_seasonal_crafting',
        'test_activity_save_monkey', 'test_activity_fish', 'test_fish_client',
        'test_activity_home', 'test_home_ordeal', 'test_tianxian_token',
        'test_pets', 'test_pet_acquisition', 'test_pet_quality', 'test_pet_quality_client',
        'test_equipment_instances', 'test_land_card_caps', 'test_progression',
        'test_activity_rank', 'test_activity_duty', 'test_local_accounts']))


def setup():
    sys.path[:0] = [str(PROGRAM), str(ROOT / 'tests'), str(ROOT), '/private/tmp/qmxy-battle-test-deps']
    import offline_android
    assert Path(offline_android.__file__).resolve().is_relative_to(PROGRAM)
    # This development-only helper is intentionally absent from the APK.
    spec = importlib.util.spec_from_file_location('offline_android.pack_payload', ROOT / 'offline_android/pack_payload.py')
    helper = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = helper
    spec.loader.exec_module(helper)
    offline_android.pack_payload = helper
    helper.verify_payload(PROGRAM)
    with zipfile.ZipFile(APK) as apk, zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as z:
        assert all(z.read(n) == (PROGRAM / n).read_bytes() for n in z.namelist())


def cases(node):
    if isinstance(node, unittest.TestSuite):
        for child in node:
            yield from cases(child)
    else:
        yield node


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--shard', type=int, choices=range(4))
    parser.add_argument('--merge', action='store_true')
    parser.add_argument('--only', nargs='+')
    args = parser.parse_args()
    setup()
    unique = {c.id().removeprefix('tests.'): c for c in
              cases(unittest.defaultTestLoader.loadTestsFromNames(args.only or suites()))}
    checksum = hashlib.sha256(APK.read_bytes()).hexdigest()
    if args.merge:
        records = [json.loads((EVIDENCE / f'protocol-shard-{i}.json').read_text()) for i in range(4)]
        recheck_path = EVIDENCE / 'protocol-recheck.json'
        recheck = json.loads(recheck_path.read_text()) if recheck_path.exists() else None
        replaced = []
        ids = []
        for data in records:
            assert data['apk_sha256'] == checksum and data['skipped'] == 0
            if not data['passed']:
                failed = {n.removeprefix('tests.') for n in data['failed_test_ids']}
                assert failed == {'test_local_accounts.AuthHTTPTests.test_form_csrf_and_registration'}
                assert data['errors'] == 1 and data['failures'] == 0
                log = (EVIDENCE / 'protocol-shard-3.log').read_text()
                assert "PermissionError: [Errno 1] error while attempting to bind on address ('127.0.0.1', 0): operation not permitted" in log
                assert recheck and recheck['passed'] and recheck['apk_sha256'] == checksum
                assert recheck['errors'] == recheck['failures'] == recheck['skipped'] == 0
                assert failed <= set(recheck['test_ids'])
                replaced.extend(sorted(failed))
            else:
                assert data['errors'] == data['failures'] == 0
            ids.extend(data['test_ids'])
        assert len(ids) == len(set(ids)) and set(ids) == set(unique)
        data = dict(passed=True, apk_sha256=checksum, tests=len(ids), errors=0, failures=0,
                    skipped=0, suites=suites(), test_ids=sorted(ids),
                    environment_rechecks=replaced, recheck_evidence='protocol-recheck.json' if replaced else None)
        name = 'protocol-validation'
    else:
        assert args.shard is not None or args.only
        chosen = {n: c for n, c in unique.items() if args.only or int(hashlib.sha256(n.encode()).hexdigest(), 16) % 4 == args.shard}
        result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(chosen.values()))
        origins = {}
        for name, module in list(sys.modules.items()):
            if name.startswith(('network_redirect.', 'offline_android.')) and name != 'offline_android.pack_payload' and getattr(module, '__file__', None):
                path = Path(module.__file__).resolve()
                assert path.is_relative_to(PROGRAM), (name, path)
                origins[name] = str(path.relative_to(PROGRAM))
        data = dict(passed=result.wasSuccessful() and not result.skipped, apk_sha256=checksum,
                    tests=result.testsRun, errors=len(result.errors), failures=len(result.failures),
                    skipped=len(result.skipped), test_ids=list(chosen), actual_packaged_modules=origins,
                    failed_test_ids=[c.id() for c, _ in result.errors + result.failures])
        name = 'protocol-recheck' if args.only else f'protocol-shard-{args.shard}'
    (EVIDENCE / (name + '.json')).write_text(json.dumps(data, indent=2) + '\n')
    print(name, data['tests'], 'passed:', data['passed'])
    raise SystemExit(not data['passed'])


if __name__ == '__main__':
    main()
