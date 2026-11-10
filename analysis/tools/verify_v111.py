"""Regress the exact packaged v111 modules and disposable copies of old saves."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v111 import WORK, EVIDENCE, OUTPUT, BASE, digest, report

SUITES = [
    'test_activity', 'test_activity_treasure', 'test_treasure_client',
    'test_activity_abyss', 'test_abyss_shop', 'test_abyss_balance',
    'test_activity_land', 'test_activity_land_players', 'test_activity_land_tower',
    'test_activity_land_balance', 'test_land_week_mail',
    'test_activity_party', 'test_party_rank_mail', 'test_activity_arena_roster',
    'test_activity_taixu', 'test_taixu_shop',
    'test_equipment', 'test_equipment_crafting', 'test_equipment_recycle_client',
    'test_cortege_recycle', 'test_achievements', 'test_reborn', 'test_item_rewards',
    'test_game_clock', 'test_game_clock_resume', 'test_game_clock_client',
    'test_time_guard', 'test_activity_clock_boundaries', 'test_battle_replay',
    'test_activity_entry_client', 'test_summon', 'test_request_recovery',
    'test_formation', 'test_expbooks', 'test_xianyuan_fruit', 'test_xianling',
    'test_activity_nine_sky', 'test_nine_sky_battle',
]
SUITES += sorted(p.stem for p in (ROOT / 'tests').glob('test_guild*.py'))


def packaged_path():
    program = WORK / 'payload-new'
    sys.path[:0] = [str(program), str(ROOT / 'tests'),
                   '/private/tmp/qmxy-battle-test-deps', '/private/tmp/jgbol-wait-test-deps']
    return program


def protocol(names=None, shard=None):
    program = packaged_path()
    def cases(node):
        if isinstance(node, unittest.TestSuite):
            for child in node:
                yield from cases(child)
        else:
            yield node
    suite = unittest.defaultTestLoader.loadTestsFromNames(names or SUITES)
    unique = {c.id().removeprefix('tests.'): c for c in cases(suite)}
    if shard is not None:
        resume = json.loads((EVIDENCE / 'protocol-completed-prefix.json').read_text())
        assert resume['apk_sha256'] == digest(OUTPUT.read_bytes())
        assert set(resume['test_ids']) <= set(unique)
        unique = {name: case for name, case in unique.items()
                  if name not in resume['test_ids'] and int(hashlib.sha256(name.encode()).hexdigest(), 16) % 3 == shard}
    result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(unique.values()))
    modules = []
    for name, module in list(sys.modules.items()):
        if name.startswith('network_redirect.') and getattr(module, '__file__', None):
            assert Path(module.__file__).resolve().is_relative_to(program.resolve()), name
            modules.append(name)
    data = dict(apk_sha256=digest(OUTPUT.read_bytes()), passed=result.wasSuccessful(),
                tests=result.testsRun, failures=len(result.failures), errors=len(result.errors),
                skipped=len(result.skipped), suites=names or SUITES, test_ids=list(unique),
                failed_test_ids=[c.id() for c, _ in result.failures + result.errors],
                actual_packaged_modules=modules)
    report(f'protocol-shard-{shard}' if shard is not None else
           ('protocol-validation' if not names else 'protocol-recheck'), data)
    raise SystemExit(not result.wasSuccessful() or bool(result.skipped))


def resume():
    log = (EVIDENCE / 'protocol-tests.log').read_text()
    assert not re.search(r'\.\.\. (?:FAIL|ERROR|skipped)', log)
    completed = [f'{cls}.{method}'.removeprefix('tests.') for method, cls in re.findall(
        r'^(test_\w+) \(([^)]+)\) \.\.\. ok$', log, re.M)]
    assert completed and len(completed) == len(set(completed))
    report('protocol-completed-prefix', dict(apk_sha256=digest(OUTPUT.read_bytes()), passed=True,
        tests=len(completed), test_ids=completed, failures=0, errors=0, skipped=0,
        source_log='protocol-tests.log', reason='Resume remaining cases in three isolated workers'))
    print('Preserved completed tests:', len(completed))


def merge():
    packaged_path()
    def cases(node):
        if isinstance(node, unittest.TestSuite):
            for child in node:
                yield from cases(child)
        else:
            yield node.id().removeprefix('tests.')
    expected = set(cases(unittest.defaultTestLoader.loadTestsFromNames(SUITES)))
    records = [json.loads((EVIDENCE / (name + '.json')).read_text()) for name in
               ['protocol-completed-prefix', 'protocol-shard-0', 'protocol-shard-1', 'protocol-shard-2']]
    ids = []
    for item in records:
        assert item['apk_sha256'] == digest(OUTPUT.read_bytes())
        assert item['passed'] and item['failures'] == item['errors'] == item['skipped'] == 0
        ids.extend(item['test_ids'])
    assert len(ids) == len(set(ids)) and set(ids) == expected
    report('protocol-validation', dict(apk_sha256=digest(OUTPUT.read_bytes()), passed=True,
        tests=len(ids), failures=0, errors=0, skipped=0, test_ids=sorted(ids), suites=SUITES,
        sources=['protocol-completed-prefix', 'protocol-shard-0', 'protocol-shard-1', 'protocol-shard-2']))
    print('All unique packaged tests passed:', len(ids))


def lua():
    program = packaged_path()
    from lupa.lua51 import LuaRuntime
    bundle = (program / 'offline_client.lua').read_text()
    LuaRuntime().execute('assert(loadstring(...))', bundle)
    checks = {}
    source = (program / 'network_redirect/battle_replay_client.lua').read_text()
    value = LuaRuntime().execute((ROOT / 'tests/battle_replay_client_regression.lua').read_text(), source)
    checks['battle_replay'] = list(value.values()) if hasattr(value, 'values') else value
    source = (program / 'network_redirect/nine_sky_client.lua').read_text()
    harness = (ROOT / 'tests/nine_sky_client_regression.lua').read_text()
    value = LuaRuntime().execute(harness.replace('-- INSTALL_PATCH', source).replace('-- INSTALL_AGAIN', source))
    checks['nine_sky'] = list(value.values()) if hasattr(value, 'values') else value
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
    assert list(vm.globals().LABELS.values()) == ['离线版·非商业·仅供学习', 'v111', '开发者@Ezan']
    assert "label('v110',0.75)" not in bundle
    checks['prelogin_shows_v111'] = True
    checks['complete_packaged_bundle_compiles'] = True
    report('lua-validation', dict(apk_sha256=digest(OUTPUT.read_bytes()), passed=True, checks=checks))
    print(json.dumps(checks, ensure_ascii=False))


def save():
    import io
    import zipfile
    from analysis.tools.verify_v110_payload import WORKER
    from analysis.tools.verify_v105_update import database_snapshot
    from offline_android.pack_payload import verify_payload
    with zipfile.ZipFile(BASE) as apk, zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as z:
        z.extractall(WORK / 'payload-old')
    for mode in ('old', 'new'):
        verify_payload(WORK / ('payload-' + mode))
    source = ROOT / '.runtime/opening-qa/after-all-tests.sqlite3'
    source_hash = digest(source.read_bytes())
    directory = Path(tempfile.mkdtemp(prefix='save-compatibility-', dir=WORK))
    database = directory / 'game.sqlite3'
    with sqlite3.connect(source.as_uri() + '?mode=ro', uri=True) as old, sqlite3.connect(database) as new:
        old.backup(new)
    snapshots, passes = [], []
    for i, mode in enumerate(('old', 'new', 'new')):
        p = subprocess.run([sys.executable, '-I', '-c', WORKER,
                            str(WORK / ('payload-' + mode)), str(directory)],
                           capture_output=True, text=True, timeout=180)
        assert p.returncode == 0, p.stderr
        passes.append(dict(mode=mode, **json.loads(p.stdout)))
        snapshot = database_snapshot(database)
        snapshots.append(snapshot)
        (directory / f'snapshot-{i}-{mode}.json').write_text(json.dumps(
            snapshot, ensure_ascii=False, default=lambda value: {'bytes_hex': value.hex()}))
    assert snapshots[0] == snapshots[1] == snapshots[2], 'Upgrade/restart changed saved account values'
    assert source_hash == digest(source.read_bytes())
    report('payload-save-validation', dict(apk_sha256=digest(OUTPUT.read_bytes()), passed=True,
        source_qa_save_unchanged=True, existing_role_values_preserved=True, all_tables_equal_after_restart=True,
        save_load_passes=passes, evidence_save_directory=str(directory.relative_to(ROOT))))
    print('v110 -> v111 -> v111: all account tables preserved; source save unchanged')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['protocol', 'lua', 'save', 'resume', 'merge'])
    parser.add_argument('--tests', nargs='+')
    parser.add_argument('--shard', type=int, choices=range(3))
    args = parser.parse_args()
    if args.mode == 'protocol':
        protocol(args.tests, args.shard)
    else:
        globals()[args.mode]()
