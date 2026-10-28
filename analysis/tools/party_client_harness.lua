local ms=assert(package.loaded.ms);local ui=ms.d_worldBossUI
local saved={};for k,v in pairs(ui) do saved[k]=v end
local send,info,report=ms.d_u.main_server_send_msg,ms.d_info.show,ms.MS_report_error
local sends=0;local message;local errors='';local checks={}
local root=CCLayer:create();root:retain();CCDirector:sharedDirector():getRunningScene():addChild(root,9999)
ms.d_u.main_server_send_msg=function() sends=sends+1 end
ms.d_info.show=function(text) message=text end
ms.MS_report_error=function(text) errors=errors..tostring(text) end
local function restore()
 root:removeFromParentAndCleanup(true);root:release()
 if ui._localPartyRestore then ui._localPartyRestore() end
 for k in pairs(ui) do if saved[k]==nil then ui[k]=nil end end
 for k,v in pairs(saved) do ui[k]=v end
 ms.d_u.main_server_send_msg=send;ms.d_info.show=info;ms.MS_report_error=report
end
partyPreview={restore=restore}
local function check(name,fn)
 errors='';local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]=name..':'..tostring(ok and errors=='')..':'..(err or '')..errors
end
if ui._localPartyRestore then ui._localPartyRestore() end
-- INSTALL_PATCH
local prizes={}
for _,id in ipairs({1001,1134,1135,1136,1137,1138,1208,1209,1210,1211,1212}) do
 prizes[#prizes+1]={object_type=5,attach_type=id,attach_count=id==1001 and 34 or 2,attach_level=1}
end
ui.g_realTimeFightInfo={fight_prize=prizes,cur_damage=349380};ui.g_currentRoundDamage=349380
ui.g_mainLayer=root;ui.g_isInWorldBossStartPage=false;ui.g_isInFightInfoPage=false
local function grid() return assert(root:getChildByTag(95120)):getChildByTag(95121) end
local function nextPage()
 local children=grid():getChildren()
 local menu=tolua.cast(children:objectAtIndex(children:count()-1),'CCMenu')
 tolua.cast(menu:getChildren():objectAtIndex(0),'CCMenuItemLabel'):activate()
end
partyPreview.nextPage=nextPage
check('luck_click_disabled',function() ui.checkLuckRank();assert(message=='离线模式，暂不开启' and sends==0) end)
check('luck_claim_disabled',function() ui.getLuckPointReward();assert(message=='离线模式，暂不开启' and sends==0) end)
check('fight_end_all_materials',function()
 ui.showFightEnd(root);assert(grid():getChildrenCount()==15)
 assert(ui.g_realTimeFightInfo.fight_prize==prizes and #prizes==11)
end)
check('reward_page_two',function() nextPage();assert(grid():getChildrenCount()==13) end)
check('reward_page_wrap',function() nextPage();assert(grid():getChildrenCount()==15) end)
check('repeated_fight_dialog',function()
 ui.showFightEnd(root);assert(root:getChildrenCount()==1);assert(grid():getChildrenCount()==15)
end)
check('one_item',function()
 ui.g_realTimeFightInfo.fight_prize={prizes[1]};ui.showFightEnd(root);assert(grid():getChildrenCount()==2)
end)
check('zero_items',function()
 ui.g_realTimeFightInfo.fight_prize={};ui.showFightEnd(root);assert(grid():getChildrenCount()==1)
end)
check('event_page_award',function()
 ui.g_realTimeFightInfo.fight_prize=prizes;ui.showAward();assert(grid():getChildrenCount()==15)
end)
return table.concat(checks,'\n')
