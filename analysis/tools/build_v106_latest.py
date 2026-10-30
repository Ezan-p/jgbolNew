"""Stage the October 31 gameplay integration on the preserved official v106."""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools import build_v106 as builder

NAME = '金箍棒3.87-离线单机-arm32-v106.apk'
FORMAL = '金箍棒3.87离线正式版v106.apk'
ARCHIVE = ROOT / 'build/archive/v106-25项更新版'
WORK = ROOT / '.runtime/v106-latest'
EVIDENCE = ROOT / 'analysis/evidence/v106_latest'
BASE_HASH = 'a5f8601bc436c8ef1c7c2d29497c36b28d074ad0f4ea8c823123406a99af7853'


def main():
    current = ROOT / 'build' / FORMAL
    assert builder.digest(current.read_bytes()) == BASE_HASH
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for path in [current, current.with_suffix('.apk.zip'),
                 ROOT / 'build' / NAME.replace('.apk', '.manifest.json'),
                 ROOT / 'build' / (NAME + '.sha256'),
                 ROOT / 'build' / (NAME + '.idsig'), ROOT / 'build/v106更新说明.txt']:
        target = ARCHIVE / path.name
        if target.exists():
            assert target.read_bytes() == path.read_bytes(), target
        else:
            shutil.copy2(path, target)
    builder.BASE = ARCHIVE / FORMAL
    builder.OUTPUT = WORK / NAME
    builder.WORK = WORK
    builder.EVIDENCE = EVIDENCE
    builder.build(base_version=106)
    report = json.loads((EVIDENCE / 'build-validation.json').read_text())
    assert set(report['changed_apk_entries']) == {
        'assets/offline/program.zip', 'assets/offline/build.properties'}
    changed = set(report['changed_program_entries'])
    required = {'network_redirect/fate_rebuild.py', 'network_redirect/fate_rebuild_client.lua',
                'network_redirect/activity_fish.py', 'network_redirect/guild_offline.py',
                'server_config/guild_rules.json', 'server_config/item_reward_rules.json',
                'server_config/moon_rules.json', 'server_config/activity_rules.json',
                'server_config/fate_rebuild_attributes.json', 'offline_client.lua'}
    assert required <= changed, required - changed
    report.update(release_revision='v106-five-updates-20261031',
                  previous_release_archive=str(ARCHIVE.relative_to(ROOT)),
                  same_version_update=True, new_feature_groups=5,
                  feature_groups=['天命石与逆天改命', '仙盟宝库调整', '六种节日礼包',
                                  '月饼粽子奖励', '东海寻宝兑换池'])
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    (EVIDENCE / 'build-validation.json').write_text(rendered)
    builder.OUTPUT.with_suffix('.manifest.json').write_text(rendered)
    print('Candidate staged; previous official release archived and unchanged.')


if __name__ == '__main__':
    main()
