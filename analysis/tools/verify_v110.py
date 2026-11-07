"""Run release regressions against modules extracted from the actual v110 APK."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v110 import OUTPUT, WORK, EVIDENCE


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['protocol', 'lua'])
    parser.add_argument('--retry-failures', action='store_true')
    parser.add_argument('--candidate', type=Path, default=WORK)
    parser.add_argument('--exclude-test', action='append', default=[])
    parser.add_argument('--only-test-ids', type=Path)
    parser.add_argument('--report-name')
    parser.add_argument('--shard', type=int, choices=range(4))
    args = parser.parse_args()
    mode = args.mode
    program = args.candidate / 'payload-new'
    assert program.is_dir()
    sys.path[:0] = [str(program), str(ROOT / 'tests'), '/private/tmp/jgbol-wait-test-deps']
    sha = hashlib.sha256((args.candidate / OUTPUT.name).read_bytes()).hexdigest()
    if mode == 'protocol':
        # Host networking/CLI/packer checks are run separately from the APK modules.
        excluded = {'test_startup', 'test_network_redirect', 'test_android_offline_backend', 'test_game_server', 'test_login_repair'}
        suites = sorted(p.stem for p in (ROOT / 'tests').glob('test_*.py') if p.stem not in excluded)
        initial = None
        scope_exclusions = []
        selected = suites
        if args.retry_failures:
            original = EVIDENCE / 'protocol-initial-validation.json'
            initial = json.loads((original if original.exists() else EVIDENCE / 'protocol-validation.json').read_text())
            assert initial['apk_sha256'] == sha and not initial['passed']
            selected = list(initial['failed_test_ids'])
            assert len(selected) == initial['errors'] + initial['failures'], selected
            # repair.py is intentionally a desktop-only tool, excluded by the
            # Android packer. Run its tests separately using the host modules.
            scope_exclusions = [name for name in selected if name == 'unittest.loader._FailedTest.test_login_repair']
            selected = [name for name in selected if name not in scope_exclusions]
            if not original.exists():
                original.write_text(json.dumps(initial, indent=2)+'\n')
        suite = unittest.defaultTestLoader.loadTestsFromNames(selected)
        # Imported base TestCases and cross-module helpers may otherwise execute twice.
        def cases(node):
            if isinstance(node, unittest.TestSuite):
                for child in node:
                    yield from cases(child)
            else:
                yield node
        unique = {case.id().removeprefix('tests.'): case for case in cases(suite)}
        assert set(args.exclude_test) <= set(unique)
        selected_cases = [case for name, case in unique.items() if name not in args.exclude_test]
        if args.shard is not None:
            assert not args.retry_failures
            selected_cases = [case for case in selected_cases
                              if int(hashlib.sha256(case.id().removeprefix('tests.').encode()).hexdigest(), 16) % 4 == args.shard]
        if args.only_test_ids:
            wanted = set(json.loads(args.only_test_ids.read_text()))
            assert wanted <= set(unique)
            selected_cases = [case for case in selected_cases if case.id().removeprefix('tests.') in wanted]
            assert len(selected_cases) == len(wanted)
        result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(selected_cases))
        modules = []
        for name, module in list(sys.modules.items()):
            if name.startswith('network_redirect.') and getattr(module, '__file__', None):
                assert Path(module.__file__).resolve().is_relative_to(program.resolve()), name
                modules.append(name)
        report = dict(apk_sha256=sha, passed=result.wasSuccessful(), tests=result.testsRun,
                      errors=len(result.errors), failures=len(result.failures),
                      skipped=len(result.skipped), actual_packaged_modules=len(modules), suites=suites)
        if initial:
            report.update(tests=initial['tests']-len(scope_exclusions), actual_packaged_modules=initial['actual_packaged_modules'],
                          skipped=initial['skipped'], initial_failures=initial['failures'],
                          initial_errors=initial['errors'], rechecked_tests=result.testsRun,
                          rechecked_test_ids=selected, original_run='protocol-tests.log',
                          desktop_loader_errors_excluded=scope_exclusions)
        report['test_ids'] = ([name for name in initial['test_ids'] if name not in scope_exclusions] if initial
                              else [case.id().removeprefix('tests.') for case in selected_cases])
        report['failed_test_ids'] = [case.id() for case, _ in result.failures + result.errors]
        report['excluded_test_ids'] = initial.get('excluded_test_ids', []) if initial else args.exclude_test
        report['shard'] = args.shard
        if initial:
            report['original_shards'] = initial.get('shards', 1)
        destination = f'protocol-shard-{args.shard}.json' if args.shard is not None else 'protocol-validation.json'
        if args.report_name:
            assert Path(args.report_name).name == args.report_name and args.report_name.endswith('.json')
            destination = args.report_name
        (EVIDENCE / destination).write_text(json.dumps(report, indent=2)+'\n')
        raise SystemExit(not result.wasSuccessful())
    from lupa.lua51 import LuaRuntime
    from network_redirect import summon, activity_rank
    checks = {}
    for fixture, adapter in [('skill', 'skill'), ('upgrade_probability', 'skill'),
                             ('dream', 'dream'), ('nine_sky', 'nine_sky')]:
        source = (program / f'network_redirect/{adapter}_client.lua').read_text()
        harness = (ROOT / f'tests/{fixture}_client_regression.lua').read_text()
        value = LuaRuntime().execute(harness.replace('-- INSTALL_PATCH', source).replace('-- INSTALL_AGAIN', source))
        checks[fixture] = list(value.values()) if hasattr(value, 'values') else value
    source = activity_rank.client_source()
    checks['rank_500'] = LuaRuntime().execute((ROOT / 'tests/rank_500_client_regression.lua').read_text(), source)
    source = (program / 'network_redirect/abyss_client.lua').read_text()
    harness = (ROOT / 'tests/abyss_success_client_regression.lua').read_text()
    vm = LuaRuntime()
    vm.globals().ABYSS_SOURCE = source
    vm.execute(harness.replace("dofile('network_redirect/abyss_client.lua')", 'assert(loadstring(ABYSS_SOURCE))()'))
    checks['abyss_success'] = True
    import tempfile
    from unittest.mock import patch
    from network_redirect.backend import Backend, login_fields
    from network_redirect.protocol import encode, decode
    with tempfile.TemporaryDirectory() as temp, patch('network_redirect.game_clock.now', return_value=1792814400):
        backend = Backend(Path(temp), 18770, lambda *a, **kw: None)
        try:
            packets = backend.respond(encode(1346, dict(serial_num=90000, id=1, data='{}')), {'authenticated': True})
            fixture = next(login_fields(d['data']) for mid, _, d in map(decode, packets) if mid == 2998 and d['id'] == 197)
        finally:
            backend.close()
    source = (program / 'network_redirect/save_monkey_client.lua').read_text().replace('__SAVE_MONKEY_ENABLED__', 'true')
    harness = (ROOT / 'tests/save_monkey_client_regression.lua').read_text()
    vm = LuaRuntime()
    vm.execute('FIXTURE=' + summon.lua(fixture))
    checks['save_monkey'] = list(vm.execute(harness.replace('-- INSTALL_PATCH', source).replace('-- INSTALL_AGAIN', source)).values())
    bundle = (program / 'offline_client.lua').read_text()
    LuaRuntime().execute('assert(loadstring(...))', bundle)
    # The real login scene runs before ms and activity modules are available.
    # A pending activity adapter must not prevent the version label from loading.
    vm = LuaRuntime()
    vm.execute('''
      LABELS={}
      local scene={getChildByTag=function() return nil end,addChild=function() end}
      package.loaded['update.updateUI']={create=function() end,g_self={main_scene=scene}}
      package.loaded['update.update_ms']={d_u={createByStyle=function(spec)
        LABELS[#LABELS+1]=spec.string;return {} end}}
      CCLayer={create=function() return {setTouchEnabled=function() end,addChild=function() end} end}
      CCDirector={sharedDirector=function() return {getRunningScene=function() return scene end} end}
    ''')
    assert vm.execute(bundle) == 'pending'
    assert list(vm.globals().LABELS.values()) == ['离线版·非商业·仅供学习', 'v110', '开发者@Ezan']
    checks['prelogin_without_activity_modules_shows_v110'] = True
    assert "label('v110',0.75)" in bundle and "label('v109',0.75)" not in bundle and "label('v108',0.75)" not in bundle
    assert 'row.id~=ui.funID.dream and row.id~=ui.funID.saveMonkey' in bundle
    checks['bundle_compiles_home_v110_and_hidden_entries'] = True
    (EVIDENCE / 'lua-validation.json').write_text(json.dumps(dict(
        apk_sha256=sha, passed=True, checks=checks), ensure_ascii=False, indent=2)+'\n')
    print(checks)


if __name__ == '__main__':
    main()
