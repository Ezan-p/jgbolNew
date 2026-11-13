-- Native abyssUI L1887-1890 compares remaining >= maximum, blocking 5/5.
-- Keep the native panel and counter; let the server settle the current day.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_abyssUI
 if not ui or not ui.showBossLayer or not ui.sendRequest then return 'pending' end
 if not ui._localBossRestore then
  local original=ui.showBossLayer
  local function challenge()
   local info=ui.g_data and ui.g_data.boss and ui.g_data.boss.specter_info
   if not info then ui.sendRequest(16,{});return end
   if info.complete then
    ms.d_info.show('九幽八十一层已全部通关，可继续挂机、炼药和兑换。');return
   end
   -- Do not reject a cached 0/5 here: the server may have crossed midnight.
   ms.d_lineupUI.getCharacterCSVConfig('specter_boss')
   ms.d_lineupUI.saveLastFightLevel()
   ui.sendRequest(6,{})
  end
  ui.showBossLayer=function(...)
   local create=ms.d_u.createMenu
   ms.d_u.createMenu=function(config,...)
    for _,row in ipairs(config) do
     if row.npic=='v2/abyssUI/challenge1.png' then row.call_back=challenge end
    end
    return create(config,...)
   end
   local ok,result=pcall(original,...)
   ms.d_u.createMenu=create
   if not ok then error(result,0) end
   return result
  end
  ui._localBossRestore=function() ui.showBossLayer=original;ui._localBossRestore=nil end
 end
end

