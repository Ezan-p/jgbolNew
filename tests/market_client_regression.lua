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
return 'market client regression passed'
