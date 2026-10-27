local ms=assert(package.loaded.ms);local ui=assert(ms.d_fishRushUI)
local saved,checks,sent,errors,scenes={},{},{},{},{}
local function preserve(t)
 local old={};for k,v in pairs(t) do old[k]=v end;saved[#saved+1]={t=t,old=old}
end
for _,t in ipairs({ui,ms.d_u,ms.d_info,ms.d_data,ms.d_time,ms.d_mainUI,ms.d_hz,ms.d_commonLayerUI}) do preserve(t) end
-- Pause the live panel's scheduled callback while globals point at the fixture.
local liveSelf=ui.g_self;local liveCountdown=ui.count_down_func
local scheduler=CCDirector:sharedDirector():getScheduler()
local liveTimer=liveSelf.CountDownHandler
if liveTimer and liveTimer~=0 then scheduler:unscheduleScriptEntry(liveTimer) end
local function restoreTimer()
 if liveTimer and liveTimer~=0 then liveSelf.CountDownHandler=scheduler:scheduleScriptFunc(liveCountdown,1,false) end
end
local report=ms.MS_report_error;ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
if ui._localFishRestore then ui._localFishRestore() end
ui.g_self=ms.d_c.table_copy(ui.g_self);ui.g_self.CountDownHandler=nil;ui.g_FishRushUI={}
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(ms.d_mainUI.g_playerInfo);ms.d_mainUI.g_playerInfo.gold_coin=1000000
local now=FIXTURE.now;local net=0
ms.d_time.getTime=function() return now end
ms.d_u.runScene=function(scene) scene:retain();scenes[#scenes+1]=scene end
ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
ms.d_data.getItemCountByType=function(typ,tid) if tid==1026 then return net else return 10000 end end
ms.d_info.show=function(text) if text=='wrong data assertion' then errors[#errors+1]=text end end
-- INSTALL_PATCH
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,ok=ok and #errors==0,error=(err or '')..table.concat(errors,'\n')}
end
local function update(v) ui.updateActivityStatus(ms.d_c.table_copy(v)) end
check('permanent entry and native scene',function()
 update(FIXTURE.status);assert(ui.canJoin());local parent=CCScene:create();parent:retain();scenes[#scenes+1]=parent;ui.show(parent);assert(ui.g_FishRushUI.main_layer)
 ui.count_down_func();local timer=ui.g_FishRushUI.main_layer:getChildByTag(ui.g_self.tags.tagTime)
 assert(timer and tolua.cast(timer,'CCLabelTTF'):getString()=='1天12小时0分0秒')
 assert(ui.g_self.gold_per_net==100)
end)
if FISH_PREVIEW then
 local parent=scenes[1]
 CCDirector:sharedDirector():getRunningScene():addChild(parent,9999)
 fishPreview={shop=function() ui.onPressCommit(1) end,preview=function() ui.showPriceListInfo() end,restore=function()
  if ui.g_self.CountDownHandler then CCDirector:sharedDirector():getScheduler():unscheduleScriptEntry(ui.g_self.CountDownHandler) end
  if ui._localFishRestore then ui._localFishRestore() end
  parent:removeFromParentAndCleanup(true);parent:release()
  for i=#saved,1,-1 do local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end;for k,v in pairs(row.old) do row.t[k]=v end end
  ms.MS_report_error=report;restoreTimer()
 end}
 return 'preview ready'
end
check('native paid single request',function()
 ui.onPressRush();local req=sent[#sent];assert(req.mid==1208 and req.data.type_id==0 and req.data.count==1)
end)
check('native paid ten request',function()
 ui.onPressTenRush();local req=sent[#sent];assert(req.mid==1208 and req.data.type_id==0 and req.data.count==10)
end)
check('native free net request',function()
 net=3;ui.createDynamicElements();assert(ui.g_FishRushUI.menuTable[4]:isVisible());ui.onPressRush();assert(sent[#sent].data.count==1);net=0
end)
check('native single and ten rewards',function()
 ui.onGetFishRushResult(ms.d_c.table_copy(FIXTURE.single))
 ui.onGetFishRushResult(ms.d_c.table_copy(FIXTURE.ten))
end)
check('native eight reward preview with silver',function()
 local count=0;local sprite=ms.d_data.getCertainSmallSprite
 local close;local menu=ms.d_u.createMenu
 ms.d_u.createMenu=function(styles,...) close=styles[1].call_back;return menu(styles,...) end
 ms.d_data.getCertainSmallSprite=function(...) count=count+1;return sprite(...) end
 ui.showPriceListInfo();ms.d_data.getCertainSmallSprite=sprite
 assert(count==8 and ui.g_FishRushUI.main_layer:getChildByTag(91027))
 close();ms.d_u.createMenu=menu;assert(not ui.g_FishRushUI.main_layer:getChildByTag(91027))
end)
for idx=1,6 do check('native high shop '..idx,function()
 update(FIXTURE.shops[idx])
 if ui.g_FishRushUI.child_layer then ui.g_FishRushUI.child_layer:removeFromParentAndCleanup(true);ui.g_FishRushUI.child_layer=nil end
 ui.onPressCommit(1);assert(#ui.g_self.goods_infos==5);assert(ui.g_self.goods_infos[5].attach_count==5)
end) end
check('native batch exchange callback and authoritative remaining',function()
 update(FIXTURE.status);ui.onGetFishRushResult(ms.d_c.table_copy(FIXTURE.exchange))
 assert(ui.g_self.goods_infos[1].count==2)
end)
local batchConfirm
check('native general batch picker and request',function()
 local original=ui.createBatchUse
 ui.createBatchUse=function(parent,options,confirm)
  batchConfirm=confirm;assert(options.max==2);return original(parent,options,confirm)
 end
 ui.pressExchange(1);ui.createBatchUse=original;assert(batchConfirm)
 batchConfirm(2);assert(sent[#sent].mid==1208 and sent[#sent].data.count==2 and sent[#sent].data.type_id==1007)
end)
check('midnight blocks stale purchase and requests refresh',function()
 now=FIXTURE.status.search_gold_data.next_daily_refresh
 local n=#sent;ui.pressExchange(1);assert(#sent==n+1 and sent[#sent].mid==1205,'requests '..n..' -> '..#sent..' mid '..tostring(sent[#sent].mid))
 ui.count_down_func();assert(#sent==n+1)
 update(FIXTURE.tomorrow);assert(ui.g_self.goods_infos[1].count>0)
end)
check('old batch confirmation cannot buy after refresh',function()
 local n=#sent;batchConfirm(1)
 for i=n+1,#sent do assert(sent[i].mid~=1208) end
end)
check('weekly countdown remains open and resets progress',function()
 now=FIXTURE.status.search_gold_data.next_weekly_refresh
 assert(ui.canJoin());ui.count_down_func()
 assert(tolua.cast(ui.g_FishRushUI.main_layer:getChildByTag(ui.g_self.tags.tagTime),'CCLabelTTF'):getString()=='0天0小时0分0秒')
 update(FIXTURE.next_week);ui.count_down_func();assert(ui.canJoin())
 assert(tolua.cast(ui.g_FishRushUI.main_layer:getChildByTag(ui.g_self.tags.tagTime),'CCLabelTTF'):getString()=='7天0小时0分0秒')
end)
check('disabled entry',function()
 local v=ms.d_c.table_copy(FIXTURE.next_week);v.search_gold_data.local_enabled=false
 update(v);assert(not ui.canJoin())
end)
if ui.g_self.CountDownHandler then CCDirector:sharedDirector():getScheduler():unscheduleScriptEntry(ui.g_self.CountDownHandler);ui.g_self.CountDownHandler=nil end
if ui._localFishRestore then ui._localFishRestore() end
for _,scene in ipairs(scenes) do scene:removeAllChildrenWithCleanup(true);scene:release() end
for i=#saved,1,-1 do local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end;for k,v in pairs(row.old) do row.t[k]=v end end
ms.MS_report_error=report;restoreTimer()
local out={};for _,v in ipairs(checks) do out[#out+1]=v.name..':'..tostring(v.ok)..':'..v.error end
return table.concat(out,'\n')
