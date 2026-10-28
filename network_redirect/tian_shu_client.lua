-- Preserve original book cells, destinations, ordering and reward callbacks.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_tianShuUI
 if not (ui and ms.d_data and ms.d_hz) then return 'pending' end
 if ui._localTianShuRestore and ui._localTianShuVersion~=2 then ui._localTianShuRestore() end
 if not ui._localTianShuRestore then
  local config=ms.d_data.callback_update_config
  local hz=ms.d_hz.gethz
  local getConfig=ui.getTaskConfig
  local allTaken=ui.isAllPrizeTaken
  local monthTag=ui.g_monthCardTag
  ms.d_data.callback_update_config=function(data,...)
   if data.local_tian_shu then
    local player=ms.d_mainUI.g_playerInfo
    if player then
     player.task_progress=data.local_tian_shu.task_progress
     player.task_prize=data.local_tian_shu.task_prize
     ui.g_isAllPrizeTaken=false
    end
    return
   end
   return config(data,...)
  end
  ui.getTaskConfig=function(...)
   local result=getConfig(...)
   -- User-requested level-nine gold reward: use native gold display/callback.
   ui.g_monthCardTag=nil
   for _,row in ipairs(ui.g_taskConfig or {}) do
    if row.stage==14 then row.desc='绑定本地游戏账号' end
   end
   return result
  end
  ms.d_hz.gethz=function(key,...)
   if key=='first_register_real' then return '绑定本地游戏账号' end
   return hz(key,...)
  end
  -- Native caches true forever, leaking completion when switching accounts.
  ui.isAllPrizeTaken=function(...)
   ui.g_isAllPrizeTaken=false
   return allTaken(...)
  end
  ui._localTianShuRestore=function()
   ms.d_data.callback_update_config=config;ms.d_hz.gethz=hz
   ui.getTaskConfig=getConfig;ui.isAllPrizeTaken=allTaken
   ui.g_monthCardTag=monthTag
   if ui.g_taskConfig then
    for _,row in ipairs(ui.g_taskConfig) do
     if row.stage==14 then row.desc='通过个人中心绑定账号并注册实名信息' end
    end
   end
   ui._localTianShuRestore=nil
   ui._localTianShuVersion=nil
  end
  ui._localTianShuVersion=2
 end
end
