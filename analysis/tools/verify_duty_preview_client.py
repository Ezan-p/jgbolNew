"""Run duty preview adapters under Lua 5.1 without changing a game account."""
import json
import sys
from pathlib import Path
from lupa.lua51 import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import summon

vm = LuaRuntime()
checks = vm.execute((ROOT/'tests/duty_client_regression.lua').read_text(),
                    (ROOT/'network_redirect/duty_client.lua').read_text()).splitlines()
vm.execute('assert(loadstring(...))', summon.client_source(summon.load_rules()))
checks.append('complete production Lua bundle compiles')
report = dict(passed=True, checks=checks, runtime='Lua 5.1',
              native_cocos=False, live_account_resources_changed=False)
(ROOT/'analysis/evidence/duty/preview_client_validation.json').write_text(
    json.dumps(report, ensure_ascii=False, indent=2)+'\n')
print(f'{len(checks)} duty preview Lua checks passed; native Cocos UI not exercised.')
