-- Restore the shipped but unbound portrait action and stale caches [B].
-- Keep native art, five gift dialogs, shop and 1334 request contracts [A].
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_twoYearsCelebrateUI
 if not ui or not ms.d_activityUI or not ms.d_time then return 'pending' end
 if ui._localYuanshiRestore and ui._localYuanshiVersion~=2 then ui._localYuanshiRestore() end
 if not ui._localYuanshiRestore then
  ui._localYuanshiVersion=2
  local act=ms.d_activityUI
  local originalNews=ui.showNews
  local originalResult,originalPray=ui.onGetResult,ui.pray
  local originalStatus,originalConfig=act.getQiwenStatus,ms.d_data.callback_update_config
  local originalTick,originalFrame,originalJoin=ui.tickTime,ui.createMainFrame,ui.canJoin
  local actions={}
  local lastQuery=-100
  local function config()
   local c=ms.d_data.g_new_config[24]
   return c and c.yuanshi_info or {}
  end
  local function query()
   local now=ms.d_time.getTime()
   if now-lastQuery>=3 or now<lastQuery then
    lastQuery=now
    ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_yuanshi_activity,{flag=0,index=0})
   end
  end
  local function stale()
   local data=ui.g_self and ui.g_self[0]
   if data and data.end_time and ms.d_time.getTime()>=data.end_time then query();return true end
   return false
  end
  ui.canJoin=function(...)
   local c=config()
   if c.permanent then return (c.end_time or 0)>0 and ms.d_time.getTime()>=c.begin_time end
   return originalJoin(...)
  end
  ui.createMainFrame=function(...)
   local create=ms.d_u.createByStyles
   ms.d_u.createByStyles=function(style,...)
    if style.pic=='v2/moonCakeUI/time.png' then
     style.pic=nil;style.type='label';style.string='距下次刷新';style.font='arial';style.fontsize=22
    end
    return create(style,...)
   end
   local ok,result=pcall(originalFrame,...)
   ms.d_u.createByStyles=create
   if not ok then error(result) end
   return result
  end
  ui.tickTime=function()
   local s=ui.g_self;local layer=s and s.main_layer
   if not layer then return end
   local c=config()
   if not c.permanent then return originalTick() end
   local left=math.max(0,math.floor((c.refresh_time or c.end_time or 0)-ms.d_time.getTime()))
   layer:removeChildByTag(s.timeTag,true)
   local label=ms.d_u.createByStyles({type='label',font='arial',fontsize=20,x=0.13,
    y=ui.my+ui.h*4.8,anchor={0.5,0.5},color={255,255,255},
    string=string.format('%d天%02d:%02d:%02d',math.floor(left/86400),math.floor(left/3600)%24,math.floor(left/60)%60,left%60)})
   layer:addChild(label,1,s.timeTag)
   if left==0 then query() else stale() end
   ms.d_u.delay(layer,1,ui.tickTime)
  end
  local claimTag=746002
  act.getQiwenStatus=function(data)
   if data.yuanshi_info then
    local config=ms.d_data.g_new_config
    config[24]=config[24] or {};config[24].yuanshi_info=data.yuanshi_info
   end
   return originalStatus(data)
  end
  ms.d_data.callback_update_config=function(data)
   local result=originalConfig(data)
   if data and data.local_yuanshi and act.g_currentActivity==46
       and ui.g_self and ui.g_self.main_layer then
    ui.onGetResult(data.local_yuanshi)
   end
   return result
  end
  ui.showNews=function(...)
   local result=originalNews(...)
   local s=ui.g_self;local data=s and s[0];local layer=s and s.main_layer
   if layer then
    layer:removeChildByTag(claimTag,true)
    if data and data.cur_progress>=100 and not data.claimed then
     -- Native getChar exists, but the shipped showNews never binds it.
     local normal=CCSprite:create('v2/twoYearsCelebrateUI/char.png')
     local selected=CCSprite:create('v2/twoYearsCelebrateUI/char.png')
     local item=CCMenuItemSprite:create(normal,selected)
     item:registerScriptTapHandler(ui.getChar)
     local menu=CCMenu:createWithItem(item);ms.d_u.setStyles(menu,{x=0.5,y=0.5})
     layer:addChild(menu,9,claimTag)
     local label=CCLabelTTF:create('点击人物领取元始天尊','arial',22)
     label:setColor(ccc3(255,215,100))
     label:setPosition(normal:getContentSize().width/2,0);normal:addChild(label)
    end
   end
   return result
  end
  ui.pray=function(...)
   if stale() then return end
   local data=ui.g_self and ui.g_self[0]
   if data and data.cur_progress>=100 and not data.claimed then return ui.getChar() end
   return originalPray(...)
  end
  for _,name in ipairs({'getChar','buy','openGiftPackEnsure','createShop','openGiftPack','showGiftDetail'}) do
   local original=ui[name];actions[name]=original
   ui[name]=function(...)
    if stale() then return end
    return original(...)
   end
  end
  ui.onGetResult=function(data)
   local s=ui.g_self
   local changed=s[0] and data.begin_time and s[0].begin_time~=data.begin_time
   if data.begin_time and data.end_time then
    local common=ms.d_data.g_new_config
    common[24]=common[24] or {}
    common[24].yuanshi_info={begin_time=data.begin_time,end_time=data.end_time,
     permanent=data.permanent,refresh_time=data.refresh_time}
   end
   -- Original callback copies only progress/free or gift_list, and buy() reads
   -- slot 3 even after updateShopNews renders slot 4. Refresh both caches first.
   if data.flag~=0 and s[0] then
    for _,key in ipairs({'claimed','wish_times','gift_list','is_today_charge','cur_progress','free_times','gift_config',
        'begin_time','end_time','permanent','refresh_time'}) do
     if data[key]~=nil then s[0][key]=data[key] end
    end
   end
   if data.flag==4 and s[3] then s[3].shop_config=data.shop_config end
   local result=originalResult(data)
   if changed then
    if s.shoplayer then ui.closeShop() end
    s[3]=nil;s[4]=nil
    if s.main_layer then s.main_layer:removeChildByTag(s.detailTag,true);ui.showNews() end
   end
   return result
  end
  ui._localYuanshiRestore=function()
   ui.showNews=originalNews
   act.getQiwenStatus=originalStatus;ms.d_data.callback_update_config=originalConfig
   ui.onGetResult=originalResult;ui.pray=originalPray;ui._localYuanshiRestore=nil
   ui.tickTime=originalTick;ui.createMainFrame=originalFrame;ui.canJoin=originalJoin
   for name,original in pairs(actions) do ui[name]=original end
   ui._localYuanshiVersion=nil
  end
 end
end
