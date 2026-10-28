"""Isolated Lua 5.1 fortnight regressions; requires lupa.lua51 on PYTHONPATH."""
from pathlib import Path
from lupa.lua51 import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]
source = (ROOT / 'network_redirect/yuanshi_client.lua').read_text()
harness = (ROOT / 'tests/yuanshi_client_regression.lua').read_text().replace('-- INSTALL_PATCH', source)
print(LuaRuntime().execute(harness))
