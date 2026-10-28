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
  local restore
  local refreshLayer,refreshTime
  local function refreshTasks()
   local layer=ui.g_pethuntUI.main_layer
   local now=ms.d_time.getTime()
   if refreshLayer==layer and refreshTime and now-refreshTime<5 then return end
   if layer and layer:getParent() then refreshLayer=layer end
   refreshTime=now
   ui.sendRequest(83,{})
  end
  local send=ui.sendRequest
  replace(ui,'sendRequest',function(op,data,...)
   if op==84 or op==85 then
    local main=ui.g_data.main or {}
    if main.task_last_time and ms.d_time.getTime()>=main.task_last_time then
     refreshTasks();return
    end
    data=data or {};data.task_day=ui.g_self.cur_task_day or main.task_day
   end
   return send(op,data,...)
  end)
  local taskLayer=ui.showTaskLayer
  replace(ui,'showTaskLayer',function(parent,task,...)
   if task then ui.g_self.cur_task_index=task.index or ui.g_self.cur_task_index end
   ui.g_self.cur_task_day=ui.g_data.main and ui.g_data.main.task_day
   return taskLayer(parent,task,...)
  end)
  local showMain=ui.showMainLayer
  replace(ui,'showMainLayer',function(...)
   refreshLayer=nil;refreshTime=nil
   local result=showMain(...)
   local layer=ui.g_pethuntUI.main_layer
   local main=ui.g_data.main
   local function tick()
    if ms._localGuildPetRestore~=restore or ui.g_pethuntUI.main_layer~=layer or not layer:getParent() then return end
    if main and main.task_last_time and ms.d_time.getTime()>=main.task_last_time then
     refreshTasks();ms.d_u.delay(layer,5,tick);return
    end
    ms.d_u.delay(layer,1,tick)
   end
   if layer and main and main.task_last_time then ms.d_u.delay(layer,1,tick) end
   return result
  end)
  local finish=ui.showTaskFinish
  replace(ui,'showTaskFinish',function(...)
   -- The native delayed reward renderer treats currency IDs as item IDs.
   -- Give its nested closure a private environment, so other screens and
   -- callbacks keep their own rendering helpers while this animation runs.
   local rewards=ui.g_data.task_finish and ui.g_data.task_finish.prize_list or {}
   local current,index=nil,0
   local dataProxy=setmetatable({
    getCertainSmallSprite=function(typ,tid,...)
     index=index+1;current=rewards[index]
     return ms.d_data.getCertainSmallSprite(typ,tid,...)
    end,
    getItemName=function(tid,...)
     if current and current.object_type==12 then return '银两' end
     if current and current.object_type==11 then return '元宝' end
     return ms.d_data.getItemName(tid,...)
    end
   },{__index=ms.d_data})
   local utilities=setmetatable({createByStyle=function(options,...)
    if current and options.type=='label' and options.y==0.3 then
     options.string=dataProxy.getItemName(current.attach_type)..'×'..tostring(current.attach_count)
     options.fontsize=22
    end
    return ms.d_u.createByStyle(options,...)
   end},{__index=ms.d_u})
   local env=getfenv(finish)
   local proxy=setmetatable({d_data=dataProxy,d_u=utilities},{__index=ms})
   setfenv(finish,setmetatable({d_ms=proxy},{__index=env,__newindex=env}))
   local ok,result=pcall(finish,...);setfenv(finish,env)
   if not ok then error(result) end
   return result
  end)
  local native=ui.onGetResult
  replace(ui,'onGetResult',function(op,data,...)
   if op==83 and data.result~=1 then refreshLayer=nil;refreshTime=nil end
   if data.result==1 and op==83 and refreshLayer then
    local layer=refreshLayer;refreshLayer=nil;refreshTime=nil
    ui.g_data.main=data
    if layer==ui.g_pethuntUI.main_layer and layer:getParent() then
     return ui.showMainLayer(layer:getParent())
    end
   end
   if data.result==1 and op==84 and data.task_state then
    ui.g_data.main=data.task_state
    ui.g_data.task_finish=data
    local layer=ui.g_pethuntUI.main_layer
    if layer and layer:getParent() then ui.showMainLayer(layer:getParent()) end
    -- Native settlement writes union_task[task_index], but the visible list
    -- is now compact after a target has been completed.
    if data.task_type==1 then return ui.showTaskFinish() end
    return
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
   local gethz,styles=ms.d_hz.gethz,ms.d_u.createByStyles
   if data.trial_reward_mode=='silver_peach' then
    local function amount(floor,typ,tid)
     local row=(data.train_prize or {})[floor] or {}
     for _,item in pairs(row.prize_list or {}) do
      if item.object_type==typ and item.attach_type==tid then return item.attach_count end
     end
     return 0
    end
    local silverRow,peachRow=0,0
    local labels={pet_reward_info1='通关一层累计',pet_reward_info2='通关二层累计',pet_reward_info3='通关三层累计',
     pet_reward_info4='银两×',pet_reward_info5='蟠桃×',pet_reward_info11='蟠桃×',
     pet_reward_info6='四层：银两×'..amount(4,12,0)..' 蟠桃×'..amount(4,5,1001)}
    ms.d_hz.gethz=function(key,...) return labels[key] or gethz(key,...) end
    ms.d_u.createByStyles=function(style,...)
     if style.type=='label' and type(style.string)=='string' then
      if style.string:find('银两×',1,true)==1 then
       silverRow=silverRow+1;style.string='银两×'..amount(silverRow,12,0)
      elseif style.string=='蟠桃×' then
       peachRow=peachRow+1;style.string='蟠桃×'..amount(peachRow,5,1001)
      elseif style.string==labels.pet_reward_info6 then style.fontsize=16 end
     end
     return styles(style,...)
    end
   end
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
   ms.d_hz.gethz=gethz;ms.d_u.createByStyles=styles
   if not ok then error(result) end
   return result
  end)

  local prize=pet.GetResultPrize
  replace(pet,'GetResultPrize',function(data,...)
   if data.result~=1 or not data.trial_state then return prize(data,...) end
   if data.trial_state.trial_reward_mode=='silver_peach' then
    pet.g_self.g_data=data.trial_state
    pet.updataShiLianLayer()
    ms.d_messageUI.createGetItemsLayer(pet.g_self.g_Shilian_layer,{result=1,attach_list=data.prize_list},500)
    return
   end
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
  restore=function()
   refreshLayer=nil;refreshTime=nil
   for i=#undo,1,-1 do undo[i]() end
   ms._localGuildPetRestore=nil
  end
  ms._localGuildPetRestore=restore
 end
end
