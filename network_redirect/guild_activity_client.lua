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
  local nativePage=secret.showPrizePage
  replace(secret,'showPrizePage',function(parent,...)
   remainingLabel=nil;remainingParent=nil
   local s=secret.g_self;local data=s.prize_data or {}
   if data.free_times~=nil then s.free_times=data.free_times end
   local count=s.fight_count
   if data.cleared_layer~=nil then s.fight_count=data.cleared_layer end
   local create=ms.d_u.createByStyles
   ms.d_u.createByStyles=function(options,...)
    local node=create(options,...)
    if options.type=='label' and options.string==string.format(ms.d_hz.gethz('secretArea_free_times'),s.free_times) then
     remainingLabel=node;remainingParent=parent;node:setTag(910043)
    end
    return node
   end
   local ok,result=pcall(nativePage,parent,...)
   ms.d_u.createByStyles=create;s.fight_count=count
   if not ok then error(result) end
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
   local ok,result=pcall(nativeTeam,...);s.fight_count=count
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
