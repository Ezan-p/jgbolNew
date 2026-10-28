"""Render the wealth snapshot in native Cocos without modifying live resources."""
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
from network_redirect import monument_wealth, summon


def main():
    import frida
    config = load_config(ROOT / 'game.json')
    pid = next(p for p, n in processes(config).items() if n == config['package'])
    session = frida.get_device(config['serial'], timeout=10).attach(pid)
    evaluator = LUA_EVALUATOR.replace('pending={code,resolve};', "const task={code,resolve};pending=task;setTimeout(()=>{if(pending===task){pending=null;resolve({status:-1,result:'No Lua frame'});}},15000);")
    script = session.create_script(evaluator)
    output = ROOT / 'analysis/evidence/monument'
    output.mkdir(exist_ok=True)
    role = dict(role_id=1, role_name='财富榜测试', vip_level=2, corteges=[])
    now = 1792944000  # Monday 00:00 UTC+8.
    monument_wealth.record(role, now-1, donation_money=1000, normal_gift=20, advanced_gift=4)
    data = monument_wealth.ranking(role, now)
    report = dict(native_cocos=True, live_resources_modified=False, sends_blocked=True)

    def check(code):
        result = script.exports_sync.evaluate(code)
        if result.get('status') != 0:
            raise RuntimeError(result)
        return result['result']

    try:
        script.load()
        check("""local ms=package.loaded.ms;local p=ms.d_guildPartyUI
assert(not wealthPreview)
wealthPreview={show=p.showRankLayer,restore=p._localWealthRestore,send=ms.d_u.main_server_send_msg}
ms.d_u.main_server_send_msg=function() error('preview cannot send') end
p._localWealthRestore=nil
return 'saved'""")
        check((ROOT / 'network_redirect/monument_client.lua').read_text())
        report['render'] = check("""local ms=package.loaded.ms;local create=ms.d_u.createByStyles
local labels={}
ms.d_u.createByStyles=function(style,...)
 if style.type=='label' then labels[#labels+1]=style.string end
 return create(style,...)
end
local ok,layer=pcall(ms.d_guildPartyUI.showRankLayer,""" + summon.lua(data) + """)
ms.d_u.createByStyles=create;assert(ok,layer)
wealthPreview.layer=layer;CCDirector:sharedDirector():getRunningScene():addChild(layer,9999)
local text=table.concat(labels,'|')
assert(string.find(text,'财富分',1,true) and string.find(text,'捐赠资金',1,true))
assert(string.find(text,'每周一00:00',1,true) and string.find(text,'VIP×1000',1,true))
return text""")
        time.sleep(.5)
        shot = subprocess.run([str(config['adb_path']), '-s', config['serial'], 'exec-out', 'screencap', '-p'],
                              env=device_environment(config), capture_output=True, timeout=15, check=True)
        (output / 'wealth_weekly_native.png').write_bytes(shot.stdout)
        report['passed'] = True
    finally:
        try:
            report['restore'] = check("""local ms=package.loaded.ms;local v=wealthPreview
if v then
 if v.layer then v.layer:removeFromParentAndCleanup(true) end
 ms.d_u.main_server_send_msg=v.send
 ms.d_guildPartyUI.showRankLayer=v.show;ms.d_guildPartyUI._localWealthRestore=v.restore
 wealthPreview=nil
end
return 'restored'""")
        finally:
            script.unload(); session.detach()
        (output / 'wealth_client_validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
