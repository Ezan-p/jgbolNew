local fixtures=__FIXTURES__
local ms=assert(package.loaded.ms)
local ui=assert(ms.d_escortUI)
local inventory=assert(ms.d_packageUI)
local root=CCLayer:create()
CCDirector:sharedDirector():getRunningScene():addChild(root,10000)
local saved={}
local function replace(t,k,v)
 saved[#saved+1]={t=t,k=k,v=rawget(t,k)};rawset(t,k,v)
end
local sent,touch,errors={},nil,{}
local report={passed=false,checks={}}
escortRewardsRestore=function()
 root:stopAllActions();root:removeFromParentAndCleanup(true)
 for i=#saved,1,-1 do local s=saved[i];rawset(s.t,s.k,s.v) end
 escortRewardsRestore=nil
end
local function check(name,fn)
 errors={}
 local ok,err=xpcall(fn,debug.traceback)
 if #errors>0 then ok=false;err=table.concat(errors,'\n') end
 report.checks[#report.checks+1]={name=name,ok=ok,error=not ok and tostring(err) or nil}
 assert(ok,name..': '..tostring(err))
end
local ok,err=xpcall(function()
 replace(ms,'MS_report_error',function(e) errors[#errors+1]=tostring(e) end)
 replace(ms.d_u,'main_server_send_msg',function(mid,data) sent[#sent+1]={mid=mid,data=data} end)
 replace(ui,'g_escortUI',{main_layer=root})
 replace(ui,'g_self',ms.d_c.table_copy(ui.g_self))
 replace(ui,'g_currentLayer',ui.g_currentLayer)
 replace(ui,'getPieceCountBySubtype',function() return 30 end)
 replace(ms.d_commonLayerUI,'ItemFall_add',function() end)
 replace(ms.d_commonLayerUI,'ItemFall_run',function() end)
 replace(inventory,'g_reorgItemsInfo',{[5]={}})
 replace(inventory,'g_lastRequestUsedItem',{})
 replace(ms.d_data,'createBatchUse',function(parent,opts,callback)
  assert(opts.min==1 and opts.max==15);callback(15)
 end)
 local register=CCLayer.registerScriptTouchHandler
 replace(CCLayer,'registerScriptTouchHandler',function(layer,fn,...)
  if debug.getinfo(fn,'S').linedefined==500 then touch=fn;return end
  return register(layer,fn,...)
 end)
 check('native_main_and_single_ten_buttons',function()
  ui.initConst(fixtures.const)
  ui.showCommonFrame()
  ui.showMainFrame()
  for _,count in ipairs({1,10}) do
   sent={};ui.pressCompose(count)
   assert(#sent==1 and sent[1].mid==1301 and sent[1].data.id==69)
   local req=assert(loadstring('return '..sent[1].data.data))()
   assert(req.flag==2 and req.ten_pick==count)
  end
 end)
 for _,f in ipairs(fixtures.singles) do
  check('single_bag_'..f.bag.type_id..'_native_lookup_and_use',function()
   local bag=ms.d_c.table_copy(f.bag)
   bag.csvInfo=ms.d_data.getCertainInfo(5,bag.type_id)
   assert(bag.csvInfo and bag.csvInfo.name)
   inventory.g_reorgItemsInfo[5][bag.csvInfo.mainType]={bag}
   sent={};touch=nil
   ui.onGetResponse(f.response)
   assert(touch,'single result must register click-to-open')
   touch()
   assert(#sent==1 and sent[1].mid==1051)
   local req=sent[1].data
   assert(req.item_type==bag.type_id and req.item_id==bag.id and req.item_count==1 and req.des_type==1)
   -- Native inventory uses the same bag metadata and supports a quantity picker.
   bag.count=16;sent={};inventory.requestUseItem(bag)
   assert(#sent==1 and sent[1].mid==1051 and sent[1].data.item_count==15)
  end)
 end
 check('ten_final_reward_rows_render_without_extra_use_requests',function()
  sent={};ui.onGetResponse(fixtures.ten)
  local state=ui.g_self
  assert(state.tenResLayer and state.tenResView and #state.tenResData==10)
  -- Advance native reveal callbacks synchronously, cancelling their timers.
  for i=1,10 do ui.showTenComposeCell(state.tenResLayer,state.tenResData,i) end
  assert(#state.tenShowData==10)
  for i,row in ipairs(state.tenShowData) do
   assert(#row==1 and row[1].attach_type==fixtures.ten.item_list[i][1].attach_type)
  end
  assert(#sent==0,'ten rewards are settled by the compose request')
 end)
 report.passed=true
end,debug.traceback)
if not ok then report.error=tostring(err) end
escortRewardsRestore()
return table.tostring(report)
