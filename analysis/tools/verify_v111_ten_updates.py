"""Validate the frozen v111 APK rather than the changing working tree."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v111_ten_updates import WORK, EVIDENCE, OUTPUT, BASE, digest, report
from analysis.tools.verify_v111_refresh import SUITES as PREVIOUS_SUITES

SUITES = sorted(set(PREVIOUS_SUITES + [
    'test_level_card', 'test_level_card_sources', 'test_gift_codes',
    'test_activity_hunt', 'test_android_offline_backend.PayloadTests',
    'test_qiankun_bags', 'test_progression', 'test_activity_rank',
]))


def setup():
    program = WORK / 'payload-new'
    sys.path[:0] = [str(program), str(ROOT / 'tests'),
                   '/private/tmp/qmxy-battle-test-deps', '/private/tmp/jgbol-wait-test-deps']
    import offline_android
    offline_android.__path__ = [str(program / 'offline_android')]
    sys.modules.pop('offline_android.backend', None)
    spec = importlib.util.spec_from_file_location('offline_android.pack_payload', ROOT / 'offline_android/pack_payload.py')
    helper = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = helper
    spec.loader.exec_module(helper)
    helper.ROOT = program
    helper.collect_files.__defaults__ = (program,)
    helper.build_payload.__defaults__ = (program,)
    offline_android.pack_payload = helper
    return program


def cases(node):
    if isinstance(node, unittest.TestSuite):
        for child in node:
            yield from cases(child)
    else:
        yield node


def protocol(shard):
    program = setup()
    unique = {c.id().removeprefix('tests.'):c for c in cases(unittest.defaultTestLoader.loadTestsFromNames(SUITES))}
    selected = {n:c for n,c in unique.items() if int(hashlib.sha256(n.encode()).hexdigest(),16)%3 == shard}
    result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(selected.values()))
    modules = {}
    for name, module in list(sys.modules.items()):
        if (name.startswith('network_redirect.') or name == 'offline_android.backend') and getattr(module, '__file__', None):
            path = Path(module.__file__).resolve()
            assert path.is_relative_to(program.resolve()), (name,path)
            modules[name] = str(path.relative_to(program))
    report(f'protocol-shard-{shard}', dict(apk_sha256=digest(OUTPUT.read_bytes()),
        passed=result.wasSuccessful() and not result.skipped, tests=result.testsRun,
        failures=len(result.failures), errors=len(result.errors), skipped=len(result.skipped),
        test_ids=list(selected), expected_test_ids=sorted(unique), actual_packaged_modules=modules,
        failed_test_ids=[c.id() for c,_ in result.failures+result.errors]))
    raise SystemExit(not result.wasSuccessful() or bool(result.skipped))


def merge():
    ids = []
    for shard in range(3):
        record = json.loads((EVIDENCE / f'protocol-shard-{shard}.json').read_text())
        assert record['apk_sha256'] == digest(OUTPUT.read_bytes()) and record['passed']
        assert record['failures'] == record['errors'] == record['skipped'] == 0
        ids.extend(record['test_ids'])
    assert len(ids) == len(set(ids)) and set(ids) == set(record['expected_test_ids'])
    report('protocol-validation', dict(apk_sha256=digest(OUTPUT.read_bytes()), passed=True,
        tests=len(ids), failures=0, errors=0, skipped=0, test_ids=sorted(ids), suites=SUITES))
    print('Passed unique packaged tests:', len(ids))


def recheck():
    program=setup()
    names=['test_activity_party','test_party_rank_mail','test_activity_rank',
           'test_activity.ActivityTests','test_activity_taixu',
           'test_android_offline_backend','test_network_time_runtime']
    selected={c.id().removeprefix('tests.'):c for c in cases(unittest.defaultTestLoader.loadTestsFromNames(names))}
    result=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(selected.values()))
    modules={}
    for name,module in list(sys.modules.items()):
        if (name.startswith('network_redirect.') or name=='offline_android.backend') and getattr(module,'__file__',None):
            path=Path(module.__file__).resolve()
            assert path.is_relative_to(program.resolve()),(name,path)
            modules[name]=str(path.relative_to(program))
    report('startup-fix-recheck',dict(apk_sha256=digest(OUTPUT.read_bytes()),
        passed=result.wasSuccessful() and not result.skipped,tests=result.testsRun,
        failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),
        test_ids=list(selected),suites=names,actual_packaged_modules=modules))
    raise SystemExit(not result.wasSuccessful() or bool(result.skipped))


def lua():
    program = setup()
    from lupa.lua51 import LuaRuntime
    from network_redirect.summon import client_source, load_rules
    bundle = (program / 'offline_client.lua').read_text()
    assert bundle == client_source(load_rules())
    LuaRuntime().execute('assert(loadstring(...))', bundle)
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
    assert list(vm.globals().LABELS.values()) == ['离线版·非商业·仅供学习','v111','开发者@Ezan']
    assert "label('v110',0.75)" not in bundle
    source = (program/'network_redirect/battle_replay_client.lua').read_text()
    LuaRuntime().execute((ROOT/'tests/battle_replay_client_regression.lua').read_text(),source)
    source = (program/'network_redirect/nine_sky_client.lua').read_text()
    harness = (ROOT/'tests/nine_sky_client_regression.lua').read_text()
    LuaRuntime().execute(harness.replace('-- INSTALL_PATCH',source).replace('-- INSTALL_AGAIN',source))
    from network_redirect import activity, activity_moon, activity_rice
    rules = activity.load_rules()
    seasonal_checks = LuaRuntime().execute((ROOT/'tests/seasonal_craft_client_regression.lua').read_text(),
        activity_moon.client_source(rules), activity_rice.client_source(rules))
    report('lua-validation', dict(apk_sha256=digest(OUTPUT.read_bytes()), passed=True,
        complete_bundle_compiles=True, generated_source_matches=True,
        prelogin_label='v111', battle_replay=True, nine_sky=True,
        seasonal_weekly_countdown=True, seasonal_checks=seasonal_checks))
    print('Packaged Lua compiles, startup shows v111; battle, Nine Sky and seasonal countdown regressions pass')


def save():
    from analysis.tools import verify_v111 as previous
    previous.WORK, previous.EVIDENCE, previous.OUTPUT, previous.BASE = WORK,EVIDENCE,OUTPUT,BASE
    previous.report = report
    import contextlib, io
    with contextlib.redirect_stdout(io.StringIO()):
        previous.save()
    print("Old v111 -> refreshed v111 -> restart: all account tables preserved; source QA save unchanged")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode',choices=['protocol','merge','lua','save','recheck'])
    parser.add_argument('--shard',type=int,choices=range(3))
    args=parser.parse_args()
    if args.mode == 'protocol':
        assert args.shard is not None
        protocol(args.shard)
    else:
        globals()[args.mode]()
