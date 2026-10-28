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
