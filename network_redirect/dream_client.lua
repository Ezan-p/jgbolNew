-- Preserve native 3x3 swaps, six illustrations, animations and friend picker [A].
-- Scope the 1263 reward/config and NPC friends to this activity [B].
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_dreamUI
 if not ui or not ms.d_followUI or not debug or not debug.getupvalue then return 'pending' end
 if not ui._localDreamRestore then
  local function up(fn,key,value,write)
   for i=1,100 do
    local name,current=debug.getupvalue(fn,i)
    if not name then break end
    if name==key then
     if write then debug.setupvalue(fn,i,value) end
     return current
    end
   end
  end
  local originalResponse,originalBless=ui.onGetResponse,ui.showBless
  local originalFinal,originalEntrance=ui.showFinalReward,ui.showEntrance
  local originalConfig=ms.d_data.getDreamConfig
  local originalTable=ms.d_data.g_dreamTable
  local originalUIConfig=ui.g_config
  local originalSend=up(ui.enter,'sendRequest')
  local originalText=up(originalFinal,'gethz')
  if not originalSend or not originalText then return 'pending' end
  local latest,roster,rewards,plus
  local function send(op,data)
   if op~=1 then
    if not latest or ms.d_time.getTime()>=latest.local_refresh_time then
     ms.d_info.show('梦境进度已刷新，请重新进入后操作')
     return originalSend(1)
    end
    data=data or {};data.local_token=latest.local_token
   end
   return originalSend(op,data)
  end
  -- Native sendRequest is one shared upvalue in enter, puzzle, bless and claim.
  up(ui.enter,'sendRequest',send,true)
  ms.d_data.getDreamConfig=function(...)
   if rewards then ms.d_data.g_dreamTable=rewards;return end
   return originalConfig(...)
  end
  ui.onGetResponse=function(data,...)
   if data.result~=1 then return originalResponse(data,...) end
   latest=data.dream_data;roster=data.local_friends;rewards=data.local_rewards;plus=data.plus_data
   if data.local_activity then ui.updateActivityStatus(data.local_activity) end
   local s=up(originalResponse,'g_self')
   if s then s.dream_data=latest;s.plus_data=plus end
   if rewards then ms.d_data.g_dreamTable=rewards;ui.g_config=rewards end
   return originalResponse(data,...)
  end
  ui.showBless=function(...)
   local view=up(originalBless,'g_dreamUI')
   if view and not view.friends and roster then
    view.friends={}
    for _,player in ipairs(roster) do
     view.friends[#view.friends+1]={isChosen=false,player=player}
    end
   end
   return originalBless(...)
  end
  -- The shipped final screen still hard-codes dream20, contradicting its preview.
  up(originalFinal,'gethz',function(key,...)
   if key=='dream20' and plus and plus.charge_prize then
    local parts={}
    for _,p in ipairs(plus.charge_prize) do
     local info=ms.d_data.getCertainInfo(p.object_type,p.attach_type)
     parts[#parts+1]=(info.name or tostring(p.attach_type))..'×'..p.attach_count
    end
    return table.concat(parts,'  ')
   end
   return originalText(key,...)
  end,true)
  ui.showFinalReward=function(...)
   if latest and latest.take_charge then return ms.d_info.show('本期仙梦居祝福已领取') end
   -- Native fallAsleep uses can_take with the display argument inverted.
   return originalFinal(latest and latest.can_take or false)
  end
  ui.showEntrance=function(...)
   local result=originalEntrance(...)
   local view=up(originalEntrance,'g_dreamUI')
   local layer=view and view.main_layer
   if layer and latest then
    layer:removeChildByTag(746040,true)
    local left=math.max(0,latest.local_refresh_time-ms.d_time.getTime())
    local label=ms.d_u.createByStyles({type='label',font='arial',fontsize=18,x=0.5,y=0.10,
     color={255,225,150},string=string.format('本期剩余%d天%d小时 · 祝福好友为离线NPC',
      math.floor(left/86400),math.floor(left/3600)%24)})
    layer:addChild(label,10,746040)
   end
   return result
  end
  ui._localDreamRestore=function()
   up(ui.enter,'sendRequest',originalSend,true)
   up(originalFinal,'gethz',originalText,true)
   ui.onGetResponse=originalResponse;ui.showBless=originalBless
   ui.showFinalReward=originalFinal;ui.showEntrance=originalEntrance
   ms.d_data.getDreamConfig=originalConfig;ms.d_data.g_dreamTable=originalTable
   ui.g_config=originalUIConfig
   ui._localDreamRestore=nil
  end
 end
end
