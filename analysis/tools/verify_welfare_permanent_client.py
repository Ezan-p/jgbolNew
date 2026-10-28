"""Render permanent welfare in disposable native nodes, with all sends intercepted."""
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis/tools')]
from android_emulator.config import load_config
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR
from network_redirect import summon, welfare
from network_redirect.backend import Backend, login_fields


def main():
    import frida
    config = load_config(ROOT / 'game.json')
    device = frida.get_device(config['serial'], timeout=10)
    session = device.attach(next(p for p, name in processes(config).items() if name == config['package']))
    script = session.create_script(LUA_EVALUATOR)
    out = ROOT / 'analysis/evidence/welfare'
    results = []
    def evaluate(code):
        result = script.exports_sync.evaluate(code)
        if result.get('status') != 0:
            raise RuntimeError(result)
        return result['result']
    try:
        script.load()
        evaluate('''local v=package.loaded.ms.d_actNoticeUI
if v._localPermanentWelfareRestore then v._localPermanentWelfareRestore() end
if v._localGrowthRestore then v._localGrowthRestore() end
if v._localWelfareRestore then v._localWelfareRestore() end''')
        evaluate((ROOT / 'network_redirect/welfare_client.lua').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            b = Backend(Path(tmp), 1, lambda *a, **k: None)
            try:
                role = b.profile()
                role.update(level=60, vip_level=10, buy_growup=1, silver_coin=1000000)
                welfare.record_charge(role, 10000, int(time.time()), b.welfare_rules)
                summon.add_item(role, 1001, 100)
                catalog = welfare.catalog(role, int(time.time()), b.welfare_rules)
            finally:
                b.close()
        player = {k: role[k] for k in ('level','vip_level','buy_growup','first_charge','first_charge_gift','take_charge_gift_time','gold_coin','silver_coin')}
        for kind, name in [(20,'createFirstChargeDouble'),(22,'createGrowthFund'),(7,'createUpgradeRole'),
                           (16,'createLoginPrize'),(23,'createnewCharge'),(21,'createCarnival'),(32,'createExchange')]:
            code = '''local ms=package.loaded.ms
local v,u,t=ms.d_actNoticeUI,ms.d_u,ms.d_time
local saved={};for k,value in pairs(v) do saved[k]=value end
local player=ms.d_mainUI.g_playerInfo
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(player)
for k,value in pairs(PLAYER) do ms.d_mainUI.g_playerInfo[k]=value end
local create,creates,menu,send,delay=u.createByStyle,u.createByStyles,u.createMenu,u.main_server_send_msg,u.delay
local texts,buttons,requests,timers,actions={},{},{},0,{}
local scene=CCDirector:sharedDirector():getRunningScene()
local layer=CCLayerColor:create(ccc4(40,25,15,255));scene:addChild(layer,9999,19878)
local function text(s) if s.string then texts[#texts+1]=tostring(s.string) end end
local ok,err=xpcall(function()
 u.createByStyle=function(s,...) text(s);return create(s,...) end
 u.createByStyles=function(s,...) text(s);return creates(s,...) end
 u.createMenu=function(styles,items,...)
  local result=menu(styles,items,...)
  for i,s in ipairs(styles) do
   buttons[#buttons+1]={pic=s.npic or '',tag=s.tag,enabled=items and items[i] and items[i]:isEnabled()}
   if s.npic=='v2/tianShuUI/get1.png' or s.npic=='v2/richmanUI/buy1.png' then actions[#actions+1]={callback=s.call_back,tag=s.tag} end
  end
  return result
 end
 u.main_server_send_msg=function(mid,data) requests[#requests+1]={mid=mid,data=data} end
 u.delay=function(...) timers=timers+1 end
 v.NAME(INFO,layer)
 local permanent=false
 for _,s in ipairs(texts) do if string.find(s,'永久',1,true) then permanent=true end end
 assert(permanent,'missing permanent label')
 assert(#requests==0,'render sent network request')
 assert(timers==0,'permanent page scheduled a timer')
 if KIND==23 or KIND==16 or KIND==32 then
  assert(#actions>0,'missing claim buttons')
  for _,action in ipairs(actions) do action.callback(action.tag) end
  assert(#requests==#actions,'native claim blocked by deadline')
  for _,request in ipairs(requests) do assert(request.mid==1127 and request.data.act_type==KIND and request.data.flag==2) end
 end
end,debug.traceback)
u.createByStyle,u.createByStyles,u.createMenu,u.main_server_send_msg,u.delay=create,creates,menu,send,delay
ms.d_mainUI.g_playerInfo=player
for k in pairs(v) do if saved[k]==nil then v[k]=nil end end
for k,value in pairs(saved) do v[k]=value end
if not ok then scene:removeChildByTag(19878,true);error(err) end
return table.tostring({texts=texts,buttons=buttons,requests=requests,timers=timers})'''
            code = code.replace('PLAYER', summon.lua(player)).replace('NAME', name).replace('INFO', summon.lua(catalog[kind])).replace('KIND', str(kind))
            data = login_fields(evaluate(code))
            results.append(dict(activity=kind, passed=True, **data))
            (out / f'permanent_{kind}.png').write_bytes(subprocess.check_output(
                [str(config['adb_path']), '-s', config['serial'], 'exec-out', 'screencap', '-p']))
            evaluate('CCDirector:sharedDirector():getRunningScene():removeChildByTag(19878,true)')
        growth = evaluate((ROOT / 'tests/growth_client_native.lua').read_text())
        assert growth == 'passed:8', growth
        report = dict(passed=True, native_cocos=True, live_save_modified=False, pages=results, growth=growth)
        (out / 'permanent_client_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps(report,ensure_ascii=False))
    finally:
        try:
            evaluate('local s=CCDirector:sharedDirector():getRunningScene();s:removeChildByTag(19878,true);s:removeChildByTag(19877,true)')
        finally:
            script.unload()
            session.detach()


if __name__ == '__main__':
    main()
