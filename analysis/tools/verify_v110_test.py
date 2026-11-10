"""Run release and new-feature checks against the candidate test APK payload."""
import hashlib
import io
import json
from pathlib import Path
import sys
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / '.runtime/v110-test/program'
EVIDENCE = ROOT / 'analysis/evidence/v110_test'
APK = ROOT / '.runtime/v110-test/金箍棒ol测试版-v110.apk'
sys.path.insert(0, str(ROOT))
import offline_android
offline_android.__path__.insert(0, str(PROGRAM / 'offline_android'))
sys.path[:0] = [str(PROGRAM), str(ROOT / 'tests'), str(ROOT), '/private/tmp/qmxy-battle-test-deps']


def main():
    from offline_android.pack_payload import verify_payload
    sys.path.insert(0, str(PROGRAM))
    with zipfile.ZipFile(APK) as apk:
        with zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as packed:
            for name in packed.namelist():
                assert packed.read(name) == (PROGRAM / name).read_bytes(), name
    verify_payload(PROGRAM)
    from lupa.lua51 import LuaRuntime
    LuaRuntime().execute('assert(loadstring(...))', (PROGRAM / 'offline_client.lua').read_text())
    additions = ['test_game_clock_resume', 'test_game_clock_client', 'test_guild_secret',
        'test_guild_secret_client', 'test_activity_arena_roster', 'test_activity_land_balance',
        'test_activity_land', 'test_activity_land_tower', 'test_activity_land_players',
        'test_land_week_mail', 'test_activity_party', 'test_activity_treasure',
        'test_treasure_client', 'test_activity_abyss', 'test_equipment_recycle_client',
        'test_equipment_crafting', 'test_equipment', 'test_battle_replay',
        'test_guild_activity_fixes', 'test_guild_npc_combat', 'test_guild',
        'test_guild_management_contract', 'test_guild_quota_restore']
    # For a payload update, focus on changed systems and their shared contracts.
    # Unchanged v110 systems are additionally covered by any completed baseline checks.
    selected = sorted(set(additions + ['test_summon', 'test_game_clock', 'test_time_guard',
        'test_activity_clock_boundaries', 'test_activity_entry_client',
        'test_request_wait', 'test_request_timing_client', 'test_resource_preload']))
    def cases(node):
        if isinstance(node, unittest.TestSuite):
            for child in node:
                yield from cases(child)
        else:
            yield node
    unique = {case.id().removeprefix('tests.'): case for case in
              cases(unittest.defaultTestLoader.loadTestsFromNames(selected))}
    prior = {}
    if '--resume-baseline-log' in sys.argv:
        log = Path(sys.argv[sys.argv.index('--resume-baseline-log') + 1])
        prior = json.loads(log.with_suffix('.json').read_text())
        assert prior['apk_sha256'] == hashlib.sha256(APK.read_bytes()).hexdigest()
        assert not prior['failures']
        for name in prior['test_ids']:
            unique.pop(name, None)
    result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(unique.values()))
    loaded = []
    for name, module in list(sys.modules.items()):
        if name.startswith('network_redirect.') and getattr(module, '__file__', None):
            assert Path(module.__file__).resolve().is_relative_to(PROGRAM.resolve()), name
            loaded.append(name)
    report = dict(apk_sha256=hashlib.sha256(APK.read_bytes()).hexdigest(),
        passed=result.wasSuccessful(), tests=result.testsRun + len(prior.get('test_ids', [])), errors=len(result.errors),
        failures=len(result.failures), skipped=len(result.skipped), actual_packaged_modules=loaded,
        suites=selected, test_ids=prior.get('test_ids', []) + list(unique),
        completed_baseline_tests=len(prior.get('test_ids', [])),
        failed_test_ids=[case.id() for case, _ in result.errors + result.failures])
    (EVIDENCE / 'protocol-validation.json').write_text(json.dumps(report, indent=2) + '\n')
    raise SystemExit(not result.wasSuccessful() or bool(result.skipped))


if __name__ == '__main__':
    main()
