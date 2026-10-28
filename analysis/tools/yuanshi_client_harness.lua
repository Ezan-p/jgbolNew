-- Real original widgets, detached root, network captured, state restored.
local ms=assert(package.loaded.ms);local ui=assert(ms.d_twoYearsCelebrateUI)
local saved,checks,sent,errors={},{},{},{}
local lastPrize
local styles={}
local function preserve(t)
 local old={};for k,v in pairs(t) do old[k]=v end;saved[#saved+1]={t=t,old=old}
end
for _,t in ipairs({ui,ms.d_activityUI,ms.d_u,ms.d_info,ms.d_data,ms.d_time,ms.d_smithUI,ms.d_mainUI,ms.d_commonLayerUI}) do preserve(t) end
local report=ms.MS_report_error;ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
if ui._localYuanshiRestore then ui._localYuanshiRestore() end
ui.g_self={newTag=12345,shopTag=12346,redPointTag=12347,timeTag=12348,detailTag=1349,x1=0.38,x2=0.62,y1=0.5}
local root=CCLayer:create();root:retain()
ms.d_time.getTime=function() return FIXTURE.now end
ms.d_u.delay=function() end
local create=ms.d_u.createByStyles
ms.d_u.createByStyles=function(style,...)
 styles[#styles+1]=style
 return create(style,...)
end
ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
ms.d_info.show=function() end
ms.d_data.g_new_config=ms.d_c.table_copy(ms.d_data.g_new_config or {})
ms.d_data.g_new_config[24]=ms.d_data.g_new_config[24] or {}
ms.d_data.g_new_config[24].yuanshi_info=FIXTURE.config
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(ms.d_mainUI.g_playerInfo or {})
ms.d_mainUI.g_playerInfo.gold_coin=100000
ms.d_smithUI.getMaterialCount=function() return 10 end
ms.d_activityUI.g_self={main_layer=root}
ms.d_activityUI.show=function(id) assert(id==46);ms.d_activityUI.g_currentActivity=46;ui.show(root) end
ms.d_commonLayerUI.showPrizeResLayer=function(parent,list,callback)
 assert(type(list)=='table');lastPrize=list;if callback then callback() end
end
-- INSTALL_PATCH
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,ok=ok and #errors==0,error=(err or '')..table.concat(errors,'\n')}
end
local function response(data) ui.onGetResult(ms.d_c.table_copy(data)) end
local function last(flag,index)
 local r=sent[#sent];assert(r and r.mid==1334 and r.data.flag==flag and r.data.index==index,'bad 1334 request')
end
check('original funUI anniversary entry',function()
 assert(ui.canJoin());local found=false
 for _,v in ipairs(ms.d_funUI.getFunList()) do if v.id==46 then found=true end end
 assert(found,'original funUI omitted anniversary')
 ms.d_activityUI.show(46);last(0,0)
end)
check('entry native rendering',function()
 response(FIXTURE.entry);assert(ui.g_self.main_layer);assert(#ui.g_self[0].gift_config==5)
 local found=false
 for _,s in ipairs(styles) do
  assert(s.pic~='v2/moonCakeUI/time.png','old expiry caption remains')
  if s.string=='距下次刷新' then found=true end
 end
 assert(found,'refresh caption missing')
end)
check('free prayer native request and reward callback',function()
 ui.pray();last(2,0);lastPrize=nil;response(FIXTURE.wish)
 assert(ui.g_self[0].cur_progress==10)
 assert(lastPrize and #lastPrize==1,'wish reward missing from native popup')
 for k,v in pairs(FIXTURE.wish.prize_list[1]) do assert(lastPrize[1][k]==v,'wish reward mismatch') end
end)
check('shop original two items',function() ui.createShop();last(3,0);response(FIXTURE.shop);assert(ui.g_self.shoplayer) end)
check('buy offering and update cached stock',function()
 ui.buy(1);last(4,1);response(FIXTURE.buy);assert(ui.g_self[3].shop_config[1].buy_times==0)
 local n=#sent;ui.buy(1);assert(#sent==n)
 ui.buy(2);last(4,2);ui.closeShop()
end)
check('portrait claim binding',function()
 response(FIXTURE.ready);assert(ui.g_self.main_layer:getChildByTag(746002));ui.getChar();last(2,0)
 response(FIXTURE.claim);assert(ui.g_self[0].claimed);assert(not ui.g_self.main_layer:getChildByTag(746002))
end)
check('continued prayer soul callback',function() ui.pray();last(2,0);response(FIXTURE.soul);assert(ui.g_self[0].claimed) end)
check('live recharge refreshes original gift state',function()
 ms.d_data.callback_update_config({local_yuanshi=ms.d_c.table_copy(FIXTURE.charged)})
 assert(ui.g_self[0].gift_list[1]==1)
end)
check('first recharge and gift claim',function()
 response(FIXTURE.charged);ui.openGiftPack(1);ui.openGiftPackEnsure(1);last(1,1)
 response(FIXTURE.gift);assert(ui.g_self[0].gift_list[1]==0)
end)
for i=1,5 do check('native gift detail '..i,function() response(FIXTURE.all_gifts);ui.showGiftDetail(i);ui.openGiftPackEnsure(i);last(1,i) end) end
check('permanent countdown zero requests refresh',function()
 ui.createShop();response(FIXTURE.shop);ui.showGiftDetail(1)
 FIXTURE.now=FIXTURE.entry.end_time
 ui.tickTime();assert(ui.canJoin());last(0,0)
 assert(styles[#styles].string=='0天00:00:00')
 local n=#sent;ui.pray();ui.getChar();ui.buy(1);ui.openGiftPackEnsure(1)
 assert(#sent==n,'stale action escaped refresh')
end)
check('new fortnight clears old dialogs and restarts countdown',function()
 local fresh=ms.d_c.table_copy(FIXTURE.entry)
 fresh.begin_time=FIXTURE.now;fresh.end_time=FIXTURE.now+14*86400;fresh.refresh_time=fresh.end_time
 response(fresh);assert(not ui.g_self.shoplayer and not ui.g_self[3] and not ui.g_self[4])
 assert(not ui.g_self.main_layer:getChildByTag(ui.g_self.detailTag))
 ui.tickTime();assert(styles[#styles].string=='14天00:00:00')
 ui.pray();last(2,0)
end)
check('closed schedule prevents entry',function() ms.d_data.g_new_config[24].yuanshi_info={begin_time=0,end_time=0};assert(not ui.canJoin()) end)
root:removeAllChildrenWithCleanup(true);root:release()
for i=#saved,1,-1 do local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end;for k,v in pairs(row.old) do row.t[k]=v end end
ms.MS_report_error=report
local out={};for _,v in ipairs(checks) do out[#out+1]=v.name..':'..tostring(v.ok)..':'..v.error end
return table.concat(out,'\n')
