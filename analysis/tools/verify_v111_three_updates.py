"""Exercise the exact v111 three-update APK, including old saves and native Lua."""
import argparse
import os
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools import verify_v111_ten_updates as prior
from analysis.tools.build_v111_three_updates import WORK, EVIDENCE, OUTPUT, BASE, digest, report

prior.WORK, prior.EVIDENCE, prior.OUTPUT, prior.BASE = WORK, EVIDENCE, OUTPUT, BASE
prior.report = report
SUITES = [
    'test_gift_codes', 'test_recharge', 'test_welfare_recharge', 'test_item_rewards',
    'test_level_card', 'test_level_card_sources',
    'test_activity_abyss', 'test_abyss_balance', 'test_abyss_shop',
    'test_activity_land_balance', 'test_activity_land', 'test_activity_land_players',
    'test_activity_land_tower', 'test_land_card_caps', 'test_land_week_mail',
    'test_activity.LandTests', 'test_activity.ActivityTests',
    'test_android_offline_backend', 'test_network_time_runtime',
]


def protocol():
    program = prior.setup()
    unique = {c.id():c for c in prior.cases(unittest.defaultTestLoader.loadTestsFromNames(SUITES))}
    result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(unique.values()))
    modules = {}
    for name, module in list(sys.modules.items()):
        if (name.startswith('network_redirect.') or name == 'offline_android.backend') and getattr(module,'__file__',None):
            path = Path(module.__file__).resolve()
            assert path.is_relative_to(program.resolve()), (name, path)
            modules[name] = str(path.relative_to(program))
    report('protocol-validation',dict(apk_sha256=digest(OUTPUT.read_bytes()),
        passed=result.wasSuccessful() and not result.skipped, tests=result.testsRun,
        failures=len(result.failures), errors=len(result.errors), skipped=len(result.skipped),
        test_ids=sorted(unique), suites=SUITES, actual_packaged_modules=modules,
        failed_test_ids=[c.id() for c,_ in result.failures+result.errors]))
    raise SystemExit(not result.wasSuccessful() or bool(result.skipped))


def lua():
    # Existing full bundle, v111 branding, battle replay and weekly UI checks.
    prior.lua()
    from lupa.lua51 import LuaRuntime
    program = WORK / 'payload-new'
    source = (program / 'network_redirect/abyss_client.lua').read_text()
    fixture = (ROOT / 'tests/abyss_number_client_regression.lua').read_text()
    try:
        LuaRuntime().execute(fixture, '')
    except Exception as exc:
        assert 'two digits must remain visible' in str(exc), str(exc)
    else:
        raise AssertionError('Must reproduce original single-digit input defect')
    LuaRuntime().execute(fixture, source)
    previous = Path.cwd()
    try:
        os.chdir(program)
        for name in ('abyss_client_regression', 'abyss_success_client_regression'):
            LuaRuntime().execute((ROOT / f'tests/{name}.lua').read_text())
    finally:
        os.chdir(previous)
    import json
    path = EVIDENCE / 'lua-validation.json'
    record = json.loads(path.read_text())
    record.update(abyss_keypad_original_failure_reproduced=True,
                  abyss_keypad_regression_passed=True, previous_abyss_regressions_passed=True)
    report('lua-validation', record)
    print('Packaged Abyss keypad and previous Abyss client regressions passed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode',choices=['protocol','lua','save'])
    args = parser.parse_args()
    if args.mode == 'save':
        prior.save()
    else:
        globals()[args.mode]()
