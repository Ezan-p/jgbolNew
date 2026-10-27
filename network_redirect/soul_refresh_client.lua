-- Native allLineupUI caches the soul array and the row count in its data source.
-- A 1046 snapshot replaces that array, so updating a cell alone reads old counts.
do
 local ms=package.loaded.ms
 local data=ms and ms.d_data
 local ui=ms and ms.d_allLineupUI
 local events=ms and ms.d_event_mgr
 if not (data and data.recvSoulsDataFromServer and ui and ui.showAllSoul
   and events and events.msg_update_spirit_list_1046) then return 'pending' end
 if not data._localSoulRefreshRestore then
  local undo={}
  local function replace(t,key,fn)
   local old=t[key];t[key]=fn
   undo[#undo+1]=function() t[key]=old end
  end
  local function up(fn,key)
   for i=1,100 do
    local name,value=debug.getupvalue(fn,i)
    if not name then break end
    if name==key then return value end
   end
  end
  local show=ui.showAllSoul
  local source=assert(up(show,'getCellsDataSource'),'soul data source is unavailable')
  local sortSoul=assert(up(show,'sortSoul'),'soul sort is unavailable')
  local depth=0
  local function refresh()
   if depth>0 then return end
   local lineup,main=ms.d_lineupUI,ms.d_mainUI
   if not (lineup and main and main.boardID
     and main.g_currentBoard==main.boardID.lineup and lineup.g_lastSelectedButton==2) then return end
   local souls=data.g_soulsInfoTable or {}
   if not souls.isSorted then table.sort(souls,sortSoul);souls.isSorted=true end
   -- Resolve this upvalue each time: the native exit handler replaces dataTable.
   local state=up(show,'dataTable')
   if not state or not state.currentTableView then
    local parent=lineup.g_lineupUI and lineup.g_lineupUI.detail_layer
    if parent and #souls>0 then show(parent) end
    return
   end
   state.infoTable=souls
   if state.currentFilter then
    ui.ensureFilter(state.currentFilter)
   else
    -- Rebuild the data source even when only one count changed: it captures
    -- the array length, and consumed/new souls change the number of rows.
    -- Native reloadData preserves and clamps the scroll position.
    state.currentTableView:reloadData(source(souls))
   end
  end
  for _,key in ipairs({'recvSoulsDataFromServer','updateSoulsData',
    'updateAllSoulsStatus','updateSoulInfo','refreshSoulNeed'}) do
   local native=data[key]
   if native then
    replace(data,key,function(...)
     depth=depth+1
     local ok,result=pcall(native,...)
     depth=depth-1
     if not ok then error(result,0) end
     if data.g_soulsInfoTable then data.g_soulsInfoTable.isSorted=false end
     local more=key=='recvSoulsDataFromServer' and events.getNextPackageType
       and events.getNextPackageType()==1046
     if not more then refresh() end
     return result
    end)
   end
  end
  -- The native updater also tries reloadData(currentShowTable) for a new type;
  -- that argument is an array, not a tableView data source.
  replace(ui,'updateSoulCellByType',refresh)
  local receive=events.msg_update_spirit_list_1046
  local function receiveSouls(event,packet,...)
   -- Original event_mgr ignores spirit_count=0, leaving the final spent soul.
   if packet and packet.first_send and packet.spirit_count==0 then
    if ms.d_alert then ms.d_alert.stop_wait() end
    return data.recvSoulsDataFromServer(packet)
   end
   return receive(event,packet,...)
  end
  replace(events,'msg_update_spirit_list_1046',receiveSouls)
  -- Registration stores the function itself, not its exported name.
  if events.g_msg_fun then replace(events.g_msg_fun,1046,receiveSouls) end
  data._localSoulRefreshRestore=function()
   for i=#undo,1,-1 do undo[i]() end
   data._localSoulRefreshRestore=nil
  end
 end
end
