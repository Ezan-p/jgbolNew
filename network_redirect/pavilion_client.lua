-- Native layouts; refresh detached inventory references and server-owned counts.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_destinyUI
 if not ui or not ms.d_data or not ms.d_time then return 'pending' end
 if ui._localPavilionRestore and ui._localPavilionVersion~=5 then ui._localPavilionRestore() end
 if not ui._localPavilionRestore then
  ui._localPavilionVersion=5
  local tables=__PAVILION_TABLES__
  local originalResult=ui.onGetResult
  local originalConfig=ms.d_data.callback_update_config
  local originalShow,originalGift,originalSend=ui.show,ui.showGift,ui.sendRequest
  local originalJoin=ui.canJoin
  local originalPage=ui.showPageDeatail
  local originalBag=ui.getGiftBagSprite
  ui.getGiftBagSprite=function(index,...)
   -- Slots 1-9 now match the final native catalog. The added gem package
   -- reuses equipment artwork (its native package also contains a gem).
   return originalBag(index==10 and 8 or index,...)
  end
  local pageCount=math.max(3,math.ceil(#(tables['csv_config/exchange_zone.csv'] or {})/3))
  ui.showPageDeatail=function(page,...)
   -- Native page_max serves BOTH page count and rows/page. Keep three rows
   -- while rendering, then restore the four-page navigation limit.
   ui.g_self.page_max=3
   local ok,result=pcall(originalPage,page,...)
   ui.g_self.page_max=pageCount
   for _,btn in pairs(ui.g_destinyUI.page_btns or {}) do
    if btn.setVisible then btn:setVisible(true) end
   end
   if not ok then error(result) end
   return result
  end
  local lastQuery=-100
  local function query()
   local now=ms.d_time.getTime()
   if now-lastQuery>=3 or now<lastQuery then lastQuery=now;originalSend(1) end
  end
  -- Native timers capture the old end_time and close the entire activity at
  -- zero. Keep their layout/scheduling, but read the latest server deadline.
  local function withCountdown(fn,...)
   local rest,delay,create=ms.d_time.getRestTime,ms.d_u.delay,ms.d_u.createByStyles
   local text
   ms.d_time.getRestTime=function()
    local config=ui.g_self.config or {}
    local left=math.max(0,math.floor((config.end_time or 0)-ms.d_time.getTime()))
    text=string.format('%d天%02d:%02d:%02d',math.floor(left/86400),math.floor(left/3600)%24,math.floor(left/60)%60,left%60)
    if left==0 then query() end
    return text
   end
   ms.d_u.createByStyles=function(style,...)
    if text and type(style.string)=='string' and style.string:sub(-#text)==text then
     style.string='刷新剩余：'..text;style.fontsize=22
    end
    return create(style,...)
   end
   ms.d_u.delay=function(layer,seconds,callback,...)
    return delay(layer,seconds,function(...) return withCountdown(callback,...) end,...)
   end
   local ok,result=pcall(fn,...)
   ms.d_time.getRestTime=rest;ms.d_u.delay=delay;ms.d_u.createByStyles=create
   if not ok then error(result) end
   return result
  end
  ui.show=function(...) return withCountdown(originalShow,...) end
  ui.showGift=function(...) return withCountdown(originalGift,...) end
  ui.canJoin=function(...)
   local c=ui.g_self.config
   if c and c.end_time and c.end_time>0 then
    -- The entry remains available while waiting for the next-period snapshot.
    return ms.d_time.getTime()>=c.begin_time
   end
   return originalJoin(...)
  end
  ui.sendRequest=function(flag,...)
   if flag~=1 and ui.g_self.config and ms.d_time.getTime()>=ui.g_self.config.end_time then
    query();return
   end
   return originalSend(flag,...)
  end
  local function refresh(data)
   if not data then return end
   local previous=ui.g_self.config
   if previous and (previous.begin_time~=data.begin_time or previous.end_time~=data.end_time)
      and ui.g_destinyUI.buy_layer then ui.closeBuyItemLayer() end
   ui.g_data.enter=data
   ui.g_self.config={begin_time=data.begin_time,end_time=data.end_time,had_prize=data.had_prize}
   for index,info in pairs(data.exchange_info or {}) do
    local row=ui.g_csv.shop and ui.g_csv.shop[index]
    if row then for k,v in pairs(info) do row[k]=v end end
   end
   for index,info in pairs(data.charge_info or {}) do
    local row=ui.g_csv.gift and ui.g_csv.gift[2] and ui.g_csv.gift[2][index]
    if row then for k,v in pairs(info) do row[k]=v end end
   end
   ui.g_self.money_info=ms.d_smithUI.getItemInfoByType(5,1141)
       or {count=0,csvInfo=ms.d_data.getCertainInfo(5,1141)}
   local view=ui.g_destinyUI
   if view.main_layer then
    ui.showMyMoney()
    ui.showPageDeatail(ui.g_self.cur_page or 1)
    if view.recharge_layer then ui.showRechargePage(view.recharge_layer,ui.g_self.last_recharge_index or 1) end
   end
  end
  ui.onGetResult=function(data)
   if data.flag==1 then
    -- Native initCsv caches both tables; rebuild them when re-entering.
    ui.g_csv={}
    ui.updateActivityStatus({begin_time=data.begin_time,end_time=data.end_time,had_prize=data.had_prize})
    local open=ms.d_csv.open2
    ms.d_csv.open2=function(path,...)
     if tables[path] then return tables[path] end
     return open(path,...)
    end
    local ok,result=pcall(originalResult,data)
    ms.d_csv.open2=open
    if not ok then error(result) end
    return result
   end
   if data.flag==2 and data.snapshot then
    -- Native subtracts counts after dismissing the prize animation. Refresh
    -- after that callback so the displayed count is not subtracted twice.
    local prize=ms.d_commonLayerUI.showPrizeResLayer
    ms.d_commonLayerUI.showPrizeResLayer=function(parent,list,callback,...)
     return prize(parent,list,function()
      if callback then callback() end
      refresh(data.snapshot)
     end,...)
    end
    local ok,result=pcall(originalResult,data)
    ms.d_commonLayerUI.showPrizeResLayer=prize
    if not ok then error(result) end
    if not ui.g_destinyUI.buy_layer then refresh(data.snapshot) end
    return result
   end
   local result=originalResult(data)
   if data.snapshot then refresh(data.snapshot) end
   return result
  end
  ms.d_data.callback_update_config=function(data)
   local result=originalConfig(data)
   if data and data.local_pavilion then
    refresh(data.local_pavilion.data)
    ui.updateActivityStatus(data.local_pavilion.status)
   end
   return result
  end
  ui._localPavilionRestore=function()
   ui.onGetResult=originalResult;ms.d_data.callback_update_config=originalConfig
   ui.show=originalShow;ui.showGift=originalGift;ui.sendRequest=originalSend
   ui.canJoin=originalJoin
   ui.showPageDeatail=originalPage
   ui.getGiftBagSprite=originalBag
   ui._localPavilionRestore=nil
   ui._localPavilionVersion=nil
  end
 end
end
