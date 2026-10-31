-- equipmentUpgradeUI:722-724 grays both buttons whenever a multi-step
-- response finishes, even when our ten-attempt batch stops below the cap.
-- Scope the correction to that result function and its delayed animation
-- closure; other screens and createEnhanceLayer keep the native utility.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_equipmentUpgradeUI
 if ui and ui.changeEquipmentInfo and ui.checkEquipmentCanUpgrade
   and ui.checkCanBatchUpgrade and not ui._localEnhanceButtonsRestore then
  local original=ui.changeEquipmentInfo
  local env=getfenv(original)
  local active=true
  local utilities=setmetatable({grayMenuItem=function(button,...)
   local buttons=ui.g_enhanceButtons
   if active and ui.g_skill_anim_on==false and buttons
     and (button==buttons[2] or button==buttons[3])
     and ui.checkEquipmentCanUpgrade(false)==0
     and (button==buttons[2] or ui.checkCanBatchUpgrade(false)) then
    return
   end
   return ms.d_u.grayMenuItem(button,...)
  end},{__index=ms.d_u})
  local proxy=setmetatable({d_u=utilities},{__index=ms})
  setfenv(original,setmetatable({d_ms=proxy},{__index=env,__newindex=env}))
  ui._localEnhanceButtonsRestore=function()
   active=false
   setfenv(original,env);ui._localEnhanceButtonsRestore=nil
  end
 end
end
-- Local protocol adapter: original lineupUI explicitly ignores owner_id deltas.
-- Keep double-precision ownership in event 83; preserve selected object references.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_stoneUI
 if ui and not ui._localEquipmentRestore then
  local original=ui.onGetResponse
  ui.onGetResponse=function(data)
   for _,link in ipairs(data.stone_links or {}) do
    for _,item in ipairs(ms.d_packageUI.g_packageItemsInfo or {}) do
     if item.id==link.id then item.owner_id=link.owner_id;item.equip_pos=link.equip_pos end
    end
   end
   return original(data)
  end
  ui._localEquipmentRestore=function() ui.onGetResponse=original;ui._localEquipmentRestore=nil end
 end
end
-- release_w 1263 has level-14 recipes and showTilian supports level 13, but
-- pressCast still rejects everything above 12. Keep all other native paths.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_stoneCastUI
 if ui and ui.pressCast and ui.showTilian and ui.initConfig and not ui._localStoneRefineRestore then
  local original=ui.pressCast
  ui.pressCast=function(parent,stone,zOrder)
   if not stone or stone.level~=13 then return original(parent,stone,zOrder) end
   ui.initConfig()
   local cfg=stone.csvInfo or ms.d_data.getCertainInfo(ms.d_common_def.object_type.item,stone.type_id)
   local recipes=ui.g_self.csv and cfg and ui.g_self.csv[cfg.sub_type]
   if not recipes or not recipes[14] then return original(parent,stone,zOrder) end
   local realm=ms.d_mainUI.g_playerInfo.reborn_layer or 0
   local condition=ms.d_roleRebornUI.g_reborn_condition[realm]
   if realm<4 or not condition or not condition.rights or not condition.rights.open_stone_sys then
    return ms.d_info.show(ms.d_hz.gethz('asc30'))
   end
   ui.g_stoneCastUI.parent_layer=parent
   ui.g_stoneCastUI.zOrder=zOrder or 100
   ui.g_stoneCastUI.stone=stone
   return ui.showTilian()
  end
  ui._localStoneRefineRestore=function()
   ui.pressCast=original;ui._localStoneRefineRestore=nil
  end
 end
end
-- The shipped fragment result always labels its prize as object_type.item.
-- Five-star passive fragments produce a skill; use the server's typed prize list.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_equipPieceUI
 if ui and not ui._localFragmentRestore then
  local original=ui.onGetComposeResult
  ui.onGetComposeResult=function(data)
   if data.object_type==6 and data.attach_list then
    local parent=ui.g_equipPieceUI and ui.g_equipPieceUI.main_layer
    if parent then
     ui.showPieceInfo()
     ms.d_commonLayerUI.showPrizeResLayer(parent,data.attach_list)
    end
    return
   end
   return original(data)
  end
  ui._localFragmentRestore=function() ui.onGetComposeResult=original;ui._localFragmentRestore=nil end
 end
end
-- [B] Mirror the narrow 10001 recipe correction in the smith preview.
-- Original getItemFromStr discards weight, so match both duplicate positions.
do
 local ms=package.loaded.ms
 local data=ms and ms.d_data
 if data and data.getTransInfoByTypeid and not data._localFragmentPoolRestore then
  local original=data.getTransInfoByTypeid
  local changed={}
  local function fix()
   for _,row in pairs((data.g_convertTable or {})[10001] or {}) do
    local src,dst=row.src_material,row.des_material
    if src and src.attach_type==10001 and dst and #dst==19
      and dst[3].object_type==5 and dst[3].attach_type==10204
      and dst[4].attach_type==10204 then
     changed[#changed+1]=dst[3];dst[3].attach_type=10203
    end
   end
  end
  data.getTransInfoByTypeid=function(id,...)
   if id==10001 then fix() end
   return original(id,...)
  end
  fix()
  data._localFragmentPoolRestore=function()
   for _,prize in ipairs(changed) do prize.attach_type=10204 end
   data.getTransInfoByTypeid=original;data._localFragmentPoolRestore=nil
  end
 end
end
-- Batch sale retains its category array even when inventory snapshots replace it.
-- Remove consumed IDs from that same array before the original result refresh.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_batchSaleUI
 if ui and not ui._localSaleRestore then
  local originalShow,originalResult=ui.show,ui.getSaleResult
  local shown
  ui.show=function(items) shown=items;return originalShow(items) end
  ui.getSaleResult=function(data)
   if shown then
    local alive={}
    for _,item in ipairs(ms.d_packageUI.g_packageItemsInfo or {}) do alive[item.id]=item.count>0 end
    for n=#shown,1,-1 do if not alive[shown[n].id] then table.remove(shown,n) end end
   end
   return originalResult(data)
  end
  ui._localSaleRestore=function() ui.show=originalShow;ui.getSaleResult=originalResult;ui._localSaleRestore=nil end
 end
end
