-- Bridge the old roster packet to the current native fate windows. Snapshots
-- are authoritative; default fields prevent nil arithmetic on older saves.
do
 local ms=package.loaded.ms
 local lineup=ms and ms.d_lineupUI
 local data=ms and ms.d_data
 if not lineup or not data then return 'pending' end
 if not ms._localFateRestore then
  local defaults=__FATE_DEFAULTS__
  local items=__FATE_ITEMS__
  local state={}
  local restores={}
  local function wrap(t,name,make)
   if not t or type(t[name])~='function' then return end
   local old=t[name];t[name]=make(old)
   restores[#restores+1]=function() t[name]=old end
  end
  local function apply(c)
   if not c then return end
   local values=state[c.id] or state[tostring(c.id)] or {}
   for k,v in pairs(defaults) do
    if values[k]~=nil then c[k]=values[k]
    else c[k]=v end
   end
  end
  local function refresh()
   for _,c in pairs(lineup.g_characterInfo or {}) do apply(c) end
   if ms.d_fateRebuildUI then apply(ms.d_fateRebuildUI.g_fateRebuildData) end
  end
  wrap(data,'callback_update_config',function(old)
   return function(config)
    if config and config.local_fate_rebuild then
     if not config.local_fate_append then state={} end
     for cid,values in pairs(config.local_fate_rebuild) do state[cid]=values end
    end
    refresh()
    local result=old(config)
    refresh()
    return result
   end
  end)
  wrap(lineup,'getDateFormServer',function(old)
   return function(packet)
    for _,c in ipairs(packet.cortege_list or {}) do apply(c) end
    local result=old(packet);refresh();return result
   end
  end)
  for _,ui in ipairs({ms.d_ascensionUI,ms.d_fateRebuildUI}) do
   wrap(ui,'getAscCorts',function(old)
    return function(...) refresh();return old(...) end
   end)
  end
  wrap(data,'getCertainInfo',function(old)
   return function(kind,tid,...)
    local info=old(kind,tid,...)
    if kind==5 and items[tid] then
     local copy={};for k,v in pairs(info or {}) do copy[k]=v end;info=copy
     for k,v in pairs(items[tid]) do info[k]=v end
    end
    return info
   end
  end)
  wrap(ms.d_packageUI,'requestUseItem',function(old)
   return function(item,...)
    if not item or item.type_id~=1370 then return old(item,...) end
    local maximum=math.min(99,item.count or 0)
    if maximum<1 then return end
    local function use(count)
     if type(count)~='number' or count~=math.floor(count) or count<1 or count>maximum then return end
     local bag=ms.d_packageUI
     bag.g_lastRequestUsedItem={item=item,count=count}
     ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_use_item,
      {item_type=1370,item_id=item.id,des_type=ms.d_common_def.object_type.role,des_id=0,item_count=count})
    end
    if maximum==1 then use(1)
    else data.createBatchUse(ms.d_mainUI.g_mainUI.main_layer,{min=1,max=maximum},use) end
   end
  end)
  refresh()
  ms._localFateRestore=function()
   for i=#restores,1,-1 do restores[i]() end
   ms._localFateRestore=nil
  end
 end
end
