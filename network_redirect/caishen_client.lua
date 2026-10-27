-- Native Caishen controls with server-owned dates, offers and weekly countdown.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_springActivityMoneyUI
 if not ui or not ms.d_u or not ms.d_time then return 'pending' end
 if not ui._localCaishenRestore then
  local old={}
  for _,k in ipairs({'updateActivityStatus','canJoin','count_down_func','show','createStaticElements',
   'onPressCommit','pressExchange','onPressRush','onGetSpringActivityExchangeResult','onGetSpringActivityMoneyResult'}) do old[k]=ui[k] end
  local hz=ms.d_hz.gethz
  local data,lastRequest,timer=nil,-100,nil
  local scheduler=CCDirector:sharedDirector():getScheduler()
  local function active() return ui.g_SpringActivityMoneyUI and ui.g_SpringActivityMoneyUI.main_layer and ui.g_SpringActivityMoneyUI.main_layer:getParent() end
  local function query()
   local now=ms.d_time.getTime()
   if now-lastRequest>=3 or now<lastRequest then
    lastRequest=now
    ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_query_event_status,{flag=0})
   end
  end
  local function stale() return not data or ms.d_time.getTime()>=data.next_daily_refresh end
  local function ready()
   if stale() then query();ms.d_info.show('财神商店正在刷新，请稍后重试');return false end
   if not data.local_enabled then ms.d_info.show('财神贺岁尚未开放');return false end
   return true
  end
  ms.d_hz.gethz=function(key,...)
   if key=='springCSEndTime' then return '常驻开放 · 每周一0点刷新' end
   if key=='springActivityTips' then return '每日0点换货；周一余币按2:1邮件返蟠桃' end
   return hz(key,...)
  end
  ui.canJoin=function(...)
   if data and data.local_permanent then return data.local_enabled end
   return old.canJoin(...)
  end
  local function button()
   if not data or not active() then return end
   local item=ui.g_SpringActivityMoneyUI.menuTable[2]
   if not item then return end
   item:setNormalImage(CCSprite:create('v2/springActivityUI/bai.png'))
   item:setSelectedImage(CCSprite:create('v2/springActivityUI/bai1.png'))
   local enabled=data.local_enabled and not data.visited_today
   item:setEnabled(enabled)
   if not enabled then ms.d_u.grayMenuItem(item,false) end
  end
  local function label(layer,tag,text,x,y,size)
   local node=layer:getChildByTag(tag)
   if node then tolua.cast(node,'CCLabelTTF'):setString(text) else
    node=ms.d_u.createByStyles({type='label',font='arial',fontsize=size,x=x,y=y,string=text,color={255,240,215}})
    layer:addChild(node,30,tag)
   end
  end
  ui.count_down_func=function()
   if not data or not active() then return end
   local left=math.max(0,data.next_weekly_refresh-ms.d_time.getTime())
   local text=string.format('%d天%d小时%d分%d秒',math.floor(left/86400),math.floor(left/3600)%24,math.floor(left/60)%60,left%60)
   local frame=ui.g_SpringActivityMoneyUI
   label(frame.main_layer,91028,'周刷新剩余 '..text,0.5,0.039,24)
   if ui.g_self.goodsList_shown==1 and frame.child_layer then
    label(frame.child_layer,ui.g_self.tags.tagTime,text,0.63,0.765,28)
   end
   if stale() then query() end
  end
  ui.createStaticElements=function(...)
   -- Replace the original dated end-time label, retaining native background art.
   local create=ms.d_u.createByStyles
   ms.d_u.createByStyles=function(styles,...)
    local node=create(styles,...)
    if styles.type=='label' and styles.y==0.039 then node:setTag(91028) end
    return node
   end
   local ok,result=pcall(old.createStaticElements,...)
   ms.d_u.createByStyles=create
   if not ok then error(result) end
   return result
  end
  local function fitShop()
   local layer=ui.g_SpringActivityMoneyUI.child_layer
   if not layer then return end
   local size=CCDirector:sharedDirector():getVisibleSize()
   local width=size.width*0.12
   -- The old deadline caption is baked into goods_bkg.png.
   if not layer:getChildByTag(91029) then
    local cover=CCLayerColor:create(ccc4(238,175,39,255),size.width*0.225,size.height*0.075)
    cover:setPosition(ccp(size.width*0.29,size.height*0.727))
    layer:addChild(cover,26,91029)
    layer:addChild(ms.d_u.createByStyles({type='label',font='arial',fontsize=28,x=0.418,y=0.765,
     string='周刷新倒计时：',color={75,40,28}}),27,91030)
   end
   local function walk(node)
    if tolua.type(node)=='CCLabelTTF' then
     local text=node:getString()
     if not string.find(text,'每日') and not string.find(text,'天') and not string.find(text,'周刷新') then
      local w=node:getContentSize().width;if w>width then node:setScale(width/w) end
     end
    end
    local children=node:getChildren()
    if children then for i=0,children:count()-1 do walk(tolua.cast(children:objectAtIndex(i),'CCNode')) end end
   end
   walk(layer)
  end
  ui.updateActivityStatus=function(value,...)
   local incoming=value and value.visit_caishen
   local changed=incoming and data and (incoming.shop_day~=data.shop_day or incoming.shop_revision~=data.shop_revision)
   if incoming then data=incoming end
   local result=old.updateActivityStatus(value,...)
   if incoming and active() then
    if ui.g_self.goodsList_shown==1 then
     if changed then
      ui.g_SpringActivityMoneyUI.child_layer:removeAllChildrenWithCleanup(true)
      old.onPressCommit(1);fitShop()
     else ui.refreshGoodsStatus() end
    end
    button();ui.count_down_func()
   end
   return result
  end
  ui.show=function(...)
   query();ui.g_self.goodsList_shown=0
   local result=old.show(...)
   button();ui.count_down_func()
   if timer then scheduler:unscheduleScriptEntry(timer) end
   timer=scheduler:scheduleScriptFunc(function()
    if active() then ui.count_down_func() else scheduler:unscheduleScriptEntry(timer);timer=nil end
   end,1,false)
   return result
  end
  ui.onPressCommit=function(...)
   if not ready() then return end
   local result=old.onPressCommit(...);fitShop();ui.count_down_func();return result
  end
  ui.pressExchange=function(index)
   if not ready() then return end
   local row=ui.g_self.goods_infos[index]
   if not row or row.count<1 then ms.d_info.show('今日已经兑换过此商品');return end
   if ui.g_self.money_count<row.qianbi_count then ms.d_info.show('上古钱币不足');return end
   ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_exchange_caishen_prize,{prize_id=row.prize_id,count=1})
  end
  ui.onPressRush=function()
   if not ready() then return end
   if data.visited_today then ms.d_info.show('今日已经拜过财神，请明日再来');return end
   ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_visit_caishen,{flag=1})
  end
  for _,name in ipairs({'onGetSpringActivityExchangeResult','onGetSpringActivityMoneyResult'}) do
   local original=old[name]
   ui[name]=function(value,...)
    if active() then original(value,...) end
    if value.local_caishen then ui.updateActivityStatus({visit_caishen=value.local_caishen}) end
   end
  end
  ui._localCaishenRestore=function()
   if timer then scheduler:unscheduleScriptEntry(timer);timer=nil end
   for k,v in pairs(old) do ui[k]=v end
   ms.d_hz.gethz=hz;ui._localCaishenRestore=nil
  end
 end
end
