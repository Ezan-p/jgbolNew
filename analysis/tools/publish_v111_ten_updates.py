"""Publish the verified v111 refresh, retaining the archived original and v110."""
import json
import shutil
import zipfile
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))

from analysis.tools.build_v111_ten_updates import (
    ROOT, WORK, EVIDENCE, OUTPUT, BASE, LATEST, ARCHIVE, BASE_SHA, LATEST_SHA, digest, report)


def main():
    sha = digest(OUTPUT.read_bytes())
    names = ['build-validation', 'scope-validation', 'protocol-validation',
             'lua-validation', 'payload-save-validation', 'device-validation', 'validated-candidate-delta']
    reports = {n:json.loads((EVIDENCE/(n+'.json')).read_text()) for n in names}
    assert all(r['apk_sha256']==sha for r in reports.values())
    assert reports['build-validation']['version_code']==111
    for name in ('scope-validation','protocol-validation','lua-validation','payload-save-validation','device-validation'):
        assert reports[name]['passed'], name
    assert reports['protocol-validation']['failures']==reports['protocol-validation']['errors']==reports['protocol-validation']['skipped']==0
    assert reports['device-validation']['startup_screenshot_reviewed']
    assert reports['lua-validation']['prelogin_label']=='v111'
    assert reports['validated-candidate-delta']['passed']
    assert reports['payload-save-validation']['all_tables_equal_after_restart']
    assert digest(BASE.read_bytes()) in (BASE_SHA, sha)
    assert digest((ARCHIVE/BASE.name).read_bytes())==BASE_SHA
    assert digest(LATEST.read_bytes()) in (LATEST_SHA, sha)
    old110=ROOT/'build/金箍棒ol离线正式版v110.apk'
    old110_sha=digest(old110.read_bytes())
    # Publish only the exact candidate already exercised on the QA device.
    shutil.copy2(OUTPUT, BASE)
    assert digest(BASE.read_bytes())==sha
    for suffix in ('.manifest.json','.apk.sha256','.apk.idsig'):
        source=OUTPUT.with_suffix(suffix)
        if source.exists():
            shutil.copy2(source,BASE.with_suffix(suffix))
    archive=BASE.with_suffix('.apk.zip')
    temp=WORK/'distribution.zip'
    if not temp.exists():
        with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as z:
            z.write(BASE,BASE.name)
    with zipfile.ZipFile(temp) as z:
        assert z.testzip() is None and digest(z.read(BASE.name))==sha
    shutil.copy2(temp,archive)
    drift=[name for name,h in reports['build-validation']['source_hashes'].items()
           if digest((ROOT/name).read_bytes())!=h]
    assert digest(old110.read_bytes())==old110_sha
    report('published-release',dict(published=True,apk_sha256=sha,
        apk_bytes=BASE.stat().st_size,version_code=111,version_name='3.87-offline.11',
        downloads=[str(p.relative_to(ROOT)) for p in (BASE,archive)],
        prior_v111_archived=str(ARCHIVE.relative_to(ROOT)),prior_v110_preserved=True,
        feature_groups=10,packaged_protocol_tests=reports['protocol-validation']['tests'],
        qa_same_version_upgrade_verified=True,physical_device_tested=False,
        startup_ui_verified=reports['device-validation']['startup_ui_verified'],
        device_validation_status=reports['device-validation']['status'],
        source_changes_after_snapshot=drift))
    print('Published',BASE.name,sha)


if __name__=='__main__':
    main()
