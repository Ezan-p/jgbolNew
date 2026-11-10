-- Keep the native wheel and two-count picker; share server prices and limits.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_treasureMapUI
 local data=ms and ms.d_data
 local menus=ms and ms.d_tableView
 local enums=ms and ms.d_common_def
 if not ui or not ui.createBatchUse or not data or not data.getItemCountByType
     or not menus or not menus.createTableViewMenu or not enums or not enums.client_config_type
     or not debug or not debug.getupvalue then return 'pending' end
 if not ui._localTreasureRestore then
  local costs=__TREASURE_COSTS__
  local limit=__TREASURE_BATCH_LIMIT__
  local oldBatch,oldMenu=ui.createBatchUse,menus.createTableViewMenu
  local function isMap(tid) return type(tid)=='number' and tid>=1431 and tid<=1440 end
  ui.createBatchUse=function(parent,defs,...)
   if not defs or not isMap(defs.itemType) then return oldBatch(parent,defs,...) end
   if (ms.d_mainUI.g_playerInfo.level or 0)<70 then
    ms.d_info.show('九幽宝图需角色达到70级');return
   end
   local maximum=math.min(limit,data.getItemCountByType(5,defs.itemType))
   if maximum<1 then ms.d_info.show('九幽宝图不足');return end
   -- Native L546 reads this table; refresh on each opening after config reload.
   data.g_new_config=data.g_new_config or {}
   local key=enums.client_config_type.common_config
   data.g_new_config[key]=data.g_new_config[key] or {}
   local common=data.g_new_config[key]
   common.specter_info=common.specter_info or {}
   common.specter_info.open_multi_cost=costs
   local options={};for k,v in pairs(defs) do options[k]=v end
   options.min=1;options.max=maximum;options.defaultCount=1
   return oldBatch(parent,options,...)
  end
  menus.createTableViewMenu=function(config,...)
   local rows=config and config.menuItems
   local row=rows and rows[2]
   -- The native batch callback closes over itemInfo (packageUI L369-376).
   -- Replace only that map button, removing its hardcoded >=10 / <=15 gates.
   if row and row.nSprite and row.sSprite and type(row.tapHandler)=='function' then
    for i=1,20 do
     local name,item=debug.getupvalue(row.tapHandler,i)
     if not name then break end
     if name=='itemInfo' and type(item)=='table' and isMap(item.type_id) then
      local tid=item.type_id
      row.nSprite=nil;row.sSprite=nil
      row.npic='v2/packageUI/piliangshiyong1.png';row.spic='v2/packageUI/piliangshiyong2.png'
      row.tapHandler=function()
       ui.createBatchUse(ms.d_mainUI.g_mainUI.main_layer,{itemType=tid,min=1})
      end
      break
     end
    end
   end
   return oldMenu(config,...)
  end
  ui._localTreasureRestore=function()
   ui.createBatchUse=oldBatch;menus.createTableViewMenu=oldMenu;ui._localTreasureRestore=nil
  end
 end
end
