-- Run the real Cocos page and callbacks against copied client data only.
local ms=assert(package.loaded.ms)
local ui=assert(ms.d_expbookUI)
if ui.g_expbookUI.main_layer then ms.d_u.remove(ui.g_expbookUI.main_layer) end
if ui._localExpbookRestore then ui._localExpbookRestore() end
assert(loadstring(ADAPTER_SOURCE))()
local bag,lineup=ms.d_packageUI,ms.d_lineupUI
local saved={items=bag.g_packageItemsInfo,props=bag.g_propsTable,reorg=bag.g_reorgItemsInfo,chars=lineup.g_characterInfo,
 state=ui.g_self,panel=ui.g_expbookUI,send=ms.d_u.main_server_send_msg,
 picker=ms.d_data.createBatchUse,report=ms.MS_report_error}
local checks,sent,errors={}, {}, {}
local picker
local function check(name,fn)
 local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,passed=ok,error=err or ''}
 if not ok then error(name..': '..tostring(err)) end
end
local function row(tid)
 for i,r in ipairs(ui.g_self.expbook) do if r.type==tid then return r,i end end
end
local function click(tid)
 local r,i=row(tid);assert(r,'missing '..tid)
 picker=nil;ui.g_expbookUI.expTableView.delegate.touchCellAtIndex(i)
 return r
end
local function choose(tid,count)
 local r=click(tid)
 if picker then picker.callback(count) else assert(count==1 and r.selectedCount==1) end
 return r
end
local metrics={}
local ok,err=xpcall(function()
 bag.g_packageItemsInfo=ms.d_c.table_copy(saved.items)
 bag.g_reorgItemsInfo=ms.d_c.table_copy(saved.reorg)
 lineup.g_characterInfo=ms.d_c.table_copy(saved.chars)
 ui.g_self=ms.d_c.table_copy(saved.state)
 ui.g_expbookUI={}
 ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
 ms.d_data.createBatchUse=function(parent,range,callback) picker={range=range,callback=callback} end
 ms.MS_report_error=function(message) errors[#errors+1]=tostring(message) end
 local character=lineup.g_characterInfo[1]
 character.level=1;character.cur_exp=0
 local total,templates=0,{}
 for _,item in ipairs(bag.g_packageItemsInfo) do
  if item.type_id>=1041 and item.type_id<=1080 and item.is_lock~=1 then
   total=total+item.count;templates[item.type_id]=true
  end
 end
 local templateCount=0;for _ in pairs(templates) do templateCount=templateCount+1 end
 check('real inventory opens without expanding individual books',function()
  local memory=collectgarbage('count');local started=os.clock()
  ui.showExpbookLayer(ms.d_mainUI.g_mainUI.main_layer,40,1)
  metrics.open_cpu_seconds=os.clock()-started
  metrics.lua_memory_delta_kb=collectgarbage('count')-memory
  metrics.inventory_books=total;metrics.template_rows=#ui.g_self.expbook
  assert(#ui.g_self.expbook==templateCount and #ui.g_self.expbook<=40)
  assert(row(1041).count>=20000000)
 end)
 check('native target selection and quantity picker contract',function()
  ui.onCortChanged(character.id)
  click(1041)
  assert(picker.range.min==1 and picker.range.max==row(1041).count and picker.range.defaultCount==1)
  picker.callback(2)
  assert(row(1041).selectedCount==2 and ui.getTotalExp()==2400)
 end)
 check('mixed templates produce exact quantities and experience',function()
  choose(1042,1);choose(1043,1)
  assert(ui.getTotalExp()==14880)
  ui.sendEatExpbookRequest()
  assert(#sent==1 and sent[1].mid==1059)
  local req=sent[1].data
  assert(req.first_send and req.flag==1 and req.cortege_id==character.id and req.roll_count==3)
  local counts={};for _,r in ipairs(req.roll_list) do counts[r.type_id]=r.count end
  assert(counts[1041]==2 and counts[1042]==1 and counts[1043]==1)
 end)
 check('native preview equals the original level and XP calculation',function()
  local _,actualLevel,actualGain,actualExp=ui.getExpResult(ui.getTotalExp())
  assert(actualLevel==EXPECTED.mixed.level and actualExp==EXPECTED.mixed.cur_exp and actualGain==14880)
 end)
 check('cancel clears quantities and all-select stays bounded',function()
  ui.cancelSelect(nil,true);assert(ui.getTotalExp()==0)
  local started=os.clock();ui.selectAllExpBook()
  metrics.all_select_cpu_seconds=os.clock()-started
  assert(#ui.g_self.expbook==templateCount and ui.getTotalExp()>0)
  local _,level=ui.getExpResult(ui.getTotalExp())
  assert(level<=ui.getMaxLimitLevel())
  ui.selectAllExpBook();assert(ui.getTotalExp()==0)
 end)
 check('native successful-use callback rebuilds remaining inventory',function()
  choose(1041,3)
  for _,item in ipairs(bag.g_propsTable) do
   if item.type_id==1041 then item.count=item.count-3;break end
  end
  character.level=EXPECTED.three.level;character.cur_exp=EXPECTED.three.cur_exp
  local previous=row(1041).count;local started=os.clock()
  ui.onGetExpResult({flag=1,experience=3600})
  metrics.result_callback_cpu_seconds=os.clock()-started
  assert(#ui.g_self.expbook==templateCount and row(1041).count==previous-3)
  assert(ui.getTotalExp()==0 and ui.g_self.selectedCortId==character.id)
  assert(ui.getCortegeInfo(character.id).level==EXPECTED.three.level)
 end)
 check('consecutive selection sends the new quantity only',function()
  choose(1041,2);ui.sendEatExpbookRequest()
  assert(#sent==2 and sent[2].data.roll_count==1 and sent[2].data.roll_list[1].count==2)
 end)
 check('repeated result-list rebuilds remain bounded',function()
  local started=os.clock()
  for i=1,20 do ui.createExpbookMutilSelectLayer();assert(#ui.g_self.expbook==templateCount) end
  metrics.twenty_rebuilds_cpu_seconds=os.clock()-started
  assert(ui.getTotalExp()==0)
 end)
 check('experience-pill tab and return preserve page state',function()
  ui.pressPage(2)
  assert(ui.g_self.last_select_page==2)
  for _,r in ipairs(ui.g_self.expbook) do assert(r.type<1041 or r.type>1080) end
  ui.pressPage(1)
  assert(ui.g_self.last_select_page==1 and #ui.g_self.expbook==templateCount and ui.getTotalExp()==0)
 end)
 check('no native Lua errors or uncaptured network sends',function()
  assert(#errors==0,table.concat(errors,'\n'));assert(#sent==2)
 end)
end,debug.traceback)
if ui.g_expbookUI.main_layer then ms.d_u.remove(ui.g_expbookUI.main_layer) end
bag.g_packageItemsInfo=saved.items;bag.g_propsTable=saved.props;bag.g_reorgItemsInfo=saved.reorg;lineup.g_characterInfo=saved.chars
ui.g_self=saved.state;ui.g_expbookUI=saved.panel
ms.d_u.main_server_send_msg=saved.send;ms.d_data.createBatchUse=saved.picker;ms.MS_report_error=saved.report
return table.tostring({passed=ok and #errors==0,checks=checks,metrics=metrics,error=err or '',
 restored=bag.g_packageItemsInfo==saved.items and lineup.g_characterInfo==saved.chars,
 network_sends_captured=true,live_account_resources_changed=false})
