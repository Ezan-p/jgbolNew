"""Run release and new-feature checks against the candidate test APK payload."""
import hashlib
import io
import json
from pathlib import Path
import sys
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / '.runtime/v111-test/program'
EVIDENCE = ROOT / 'analysis/evidence/v111_test'
APK = ROOT / '.runtime/v111-test/金箍棒ol测试版-v111.apk'
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
    from analysis.tools.verify_v111 import SUITES
    # Build-tool imports prepend the workspace. Restore the artifact before
    # loading any gameplay module, and verify the package origin immediately.
    sys.path.insert(0, str(PROGRAM))
    import network_redirect
    assert Path(network_redirect.__file__).resolve().is_relative_to(PROGRAM.resolve())
    selected = sorted(set(SUITES + [
        'test_network_time', 'test_trusted_game_clock', 'test_seasonal_weekly',
        'test_activity_moon', 'test_activity_rice', 'test_seasonal_crafting',
        'test_activity_save_monkey', 'test_activity_fish', 'test_fish_client',
        'test_activity_home', 'test_home_ordeal', 'test_tianxian_token',
        'test_pets', 'test_pet_acquisition', 'test_pet_quality', 'test_pet_quality_client',
        'test_equipment_instances', 'test_land_card_caps']))
    if '--only' in sys.argv:
        selected = sys.argv[sys.argv.index('--only') + 1:]
    def cases(node):
        if isinstance(node, unittest.TestSuite):
            for child in node:
                yield from cases(child)
        else:
            yield node
    unique = {case.id().removeprefix('tests.'): case for case in
              cases(unittest.defaultTestLoader.loadTestsFromNames(selected))}
    prior = {}
    shard = int(sys.argv[sys.argv.index('--shard')+1]) if '--shard' in sys.argv else None
    if shard is not None:
        unique = {name: case for name, case in unique.items()
                  if int(hashlib.sha256(name.encode()).hexdigest(),16) % 3 == shard}
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
    name = f'protocol-shard-{shard}' if shard is not None else 'protocol-validation'
    if '--report-name' in sys.argv:
        name = sys.argv[sys.argv.index('--report-name') + 1]
    (EVIDENCE / (name + '.json')).write_text(json.dumps(report, indent=2) + '\n')
    raise SystemExit(not result.wasSuccessful() or bool(result.skipped))


if __name__ == '__main__':
    main()
