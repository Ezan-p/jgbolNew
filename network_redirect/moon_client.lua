-- Native recipes with weekly settlement and independent daily craft quotas.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_moonCakeUI
 if not ui or not ms.d_activityUI or not ms.d_ricePuddingUI or not ms.d_hz or not ms.d_u or not ms.d_data or not ms.d_data.createBatchUse or not ms.d_packageUI then return 'pending' end
 if not ui._localMoonRestore then
  local old={}
  for _,key in ipairs({'updateActivityStatus','canJoin','tickTime','create','cook','showNews','onGetResult'}) do old[key]=ui[key] end
  local originalStatus=ms.d_activityUI.getQiwenStatus
  ms.d_activityUI.getQiwenStatus=function(value,...)
   if value and value.local_seasonal_only then
    ui.updateActivityStatus(value.midautumn_data)
    ms.d_ricePuddingUI.updateActivityStatus(value.dragon_boat_info)
    return
   end
   return originalStatus(value,...)
  end
  local hz=ms.d_hz.gethz
  local enabled=__MOON_ENABLED__
__SEASONAL_CRAFT_HELPER__
  local originalEnd=ui.g_self.end_time
  local labels={
   mooncake1='本周每制作__MOON_BONUS_EVERY__个月饼，额外领取蟠桃×__MOON_BONUS_COUNT__',
   mooncake2='旅途、天命胜利及蟠桃会挑战均可随机获得材料',
   mooncake6='再做%d个，可领取累计奖励',
   mooncake8='累计制作月饼领好礼',
   mooncake9='本周累计制作进度'
  }
  ms.d_hz.gethz=function(key,...)
   return labels[key] or hz(key,...)
  end
  ui.updateActivityStatus=function(data,...)
   updateCraft(data)
   if data and data.local_permanent then enabled=data.local_enabled end
   local result=old.updateActivityStatus(data,...)
   originalEnd=ui.g_self.end_time
   -- The original cook callback checks this field as well as canJoin.
   ui.g_self.end_time=enabled and math.huge or 0
   ui.tickTime()
   return result
  end
  ui.canJoin=function() return enabled end
  ui.cook=function(index)
   return craftBatch(index,'moon',ui.g_moonCakeUI)
  end
  ui.onGetResult=function(data,...)
   updateCraft(data)
   return old.onGetResult(data,...)
  end
  ui.tickTime=function()
   showActivityCountdown('g_moonCakeUI')
  end
  ui.create=function(...)
   local create=ms.d_u.createByStyles
   ms.d_u.createByStyles=function(styles,...)
    local node=create(styles,...)
    if styles.pic=='v2/moonCakeUI/time.png' then node:setVisible(false) end
    return node
   end
   local ok,result=pcall(old.create,...)
   ms.d_u.createByStyles=create
   if not ok then error(result) end
   return result
  end
  ui.showNews=function(...)
   -- The old server-wide heading is baked into reward_bkg.png.
   local styles=ms.d_u.setStyles
   ms.d_u.setStyles=function(node,style,...)
    local result=styles(node,style,...)
    if style.scale==0.2 then
     local size=node:getContentSize()
     local cover=CCLayerColor:create(ccc4(127,55,14,255),size.width*0.88,size.height*0.25)
     cover:setPosition(ccp(size.width*0.06,size.height*0.72));node:addChild(cover,10)
     local title=CCLabelTTF:create('本周月饼累计制作','arial',size.height*0.16)
     title:setPosition(ccp(size.width*0.5,size.height*0.85));title:setColor(ccc3(255,221,164))
     node:addChild(title,11,91133)
    end
    return result
   end
   local ok,result=pcall(old.showNews,...)
   ms.d_u.setStyles=styles
   if not ok then error(result) end
   return result
  end
  ui._localMoonRestore=function()
   stopActivityCountdown()
   for key,value in pairs(old) do ui[key]=value end
   ui.g_self.end_time=originalEnd
   ms.d_activityUI.getQiwenStatus=originalStatus
   ms.d_hz.gethz=hz;ui._localMoonRestore=nil
  end
 end
end
