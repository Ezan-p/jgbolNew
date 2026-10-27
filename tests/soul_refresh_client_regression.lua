-- Native-style cached arrays and captured row counts, without a Cocos scene.
local data={g_soulsInfoTable={},g_soulsTypeTable={}}
local ui,events={}, {g_msg_fun={}}
local nextPacket,redraws,stops=0,0,0
local dataTable={}
local owned={[11]=true}
local need={[11]=20}
local function soul(t,n)
 local row={type=t,type_id=t,count=n}
 if owned[t] then row.feiShengCount=(need[t] or 20)-n else row.huanHunCount=30-n end
 return row
end
local function getCellsDataSource(rows)
 dataTable.currentShowTable=rows
 local count=#rows
 return {tableViewNumberOfRows=function() return count+1 end,
  drawCellAtIndex=function(i) return rows[i-1] end}
end
local function sortSoul(a,b) return a.type<b.type end
local view={scrollY=125,reloadData=function(self,source)
 assert(type(source.tableViewNumberOfRows)=='function','raw rows passed as data source')
 self.source=source;redraws=redraws+1
end}
ui.showAllSoul=function(parent)
 local rows=data.g_soulsInfoTable
 if #rows==0 then return end
 table.sort(rows,sortSoul)
 dataTable={infoTable=rows,currentTableView=view}
 view:reloadData(getCellsDataSource(rows))
end
ui.ensureFilter=function(filter)
 dataTable.currentFilter=filter
 local rows={}
 for _,v in ipairs(dataTable.infoTable) do if filter(v) then rows[#rows+1]=v end end
 view:reloadData(getCellsDataSource(rows))
end
ui.updateSoulCellByType=function() view:reloadData(getCellsDataSource(dataTable.currentShowTable)) end
data.recvSoulsDataFromServer=function(packet)
 if packet.first_send then data.g_soulsInfoTable={};data.g_soulsTypeTable={} end
 for _,v in ipairs(packet.spirit_list) do
  if v.count>0 then
   table.insert(data.g_soulsInfoTable,soul(v.type_id,v.count));data.g_soulsTypeTable[v.type_id]=v.count
  end
 end
 data.g_soulsInfoTable.isSorted=false
end
data.updateAllSoulsStatus=function()
 for i,v in ipairs(data.g_soulsInfoTable) do data.g_soulsInfoTable[i]=soul(v.type,v.count) end
end
data.updateSoulInfo=function(t)
 for i,v in ipairs(data.g_soulsInfoTable) do if v.type==t then data.g_soulsInfoTable[i]=soul(t,v.count) end end
end
data.refreshSoulNeed=data.updateSoulInfo
data.updateSoulsData=function(packet)
 local found=false
 for i=#data.g_soulsInfoTable,1,-1 do
  if data.g_soulsInfoTable[i].type==packet.type_id then
   table.remove(data.g_soulsInfoTable,i);found=true
  end
 end
 if packet.total_count>0 then table.insert(data.g_soulsInfoTable,soul(packet.type_id,packet.total_count)) end
 data.g_soulsTypeTable[packet.type_id]=packet.total_count>0 and packet.total_count or nil
 ui.updateSoulCellByType(packet.type_id)
end
events.getNextPackageType=function() return nextPacket end
events.msg_update_spirit_list_1046=function(_,packet)
 if packet.spirit_count>0 then data.recvSoulsDataFromServer(packet) end
end
events.g_msg_fun[1046]=events.msg_update_spirit_list_1046
local main={boardID={lineup=4},g_currentBoard=4}
local lineup={g_lastSelectedButton=2,g_lineupUI={detail_layer={}}}
package.loaded.ms={d_data=data,d_allLineupUI=ui,d_event_mgr=events,
 d_mainUI=main,d_lineupUI=lineup,d_alert={stop_wait=function() stops=stops+1 end}}
local originalReceive=events.g_msg_fun[1046]
local originalSnapshot=data.recvSoulsDataFromServer
-- INSTALL_PATCH
local function receive(first,rows)
 events.g_msg_fun[1046](nil,{first_send=first,spirit_count=#rows,spirit_list=rows})
end
local function row(t)
 for i=2,view.source.tableViewNumberOfRows() do
  local v=view.source.drawCellAtIndex(i);if v and v.type==t then return v end
 end
end
receive(true,{{type_id=11,count=50},{type_id=12,count=7}})
assert(row(11).count==50,'an initially empty open soul tab did not populate')
local initial=dataTable.infoTable
need[11]=30
receive(true,{{type_id=11,count=30},{type_id=12,count=7}})
assert(dataTable.infoTable~=initial and row(11).count==30 and row(11).feiShengCount==0,
 'ascension left cached counts or next-stage requirements')
assert(view.scrollY==125,'refresh reset scroll position')
need[11]=40;data.updateAllSoulsStatus()
assert(row(11).feiShengCount==10,'companion growth did not update soul requirement')
local filter=function(v) return v.type==11 end
ui.ensureFilter(filter)
receive(true,{{type_id=11,count=25},{type_id=12,count=8}})
assert(dataTable.currentFilter==filter and row(11).count==25 and not row(12),'filter lost or stale')
data.updateSoulsData({type_id=11,total_count=0})
assert(view.source.tableViewNumberOfRows()==1 and not row(11),'spent filtered soul retained')
dataTable.currentFilter=nil
data.updateSoulsData({type_id=13,total_count=9})
assert(row(13).count==9 and view.source.tableViewNumberOfRows()==3,'new soul row not added')
local before=redraws
nextPacket=1046;receive(true,{{type_id=11,count=20}})
assert(redraws==before,'intermediate chunk redrew partial list')
nextPacket=0;receive(false,{{type_id=12,count=6}})
assert(row(11).count==20 and row(12).count==6 and not row(13),'chunked snapshot retained stale rows')
owned[12]=true;need[12]=50;data.updateSoulInfo(12)
assert(row(12).feiShengCount==44 and row(12).huanHunCount==nil,'soul compose status remained stale')
need[12]=15;data.refreshSoulNeed(12)
assert(row(12).feiShengCount==9,'recycle need was stale')
receive(true,{})
assert(#data.g_soulsInfoTable==0 and view.source.tableViewNumberOfRows()==1 and stops==1,
 'empty 1046 snapshot was dropped by registered handler')
before=redraws;lineup.g_lastSelectedButton=1
receive(true,{{type_id=11,count=10}})
assert(redraws==before,'hidden soul tab was redrawn')
lineup.g_lastSelectedButton=2;dataTable={};main.g_currentBoard=0
receive(true,{{type_id=11,count=11}})
assert(redraws==before,'released scene was accessed')
data._localSoulRefreshRestore()
assert(events.g_msg_fun[1046]==originalReceive and events.msg_update_spirit_list_1046==originalReceive
 and data.recvSoulsDataFromServer==originalSnapshot,'restore leaked a wrapped handler')
return {'empty open soul tab gains rows','ascension refreshes counts and requirements',
 'scroll and filter retained','companion updates refresh eligibility','spent souls removed',
 'new soul rows added','chunked snapshots rebuild once','compose and recycle state refreshed',
 'empty snapshot handled through registered event','hidden and released scene guarded','original handlers restored'}
