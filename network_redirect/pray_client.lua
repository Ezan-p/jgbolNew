-- The local save stores COMPLETED prayers (0,1,2,...), while qiFuUI uses
-- pray_spirit_times directly as a CSV index and falls back to its final row.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_qiFuUI
 if not ui or not ui.startQiFu then return 'pending' end
 if not ui._localPrayRestore then
  local oldStart=ui.startQiFu
  local oldConfig=ui.g_qiFuConsumeConfig
  local costs=__PRAY_COSTS__
  ui.startQiFu=function(...)
   local player=ms.d_mainUI.g_playerInfo
   if (player.level or 0)<15 then
    ms.d_info.show('神石祈福15级开放')
    return
   end
   local config={}
   for i=0,#costs do
    config[i]={spirit_coins=costs[math.min(i+1,#costs)]}
   end
   ui.g_qiFuConsumeConfig=config
   return oldStart(...)
  end
  ui._localPrayRestore=function()
   ui.startQiFu=oldStart;ui.g_qiFuConsumeConfig=oldConfig
   ui._localPrayRestore=nil
  end
 end
end
