-- Retain the original map/rank widgets; supply the omitted personal rank data.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_tongtiantaUI
 if ui and ui.onGetResult and not ui._localBabelRestore then
  local oldResult,oldRank=ui.onGetResult,ui.showRank
  local textIndex,textOriginal
  if oldRank and debug and debug.getupvalue then
   for i=1,100 do
    local name,value=debug.getupvalue(oldRank,i)
    if not name then break end
    if name=='gethz' then
     textIndex,textOriginal=i,value
     debug.setupvalue(oldRank,i,function(key,...)
      if key=='tongtianta18' then return '离线NPC榜：同层按到达时间排名' end
      if key=='tongtianta19' then return '周一结算，奖励由系统邮件领取' end
      return value(key,...)
     end)
     break
    end
   end
  end
  ui.onGetResult=function(message,...)
   local data=message and message.data
   if message and message.id==3 and data then
    ui.g_self=ui.g_self or {}
    local rank=ui.g_self.rankData or {{},{}}
    rank[1]=rank[1] or {};rank[2]=rank[2] or {}
    rank[1].my_top_data=data.my_top
    rank[2].my_top_data=(data.last_my_top and type(data.last_my_top.order)=='number') and data.last_my_top or nil
    ui.g_self.rankData=rank
   end
   local result=oldResult(message,...)
   if message and message.id==2 and data and data.completed_now then
    ms.d_info.show('已通关通天塔60层！本周可继续探索与兑换，周一结算榜奖。')
   end
   return result
  end
  ui._localBabelRestore=function()
   ui.onGetResult=oldResult
   if textIndex then debug.setupvalue(oldRank,textIndex,textOriginal) end
   ui._localBabelRestore=nil
  end
 end
end
