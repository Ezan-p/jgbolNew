"""Stage the 25-item v106 release without replacing the current download."""
import json
from pathlib import Path
import shutil
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from analysis.tools import build_v106 as builder
from offline_android.native.build_native import build as build_native
NAME='金箍棒3.87-离线单机-arm32-v106.apk'
ARCHIVE=ROOT/'build/archive/v106-19项更新版'
WORK=ROOT/'.runtime/v106-final'
EVIDENCE=ROOT/'analysis/evidence/v106_final'
BASE_HASH='228bb674fc7ea3bd6cad73895d6589d74ca5724210c9b99dbe8351ffd4a657d5'

def main():
    current=ROOT/'build'/NAME
    assert builder.digest(current.read_bytes())==BASE_HASH
    ARCHIVE.mkdir(parents=True,exist_ok=True)
    for path in [current,current.with_suffix('.manifest.json'),current.with_suffix('.apk.sha256'),current.with_suffix('.apk.idsig'),ROOT/'build/v106更新说明.txt']:
        target=ARCHIVE/path.name
        if target.exists(): assert target.read_bytes()==path.read_bytes(),target
        else: shutil.copy2(path,target)
    WORK.mkdir(parents=True,exist_ok=True)
    native=build_native(WORK/'liboffline.so')
    builder.BASE=ARCHIVE/NAME
    builder.OUTPUT=WORK/NAME
    builder.WORK=WORK
    builder.EVIDENCE=EVIDENCE
    builder.build(base_version=106,native_adapter=native)
    report=json.loads((EVIDENCE/'build-validation.json').read_text())
    expected={'network_redirect/achievements.py','network_redirect/activity_rape.py',
      'network_redirect/backend.py','network_redirect/equipment_client.lua','network_redirect/guild.py',
      'network_redirect/guild_offline.py','network_redirect/journey.py','network_redirect/rape_client.lua',
      'network_redirect/summon.py','network_redirect/login_branding_client.lua',
      'server_config/guild_rules.json','offline_client.lua','payload-manifest.json'}
    assert set(report['changed_program_entries'])==expected,report['changed_program_entries']
    assert set(report['changed_apk_entries'])=={'assets/offline/build.properties','assets/offline/program.zip','lib/armeabi-v7a/liboffline.so'}
    report.update(release_revision='v106-25-changes-20261030',previous_release_archive=str(ARCHIVE.relative_to(ROOT)),
      same_version_update=True,total_change_items=25,new_change_items=6,
      original_game_java_engine_runtime_video_unchanged=True,
      native_adapter_sha256=builder.digest(native.read_bytes()),
      native_source_sha256=builder.digest((ROOT/'offline_android/native/offline.c').read_bytes()))
    rendered=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
    (EVIDENCE/'build-validation.json').write_text(rendered)
    builder.OUTPUT.with_suffix('.manifest.json').write_text(rendered)
    print('Staged candidate; release download unchanged.')
if __name__=='__main__':main()
