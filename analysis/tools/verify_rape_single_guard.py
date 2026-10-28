"""Reproduce and verify the one-guard layout in the original Cocos runtime."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis/tools')]
from android_emulator.config import load_config
from observability.collector import processes
from network_redirect import summon
from network_redirect.backend import login_fields
from verify_guild_client import LUA_EVALUATOR


def main():
    import frida
    config = load_config(ROOT / 'game.json')
    pid = next(p for p, n in processes(config).items() if n == config['package'])
    session = frida.get_device(config['serial'], timeout=10).attach(pid)
    evaluator = LUA_EVALUATOR.replace('pending={code,resolve};',
        "const task={code,resolve};pending=task;setTimeout(()=>{if(pending===task){"
        "pending=null;resolve({status:-1,result:'No Lua frame'});}},15000);")
    script = session.create_script(evaluator)
    patch = (ROOT / 'network_redirect/rape_client.lua').read_text()
    source = (ROOT / 'analysis/tools/rape_single_guard_harness.lua').read_text().replace('-- INSTALL_PATCH', patch)
    report = dict(native_cocos=True, live_account_resources_changed=False)
    try:
        script.load()
        raw = script.exports_sync.evaluate(source)
        report['raw'] = raw
        checks = list(login_fields(raw['result']).values()) if raw.get('status') == 0 else []
        report['checks'] = checks
        report['passed'] = len(checks) == 41 and all(c['passed'] for c in checks)
        regression = (ROOT / 'tests/rape_client_regression.lua').read_text().replace(
            "dofile('network_redirect/rape_client.lua')", 'assert(loadstring(' + summon.lua(patch) + '))()')
        report['continue_regression'] = script.exports_sync.evaluate(
            'local saved=package.loaded.ms;local ok,err=pcall(function()\n' + regression +
            '\nend);package.loaded.ms=saved;assert(ok,err);return "passed"')
        report['passed'] = report['passed'] and report['continue_regression'].get('result') == 'passed'
        if report['passed'] and '--install' in sys.argv:
            # Upgrade the running client and fill only missing single-guard heads.
            install = "local ui=package.loaded.ms.d_crossDoomUI;if ui._localRapeRestore then ui._localRapeRestore() end\n" + patch + '''
local state=ui.g_self
if state and state.cardPage_layer and state.card_data and state.cardPage_enmey_map then
 for column,board in ipairs(state.card_data.rape_list or {}) do
  local heads={}
  for typ,rows in pairs(board.form_list or {}) do
   for id,v in pairs(rows) do heads[#heads+1]={type=typ,id=id,v=v} end
  end
  if #heads==1 and not state.cardPage_enmey_map[column*100+1] then
   ui.createCardHead(column,heads,nil,true)
  end
 end
end
return 'installed'
'''
            report['installation'] = script.exports_sync.evaluate(install)
    finally:
        script.unload()
        session.detach()
    destination = ROOT / 'analysis/evidence/rape/single_guard_validation.json'
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(f"Native Cocos: {sum(c['passed'] for c in checks)}/{len(checks)} passed; "
          f"Continue regression: {report['continue_regression']}; "
          f"installation: {report.get('installation', 'not requested')}")
    if not report.get('passed') or ('--install' in sys.argv and
            report.get('installation') != dict(status=0, result='installed')):
        print(json.dumps(report, ensure_ascii=False, indent=2))
        raise SystemExit(1)


if __name__ == '__main__':
    main()
