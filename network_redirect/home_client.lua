-- Offline home: retain native screens, refresh authoritative cooperation/goals.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_homeUI
 if ui and not ui._localHomeRestore then
  local oldResult,oldRest,oldActivity=ui.onGetResult,ui.getRestDay,ui.hasActivity
  local oldHCJ=ui.showHCJ
  local oldPet=ui.showPet
  local textIndex,textOriginal
  if ui.showHolePlan and debug and debug.getupvalue then
   for i=1,100 do
    local name,value=debug.getupvalue(ui.showHolePlan,i)
    if not name then break end
    if name=='gethz' then
     textIndex,textOriginal=i,value
     debug.setupvalue(ui.showHolePlan,i,function(key,...)
      if key=='home_welfare12' then return '豪华度达标即可领取，已领档位不会重复发放' end
      return value(key,...)
     end)
     break
    end
   end
  end
  ui.hasActivity=function(...)
   local config=ui.g_data and ui.g_data.config_data
   if config and config.offline_home then return true end
   local flags=config and config.activity_flag
   if flags and (flags[68] or flags[69] or flags[70] or flags[72]) then return true end
   return oldActivity(...)
  end
  ui.getRestDay=function(kind,...)
   if kind==69 or kind==70 or kind==72 then return '长期开放' end
   if kind==68 then return '每周一结算，奖励邮件领取' end
   return oldRest(kind,...)
  end
  ui.onGetResult=function(op,data,...)
   -- Native scale success refreshes its buttons inside oldResult, but only
   -- copies level/point. Install the new stage before that refresh runs.
   if op==26 and data and data.result==1 and data.upgrade_info and ui.g_data then
    ui.g_data.base_data=ui.g_data.base_data or {}
    ui.g_data.base_data.upgrade_info=data.upgrade_info
   end
   local result=oldResult(op,data,...)
   if data and data.result==1 then
    if op==5 and ui.g_data then
     for _,f in pairs(ui.g_data.friend_list or {}) do
      if f.id==data.friend_id then f.has_invited=true end
     end
     if not ui.g_read_only then
      local garden=ui.g_data.garden_data
      for index,count in pairs(data.plants_plus_time or {}) do
       if garden and garden.plant_data and garden.plant_data[index] then
        garden.plant_data[index].cur_plus_times=count
       end
      end
     end
    elseif op==24 and data.flag==2 and data.all_activity and ui.g_data then
     ui.g_data.all_activity=data.all_activity
     ui.refreshWelfare(data.act_type)
    end
   end
   return result
  end
  if oldHCJ then
   ui.showHCJ=function(...)
    local base=ui.g_data and ui.g_data.base_data
    if base and base.upgrade_info and base.upgrade_info.is_max_scale then return end
    return oldHCJ(...)
   end
  end
  if oldPet then
   ui.showPet=function(...)
    local create=ms.d_u.createMenu
    ms.d_u.createMenu=function(styles,...)
     -- Native 1205/1263 skill entry only displays the unfinished-feature tip.
     for _,button in ipairs(styles) do
      if button.npic=='v2/homeUI/pet_skill1.png' then button.visible=false end
     end
     return create(styles,...)
    end
    local ok,result=pcall(oldPet,...)
    ms.d_u.createMenu=create
    if not ok then error(result,0) end
    return result
   end
  end
  ui._localHomeRestore=function()
   ui.onGetResult=oldResult;ui.getRestDay=oldRest;ui.hasActivity=oldActivity
   ui.showHCJ=oldHCJ
   ui.showPet=oldPet
   if textIndex then debug.setupvalue(ui.showHolePlan,textIndex,textOriginal) end
   ui._localHomeRestore=nil
  end
 end
end