-- Native showNumberGuess L3704 counts digits in min_num (0 initially), so
-- pressNum rejects the second digit. Its keypad/reset closures share numCount.
-- Size that input from the largest allowed integer; keep the native rendering,
-- reset button, range checks and request callback.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_abyssUI
 if ui and ui.showNumberGuess and not ui._localAbyssNumberRestore then
  if not debug or not debug.getupvalue or not debug.setupvalue then return 'pending' end
  local original=ui.showNumberGuess
  ui.showNumberGuess=function(...)
   local data=ui.g_data and ui.g_data.random
   local maximum=data and tonumber(data.max_num) or 40
   local digits=math.max(2,#tostring(math.ceil(maximum)-1))
   local create=ms.d_u.createMenu
   local initialized=false
   ms.d_u.createMenu=function(config,...)
    for _,row in ipairs(config) do
     if not initialized and row.npic=='v2/abyssUI/randomEvent/num_btn1.png' then
      local callback=row.call_back
      local countIndex,reset
      for i=1,64 do
       local name,value=debug.getupvalue(callback,i)
       if not name then break end
       if name=='numCount' then countIndex=i end
       if name=='pressReenter' then reset=value end
      end
      if countIndex and reset then
       debug.setupvalue(callback,countIndex,digits)
       reset()
       initialized=true
      end
     end
    end
    return create(config,...)
   end
   local ok,result=pcall(original,...)
   ms.d_u.createMenu=create
   if not ok then error(result,0) end
   return result
  end
  ui._localAbyssNumberRestore=function()
   ui.showNumberGuess=original;ui._localAbyssNumberRestore=nil
  end
 end
end

-- Native showChallengeSuccess looks up every reward as an item (L2393).
-- Silver has attach_type=0, so it throws before installing the close touch
-- handler (L2407). Give the delayed renderer its own currency-aware helpers;
-- nested Lua 5.1 closures retain this environment after the outer call returns.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_abyssUI
 if ui and ui.showChallengeSuccess and not ui._localAbyssSuccessRestore then
  local original=ui.showChallengeSuccess
  ui.showChallengeSuccess=function(...)
   local rewardType
   local data=setmetatable({
    getCertainSmallSprite=function(typ,...)
     rewardType=typ
     return ms.d_data.getCertainSmallSprite(typ,...)
    end,
    getItemName=function(tid,...)
     if rewardType==12 then return '银币' end
     if rewardType==11 then return '元宝' end
     return ms.d_data.getItemName(tid,...)
    end
   },{__index=ms.d_data})
   local env=getfenv(original)
   local proxy=setmetatable({d_data=data},{__index=ms})
   setfenv(original,setmetatable({d_ms=proxy},{__index=env,__newindex=env}))
   local ok,result=pcall(original,...)
   setfenv(original,env)
   if not ok then error(result,0) end
   return result
  end
  ui._localAbyssSuccessRestore=function()
   ui.showChallengeSuccess=original;ui._localAbyssSuccessRestore=nil
  end
 end
end

-- Native getShopItem L1655-1661 only batches slots 5/6, capped at 15.
-- Keep its card layout and native quantity picker, enable all six slots up to 100.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_abyssUI
 if ui and ui.getShopItem and not ui._localAbyssShopBatchRestore then
  local original=ui.getShopItem
  local knownShop,unitCounts
  ui.getShopItem=function(item,index,...)
   local shop=ui.g_data and ui.g_data.shop
   if shop~=knownShop then
    knownShop=shop;unitCounts={}
    for i,row in pairs(shop and shop.shop_list or {}) do unitCounts[i]=row.attach_count end
   end
   unitCounts=unitCounts or {}
   unitCounts[index]=unitCounts[index] or item.attach_count
   -- Purchase replies contain the total received quantity. The native renderer
   -- stores that reply as a shop row; display the original per-portion quantity.
   local card={}
   for key,value in pairs(item) do card[key]=value end
   card.attach_count=unitCounts[index]
   local day,revision=shop and shop.shop_day,shop and shop.shop_revision
   local function maximum()
    local current=ui.g_data and ui.g_data.shop
    local row=current and current.shop_list and current.shop_list[index]
    if not current or current.shop_day~=day or current.shop_revision~=revision or
       not row or row.attach_type~=card.attach_type then return 0,'商店已刷新，请重新打开商店。' end
    local remaining=math.max(0,math.floor(tonumber(row.buy_times) or 0))
    if remaining==0 then return 0,'该商品今日兑换次数已用尽。' end
    local info=ui.g_data.hook and ui.g_data.hook.specter_data
    local balance=math.max(0,tonumber(info and info.crystal_count) or 0)
    local price=tonumber(row.crystals) or 0
    if price<=0 then return 0,'商品价格无效，请重新打开商店。' end
    local count=math.min(100,remaining,math.floor(balance/price))
    if count==0 then return 0,'魂晶不足。' end
    return count
   end
   local function confirm(count)
    local limit,message=maximum()
    if type(count)~='number' or count~=math.floor(count) or count<1 or count>limit then
     ms.d_info.show(message or '兑换数量已变化，请重新选择。');return
    end
    ui.sendRequest(12,{index=index,count=count,shop_day=day,shop_revision=revision})
   end
   local function buy()
    local limit,message=maximum()
    if limit==0 then ms.d_info.show(message);return end
    if limit==1 then confirm(1);return end
    ms.d_data.createBatchUse(ui.g_abyssUI.shop_layer,{min=1,max=limit,defaultCount=1},confirm)
   end
   local create=ms.d_tableView.createTableViewMenu
   ms.d_tableView.createTableViewMenu=function(config,...)
    for _,row in ipairs(config.menuItems or {}) do
     if row.npic=='v2/soulHuntUI/btn_buy1.png' then row.tapHandler=buy end
    end
    return create(config,...)
   end
   local ok,result=pcall(original,card,index,...)
   ms.d_tableView.createTableViewMenu=create
   if not ok then error(result,0) end
   return result
  end
  ui._localAbyssShopBatchRestore=function()
   ui.getShopItem=original;ui._localAbyssShopBatchRestore=nil
  end
 end
end

-- The native random-event redraw creates a fresh empty button upvalue when
-- reusing its existing layer. A thief response then indexes btns[2] (nil).
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_abyssUI
 if ui and ui.showRandomEvent and not ui._localAbyssEventsRestore then
  local original=ui.showRandomEvent
  ui.showRandomEvent=function(parent,...)
   local data=ui.g_data and ui.g_data.random
   local layer=parent or (ui.g_abyssUI and ui.g_abyssUI.hook_layer)
   if data and data.event_type==4 and data.op_type~=2 and layer and ui.tagDef then
    local old=layer:getChildByTag(ui.tagDef.random_layer)
    if old then layer:removeChild(old,true) end
   end
   return original(parent,...)
  end
  ui._localAbyssEventsRestore=function() ui.showRandomEvent=original;ui._localAbyssEventsRestore=nil end
 end
 local drug=ms and ms.d_yaoshendianUI
 if drug and drug.getBitFromInt and not drug._localAbyssDrugBitsRestore then
  local original=drug.getBitFromInt
  drug.getBitFromInt=function(value,...)
   return original((tonumber(value) or 0)%4294967296,...)
  end
  drug._localAbyssDrugBitsRestore=function() drug.getBitFromInt=original;drug._localAbyssDrugBitsRestore=nil end
 end
end
