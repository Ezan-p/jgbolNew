"""Run disjoint APK test shards in separate processes and retain every result."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v109 import EVIDENCE


def main():
    jobs = []
    for shard in range(4):
        log = (EVIDENCE / f'protocol-shard-{shard}.log').open('w')
        process = subprocess.Popen([sys.executable, '-u', str(ROOT / 'analysis/tools/verify_v109.py'),
                                    'protocol', '--shard', str(shard)], stdout=log, stderr=subprocess.STDOUT)
        jobs.append((shard, process, log))
    codes = []
    for shard, process, log in jobs:
        codes.append(process.wait())
        log.close()
        print('Finished shard', shard, 'exit', codes[-1], flush=True)
    reports = [json.loads((EVIDENCE / f'protocol-shard-{n}.json').read_text()) for n in range(4)]
    assert len({r['apk_sha256'] for r in reports}) == 1
    ids = [ident for r in reports for ident in r['test_ids']]
    assert len(ids) == len(set(ids)) == sum(r['tests'] for r in reports)
    report = dict(apk_sha256=reports[0]['apk_sha256'], passed=all(r['passed'] for r in reports),
                  tests=len(ids), errors=sum(r['errors'] for r in reports),
                  failures=sum(r['failures'] for r in reports), skipped=sum(r['skipped'] for r in reports),
                  actual_packaged_modules=min(r['actual_packaged_modules'] for r in reports),
                  suites=reports[0]['suites'], shards=4,
                  failed_test_ids=[ident for r in reports for ident in r['failed_test_ids']],
                  test_ids=ids)
    (EVIDENCE / 'protocol-validation.json').write_text(json.dumps(report, indent=2)+'\n')
    (EVIDENCE / 'protocol-tests.log').write_text('\n'.join(
        (EVIDENCE / f'protocol-shard-{n}.log').read_text() for n in range(4)))
    print(json.dumps({k:v for k,v in report.items() if k not in ('test_ids','suites')}, indent=2), flush=True)
    raise SystemExit(not report['passed'])


if __name__ == '__main__':
    main()
