"""Archive the 13-change v106 and stage its six-change same-version update."""
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools import build_v106 as builder

ARCHIVE = ROOT / 'build/archive/v106-13项更新版'
WORK = ROOT / '.runtime/v106-update'
EVIDENCE = ROOT / 'analysis/evidence/v106_update'
NAME = '金箍棒3.87-离线单机-arm32-v106.apk'
BASE_HASH = 'de14a53865b856b828402a74e316799d9430803546315a720aa3cb4e4dcde1ca'


def main():
    current = ROOT / 'build' / NAME
    assert builder.digest(current.read_bytes()) == BASE_HASH, 'Unexpected current v106 release'
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for path in [current, current.with_suffix('.manifest.json'),
                 current.with_suffix('.apk.sha256'), current.with_suffix('.apk.idsig'),
                 ROOT / 'build/v106更新说明.txt']:
        target = ARCHIVE / path.name
        if target.exists():
            assert target.read_bytes() == path.read_bytes(), 'Archive must never be overwritten'
        else:
            shutil.copy2(path, target)
    builder.BASE = ARCHIVE / NAME
    builder.OUTPUT = WORK / NAME
    builder.WORK = WORK
    builder.EVIDENCE = EVIDENCE
    builder.build(base_version=106)
    report = json.loads((EVIDENCE / 'build-validation.json').read_text())
    expected = {
        'network_redirect/activity.py', 'network_redirect/activity_land.py',
        'network_redirect/activity_land_encounters.py', 'network_redirect/backend.py',
        'network_redirect/skill_client.lua', 'network_redirect/trial_client.lua',
        'server_config/land_boss_rules.json', 'server_config/trial_rules.json',
        'offline_client.lua', 'payload-manifest.json',
    }
    assert set(report['changed_program_entries']) == expected, report['changed_program_entries']
    assert report['changed_apk_entries'] == ['assets/offline/build.properties', 'assets/offline/program.zip']
    report.update(release_revision='v106-19-changes-20261030',
                  previous_release_archive=str(ARCHIVE.relative_to(ROOT)),
                  same_version_update=True, total_change_items=19, new_change_items=6)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    (EVIDENCE / 'build-validation.json').write_text(rendered)
    builder.OUTPUT.with_suffix('.manifest.json').write_text(rendered)
    print('Candidate staged; latest download will be replaced after validation.')


if __name__ == '__main__':
    main()
