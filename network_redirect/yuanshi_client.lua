-- Restore the shipped but unbound portrait action and stale caches [B].
-- Keep native art, five gift dialogs, shop and 1334 request contracts [A].
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_twoYearsCelebrateUI
 if not ui or not ms.d_activityUI then return 'pending' end
 if not ui._localYuanshiRestore then
  local act=ms.d_activityUI
  local originalNews=ui.showNews
  local originalResult,originalPray=ui.onGetResult,ui.pray
  local originalStatus,originalConfig=act.getQiwenStatus,ms.d_data.callback_update_config
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
   local data=ui.g_self and ui.g_self[0]
   if data and data.cur_progress>=100 and not data.claimed then return ui.getChar() end
   return originalPray(...)
  end
  ui.onGetResult=function(data)
   local s=ui.g_self
   -- Original callback copies only progress/free or gift_list, and buy() reads
   -- slot 3 even after updateShopNews renders slot 4. Refresh both caches first.
   if data.flag~=0 and s[0] then
    for _,key in ipairs({'claimed','wish_times','gift_list','is_today_charge','cur_progress','free_times','gift_config'}) do
     if data[key]~=nil then s[0][key]=data[key] end
    end
   end
   if data.flag==4 and s[3] then s[3].shop_config=data.shop_config end
   return originalResult(data)
  end
  ui._localYuanshiRestore=function()
   ui.showNews=originalNews
   act.getQiwenStatus=originalStatus;ms.d_data.callback_update_config=originalConfig
   ui.onGetResult=originalResult;ui.pray=originalPray;ui._localYuanshiRestore=nil
  end
 end
end
