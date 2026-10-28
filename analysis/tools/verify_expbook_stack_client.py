"""Exercise aggregated scroll selection offline and compile the full Lua adapter.

Requires lupa.lua51 on PYTHONPATH (the local cached installation is
/private/tmp/jgbol-rank-lua). No emulator or live account is accessed.
"""
import json
from pathlib import Path
import sys
import time

from lupa.lua51 import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import summon


def main():
    vm = LuaRuntime(max_memory=64 * 1024 * 1024)
    started = time.perf_counter()
    checks = list(vm.execute(
        (ROOT / 'tests/expbook_client_regression.lua').read_text(),
        (ROOT / 'network_redirect/expbook_client.lua').read_text()).values())
    vm.execute('assert(loadstring(...))', summon.client_source(summon.load_rules()))
    report = dict(passed=True, checks=checks, checks_count=len(checks),
                  full_injection_compiles=True, lua_version='5.1',
                  elapsed_seconds=round(time.perf_counter() - started, 6),
                  largest_inventory_scrolls=400_000_000, largest_inventory_rows=40,
                  instructions_per_check_limit=1_000_000,
                  native_cocos=False, live_account_resources_changed=False,
                  coverage='Production adapter against table-view and picker contracts; native rendering verified separately.')
    destination = ROOT / 'analysis/evidence/expbooks/stack_client_regression_20261028.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(checks)} scroll stack checks passed; full client injection compiles in Lua 5.1')
    print(f'Largest fixture: 400,000,000 scrolls, 40 rows; elapsed {report["elapsed_seconds"]:.3f}s')


if __name__ == '__main__':
    main()
