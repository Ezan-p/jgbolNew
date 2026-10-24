-- Minimal offline lifecycle fixes; retain original layouts and claim callbacks.
do
 local ms=package.loaded.ms
 local v=ms and ms.d_actNoticeUI
 if not v or not ms.d_data then return 'pending' end
 if not v._localWelfareRestore then
  local callback,meiri,showItem,fund=v.callbackGetActNoticeData,v.setMeiridata,v.showgetItem,v.createGrowthFund
  v.callbackGetActNoticeData=function(data)
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
      if exists then table.remove(current.order_list,i) else exists=true end
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
   local note=CCLabelTTF:create('本地模拟购买（不扣款）','Arial',14)
   note:setPosition(v.g_self.w1*0.68,v.g_self.h1*0.94)
   layer:addChild(note,100)
  end
  v._localWelfareRestore=function()
   v.callbackGetActNoticeData=callback;v.setMeiridata=meiri;v.showgetItem=showItem;v.createGrowthFund=fund
   v._localWelfareRestore=nil
  end
 end
end
