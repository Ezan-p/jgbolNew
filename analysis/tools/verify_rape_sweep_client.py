"""Isolated sweep UI contracts plus full Lua adapter compilation (lupa.lua51)."""
from pathlib import Path
import sys
from lupa.lua51 import LuaRuntime
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import summon
vm=LuaRuntime()
checks=vm.execute((ROOT/'tests/rape_sweep_client_regression.lua').read_text(),
                  (ROOT/'network_redirect/rape_client.lua').read_text())
for name in checks.values():
    print('PASS',name)
revenge=vm.execute((ROOT/'tests/rape_revenge_client_regression.lua').read_text(),
                   (ROOT/'network_redirect/rape_client.lua').read_text())
for name in revenge.values():
    print('PASS',name)
vm.execute((ROOT/'tests/rape_client_regression.lua').read_text())
vm.execute('assert(loadstring(...))',summon.client_source(summon.load_rules()))
print(f'{len(checks)} sweep and {len(revenge)} revenge checks passed; Continue regression passed; full Lua 5.1 adapter compiles')
