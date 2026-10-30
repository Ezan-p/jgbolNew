local calls={movie=0,original=0,main=0,scene=0}
local guide={guideState={playMoive=2,beforeNaming=3},g_currentGuide=2}
guide.startPlayMoive=function() calls.original=calls.original+1 end
guide.moiveFinished=function()
 if not guide.g_isPlayingMoving then return end
 guide.g_isPlayingMoving=false;guide.g_currentGuide=3;calls.main=calls.main+1
end
local player={guide_progress=0}
local ms={d_guideUI=guide,d_mainUI={g_playerInfo=player},
 d_music_mgr={stop_bkg=function() end},d_u={runScene=function() calls.scene=calls.scene+1 end}}
package.loaded.ms=ms
main_server={startPlayMoive=function(name) assert(name=='none');calls.movie=calls.movie+1 end}
SimpleAudioEngine={sharedEngine=function() return {pauseBackgroundMusic=function() end} end}
CCScene={create=function() return {} end}
local function install()
 -- INSTALL_PATCH
end
local checks={}
local function check(name,fn) fn();checks[#checks+1]=name end
check('installation does not start movie',function() install();assert(calls.movie==0) end)
check('new role waits for native completion',function()
 guide.startPlayMoive();assert(calls.movie==1 and calls.main==0 and guide.g_isPlayingMoving)
 assert(guide.g_currentGuide==2 and player.guide_progress==0)
end)
check('duplicate entry and reinstall cannot start twice',function()
 install();guide.startPlayMoive();assert(calls.movie==1)
end)
check('completion or skip continues exactly once',function()
 guide.moiveFinished();guide.moiveFinished();assert(calls.main==1 and guide.g_currentGuide==3)
 assert(player.guide_progress==0)
end)
check('existing and resumed guides use original flow',function()
 for _,progress in ipairs({2,14,16382}) do
  player.guide_progress=progress;guide.g_currentGuide=2;guide.startPlayMoive()
 end
 assert(calls.movie==1 and calls.original==3)
end)
check('second fresh role in same process can play',function()
 ms.d_mainUI.g_playerInfo={guide_progress=0};guide.g_currentGuide=2
 guide.startPlayMoive();assert(calls.movie==2);guide.moiveFinished()
end)
check('native bridge failure unblocks opening flow',function()
 main_server.startPlayMoive=function() error('decoder unavailable') end
 guide.g_currentGuide=2;guide.startPlayMoive();assert(calls.main==3 and not guide.g_isPlayingMoving)
end)
check('restore removes adapter',function()
 guide._localOpeningRestore();assert(not guide._localOpeningRestore)
 guide.startPlayMoive();assert(calls.original==4)
end)
return checks
