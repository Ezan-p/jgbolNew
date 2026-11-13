"""Freeze and append the requested Abyss changes to the latest formal v112."""
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools import build_v112_taixu as builder

WORK = ROOT / '.runtime/v112-abyss-20261114'
EVIDENCE = ROOT / 'analysis/evidence/v112-abyss-20261114'
BASE = WORK / 'baseline-v112.apk'
BASE_SHA = '1521f658b445063e157782f479ef3c6452e44bf22432b141c3de36a2ab13064e'
OUTPUT = WORK / '金箍棒ol离线正式版v112.apk'
CHANGES = {'network_redirect/abyss_client.lua','network_redirect/activity.py',
           'network_redirect/activity_abyss.py','server_config/activity_rules.json'}
VERSION_NAME = builder.VERSION_NAME
digest = builder.digest

for name in ('WORK','EVIDENCE','BASE','BASE_SHA','OUTPUT','CHANGES'):
    setattr(builder,name,globals()[name])
builder.FEATURE_GROUPS = 13
builder.APPENDED_FEATURE_GROUPS = 3
builder.RELEASE_REVISION = '2026-11-14-formal-v112-abyss'
report = builder.report


if __name__ == '__main__':
    current = ROOT / 'build' / OUTPUT.name
    assert digest(current.read_bytes()) == BASE_SHA
    assert not BASE.exists(), 'Do not overwrite frozen baseline'
    WORK.mkdir(parents=True,exist_ok=True)
    shutil.copy2(current,BASE)
    builder.build()
