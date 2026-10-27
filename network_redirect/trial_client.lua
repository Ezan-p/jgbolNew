-- Preserve the original boss, cooldown, battle and reward widgets.
-- Add the daily-completion message and explicitly unavailable solo-mode actions.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_shilianUI
 if not ui or not ui.processStatus or not ms.d_u then return 'pending' end
 if not ui._localTrialRestore then
  local original,send=ui.processStatus,ms.d_u.main_server_send_msg
  local function up(fn,key)
   for i=1,100 do
    local name,value=debug.getupvalue(fn,i)
    if not name then break end
    if name==key then return value end
   end
  end
  local show=up(original,'show')
  local function finish()
   -- Native exit callbacks replace dataTable; resolve the current table each time.
   local state=show and up(show,'dataTable')
   if not state or not state.main_layer then return end
   -- A pending native cooldown callback may run while the reward box is open.
   -- Its menu builder must return before indexing the now-empty bossList.
   state.lastSelectBoss=nil
   for _,tag in ipairs({1001,1005}) do
    local node=state.main_layer:getChildByTag(tag)
    if node then node:removeAllChildrenWithCleanup(true) end
   end
   for _,key in ipairs({'rightLayer','challengeInfoLayer','select'}) do
    if state[key] then state[key]:setVisible(false) end
   end
  end
  ui.processStatus=function(data)
   if data.flag==2 and data.train_data and data.train_data.daily_complete then
    ms.d_info.show('今日诸神试炼已完成，明日零点刷新五星首领。')
    return
   end
   local result=original(data)
   if data.flag==9 and data.result==1 then finish() end
   return result
  end
  ms.d_u.main_server_send_msg=function(mid,data,...)
   if mid==1064 and data and (data.flag==3 or data.flag==4 or data.flag==7) then
    ms.d_info.show('好友助战暂未开放，请独自挑战今日首领。')
    return
   end
   return send(mid,data,...)
  end
  ui._localTrialRestore=function()
   ui.processStatus=original;ms.d_u.main_server_send_msg=send;ui._localTrialRestore=nil
  end
 end
end
