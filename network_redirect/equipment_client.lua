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
-- 3.87 eventMgr retains event 7 but forgeUI no longer exports updateForgeList.
-- Bridge it to the shipped activity snapshot reader, preserving original UI.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_forgeUI
 if ui and not ui._localCraftingRestore then
  local original=ui.updateForgeList
  local originalShow,originalNeed=ui.show,ui.isNeedUpdateList
  ui.isNeedUpdateList=function() return not ui.canJoin() end
  ui.show=function(parent)
   if not ui.canJoin() then ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_query_compose_list,{flag=0});return end
   return originalShow(parent or (ms.d_mainUI.g_mainUI and ms.d_mainUI.g_mainUI.main_layer))
  end
  ui.updateForgeList=function(data)
   if not data.equip_compose then if original then return original(data) end; return end
   ui.updateActivityStatus(data)
   if data.show then ui.show() end
  end
  ui._localCraftingRestore=function() ui.updateForgeList=original;ui.show=originalShow;ui.isNeedUpdateList=originalNeed;ui._localCraftingRestore=nil end
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
