"""Build reversible Cocos probes; all outgoing messages are intercepted locally."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import summon

adapter = (ROOT / 'network_redirect/pray_client.lua').read_text().replace(
    '__PRAY_COSTS__', summon.lua([int(r['spirit_coins']) for r in summon.rows('pray_spirit_config.csv')]))
script = r'''
local ms=assert(package.loaded.ms);local ui=ms.d_qiFuUI
if localPrayFixtureCleanup then localPrayFixtureCleanup() end
local function upvalue(fn,name)
 for i=1,100 do local k,v=debug.getupvalue(fn,i);if not k then break end;if k==name then return v,i end end
 error('missing upvalue '..name)
end
local function clone(t) local out={};for k,v in pairs(t) do out[k]=v end;return out end
local saved=clone(ui)
local oldStart=ui.startQiFu
local qdata,qindex=upvalue(ui.ensureChoose,'qifuData')
local player=ms.d_mainUI.g_playerInfo
local souls=ms.d_data.g_soulsInfoTable
local chars=ms.d_lineupUI.g_characterInfo
local scroll=ms.d_inertiaLayer.scrollViewHelper.scrollViewDidScroll
local send,report,delay=ms.d_u.main_server_send_msg,ms.MS_report_error,ms.d_u.delay
local confirm=ms.d_data.createEnsureBox
local root=CCLayer:create();CCDirector:sharedDirector():getRunningScene():addChild(root,9999)
local function restore()
 pcall(function() root:removeFromParentAndCleanup(true) end)
 debug.setupvalue(ui.ensureChoose,qindex,qdata)
 for k in pairs(ui) do if saved[k]==nil then ui[k]=nil end end;for k,v in pairs(saved) do ui[k]=v end
 ms.d_mainUI.g_playerInfo=player;ms.d_data.g_soulsInfoTable=souls;ms.d_lineupUI.g_characterInfo=chars
 ms.d_inertiaLayer.scrollViewHelper.scrollViewDidScroll=scroll
 ms.d_u.main_server_send_msg=send;ms.MS_report_error=report;ms.d_u.delay=delay;ms.d_data.createEnsureBox=confirm
 localPrayFixtureCleanup=nil
end
localPrayFixtureCleanup=restore
debug.setupvalue(ui.ensureChoose,qindex,{})
local sent,errors,confirmation={},'',nil
ms.d_mainUI.g_playerInfo=clone(player)
local p=ms.d_mainUI.g_playerInfo;p.level=60;p.pray_spirit_times=0;p.spirit_retain=0
ms.d_data.g_soulsInfoTable=ms.d_c.table_copy(souls)
for _,v in ipairs(ms.d_data.g_soulsInfoTable) do v.count=200 end
ms.d_lineupUI.g_characterInfo=ms.d_c.table_copy(chars)
ms.d_u.main_server_send_msg=function(id,data) sent[#sent+1]={id=id,data=data} end
ms.MS_report_error=function(e) errors=errors..'\n'..tostring(e) end
ms.d_u.delay=function(node,time,fn) fn() end
ms.d_data.createEnsureBox=function(node,config) confirmation=config end
local results={}
pray_fixture_progress='setup'
local function check(name,fn)
 pray_fixture_progress=name
 errors='';local ok,err=xpcall(fn,debug.traceback)
 results[#results+1]={name=name,ok=ok and errors=='',error=(err or '')..errors}
end
local function data() return upvalue(ui.ensureChoose,'qifuData') end
local function close()
 if ui.g_mainLayer and ui.g_mainLayer:getChildByTag(ui.chooseLayerTag) then
  ui.g_mainLayer:removeChildByTag(ui.chooseLayerTag,true)
 end
end
'''
script += '\n' + adapter + '\n'
script += r'''
check('entry',function() ui.show(root);assert(ui.g_isInQiFuPage) end)
for _,v in ipairs({{0,200},{1,500},{2,1000},{3,1000}}) do
 check('cost_'..v[1],function()
  close();p.pray_spirit_times=v[1];ui.startQiFu()
  assert(data().consumeCount==v[2],tostring(data().consumeCount))
  assert(data().curentWorth==0)
 end)
end
check('soul_selection_deselection_and_request',function()
 close();p.pray_spirit_times=0;ui.startQiFu()
 local d=data();d.isTouchInChooseLayer=true
 ui.touchCellBkg({getTag=function() return 1 end})
 assert(d.soulList[1].isChecked and d.curentWorth>0)
 ui.touchCellBkg({getTag=function() return 1 end})
 assert(not d.soulList[1].isChecked and d.curentWorth==0)
 ui.touchCellBkg({getTag=function() return 1 end})
 ui.ensureChoose()
 local msg=sent[#sent];assert(msg.id==1085 and msg.data.object_count==1)
 assert(msg.data.object_list[1].object_type==10 and msg.data.object_list[1].count==200)
end)
check('bulk_select_low_souls_only',function()
 close();ui.startQiFu()
 local native=oldStart
 if saved._localPrayRestore then native=upvalue(oldStart,'oldStart') end
 local switch=upvalue(native,'showChooseLayer');local all=upvalue(switch,'chooseAllFunc')
 all(true);local n=0
 for _,v in ipairs(data().soulList) do
  if v.csvInfo.quality<=3 then assert(v.isChecked);n=n+1 else assert(not v.isChecked) end
 end
 assert(n>0);all(false);assert(data().curentWorth==0)
end)
check('companion_tab_and_high_level_confirmation',function()
 close();p.spirit_retain=196;ui.startQiFu()
 local native=oldStart
 if saved._localPrayRestore then native=upvalue(oldStart,'oldStart') end
 local switch=upvalue(native,'showChooseLayer');switch(ui.qifuType.char)
 local d=data();assert(#d.charList>0);d.isTouchInChooseLayer=true
 for _,v in ipairs(d.charList) do assert(v.csvInfo.quality<=3 and v.order==0 and v.cheer_order==0) end
 d.charList[1].level=2
 ui.touchCellBkg({getTag=function() return 1 end})
 local n=#sent;ui.ensureChoose();assert(#sent==n and confirmation)
 confirmation.secondBtn.callback()
 local msg=sent[#sent];assert(msg.id==1085 and msg.data.object_count==1 and msg.data.object_list[1].object_type==4)
end)
check('gold_reward_animation_and_popup',function()
 ui.getQiFuResult({pray_item_list={{object_type=11,attach_type=0,attach_count=20,attach_level=1}}})
 assert(ui.g_startQiFuMenuItem:isVisible() and ui.g_backMenuItem:isVisible())
end)
check('retained_only_empty_inventory',function()
 close();ms.d_data.g_soulsInfoTable={};ms.d_lineupUI.g_characterInfo={}
 p.spirit_retain=200;p.pray_spirit_times=0;ui.startQiFu()
 assert(data().curentWorth==200 and ui.g_ensureMenuItem:isVisible())
 ui.ensureChoose();local msg=sent[#sent];assert(msg.id==1085 and msg.data.object_count==0)
end)
check('insufficient_empty_inventory',function()
 close();p.spirit_retain=0;ui.startQiFu()
 assert(not ui.g_ensureMenuItem:isVisible() and ui.g_ensureMenuItem2:isVisible())
end)
restore()
local out={};for _,v in ipairs(results) do out[#out+1]=v.name..':'..tostring(v.ok)..':'..v.error end
pray_fixture_progress='complete'
return table.concat(out,'\n')
'''
(ROOT / '.runtime/pray-fixture.lua').write_text(script)
print('Built original 神石祈福 UI probes with reversible state and intercepted requests')
