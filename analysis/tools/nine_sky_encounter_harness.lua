-- Run original timed movement in a hidden temporary Cocos layer; all sends captured.
local ms=assert(package.loaded.ms);local ui=assert(ms.d_towerUI)
assert(not nine_sky_animation_restore,'restore prior fixture first')
nine_sky_animation_result=nil
local saved,errors,buttons={},{},{}
local function keep(t) local old={};for k,v in pairs(t) do old[k]=v end;saved[#saved+1]={t=t,old=old} end
for _,t in ipairs({ui,ms.d_fightUI,ms.d_event_mgr,ms.d_loginUI,ms.d_activityUI,ms.d_u,ms.d_data,ms.d_time,ms.d_mainUI,ms.d_lineupUI,ms.d_info,ms.d_commonLayerUI}) do keep(t) end
if ui._localNineSkyRestore then ui._localNineSkyRestore() end
local testFight={};for k,v in pairs(ms.d_fightUI.g_fightUI) do testFight[k]=v end
testFight.tableChar={};ms.d_fightUI.g_fightUI=testFight
ui.g_self=ms.d_c.table_copy(ui.g_self);ui.g_self.Help1=true;ui.g_towerUI={}
local report=ms.MS_report_error;ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
local originalScene=CCDirector:sharedDirector():getRunningScene()
local root=CCLayer:create();root:setVisible(false);CCDirector:sharedDirector():getRunningScene():addChild(root,9999)
ms.d_activityUI.g_self={main_layer=root};ms.d_activityUI.show=function() end
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(ms.d_mainUI.g_playerInfo);ms.d_mainUI.g_playerInfo.gold_coin=1000000
ms.d_lineupUI.g_usedCharacters={{character={type=5001,reborn_layer=0}}}
ms.d_time.getTime=function() return FIXTURE.now end
ms.d_u.main_server_send_msg=function(mid,data)
 -- Other visible panels may poll during this hidden 50-second fixture.
 -- Capture all traffic, but only tower requests indicate an animation error.
 if mid==1309 then errors[#errors+1]='unexpected tower send: '..tostring(data and data.id) end
end
ms.d_info.show=function(text) if text=='wrong data assertion' then errors[#errors+1]=text end end
local menu=ms.d_u.createMenu
ms.d_u.createMenu=function(styles,...)
 for _,style in ipairs(styles) do
  if style.npic and style.call_back then
   buttons[style.npic]=style.call_back
  end
 end
 return menu(styles,...)
end
local nativeCancel=ui.cancelSwallow
local observed=nil
ui.cancelSwallow=function(...)
 if ui.g_self.role_data and ui.g_self.role_data.steps==FIXTURE.ten.local_snapshot.steps then
  observed=ms.d_c.table_copy(ui.g_self.role_data)
 end
 return nativeCancel(...)
end
-- INSTALL_PATCH
local battleEnds=0;local trace={}
local act=ms.d_fightUI.actFight
ms.d_fightUI.actFight=function(...)
 trace[#trace+1]="actFight"
 local ok,value=pcall(act,...)
 if not ok then errors[#errors+1]=tostring(value);return end
 trace[#trace+1]="scene="..tostring(CCDirector:sharedDirector():getRunningScene()==ms.d_fightUI.g_fightUI.sceneMain)
 return value
end
local endFight=ms.d_fightUI.showFightEnd
ms.d_fightUI.showFightEnd=function(...)
 local result=endFight(...);battleEnds=battleEnds+1
 local panel=ms.d_fightUI.g_fightUI.layerFightEnd:getChildByTag(91037)
 assert(panel,'battle reward/result panel missing')
 local text=tolua.cast(panel:getChildByTag(1),'CCLabelTTF'):getString()
 assert(text:find(battleEnds==1 and '获得奖励' or '未获胜'),'wrong encounter outcome')
 local close=assert(buttons['v2/introUI/close1.png'])
 ms.d_u.delay(panel,0.2,close)
 return result
end
local random=ui.showRandomPrize
ui.showRandomPrize=function(items,callback)
 trace[#trace+1]="prize marker="..tostring(items[1] and items[1].local_nine_sky_battle~=nil)
 local layer=random(items,callback)
 if items[1] and items[1].local_nine_sky_battle then return layer end
 ms.d_u.delay(root,0.05,function()
  ms.d_u.remove(layer);if callback then callback() end
 end)
 return layer
end
local palace=ui.showMysteryShopLayer
local palaceSeen=0
ui.showMysteryShopLayer=function(...)
 palace(...);palaceSeen=palaceSeen+1
 local palaceClose=buttons['v2/common/close1.png']
 ui.onGetActResult(ms.d_c.table_copy(FIXTURE.palace_buy))
 ui.onGetActResult(ms.d_c.table_copy(FIXTURE.card_buy))
 ms.d_u.delay(root,0.05,function()
  assert(palaceClose,'palace close');palaceClose()
 end)
end
function nine_sky_animation_restore()
 if ui._localNineSkyRestore then ui._localNineSkyRestore() end
 if CCDirector:sharedDirector():getRunningScene()~=originalScene then CCDirector:sharedDirector():popScene() end
 ms.d_fightUI.cleanTableChar()
 if main_server and main_server.change_speed then main_server.change_speed(1) end
 ms.d_music_mgr.playUIMusic()
 root:removeFromParentAndCleanup(true)
 for i=#saved,1,-1 do local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end;for k,v in pairs(row.old) do row.t[k]=v end end
 ms.MS_report_error=report;nine_sky_animation_restore=nil
end
local ok,err=xpcall(function()
 ui.updateActivityStatus(FIXTURE.status);ui.onGetActResult(ms.d_c.table_copy(FIXTURE.after_single))
 ms.d_u.delay(root,0.2,function() ui.onGetActResult(ms.d_c.table_copy(FIXTURE.ten)) end)
 local function verify()
  if not observed and #errors==0 then ms.d_u.delay(root,1,verify);return end
  local pass,message=xpcall(function()
   assert(#errors==0,table.concat(errors,'\n'));assert(battleEnds==2,'expected two actual battle endings, got '..battleEnds..' trace='..table.concat(trace,','));assert(observed,'ten movement callbacks did not finish: '..tostring(ui.g_self.role_data.steps)..'/'..tostring(FIXTURE.ten.local_snapshot.steps)..' palace='..palaceSeen)
   local expected=FIXTURE.ten.local_snapshot
   assert(observed.stars==expected.stars,'native animation star mismatch')
   assert(observed.cur_point.x==expected.cur_point.x and observed.cur_point.y==expected.cur_point.y,'native coordinate mismatch')
   assert(ui.g_self.role_data.free_times==expected.free_times,'dice balance mismatch')
   assert(palaceSeen==1,'palace was not rendered and closed exactly once')
   local counts={};for _,card in ipairs(ui.g_self.card_list) do counts[card.value]=card.max end
   for value,count in pairs(FIXTURE.card_buy.local_cards) do assert(counts[value]==count,'pending purchase card sync') end
  end,debug.traceback)
  nine_sky_animation_result=(pass and 'PASS:' or 'FAIL:')..(message or '')
  nine_sky_animation_restore()
 end
 ms.d_u.delay(root,1,verify)
end,debug.traceback)
if not ok then nine_sky_animation_restore();error(err) end
return 'RUNNING'
