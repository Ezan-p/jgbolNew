-- Offline guild activity fixes; keep original Cocos screens and callbacks.
do
 local ms=package.loaded.ms
 if not (ms and ms.d_petHomeUI and ms.d_secretAreaUI and ms.d_escortUI) then return 'pending' end
 if not ms._localGuildActivitiesRestore then
  local undo={}
  local function replace(t,key,fn)
   local old=t[key];t[key]=fn
   undo[#undo+1]=function() t[key]=old end
   return old
  end
  -- Per-function environments also cover the nested native timer closures.
  -- Never change the game's global clock/weekend rules for other activities.
  local pet=ms.d_petHomeUI
  for name,weekend in pairs({GetPetMenu=true,createShiLianLayer=true,GetResultInsidePetInfo=false}) do
   local fn=pet[name];local original=getfenv(fn)
   local time=setmetatable({is_weekend=function() return weekend end},{__index=ms.d_time})
   local proxy=setmetatable({d_time=time},{__index=ms})
   local env=setmetatable({d_ms=proxy},{__index=original,__newindex=original})
   setfenv(fn,env);undo[#undo+1]=function() setfenv(fn,original) end
  end
  local petMS=pet.d_ms
  local hz=setmetatable({gethz=function(key,...)
   if key=='pet_lucky_hint5' then return '领养活动每日开放' end
   return ms.d_hz.gethz(key,...)
  end},{__index=ms.d_hz})
  pet.d_ms=setmetatable({d_hz=hz},{__index=petMS})
  undo[#undo+1]=function() pet.d_ms=petMS end

  local secret=ms.d_secretAreaUI
  local remainingLabel,remainingParent
  local function rememberLabel(node,parent)
   remainingLabel=node;remainingParent=parent;node:setTag(910043)
   node:registerScriptHandler(function(event)
    if (event=='exit' or type(event)=='table' and event.name=='exit') and remainingLabel==node then
     remainingLabel=nil;remainingParent=nil
    end
   end)
  end
  local nativePage=secret.showPrizePage
  replace(secret,'showPrizePage',function(parent,...)
   remainingLabel=nil;remainingParent=nil
   local s=secret.g_self;local data=s.prize_data or {}
   -- Repair a cached 25-slot page until the new server response arrives.
   if data.prize_items and #data.prize_items>18 then
    for i=#data.prize_items,19,-1 do data.prize_items[i]=nil end
    data.sort_list={}
   end
   if data.free_times~=nil then s.free_times=data.free_times end
   local count=s.fight_count
   if data.cleared_layer~=nil then s.fight_count=data.cleared_layer end
   local create=ms.d_u.createByStyles
   local menu=ms.d_u.createMenu
   ms.d_u.createMenu=function(styles,buttons,...)
    if styles[3] and styles[3].call_back==secret.pressCloseSearch then
     if s.free_times>0 then
      styles[1].npic='v2/secretArea/onekey_money1.png'
      styles[1].spic='v2/secretArea/onekey_money2.png'
      styles[1].dispic='v2/secretArea/onekey_money3.png'
      local w=ms.d_u.getRealScale(s.prize_bkg)
      parent:addChild(create({type='label',fontsize=26,string=tostring(data.sweep_gold_cost or 10),x=0.5+0.4*w,y=styles[1].y,color={235,225,185}}),200)
     end
     local function draw(flag)
      if (s.free_times or 0)<=0 then return end
      secret.send_msg_union_event(43,{flag=flag})
     end
     styles[1].call_back=function()
      if (s.free_times or 0)<=0 then return end
      ms.d_quitUI.createYesNoByStyle(parent,{string=string.format('消耗%d元宝，探宝剩余%d次？',data.sweep_gold_cost or 10,s.free_times)},function() draw(6) end)
     end
     styles[2].call_back=function() draw(2) end
    end
    return menu(styles,buttons,...)
   end
   local costNodes={}
   ms.d_u.createByStyles=function(options,...)
    if options.type=='label' and options.string==string.format(ms.d_hz.gethz('secretArea_prize_tink1'),s.fight_count,data.max_free_times or s.fight_count) then
     options.string=string.format('今日已通关%d/%d层，累计获得%d次探宝机会。',data.cleared_layer or 0,data.max_layer or 3,data.earned_search_times or 0)
    end
    local node=create(options,...)
    if options.type=='label' and options.string==string.format(ms.d_hz.gethz('secretArea_free_times'),s.free_times) then
     rememberLabel(node,parent)
    elseif s.free_times==0 and options.pic=='v2/money_gold.png' then
     node:setVisible(false)
    elseif s.free_times==0 and (options.x or 0)>0.5 then
     costNodes[#costNodes+1]={node=node,y=options.y}
    end
    return node
   end
   local ok,result=pcall(nativePage,parent,...)
   ms.d_u.createByStyles=create;ms.d_u.createMenu=menu;s.fight_count=count
   if not ok then error(result) end
   if s.free_times==0 then
    local w,h=ms.d_u.getRealScale(s.prize_bkg)
    for _,entry in ipairs(costNodes) do
     if entry.y==0.45-0.14*h then entry.node:setVisible(false) end
    end
    local label=create({type='label',fontsize=22,string=string.format(ms.d_hz.gethz('secretArea_free_times'),0),x=0.5+0.32*w,y=0.45-0.14*h,color={211,198,176}})
    rememberLabel(label,parent);parent:addChild(label)
    for i=1,2 do if s.prize_btns[i] then ms.d_u.grayMenuItem(s.prize_btns[i]);s.prize_btns[i]:setEnabled(false) end end
   end
   return result
  end)
  local nativeFree=secret.setFreeTimes
  replace(secret,'setFreeTimes',function(count,...)
   local result=nativeFree(count,...)
   if count~=nil and remainingLabel and remainingParent==secret.g_self.main_layer and remainingParent:getChildByTag(910043) then
    remainingLabel:setString(string.format(ms.d_hz.gethz('secretArea_free_times'),count))
   end
   return result
  end)
  local nativeSearch=secret.callback_fam_search_gold
  replace(secret,'callback_fam_search_gold',function(data,...)
   if data.result==1 and (data.flag==2 or data.flag==6) and data.board_size==18 then
    -- Use the authoritative board and counts for both single and sweep results.
    secret.g_self.prize_data=data;data.sort_list={}
    secret.setFreeTimes(data.free_times,data.fight_count)
    secret.showPrizePage(secret.g_self.main_layer)
    local prizes={}
    for _,p in pairs(data.prize_list or {}) do prizes[#prizes+1]=p end
    ms.d_commonLayerUI.showPrizeResLayer(secret.g_self.g_parent_layer,prizes)
    return
   end
   if data.result==1 and data.flag~=7 then
    local cached=secret.g_self.prize_data
    if cached then
     for _,key in ipairs({'free_times','max_free_times','search_count','cleared_layer','max_layer','all_point'}) do
      if data[key]~=nil then cached[key]=data[key] end
     end
    end
   end
   return nativeSearch(data,...)
  end)
  local nativeTeam=secret.showTeamPage
  replace(secret,'showTeamPage',function(...)
   remainingLabel=nil;remainingParent=nil
   local s=secret.g_self;local team=s.teams_info and s.teams_info.team
   local count=s.fight_count
   if team and team.cleared_layer~=nil then s.fight_count=team.cleared_layer end
   local menu=ms.d_u.createMenu
   ms.d_u.createMenu=function(styles,buttons,...)
    -- Keep the native timestamp/label logic. Only the primary action needs
    -- to continue after the first fight instead of switching permanently.
    if team and team.can_continue~=nil and styles[5] and styles[6] and styles[6].call_back==secret.getTeamsInfo then
     local action=styles[5]
     if team.can_continue then
      action.npic='v2/worldTreeUI/fight1.png';action.spic='v2/worldTreeUI/fight2.png';action.call_back=secret.pressFight
     else
      action.npic='v2/secretArea/explore21.png';action.spic='v2/secretArea/explore22.png';action.call_back=secret.pressExplore
     end
    end
    return menu(styles,buttons,...)
   end
   local ok,result=pcall(nativeTeam,...);s.fight_count=count;ms.d_u.createMenu=menu
   if not ok then error(result) end
   return result
  end)

  local escort=ms.d_escortUI
  local nativeRest=escort.getEscortRestTime
  replace(escort,'getEscortRestTime',function(format,...)
   local state=escort.g_escortUI
   if state and state.offline_active~=nil then
    if not state.offline_active then return false end
    return ms.d_time.getRestTime(state.offline_end_time,format or ms.d_time.g_format.colon)
   end
   return nativeRest(format,...)
  end)
  local nativeResponse=escort.onGetResponse
  replace(escort,'onGetResponse',function(data,...)
   if data.result==1 and data.escort_active~=nil then
    local state=escort.g_escortUI
    state.offline_active=data.escort_active;state.offline_end_time=data.escort_end_time
    state.can_rece_prize=data.can_rece_prize;state.my_road_type=data.on_road_type
    if data.escort_active then ms.d_mainUI.g_playerInfo.last_west_book_time=data.escort_end_time-3600 end
   end
   return nativeResponse(data,...)
  end)
  ms._localGuildActivitiesRestore=function()
   for i=#undo,1,-1 do undo[i]() end
   ms._localGuildActivitiesRestore=nil
  end
 end
end
