local ms=assert(package.loaded.ms)
local saved,checks,sent,errors={},{},{},{}
local function preserve(t)
 local old={};for k,v in pairs(t) do old[k]=v end
 saved[#saved+1]={t=t,old=old}
end
for _,t in ipairs({ms.d_packageUI,ms.d_mainUI,ms.d_data,ms.d_u,ms.d_info,ms.d_saodangUI}) do preserve(t) end
local oldReport=ms.MS_report_error
local batch,tip,reloads
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,passed=ok and #errors==0,error=(err or '')..table.concat(errors,'\n')}
end
local ok,err=xpcall(function()
 ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
 ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(ms.d_mainUI.g_playerInfo)
 ms.d_packageUI.g_lastRequestUsedItem={}
 ms.d_mainUI.g_playerInfo.union_id=1
 ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
 ms.d_data.createBatchUse=function(parent,range,fn) batch={range=range,fn=fn} end
 ms.d_info.show=function(text) tip=text end
 ms.d_saodangUI.reloadData=function() reloads=reloads+1 end
 local function use(tid,count)
  batch=nil;tip=nil
  ms.d_packageUI.requestUseItem({type_id=tid,id=900000+tid,count=count,csvInfo=assert(ms.d_packageUI.g_itemAttrTable[tid])})
 end
 local function request(tid,count)
  local p=assert(sent[#sent]);assert(p.mid==1051)
  assert(p.data.item_type==tid and p.data.item_id==900000+tid and p.data.item_count==count)
  assert(p.data.des_type==1 and p.data.des_id==0)
 end
 check('small bun native single request',function() use(1020,20);assert(not batch);request(1020,1) end)
 check('token native single request',function() use(1029,9);assert(not batch);request(1029,1) end)
 check('token native batch threshold and inventory cap',function()
  local n=#sent;use(1029,10);assert(#sent==n and batch.range.min==1 and batch.range.max==10)
  batch.fn(10);request(1029,10)
 end)
 check('token native batch maximum 15',function()
  use(1029,20);assert(batch.range.max==15);batch.fn(15);request(1029,15)
 end)
 check('token without guild blocked before send',function()
  ms.d_mainUI.g_playerInfo.union_id=0;local n=#sent;use(1029,20)
  assert(#sent==n and not batch and tip);ms.d_mainUI.g_playerInfo.union_id=1
 end)
 check('empty item blocked before send',function()
  local n=#sent;use(1020,0);assert(#sent==n and tip)
 end)
 for _,row in ipairs(FIXTURE) do
  check('native result '..row.tid..' x'..row.count,function()
   tip=nil;reloads=0
   ms.d_commonLayerUI.recvUsedItem(row.result)
   assert(tip and string.find(tip,tostring(row.result.effect_value),1,true),tostring(tip))
   if row.tid==1020 or row.tid==1022 then assert(reloads==1) end
  end)
 end
 check('callback is display only and does not send or credit twice',function()
  local n=#sent;local before=ms.d_c.table_copy(ms.d_mainUI.g_playerInfo)
  ms.d_commonLayerUI.recvUsedItem(FIXTURE[1].result)
  assert(#sent==n and before.strength==ms.d_mainUI.g_playerInfo.strength)
 end)
end,debug.traceback)
for i=#saved,1,-1 do
 local row=saved[i];for k in pairs(row.t) do if row.old[k]==nil then row.t[k]=nil end end
 for k,v in pairs(row.old) do row.t[k]=v end
end
ms.MS_report_error=oldReport
local restored=true
for _,row in ipairs(saved) do for k,v in pairs(row.old) do if row.t[k]~=v then restored=false end end end
return table.tostring({checks=checks,restored=restored,error=not ok and tostring(err) or nil})
