"""Isolated Lua 5.1 clock, catalog and animation callback regressions (lupa)."""
import json
from pathlib import Path
import sys
from lupa.lua51 import LuaRuntime
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import summon
vm=LuaRuntime(unpack_returned_tuples=True)
source=(ROOT/'tests/nine_sky_client_regression.lua').read_text().replace(
    '-- INSTALL_PATCH',(ROOT/'network_redirect/nine_sky_client.lua').read_text())
checks=list(vm.execute(source).values())
vm.execute('assert(loadstring(...))',summon.client_source(summon.load_rules()))
checks.append('full production injection compiles')
report=dict(passed=True,lua_version='5.1',native_cocos=False,checks=checks)
path=ROOT/'analysis/evidence/nine_sky/client_patch_validation.json'
path.parent.mkdir(parents=True,exist_ok=True)
path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))
