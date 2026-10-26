-- Keep the shipped barrel, bun animations and ten-second click game.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_eatBunUI
 if not ui then return 'pending' end
 if not ui._localFeedRestore then
  local tiers=__FEED_REWARD_TIERS__
  local maxCount=__FEED_MAX_COUNT__
  local old={}
  for _,name in ipairs({'show','pressBegin','createCountDownLayer','checkCanFeedNow',
      'pressEatBun','count_down','sendResult','pressClose','feedOk','callbackFeedRet'}) do old[name]=ui[name] end
  local epoch=0
  local function invalidate()
   epoch=epoch+1
   local s=ui.g_self
   s._feedPhase='idle'
   if s.label_time_count_down then s.label_time_count_down:stopAllActions() end
  end
  local function hint()
   local s=ui.g_self
   if not s._feedTierLabel then return end
   if s.press_count==0 then s._feedTierLabel:setString('点击木桶开始，10秒内连续点击包子');return end
   local index,strength=0,0
   for i,row in ipairs(tiers) do
    if s.press_count>=row.min_count then index=i;strength=row.strength end
   end
   local capped=s.press_count>=maxCount and '（计分上限）' or ''
   s._feedTierLabel:setString('连击 '..s.press_count..' · 第'..index..'档 '..strength..'体力'..capped)
  end
  -- The wire/activity menu uses 1 for available. These two old functions
  -- instead test nil/truthiness. Normalize only during those calls.
  local function withNativeFlags(fn,...)
   local s=ui.g_self;local wire=s.feed_list;local flags={}
   for i=1,2 do if type(wire[i])=='number' and wire[i]>1 then flags[i]=wire[i] end end
   s.feed_list=flags
   local ok,result=pcall(fn,...)
   s.feed_list=wire
   if not ok then error(result) end
   return result
  end
  ui.show=function(...)
   invalidate()
   local s=ui.g_self
   s.feed_list={};s.in_time_act=0;s.enable_act=0;s.last_server_time=0
   s.press_count=0;s.time_left=10;s._feedTierLabel=nil
   return old.show(...)
  end
  ui.checkCanFeedNow=function(...)
   local s=ui.g_self
   s.enable_act=0
   for i=1,2 do
    local got=s['got'..i]
    if got then got:setVisible(type(s.feed_list[i])=='number' and s.feed_list[i]>1) end
   end
   return withNativeFlags(old.checkCanFeedNow,...)
  end
  ui.pressBegin=function(...)
   if ui.g_self._feedPhase~='idle' then return end
   return withNativeFlags(old.pressBegin,...)
  end
  ui.createCountDownLayer=function(...)
   invalidate()
   local result=old.createCountDownLayer(...)
   local s=ui.g_self;s._feedPhase='ready'
   s._feedTierLabel=ms.d_u.createByStyle({type='label',font='arial',fontsize=22,x=0.62,y=0.74,string=''})
   s.countDownlayer:addChild(s._feedTierLabel,30);hint()
   return result
  end
  ui.count_down=function()
   local s=ui.g_self
   if s._feedPhase~='playing' then return end
   -- A callback from a closed/previous round must never submit the new one.
   local token=epoch;local delay=ms.d_u.delay
   ms.d_u.delay=function(node,seconds,callback)
    return delay(node,seconds,function() if token==epoch then callback() end end)
   end
   local ok,result=pcall(old.count_down)
   ms.d_u.delay=delay
   if not ok then error(result) end
   if s.time_left<=0 then s._feedPhase='finished' end
   return result
  end
  ui.pressEatBun=function()
   local s=ui.g_self
   if s._feedPhase=='ready' then s._feedPhase='playing'
   elseif s._feedPhase~='playing' then return end
   if s.press_count>0 and ms.d_time.getTime()-s.time_begin_sec>=10 then
    ui.count_down();return
   end
   if s.press_count>=maxCount then return end
   local result=old.pressEatBun();hint();return result
  end
  ui.sendResult=function()
   local s=ui.g_self
   if s._feedPhase~='finished' or s.press_count<=0 then return end
   s._feedPhase='submitted'
   return old.sendResult()
  end
  ui.feedOk=function(message)
   invalidate()
   local result=old.feedOk(message)
   local s=ui.g_self;s._feedTierLabel=nil;s.label_time_count_down=nil
   s.countDownlayer=nil
   if s.menuTable and s.menuTable[2] then
    s.menuTable[2]:setVisible(true);s.menuTable[2]:setEnabled(true)
   end
   return result
  end
  ui.callbackFeedRet=function(message)
   local result=old.callbackFeedRet(message)
   if message.personal_best_strength and ui.g_self.g_parent_layer
       and ui.g_self.g_parent_layer:getChildByTag(ui.g_eatBun_tag) then
    ui.g_self.self_feed_strength=message.personal_best_strength
    ui.setFeedChampion()
   end
   return result
  end
  ui.pressClose=function(...)
   invalidate();ui.g_self.label_time_count_down=nil;ui.g_self._feedTierLabel=nil
   return old.pressClose(...)
  end
  ui._localFeedRestore=function()
   invalidate()
   for name,fn in pairs(old) do ui[name]=fn end
   ui._localFeedRestore=nil
  end
 end
end
