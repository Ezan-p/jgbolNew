-- Retain native routes, shops and movement; settle offline snapshots after walking.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_towerUI
 if not ui or not ms.d_c or not ms.d_time or not ms.d_fightUI then return 'pending' end
 if not ui._localNineSkyRestore then
  local old={}
  for _,key in ipairs({'onGetActResult','cancelSwallow','showFloorTitle','updateActivityStatus',
   'canJoin','sendRequest','create','showShopLayer','showComplexBuyLayer','getShopItem','showRandomPrize'}) do old[key]=ui[key] end
  local pending,meta,timerLayer,activeBattle=nil,nil,nil,nil
  local fight=ms.d_fightUI;local nativeFightEnd=fight.showFightEnd
  local shopVersions={};local lastRequest=-100;local installed=true
  local battleTag=91037
  local function main() return ui.g_towerUI and ui.g_towerUI.main_layer end
  local function shopLayer()
   local layer=main();return layer and layer:getChildByTag(ui.g_self.Tags.Shop)
  end
  local function stale(weekly)
   local untilTime=meta and meta[weekly and 'next_weekly_refresh' or 'next_daily_refresh']
   return untilTime and ms.d_time.getTime()>=untilTime
  end
  local function clearShops(all)
   ui.g_self.shop_data=ui.g_self.shop_data or {};ui.g_self.role_shop_data=ui.g_self.role_shop_data or {}
   if all then ui.g_self.shop_data={};ui.g_self.role_shop_data={}
   else for page=1,2 do ui.g_self.shop_data[page]=nil;ui.g_self.role_shop_data[page]=nil end end
   shopVersions={}
   local layer=main()
   if layer then layer:removeChildByTag(ui.g_self.Tags.Buy,true) end
   ui.g_towerUI.BuyInfo={}
  end
  local function refresh(page)
   if pending then return end
   local now=ms.d_time.getTime()
   if now-lastRequest<3 and now>=lastRequest then return end
   lastRequest=now
   if stale(true) or not page then old.sendRequest(1,{})
   else old.sendRequest(3,{buy_type=page,first_send=true}) end
  end
  local function label(layer,tag,text,x,y,size,anchor)
   layer:removeChildByTag(tag,true)
   local node=ms.d_u.createByStyle({type='label',font='arial',fontsize=size,string=text,
    x=x,y=y,anchor=anchor or {0.5,0.5},color={255,240,225}})
   layer:addChild(node,3,tag)
   return node
  end
  local function duration(value,withDays)
   local left=math.max(0,math.floor(value-ms.d_time.getTime()))
   local text=string.format('%02d:%02d:%02d',math.floor(left/3600)%24,math.floor(left/60)%60,left%60)
   return withDays and string.format('%d天 ',math.floor(left/86400))..text or text
  end
  ui._localNineSkyTick=function()
   local layer=main()
   if not installed or not layer or not meta or not meta.local_permanent then return end
   local frame=ui.g_towerUI
   if meta.next_weekly_refresh and frame.bw and frame.bh then
    label(layer,ui.g_self.Tags.Time,duration(meta.next_weekly_refresh,true),
     0.5-frame.bw*0.36,frame.bh*0.3384,24)
   end
   local shop=shopLayer()
   if shop and frame.local_shop_width and meta.next_daily_refresh then
    label(shop,11,duration(meta.next_daily_refresh,false),
     0.5-frame.local_shop_width*0.29,0.5+frame.local_shop_height*0.315,24,{0,0.5})
   end
   -- A ten-roll animation owns its old-week coordinates until its final callback.
   if not pending and (stale() or stale(true)) then refresh(shop and frame.shopType) end
  end
  local function schedule()
   local layer=main()
   if timerLayer==layer then return end
   timerLayer=layer
   local function tick()
    if not installed or timerLayer~=layer or main()~=layer or not layer:getParent() then return end
    ui._localNineSkyTick();ms.d_u.delay(layer,1,tick)
   end
   ui._localNineSkyTick();ms.d_u.delay(layer,1,tick)
  end
  -- Native timers capture the old event end forever. Disable them only while
  -- building this UI, replace their captions and run a fresh metadata-aware timer.
  local function render(kind,fn,...)
   if not meta or not meta.local_permanent then return fn(...) end
   local create,rest=ms.d_u.createByStyle,ms.d_time.getRestTime
   ms.d_time.getRestTime=function() return nil end
   ms.d_u.createByStyle=function(style,...)
    local value=style
    if kind=='main' and style.pic=='v2/towerUI/p_label1.png' then
     value=ms.d_c.table_copy(style);value.pic=nil;value.type='label';value.fontsize=24
     value.string='周重置倒计时';value.color={250,193,128}
    elseif kind=='shop' and style.string==ms.d_hz.gethz('upgrade_role_t2') then
     value=ms.d_c.table_copy(style);value.string='每日刷新：'
    end
    local node=create(value,...)
    if kind=='shop' and style.pic=='v2/towerUI/s_bkg.png' then
     ui.g_towerUI.local_shop_width,ui.g_towerUI.local_shop_height=ms.d_u.getRealScale(node)
    end
    return node
   end
   local args={...};local ok,result=pcall(function() return fn(unpack(args)) end)
   ms.d_u.createByStyle=create;ms.d_time.getRestTime=rest
   if not ok then error(result) end
   schedule();ui._localNineSkyTick()
   return result
  end
  ui.create=function(...) return render('main',old.create,...) end
  ui.showShopLayer=function(...) return render('shop',old.showShopLayer,...) end
  ui.getShopItem=function(row,index,bought,page)
   if page~=1 and page~=2 then return old.getShopItem(row,index,bought,page) end
   -- Native titles append X<count> at a fixed font size and overrun the last
   -- column. Fit the complete title inside its own card, including on purchase redraw.
   local expected=ui.getItemName(row.attach_data)
   if row.attach_data.attach_count>1 then expected=expected..'X'..row.attach_data.attach_count end
   local create=ms.d_u.createByStyle
   local title
   ms.d_u.createByStyle=function(style,...)
    local isTitle=style.type=='label' and style.string==expected and style.fontsize==28
    local node=create(style,...)
    if isTitle then title=node end
    return node
   end
   local ok,item=pcall(old.getShopItem,row,index,bought,page)
   ms.d_u.createByStyle=create
   if not ok then error(item) end
   if title then
    local background=tolua.cast(item:getChildren():objectAtIndex(0),'CCNode')
    local right=background:getPositionX()+background:getContentSize().width*background:getScaleX()
    local available=math.max(1,right-title:getPositionX()-12)
    local width=title:getContentSize().width
    if width>0 then title:setScale(math.min(title:getScaleX(),available/width)) end
    title:setTag(91038)
   end
   return item
  end
  ui.updateActivityStatus=function(value,...)
   if value and value.local_permanent then
    -- Status is global; exchange versions are only supplied by a rendered shop.
    if not meta then meta=ms.d_c.table_copy(value) end
    meta.local_enabled=value.local_enabled
   elseif value and value.begin_time==0 and value.end_time==0 and meta then meta.local_enabled=false end
   return old.updateActivityStatus(value,...)
  end
  ui.canJoin=function(...)
   if meta and meta.local_permanent then return meta.local_enabled~=false end
   return old.canJoin(...)
  end
  ui.sendRequest=function(op,data)
   data=data or {}
   if op~=1 and (stale(true) or (op==4 and stale())) then
    refresh(data.buy_type);ms.d_info.show('九重天已到刷新时间，正在更新，请重新操作');return
   end
   if op==3 then data=ms.d_c.table_copy(data);data.first_send=true end
   if op==4 and meta and meta.local_permanent then
    local version=shopVersions[data.buy_type]
    if not version or version.day~=meta.shop_day or version.revision~=meta.shop_revision then
     refresh(data.buy_type);ms.d_info.show('商店已刷新，请重新选择商品');return
    end
    data=ms.d_c.table_copy(data);data.shop_day=version.day;data.shop_revision=version.revision
   end
   return old.sendRequest(op,data)
  end
  ui.showComplexBuyLayer=function(...)
   if stale() then refresh(1);ms.d_info.show('商店已到刷新时间，正在更新');return end
   return old.showComplexBuyLayer(...)
  end
  local function sync(data)
   if not data or not data.local_snapshot then return end
   ui.g_self.role_data=ms.d_c.table_copy(data.local_snapshot)
   ui.g_self.role_data.floor=math.min(9,ui.getTowerFloor(ui.g_self.role_data.steps))
   ui.g_self.card_list=ui.processCardList(data.local_cards or {})
   ui.g_self.top_data=data.local_top
   if main() then ui.showDynamicInfo();ui.showTokenCount();ui.showTopPlayer() end
  end
  -- Native movement pauses at showRandomPrize and resumes through its callback.
  -- A private marker lets a battle use that same checkpoint, including rolls
  -- which also contain treasure or a palace, without inventing a reward.
  ui.showRandomPrize=function(items,callback)
   local marker=items and items[1] and items[1].local_nine_sky_battle
   if not marker then return old.showRandomPrize(items,callback) end
   local parent=main();local holder=CCLayer:create()
   local context={row=marker,parent=parent,holder=holder,callback=callback,treasure={},
    sceneID=ms.d_loginUI and ms.d_loginUI.g_currentSence}
   for i=2,#items do context.treasure[#context.treasure+1]=items[i] end
   activeBattle=context
   -- The caller first attaches the returned holder to the map. Start on the
   -- next tick so leaving the scene cannot interrupt that native callback.
   ms.d_u.delay(holder,0.05,function()
    if activeBattle~=context or main()~=parent then return end
    local director=CCDirector:sharedDirector()
    local runScene=ms.d_u.runScene
    ms.d_u.runScene=function(scene)
     context.pushed=true;director:pushScene(scene)
    end
    ms.d_event_mgr.setSpecialFightType(2)
    local ok,err=pcall(fight.actFight,ms.d_c.table_copy(marker.replay),2)
    ms.d_u.runScene=runScene
    if not ok then error(err) end
   end)
   return holder
  end
  fight.showFightEnd=function(...)
   local context=activeBattle
   if not context then return nativeFightEnd(...) end
   if context.finished then return end
   context.finished=true
   local row=context.row
   fight.g_fightUI.is_fight_end=true
   fight.getSkipFightBtn():setVisible(false)
   local parent=fight.g_fightUI.layerFightEnd
   parent:removeAllChildrenWithCleanup(true)
   local layer=CCLayerColor:create(ccc4(18,29,44,240));parent:addChild(layer,100,battleTag)
   ms.d_u.createSwallowTouchLayer(layer)
   label(layer,1,row.won and '战斗胜利 · 获得奖励' or '战斗结束 · 未获胜',0.5,0.82,32)
   label(layer,2,string.format('%d重天 · %s',row.floor,row.enemy_name or '守关敌人'),0.5,0.71,24)
   for i,reward in ipairs(row.rewards or {}) do
    local y=0.53-(i-1)*0.14
    local icon=ui.getItemIcon(reward)
    ms.d_u.setStyles(icon,{x=0.35,y=y,scale=0.10});layer:addChild(icon,3)
    local title=label(layer,10+i,ui.getItemName(reward)..'×'..reward.attach_count,0.58,y,26)
    local width=CCDirector:sharedDirector():getVisibleSize().width*0.50
    if title:getContentSize().width>width then title:setScale(width/title:getContentSize().width) end
   end
   if not row.won then label(layer,3,'本次未获得战利品，可以继续探索',0.5,0.50,24) end
   label(layer,4,'关闭后继续前进',0.5,0.24,24)
   local closed=false
   layer:addChild(ms.d_u.createMenu({x=0,y=0,{npic='v2/introUI/close1.png',spic='v2/introUI/close2.png',
    x=0.92,y=0.88,scalexx=0.1,call_back=function()
     if closed or activeBattle~=context then return end
     closed=true;activeBattle=nil
     ms.d_event_mgr.setSpecialFightType(0)
     if ms.d_loginUI then ms.d_loginUI.g_currentSence=context.sceneID end
     if main_server and main_server.change_speed then main_server.change_speed(1) end
     if ms.d_music_mgr then ms.d_music_mgr.playUIMusic() end
     if context.pushed then CCDirector:sharedDirector():popScene() end
     -- Wait for the map to re-enter before continuing its Cocos actions.
     ms.d_u.delay(context.parent,0.05,function()
      if main()~=context.parent then return end
      ms.d_u.remove(context.holder)
      if #context.treasure>0 then
       context.parent:addChild(old.showRandomPrize(context.treasure,context.callback),100)
      elseif context.callback then context.callback() end
     end)
    end}}),4)
  end
  ui.cancelSwallow=function(...)
   local result=old.cancelSwallow(...)
   -- Native addSwallow also invokes cancelSwallow at intermediate floor changes.
   if pending and not activeBattle and ui.g_self.role_data.steps==pending.local_snapshot.steps then
    local data=pending;pending=nil;sync(data);ui.showGameLayer()
    ui._localNineSkyTick()
   end
   return result
  end
  ui.showFloorTitle=function(...)
   if ui.g_self.role_data and ui.g_self.role_data.floor>9 then ui.g_self.role_data.floor=9 end
   return old.showFloorTitle(...)
  end
  ui.onGetActResult=function(data,...)
   local incoming=data.local_snapshot
   local weekChanged=incoming and meta and incoming.next_weekly_refresh~=meta.next_weekly_refresh
   if incoming then
    local changed=meta and (incoming.shop_day~=meta.shop_day or incoming.shop_revision~=meta.shop_revision)
    if changed or data.flag==1 then clearShops(data.flag==1) end
    meta=ms.d_c.table_copy(incoming)
   end
   if data.flag==1 then
    pending=nil;ui.g_self.card_list=ui.processCardList(data.local_cards or {})
    -- Old servers/replayed entry packets may still carry the last encounter.
    -- Only an actual movement event should open the mystery shop.
    data=ms.d_c.table_copy(data);data.tina_shop=nil
    if ui.clearTinaInfo then ui.clearTinaInfo() end
    ui.g_self.tinaIndex=nil
   elseif data.flag==3 and meta then
    shopVersions[data.shop_type]={day=meta.shop_day,revision=meta.shop_revision}
   end
   -- A request can leave the client just before Monday and reach the server
   -- after reset. Start native movement from the server's pre-roll coordinates.
   if data.flag==2 and data.local_before_snapshot then
    local before=data.local_before_snapshot;local current=ui.g_self.role_data
    if weekChanged or not current or current.steps~=before.steps then
     ui.g_self.role_data=ms.d_c.table_copy(before)
     ui.g_self.role_data.floor=math.min(9,ui.getTowerFloor(before.steps))
     if weekChanged and ui.clearTinaInfo then ui.clearTinaInfo() end
     ui.showGameLayer()
    end
   end
   if data.flag==2 then
    data=ms.d_c.table_copy(data)
    for _,event in ipairs(data.map_event_list or {}) do
     local row=(data.local_battles or {})[event.local_battle_index]
     if row and row.replay then
      table.insert(event.meet_rand_list,1,{local_nine_sky_battle=row})
     end
    end
    pending=data
   end
   local result=old.onGetActResult(data,...)
   if data.flag==2 then -- movement owns the snapshot until its final callback
   elseif pending and data.flag==5 then
    -- Palace purchases happen while walking is paused; preserve their new balances.
    for _,key in ipairs({'stars','credits','free_times'}) do
     ui.g_self.role_data[key]=ui.g_self.role_data[key]+data.local_snapshot[key]-pending.local_snapshot[key]
    end
    pending.local_snapshot=data.local_snapshot;pending.local_cards=data.local_cards;pending.local_top=data.local_top
    ui.g_self.card_list=ui.processCardList(data.local_cards or {});ui.showDynamicInfo()
   else sync(data) end
   ui._localNineSkyTick()
   return result
  end
  ui._localNineSkyRestore=function()
   installed=false;timerLayer=nil;pending=nil;activeBattle=nil
   fight.showFightEnd=nativeFightEnd
   for key,value in pairs(old) do ui[key]=value end
   ui._localNineSkyTick=nil;ui._localNineSkyRestore=nil
  end
 end
end
