"""Verify the repair's actual packaged modules, old-save compatibility and QA install."""
import argparse
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v106_stone_fix import APK, BASE, WORK, EVIDENCE


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('payload', 'protocol', 'device'))
    mode = parser.parse_args().mode
    if mode == 'protocol':
        program = WORK / 'program'
        sys.path[:0] = [str(program), str(ROOT / 'tests')]
        result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName('test_equipment'))
        from network_redirect import equipment
        assert Path(equipment.__file__).resolve().is_relative_to(program.resolve())
        build = json.loads((EVIDENCE / 'build-validation.json').read_text())
        (EVIDENCE / 'packaged-tests.json').write_text(json.dumps(dict(
            apk_sha256=build['apk_sha256'], passed=result.wasSuccessful(), tests=result.testsRun,
            module=str(Path(equipment.__file__).relative_to(ROOT))), indent=2) + '\n')
        raise SystemExit(not result.wasSuccessful())
    if mode == 'device':
        from analysis.tools import verify_v106_device as verify
        verify.WORK = WORK / 'device'
    else:
        from analysis.tools import verify_v106_payload as verify
        verify.WORK = WORK
    verify.APK, verify.BASE, verify.EVIDENCE = APK, BASE, EVIDENCE
    if mode == 'device':
        verify.main(expected_version=106, install_baseline=False)
    else:
        verify.main()
        from lupa.lua51 import LuaRuntime
        checks = LuaRuntime().execute((ROOT/'tests/stone_refine_client_regression.lua').read_text(),
                                     (WORK/'payload-new/network_redirect/equipment_client.lua').read_text())
        assert len(checks) == 17
        print('Packaged stone client:', len(checks), 'checks passed')


if __name__ == '__main__':
    main()
