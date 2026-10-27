local ms=assert(package.loaded.ms);local ui=assert(ms.d_springActivityMoneyUI)
local saved,checks,sent,errors,scenes={},{},{},{},{}
local function preserve(t)
 local old={};for k,v in pairs(t) do old[k]=v end;saved[#saved+1]={t=t,old=old}
end
for _,t in ipairs({ui,ms.d_u,ms.d_info,ms.d_data,ms.d_time,ms.d_hz,ms.d_commonLayerUI}) do preserve(t) end
local liveSelf=ui.g_self;local liveCountdown=ui.count_down_func
local scheduler=CCDirector:sharedDirector():getScheduler()
local liveTimer=liveSelf.CountDownHandler
if liveTimer and liveTimer~=0 then scheduler:unscheduleScriptEntry(liveTimer) end
local function restoreTimer()
 if liveTimer and liveTimer~=0 then liveSelf.CountDownHandler=scheduler:scheduleScriptFunc(liveCountdown,1,false) end
end
local report=ms.MS_report_error;ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
if ui._localCaishenRestore then ui._localCaishenRestore() end
ui.g_self=ms.d_c.table_copy(ui.g_self);ui.g_self.CountDownHandler=nil;ui.g_SpringActivityMoneyUI={}
local now=FIXTURE.now
ms.d_time.getTime=function() return now end
ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
ms.d_data.getItemCountByType=function() return 10000 end
ms.d_info.show=function(text) if text=='wrong data assertion' then errors[#errors+1]=text end end
-- INSTALL_PATCH
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,ok=ok and #errors==0,error=(err or '')..table.concat(errors,'\n')}
end
local function update(v) ui.updateActivityStatus(ms.d_c.table_copy(v)) end
local function cleanup()
 if ui.g_self.CountDownHandler then scheduler:unscheduleScriptEntry(ui.g_self.CountDownHandler);ui.g_self.CountDownHandler=nil end
 if ui._localCaishenRestore then ui._localCaishenRestore() end
 for _,scene in ipairs(scenes) do scene:removeFromParentAndCleanup(true);scene:removeAllChildrenWithCleanup(true);scene:release() end
 for i=#saved,1,-1 do local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end;for k,v in pairs(row.old) do row.t[k]=v end end
 ms.MS_report_error=report;restoreTimer()
end
check('permanent native scene and week countdown',function()
 update(FIXTURE.status);assert(ui.canJoin());local parent=CCScene:create();parent:retain();scenes[#scenes+1]=parent
 ui.show(parent);assert(ui.g_SpringActivityMoneyUI.main_layer)
 local label=tolua.cast(ui.g_SpringActivityMoneyUI.main_layer:getChildByTag(91028),'CCLabelTTF')
 assert(label and label:getString()=='周刷新剩余 1天12小时0分0秒')
 assert(ui.g_SpringActivityMoneyUI.menuTable[2]:isEnabled())
end)
if CAISHEN_PREVIEW then
 CCDirector:sharedDirector():getRunningScene():addChild(scenes[1],9999)
 caishenPreview={shop=function() ui.onPressCommit(1) end,restore=cleanup}
 return 'preview ready'
end
check('native visit request',function()
 ui.onPressRush();local req=sent[#sent];assert(req.mid==1210 and req.data.flag==1)
end)
check('native two rewards and visited button',function()
 ui.onGetSpringActivityMoneyResult(ms.d_c.table_copy(FIXTURE.visit))
 assert(not ui.g_SpringActivityMoneyUI.menuTable[2]:isEnabled())
 local n=#sent;ui.onPressRush();assert(#sent==n)
end)
for idx=1,5 do check('native high offer '..idx,function()
 update(FIXTURE.shops[idx]);ui.g_SpringActivityMoneyUI.child_layer:removeAllChildrenWithCleanup(true)
 ui.onPressCommit(1);assert(#ui.g_self.goods_infos==5)
 assert(ui.g_self.goods_infos[5].attach_count==(idx==2 and 1 or 5))
end) end
check('native exchange request and authoritative remaining',function()
 update(FIXTURE.status);ui.pressExchange(1)
 local req=sent[#sent];assert(req.mid==1211 and req.data.count==1 and req.data.prize_id==FIXTURE.status.visit_caishen.prize_list[1].prize_id)
 ui.onGetSpringActivityExchangeResult(ms.d_c.table_copy(FIXTURE.exchange))
 assert(ui.g_self.goods_infos[1].count==0)
 local n=#sent;ui.pressExchange(1);assert(#sent==n)
end)
check('midnight blocks old screen and query throttled',function()
 now=FIXTURE.status.visit_caishen.next_daily_refresh
 local n=#sent;ui.pressExchange(2);assert(#sent==n+1 and sent[#sent].mid==1205)
 ui.count_down_func();assert(#sent==n+1)
end)
check('daily refresh rebuilds native shop and visit button',function()
 update(FIXTURE.tomorrow);assert(ui.g_SpringActivityMoneyUI.menuTable[2]:isEnabled())
 assert(ui.g_self.goods_infos[1].count==1)
 assert(ui.g_self.goods_infos[1].prize_id~=FIXTURE.status.visit_caishen.prize_list[1].prize_id)
 ui.onPressRush();assert(sent[#sent].mid==1210)
end)
check('week boundary stays open and zero countdown',function()
 now=FIXTURE.status.visit_caishen.next_weekly_refresh;assert(ui.canJoin());ui.count_down_func()
 local node=ui.g_SpringActivityMoneyUI.main_layer:getChildByTag(91028)
 assert(tolua.cast(node,'CCLabelTTF'):getString()=='周刷新剩余 0天0小时0分0秒')
end)
check('new week shows seven days',function()
 update(FIXTURE.next_week);assert(ui.canJoin());ui.count_down_func()
 local node=ui.g_SpringActivityMoneyUI.main_layer:getChildByTag(91028)
 assert(tolua.cast(node,'CCLabelTTF'):getString()=='周刷新剩余 7天0小时0分0秒')
 assert(ui.g_self.goods_infos[1].count==1)
end)
check('disabled activity refuses entry and requests',function()
 local v=ms.d_c.table_copy(FIXTURE.next_week);v.visit_caishen.local_enabled=false;update(v);assert(not ui.canJoin())
 local n=#sent;ui.onPressRush();ui.pressExchange(1);assert(#sent==n)
end)
check('updated permanent and recycle text',function()
 assert(ms.d_hz.gethz('springCSEndTime')=='常驻开放 · 每周一0点刷新')
 assert(string.find(ms.d_hz.gethz('springActivityTips'),'2:1'))
end)
cleanup()
local out={};for _,v in ipairs(checks) do out[#out+1]=v.name..':'..tostring(v.ok)..':'..v.error end
return table.concat(out,'\n')
