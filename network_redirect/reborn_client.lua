-- The installed release_w ascension list also sorts by fate_rebullding_state.
-- The preserved 3.87 protocol has no such field: absent means not activated.
-- Normalize only missing client fields, before the original filter and sort.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_ascensionUI
 if not ui or type(ui.getAscCorts)~='function' then return 'pending' end
 if not ui._localRebornRestore then
  local original=ui.getAscCorts
  ui.getAscCorts=function(...)
   for _,c in pairs(ms.d_lineupUI.g_characterInfo or {}) do
    if c.fate_rebullding_state==nil then c.fate_rebullding_state=0 end
   end
   return original(...)
  end
  ui._localRebornRestore=function()
   ui.getAscCorts=original
   ui._localRebornRestore=nil
  end
 end
end

-- Keep the target realm and eligibility current after construction/success.
-- The original constructor caps next_reborn_level at 3; its refresh already
-- renders fourth-realm conditions, but leaves these cached fields stale.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_roleRebornUI
 if not ui or type(ui.update_rightpanel_info)~='function' or
    type(ui.sendRebornRequest)~='function' then return 'pending' end
 if not ui._localRealmRestore then
  local refresh,send,upgrade=ui.update_rightpanel_info,ui.sendRebornRequest,ui.reborn_update_func
  local function full()
   if (ms.d_mainUI.g_playerInfo.reborn_layer or 0)<4 then return false end
   ui.g_can_reborn=false
   ms.d_info.show(ms.d_hz.gethz('reborn_on_limit'),2,0.6)
   return true
  end
  ui.update_rightpanel_info=function(layer,...)
   local player=ms.d_mainUI.g_playerInfo
   local target=math.min((player.reborn_layer or 0)+1,4)
   ui.next_reborn_level=target
   ui.g_reborn_condition_next=ui.g_reborn_condition[target]
   local result=refresh(layer,...)
   local cond=ui.g_reborn_condition_next.condiction
   local can=(player.reborn_layer or 0)<4 and player.level>=cond.need_role_level and
             (player.maxlayer_reborn_count or 0)>=cond.reborn_count
   for _,item in ipairs(cond.consume_list) do
    if ms.d_data.getItemCountByType(item.object_type,item.attach_type)<item.attach_count then can=false end
   end
   ui.g_can_reborn=can
   return result
  end
  ui.sendRebornRequest=function(...)
   if full() then return end
   return send(...)
  end
  if type(upgrade)=='function' then
   ui.reborn_update_func=function(...)
    if full() then return end
    return upgrade(...)
   end
  end
  ui._localRealmRestore=function()
   ui.update_rightpanel_info,ui.sendRebornRequest,ui.reborn_update_func=refresh,send,upgrade
   ui._localRealmRestore=nil
  end
 end
end
