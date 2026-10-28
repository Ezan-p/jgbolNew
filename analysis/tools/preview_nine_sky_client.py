"""Capture isolated native Nine Sky shop bundles, restoring all live UI references."""
import json
import sys
import subprocess
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis/tools')]
from build_nine_sky_client_fixture import main as build
from verify_guild_client import LUA_EVALUATOR
from android_emulator.config import load_config,device_environment
from observability.collector import processes


def main():
    import frida
    build()
    fixture=(ROOT/'.runtime/nine-sky-native-fixture.lua').read_text().split('local ms=assert(package.loaded.ms)',1)[0]
    source=fixture+'''
local ms=assert(package.loaded.ms);local ui=assert(ms.d_towerUI)
assert(not nineShopPreview)
local saved={}
for _,t in ipairs({ui,ms.d_u,ms.d_activityUI,ms.d_time,ms.d_mainUI,ms.d_lineupUI}) do
 local old={};for k,v in pairs(t) do old[k]=v end;saved[#saved+1]={t=t,old=old}
end
if ui._localNineSkyRestore then ui._localNineSkyRestore() end
ui.g_self=ms.d_c.table_copy(ui.g_self);ui.g_self.Help1=true;ui.g_towerUI={}
local root=CCLayer:create();CCDirector:sharedDirector():getRunningScene():addChild(root,9999)
ms.d_activityUI.g_self={main_layer=root};ms.d_activityUI.show=function() end
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(ms.d_mainUI.g_playerInfo)
ms.d_lineupUI.g_usedCharacters={{character={type=5001,reborn_layer=0}}}
ms.d_time.getTime=function() return FIXTURE.now end
ms.d_u.delay=function() end
ms.d_u.main_server_send_msg=function() error('preview must not send requests') end
nineShopPreview={restore=function()
 if ui._localNineSkyRestore then ui._localNineSkyRestore() end
 root:removeFromParentAndCleanup(true)
 for i=#saved,1,-1 do local r=saved[i];for k in pairs(r.t) do r.t[k]=nil end;for k,v in pairs(r.old) do r.t[k]=v end end
 nineShopPreview=nil
end}
'''+(ROOT/'network_redirect/nine_sky_client.lua').read_text()+'''
nineShopPreview.show=function(tid)
 ui.onGetActResult(ms.d_c.table_copy(FIXTURE.rich))
 local data=ms.d_c.table_copy(FIXTURE.big)
 data.shop_data[6]={attach_data={object_type=5,attach_type=tid,attach_count=tid==1249 and 50 or 1,attach_level=1},
 buy_limit=1,need_stars=500,need_credits=500,money_type=11,need_count=500}
 data.role_buy_list[6]=0
 ui.onGetActResult(data)
end
nineShopPreview.show(1249)
return 'ready'
'''
    config=load_config(ROOT/'game.json')
    pid=next(p for p,n in processes(config).items() if n==config['package'])
    session=frida.get_device(config['serial'],timeout=10).attach(pid)
    script=session.create_script(LUA_EVALUATOR);script.load()
    out=ROOT/'analysis/evidence/nine_sky';report=dict(live_account_resources_changed=False,screenshots=[])
    def evaluate(code):
        result=script.exports_sync.evaluate(code)
        if result.get('status')!=0:raise RuntimeError(result)
        return result['result']
    try:
        evaluate(source)
        for tid,name in [(1249,'shop_soul_box_50.png'),(1243,'shop_nine_sky_bag.png')]:
            evaluate(f"nineShopPreview.show({tid});return 'shown'")
            time.sleep(.7)
            raw=subprocess.check_output([str(config['adb_path']),'-s',config['serial'],'exec-out','screencap','-p'],env=device_environment(config))
            (out/name).write_bytes(raw);report['screenshots'].append(name)
        report['passed']=True
    finally:
        evaluate("if nineShopPreview then nineShopPreview.restore() end;return 'restored'")
        script.unload();session.detach()
    (out/'shop_preview.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))


if __name__=='__main__':main()
