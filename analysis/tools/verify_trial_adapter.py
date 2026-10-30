"""Isolated Lua 5.1 adapter contracts; does not require a running emulator."""
from pathlib import Path
import sys
from lupa.lua51 import LuaRuntime
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import summon
vm = LuaRuntime()
checks = vm.execute((ROOT / 'tests/trial_client_regression.lua').read_text(),
                    (ROOT / 'network_redirect/trial_client.lua').read_text())
for name in checks.values():
    print('PASS', name)
vm.execute('assert(loadstring(...))', summon.client_source(summon.load_rules()))
print(f'{len(checks)} Lua contracts passed; full injected Lua compiles')
