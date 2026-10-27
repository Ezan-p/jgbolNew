local ms=assert(package.loaded.ms);local ui=assert(ms.d_moonCakeUI)
local saved,checks,sent,errors={},{},{},{}
local function preserve(t)
 local old={};for k,v in pairs(t) do old[k]=v end;saved[#saved+1]={t=t,old=old}
end
for _,t in ipairs({ui,ms.d_u,ms.d_info,ms.d_data,ms.d_time,ms.d_hz,ms.d_packageUI,ms.d_prizeUI,ms.d_smithUI,ms.d_commonLayerUI,ms.d_mainUI}) do preserve(t) end
local report=ms.MS_report_error;ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
if ui._localMoonRestore then ui._localMoonRestore() end
ui.g_self=ms.d_c.table_copy(ui.g_self);ui.g_moonCakeUI={}
local now,prize,batch=FIXTURE.now,nil,nil
ms.d_time.getTime=function() return now end
ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
ms.d_info.show=function() end
ms.d_data.createBatchUse=function(parent,range,fn) batch={range=range,fn=fn} end
ms.d_smithUI.getItemInfoByType=function(typ,tid)
 return {id=900000+tid,type_id=tid,attach_type=typ,count=60,level=1}
end
ms.d_packageUI.g_lastRequestUsedItem={}
local nativePrize=ms.d_commonLayerUI.showPrizeResLayer
ms.d_commonLayerUI.showPrizeResLayer=function(parent,list,...)
 prize=list;return nativePrize(parent,list,...)
end
-- INSTALL_PATCH
local parent=CCScene:create();parent:retain()
ms.d_mainUI.g_mainUI={main_layer=parent}
local timeImage,delays=nil,0
local create=ms.d_u.createByStyles
ms.d_u.createByStyles=function(styles,...)
 local node=create(styles,...)
 if styles.pic=='v2/moonCakeUI/time.png' then timeImage=node end
 return node
end
local delay=ms.d_u.delay
ms.d_u.delay=function(...) delays=delays+1;return delay(...) end
local function cleanup()
 if ui._localMoonRestore then ui._localMoonRestore() end
 parent:removeFromParentAndCleanup(true);parent:removeAllChildrenWithCleanup(true);parent:release()
 for i=#saved,1,-1 do local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end;for k,v in pairs(row.old) do row.t[k]=v end end
 ms.MS_report_error=report
end
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,ok=ok and #errors==0,error=(err or '')..table.concat(errors,'\n')}
end
check('native scene and query',function()
 ui.updateActivityStatus(FIXTURE.status);assert(ui.canJoin());ui.show(parent)
 assert(ui.g_moonCakeUI.main_layer and sent[#sent].mid==1333 and sent[#sent].data.flag==0)
end)
check('permanent label and no countdown recursion',function()
 local before=delays;ui.tickTime();ui.tickTime();assert(before==delays)
 local n=tolua.cast(ui.g_moonCakeUI.main_layer:getChildByTag(ui.g_self.timeTag),'CCLabelTTF')
 assert(n:getString()=='常驻开放');assert(timeImage and not timeImage:isVisible())
end)
check('expired historical dates still allow entry',function()
 now=2147483648;ui.updateActivityStatus({begin_time=1,end_time=2,local_permanent=true,local_enabled=true});assert(ui.canJoin())
end)
for index=1,4 do
 check('native crafting recipe '..index,function()
  ui.cook(index);local p=sent[#sent];assert(p.mid==1333 and p.data.flag==1 and p.data.src_type==1134+index)
 end)
end
check('disabled event blocks entry and craft',function()
 ui.updateActivityStatus({begin_time=0,end_time=0,local_permanent=true,local_enabled=false})
 local n=#sent;assert(not ui.canJoin());ui.cook(1);assert(#sent==n)
 ui.updateActivityStatus(FIXTURE.status);now=FIXTURE.now
end)
check('personal progress and craft reward',function()
 ui.onGetResult(FIXTURE.news);ui.onGetResult(FIXTURE.crafted)
 assert(ui.g_self.luck_list.mooncake_count==1);assert(ms.d_hz.gethz('mooncake1'):find('蟠桃',1,true))
end)
for tid=1130,1133 do
 check('native bag use '..tid,function()
  batch=nil;local n=#sent
  ms.d_packageUI.requestUseItem({type_id=tid,id=900000+tid,count=10,csvInfo=assert(ms.d_packageUI.g_itemAttrTable[tid])})
  if batch then batch.fn(3) end
  local p=sent[#sent];assert(#sent>n and p.mid==1051 and p.data.item_type==tid and p.data.item_count==(batch and 3 or 1))
 end)
end
check('native random opening reward list',function()
 local n=#sent;prize=nil;ms.d_commonLayerUI.recvUsedItem(FIXTURE.opened)
 assert(prize and #prize==3);assert(#sent==n)
end)
local lines={};local passed=true
for _,c in ipairs(checks) do passed=passed and c.ok;lines[#lines+1]=c.name..':'..tostring(c.ok)..':'..c.error end
if MOON_PREVIEW and passed then
 -- Rebuild after native prize checks so recipe children contain no reward overlay.
 ui.g_moonCakeUI.main_layer:removeFromParentAndCleanup(true)
 ui.g_moonCakeUI={};ui.show(parent)
 -- Hide the test reward overlays before capturing the recipe screen.
 local children=parent:getChildren()
 for i=0,children:count()-1 do
  local child=tolua.cast(children:objectAtIndex(i),'CCNode')
  if child~=ui.g_moonCakeUI.main_layer then child:setVisible(false) end
 end
 CCDirector:sharedDirector():getRunningScene():addChild(parent,9999)
 moonPreview={restore=cleanup}
else cleanup() end
return table.concat(lines,'\n')
