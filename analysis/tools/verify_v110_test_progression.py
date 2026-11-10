"""Reuse the full allowance-consumption harness on the v110 test APK payload."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HARNESS = ROOT / 'analysis/tools/verify_v108_test.py'


def main():
    source = HARNESS.read_text().replace('.runtime/v108-test/program', '.runtime/v110-test/program')
    source = source.replace('analysis/evidence/v108_test', 'analysis/evidence/v110_test')
    exec(compile(source, str(HARNESS), 'exec'), dict(__name__='__main__', __file__=str(HARNESS)))
    destination = ROOT / 'analysis/evidence/v110_test/progression-validation.json'
    report = json.loads(destination.read_text())
    report['apk_sha256'] = hashlib.sha256((ROOT / '.runtime/v110-test/金箍棒ol测试版-v110.apk').read_bytes()).hexdigest()
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
