-- Add metadata to the native inventory registry; retain its card icon and UI.
do
 local ms=package.loaded.ms
 local bag=ms and ms.d_packageUI
 local common=ms and ms.d_commonLayerUI
 if not bag or not bag.getPackageCSVConfig or not bag.requestUseItem
  or not common or not common.recvUsedItem then return 'pending' end
 if not bag._localLevelCardRestore then
  local config=__LEVEL_CARD__
  local originalConfig,originalUse=bag.getPackageCSVConfig,bag.requestUseItem
  local originalResult=common.recvUsedItem
  local function register()
   local items=bag.g_itemAttrTable
   if not items or not items[1152] then return false end
   if not items[config.id] then
    local info={}
    for k,v in pairs(items[1152]) do info[k]=v end
    for _,k in ipairs({'name','description','introduction','sortOrder','product_desc'}) do info[k]=config[k] end
    info.script_id=0;info.use_limit=0
    items[config.id]=info
   end
   return true
  end
  originalConfig()
  if not register() then return 'pending' end
  bag.getPackageCSVConfig=function(...)
   local result=originalConfig(...);register();return result
  end
  bag.requestUseItem=function(item,...)
   if not item or item.type_id~=config.id then return originalUse(item,...) end
   if (item.count or 0)<1 then return end
   local player=ms.d_mainUI and ms.d_mainUI.g_playerInfo
   if player and (player.level or 0)>=config.max_level then
    ms.d_info.show('主角已达等级上限，等级卡未消耗');return
   end
   bag.g_lastRequestUsedItem={item=item,count=1}
   ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_use_item,{
    item_type=config.id,item_id=item.id or bag.getPropIDByTypeId(config.id),
    des_type=ms.d_common_def.object_type.role,des_id=0,item_count=1})
  end
  common.recvUsedItem=function(data,...)
   if not data or data.type_id~=config.id then return originalResult(data,...) end
   -- Event 2 owns the level rewards. The native gift callback expects an
   -- attach_list and would otherwise open a second, empty reward window.
   if data.result==1 then bag.refreshPackage() end
  end
  bag._localLevelCardRestore=function()
   bag.getPackageCSVConfig=originalConfig;bag.requestUseItem=originalUse
   common.recvUsedItem=originalResult
   if bag.g_itemAttrTable then bag.g_itemAttrTable[config.id]=nil end
   bag._localLevelCardRestore=nil
  end
 end
end
