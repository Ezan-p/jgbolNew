-- Retain native fishing/exchange controls; use authoritative offline snapshots.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_fishRushUI
 if not ui or not ms.d_u or not ms.d_time then return 'pending' end
 if not ui._localFishRestore then
  local old={}
  for _,k in ipairs({'updateActivityStatus','canJoin','count_down_func','showPriceListInfo','onGetFishRushResult','show','onPressCommit','pressExchange','onPressRush','onPressTenRush','createDynamicElements','createStaticElements'}) do old[k]=ui[k] end
  local hz=ms.d_hz.gethz
  local data,lastRequest=nil,-100
  local function active() return ui.g_FishRushUI and ui.g_FishRushUI.main_layer and ui.g_FishRushUI.main_layer:getParent() end
  local function query()
   local now=ms.d_time.getTime()
   if now-lastRequest>=3 or now<lastRequest then
    lastRequest=now
    ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_query_event_status,{flag=0})
   end
  end
  local function stale()
   return data and ms.d_time.getTime()>=data.next_daily_refresh
  end
  ms.d_hz.gethz=function(key,...)
   if key=='catch_fish_tips1' then return '商店每日0点刷新，活动常驻开放' end
   if key=='catch_fish_tips2' then return '周一0点结算，剩余锦鲤邮件返蟠桃' end
   return hz(key,...)
  end
  ui.canJoin=function(...)
   if data and data.local_permanent then return data.local_enabled end
   return old.canJoin(...)
  end
  ui.count_down_func=function()
   if not data or not active() then return end
   local now=ms.d_time.getTime()
   local left=math.max(0,data.next_weekly_refresh-now)
   local text=string.format('%d天%d小时%d分%d秒',
    math.floor(left/86400),math.floor(left/3600)%24,math.floor(left/60)%60,left%60)
   local layer=ui.g_FishRushUI.main_layer;local tag=ui.g_self.tags.tagTime
   local node=layer:getChildByTag(tag)
   if node then tolua.cast(node,'CCLabelTTF'):setString(text) else
    node=ms.d_u.createByStyles({type='label',font='arial',fontsize=28,x=0.22,y=0.151,
     string=text,color={255,255,255}})
    layer:addChild(node,33,tag)
   end
   local width=CCDirector:sharedDirector():getVisibleSize().width*0.315
   node:setScale(math.min(1,width/node:getContentSize().width))
   if stale() then query() end
  end
  ui.createStaticElements=function(...)
   local result=old.createStaticElements(...)
   -- The native main-layer touch handler only opens the reward preview.
   -- Menu controls handle casting, exchange and closing independently.
   ui.g_FishRushUI.main_layer:unregisterScriptTouchHandler()
   ui.g_FishRushUI.main_layer:setTouchEnabled(false)
   -- The original "activity ends" caption is baked into the background bitmap.
   local size=CCDirector:sharedDirector():getVisibleSize()
   local cover=CCLayerColor:create(ccc4(15,47,56,255),size.width*0.34,size.height*0.145)
   cover:setPosition(ccp(size.width*0.05,size.height*0.112))
   ui.g_FishRushUI.main_layer:addChild(cover,31)
   -- Reuse the exact gold calligraphy heading and bronze frame from the game.
   local function picture(path,y,width,height)
    local sprite=CCSprite:create(path)
    local bounds=sprite:getContentSize()
    sprite:setScaleX(size.width*width/bounds.width);sprite:setScaleY(size.height*height/bounds.height)
    sprite:setPosition(ccp(size.width*0.22,size.height*y))
    ui.g_FishRushUI.main_layer:addChild(sprite,32)
   end
   picture('v2/moonCakeUI/time.png',0.219,0.215,0.072)
   picture('v2/newTurnTableUI/time_bkg.png',0.151,0.335,0.072)
   return result
  end
  local function fitShop()
   local layer=ui.g_FishRushUI.child_layer
   if not layer then return end
   local width=CCDirector:sharedDirector():getVisibleSize().width*0.105
   local function walk(node)
    if tolua.type(node)=='CCLabelTTF' then
     local w=node:getContentSize().width
     if w>width then node:setScale(width/w) end
    end
    local children=node:getChildren()
    if children then for i=0,children:count()-1 do walk(tolua.cast(children:objectAtIndex(i),'CCNode')) end end
   end
   walk(layer)
  end
  ui.createDynamicElements=function(...)
   local result=old.createDynamicElements(...)
   local frame=ui.g_FishRushUI
   if frame and frame.main_layer and frame.menuTable and frame.menuTable[4] then
    frame.menuTable[4]:setVisible(true)
    local tag=ui.g_self.tags.tagGoldPerTenNetLab
    local node=frame.main_layer:getChildByTag(tag)
    if node then frame.main_layer:removeChild(node,true) end
    frame.main_layer:addChild(ms.d_u.createByStyles({type='label',font='arial',fontsize=30,x=0.564,y=0.294,
     string=tostring(ui.g_self.gold_per_net*10),color={254,250,161}}),30,tag)
   end
   return result
  end
  ui.updateActivityStatus=function(value,...)
   local incoming=value and value.search_gold_data
   local changed=incoming and data and (incoming.shop_day~=data.shop_day or incoming.shop_revision~=data.shop_revision)
   if incoming then data=incoming end
   local result=old.updateActivityStatus(value,...)
   if incoming and active() then
    if changed and ui.g_self.goodsList_shown==1 and ui.g_FishRushUI.child_layer then
     ui.g_FishRushUI.child_layer:removeFromParentAndCleanup(true)
     ui.g_FishRushUI.child_layer=nil
     old.onPressCommit(1);fitShop()
    elseif ui.g_self.goodsList_shown==1 then ui.refreshGoodsStatus() end
    ui.createDynamicElements();ui.onNewOthersMsg();ui.count_down_func()
   end
   return result
  end
  -- Keep stale/native callbacks harmless without opening a preview layer.
  ui.showPriceListInfo=function() end
  ui.onGetFishRushResult=function(value,...)
   local result=old.onGetFishRushResult(value,...)
   if value.local_fish then
    -- Event 86 broadcasts the new exchange separately; do not duplicate it.
    local snapshot=ms.d_c.table_copy(value.local_fish)
    if value.item_data then snapshot.broad_data=nil end
    ui.updateActivityStatus({search_gold_data=snapshot})
   end
   return result
  end
  ui.show=function(...)
   query()
   local result=old.show(...)
   ui.count_down_func()
   return result
  end
  for _,name in ipairs({'onPressCommit','pressExchange','onPressRush','onPressTenRush'}) do
   local original=old[name]
   ui[name]=function(...)
    if stale() then query();ms.d_info.show('商店已到刷新时间，正在更新，请稍后重试');return end
    local result=original(...)
    if name=='onPressCommit' then fitShop() end
    return result
   end
  end
  ui.pressExchange=function(index)
   if stale() then query();ms.d_info.show('商店已到刷新时间，请更新后兑换');return end
   local row=ui.g_self.goods_infos[index]
   if not row or row.count<=0 then return end
   local count=math.min(100,row.count,math.floor(ui.g_self.fish_count/row.cost_fish_count))
   if count<1 then ms.d_info.show('锦鲤不足');return end
   local day=data and data.shop_day
   local revision=data and data.shop_revision
   local function confirm(n)
    if stale() or not data or (data.shop_day~=day or data.shop_revision~=revision) then
     query();ms.d_info.show('商店已刷新，请重新选择商品');return
    end
    ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_search_gold,{type_id=row.type_id,count=n})
   end
   if count==1 then confirm(1) else
    -- Attach the picker to the shop so a daily rebuild also removes old offers.
    ui.createBatchUse(ui.g_FishRushUI.child_layer or ui.g_FishRushUI.main_layer,{min=1,max=count,tag=2},confirm)
   end
  end
  ui._localFishRestore=function()
   for k,v in pairs(old) do ui[k]=v end
   ms.d_hz.gethz=hz;ui._localFishRestore=nil
  end
 end
end
