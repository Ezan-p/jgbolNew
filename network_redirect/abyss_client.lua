-- Native abyssUI L1887-1890 compares remaining >= maximum, blocking 5/5.
-- Keep the native panel and counter; let the server settle the current day.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_abyssUI
 if not ui or not ui.showBossLayer or not ui.sendRequest then return 'pending' end
 if not ui._localBossRestore then
  local original=ui.showBossLayer
  local function challenge()
   local info=ui.g_data and ui.g_data.boss and ui.g_data.boss.specter_info
   if not info then ui.sendRequest(16,{});return end
   if info.complete then
    ms.d_info.show('九幽八十一层已全部通关，可继续挂机、炼药和兑换。');return
   end
   -- Do not reject a cached 0/5 here: the server may have crossed midnight.
   ms.d_lineupUI.getCharacterCSVConfig('specter_boss')
   ms.d_lineupUI.saveLastFightLevel()
   ui.sendRequest(6,{})
  end
  ui.showBossLayer=function(...)
   local create=ms.d_u.createMenu
   ms.d_u.createMenu=function(config,...)
    for _,row in ipairs(config) do
     if row.npic=='v2/abyssUI/challenge1.png' then row.call_back=challenge end
    end
    return create(config,...)
   end
   local ok,result=pcall(original,...)
   ms.d_u.createMenu=create
   if not ok then error(result,0) end
   return result
  end
  ui._localBossRestore=function() ui.showBossLayer=original;ui._localBossRestore=nil end
 end
end

-- Native showChallengeSuccess looks up every reward as an item (L2393).
-- Silver has attach_type=0, so it throws before installing the close touch
-- handler (L2407). Give the delayed renderer its own currency-aware helpers;
-- nested Lua 5.1 closures retain this environment after the outer call returns.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_abyssUI
 if ui and ui.showChallengeSuccess and not ui._localAbyssSuccessRestore then
  local original=ui.showChallengeSuccess
  ui.showChallengeSuccess=function(...)
   local rewardType
   local data=setmetatable({
    getCertainSmallSprite=function(typ,...)
     rewardType=typ
     return ms.d_data.getCertainSmallSprite(typ,...)
    end,
    getItemName=function(tid,...)
     if rewardType==12 then return '银币' end
     if rewardType==11 then return '元宝' end
     return ms.d_data.getItemName(tid,...)
    end
   },{__index=ms.d_data})
   local env=getfenv(original)
   local proxy=setmetatable({d_data=data},{__index=ms})
   setfenv(original,setmetatable({d_ms=proxy},{__index=env,__newindex=env}))
   local ok,result=pcall(original,...)
   setfenv(original,env)
   if not ok then error(result,0) end
   return result
  end
  ui._localAbyssSuccessRestore=function()
   ui.showChallengeSuccess=original;ui._localAbyssSuccessRestore=nil
  end
 end
end

-- The native random-event redraw creates a fresh empty button upvalue when
-- reusing its existing layer. A thief response then indexes btns[2] (nil).
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_abyssUI
 if ui and ui.showRandomEvent and not ui._localAbyssEventsRestore then
  local original=ui.showRandomEvent
  ui.showRandomEvent=function(parent,...)
   local data=ui.g_data and ui.g_data.random
   local layer=parent or (ui.g_abyssUI and ui.g_abyssUI.hook_layer)
   if data and data.event_type==4 and data.op_type~=2 and layer and ui.tagDef then
    local old=layer:getChildByTag(ui.tagDef.random_layer)
    if old then layer:removeChild(old,true) end
   end
   return original(parent,...)
  end
  ui._localAbyssEventsRestore=function() ui.showRandomEvent=original;ui._localAbyssEventsRestore=nil end
 end
 local drug=ms and ms.d_yaoshendianUI
 if drug and drug.getBitFromInt and not drug._localAbyssDrugBitsRestore then
  local original=drug.getBitFromInt
  drug.getBitFromInt=function(value,...)
   return original((tonumber(value) or 0)%4294967296,...)
  end
  drug._localAbyssDrugBitsRestore=function() drug.getBitFromInt=original;drug._localAbyssDrugBitsRestore=nil end
 end
end
