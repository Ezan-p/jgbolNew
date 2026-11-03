-- Keep native manual dragging; single/batch exchange and weekly countdown.
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
  local batchPressed
  local function usable(c)
   return c.type_id==1094 and c.level>=1 and c.level<=8 and (c.count or 0)>0
    and (not c.is_lock or c.is_lock==0) and (not c.equip_pos or c.equip_pos==0)
    and (not c.equip_order or c.equip_order==0) and (not c.owner_id or c.owner_id==0)
  end
  local function inventory()
   local items=ms.d_packageUI.g_reorgItemsInfo[ms.d_common_def.object_type.item]
   return items and items[ms.d_common_def.item_main_type.invisible_card] or {}
  end
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
   local exchangeY
   ms.d_u.createMenu=function(styles,...)
    local filtered={}
    for k,v in pairs(styles) do if type(k)~='number' then filtered[k]=v end end
    for _,v in ipairs(styles) do
     if not (v.npic and v.npic:find('v2/CardUI/scheme',1,true)) then
      local row=ms.d_c.table_copy(v)
      if row.npic=='v2/CardUI/exchange1.png' then row.x=0.36;exchangeY=row.y end
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
   if exchangeY then
    local layer=ui.g_cardUI.main_layer
    layer:addChild(menu({x=0,y=0,{npic='v2/crossServerUI/btn_bkg.png',
     spic='v2/crossServerUI/btn_bkg.png',x=0.66,y=exchangeY,scalexx=0.21,
     call_back=function() batchPressed() end}}),3)
    layer:addChild(create({type='label',font='arial',fontsize=26,x=0.66,y=exchangeY,
     string='批量兑换',color={254,235,185}}),4)
   end
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
     if usable(c) then available[#available+1]=c end
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
   if not active() then return false end
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
  batchPressed=function()
   if not ready() then return end
   if not data.max_batch then ms.d_info.show('请更新离线服务后使用批量兑换');return end
   local levels,byLevel,needed={},{},{}
   for i=1,4 do
    local lv=ui.g_cardUI.UsedCards[i].level
    levels[i]=lv;needed[lv]=(needed[lv] or 0)+1
   end
   local seen={}
   for _,c in pairs(inventory()) do
    if usable(c) and not seen[c.id] then
     seen[c.id]=true;byLevel[c.level]=byLevel[c.level] or {}
     table.insert(byLevel[c.level],c.id)
    end
   end
   local maximum=math.min(63,data.max_batch)
   for lv,n in pairs(needed) do
    local ids=byLevel[lv] or {};table.sort(ids)
    maximum=math.min(maximum,math.floor(#ids/n))
   end
   if maximum<1 then ms.d_info.show('可用金牌不足，请重新组合');return end
   local week,revision,main=data.week,selectionRevision,ui.g_cardUI.main_layer
   local submitted=false
   local function valid()
    if not ready() then return false end
    if submitted or data.week~=week or revision~=selectionRevision or ui.g_cardUI.main_layer~=main then
     ms.d_info.show('金牌选择已更新，请重新组合');return false
    end
    for i,lv in ipairs(levels) do
     if ui.g_cardUI.UsedCards[i].level~=lv then
      ms.d_info.show('金牌选择已更新，请重新组合');return false
     end
    end
    return true
   end
   ms.d_data.createBatchUse(main,{min=1,max=maximum,defaultCount=1,
    buyTip='兑换组数：每组4枚，最多'..maximum..'组'},function(count)
    if not valid() then return end
    if type(count)~='number' or count~=math.floor(count) or count<1 or count>maximum then return end
    local cards,offsets={},{}
    for n=1,count do for _,lv in ipairs(levels) do
     offsets[lv]=(offsets[lv] or 0)+1
     cards[#cards+1]={id=byLevel[lv][offsets[lv]]}
    end end
    local words={};for _,lv in ipairs(levels) do words[#words+1]=data.letters[lv] end
    local warning=ui.checkCompose() and '每组独立随机获得一项对应组合奖励。' or
     '未构成指定组合，每组仅随机获得银两或小包子。'
    ms.d_quitUI.createYesNoByStyle(main,{string=string.format('按“%s”兑换%d组，消耗%d枚金牌。%s确认兑换？',
     table.concat(words),count,count*4,warning)},function()
     if not valid() then return end
     local available={};for _,c in pairs(inventory()) do if usable(c) then available[c.id]=c.level end end
     for i,c in ipairs(cards) do
      if available[c.id]~=levels[(i-1)%4+1] then
       ms.d_info.show('金牌库存已变化，请重新选择兑换数量');return
      end
     end
     submitted=true;selectionRevision=selectionRevision+1
     ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_exchange_tangwang_prize,
      {count=#cards,card_list=cards})
    end)
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
  -- Reuse the native gold/brown panel and layout, replacing only its copy.
  ui.showTips=function()
   if not active() then return end
   local main=ui.g_cardUI.main_layer;main:removeChildByTag(91094,true)
   local getConfig,savedTips=ms.d_data.getCardTipConfig,ms.d_data.g_card_tip
   local gethz=ms.d_hz.gethz
   ms.d_data.getCardTipConfig=function()
    ms.d_data.g_card_tip={'国庆快乐：可兑换特殊奖励','国庆有礼：可兑换特殊奖励','欢度国庆：可兑换特殊奖励'}
   end
   ms.d_hz.gethz=function(key,...)
    if key=='springCardTip6' then return '收集到以下组合会有特殊奖励：' end
    if key=='springCardTip7' then return '放入四枚金牌，未构成以上组合也可进行兑换' end
    return gethz(key,...)
   end
   local ok,result=pcall(old.showTips)
   ms.d_data.getCardTipConfig=getConfig;ms.d_data.g_card_tip=savedTips;ms.d_hz.gethz=gethz
   if not ok then error(result) end
   -- Native showTips adds its panel last; tag it to prevent duplicate overlays.
   local children=main:getChildren()
   tolua.cast(children:objectAtIndex(children:count()-1),'CCNode'):setTag(91094)
   return result
  end
  ui._localTangwangRestore=function()
   for k,v in pairs(old) do ui[k]=v end
   ms.d_data.getSpringCardLetters=oldLetters;ms.d_data.g_letters=savedLetters
   ms.d_activityUI.getQiwenStatus=originalStatus
   ms.d_hz.gethz=hz;ui._localTangwangRestore=nil
  end
 end
end
