-- Keep original widgets, routes and animations. Reconcile server-only rewards
-- after the final movement callback, never before the native walk consumes it.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_towerUI
 if not ui or not ms.d_c then return "pending" end
 if not ui._localNineSkyRestore then
  local original=ui.onGetActResult
  local cancel=ui.cancelSwallow
  local title=ui.showFloorTitle
  local pending=nil
  local function sync(data)
   if not data or not data.local_snapshot then return end
   ui.g_self.role_data=ms.d_c.table_copy(data.local_snapshot)
   ui.g_self.role_data.floor=ui.getTowerFloor(ui.g_self.role_data.steps)
   ui.g_self.card_list=ui.processCardList(data.local_cards or {})
   ui.g_self.top_data=data.local_top
   if ui.g_towerUI.main_layer then
    ui.showDynamicInfo();ui.showTokenCount();ui.showTopPlayer()
   end
  end
  ui.cancelSwallow=function(...)
   local result=cancel(...)
   -- Native addSwallow also calls cancelSwallow at each floor transition.
   -- Only the final accumulated distance identifies completion of this batch.
   if pending and ui.g_self.role_data.steps==pending.local_snapshot.steps then
    local data=pending;pending=nil;sync(data)
    -- Also redraw coordinates after the ninth-sky sentinel wrap.
    ui.showGameLayer()
   end
   return result
  end
  ui.showFloorTitle=function(...)
   -- No tenth-floor resource exists; the ninth sentinel reuses sky9.
   if ui.g_self.role_data and ui.g_self.role_data.floor>9 then ui.g_self.role_data.floor=9 end
   return title(...)
  end
  ui.onGetActResult=function(data,...)
   if data.flag==1 then
    pending=nil
    -- A new season must discard stale prices, card selectors and palace widgets.
    ui.g_self.shop_data={};ui.g_self.role_shop_data={}
    ui.g_self.card_list=ui.processCardList(data.local_cards or {})
   end
   local result=original(data,...)
   if data.flag==2 then
    pending=data
   elseif pending and data.flag==5 then
    -- Palace purchases can arrive while ten-roll animation is paused in a shop.
    for _,k in ipairs({'stars','credits','free_times'}) do
     ui.g_self.role_data[k]=ui.g_self.role_data[k]+data.local_snapshot[k]-pending.local_snapshot[k]
    end
    pending.local_snapshot=data.local_snapshot;pending.local_cards=data.local_cards
    pending.local_top=data.local_top
    ui.g_self.card_list=ui.processCardList(data.local_cards or {})
    ui.showDynamicInfo()
   else sync(data) end
   return result
  end
  ui._localNineSkyRestore=function()
   ui.onGetActResult=original;ui.cancelSwallow=cancel;ui.showFloorTitle=title
   ui._localNineSkyRestore=nil;pending=nil
  end
 end
end
