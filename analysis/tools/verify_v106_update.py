"""Verify the staged same-version v106 update without touching player saves."""
import argparse
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
WORK = ROOT / '.runtime/v106-update'
EVIDENCE = ROOT / 'analysis/evidence/v106_update'
NAME = '金箍棒3.87-离线单机-arm32-v106.apk'
BASE = ROOT / 'build/archive/v106-13项更新版' / NAME


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['payload', 'device', 'protocol'])
    mode = parser.parse_args().mode
    if mode == 'protocol':
        program = WORK / 'payload-new'
        sys.path[:0] = [str(program), str(ROOT / 'tests')]
        names = [
            'tests.test_land_week_mail',
            'tests.test_activity_trial.TrialTests',
            'tests.test_activity_rank.RankTests.test_rank_44_skill_effects_settle_persist_and_replay_once',
            'tests.test_guild_escort_rewards.EscortRewardTests.test_ten_independent_openings_nested_native_rows_and_existing_bags_untouched',
            'tests.test_seasonal_crafting.SeasonalCraftTests.test_hundred_at_once_replay_and_independent_daily_limits',
        ]
        suite = unittest.defaultTestLoader.loadTestsFromNames(names)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        modules = 0
        for name, module in list(sys.modules.items()):
            if name.startswith('network_redirect.') and getattr(module, '__file__', None):
                assert Path(module.__file__).resolve().is_relative_to(program.resolve()), name
                modules += 1
        print(f'Validated {modules} gameplay modules loaded from the actual staged APK')
        sys.exit(not result.wasSuccessful())
    if mode == 'payload':
        from analysis.tools import verify_v106_payload as verify
        verify.WORK = WORK
    else:
        from analysis.tools import verify_v106_device as verify
        verify.WORK = WORK / 'device'
    verify.EVIDENCE = EVIDENCE
    verify.BASE = BASE
    verify.APK = WORK / NAME
    if mode == 'payload':
        verify.main()
    else:
        verify.main(expected_version=106, install_baseline=False)


if __name__ == '__main__':
    main()
