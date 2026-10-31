"""Package the stone refinement repair on the current official v106 shell."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools import build_v106 as builder

BASE = ROOT / 'build/金箍棒3.87离线正式版v106.apk'
APK = ROOT / 'build/金箍棒3.87离线正式版v106-神石修复.apk'
WORK = ROOT / '.runtime/v106-stone-fix'
EVIDENCE = ROOT / 'analysis/evidence/stone_refine_fix'
BASE_HASH = '140d850a791267cfcdae725b5cd9e650cfb3fffff894759bb024ff17cf5ed494'


def main():
    assert builder.digest(BASE.read_bytes()) == BASE_HASH
    builder.BASE, builder.OUTPUT, builder.WORK, builder.EVIDENCE = BASE, APK, WORK, EVIDENCE
    builder.build(base_version=106)
    report = json.loads((EVIDENCE / 'build-validation.json').read_text())
    assert set(report['changed_program_entries']) == {
        'network_redirect/equipment.py', 'network_redirect/equipment_client.lua',
        'analysis/configs/stone/stone_reborn_cost_worth.csv',
        'offline_client.lua', 'payload-manifest.json'}
    assert set(report['changed_apk_entries']) == {
        'assets/offline/program.zip', 'assets/offline/build.properties'}
    report.update(release_revision='v106-stone-refinement-20261031', same_version_update=True)
    text = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    (EVIDENCE / 'build-validation.json').write_text(text)
    APK.with_suffix('.manifest.json').write_text(text)


if __name__ == '__main__':
    main()
