"""Lua 5.1 regressions for realtime model references and displayed values.

Requires lupa.lua51 on PYTHONPATH. This checks adapter behavior; native Cocos
label and callback replay is recorded separately.
"""
import json
from pathlib import Path
import sys

from lupa.lua51 import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import summon


def main():
    checks = []
    for name, adapter in (("state_refresh", "state_refresh"), ("skill", "skill"), ("soul_refresh", "soul_refresh")):
        vm = LuaRuntime(unpack_returned_tuples=True)
        source = (ROOT / f"tests/{name}_client_regression.lua").read_text().replace(
            "-- INSTALL_PATCH", (ROOT / f"network_redirect/{adapter}_client.lua").read_text())
        checks.extend(list(vm.execute(source).values()))
    vm.execute("assert(loadstring(...))", summon.client_source(summon.load_rules()))
    checks.append("full production injection compiles in Lua 5.1")
    report = dict(passed=True, native_cocos=False, checks=checks)
    dest = ROOT / "analysis/evidence/realtime_refresh"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "client_patch_validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
