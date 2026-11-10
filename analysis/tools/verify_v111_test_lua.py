"""Verify the exact test payload's generated Lua, branding, and client harnesses."""
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, '/private/tmp/qmxy-battle-test-deps')
from lupa.lua51 import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / '.runtime/v111-test/program'
EVIDENCE = ROOT / 'analysis/evidence/v111_test'


def main():
    bundle = (PROGRAM / 'offline_client.lua').read_text()
    vm = LuaRuntime()
    vm.execute('assert(loadstring(...))', bundle)
    vm.execute('''LABELS={}
local scene={getChildByTag=function() return nil end,addChild=function() end}
package.loaded['update.updateUI']={create=function() end,g_self={main_scene=scene}}
package.loaded['update.update_ms']={d_u={createByStyle=function(spec) LABELS[#LABELS+1]=spec.string;return {} end}}
CCLayer={create=function() return {setTouchEnabled=function() end,addChild=function() end} end}
CCDirector={sharedDirector=function() return {getRunningScene=function() return scene end} end}
''')
    assert vm.execute(bundle) == 'pending'
    assert list(vm.globals().LABELS.values()) == ['离线版·非商业·仅供学习', 'v111', '开发者@Ezan']
    checks = dict(full_bundle_compiles=True, prelogin_branding_v111=True)
    for fixture, adapter in [('skill', 'skill'), ('upgrade_probability', 'skill'),
                             ('dream', 'dream'), ('nine_sky', 'nine_sky')]:
        source = (PROGRAM / f'network_redirect/{adapter}_client.lua').read_text()
        harness = (ROOT / f'tests/{fixture}_client_regression.lua').read_text()
        LuaRuntime().execute(harness.replace('-- INSTALL_PATCH', source).replace('-- INSTALL_AGAIN', source))
        checks[fixture] = True
    result = LuaRuntime().execute((ROOT / 'tests/battle_replay_client_regression.lua').read_text(),
                                  (PROGRAM / 'network_redirect/battle_replay_client.lua').read_text())
    checks['battle_replay'] = list(result.values()) if hasattr(result, 'values') else result
    home_vm = LuaRuntime()
    home_vm.globals().HOME_SOURCE = (PROGRAM / 'network_redirect/home_client.lua').read_text()
    home_vm.execute((ROOT / 'tests/home_client_regression.lua').read_text().replace(
        "dofile('network_redirect/home_client.lua')", 'assert(loadstring(HOME_SOURCE))()'))
    checks['home_stage_refresh'] = True
    sys.path.insert(0, str(PROGRAM))
    from network_redirect import activity, activity_moon, activity_rice
    assert Path(activity.__file__).resolve().is_relative_to(PROGRAM.resolve())
    rules = activity.load_rules()
    LuaRuntime().execute((ROOT / 'tests/seasonal_craft_client_regression.lua').read_text(),
        activity_moon.client_source(rules), activity_rice.client_source(rules))
    checks['seasonal_weekly_client'] = True
    report = dict(passed=True,
        apk_sha256=hashlib.sha256((ROOT / '.runtime/v111-test/金箍棒ol测试版-v111.apk').read_bytes()).hexdigest(),
        checks=checks)
    (EVIDENCE / 'lua-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
