"""Run consumable quantity-picker regression and compile production Lua 5.1."""
from pathlib import Path
import sys

from lupa.lua51 import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import summon

vm = LuaRuntime()
print(vm.execute((ROOT / 'tests/resource_item_client_regression.lua').read_text(),
                 (ROOT / 'network_redirect/resource_item_client.lua').read_text()))
vm.execute('assert(loadstring(...))', summon.client_source(summon.load_rules()))
print('Full client injection compiles in Lua 5.1')
