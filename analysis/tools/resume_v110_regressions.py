"""Resume a partial shard using recorded successful test IDs and disjoint workers."""
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[2]
EVIDENCE=ROOT/'analysis/evidence/v110'
CANDIDATE=ROOT/'.runtime/v110-build-r2'
EXCLUDED='test_activity_babel.BabelTests.test_late_floors_full_wire_loot_budget_and_terminal_once'


def main(pid):
    command=subprocess.check_output(['ps','-p',str(pid),'-o','command='],text=True)
    assert 'verify_v110.py protocol --shard 2' in command and 'v110-build-r2' in command
    os.kill(pid,signal.SIGTERM)
    progress=EVIDENCE/'protocol-shard-2.log'
    saved=EVIDENCE/'protocol-shard-2-before-continuation.log'
    progress.rename(saved)
    contents=saved.read_text()
    assert '... FAIL' not in contents and '... ERROR' not in contents
    completed={f'{cls}.{method}'.removeprefix('tests.') for method,cls in
               re.findall(r'^(test_\w+) \(([^)]+)\) \.\.\. ok$',contents,re.M)}
    sys.path[:0]=[str(CANDIDATE/'payload-new'),str(ROOT/'tests'),str(ROOT),'/private/tmp/jgbol-wait-test-deps']
    excluded_suites={'test_startup','test_network_redirect','test_android_offline_backend','test_game_server','test_login_repair'}
    suites=sorted(p.stem for p in (ROOT/'tests').glob('test_*.py') if p.stem not in excluded_suites)
    def cases(node):
        if isinstance(node,unittest.TestSuite):
            for child in node: yield from cases(child)
        else: yield node
    unique={case.id().removeprefix('tests.'):case for case in cases(unittest.defaultTestLoader.loadTestsFromNames(suites))}
    planned={name for name in unique if name!=EXCLUDED and int(hashlib.sha256(name.encode()).hexdigest(),16)%4==2}
    assert completed and completed<=planned
    remaining=sorted(planned-completed)
    jobs=[]
    for part in range(4):
        names=remaining[part::4]
        selection=EVIDENCE/f'continuation-{part}-ids.json'
        selection.write_text(json.dumps(names,indent=2)+'\n')
        log=(EVIDENCE/f'continuation-{part}.log').open('w')
        proc=subprocess.Popen([sys.executable,'-u',str(ROOT/'analysis/tools/verify_v110.py'),'protocol',
             '--candidate',str(CANDIDATE),'--only-test-ids',str(selection),
             '--report-name',f'continuation-{part}.json'],stdout=log,stderr=subprocess.STDOUT,cwd=ROOT)
        jobs.append((part,proc,log))
    print(f'Preserved {len(completed)} passed tests; continuing {len(remaining)} tests in four disjoint workers.',flush=True)
    for part,proc,log in jobs:
        code=proc.wait();log.close();print('Continuation',part,'exit',code,flush=True)
    reports=[json.loads((EVIDENCE/f'continuation-{part}.json').read_text()) for part in range(4)]
    sha=hashlib.sha256((CANDIDATE/'金箍棒3.87离线正式版v110.apk').read_bytes()).hexdigest()
    assert {r['apk_sha256'] for r in reports}=={sha}
    ids=sorted(completed)+[name for r in reports for name in r['test_ids']]
    assert len(ids)==len(set(ids)) and set(ids)==planned
    report=dict(apk_sha256=sha,passed=all(r['passed'] for r in reports),tests=len(ids),
        errors=sum(r['errors'] for r in reports),failures=sum(r['failures'] for r in reports),
        skipped=sum(r['skipped'] for r in reports),
        actual_packaged_modules=min(r['actual_packaged_modules'] for r in reports),suites=suites,
        test_ids=ids,failed_test_ids=[name for r in reports for name in r['failed_test_ids']],
        excluded_test_ids=[EXCLUDED],shard=2,resumed=True,
        previously_completed_tests=len(completed),previously_completed_ids=sorted(completed),
        previous_log=saved.name,continuation_parts=4)
    (EVIDENCE/'protocol-shard-2.json').write_text(json.dumps(report,indent=2)+'\n')
    progress.write_text(contents+'\n'+'\n'.join((EVIDENCE/f'continuation-{n}.log').read_text() for n in range(4)))
    print(json.dumps({k:v for k,v in report.items() if k not in ('test_ids','suites','previously_completed_ids')},indent=2))
    raise SystemExit(not report['passed'])


if __name__=='__main__': main(int(sys.argv[1]))
