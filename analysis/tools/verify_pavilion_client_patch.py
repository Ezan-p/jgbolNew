"""Isolated Lua 5.1 fortnight timer regression (requires lupa.lua51)."""
from pathlib import Path
import sys
from lupa.lua51 import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity_pavilion, summon

source = (ROOT / 'network_redirect/pavilion_client.lua').read_text().replace(
    '__PAVILION_TABLES__', summon.lua(activity_pavilion.client_tables()))
harness = (ROOT / 'tests/pavilion_client_regression.lua').read_text().replace('-- INSTALL_PATCH', source)
print(LuaRuntime().execute(harness))
