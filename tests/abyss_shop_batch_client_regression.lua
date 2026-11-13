-- Native contracts: getShopItem L1607-1673, quantity picker callback L1658.
local source=...
local sent,notices,button,picker={},{},nil,nil
local ms={d_u={},d_data={},d_tableView={},d_info={},d_abyssUI={}}
local ui=ms.d_abyssUI
package.loaded.ms=ms
ui.showBossLayer=function() end
ui.g_abyssUI={shop_layer={}}
ui.sendRequest=function(op,data) sent[#sent+1]={op=op,data=data} end
ms.d_info.show=function(message) notices[#notices+1]=message end
ms.d_tableView.createTableViewMenu=function(config)
 for _,row in ipairs(config.menuItems) do
  if row.npic=='v2/soulHuntUI/btn_buy1.png' then button=row.tapHandler end
 end
 return config
end
ms.d_data.createBatchUse=function(parent,config,callback)
 assert(parent==ui.g_abyssUI.shop_layer)
 picker={config=config,callback=callback,count=config.defaultCount}
end
ui.getShopItem=function(item,index)
 local function nativeBuy()
  if item.buy_times<=0 or ui.g_data.hook.specter_data.crystal_count<item.crystals then return end
  local affordable=math.floor(ui.g_data.hook.specter_data.crystal_count/item.crystals)
  if (index==5 or index==6) and affordable>10 then
   ms.d_data.createBatchUse(ui.g_abyssUI.shop_layer,{min=1,max=math.min(affordable,15),defaultCount=1},
    function(count) ui.sendRequest(12,{index=index,count=count}) end)
  else ui.sendRequest(12,{index=index,count=1}) end
 end
 ms.d_tableView.createTableViewMenu({menuItems={
  {npic='other',tapHandler=function() end},
  {npic='v2/soulHuntUI/btn_buy1.png',tapHandler=nativeBuy}}})
 if item.render_error then error('render failure') end
 return item
end
local native,create=ui.getShopItem,ms.d_tableView.createTableViewMenu
assert(loadstring(source))()
local wrapper=ui.getShopItem
assert(loadstring(source))();assert(ui.getShopItem==wrapper,'installation must be idempotent')
local function fresh(balance,remaining,price,index)
 index=index or 1
 sent={};notices={};picker=nil
 local row={object_type=5,attach_type=1310,attach_count=1,attach_level=1,
            crystals=price or 20,buy_times=remaining or 500}
 ui.g_data={hook={specter_data={crystal_count=balance}},
  shop={shop_day=123,shop_revision='current',shop_list={[index]=row}}}
 local card=ui.getShopItem(row,index)
 assert(ms.d_tableView.createTableViewMenu==create,'renderer must restore helper')
 return row,card
end
for index=1,6 do
 fresh(10000,500,20,index);button()
 assert(picker and picker.config.max==100,'all six slots must open a picker capped at 100')
 assert(picker.config.min==1 and picker.count==1)
 for _=1,110 do picker.count=math.min(picker.config.max,picker.count+1) end
 assert(picker.count==100)
 picker.callback(picker.count)
 local request=sent[1]
 assert(#sent==1 and request.op==12 and request.data.index==index and request.data.count==100)
 assert(request.data.shop_day==123 and request.data.shop_revision=='current')
end
for _,case in ipairs({{10000,7,20,7},{99,500,20,4},{10000,20,200,20},{10000,10,1000,10}}) do
 fresh(case[1],case[2],case[3]);button()
 assert(picker and picker.config.max==case[4],'respect quota and affordable quantity')
end
fresh(20,500,20);button();assert(not picker and sent[1].data.count==1)
for _,case in ipairs({{19,500,20},{10000,0,20},{10000,500,0}}) do
 fresh(case[1],case[2],case[3]);button()
 assert(not picker and #sent==0 and #notices==1,'unavailable purchase must not be sent')
end
fresh(10000,500);button()
local confirm=picker.callback
for _,count in ipairs({0,-1,1.5,101}) do confirm(count) end
assert(#sent==0,'invalid batch quantities')
ui.g_data.hook.specter_data.crystal_count=20;confirm(100)
assert(#sent==0,'balance changed while dialog was open')
fresh(10000,500);button();confirm=picker.callback
ui.g_data.shop.shop_list[1].buy_times=2;confirm(100)
assert(#sent==0,'quota changed while dialog was open')
fresh(10000,500);button();confirm=picker.callback
ui.g_data.shop.shop_revision='new';confirm(100)
assert(#sent==0,'stale dialog cannot buy a refreshed shelf')
fresh(10000,500);button();confirm=picker.callback
ui.g_data.shop.shop_day=124;confirm(100);assert(#sent==0,'stale day')
local row=fresh(10000,500);button();picker.callback(100)
-- Native response handler renders the received quantity, then stores it as row.
local reply={object_type=5,attach_type=1310,attach_count=100,attach_level=1,crystals=20,buy_times=400}
local card=ui.getShopItem(reply,1)
assert(card.attach_count==1 and reply.attach_count==100,'preserve unit display and actual reward count')
ui.g_data.shop.shop_list[1]=reply
reply.attach_count=70
assert(ui.getShopItem(reply,1).attach_count==1,'successive redraw must not multiply unit quantity')
row=fresh(10000,500);row.render_error=true
assert(not pcall(ui.getShopItem,row,1))
assert(ms.d_tableView.createTableViewMenu==create,'helper must be restored on render error')
ui._localAbyssShopBatchRestore();assert(ui.getShopItem==native)
print('Abyss batch UI: six slots, 100 cap, balance/quota, stale dialogs, redraw, restore passed')
