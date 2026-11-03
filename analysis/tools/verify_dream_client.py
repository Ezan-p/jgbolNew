"""Run isolated Lua 5.1 callbacks and compile the production injection (requires lupa)."""
import json
from pathlib import Path
import sys
from lupa.lua51 import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import summon


def main():
    patch = (ROOT/'network_redirect/dream_client.lua').read_text()
    harness = (ROOT/'tests/dream_client_regression.lua').read_text()
    harness = harness.replace('-- INSTALL_PATCH', patch).replace('-- INSTALL_AGAIN', patch)
    vm = LuaRuntime(unpack_returned_tuples=True)
    checks = list(vm.execute(harness).values())
    vm.execute('assert(loadstring(...))', summon.client_source(summon.load_rules()))
    checks.append('full production client compiles in Lua 5.1')
    report = dict(passed=True, native_cocos=False, checks=checks)
    out = ROOT/'analysis/evidence/dream/client_validation.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
