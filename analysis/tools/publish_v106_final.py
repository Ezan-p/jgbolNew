"""Publish only after package, protocol, upgrade, and cold-start UI validation."""
import hashlib,json,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from offline_android.pack_payload import collect_files
from network_redirect.summon import client_source,load_rules
WORK=ROOT/'.runtime/v106-final'
EVIDENCE=ROOT/'analysis/evidence/v106_final'
NAME='金箍棒3.87-离线单机-arm32-v106.apk'
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    read=lambda name:json.loads((EVIDENCE/name).read_text())
    build=read('build-validation.json');payload=read('payload-save-validation.json')
    device=read('device-validation.json');protocol=read('protocol-validation.json');ui=read('startup-ui-validation.json')
    assert build['apk_sha256']==payload['apk_sha256']==device['apk_sha256']==ui['apk_sha256']
    assert payload['all_database_tables_equal_after_upgrade_and_restart']
    assert payload['new_lua_checks']=={'enhance':17,'revenge':7}
    assert device['same_version_update'] and device['save_byte_identical_after_install_start_and_stop'] and device['new_program_ready']
    assert ui['cold_start_native_branding_verified'] and ui['no_external_ui_patch'] and ui['no_lua_error']
    assert ui['save_hash_after_ui']==device['baseline']['sha256']
    assert protocol['passed'] and protocol['tests']>=100 and protocol['actual_packaged_modules']>=50
    log=(EVIDENCE/'android-tests.log').read_text()
    assert 'Ran 5 tests' in log and '\nOK\n' in log
    for name,path in collect_files().items():
        if name!='network_redirect/login.html':assert digest(path)==digest(WORK/'payload-new'/name),'Source changed: '+name
    assert client_source(load_rules())==(WORK/'payload-new/offline_client.lua').read_text()
    assert digest(ROOT/'offline_android/native/offline.c')==build['native_source_sha256']
    assert digest(WORK/'liboffline.so')==build['native_adapter_sha256']
    latest=ROOT/'build'/NAME
    archived=ROOT/build['previous_release_archive']/NAME
    assert digest(latest)==digest(archived)==build['baseline_sha256']
    assert digest(WORK/NAME)==build['apk_sha256']
    notes=WORK/'v106更新说明.txt'
    assert build['apk_sha256'] in notes.read_text() and '25项' in notes.read_text()
    for path in [WORK/NAME.replace('.apk','.manifest.json'),WORK/(NAME+'.sha256'),WORK/(NAME+'.idsig'),notes,WORK/NAME]:
        target=ROOT/'build'/path.name;temporary=target.with_name(target.name+'.publishing')
        shutil.copy2(path,temporary);assert digest(temporary)==digest(path);temporary.replace(target)
    report=dict(apk=str(latest.relative_to(ROOT)),apk_sha256=digest(latest),published=True,all_25_changes=True,
      same_version_upgrade_verified=True,previous_release_archive=build['previous_release_archive'],
      packaged_protocol_tests=protocol['tests'],native_startup_screenshot='startup-home.png')
    (EVIDENCE/'published-release.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
