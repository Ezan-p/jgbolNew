"""Check real guide entry/completion with the video and all sends intercepted."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis/tools')]
from android_emulator.config import load_config
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR

HARNESS = r'''
local ms=assert(package.loaded.ms)
local guide=ms.d_guideUI
local saved,ups,checks={},{},{}
local function replace(t,k,v) saved[#saved+1]={t,k,t[k]};t[k]=v end
local function check(name,fn)
 local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]=name..':'..tostring(ok)..':'..(err or '')
end
local originalStart=guide.startPlayMoive
local ok,err=xpcall(function()
 local movie,main,scene=0,0,0
 replace(guide,'startPlayMoive',guide.startPlayMoive)
 replace(guide,'_localOpeningRestore',nil)
 replace(guide,'g_currentGuide',guide.guideState.playMoive)
 replace(guide,'g_isPlayingMoving',false)
 replace(ms.d_mainUI,'g_playerInfo',{level=1,guide_progress=0})
 replace(ms.d_mainUI,'show',function() main=main+1 end)
 replace(ms.d_u,'runScene',function() scene=scene+1 end)
 replace(ms.d_u,'main_server_send_msg',function() end)
 replace(ms.d_stat,'getGsReportParams',function() return '' end)
 replace(ms.d_file,'set',function() end)
 replace(ms.d_file,'get',function() return 1 end)
 replace(ms.d_music_mgr,'stop_bkg',function() end)
 replace(main_server,'startPlayMoive',function(name) assert(name=='none');movie=movie+1 end)
 local audio={sharedEngine=function() return {
  pauseBackgroundMusic=function() end,resumeBackgroundMusic=function() end} end}
 replace(_G,'SimpleAudioEngine',audio)
 replace(_G,'CCScene',{create=function() return {} end})
 for i=1,20 do
  local name,value=debug.getupvalue(guide.moiveFinished,i)
  if not name then break end
  if name=='SimpleAudioEngine' or name=='CCTextureCache' then
   ups[#ups+1]={guide.moiveFinished,i,value}
   debug.setupvalue(guide.moiveFinished,i,name=='SimpleAudioEngine' and audio or
    {sharedTextureCache=function() return {removeUnusedTextures=function() end} end})
  end
 end
 -- INSTALL_PATCH
 check('new guide starts video before main UI',function()
  guide.show();assert(movie==1 and main==0 and scene==1 and guide.g_isPlayingMoving)
 end)
 check('duplicate start is ignored',function() guide.show();assert(movie==1) end)
 check('native finish resumes original beforeNaming flow',function()
  guide.moiveFinished()
  assert(main==1 and not guide.g_isPlayingMoving and guide.g_currentGuide==guide.guideState.beforeNaming)
 end)
 check('duplicate native finish is ignored',function() guide.moiveFinished();assert(main==1) end)
 check('existing role uses original channel flow without video',function()
  ms.d_mainUI.g_playerInfo.guide_progress=2;guide.g_currentGuide=guide.guideState.playMoive
  guide.startPlayMoive();assert(movie==1 and main==2)
 end)
 check('another fresh role can play in same process',function()
  ms.d_mainUI.g_playerInfo={level=1,guide_progress=0};guide.g_currentGuide=guide.guideState.playMoive
  guide.show();assert(movie==2 and main==2)
 end)
end,debug.traceback)
for i=#ups,1,-1 do local s=ups[i];debug.setupvalue(s[1],s[2],s[3]) end
for i=#saved,1,-1 do local s=saved[i];s[1][s[2]]=s[3] end
if not ok then checks[#checks+1]='harness:false:'..err end
return table.concat(checks,'\n')
'''


def main():
    import frida
    config = load_config(ROOT / 'game.json')
    device = frida.get_device(config['serial'], timeout=10)
    pid = next(p for p, name in processes(config).items() if name == config['package'])
    session = device.attach(pid)
    script = session.create_script(LUA_EVALUATOR)
    try:
        script.load()
        raw = script.exports_sync.evaluate(HARNESS.replace(
            '-- INSTALL_PATCH', (ROOT / 'network_redirect/opening_client.lua').read_text()))
    finally:
        script.unload()
        session.detach()
    lines = raw.get('result', '').splitlines()
    passed = raw.get('status') == 0 and len(lines) == 6 and all(':true:' in line for line in lines)
    report = dict(passed=passed, native_guide=True, movie_intercepted=True,
                  live_save_modified=False, checks=lines, raw=raw)
    output = ROOT / 'analysis/evidence/new_role_guide/opening_validation.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not passed:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
