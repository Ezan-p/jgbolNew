-- Minimal offline lifecycle fixes; retain original layouts and claim callbacks.
do
 local ms=package.loaded.ms
 local v=ms and ms.d_actNoticeUI
 if not v or not ms.d_data then return 'pending' end
 if not v._localWelfareRestore then
  local callback,meiri,showItem,fund=v.callbackGetActNoticeData,v.setMeiridata,v.showgetItem,v.createGrowthFund
  local configCallback=ms.d_data.callback_update_config
  local anniversary=v.createAnniversaryRecharge
  v.createAnniversaryRecharge=function(...)
   -- This page binds an anonymous callback that removes the activity layer
   -- before opening recharge; replace only its recharge button at creation.
   local createMenu=ms.d_u.createMenu
   ms.d_u.createMenu=function(styles,...)
    for _,style in ipairs(styles) do
     if style.npic=='v2/rechargeUI/recharge1.png' then
      style.call_back=function() ms.d_rechargeUI.show() end
      style.tag=19890
     end
    end
    return createMenu(styles,...)
   end
   local ok,result=pcall(anniversary,...)
   ms.d_u.createMenu=createMenu
   if not ok then error(result) end
   return result
  end
  v._localRefreshContent=function()
   local view=v.g_self
   local recharge=ms.d_rechargeUI
   -- Refresh an already open tab in place; never call show/navigation here.
   if not view or not view.data or not view.main_layer or not view.main_layer:getParent()
      or not view.last_press_btn_tag then return end
   if recharge and recharge._localIsOpen and recharge._localIsOpen() then return end
   if recharge and recharge._localCardSelection then return end
   v.showContent(view.main_layer,view.last_press_btn_tag)
  end
  ms.d_data.callback_update_config=function(data)
   local result=configCallback(data)
   local current=data and data.local_welfare
   if current then
    local view=v.g_self
    if view and view.data then
     view.data.all_activity=current.all_activity
     view.meiri=current.all_activity[74] or {data={isopen=false}}
    end
    if current.spring_info and ms.d_chargePresentUI then
     ms.d_chargePresentUI.updateActivityStatus({spring_info=current.spring_info})
    end
    v._localRefreshContent()
   end
   return result
  end
  v.callbackGetActNoticeData=function(data)
   -- A recharge can refresh the current tab while its parent is closing.
   -- Keep the response cached without recreating a closed activity window.
   if data and data.flag==1 and data.act_type and not data.all_activity and
      (not v.g_self.main_layer or not v.g_self.main_layer:getParent()) then
    if v.g_self.data and v.g_self.data.all_activity then v.g_self.data.all_activity[data.act_type]=data.activity_data end
    return
   end
   if data and data.flag==1 and data.all_activity then
    v.g_self.meiri=data.all_activity[74] or {data={isopen=false}}
    -- Original createLeftBtnsSlid appends the separate daily-pay entry.
    for i=#data.order_list,1,-1 do if data.order_list[i]==74 then table.remove(data.order_list,i) end end
   end
   return callback(data)
  end
  v.setMeiridata=function(data)
   v.g_self.meiri=data
   local current=v.g_self.data
   if current then
    current.all_activity[74]=data
    local exists=false
    for i=#current.order_list,1,-1 do
     if current.order_list[i]==74 then
      if exists or not (data.data and data.data.isopen) then table.remove(current.order_list,i) else exists=true end
     end
    end
    if not exists and data.data and data.data.isopen then table.insert(current.order_list,74) end
    if v.g_self.main_layer then v.showContent(v.g_self.main_layer,v.g_self.last_press_btn_tag) end
   end
  end
  v.showgetItem=function(data)
   showItem(data)
   if data and data.attach_list then ms.d_commonLayerUI.showPrizeResLayer(v.g_self.main_layer,data.attach_list) end
  end
  v.createGrowthFund=function(info,layer)
   fund(info,layer)
   local note=CCLabelTTF:create('使用传世金卡购买（45元）','Arial',14)
   note:setPosition(v.g_self.w1*0.68,v.g_self.h1*0.94)
   layer:addChild(note,100)
  end
  v._localWelfareRestore=function()
   ms.d_data.callback_update_config=configCallback
   v._localRefreshContent=nil
   v.callbackGetActNoticeData=callback;v.setMeiridata=meiri;v.showgetItem=showItem;v.createGrowthFund=fund
   v.createAnniversaryRecharge=anniversary
   v._localWelfareRestore=nil
  end
 end
end
