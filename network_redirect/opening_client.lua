-- Restore the native new-role movie skipped by the original 360 channel branch.
do
 local ms=package.loaded.ms
 local guide=ms and ms.d_guideUI
 if not guide or not guide.startPlayMoive then return 'waiting for guide' end
 if not guide._localOpeningRestore then
  local original=guide.startPlayMoive
  local server=main_server or package.loaded.main_server
  if not server or not server.startPlayMoive then return 'waiting for movie bridge' end
  guide.startPlayMoive=function(...)
   local player=ms.d_mainUI and ms.d_mainUI.g_playerInfo
   if not player or tonumber(player.guide_progress)~=0 or
      guide.g_currentGuide~=guide.guideState.playMoive then return original(...) end
   if guide.g_isPlayingMoving then return end
   -- Set the guard before invoking Java; completion can arrive immediately on error.
   guide.g_isPlayingMoving=true
   ms.d_music_mgr.stop_bkg()
   SimpleAudioEngine:sharedEngine():pauseBackgroundMusic()
   ms.d_u.runScene(CCScene:create())
   local ok=pcall(server.startPlayMoive,'none')
   if not ok then guide.moiveFinished() end
  end
  guide._localOpeningRestore=function()
   guide.startPlayMoive=original
   guide._localOpeningRestore=nil
  end
 end
end
