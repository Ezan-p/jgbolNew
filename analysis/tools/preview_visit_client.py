"""Capture Shou reward in native Cocos using isolated, restored fixtures."""
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis/tools')]
from android_emulator.config import load_config, device_environment
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR
from build_visit_client_fixture import main as build


def main():
    import frida
    config = load_config(ROOT / 'game.json')
    pid = next(p for p, name in processes(config).items() if name == config['package'])
    session = frida.get_device(config['serial'], timeout=10).attach(pid)
    evaluator = LUA_EVALUATOR.replace('pending={code,resolve};',
        "const task={code,resolve};pending=task;setTimeout(()=>{if(pending===task){"
        "pending=null;resolve({status:-1,result:'No Lua frame; open an in-game panel first'});}},15000);")
    script = session.create_script(evaluator)
    destination = ROOT / 'analysis/evidence/visit'
    report = dict(native_cocos=True, live_account_resources_changed=False, screenshots=[])

    def evaluate(code):
        result = script.exports_sync.evaluate(code)
        if result.get('status') != 0:
            raise RuntimeError(result)
        return result['result']

    def capture(name):
        time.sleep(.7)  # Let Cocos draw the newly installed nodes.
        shot = subprocess.run([str(config['adb_path']), '-s', config['serial'],
                               'exec-out', 'screencap', '-p'],
                              env=device_environment(config), capture_output=True,
                              timeout=15, check=True)
        (destination / name).write_bytes(shot.stdout)
        report['screenshots'].append(name)

    build()
    source = 'local VISIT_PREVIEW=true\nassert(not visitPreview)\n' + (ROOT/'.runtime/visit-native-fixture.lua').read_text()
    try:
        script.load()
        assert evaluate(source) == 'preview ready'
        report['visible_state'] = evaluate("local r=visitPreview.root;local u=package.loaded.ms.d_loginGameUI;return table.concat({tostring(r:isVisible()),r:getChildrenCount(),tostring(r:getParent()==CCDirector:sharedDirector():getRunningScene()),u.g_mainLayer:getChildrenCount()},' / ')")
        capture('shou_reward.png')
        report['passed'] = True
    finally:
        try:
            report['restored'] = evaluate('if visitPreview then '
                'visitPreview.restore();visitPreview=nil end;return "restored"') == 'restored'
        finally:
            script.unload()
            session.detach()
        (destination / 'style_preview.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
