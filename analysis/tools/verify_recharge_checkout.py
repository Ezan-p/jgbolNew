"""Offline checkout regression; requires lupa.lua51 (no emulator or live save)."""
from pathlib import Path
import sys

from lupa.lua51 import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import summon


def main():
    vm = LuaRuntime()
    checks = vm.execute((ROOT / 'tests/recharge_checkout_regression.lua').read_text(),
                        (ROOT / 'network_redirect/vip_client.lua').read_text())
    vm.execute('assert(loadstring(...))', summon.client_source(summon.load_rules()))
    for name in checks.values():
        print('PASS:', name)
    print(f'{len(checks)} checkout checks passed; full Lua 5.1 injection compiles')


if __name__ == '__main__':
    main()
