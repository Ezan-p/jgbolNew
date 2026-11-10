"""Publish the verified v110 refresh, retaining the archived original and v111."""
import json
import shutil
import zipfile
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))

from analysis.tools.build_v110_refresh_20261110 import (
    ROOT, WORK, EVIDENCE, OUTPUT, BASE, LATEST, ARCHIVE, BASE_SHA, LATEST_SHA, digest, report)


def main():
    raise RuntimeError("Target corrected to v111; use publish_v111_ten_updates.py")
    sha = digest(OUTPUT.read_bytes())
    names = ['build-validation', 'scope-validation', 'protocol-validation',
             'lua-validation', 'payload-save-validation', 'device-validation']
    reports = {n:json.loads((EVIDENCE/(n+'.json')).read_text()) for n in names}
    assert all(r['apk_sha256']==sha for r in reports.values())
    assert reports['build-validation']['version_code']==110
    for name in ('scope-validation','protocol-validation','lua-validation','payload-save-validation','device-validation'):
        assert reports[name]['passed'], name
    assert reports['protocol-validation']['failures']==reports['protocol-validation']['errors']==reports['protocol-validation']['skipped']==0
    assert reports['device-validation']['startup_screenshot_reviewed']
    assert reports['lua-validation']['prelogin_label']=='v110'
    assert reports['payload-save-validation']['all_tables_equal_after_restart']
    assert digest(BASE.read_bytes())==BASE_SHA
    assert digest((ARCHIVE/BASE.name).read_bytes())==BASE_SHA
    assert digest(LATEST.read_bytes())==LATEST_SHA
    # Publish only the exact candidate already exercised on the QA device.
    shutil.copy2(OUTPUT, BASE)
    assert digest(BASE.read_bytes())==sha
    for suffix in ('.manifest.json','.apk.sha256','.apk.idsig'):
        source=OUTPUT.with_suffix(suffix)
        if source.exists():
            shutil.copy2(source,BASE.with_suffix(suffix))
    archive=BASE.with_suffix('.apk.zip')
    temp=WORK/'distribution.zip'
    with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as z:
        z.write(BASE,BASE.name)
    with zipfile.ZipFile(temp) as z:
        assert z.testzip() is None and digest(z.read(BASE.name))==sha
    shutil.copy2(temp,archive)
    drift=[name for name,h in reports['build-validation']['source_hashes'].items()
           if digest((ROOT/name).read_bytes())!=h]
    report('published-release',dict(published=True,apk_sha256=sha,
        apk_bytes=BASE.stat().st_size(),version_code=110,version_name='3.87-offline.10',
        downloads=[str(p.relative_to(ROOT)) for p in (BASE,archive)],
        prior_v110_archived=str(ARCHIVE.relative_to(ROOT)),prior_v111_preserved=True,
        feature_groups=10,packaged_protocol_tests=reports['protocol-validation']['tests'],
        qa_same_version_upgrade_verified=True,physical_device_tested=False,
        source_changes_after_snapshot=drift))
    print('Published',BASE.name,sha)


if __name__=='__main__':
    main()
