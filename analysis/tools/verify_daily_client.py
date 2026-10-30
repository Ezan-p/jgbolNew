"""Isolated Lua 5.1 daily-panel adapter regression; requires lupa.lua51."""
from pathlib import Path
import sys

from lupa.lua51 import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import summon

vm = LuaRuntime()
print(vm.execute((ROOT / 'tests/daily_client_regression.lua').read_text(),
                 (ROOT / 'network_redirect/daily_client.lua').read_text()))
vm.execute('assert(loadstring(...))', summon.client_source(summon.load_rules()))
print('Full client injection compiles in Lua 5.1')
