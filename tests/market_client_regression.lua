local source=...
local calls,popups=0,0
local scene={}
CCDirector={sharedDirector=function() return {getRunningScene=function() return scene end} end}
local shop={recvBuyShopItem=function() calls=calls+1;return 'native' end}
local ms={d_shopUI=shop,d_hz={gethz=function(k) return k end},d_commonLayerUI={
 showPrizeResLayer=function(parent,rewards)
  assert(parent==scene and rewards[1].attach_count==20);popups=popups+1
 end}}
local sales={g_self={data={activity_data={sale_item={{price=20,panic_price=14},{price=40,panic_price=28}}}}},
 getCurrentPrice=function() return 20 end}
ms.d_salesUI=sales
package.loaded.ms=ms
assert(loadstring(source))()
assert(loadstring(source))()
local data={first_send=0,result=1,attach_list={{object_type=5,attach_type=1001,attach_count=20}}}
assert(shop.recvBuyShopItem(data)=='native')
shop.recvBuyShopItem({first_send=1,result=1,attach_list=data.attach_list})
shop.recvBuyShopItem({first_send=0,result=6,attach_list=data.attach_list})
assert(calls==3 and popups==1)
assert(ms.d_hz.gethz('sales8'):find('七折'))
assert(ms.d_hz.gethz('sales1')=='每周二、四、六开启')
assert(ms.d_hz.gethz('sales8'):find('每周二、四、六零点刷新商品'))
assert(ms.d_hz.gethz('sales2')=='sales2')
shop._localMarketRestore()
assert(ms.d_hz.gethz('sales1')=='sales1')
shop.recvBuyShopItem(data)
assert(calls==4 and popups==1)
for _,status in ipairs({'preview','active','sold_out','closed'}) do
 sales.g_self.data.activity_data.status=status
 assert(sales.getCurrentPrice()==14,status)
 assert(sales.g_self.data.activity_data.sale_item[1].price==20)
 assert(sales.g_self.data.activity_data.sale_item[2].panic_price==28)
end
-- A second installation must not stack wrappers; legacy data uses native pricing.
assert(loadstring(source))()
sales.g_self.data.activity_data.sale_item[1].panic_price=nil
assert(sales.getCurrentPrice()==20)
sales.g_self.data=nil
assert(sales.getCurrentPrice()==20)
sales._localMarketPriceRestore()
assert(sales.getCurrentPrice()==20)
local nativeBuys,sends,shortGold,soldOut=0,0,0,0
local nativeBuy=function() nativeBuys=nativeBuys+1 end
shop.buyShopItem=nativeBuy
ms.d_mainUI={g_playerInfo={gold_coin=10,strength_item_count=0,energy_item_count=0},g_mainUI={main_layer=scene}}
ms.d_info={show=function() soldOut=soldOut+1 end}
ms.d_summonUI={needGold=function() shortGold=shortGold+1 end}
ms.d_msg_def={gscl_msg_id={msg_buy_item_in_batch=1057}}
local expectedIndex
ms.d_u={main_server_send_msg=function(mid,request)
 assert(mid==1057 and request.index==expectedIndex and request.page_id==1 and request.count==1)
 sends=sends+1
end}
assert(loadstring(source))()
assert(loadstring(source))()
for _,case in ipairs({{1022,24,5},{1023,27,10}}) do
 local goods={buyInfo={type_id=case[1],index=case[2],buy_price=case[3],buy_limit_times=10}}
 expectedIndex=case[2]
 ms.d_mainUI.g_playerInfo.gold_coin=case[3]
 local before=sends
 shop.g_buyAndUse=1
 shop.buyShopItem(goods,1)
 assert(sends==before+1 and nativeBuys==0 and shop.g_buyAndUse==0)
 goods.buyInfo.buy_limit_times=0;shop.buyShopItem(goods,1)
 assert(sends==before+1)
 goods.buyInfo.buy_limit_times=10;ms.d_mainUI.g_playerInfo.gold_coin=case[3]-1
 shop.buyShopItem(goods,1)
 assert(sends==before+1)
end
assert(shortGold==2 and soldOut==2)
assert(ms.d_mainUI.g_playerInfo.strength_item_count==0 and ms.d_mainUI.g_playerInfo.energy_item_count==0)
shop.buyShopItem({buyInfo={type_id=1093}},1)
assert(nativeBuys==1)
shop._localMarketBunRestore()
assert(shop.buyShopItem==nativeBuy)
return 'market client regression passed'
