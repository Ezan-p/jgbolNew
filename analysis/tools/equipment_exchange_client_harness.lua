local ms=assert(package.loaded.ms);local ui=ms.d_forgeUI
local saved,checks,sent,errors={},{},{},{}
local function preserve(t)
 local old={};for k,v in pairs(t) do old[k]=v end;saved[#saved+1]={t=t,old=old}
end
local function up(fn,key)
 for i=1,40 do local k,v=debug.getupvalue(fn,i);if not k then break end;if k==key then return v end end
end
for _,t in ipairs({ui,ms.d_funUI,ms.d_u,ms.d_info,ms.d_mainUI,ms.d_packageUI,ms.d_commonLayerUI,ms.d_data,ms.d_time}) do preserve(t) end
-- Imperial-exam status may not have arrived in a newly connected live client.
-- Keep that unrelated activity closed in this isolated entry fixture.
preserve(ms.d_answerUI);ms.d_answerUI.canJoin=function() return false end
if ui._localExchangeRestore then ui._localExchangeRestore() end
if ui._localCraftingRestore then ui._localCraftingRestore() end
local state=assert(up(ui.showForgeMainLayer,'g_forgeUI'))
local config=assert(up(ui.showForgeMainLayer,'g_self'))
preserve(state);preserve(config)
for k in pairs(state) do state[k]=nil end
local parent=CCLayer:create();ms.d_mainUI.g_mainUI.main_layer:addChild(parent,1000)
ms.d_mainUI.g_mainUI={main_layer=parent}
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(ms.d_mainUI.g_playerInfo);ms.d_mainUI.g_playerInfo.level=99
ms.d_funUI.g_funUI={main_layer=CCLayer:create()}
parent:addChild(ms.d_funUI.g_funUI.main_layer)
local report=ms.MS_report_error;ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
local notices={}
ms.d_info.show=function(message) notices[#notices+1]=message end
local now=FIXTURE.now
ms.d_time.getTime=function() return now end
local menus={};local nativeMenu=ms.d_u.createMenu
ms.d_u.createMenu=function(style,...)
 for _,row in ipairs(style) do if row.call_back then menus[#menus+1]=row end end
 return nativeMenu(style,...)
end
local countLabel;local create=ms.d_u.createByStyle
ms.d_u.createByStyle=function(style,...)
 local node=create(style,...)
 if style.type=='label' and tostring(style.string):find('本周剩余兑换',1,true) then countLabel=node end
 return node
end
local prize;ms.d_commonLayerUI.showPrizeResLayer=function(p,list) prize=list end
-- Invoke both native animation completion callbacks deterministically. Native
-- widgets/CCLabels/CCMenus are real; this does not claim animation timing QA.
local nativeAnimation=ms.d_u.createAnimation_new
ms.d_u.createAnimation_new=function(file,style,times,callback,p) if callback then callback() end end
ms.d_packageUI.g_packageItemsInfo={};ms.d_packageUI.g_isPackageSorted=false
for _,p in ipairs(FIXTURE.inventory) do ms.d_packageUI.getDateFormServer(p) end
ms.d_packageUI.sortItems()
-- INSTALL_PATCH
-- A repeated injection must continue to the subsequent adapters in the bundle.
-- INSTALL_PATCH
local reinjected=true
local function restore()
 if ui._localExchangeRestore then ui._localExchangeRestore() end
 parent:removeFromParentAndCleanup(true)
 for i=#saved,1,-1 do local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end;for k,v in pairs(row.old) do row.t[k]=v end end
 ms.MS_report_error=report
end
exchangePreview={restore=restore}
exchangePreview.animate=function()
 now=FIXTURE.next_now
 ui.updateForgeList(FIXTURE.next_query);ui.ForgeTypeBtnPressed(3)
 ms.d_u.createAnimation_new=nativeAnimation
 prize=nil;errors={};ui.getForgeResult(FIXTURE.next_result)
end
exchangePreview.animationResult=function()
 return table.tostring({finished=prize~=nil,count=prize and prize[1].attach_count or 0,
   label=countLabel and countLabel:getString() or '',notice=notices[#notices],errors=errors})
end
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,ok=ok and #errors==0,error=(err or '')..table.concat(errors,'\n')}
end
local function menu(x,y)
 for i=#menus,1,-1 do local m=menus[i];if m.x==x and m.y==y then return m.call_back end end
 error('missing native menu '..x..','..y)
end
check('repeat installation continues the client bundle',function() assert(reinjected and ui._localExchangeRestore) end)
check('activity entry sends original query',function()
 ms.d_funUI.create();menu(.76,.91)();assert(sent[#sent].mid==1055 and sent[#sent].data.flag==0)
end)
check('original query opens attached forge',function()
 ui.updateForgeList(FIXTURE.query);assert(state.main_layer:getParent()==parent)
end)
check('native close button removes only forge',function()
 local old=state.main_layer;old:retain();menu(.45,.48)()
 assert(old:getParent()==nil and state.main_layer==nil);old:release()
 assert(ms.d_funUI.g_funUI.main_layer:getParent()==parent)
 ui.returnBack() -- Repeat close is harmless.
end)
check('reopen and tab switch',function()
 ui.updateForgeList(FIXTURE.query);ui.ForgeTypeBtnPressed(3)
 assert(countLabel:getString()=='本周剩余兑换: 1/1')
end)
check('four shard targets reachable',function()
 local found={};for _,v in ipairs(config.forgeList[3]) do found[v.equip_type]=true end
 menu(.23,.9)();for _,v in ipairs(config.forgeList[3]) do found[v.equip_type]=true end
 for t=6001,6004 do assert(found[t],t) end
 assert(state.lastTargetIndex==1 and #state.chosenEquips==0)
 menu(.09,.9)()
end)
check('all equipment targets reachable',function()
 ui.ForgeTypeBtnPressed(2);local found={}
 for i=1,30 do
  for _,row in ipairs(config.forgeList[2]) do found[row.equip_type]=true end
  menu(.23,.9)()
 end
 for _,row in ipairs(FIXTURE.query.equip_compose.appoint) do assert(found[row.material_type],row.material_type) end
end)
check('last page forged target is marked and cannot repeat',function()
 local index
 for i,row in ipairs(config.forgeList[2]) do if row.equip_type==FIXTURE.forged.equip_type then index=i end end
 assert(index);ui.targetChanged(index);ui.getForgeResult(FIXTURE.forged);ui.showForgeMainLayer()
 assert(config.forgeList[2][index].isForged);ui.targetChanged(index);assert(not ui.canForge(false))
 assert(prize[1].attach_count==1 and prize[1].attach_type==FIXTURE.forged.equip_type)
end)
check('materials exclude locked worn and advanced gear',function()
 local items=ui.getEquipsByQuality(4);local found={}
 for _,i in ipairs(items) do found[i.id]=true end
 for _,id in ipairs(FIXTURE.materials) do assert(found[id],id) end
 for _,id in ipairs(FIXTURE.invalid) do assert(not found[id],id) end
 assert(found[FIXTURE.enhanced])
end)
check('original high level material confirmation precedes sending',function()
 ui.updateForgeList(FIXTURE.query) -- independent fresh-week fixture
 ui.ForgeTypeBtnPressed(3);menu(.09,.9)();ui.targetChanged(1)
 local confirmation;local original=ms.d_data.createEnsureBox
 ms.d_data.createEnsureBox=function(parent,options) confirmation=options end
 state.chosenEquips=ui.getEquipsByQuality(4)
 local checked=0
 for _,item in ipairs(state.chosenEquips) do
  item.isChecked=item.id==FIXTURE.enhanced or checked<4
  if item.isChecked and item.id~=FIXTURE.enhanced then checked=checked+1 end
 end
 local before=#sent;ui.forgeBtnPressed();assert(#sent==before and confirmation and confirmation.secondBtn.callback)
 confirmation.secondBtn.callback();assert(#sent==before+1 and sent[#sent].mid==1053)
 ms.d_data.createEnsureBox=original
end)
check('native material selection and exchange request',function()
 ui.ForgeTypeBtnPressed(3);menu(.09,.9)();ui.targetChanged(1)
 state.chosenEquips=ui.getEquipsByQuality(4)
 for n,i in ipairs(state.chosenEquips) do i.isChecked=n<=5 end
 ui.forgeBtnPressed();local p=sent[#sent]
 assert(p.mid==1053 and p.data.compose_type==3 and p.data.material_count==5)
 assert(p.data.equip_type==6001 and #p.data.material_list==5)
end)
for i,result in ipairs(FIXTURE.results) do
 check('40 shards consume one quota '..i,function()
  ui.getForgeResult(result);ui.showForgeMainLayer()
  assert(countLabel:getString()=='本周剩余兑换: 0/1',countLabel:getString())
  assert(prize[1].attach_count==40)
 end)
end
check('exhaustion blocks native compose and material buttons',function()
 local n=#sent;assert(not ui.canForge(false));ui.forgeBtnPressed();ui.AddMaterialPressed();assert(#sent==n)
end)
check('result replay uses authoritative saved quota',function()
 ui.getForgeResult(FIXTURE.results[1]);ui.showForgeMainLayer()
 assert(countLabel:getString()=='本周剩余兑换: 0/1')
end)
check('late result after close is safe',function()
 ui.returnBack();ui.getForgeResult(FIXTURE.results[1]);assert(state.main_layer==nil)
end)
check('level gate blocks direct query and open',function()
 ms.d_mainUI.g_playerInfo.level=29;local n=#sent;menu(.76,.91)();ui.show();assert(#sent==n and not state.main_layer)
 ms.d_mainUI.g_playerInfo.level=30;menu(.76,.91)();assert(#sent==n+1 and sent[#sent].mid==1055)
 ms.d_mainUI.g_playerInfo.level=99
end)
check('fresh response repairs historical minus thirty',function()
 ui.updateForgeList(FIXTURE.query);ui.ForgeTypeBtnPressed(3)
 config.forgeList[3].left_times=-30
 ui.updateForgeList(FIXTURE.query);ui.ForgeTypeBtnPressed(3)
 assert(countLabel:getString()=='本周剩余兑换: 1/1')
end)
check('success notice includes exhaustion and next reset',function()
 ui.ForgeTypeBtnPressed(3);ui.getForgeResult(FIXTURE.results[1])
 local notice=notices[#notices];assert(notice:find('兑换成功',1,true) and notice:find('1/1',1,true) and notice:find('下次刷新',1,true))
end)
check('both tabs block after weekly exchange',function()
 ui.ForgeTypeBtnPressed(2);assert(countLabel:getString()=='本周剩余兑换: 0/1')
 local before=#sent;ui.forgeBtnPressed();ui.AddMaterialPressed();assert(#sent==before)
 ui.ForgeTypeBtnPressed(3);assert(not ui.canForge(false))
end)
check('week boundary refreshes from server and ignores older snapshot',function()
 now=FIXTURE.next_now
 local before=#sent;assert(not ui.canForge(false));assert(#sent==before+1 and sent[#sent].data.flag==1)
 ui.updateForgeList(FIXTURE.next_query);ui.ForgeTypeBtnPressed(3)
 assert(countLabel:getString()=='本周剩余兑换: 1/1' and ui.canForge(false))
 ui.getForgeResult(FIXTURE.results[1]);ui.showForgeMainLayer()
 assert(countLabel:getString()=='本周剩余兑换: 1/1')
end)
local result={};for _,c in ipairs(checks) do result[#result+1]=c.name..':'..tostring(c.ok)..':'..c.error end
return table.concat(result,'\n')
