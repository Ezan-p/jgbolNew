-- Retain the native daily panel, chest previews and claim callbacks.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_checkinUI
 if not ui or not ms.d_u or not ms.d_hz then return 'pending' end
 if not ui._localDailyRestore then
  local show,result=ui.showDaily,ui.onGetResult
  local originalTip=ms.d_hz.gethz('checkin_tink4')
  ui.showDaily=function(...)
   local create=ms.d_u.createByStyle
   local rows=ui.g_day and ui.g_day.data and ui.g_day.data.point_data or {}
   local count=#rows
   ms.d_u.createByStyle=function(style,...)
    local copy
    if style.type=='label' and style.string==originalTip then
     copy={};for k,v in pairs(style) do copy[k]=v end
     copy.string='每日完成任务获得活跃值，达到指定值可领取奖励。活跃值及礼包每日0点（北京时间）重置，点击礼包查看奖励。'
    elseif count>9 and style.type=='label' and style.fontsize==22
        and type(style.x)=='number' and type(style.y)=='number'
        and (math.abs(style.x-0.18)<0.0001 or math.abs(style.x-0.484)<0.0001) then
     -- Native rows start at .6188 with a .0528 step. Fit all rows into
     -- the original nine-row height, leaving the chests on the right intact.
     local index=(0.6188-style.y)/0.0528
     if index>=-0.0001 and index<count-0.9999 then
      copy={};for k,v in pairs(style) do copy[k]=v end
      copy.y=0.6188-index*(0.0528*8/(count-1))
     end
    end
    return create(copy or style,...)
   end
   local ok,value=pcall(show,...)
   ms.d_u.createByStyle=create
   if not ok then error(value) end
   return value
  end
  ui.onGetResult=function(data)
   local value=result(data)
   if data.id==3 and data.local_day then
    local current=ui.g_day and ui.g_day.data
    local layer=ui.g_self and ui.g_self.daily_main_layer
    if current and current.local_day~=data.local_day and layer then
     local ok,parent=pcall(function() return layer:getParent() end)
     if ok and parent then ui.pressDaily() end
    end
   end
   return value
  end
  ui._localDailyRestore=function()
   ui.showDaily=show;ui.onGetResult=result;ui._localDailyRestore=nil
  end
 end
end
