"""Run the summon adapter's isolated behavior checks (requires lupa.lua51)."""
from pathlib import Path

from lupa.lua51 import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]
source = (ROOT / 'network_redirect/summon_client.lua').read_text(encoding='utf-8')
source = source.replace('__SUMMON_GOLD_PRICES__', '{17,123,456}')
harness = (ROOT / 'analysis/tools/summon_client_harness.lua').read_text(encoding='utf-8')
report = LuaRuntime().execute(harness, source)
print(report)
print(f'PASS: {len(report.splitlines())} checks')
