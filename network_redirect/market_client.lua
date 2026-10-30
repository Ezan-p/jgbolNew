-- Preserve native purchase bookkeeping; display the server's actual bundle award.
do
 local ms=package.loaded.ms
 local shop=ms and ms.d_shopUI
 if shop and shop.recvBuyShopItem and not shop._localMarketRestore then
  local original=shop.recvBuyShopItem
  local hz=ms.d_hz.gethz
  ms.d_hz.gethz=function(key,...)
   if key=='sales1' then return '每周二、四、六开启' end
   if key=='sales8' then return '每周二、四、六零点刷新商品，七折出售；前件限购3份，购完解锁后件1份' end
   return hz(key,...)
  end
  shop.recvBuyShopItem=function(data,...)
   local result=original(data,...)
   if data.first_send==0 and data.result==1 and data.attach_list and #data.attach_list>0 then
    ms.d_commonLayerUI.showPrizeResLayer(CCDirector:sharedDirector():getRunningScene(),data.attach_list)
   end
   return result
  end
  shop._localMarketRestore=function()
   shop.recvBuyShopItem=original;ms.d_hz.gethz=hz;shop._localMarketRestore=nil
  end
 end
end

-- Buying a bun into inventory has its own shop quota. Native buyShopItem
-- incorrectly gates it on strength_item_count (the quick-use counter).
do
 local ms=package.loaded.ms
 local shop=ms and ms.d_shopUI
 if shop and shop.buyShopItem and not shop._localMarketBunRestore then
  local buy=shop.buyShopItem
  shop.buyShopItem=function(goods,page,count)
   local row=goods and goods.buyInfo
   if (page~=1 and page~=2) or not row or row.type_id~=1022 then return buy(goods,page,count) end
   count=count or 1
   if type(count)~='number' or count~=math.floor(count) or count<1 or count>999 then return end
   if page==1 and (count~=1 or (row.buy_limit_times or 0)<1) then
    ms.d_info.show('今日特惠包子已售罄');return
   end
   local player=ms.d_mainUI.g_playerInfo
   if (player.gold_coin or 0)<row.buy_price*count then
    ms.d_summonUI.needGold(ms.d_mainUI.g_mainUI.main_layer);return
   end
   shop.g_buyAndUse=0
   return ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_buy_item_in_batch,
    {first_send=0,page_id=page,index=row.index,type_id=row.type_id,count=count})
  end
  shop._localMarketBunRestore=function()
   shop.buyShopItem=buy;shop._localMarketBunRestore=nil
  end
 end
end

-- Native getCurrentPrice returns the original price outside the opening window.
-- Fixed-price pools carry an explicit quote, including in previews and sold-out UI.
do
 local ms=package.loaded.ms
 local sales=ms and ms.d_salesUI
 if sales and sales.getCurrentPrice and not sales._localMarketPriceRestore then
  local original=sales.getCurrentPrice
  sales.getCurrentPrice=function(...)
   local data=sales.g_self and sales.g_self.data
   local activity=data and data.activity_data
   local first=activity and activity.sale_item and activity.sale_item[1]
   if first and type(first.panic_price)=='number' then return first.panic_price end
   return original(...)
  end
  sales._localMarketPriceRestore=function()
   sales.getCurrentPrice=original;sales._localMarketPriceRestore=nil
  end
 end
end
