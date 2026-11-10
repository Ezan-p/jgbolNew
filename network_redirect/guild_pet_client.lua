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
  local function guardTask(index,typ)
   local main=ui.g_data.main or {}
   if main.task_last_time and ms.d_time.getTime()>=main.task_last_time then
    refreshTasks();return true
   end
   for _,task in pairs(main.union_task or {}) do
    local completed=task.completed
    if typ and task.completed_modes then completed=task.completed_modes[typ] end
    if task.index==index and completed then
     ms.d_info.show('已挑战');return true
    end
   end
   return false
  end
  local send=ui.sendRequest
  replace(ui,'sendRequest',function(op,data,...)
   if op==84 or op==85 then
    local main=ui.g_data.main or {}
    data=data or {}
    if guardTask(data.task_index or ui.g_self.cur_task_index,data.task_type or (op==85 and 2)) then return end
    data.task_day=ui.g_self.cur_task_day or main.task_day
   end
   return send(op,data,...)
  end)
  local taskLayer=ui.showTaskLayer
  replace(ui,'showTaskLayer',function(parent,task,...)
   if guardTask(task and task.index or ui.g_self.cur_task_index) then return end
   if task then ui.g_self.cur_task_index=task.index or ui.g_self.cur_task_index end
   ui.g_self.cur_task_day=ui.g_data.main and ui.g_data.main.task_day
   local index,day=ui.g_self.cur_task_index,ui.g_self.cur_task_day
   local menu=ms.d_u.createMenu
   ms.d_u.createMenu=function(options,...)
    for _,row in ipairs(options) do
     local typ=({['v2/pethuntUI/rtask1.png']=1,['v2/pethuntUI/ctask1.png']=2,['v2/pethuntUI/mtask1.png']=2})[row.npic]
     if typ and row.call_back then
      local callback=row.call_back
      row.call_back=function(...)
       if day~=ui.g_data.main.task_day then return end
       if guardTask(index,typ) then return end
       return callback(...)
      end
     end
    end
    return menu(options,...)
   end
   local ok,result=pcall(taskLayer,parent,task,...)
   ms.d_u.createMenu=menu
   if not ok then error(result) end
   return result
  end)
  local showMain=ui.showMainLayer
  replace(ui,'showMainLayer',function(...)
   refreshLayer=nil;refreshTime=nil
   -- Native buttons check quotas before opening the task. Check completion
   -- first so a finished target still says "已挑战" when all quotas are zero.
   local menu=ms.d_u.createMenu
   ms.d_u.createMenu=function(options,...)
    for _,row in ipairs(options) do
     if row.npic=='v2/pethuntUI/challenge1.png' and row.call_back then
      local task=(ui.g_data.main.union_task or {})[row.tag]
      local callback,index,day=row.call_back,task and task.index,ui.g_data.main.task_day
      row.call_back=function(...)
       if day~=ui.g_data.main.task_day then return end
       if guardTask(index) then return end
       -- Six daily challenges can bank six encounters. The original button
       -- blocks at five, which would otherwise prevent the sixth challenge.
       if task and task.completed_modes then
        local main=ui.g_data.main
        if (main.free_task_times or 0)<=0 and (main.pay_task_times or 0)<=0 then
         return ms.d_info.show('挑战次数不足')
        end
        return ui.showTaskLayer(ui.g_pethuntUI.main_layer,task)
       end
       return callback(...)
      end
     end
    end
    return menu(options,...)
   end
   local ok,result=pcall(showMain,...)
   ms.d_u.createMenu=menu
   if not ok then error(result) end
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
    -- Keep the authoritative full list and its completion flags; bypass
    -- the native settlement's per-target mutation.
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

  local function canSupport(data)
   -- Native callbacks use 0=available/1=unavailable; new replies use booleans.
   if not data or not (data.can_support==true or data.can_support==0) then return false end
   if (data.support_remaining or 0)<=0 then return false end
   local deadline=data.rest_time or data.last_time
   return not deadline or ms.d_time.getTime()<deadline
  end
  local updateSupport=pet.upDateSupport
  replace(pet,'upDateSupport',function(...)
   local state=pet.g_self;local data=state.g_data
   if not data or data.support_limit==nil then
    if updateSupport then return updateSupport(...) end
    return
   end
   if not state.g_Shilian_layer then return end
   local enabled=canSupport(data)
   if state.support1 then
    state.support1:setVisible(enabled)
    if state.support1.setEnabled then state.support1:setEnabled(enabled) end
   end
   if state.support2 then state.support2:setVisible(not enabled) end
   for _,node in pairs(state.g_suppor_info or {}) do
    node:setString('+'..tostring(data.support_bonus_percent or 0)..'%')
   end
   local parent=state.support2 and state.support2:getParent()
   if parent then
    local label=parent:getChildByTag(910078)
    if not label then
     label=ms.d_u.createByStyles({type='label',fontsize=16,color={255,210,181},string=''})
     label:setTag(910078);parent:addChild(label)
     ms.d_u.setProperties(parent,label,{x=0.5,y=0.08})
    end
    label:setString('今日点赞 '..tostring(data.support or 0)..'/'..data.support_limit..'（每次+'..data.support_percent..'%）')
   end
  end)
  local support=pet.sendMsgSupport
  if support then replace(pet,'sendMsgSupport',function(...)
   local data=pet.g_self.g_data
   if data and data.support_limit~=nil then
    if not canSupport(data) then
     return ms.d_info.show((data.support_remaining or 0)<=0 and '今日试炼点赞次数已用完' or '当前试炼不可点赞')
    end
    local cost=data.support_gold or 0
    if cost>0 then
     local function enoughGold()
      local player=ms.d_mainUI and ms.d_mainUI.g_playerInfo
      if player and tonumber(player.gold_coin) and tonumber(player.gold_coin)<cost then
       ms.d_info.show('元宝不足，点赞需要'..cost..'元宝');return false
      end
      return true
     end
     if not enoughGold() then return end
     local layer=pet.g_self.g_Shilian_layer
     if not layer then return end
     local used=data.support;local finished=false;local args={...}
     data.can_support=false;pet.upDateSupport()
     local function restore()
      if finished then return false end
      finished=true
      if pet.g_self.g_data~=data or pet.g_self.g_Shilian_layer~=layer or data.support~=used then return false end
      data.can_support=true;pet.upDateSupport()
      return true
     end
     return ms.d_quitUI.createYesNoByStyle(layer,{string=string.format(
      '本次点赞消耗%d元宝，挑战队伍生命、攻击、防御、法术各增加%d%%。今日还可点赞%d次，是否继续？',
      cost,data.support_percent,data.support_remaining)},function()
       if not restore() then return end
       if not canSupport(data) then return ms.d_info.show('当前试炼不可点赞') end
       if not enoughGold() then return end
       data.can_support=false;pet.upDateSupport()
       return support(unpack(args))
      end,function() restore() end)
    end
    data.can_support=false
    pet.upDateSupport()
   end
   return support(...)
  end) end
  local supportResult=pet.GetResultSupport
  replace(pet,'GetResultSupport',function(data,...)
   if data.result~=1 or data.support_limit==nil then
    if supportResult then return supportResult(data,...) end
    return
   end
   local cached=pet.g_self.g_data
   if not cached then return end
   for _,key in ipairs({'support','support_limit','support_remaining','support_percent','support_bonus_percent','support_gold','can_support'}) do
    cached[key]=data[key]
   end
   pet.upDateSupport()
   if (data.gold_cost or 0)>0 then
    ms.d_info.show('点赞成功，消耗'..data.gold_cost..'元宝，当前加成+'..data.support_bonus_percent..'%')
   end
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
   local menu,button=ms.d_u.createMenu,ms.d_u.CreateButton
   -- The native callback marks the button unavailable immediately after send.
   -- Our send opens a confirmation first, and owns locking/cancellation itself.
   ms.d_u.CreateButton=function(normal,selected,callback,...)
    if normal=='v2/petHomeUI/support1.png' then callback=function() pet.sendMsgSupport() end end
    return button(normal,selected,callback,...)
   end
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
    local function adoption(floor)
     return ((data.train_prize or {})[floor] or {}).add_catch_count or 0
    end
    local labels={pet_reward_info1='一层累计领养+'..adoption(1),pet_reward_info2='二层累计领养+'..adoption(2),pet_reward_info3='三层累计领养+'..adoption(3),
     pet_reward_info4='银两×',pet_reward_info5='蟠桃×',pet_reward_info11='蟠桃×',
     pet_reward_info6='四层累计：银两×'..amount(4,12,0)..' 蟠桃×'..amount(4,5,1001)..' 领养+'..adoption(4)}
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
   ms.d_u.CreateButton=button
   ms.d_hz.gethz=gethz;ms.d_u.createByStyles=styles
   if not ok then error(result) end
   return result
  end)

  local prize=pet.GetResultPrize
  replace(pet,'GetResultPrize',function(data,...)
   if data.result~=1 or not data.trial_state then return prize(data,...) end
   if data.trial_state.trial_reward_mode=='silver_peach' then
    local cached=pet.g_self.g_InsidePetInfo
    if cached then
     if data.total_catch_times~=nil then cached.total_catch_times=data.total_catch_times end
     if data.left_catch_times~=nil then cached.left_catch_times=data.left_catch_times end
     if pet.g_self.total_catch_times then pet.g_self.total_catch_times:setString(tostring(cached.total_catch_times)) end
     if pet.g_self.g_rest_catch_times then pet.g_self.g_rest_catch_times:setString(tostring(cached.left_catch_times)) end
    end
    pet.g_self.g_data=data.trial_state
    pet.updataShiLianLayer()
    ms.d_messageUI.createGetItemsLayer(pet.g_self.g_Shilian_layer,{result=1,attach_list=data.prize_list},500)
    if (data.add_catch_count or 0)>0 then ms.d_info.show('获得领养次数×'..data.add_catch_count..'，周末可使用') end
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
