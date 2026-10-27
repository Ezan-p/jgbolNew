-- Original activity-30 UI, isolated module state and intercepted network sends.
local m=assert(package.loaded.ms)
local ui=assert(m.d_chargePresentUI)
local saved,ups,checks,sent,errors,seen={},{},{},{},{},{}
local private={springInfo=true,presentsInfo=true,timeTable=true,isOpen=true,dataTable=true}
local recurse={genPresentInfo=true,showPresent=true,createDataSource=true,createCell=true,requestGetPresent=true}
local function preserve(t)
 local old={};for k,v in pairs(t) do old[k]=v end;saved[#saved+1]={t=t,old=old}
end
for _,t in ipairs({ui,m.d_activityUI,m.d_u,m.d_time,m.d_commonLayerUI,m.d_alert}) do preserve(t) end
local function scan(fn)
 if seen[fn] then return end;seen[fn]=true
 for i=1,100 do
  local name,value=debug.getupvalue(fn,i);if not name then break end
  if private[name] then ups[#ups+1]={fn=fn,index=i,name=name,value=value} end
  if recurse[name] and type(value)=='function' then scan(value) end
 end
end
for _,fn in pairs(ui) do if type(fn)=='function' then scan(fn) end end
local function up(fn,key)
 for i=1,100 do local name,value=debug.getupvalue(fn,i);if not name then break end;if name==key then return value end end
end
local report=m.MS_report_error
m.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
local layer=CCLayer:create();layer:retain()
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]=name..':'..tostring(ok and #errors==0)..':'..(err or '')..table.concat(errors,' ')
end
local function claimButton(node,index)
 local kind=tolua.type(node) or ''
 if string.find(kind,'CCMenuItemImage',1,true) and node:getTag()==index then return tolua.cast(node,'CCMenuItem') end
 local children=node:getChildren()
 if children then for i=0,children:count()-1 do
  local hit=claimButton(tolua.cast(children:objectAtIndex(i),'CCNode'),index)
  if hit then return hit end
 end end
end
local ok,err=xpcall(function()
 for _,row in ipairs(ups) do
  local replacement=row.name=='dataTable' and {} or type(row.value)=='table' and m.d_c.table_copy(row.value) or row.value
  debug.setupvalue(row.fn,row.index,replacement)
 end
 m.d_activityUI.g_self=m.d_c.table_copy(m.d_activityUI.g_self)
 m.d_activityUI.g_self.main_layer=layer;m.d_activityUI.g_isCurrentSenceRun=true
 m.d_time.getTime=function() return FIXTURE.now end
 m.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
 m.d_u.delay=function() end;m.d_alert.stop_wait=function() end
 local prizeCalls=0
 m.d_commonLayerUI.showPrizeResLayer=function(parent,prizes,callback)
  assert(parent and #prizes>0);prizeCalls=prizeCalls+1;if callback then callback() end
 end
 check('activity30_query_1216',function()
  m.d_activityUI.requestChargeInfo()
  local req=sent[#sent];assert(req.mid==1216 and req.data.flag==1)
 end)
 check('native_status_and_event93_build_original_reward_table',function()
  ui.updateActivityStatus({spring_info=m.d_c.table_copy(FIXTURE.info)})
  assert(ui.isActivityOpen() and ui.getPresentCount()==FIXTURE.ready)
  m.d_event_mgr.msg_common_event_2998(nil,FIXTURE.query,nil)
  local data=assert(up(ui.show,'dataTable'))
  assert(data.main_layer and data.presentTableView)
  assert(data.main_layer:getChildrenCount()>0)
 end)
 check('original_claim_button_emits_1215',function()
  local data=assert(up(ui.show,'dataTable'))
  local button=assert(claimButton(data.main_layer,1),'claim button missing')
  button:activate()
  local req=sent[#sent];assert(req.mid==1215 and tonumber(req.data.prize_id)==1)
 end)
 check('event92_refreshes_claimed_row_and_reward_payload',function()
  m.d_event_mgr.msg_common_event_2998(nil,FIXTURE.claim,nil)
  assert(ui.getPresentCount()==FIXTURE.ready-1 and prizeCalls==1)
  local info=assert(up(ui.getPresentCount,'presentsInfo'));assert(info[1].status==3)
 end)
 check('claimed_row_has_no_claim_button',function()
  local data=assert(up(ui.show,'dataTable'))
  assert(not claimButton(data.main_layer,1))
 end)
 check('expired_activity_closes_native_eligibility',function()
  local expired=m.d_c.table_copy(FIXTURE.info);expired.end_time=FIXTURE.now-1
  for _,row in ipairs(expired) do row.status=1 end
  ui.updateActivityStatus({spring_info=expired})
  assert(not ui.isActivityOpen() and ui.getPresentCount()==0)
 end)
end,debug.traceback)
layer:removeAllChildrenWithCleanup(true);layer:release()
for _,row in ipairs(ups) do debug.setupvalue(row.fn,row.index,row.value) end
for i=#saved,1,-1 do
 local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end
 for k,v in pairs(row.old) do row.t[k]=v end
end
m.MS_report_error=report
if not ok then return 'fixture:false:'..tostring(err) end
return table.concat(checks,'\n')
