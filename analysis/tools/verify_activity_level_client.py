"""Run isolated Lua 5.1 callbacks and compile the actual production injection."""
import json
from pathlib import Path
import sys
from lupa.lua51 import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import summon

source = (ROOT / 'network_redirect/activity_level_client.lua').read_text()
harness = (ROOT / 'tests/activity_level_client_regression.lua').read_text()
harness = harness.replace('-- INSTALL_PATCH', source).replace('-- INSTALL_AGAIN', source)
vm = LuaRuntime(unpack_returned_tuples=True)
checks = list(vm.execute(harness).values())
vm.execute('assert(loadstring(...))', summon.client_source(summon.load_rules()))
checks.append('full production injection compiles in Lua 5.1')
report = dict(passed=True, native_cocos=False, checks=checks)
out = ROOT / 'analysis/evidence/feature_levels/client_regression.json'
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report, ensure_ascii=False))
