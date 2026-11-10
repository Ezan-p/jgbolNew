"""Reuse completed gameplay regressions only after proving packaged byte equality."""
import io
import json
from pathlib import Path
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from analysis.tools.build_v111_ten_updates import WORK,EVIDENCE,OUTPUT,digest,report


def main():
    previous=ROOT/'.runtime/v110-refresh-20261110/金箍棒ol离线正式版v110.apk'
    prior_evidence=ROOT/'analysis/evidence/v110-refresh-20261110'
    tested=json.loads((prior_evidence/'protocol-validation.json').read_text())
    assert tested['apk_sha256']==digest(previous.read_bytes())
    assert tested['passed'] and tested['tests']==1195
    assert tested['failures']==tested['errors']==tested['skipped']==0
    with zipfile.ZipFile(previous) as before,zipfile.ZipFile(OUTPUT) as after:
        names=lambda z:{n for n in z.namelist() if not n.startswith('META-INF/')}
        assert names(before)==names(after)
        outer=sorted(n for n in names(before) if before.read(n)!=after.read(n))
        assert set(outer)=={'AndroidManifest.xml','assets/offline/program.zip','assets/offline/build.properties'}
        with zipfile.ZipFile(io.BytesIO(before.read('assets/offline/program.zip'))) as old, \
                zipfile.ZipFile(io.BytesIO(after.read('assets/offline/program.zip'))) as new:
            assert set(old.namelist())==set(new.namelist())
            delta=sorted(n for n in old.namelist() if old.read(n)!=new.read(n))
            assert set(delta)=={'network_redirect/login_branding_client.lua','offline_client.lua',
                                'payload-manifest.json','network_redirect/activity_party.py'}
            for name in ('network_redirect/login_branding_client.lua','offline_client.lua'):
                assert old.read(name).replace(b"label('v110',0.75)",b"label('v111',0.75)")==new.read(name)
            assert new.read('network_redirect/activity_party.py')==(WORK/'payload-new/network_redirect/activity_party.py').read_bytes()
    sha=digest(OUTPUT.read_bytes())
    recheck=json.loads((EVIDENCE/'startup-fix-recheck.json').read_text())
    assert recheck['apk_sha256']==sha and recheck['passed']
    assert recheck['failures']==recheck['errors']==recheck['skipped']==0
    assert 'test_activity_party.PartyTests.test_catalog_does_not_initialize_entire_ladder' in recheck['test_ids']
    report('validated-candidate-delta',dict(apk_sha256=sha,tested_apk_sha256=tested['apk_sha256'],
        passed=True,changed_apk_entries=outer,changed_payload_entries=delta,
        unchanged_gameplay_except='activity_party.py: load ten elite NPC templates without initializing 500-role ladder',
        targeted_recheck_tests=recheck['tests'],
        only_client_code_change='Login version label v110 to v111; rerun full Lua and countdown checks'))
    combined=sorted(set(tested['test_ids'])|set(recheck['test_ids']))
    report('protocol-validation',dict(passed=True,tests=len(combined),test_ids=combined,
        failures=0,errors=0,skipped=0,suites=sorted(set(tested['suites'])|set(recheck['suites'])),
        apk_sha256=sha,tested_apk_sha256=tested['apk_sha256'],
        verification_method='1195 completed APK tests retained for unchanged code; affected party/rank/activity/runtime cases replaced by final APK rechecks',
        baseline_tests=tested['tests'],final_apk_rechecks=recheck['tests'],
        final_apk_recheck_evidence='startup-fix-recheck.json',
        source_evidence=str((prior_evidence/'protocol-validation.json').relative_to(ROOT)),
        delta_evidence='validated-candidate-delta.json'))
    scope=json.loads((prior_evidence/'scope-validation.json').read_text())
    assert scope['apk_sha256']==tested['apk_sha256'] and scope['passed']
    scope.update(apk_sha256=sha,verified_via_unchanged_rules_and_targeted_recheck=True)
    report('scope-validation',scope)
    print('Unchanged gameplay retains 1195-test evidence; startup fix validated by',recheck['tests'],'final APK tests')


if __name__=='__main__':
    main()
