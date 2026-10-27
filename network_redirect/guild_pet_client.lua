-- Spirit-land battles, settlement and trial navigation on the native Cocos UI.
do
 local ms=package.loaded.ms
 if not (ms and ms.d_pethuntUI and ms.d_fightUI and ms.d_petHomeUI) then return 'pending' end
 if not ms._localGuildPetRestore then
  local ui,pet,fight=ms.d_pethuntUI,ms.d_petHomeUI,ms.d_fightUI
  local undo={}
  local function replace(t,key,fn)
   local old=t[key];t[key]=fn;undo[#undo+1]=function() t[key]=old end
  end
  local native=ui.onGetResult
  replace(ui,'onGetResult',function(op,data,...)
   if data.result==1 and op==84 and data.task_state then
    ui.g_data.main=data.task_state
    if ui.g_pethuntUI.main_layer then ui.addMainBottomLayer(ui.g_pethuntUI.main_layer) end
   end
   if data.result==1 and op==85 then
    local replay=data.fight_result_list and data.fight_result_list[1]
    if not replay then return ms.d_info.show('暂无挑战战报，请重新进入挑战') end
    ui.g_self.cur_task_index=data.task_index or ui.g_self.cur_task_index
    replay.line_up_msg.lineup_count=#replay.line_up_msg.lineup
    replay.fight_result_msg.fight_round=#replay.fight_result_msg.fight_result
    -- showFightEnd reads the event type, independently of actFight's argument.
    ms.d_event_mgr.setSpecialFightType(28)
    return fight.actFight(replay,28)
   end
   if data.result==1 and op==87 then
    if ui.g_data.field_boss and data.left_times~=nil then ui.g_data.field_boss.left_times=data.left_times end
    if data.two_type==1 then ui.g_self.playing_hunt_ani=false end
   end
   return native(op,data,...)
  end)

  local returnToTrial=false
  local inside=pet.GetResultInsidePetInfo
  replace(pet,'GetResultInsidePetInfo',function(...)
   local result=inside(...)
   if returnToTrial then returnToTrial=false;pet.showShilianLayer() end
   return result
  end)
  local endFight=fight.showFightEnd
  local originalHome=fight.menuHome_private
  replace(fight,'showFightEnd',function(...)
   local kind=fight.g_fightUI.last_fight_type
   if kind~=27 and kind~=28 then return endFight(...) end
   -- Render the ordinary victory/defeat panel instead of trial auto-play.
   local getType=ms.d_event_mgr.getLastFightType
   ms.d_event_mgr.getLastFightType=function() return 28 end
   local ok,result=pcall(endFight,...)
   ms.d_event_mgr.getLastFightType=getType
   if not ok then error(result) end
   local home=fight.menuHome_private
   fight.menuHome_private=function(...)
    if kind==28 then
     local value=home(...)
     ms.d_event_mgr.setSpecialFightType(0)
     return value
    end
    if ms.d_u.try_lock_btn()==false then return end
    ms.d_event_mgr.setSpecialFightType(0)
    returnToTrial=true
    ms.d_xianmengUI.show(ms.d_xianmengUI.showTypeDef.pet)
    ui.showPetHome()
   end
   return result
  end)
  undo[#undo+1]=function() fight.menuHome_private=originalHome end

  local createTrial=pet.createShiLianLayer
  replace(pet,'createShiLianLayer',function(...)
   local data=pet.g_self.g_data
   -- The native page draws last_time and rest_time in the same header.
   -- Use its first timer for the active deadline, with only one timer closure.
   if data.rest_time then data.last_time=data.rest_time;data.rest_time=false end
   local menu=ms.d_u.createMenu
   ms.d_u.createMenu=function(options,...)
    local filtered={}
    for k,v in pairs(options) do if type(k)~='number' then filtered[k]=v end end
    for _,row in ipairs(options) do
     if row.npic~='v2/petHomeUI/pos1.png' then filtered[#filtered+1]=row end
    end
    return menu(filtered,...)
   end
   local ok,result=pcall(createTrial,...)
   ms.d_u.createMenu=menu
   if not ok then error(result) end
   return result
  end)

  local prize=pet.GetResultPrize
  replace(pet,'GetResultPrize',function(data,...)
   if data.result~=1 or not data.trial_state then return prize(data,...) end
   -- Preserve the native reputation/capture counters, then attach rewards to
   -- the refreshed page so rebuilding the next floor cannot destroy the popup.
   local popup=ms.d_messageUI.createGetItemsLayer
   local reward
   ms.d_messageUI.createGetItemsLayer=function(parent,items,z) reward={items=items,z=z} end
   local ok,result=pcall(prize,data,...)
   ms.d_messageUI.createGetItemsLayer=popup
   if not ok then error(result) end
   pet.g_self.g_data=data.trial_state
   pet.updataShiLianLayer()
   if reward and pet.g_self.g_Shilian_layer then popup(pet.g_self.g_Shilian_layer,reward.items,reward.z) end
   return result
  end)
  ms._localGuildPetRestore=function()
   for i=#undo,1,-1 do undo[i]() end
   ms._localGuildPetRestore=nil
  end
 end
end
