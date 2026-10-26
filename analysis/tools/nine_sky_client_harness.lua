local ms=assert(package.loaded.ms);local ui=assert(ms.d_towerUI)
local saved,checks,sent,errors,scenes,buttons={},{},{},{},{},{}
local function preserve(t)
 local old={};for k,v in pairs(t) do old[k]=v end;saved[#saved+1]={t=t,old=old}
end
for _,t in ipairs({ui,ms.d_activityUI,ms.d_u,ms.d_info,ms.d_data,ms.d_time,ms.d_loginUI,ms.d_commonLayerUI,ms.d_answerUI,ms.d_mainUI,ms.d_lineupUI}) do preserve(t) end
local report=ms.MS_report_error;ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
if ui._localNineSkyRestore then ui._localNineSkyRestore() end
ui.g_self=ms.d_c.table_copy(ui.g_self);ui.g_self.Help1=true;ui.g_towerUI={}
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(ms.d_mainUI.g_playerInfo);ms.d_mainUI.g_playerInfo.gold_coin=1000000
ms.d_lineupUI.g_usedCharacters={{character={type=5001,reborn_layer=0}}}
ms.d_time.getTime=function() return FIXTURE.now end
ms.d_u.delay=function() end
ms.d_u.runScene=function(scene) scene:retain();scenes[#scenes+1]=scene end
ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
ms.d_info.show=function(text) if text=='wrong data assertion' then errors[#errors+1]=text end end
ms.d_answerUI.g_self=ms.d_c.table_copy(ms.d_answerUI.g_self or {})
ms.d_answerUI.g_self.config={start_time=0,end_time=0}
ms.d_activityUI.returnBack=function() end
local menu=ms.d_u.createMenu
ms.d_u.createMenu=function(styles,...)
 for _,style in ipairs(styles) do if style.npic and style.call_back then buttons[style.npic]=style.call_back end end
 return menu(styles,...)
end
-- INSTALL_PATCH
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,ok=ok and #errors==0,error=(err or '')..table.concat(errors,'\n')}
end
local function response(data) ui.onGetActResult(ms.d_c.table_copy(data)) end
check('native timed entry and request',function()
 ui.updateActivityStatus(FIXTURE.status);assert(ui.canJoin())
 local found=false;for _,v in ipairs(ms.d_funUI.getFunList()) do if v.id==37 then found=true end end
 assert(found);ui.sendRequest(1);assert(sent[#sent].mid==1309 and sent[#sent].data.id==1)
end)
check('native initial screen and all 42 route rows',function()
 response(FIXTURE.entry);assert(ui.g_towerUI.main_layer)
 for old=0,6 do for new=1,6 do assert(#ui.g_self.UnionConfig[old][new].road>0) end end
 assert(ui.g_self.role_data.floor==1)
end)
check('native free single request',function()
 buttons['v2/towerUI/p_roll.png'](1)
 local req=sent[#sent];local d=loadstring('return '..req.data.data)()
 assert(req.mid==1309 and req.data.id==2 and d.count==1 and d.index==0)
end)
check('native paid ten request',function()
 buttons['v2/towerUI/p_roll.png'](10)
 local req=sent[#sent];local d=loadstring('return '..req.data.data)()
 assert(req.mid==1309 and req.data.id==2 and d.count==10 and d.index==1)
end)
check('native paid single after free exhausted',function()
 ui.g_self.role_data.free_times=0;buttons['v2/towerUI/p_roll.png'](1)
 local req=sent[#sent];local d=loadstring('return '..req.data.data)()
 assert(d.count==1 and d.index==1)
 response(FIXTURE.entry)
end)
check('native single roll animation setup and final sync',function()
 response(FIXTURE.single)
 -- Isolated layer does not tick; timed walking is verified separately.
 ui.g_self.role_data=ms.d_c.table_copy(FIXTURE.single.local_snapshot)
 ui.cancelSwallow()
 assert(ui.g_self.role_data.steps==FIXTURE.single.local_snapshot.steps)
 assert(ui.g_self.role_data.stars==FIXTURE.single.local_snapshot.stars)
end)
check('native ten roll animation setup',function()
 response(FIXTURE.after_single);response(FIXTURE.ten);ui.g_self.role_data=ms.d_c.table_copy(FIXTURE.ten.local_snapshot);ui.cancelSwallow()
 assert(ui.g_self.role_data.steps==FIXTURE.ten.local_snapshot.steps)
end)
check('native palace reopening and preview',function()
 response(FIXTURE.palace)
 assert(ui.g_self.tinaIndex>0 and #ui.g_self.shop_data[3]==2 and #ui.g_self.shop_data[4]==2)
end)
check('native palace item purchase callback',function() response(FIXTURE.palace_buy) end)
check('native palace card purchase callback',function()
 response(FIXTURE.card_buy);assert(#ui.g_self.card_list>0)
end)
check('native star shop and card picker',function()
 response(FIXTURE.rich);response(FIXTURE.big)
 ui.showComplexBuyLayer(1);assert(ui.g_towerUI.BuyInfo and #ui.g_towerUI.BuyInfo.card_list==3)
end)
check('native star card payment response',function()
 response(FIXTURE.big_buy);assert(ui.g_self.role_data.stars==FIXTURE.big_buy.stars)
end)
check('native residual star shop and purchase',function()
 response(FIXTURE.small);response(FIXTURE.small_buy)
 assert(ui.g_self.role_data.credits==FIXTURE.small_buy.credits)
end)
check('native special treasure icons',function()
 for _,v in ipairs({{object_type=1,attach_type=-1,attach_level=50,attach_count=1},{object_type=1,attach_type=-2,attach_level=1,attach_count=1}}) do
  assert(ui.getItemIcon(v));assert(ui.getItemName(v));ui.showRandomPrize({v})
 end
end)
for floor=1,9 do check('native floor '..floor,function()
 response(FIXTURE.floors[floor]);assert(ui.g_self.role_data.floor==floor)
end) end
check('native ninth sentinel never renders tenth title',function()
 ui.g_self.role_data.floor=10;ui.showFloorTitle(false)
 assert(ui.g_self.role_data.floor==9)
end)
check('native closed schedule',function()
 ui.updateActivityStatus({begin_time=0,end_time=0});assert(not ui.canJoin())
end)
if ui._localNineSkyRestore then ui._localNineSkyRestore() end
for _,scene in ipairs(scenes) do scene:removeAllChildrenWithCleanup(true);scene:release() end
for i=#saved,1,-1 do local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end;for k,v in pairs(row.old) do row.t[k]=v end end
ms.MS_report_error=report
local out={};for _,v in ipairs(checks) do out[#out+1]=v.name..':'..tostring(v.ok)..':'..v.error end
return table.concat(out,'\n')
