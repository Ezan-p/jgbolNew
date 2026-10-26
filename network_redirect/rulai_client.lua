-- Keep original turntable widgets, animations and requests [A].
-- Synchronize local recharge/season state without opening a scene at login [B].
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_turntableUI
 if not ui or not ms.d_data or not ms.d_rechargeUI then return 'pending' end
 if not ui._localRulaiRestore then
  local originalConfig=ms.d_data.callback_update_config
  local originalResult=ui.onGetResult
  local originalClose=ms.d_rechargeUI.pressClose
  local pending
  local function active()
   return ms.d_loginUI.g_currentSence==ms.d_loginUI.senceID.rulaitable
      and ui.g_self and ui.g_self.main_layer and ui.g_self.main_layer:getParent()
  end
  local function refresh(data)
   -- Native create() closes an expired scene mid-build and then dereferences it.
   -- Exit before rebuilding when the event was disabled or has expired.
   if not ui.canJoin() then
    ui.close_schedulescriptfunc()
    if ui.g_bagua then ui.g_bagua:stopAllActions() end
    ui.call_back_close()
    return
   end
   local s=ui.g_self;local p=data.pack_data;local e=p.ext_info
   s.data={total_time=p.cur_count,total_charge=p.order_pay,charge_his=p.order_list,
     reward_list=p.random_table,itemInfo=e.item,itemList=e.attach_list,
     prize_status=e.prize_flag,special_need_charge=e.reach_money}
   s.end_time=p.end_time
   ui.close_schedulescriptfunc()
   ui.update()
  end
  ms.d_data.callback_update_config=function(data)
   local result=originalConfig(data)
   if data and data.local_rulai then
    local v=data.local_rulai
    ui.getActivityTime(v.times);ui.g_self.showtime=v.flag
    if active() then
     if ms.d_rechargeUI.g_self.main_layer then pending=v else refresh(v) end
    end
   end
   return result
  end
  ms.d_rechargeUI.pressClose=function(...)
   local result=originalClose(...)
   if pending then
    local data=pending;pending=nil
    if active() then refresh(data) end
   end
   return result
  end
  ui.onGetResult=function(data)
   if data.id==0 and data.pack_data then
    local p=data.pack_data
    ui.g_self.showtime=p.cur_count>0 or p.ext_info.prize_flag==2
   end
   return originalResult(data)
  end
  ui._localRulaiRestore=function()
   ms.d_data.callback_update_config=originalConfig
   ms.d_rechargeUI.pressClose=originalClose
   ui.onGetResult=originalResult;ui._localRulaiRestore=nil
  end
 end
end
