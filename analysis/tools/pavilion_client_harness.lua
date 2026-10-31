-- Execute native, unmodified destinyUI widgets on a detached Cocos layer.
local ms=assert(package.loaded.ms);local ui=assert(ms.d_destinyUI)
local saved={};local checks={};local errors={};local sent={}
local function preserve(t)
 local old={};for k,v in pairs(t) do old[k]=v end;saved[#saved+1]={t=t,old=old}
end
for _,name in ipairs({'d_destinyUI','d_activityUI','d_u','d_info','d_commonLayerUI','d_smithUI','d_data','d_rechargeUI','d_csv'}) do preserve(ms[name]) end
if ui._localPavilionRestore then ui._localPavilionRestore() end
ms.d_data.callback_update_config=function() end
-- INSTALL_PATCH
local report=ms.MS_report_error;ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
local root=CCLayer:create();root:retain()
ui.g_self={};ui.g_csv={};ui.g_data={};ui.g_destinyUI={};ui.parent=root
ms.d_activityUI.g_self={main_layer=root};ms.d_activityUI.show=function() end
ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
ms.d_info.show=function() end
-- Rewards are asserted and completed synchronously; no animation waits or sends.
ms.d_commonLayerUI.showPrizeResLayer=function(parent,list,callback)
 assert(type(list)=='table' and #list>0,'missing reward array');if callback then callback() end
end
ms.d_smithUI.getItemInfoByType=function(kind,tid)
 return {count=3000,type_id=tid,csvInfo=ms.d_data.getCertainInfo(kind,tid)}
end
local balance=3000
ms.d_smithUI.getItemInfoByType=function(kind,tid) return {count=balance,type_id=tid,csvInfo=ms.d_data.getCertainInfo(kind,tid)} end
local nativeMenu=ms.d_u.createMenu;local buyButtons
ms.d_u.createMenu=function(items,...)
 if items[3] and items[3].npic=='v2/towerUI/b_btn11.png' then buyButtons=items end
 return nativeMenu(items,...)
end
local raw=ui.getRawCardList
ui.getRawCardList=function() return {{type_id=1143,cur=0,max=10,value=10},{type_id=1142,cur=0,max=10,value=5}} end
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,ok=ok and #errors==0,error=(err or '')..table.concat(errors,'\n')}
end
check('activity status and enter request',function()
 ui.updateActivityStatus(FIXTURE.status);assert(ui.canJoin());ui.enter();assert(sent[#sent].mid==1227 and sent[#sent].data.flag==1)
end)
check('entry response',function() ui.onGetResult(FIXTURE.entry);assert(ui.g_csv.shop[9]) end)
for page=1,4 do check('shop page '..page,function() ui.g_self.cur_page=page;ui.showPageDeatail(page) end) end
for index=1,10 do check('purchase dialog '..index,function()
 ui.showBuyItem(root,index);ui.showDynamicBuyLayer();assert(ui.g_destinyUI.buyInfo.singlePrice==ui.g_csv.shop[index].goldon_count);ui.closeBuyItemLayer()
end) end
check('native coupon batch purchase request',function()
 ui.showBuyItem(root,4);local info=ui.g_destinyUI.buyInfo;info.count=3
 info.card_list[1].cur=2;info.card_list[2].cur=1;ui.showDynamicBuyLayer()
 assert(info.real_price==65,'price='..tostring(info.real_price));assert(buyButtons,'buy menu not captured');buyButtons[3].call_back()
 local req=sent[#sent];assert(req.mid==1227 and req.data.flag==2 and req.data.count==3 and req.data.index==4 and req.data.ten_card==2 and req.data.five_card==1)
 ui.closeBuyItemLayer()
end)
check('exchange reward and limit callback',function()
 ui.showBuyItem(root,4);local old=ui.g_csv.shop[4].left_buy_count
 balance=2940;ui.onGetResult(FIXTURE.exchange);assert(ui.g_csv.shop[4].left_buy_count==old-2);assert(ui.g_self.money_info.count==2940)
end)
check('recharge overview and bonus table',function() ui.showRecharge();ui.showRechargePage(ui.g_destinyUI.recharge_layer,1) end)
check('public gifts and claim callback',function()
 ui.showRechargePage(ui.g_destinyUI.recharge_layer,2);ui.onGetResult(FIXTURE.gift);assert(ui.g_csv.gift[2][1].state==3)
end)
check('live recharge and mail snapshot refresh',function()
 balance=0;ms.d_data.callback_update_config({local_pavilion={data=FIXTURE.entry,status=FIXTURE.status}})
 assert(ui.g_self.money_info.count==0);assert(ui.g_csv.shop[4].left_buy_count==15)
end)
for index,data in ipairs(FIXTURE.ascension) do
 check('ascension exhausted hint '..index,function()
  ui.g_self.cur_page=1
  local labels={};local create=ms.d_u.createByStyle
  ms.d_u.createByStyle=function(style,...)
   if style.string then labels[#labels+1]=tostring(style.string) end
   return create(style,...)
  end
  local ok,err=pcall(ms.d_data.callback_update_config,{local_pavilion={data=data,status=FIXTURE.status}})
  ms.d_u.createByStyle=create
  assert(ok,err)
  local text=table.concat(labels,'\n')
  if index<3 then
   assert(string.find(text,'可以提升1次购买上限',1,true),text)
   assert(string.find(text,tostring(data.exchange_info[1].need_charge),1,true),text)
  else
   assert(not string.find(text,'可以提升',1,true),text)
  end
 end)
end
root:removeAllChildrenWithCleanup(true);root:release()
for i=#saved,1,-1 do local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end;for k,v in pairs(row.old) do row.t[k]=v end end
ms.MS_report_error=report
pavilion_fixture_results=checks
local out={};for _,v in ipairs(checks) do out[#out+1]=v.name..':'..tostring(v.ok)..':'..v.error end
return table.concat(out,'\n')
