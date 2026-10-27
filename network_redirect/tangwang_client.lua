-- Keep native manual dragging/exchange; permanent entry and weekly countdown.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_cardUI
 if not ui or not ms.d_data or not ms.d_time then return 'pending' end
 if not ui._localTangwangRestore then
  local old={}
  for _,k in ipairs({'updateActivityStatus','canJoin','show','createExchangeLayer',
   'count_down_func','showTips','sendExchangeRequest','exchangePressed','onGetExchangeResponse','resetCards',
   'pressOneKey1','pressOneKey2','pressOneKey3'}) do old[k]=ui[k] end
  local oldLetters=ms.d_data.getSpringCardLetters;local savedLetters=ms.d_data.g_letters
  local hz=ms.d_hz.gethz
  local originalStatus=ms.d_activityUI.getQiwenStatus
  local data,lastRequest,countdownY,selectionRevision=nil,-100,0.13,0
  local function active() return ui.g_cardUI and ui.g_cardUI.main_layer and ui.g_cardUI.main_layer:getParent() end
  local function query()
   local now=ms.d_time.getTime()
   if now-lastRequest>=3 or now<lastRequest then
    lastRequest=now
    ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_query_event_status,{flag=0})
   end
  end
  local function stale() return not data or ms.d_time.getTime()>=data.next_weekly_refresh end
  ms.d_data.getSpringCardLetters=function()
   ms.d_data.g_letters=data and data.letters or {'国','庆','快','乐','有','礼','欢','度'}
  end
  ms.d_data.getSpringCardLetters()
  ms.d_hz.gethz=function(key,...)
   if key=='springCardTip8' then return '按顺序拖入四枚金牌，手动组合兑换' end
   if key=='springCardTip9' then return '请先放入四枚金牌' end
   if key=='springCardTip10' then return '未构成指定组合，将随机获得银两或小包子，确认兑换？' end
   return hz(key,...)
  end
  ui.canJoin=function(...)
   if data and data.local_permanent then return data.local_enabled end
   return old.canJoin(...)
  end
  ui.count_down_func=function()
   if not data or not active() then return end
   local left=math.max(0,data.next_weekly_refresh-ms.d_time.getTime())
   local text=string.format('%d天%d小时%d分%d秒',math.floor(left/86400),math.floor(left/3600)%24,math.floor(left/60)%60,left%60)
   local layer=ui.g_cardUI.main_layer;local tag=ui.g_self.timeLabelTag
   local node=layer:getChildByTag(tag)
   if node then tolua.cast(node,'CCLabelTTF'):setString(text) else
    node=ms.d_u.createByStyles({type='label',font='arial',fontsize=26,x=0.58,y=countdownY,
     string=text,color={254,250,161}})
    layer:addChild(node,4,tag)
   end
   local width=CCDirector:sharedDirector():getVisibleSize().width*0.29
   node:setScale(math.min(1,width/node:getContentSize().width))
   if data.local_enabled and (data.daily_gift_pending or ms.d_time.getTime()>=data.next_daily_refresh) then query() end
  end
  ui.createExchangeLayer=function(...)
   local create=ms.d_u.createByStyles
   local menu=ms.d_u.createMenu
   ms.d_u.createMenu=function(styles,...)
    local filtered={}
    for k,v in pairs(styles) do if type(k)~='number' then filtered[k]=v end end
    for _,v in ipairs(styles) do
     if not (v.npic and v.npic:find('v2/CardUI/scheme',1,true)) then
      local row=ms.d_c.table_copy(v)
      if row.npic=='v2/CardUI/exchange1.png' then row.x=0.5 end
      filtered[#filtered+1]=row
     end
    end
    return menu(filtered,...)
   end
   ms.d_u.createByStyles=function(styles,...)
    if styles.pic=='v2/CardUI/text2.png' then
     countdownY=styles.y
     styles={type='label',font='arial',fontsize=24,x=0.36,y=styles.y,
      string='本周刷新剩余',color={147,43,42}}
    end
    return create(styles,...)
   end
   local ok,result=pcall(old.createExchangeLayer,...)
   ms.d_u.createByStyles=create;ms.d_u.createMenu=menu
   if not ok then error(result) end
   ui.count_down_func()
   return result
  end
  -- Exclude unusable cards from native instance selection as well as the server.
  ui.resetCards=function(...)
   selectionRevision=selectionRevision+1
   local typ=ms.d_common_def.object_type.item
   local kind=ms.d_common_def.item_main_type.invisible_card
   local items=ms.d_packageUI.g_reorgItemsInfo[typ]
   local original=items and items[kind]
   if original then
    local available={}
    for _,c in pairs(original) do
     if c.type_id==1094 and c.level>=1 and c.level<=8 and (not c.is_lock or c.is_lock==0)
      and (not c.equip_pos or c.equip_pos==0) and (not c.equip_order or c.equip_order==0)
      and (not c.owner_id or c.owner_id==0) then available[#available+1]=c end
    end
    items[kind]=available
   end
   local ok,result=pcall(old.resetCards,...)
   if items then items[kind]=original end
   if not ok then error(result) end
   return result
  end
  ui.updateActivityStatus=function(value,...)
   local incoming=value and value.tangwang_info
   local changed=incoming and (not data or incoming.week~=data.week or incoming.weekly_cards~=data.weekly_cards)
   if incoming then data=incoming;ms.d_data.getSpringCardLetters() end
   local result=old.updateActivityStatus(value,...)
   if incoming and active() then
    if changed then ui.resetCards() end
    ui.count_down_func()
   end
   return result
  end
  ms.d_activityUI.getQiwenStatus=function(value,...)
   -- A heartbeat has only card status; do not rebuild the menu or clear other activities.
   if value and value.local_tangwang_only then return ui.updateActivityStatus(value) end
   return originalStatus(value,...)
  end
  ui.show=function(...)
   query();local result=old.show(...);ui.count_down_func();return result
  end
  local function ready()
   if stale() then query();ms.d_info.show('金牌已到周刷新时间，正在更新，请重新组合');return false end
   if not data.local_enabled then ms.d_info.show('唐王集卡诏暂未开放');return false end
   for i=1,4 do
    local row=ui.g_cardUI.UsedCards and ui.g_cardUI.UsedCards[i]
    if not row or not row.level or row.level<1 then ms.d_info.show('请先放入四枚金牌');return false end
   end
   return true
  end
  ui.sendExchangeRequest=function(...)
   if ready() then return old.sendExchangeRequest(...) end
  end
  ui.exchangePressed=function()
   if not ready() then return end
   if ui.checkCompose() then return ui.sendExchangeRequest() end
   local week,revision=data.week,selectionRevision
   return ms.d_quitUI.createYesNoByStyle(ui.g_cardUI.main_layer,
    {string=ms.d_hz.gethz('springCardTip10')},function()
     if not data or data.week~=week or selectionRevision~=revision then
      ms.d_info.show('金牌选择已更新，请重新组合');return
     end
     ui.sendExchangeRequest()
    end)
  end
  ui.onGetExchangeResponse=function(value,...)
   if value.local_tangwang then ui.updateActivityStatus({tangwang_info=value.local_tangwang}) end
   if not active() then return end
   ui.resetCards()
   -- Runtime 3.87's native callback expects a bare array; our event also has status.
   ms.d_prizeUI.setPrize({prize_list=value.prize_list or value})
   ms.d_prizeUI.show(ui.g_cardUI.main_layer)
  end
  for _,name in ipairs({'pressOneKey1','pressOneKey2','pressOneKey3'}) do
   if old[name] then ui[name]=function() ms.d_info.show('请手动拖入金牌组合兑换') end end
  end
  -- The introduction contains only recipes, with no auto-combine controls or rewards after them.
  ui.showTips=function()
   if not active() then return end
   local main=ui.g_cardUI.main_layer;main:removeChildByTag(91094,true)
   local layer=CCLayerColor:create(ccc4(25,20,15,245));main:addChild(layer,100,91094)
   ms.d_u.createSwallowTouchLayer(layer)
   local function label(text,y,size)
    layer:addChild(ms.d_u.createByStyles({type='label',font='arial',fontsize=size,x=0.5,y=y,
     string=text,color={254,235,185}}),2)
   end
   label('唐王集卡诏 · 组合介绍',0.87,32)
   label('组合一：国庆快乐',0.73,30)
   label('组合二：国庆有礼',0.62,30)
   label('组合三：欢度国庆',0.51,30)
   label('按上述顺序手动放入四枚金牌，再点击兑换',0.37,24)
   label(string.format('每日领%d枚随机金牌；关卡胜利有%d%%概率掉落1枚',data and data.daily_cards or 4,data and data.travel_drop_percent or 30),0.26,24)
   label('每周一0点刷新，剩余金牌按1:1邮件返还蟠桃',0.15,24)
   layer:addChild(ms.d_u.createMenu({x=0,y=0,{npic='v2/introUI/close1.png',spic='v2/introUI/close2.png',
    x=0.95,y=0.93,scalexx=0.1,call_back=function() main:removeChildByTag(91094,true) end}}),3)
  end
  ui._localTangwangRestore=function()
   for k,v in pairs(old) do ui[k]=v end
   ms.d_data.getSpringCardLetters=oldLetters;ms.d_data.g_letters=savedLetters
   ms.d_activityUI.getQiwenStatus=originalStatus
   ms.d_hz.gethz=hz;ui._localTangwangRestore=nil
  end
 end
end
