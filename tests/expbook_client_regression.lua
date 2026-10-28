-- Exercise the production adapter with the original table-view/picker contracts.
-- No game process, network, account inventory or on-disk save is involved.
local source=...
local checks={}
local function check(name,fn)
 local ticks=0
 debug.sethook(function()
  ticks=ticks+1
  if ticks>100 then debug.sethook();error('selector exceeded one million Lua instructions') end
 end,'',10000)
 local ok,err=xpcall(fn,debug.traceback)
 debug.sethook()
 assert(ok,name..': '..tostring(err))
 checks[#checks+1]=name
end
local function same(actual,expected,message)
 assert(actual==expected,(message or 'value')..': '..tostring(actual)..' ~= '..tostring(expected))
end
local function copy(row)
 local result={};for k,v in pairs(row) do result[k]=v end;return result
end
local function node()
 return {children={},addChild=function(self,child) self.children[#self.children+1]=child end,
  setPosition=function() end,removeChildByTag=function() end,
  setScale=function() end,setAnchorPoint=function() end,
  getContentSize=function() return {width=500,height=80} end}
end
CCDirector={sharedDirector=function() return {getVisibleSize=function() return {width=960,height=540} end,
 getWinSize=function() return {width=960,height=540} end} end}
CCSizeMake=function(w,h) return {width=w,height=h} end
CCNode={create=node}
local ui,bag={},{}
local inventory,picker,sends,notices,drawn,views={},{},{},{},{},{}
local originalCalls={}
local character={id=11,level=1,cur_exp=0,csvInfo={quality=5}}
local cap=200
local curve={};for i=1,300 do curve[i]=100 end
local ms={d_expbookUI=ui,d_packageUI=bag,
 d_mainUI={g_playerInfo={level=80},g_mainUI={main_layer=node()}},
 d_common_def={item_sub_type={roll=99,exp_pill=100}},
 d_msg_def={gscl_msg_id={msg_consume_fairy_roll=1059}},
 d_hz={gethz=function(key) return key end},
 d_info={show=function(text) notices[#notices+1]=text end},
 d_data={g_characterExpTable={[5]=curve},createBatchUse=function(parent,range,callback)
  picker={parent=parent,range=range,callback=callback}
 end},
 d_u={clearLayer=function(parent) parent.children={};return parent end,
  createByStyle=function(style) local n=node();n.style=copy(style);return n end,
  main_server_send_msg=function(mid,data) sends[#sends+1]={mid=mid,data=data} end},
 d_tableView={tableView=function(parent,rect)
  local view={rect=rect,reloads=0,updates=0}
  function view:startScroll() self.started=true end
  function view:setDataSource(ds) self.data=ds end
  function view:setDelegate(delegate) self.delegate=delegate end
  function view:updateCellAtIndex(index) self.updates=self.updates+1;self.lastUpdated=index end
  function view:reloadData() self.reloads=self.reloads+1 end
  function view:showIndexAtCenter(index) self.center=index end
  views[#views+1]=view
  return view
 end}}
ms.d_u.createByStyles=ms.d_u.createByStyle
bag.getAllProps=function() bag.g_propsTable=inventory end
bag.g_propsTable=inventory
ui.getCortegeInfo=function(id) if id==character.id then return character end end
ui.getMaxLimitLevel=function() return cap end
ui.isMorethan80=function() return ms.d_mainUI.g_playerInfo.level>=80 end
ui.getExpResult=function(raw)
 local level,current,gain=character.level,character.cur_exp,0
 local player=ms.d_mainUI.g_playerInfo.level
 local maximum=math.min(cap,#curve,player<80 and player*3 or #curve)
 while raw>0 and level<maximum do
  local rate=(player<80 and level>=math.floor(player*2.5)) and .2 or 1
  local consumed=math.min(raw,(curve[level]-current)/rate)
  current=current+consumed*rate;gain=gain+consumed*rate;raw=raw-consumed
  if current>=curve[level] then level=level+1;current=0 end
 end
 return character.level,level,gain,current
end
ui.setSelectBtn=function() originalCalls.button=(originalCalls.button or 0)+1 end
ui.onSelectedListChanged=function()
 originalCalls.changed=(originalCalls.changed or 0)+1
 originalCalls.previewExperience=ui.getTotalExp()
end
ui.createExpBookCell=function(parent,row,size) drawn[#drawn+1]=copy(row) end
ui.createExpBookDataSource=function(size)
 return {tableViewNumberOfRows=function() return #ui.g_self.expbook end,
  drawCellAtIndex=function(index)
   local n=node();ui.createExpBookCell(n,ui.g_self.expbook[index],size);return n
  end,
  heightForRowAtIndex=function() return size.height end}
end
for _,name in ipairs({'createExpbookMutilSelectLayer','getTotalExp','cancelSelect',
 'selectAllExpBook','filterSelectedList','sendEatExpbookRequest'}) do
 ui[name]=function() originalCalls[name]=(originalCalls[name] or 0)+1;return 'native '..name end
end
local originals={};for name,fn in pairs(ui) do originals[name]=fn end
package.loaded.ms=ms;package.loaded['ui.expbookUI']=ui
local bookExp={1200,2480,10000,20000,20000,32000,21600,44000,
 35200,80000,50000,120000,80000,200000,100000,368000,
 132000,512000,208000,800000,360000,1440000,640000,2560000,
 1016000,4000000,1800000,7200000,6000000,24000000,
 10800000,44000000,17064000,70400000,24401520,100672000,
 30400000,120000000,38400000,156000000}
local function item(tid,count,lock,id)
 return {id=id or tid,type_id=tid,count=count,is_lock=lock or 0,level=1,
  csvInfo={base_experience_plus=bookExp[tid-1040] or 500,sub_type=tid<2000 and 99 or 100,
   show_level=tid<2000 and math.ceil((tid-1040)/2)*5 or 1,
   name=tid%2==1 and '仙佛密卷' or '高级仙佛密卷'}}
end
local function fresh(rows,page)
 inventory=rows;bag.g_propsTable=rows
 ui.g_self={last_select_page=page or 1,selectedCortId=character.id,MAXLV=300,
  tags={exp=7},lvLimit={{lv=0,rate=1},{lv=2.5,rate=.2},{lv=3,rate=0}}}
 ui.g_expbookUI={page_layer=node(),main_layer=node(),allBtn=node(),isDeselect=false}
 picker={};sends={};notices={};drawn={};views={}
 ui.createExpbookMutilSelectLayer()
end
local function find(tid)
 for i,row in ipairs(ui.g_self.expbook) do if row.type==tid then return row,i end end
end
local function choose(tid,count)
 local row,index=find(tid);assert(row,'missing template '..tid)
 ui.g_expbookUI.expTableView.delegate.touchCellAtIndex(index)
 assert(picker.callback,'quantity picker not opened')
 picker.callback(count)
 return row,index
end
local function restoreSettings()
 ms.d_mainUI.g_playerInfo.level=80;character.level=1;character.cur_exp=0;cap=200
end
check('installation is idempotent',function()
 assert(loadstring(source))();local first=ui.createExpbookMutilSelectLayer
 assert(type(ui._localExpbookRestore)=='function')
 assert(loadstring(source))();same(ui.createExpbookMutilSelectLayer,first)
end)
check('forty templates and 400 million scrolls render forty rows',function()
 local rows={};for tid=1041,1080 do rows[#rows+1]=item(tid,10000000) end
 fresh(rows)
 same(#ui.g_self.expbook,40);same(ui.g_expbookUI.expTableView.data.tableViewNumberOfRows(),40)
 local previous=0
 for _,row in ipairs(ui.g_self.expbook) do
  same(row.count,10000000);same(row.exp,bookExp[row.type-1040]);same(row.selectedCount,0)
  assert(row.exp>=previous,'list is not sorted by experience');previous=row.exp
 end
 for i=1,40 do ui.g_expbookUI.expTableView.data.drawCellAtIndex(i) end
 same(#drawn,40)
 for _,row in ipairs(rows) do same(row.count,10000000);same(row.csvInfo.name,row.type_id%2==1 and '仙佛密卷' or '高级仙佛密卷') end
end)
check('same-template stacks merge and locked or empty stacks are excluded',function()
 local rows={item(1041,3,0,1),item(1041,7,0,2),item(1041,200,1,3),
  item(1042,100,true,4),item(1043,0,0,5),item(1045,4,0,6)}
 fresh(rows)
 same(#ui.g_self.expbook,2);same(find(1041).count,10);same(find(1045).count,4)
 same(find(1042),nil);same(find(1043),nil)
 same(rows[1].count,3);same(rows[2].count,7);same(rows[3].count,200)
end)
check('mixed quantities preserve exact experience and native wire grouping',function()
 fresh({item(1041,10),item(1042,10),item(1043,10)})
 choose(1041,2);choose(1042,3);choose(1043,1)
 same(ui.getTotalExp(),19840)
 ui.sendEatExpbookRequest();same(#sends,1);same(sends[1].mid,1059)
 local req=sends[1].data;same(req.flag,1);same(req.first_send,true);same(req.cortege_id,11);same(req.roll_count,3)
 local counts={};for _,r in ipairs(req.roll_list) do assert(not counts[r.type_id]);counts[r.type_id]=r.count end
 same(counts[1041],2);same(counts[1042],3);same(counts[1043],1)
end)
check('large manual quantity does not expand requests',function()
 fresh({item(1080,10000000)})
 local row=choose(1080,10000000)
 same(row.selectedCount,10000000);same(ui.getTotalExp(),1560000000000000)
 ui.sendEatExpbookRequest();same(#sends,1);same(sends[1].data.roll_count,1)
 same(sends[1].data.roll_list[1].count,10000000)
end)
check('invalid quantity callbacks never select or send',function()
 fresh({item(1041,10)})
 local row,index=find(1041)
 ui.g_expbookUI.expTableView.delegate.touchCellAtIndex(index)
 same(picker.range.min,1);same(picker.range.max,10)
 same(picker.range.defaultCount,1,'quantity picker must not default to all owned scrolls')
 for _,count in ipairs({0,-1,1.5,11,'2',math.huge,-math.huge,0/0}) do picker.callback(count) end
 same(row.selectedCount,0);same(ui.getTotalExp(),0);same(#sends,0)
end)
check('clicking a selected row cancels its whole quantity',function()
 fresh({item(1041,10)})
 local row,index=choose(1041,4)
 ui.g_expbookUI.expTableView.delegate.touchCellAtIndex(index)
 same(row.selectedCount,0);same(row.isChosen,false);same(ui.getTotalExp(),0)
end)
check('cancel one or all clears counts and previews',function()
 fresh({item(1041,10),item(1042,10)})
 local row,index=choose(1041,2);choose(1042,3)
 ui.cancelSelect(index,true);same(row.selectedCount,0);same(ui.getTotalExp(),7440)
 ui.cancelSelect(nil,true);same(ui.getTotalExp(),0);same(find(1042).selectedCount,0)
end)
check('all-select stops before the under-80 efficiency threshold',function()
 ms.d_mainUI.g_playerInfo.level=21
 fresh({item(1041,10000000),item(1042,10000000)})
 ui.selectAllExpBook()
 same(find(1041).selectedCount,4);same(find(1042).selectedCount,0);same(ui.getTotalExp(),4800)
 same(ui.g_expbookUI.isDeselect,true)
 ui.selectAllExpBook();same(ui.getTotalExp(),0);same(ui.g_expbookUI.isDeselect,false)
 restoreSettings()
end)
check('all-select respects existing choices and exact-fit cap',function()
 cap=25 -- 2,400 raw experience from level 1 on the test curve.
 fresh({item(1041,10000000)})
 choose(1041,1);ui.selectAllExpBook()
 same(find(1041).selectedCount,2);same(ui.getTotalExp(),2400)
 restoreSettings()
end)
check('all-select never spends an oversized scroll to cross the cap',function()
 cap=2
 fresh({item(1080,10000000)})
 ui.selectAllExpBook();same(ui.getTotalExp(),0);same(find(1080).selectedCount,0)
 restoreSettings()
end)
check('switching to a near-cap target trims counts rather than whole stacks',function()
 fresh({item(1041,10),item(1042,10)})
 choose(1041,10);choose(1042,3)
 character.level=175 -- 2,500 raw experience remains before level 200.
 ui.filterSelectedList()
 same(find(1041).selectedCount,2);same(find(1042).selectedCount,0);same(ui.getTotalExp(),2400)
 restoreSettings()
end)
check('full-level target selects nothing',function()
 character.level=200
 fresh({item(1041,10000000)})
 ui.selectAllExpBook();same(ui.getTotalExp(),0)
 restoreSettings()
end)
check('rebuilding after use reflects current stock and resets selection',function()
 local rows={item(1041,10),item(1042,8)}
 fresh(rows);choose(1041,3);choose(1042,4)
 rows[1].count=7;rows[2].count=4
 ui.createExpbookMutilSelectLayer()
 same(find(1041).count,7);same(find(1042).count,4);same(ui.getTotalExp(),0)
 choose(1041,2);ui.sendEatExpbookRequest()
 same(sends[#sends].data.roll_list[1].count,2)
end)
check('changing material pages clears the old full-experience state and preview',function()
 fresh({item(1041,10),item(2001,10)})
 choose(1041,2);same(originalCalls.previewExperience,2400)
 ui.g_self.enoughExpbook=true;ui.g_expbookUI.isDeselect=true
 ui.g_self.last_select_page=2
 local changed=originalCalls.changed
 ui.createExpbookMutilSelectLayer()
 same(ui.g_self.enoughExpbook,false);same(ui.g_expbookUI.isDeselect,false)
 assert(originalCalls.changed>changed,'preview did not refresh')
 same(originalCalls.previewExperience,0);same(#ui.g_self.expbook,1)
 choose(2001,2);same(ui.getTotalExp(),1000)
end)
check('a stale picker cannot change a rebuilt list',function()
 fresh({item(1041,10)})
 local row,index=find(1041)
 ui.g_expbookUI.expTableView.delegate.touchCellAtIndex(index)
 local oldCallback=picker.callback
 ui.createExpbookMutilSelectLayer();oldCallback(5)
 same(ui.getTotalExp(),0);same(find(1041).selectedCount,0)
end)
check('a stale picker cannot change a different target or page',function()
 fresh({item(1041,10)})
 local row,index=find(1041)
 ui.g_expbookUI.expTableView.delegate.touchCellAtIndex(index)
 local callback=picker.callback
 ui.g_self.selectedCortId=22;callback(4)
 same(row.selectedCount,0)
 ui.g_self.selectedCortId=11;ui.g_self.last_select_page=2;callback(4)
 same(row.selectedCount,0)
 ui.g_self.last_select_page=1;ui.g_expbookUI.main_layer=nil;callback(4)
 same(row.selectedCount,0);same(ui.getTotalExp(),0)
end)
check('single remaining scroll uses one without a quantity dialog',function()
 fresh({item(1041,1)})
 local row,index=find(1041)
 ui.g_expbookUI.expTableView.delegate.touchCellAtIndex(index)
 same(row.selectedCount,1);same(picker.callback,nil);same(ui.getTotalExp(),1200)
 ui.sendEatExpbookRequest();same(sends[1].data.roll_list[1].count,1)
end)
check('legacy single-scroll fixtures still group by type ID',function()
 fresh({})
 ui.g_self.expbook={{type=1041,exp=1200,isChosen=true},{type=1041,exp=1200,isChosen=true},
  {type=1043,exp=10000,isChosen=true},{type=1042,exp=2480,isChosen=true},
  {type=1080,exp=156000000,isChosen=false}}
 same(ui.getTotalExp(),14880)
 ui.sendEatExpbookRequest();same(#sends,1);same(sends[1].data.roll_count,3)
 local counts={};for _,row in ipairs(sends[1].data.roll_list) do counts[row.type_id]=row.count end
 same(counts[1041],2);same(counts[1042],1);same(counts[1043],1);same(counts[1080],nil)
end)
check('experience pills keep their own page and request flag',function()
 fresh({item(1041,10),item(2001,10000000)},2)
 same(#ui.g_self.expbook,1);same(find(1041),nil)
 choose(2001,7);same(ui.getTotalExp(),3500)
 ui.sendEatExpbookRequest();same(sends[1].data.flag,2);same(sends[1].data.roll_count,1)
 same(sends[1].data.roll_list[1].type_id,2001);same(sends[1].data.roll_list[1].count,7)
end)
check('empty inventories display no rows and send no empty use request',function()
 fresh({item(1041,0),item(1042,10,true)})
 same(#ui.g_self.expbook,0);same(ui.getTotalExp(),0)
 ui.selectAllExpBook();ui.sendEatExpbookRequest();same(#sends,0)
end)
check('restore returns all patched functions and allows reinstall',function()
 ui._localExpbookRestore();same(ui._localExpbookRestore,nil)
 for name,fn in pairs(originals) do same(ui[name],fn,'restored '..name) end
 same(ui.createExpbookMutilSelectLayer(),'native createExpbookMutilSelectLayer')
 assert(loadstring(source))();assert(type(ui._localExpbookRestore)=='function')
 fresh({item(1041,10000000)});same(#ui.g_self.expbook,1)
 ui._localExpbookRestore()
end)
return checks
