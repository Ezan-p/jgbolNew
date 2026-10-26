-- Execute original 3.87 widgets with captured network and detached scenes.
local ms=assert(package.loaded.ms);local ui=assert(ms.d_turntableUI)
local saved,checks,sent,errors,scenes,buttons={},{},{},{},{},{}
local function preserve(t)
 local old={};for k,v in pairs(t) do old[k]=v end;saved[#saved+1]={t=t,old=old}
end
for _,t in ipairs({ui,ms.d_activityUI,ms.d_u,ms.d_info,ms.d_data,ms.d_time,ms.d_loginUI,ms.d_rechargeUI,ms.d_commonLayerUI,ms.d_packageUI,ms.d_lineupUI,ms.d_answerUI}) do preserve(t) end
local report=ms.MS_report_error;ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
if ui._localRulaiRestore then ui._localRulaiRestore() end
ui.g_self={main_tag=1,timetip_tag=2,giftDetailTag=3};ui.g_boxUI={};ui.g_progressSchedule=nil
ms.d_time.getTime=function() return FIXTURE.now end
ms.d_u.delay=function() end
ms.d_u.runScene=function(scene) scene:retain();scenes[#scenes+1]=scene end
ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
ms.d_info.show=function() end
ms.d_data.g_new_config=ms.d_c.table_copy(ms.d_data.g_new_config or {})
ms.d_answerUI.g_self=ms.d_c.table_copy(ms.d_answerUI.g_self or {})
ms.d_answerUI.g_self.config={start_time=0,end_time=0}
ms.d_activityUI.returnBack=function() ms.d_loginUI.g_currentSence=0 end
ms.d_rechargeUI.g_self={}
ms.d_rechargeUI.pressClose=function() ms.d_rechargeUI.g_self.main_layer=nil end
local menu=ms.d_u.createMenu
ms.d_u.createMenu=function(styles,...)
 for _,style in ipairs(styles) do if style.npic and style.call_back then buttons[style.npic]=style.call_back end end
 return menu(styles,...)
end
ms.d_data.getItemCountByType=function() return 2 end
ms.d_data.getPropsID=function(tid) return tid+900000 end
ms.d_data.getSpecialitemuseCSVConfig()
ms.d_lineupUI.g_characterInfo={}
ms.d_packageUI.g_reorgItemsInfo={[5]={}}
-- INSTALL_PATCH
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,ok=ok and #errors==0,error=(err or '')..table.concat(errors,'\n')}
end
local function response(data) ui.onGetResult(ms.d_c.table_copy(data)) end
local function last(op)
 local req=sent[#sent];assert(req and req.mid==1351 and req.data.id==op,'wrong 1351 operation')
 assert(type(req.data.data)=='string' and req.data.data:gsub('%s','')=='{}','nonempty native payload: '..tostring(req.data.data))
end
check('native schedule and fun menu entry',function()
 ms.d_activityUI.updateAllActivityStatus({[73]=FIXTURE.times});assert(ui.canJoin())
 local found=false;for _,v in ipairs(ms.d_funUI.getFunList()) do if v.id==49 then found=true end end
 assert(found);ui.enter();last(0)
end)
check('native initial screen eight rewards',function()
 response(FIXTURE.entry);assert(ui.g_self.main_layer);assert(#ui.g_self.data.reward_list==8)
 assert(#ui.g_self.tt_reward_splash==8);assert(ui.g_self.data.total_time==0)
 local n=#sent;buttons['v2/newTurnTableUI/luckdraw1.png']();assert(#sent==n)
end)
check('native live charge refresh and hint',function()
 ms.d_data.callback_update_config(ms.d_c.table_copy(FIXTURE.sync))
 assert(ui.g_self.data.total_time==10);assert(ui.g_self.data.prize_status==2);assert(ui.getShowHint()==1)
end)
check('recharge overlay defers redraw until close',function()
 ms.d_rechargeUI.g_self.main_layer=true
 local layer=ui.g_self.main_layer
 ms.d_data.callback_update_config(ms.d_c.table_copy(FIXTURE.sync))
 assert(ui.g_self.main_layer==layer)
 ms.d_rechargeUI.pressClose()
 assert(ui.g_self.main_layer~=layer);assert(ui.g_self.data.total_time==10)
end)
for i=1,8 do check('native wheel request animation reward '..i,function()
 buttons['v2/newTurnTableUI/luckdraw1.png']();last(1)
 response(FIXTURE.draws[i]);assert(ui.g_self.data.result_index==i)
 assert(ui.g_progressSchedule and ui.g_progressSchedule~=0)
 ui.close_schedulescriptfunc();ui.g_bagua:stopAllActions()
 ui.g_self.index=i;ui.showreward();assert(ui.g_self.data.total_time==10-i)
end) end
check('native extra gift claim callback',function()
 response(FIXTURE.charged)
 buttons['v2/actNoticeUI/get1.png']();last(2)
 response(FIXTURE.bonus);assert(ui.g_self.data.prize_status==3)
 ui.showRewardDetail(ui.g_self.data.itemList)
end)
for _,tid in ipairs({1367,1368}) do
 for _,target in ipairs({{10,5053},{5,1249}}) do
  check('native bag choice '..tid..' target '..target[1],function()
   ui.g_boxUI={};ui.showBoxUseLayer(ui.g_self.main_layer,30,tid)
   assert(#ui.g_boxUI.data_list==2)
   for i,row in ipairs(ui.g_boxUI.data_list) do
    if (target[1]==5 and row.isItem) or (target[1]==10 and not row.isItem) then ui.g_boxUI.lastTouchIndex=i end
   end
   buttons['v2/kickUI/btn11.png']()
   local req=sent[#sent];assert(req.mid==1051 and req.data.item_type==tid and req.data.item_count==1)
   assert(req.data.des_type==target[1] and req.data.des_id==target[2])
  end)
 end
end
check('disabled config stays closed on current screen',function()
 local data=ms.d_c.table_copy(FIXTURE.sync)
 data.local_rulai.times={{start_time=0,end_time=0}}
 data.local_rulai.pack_data.end_time=0;data.local_rulai.flag=false
 ms.d_data.callback_update_config(data)
 assert(not ui.canJoin());assert(ui.getShowHint()==0)
end)
check('closed schedule disables native entry',function()
 ui.getActivityTime({{start_time=0,end_time=0}});assert(not ui.canJoin())
end)
ui.close_schedulescriptfunc();if ui.g_bagua then ui.g_bagua:stopAllActions() end
for _,scene in ipairs(scenes) do scene:removeAllChildrenWithCleanup(true);scene:release() end
for i=#saved,1,-1 do local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end;for k,v in pairs(row.old) do row.t[k]=v end end
ms.MS_report_error=report
local out={};for _,v in ipairs(checks) do out[#out+1]=v.name..':'..tostring(v.ok)..':'..v.error end
return table.concat(out,'\n')
