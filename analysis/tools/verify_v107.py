"""Verify v107's actual APK payload, fourteen update groups and save compatibility."""
import argparse
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v107 import BASE, OUTPUT as APK, WORK, EVIDENCE

SUITES = [
    'test_equipment', 'test_equipment_crafting', 'test_activity_rank', 'test_market',
    'test_activity_home', 'test_tianxian_token', 'test_activity_pavilion',
    'test_taixu_shop', 'test_activity_taixu', 'test_abyss_shop', 'test_activity_abyss',
    'test_abyss_balance', 'test_activity_land_tower', 'test_activity_land',
    'test_activity_land_players', 'test_land_week_mail', 'test_activity_babel',
    'test_guild_war_feast', 'test_guild', 'test_guild_social_npc',
    'test_activity_party', 'test_party_rank_mail', 'test_system_mail', 'test_qiankun_bags',
    'test_vip', 'test_item_rewards', 'test_activity', 'test_daily',
    'test_achievements', 'test_combat_engine', 'test_combat_lanes',
    'test_combat_termination', 'test_battle_replay', 'test_combat',
    'test_combat_loadout', 'test_combat_power', 'test_reborn', 'test_formation',
    'test_fate_rebuild', 'test_guild_store', 'test_activity_fish', 'test_activity_moon',
    'test_activity_rice', 'test_seasonal_crafting', 'test_summon', 'test_gift_codes',
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['payload', 'protocol', 'lua'])
    mode = parser.parse_args().mode
    if mode == 'payload':
        from analysis.tools import verify_v106_payload as verify
        verify.BASE, verify.APK, verify.WORK, verify.EVIDENCE = BASE, APK, WORK, EVIDENCE
        verify.main()
        return
    program = WORK / 'payload-new'
    assert program.is_dir(), 'Run payload verification first'
    sys.path[:0] = [str(program), str(ROOT / 'tests')]
    build = json.loads((EVIDENCE / 'build-validation.json').read_text())
    if mode == 'protocol':
        result = unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromNames(SUITES))
        modules = 0
        for name, module in list(sys.modules.items()):
            if name.startswith('network_redirect.') and getattr(module, '__file__', None):
                assert Path(module.__file__).resolve().is_relative_to(program.resolve()), name
                modules += 1
        report = dict(apk_sha256=build['apk_sha256'], passed=result.wasSuccessful(),
                      tests=result.testsRun, errors=len(result.errors), failures=len(result.failures),
                      actual_packaged_modules=modules, suites=SUITES)
        (EVIDENCE / 'protocol-validation.json').write_text(json.dumps(report, indent=2) + '\n')
        raise SystemExit(not result.wasSuccessful())
    from lupa.lua51 import LuaRuntime
    from network_redirect import activity_pavilion, summon
    checks = {}
    for name, fixture, adapter in [
        ('stone', 'stone_refine_client_regression.lua', 'equipment_client.lua'),
        ('enhance', 'equipment_enhance_client_regression.lua', 'equipment_client.lua'),
        ('market', 'market_client_regression.lua', 'market_client.lua')]:
        value = LuaRuntime().execute((ROOT / 'tests' / fixture).read_text(),
                                    (program / 'network_redirect' / adapter).read_text())
        checks[name] = value if isinstance(value, (str, int, bool)) else len(value)
    patch = (program / 'network_redirect/pavilion_client.lua').read_text().replace(
        '__PAVILION_TABLES__', summon.lua(activity_pavilion.client_tables()))
    checks['pavilion'] = LuaRuntime().execute((ROOT / 'tests/pavilion_client_regression.lua').read_text().replace('-- INSTALL_PATCH', patch))
    bundle = (program / 'offline_client.lua').read_text()
    LuaRuntime().execute('assert(loadstring(...))', bundle)
    assert "label('v107',0.75)" in bundle and "label('v106',0.75)" not in bundle
    checks['bundle_compiles_and_home_version_is_v107'] = True
    (EVIDENCE / 'lua-validation.json').write_text(json.dumps(dict(apk_sha256=build['apk_sha256'], checks=checks), ensure_ascii=False, indent=2) + '\n')
    print(checks)


if __name__ == '__main__':
    main()
