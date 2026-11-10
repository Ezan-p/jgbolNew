"""Reuse proven release harnesses against the exact reversioned v111 APK."""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['lua', 'runtime', 'upgrade'])
    mode = parser.parse_args().mode
    harness = ROOT / f'analysis/tools/verify_v110_test_refresh_{mode}.py'
    source = harness.read_text()
    source = source.replace('build_v110_test_refresh', 'reversion_v111_test')
    source = source.replace('.runtime/v110-test-refresh-20261110', '.runtime/v111-test-version-20261110')
    source = source.replace('analysis/evidence/v110-test-refresh-20261110', 'analysis/evidence/v111-test-version-20261110')
    source = source.replace('金箍棒ol测试版-v110-20261110整合更新.apk', '金箍棒ol测试版-v111.apk')
    source = source.replace("'v110'", "'v111'").replace('prelogin_branding_v110', 'prelogin_branding_v111')
    source = source.replace('v110整合升级检查', 'v111十项更新升级检查')
    exec(compile(source, str(harness), 'exec'), {'__name__':'__main__', '__file__':str(harness)})


if __name__ == '__main__':
    main()
