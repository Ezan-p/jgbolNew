"""Lua 5.1 animation-control regression; no emulator or player save changes."""
from pathlib import Path
import sys

from lupa.lua51 import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import summon

vm = LuaRuntime()
checks = vm.execute((ROOT / 'tests/equipment_enhance_client_regression.lua').read_text(),
                    (ROOT / 'network_redirect/equipment_client.lua').read_text())
for name in checks.values():
    print('PASS', name)
vm.execute('assert(loadstring(...))', summon.client_source(summon.load_rules()))
print(f'{len(checks)} isolated checks passed; full Lua 5.1 client bundle compiles')
