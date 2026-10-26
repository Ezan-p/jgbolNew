-- Native layouts; refresh detached inventory references and server-owned counts.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_destinyUI
 if not ui or not ms.d_data then return 'pending' end
 if not ui._localPavilionRestore then
  local tables=__PAVILION_TABLES__
  local originalResult=ui.onGetResult
  local originalConfig=ms.d_data.callback_update_config
  local function refresh(data)
   if not data then return end
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
   ui._localPavilionRestore=nil
  end
 end
end
