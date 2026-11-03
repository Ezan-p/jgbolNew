"""Isolated Lua 5.1 regressions; no emulator or live account mutations."""
import json
from pathlib import Path
import sys

from lupa.lua51 import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import summon


def main():
    checks = []
    adapter = (ROOT / 'network_redirect/skill_client.lua').read_text()
    for name in ('skill', 'upgrade_probability'):
        vm = LuaRuntime(unpack_returned_tuples=True)
        source = (ROOT / f'tests/{name}_client_regression.lua').read_text()
        checks.extend(vm.execute(source.replace('-- INSTALL_PATCH', adapter)).values())
    vm.execute('assert(loadstring(...))', summon.client_source(summon.load_rules()))
    checks.append('full production injection compiles in Lua 5.1')
    report = dict(passed=True, native_cocos=False, live_account_resources_changed=False, checks=checks)
    destination = ROOT / 'analysis/evidence/upgrade_probability'
    destination.mkdir(parents=True, exist_ok=True)
    (destination / 'client_validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
