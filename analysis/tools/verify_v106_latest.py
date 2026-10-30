"""Validate the five new feature groups using the actual staged APK."""
import argparse
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v106_latest import WORK, EVIDENCE, ARCHIVE, NAME, FORMAL


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['payload', 'protocol', 'device', 'ui'])
    mode = parser.parse_args().mode
    if mode == 'protocol':
        program = WORK / 'payload-new'
        sys.path[:0] = [str(program), str(ROOT / 'tests')]
        names = ['test_fate_rebuild', 'test_guild_store', 'test_guild', 'test_activity_fish',
                 'test_item_rewards', 'test_activity_moon', 'test_activity_rice',
                 'test_seasonal_crafting', 'test_activity_pavilion', 'test_immortal',
                 'test_reborn', 'test_combat', 'test_combat_engine', 'test_combat_loadout',
                 'test_combat_power', 'test_combat_essence_integrity', 'test_combat_round_limit',
                 'test_summon', 'test_guild_escort_rewards', 'test_formation', 'test_gift_codes']
        result = unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromNames(names))
        modules = 0
        for name, module in list(sys.modules.items()):
            if name.startswith('network_redirect.') and getattr(module, '__file__', None):
                assert Path(module.__file__).resolve().is_relative_to(program.resolve()), name
                modules += 1
        build = json.loads((EVIDENCE / 'build-validation.json').read_text())
        report = dict(apk_sha256=build['apk_sha256'], passed=result.wasSuccessful(),
                      tests=result.testsRun, errors=len(result.errors), failures=len(result.failures),
                      actual_packaged_modules=modules, suites=names)
        (EVIDENCE / 'protocol-validation.json').write_text(json.dumps(report, indent=2) + '\n')
        sys.exit(not result.wasSuccessful())
    if mode == 'ui':
        from analysis.tools import verify_v106_startup_ui as verify
        verify.EVIDENCE = EVIDENCE
        verify.main()
        return
    if mode == 'device':
        from analysis.tools import verify_v106_device as verify
        verify.WORK = WORK / 'device'
    else:
        from analysis.tools import verify_v106_payload as verify
        verify.WORK = WORK
    verify.BASE = ARCHIVE / FORMAL
    verify.APK = WORK / NAME
    verify.EVIDENCE = EVIDENCE
    if mode == 'device':
        verify.main(expected_version=106, install_baseline=False)
        path = EVIDENCE / 'device-validation.json'
        report = json.loads(path.read_text())
        report['date'] = '2026-10-31'
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
        return
    allowed = json.loads((WORK / 'payload-new/server_config/fate_rebuild_attributes.json').read_text())
    verify.main(allowed_new_cortege_fields=allowed)
    from lupa.lua51 import LuaRuntime
    checks = {}
    for name, fixture, adapter in [
        ('enhance', 'equipment_enhance_client_regression.lua', 'equipment_client.lua'),
        ('revenge', 'rape_revenge_client_regression.lua', 'rape_client.lua')]:
        checks[name] = len(LuaRuntime().execute((ROOT / 'tests' / fixture).read_text(),
                          (WORK / 'payload-new/network_redirect' / adapter).read_text()))
    path = EVIDENCE / 'payload-save-validation.json'
    report = json.loads(path.read_text())
    report['retained_lua_checks'] = checks
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
