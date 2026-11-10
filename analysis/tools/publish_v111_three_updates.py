"""Replace the local v111 distribution with the exact verified three-update APK."""
import json
from pathlib import Path
import shutil
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from analysis.tools.build_v111_three_updates import WORK,EVIDENCE,OUTPUT,BASE,BASE_SHA,ARCHIVE,digest,report


def main():
    sha=digest(OUTPUT.read_bytes())
    reports={name:json.loads((EVIDENCE/(name+'.json')).read_text()) for name in (
        'build-validation','scope-validation','protocol-validation','lua-validation','payload-save-validation')}
    assert all(r['apk_sha256']==sha for r in reports.values())
    assert all(reports[n]['passed'] for n in reports if n!='build-validation')
    protocol=reports['protocol-validation']
    assert protocol['failures']==protocol['errors']==protocol['skipped']==0
    assert reports['lua-validation']['abyss_keypad_regression_passed']
    assert reports['payload-save-validation']['all_tables_equal_after_restart']
    assert digest(BASE.read_bytes())==BASE_SHA
    assert digest((ARCHIVE/BASE.name).read_bytes())==BASE_SHA
    device=json.loads((EVIDENCE/'device-validation.json').read_text())
    assert device['apk_sha256']==sha
    assert device['passed'] and device['same_version_replacement_verified']
    assert device['complete_save_preserved_after_install'] and device['installed_apk_hash_verified']
    # Screenshot review is recorded separately from install/runtime verification.
    preserved={str(p.relative_to(ROOT)):digest(p.read_bytes())
               for p in (ROOT/'build').glob('*.apk') if p!=BASE}
    for suffix in ('.apk','.manifest.json','.apk.sha256','.apk.idsig'):
        source=OUTPUT.with_suffix(suffix)
        if source.exists():shutil.copy2(source,BASE.with_suffix(suffix))
    distribution=WORK/'distribution.zip'
    with zipfile.ZipFile(distribution,'w',zipfile.ZIP_DEFLATED) as z:
        z.write(OUTPUT,OUTPUT.name)
    with zipfile.ZipFile(distribution) as z:
        assert z.testzip() is None and digest(z.read(OUTPUT.name))==sha
    shutil.copy2(distribution,BASE.with_suffix('.apk.zip'))
    assert digest(BASE.read_bytes())==sha
    assert all(digest((ROOT/p).read_bytes())==h for p,h in preserved.items())
    report('published-release',dict(published=True,apk_sha256=sha,apk_bytes=BASE.stat().st_size,
        version_code=111,version_name='3.87-offline.11',package=reports['build-validation']['package'],
        downloads=[str(p.relative_to(ROOT)) for p in (BASE,BASE.with_suffix('.apk.zip'))],
        prior_v111_archived=str(ARCHIVE.relative_to(ROOT)),other_apks_preserved=True,
        feature_groups=3,total_gift_codes=100,packaged_protocol_tests=protocol['tests'],
        old_save_compatibility_verified=True,device_validation_status=device['status'],
        qa_same_version_upgrade_verified=device.get('same_version_replacement_verified',False),
        startup_ui_verified=device.get('startup_ui_verified',False),physical_device_tested=False))
    print('Published',BASE.name,sha)


if __name__=='__main__':
    main()
