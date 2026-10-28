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

-- Permanent, once-per-role growth plan. Keep the original art and reward callback.
do
 local ms=package.loaded.ms
 local v=ms and ms.d_actNoticeUI
 if v and v.createUpgradeRole and not v._localGrowthRestore then
  local original=v.createUpgradeRole
  v.createUpgradeRole=function(info,layer)
   if not info.permanent then return original(info,layer) end
   local w,h=v.g_self.w1,v.g_self.h1
   local u=ms.d_u
   local create,menu,leftTime=u.createByStyle,u.createMenu,v.getLeftTimeTink
   local level=tonumber(info.role_info.level) or 0
   local taken=info.had_taken_gift==true
   local eligible=not taken and level>=info.prize_list[1].min_level
   local amount=0
   for _,row in ipairs(info.prize_list) do
    if level>=row.min_level then amount=row.attach_list[1].attach_count end
   end
   -- Scoped hooks affect only this synchronous native page construction.
   u.createByStyle=function(style,...)
    if style.pic and string.find(style.pic,'v2/actNoticeUI/jdt',1,true)==1 then return CCNode:create() end
    if style.type=='label' and type(style.string)=='string' then
     if string.match(style.string,'^%d+级$') then return CCNode:create() end
     if string.find(style.string,'玩家当前等级',1,true) then
      style.y=0.5-h*0.28;style.fontsize=20;style.color={240,200,100}
     end
    end
    if style.y and math.abs(style.y-(0.5-h*0.06))<0.00001 then style.y=0.5-h*0.092 end
    return create(style,...)
   end
   v.getLeftTimeTink=function() return '活动剩余时间：永久' end
   u.createMenu=function(styles,items,...)
    for _,style in ipairs(styles) do
     if style.npic=='v2/actNoticeUI/get1.png' then
      local send=style.call_back
      local armed=false
      style.call_back=function(...)
       if not eligible then return end
       -- Require a deliberate second tap below the maximum tier.
       if level<info.prize_list[#info.prize_list].min_level and not armed then
        armed=true
        ms.d_info.show('本次领取'..amount..'元宝后无法再领更高档。确认领取请再次点击；也可升级后再领。')
        return
       end
       return send(...)
      end
     end
    end
    local result=menu(styles,items,...)
    if items and items[1] and not eligible then u.grayMenuItem(items[1]);items[1]:setEnabled(false) end
    return result
   end
   local ok,err=pcall(original,info,layer)
   u.createByStyle,u.createMenu,v.getLeftTimeTink=create,menu,leftTime
   if not ok then error(err) end
   local function label(text,x,y,size,color)
    layer:addChild(create({type='label',string=text,x=x,y=y,fontsize=size,color=color or {240,200,100}}),30)
   end
   local x,y,width=0.5-w*0.10,0.5-h*0.20,w*0.28
   local maxLevel=info.prize_list[#info.prize_list].min_level
   layer:addChild(create({pic='v2/actNoticeUI/jdt2.png',x=x,y=y,anchor={0,0.5},scaleX=width}),10)
   local progress=math.max(0,math.min(1,level/maxLevel))
   if progress>0 then
    layer:addChild(create({pic='v2/actNoticeUI/jdt_full.png',x=x,y=y,anchor={0,0.5},scaleX=width*progress}),11)
   end
   for _,row in ipairs(info.prize_list) do
    label(row.min_level..'级',x+width*row.min_level/maxLevel,y-h*0.035,14)
   end
   label('仅领取当前最高档一次，不累加',0.5-w*0.005,0.5-h*0.33,16)
   label(taken and '已领取 · 永久不可重复' or eligible and '当前可领取 '..amount..' 元宝' or '达到10级后可领取',
    0.5+w*0.34,0.5-h*0.31,16)
  end
  v._localGrowthRestore=function() v.createUpgradeRole=original;v._localGrowthRestore=nil end
 end
end

-- The seven retained welfare pages have no deadline or daily exchange reset.
do
 local ms=package.loaded.ms
 local v=ms and ms.d_actNoticeUI
 if v and not v._localPermanentWelfareRestore then
  local originals={}
  local pages={createFirstChargeDouble=20,createGrowthFund=22,createnewCharge=23,
   createLoginPrize=16,createCarnival=21,createExchange=32}
  for name,kind in pairs(pages) do
   local original=v[name]
   originals[name]=original
   v[name]=function(info,layer)
    if not info.permanent then return original(info,layer) end
    -- Native recharge and exchange compare numeric deadlines in button callbacks.
    -- Infinity exists only in this client-side view copy, never in wire/save data.
    local view={};for k,value in pairs(info) do view[k]=value end
    view.end_time=math.huge;view.flush_time=math.huge
    if kind==23 then
     view.prize_list={};for k,value in pairs(info.prize_list) do view.prize_list[k]=value end
     view.prize_list.end_time=math.huge
    end
    local u,t=ms.d_u,ms.d_time
    local left,rest,delay=v.getLeftTimeTink,t.getRestTime,u.delay
    local gethz=ms.d_hz.gethz
    ms.d_hz.gethz=function(key,...)
     if kind==32 and key=='exchange1' then return '每种奖励仅可兑换一次，已兑换项目不再刷新' end
     return gethz(key,...)
    end
    v.getLeftTimeTink=function() return '活动剩余时间：永久' end
    t.getRestTime=function(deadline,...)
     if deadline==math.huge then return '永久' end
     return rest(deadline,...)
    end
    u.delay=function(node,seconds,callback,...)
     -- Exchange's first tick paints the permanent label; no refresh timer follows.
     if kind==32 and node==layer and seconds==1 then return end
     return delay(node,seconds,callback,...)
    end
    local ok,result=pcall(original,view,layer)
    v.getLeftTimeTink,t.getRestTime,u.delay=left,rest,delay
    ms.d_hz.gethz=gethz
    if not ok then error(result) end
    return result
   end
  end
  v._localPermanentWelfareRestore=function()
   for name,original in pairs(originals) do v[name]=original end
   v._localPermanentWelfareRestore=nil
  end
 end
end
