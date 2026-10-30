"""Validate the staged 25-item v106 from its packaged files."""
import argparse,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
WORK=ROOT/'.runtime/v106-final'
EVIDENCE=ROOT/'analysis/evidence/v106_final'
NAME='金箍棒3.87-离线单机-arm32-v106.apk'
BASE=ROOT/'build/archive/v106-19项更新版'/NAME

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['payload','device','protocol'])
    mode=parser.parse_args().mode
    if mode=='protocol':
        program=WORK/'payload-new'
        sys.path[:0]=[str(program),str(ROOT/'tests')]
        names=['tests.test_equipment','tests.test_guild_store','tests.test_guild',
          'tests.test_small_bun_contribution','tests.test_activity_rape',
          'tests.test_journey.JourneyTests.test_eat_and_buy_resource_item_and_limits',
          'tests.test_land_week_mail','tests.test_activity_trial.TrialTests',
          'tests.test_activity_rank.RankTests.test_rank_44_skill_effects_settle_persist_and_replay_once',
          'tests.test_guild_escort_rewards.EscortRewardTests.test_ten_independent_openings_nested_native_rows_and_existing_bags_untouched',
          'tests.test_seasonal_crafting.SeasonalCraftTests.test_hundred_at_once_replay_and_independent_daily_limits']
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names))
        modules=0
        for name,module in list(sys.modules.items()):
            if name.startswith('network_redirect.') and getattr(module,'__file__',None):
                assert Path(module.__file__).resolve().is_relative_to(program.resolve()),name
                modules+=1
        (EVIDENCE/'protocol-validation.json').write_text(json.dumps(dict(passed=result.wasSuccessful(),tests=result.testsRun,
            errors=len(result.errors),failures=len(result.failures),actual_packaged_modules=modules),indent=2)+'\n')
        print('Gameplay modules loaded from staged APK:',modules)
        sys.exit(not result.wasSuccessful())
    if mode=='payload':
        from analysis.tools import verify_v106_payload as verify
        verify.WORK=WORK
    else:
        from analysis.tools import verify_v106_device as verify
        verify.WORK=WORK/'device'
    verify.EVIDENCE=EVIDENCE;verify.BASE=BASE;verify.APK=WORK/NAME
    if mode=='device':
        verify.main(expected_version=106,install_baseline=False)
        return
    verify.main()
    from lupa.lua51 import LuaRuntime
    checks={}
    for name,fixture,adapter in [('enhance','equipment_enhance_client_regression.lua','equipment_client.lua'),
                               ('revenge','rape_revenge_client_regression.lua','rape_client.lua')]:
        vm=LuaRuntime()
        cases=vm.execute((ROOT/'tests'/fixture).read_text(),(WORK/'payload-new/network_redirect'/adapter).read_text())
        checks[name]=len(cases)
    path=EVIDENCE/'payload-save-validation.json'
    report=json.loads(path.read_text());report.update(new_lua_checks=checks)
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('New packaged Lua checks:',checks)
if __name__=='__main__':main()
