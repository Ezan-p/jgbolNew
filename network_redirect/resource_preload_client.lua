-- Pure resource work only: no UI construction, role mutations or network sends.
do
 local function install()
  local ms=package.loaded.ms
  local main=type(ms)=='table' and ms.d_mainUI
  local login=type(ms)=='table' and ms.d_loginUI
  local u=type(ms)=='table' and ms.d_u
  if type(main)~='table' or type(main.show)~='function' or type(login)~='table'
      or type(login.show)~='function' or type(u)~='table' then return end
  local previous=rawget(_G,'_localResourcePreload')
  if previous and previous.current() then return end
  if previous then previous.restore() end
  if not CCDirector or not CCDirector.sharedDirector then return end
  local ok,scheduler=pcall(function() return CCDirector:sharedDirector():getScheduler() end)
  if not ok or not scheduler or not scheduler.scheduleScriptFunc or not scheduler.unscheduleScriptEntry then return end
  local plan=__RESOURCE_PRELOAD_PLAN__
  local originalShow,originalLogin,originalClear=main.show,login.show,u.removeAllCache
  local data=ms.d_data
  local state={phase='core',core=1,warm=1,loaded=0,skipped=0,failed=0,retained_bytes=0}
  local pins,timer={},nil
  local texturePaused=false
  local entered=false
  local age,delay,cooldown=0,0,0
  local wrappedShow,wrappedLogin,wrappedClear
  local function pack(...) return {n=select('#',...),...} end
  local function clock() return os.clock() end
  local function log(stage,extra)
   print('[resource_preload] stage='..stage..' loaded='..state.loaded..' skipped='..state.skipped..
    ' failed='..state.failed..' retained_bytes='..state.retained_bytes..(extra or ''))
  end
  local function stop()
   if timer then pcall(scheduler.unscheduleScriptEntry,scheduler,timer);timer=nil end
  end
  local function release()
   for _,entry in pairs(pins) do pcall(function() entry.texture:release() end) end
   pins={};state.retained_bytes=0
  end
  local function reset()
   stop();release()
   state.phase='core';state.core=1;state.warm=1
   state.loaded=0;state.skipped=0;state.failed=0
   entered=false;texturePaused=false;age=0;delay=0;cooldown=0
  end
  local function lowMemory()
   local server=rawget(_G,'main_server') or package.loaded.main_server
   if type(server)=='table' and type(server.get_free_mem_rate)=='function' then
    local good,rate=pcall(server.get_free_mem_rate)
    -- Native cleanAndroidMem clears all textures below 50 percent.
    return good and type(rate)=='number' and rate<55
   end
   return false
  end
  local function atMain()
   return login.senceID and login.senceID.mainUI~=nil
    and login.g_currentSence==login.senceID.mainUI
    and main.g_mainUI and main.g_mainUI.main_scene
  end
  local function idle()
   if not atMain() or u.g_sys_busy or u.g_is_waiting_1106 then return false end
   if not main.boardID or main.g_currentBoard~=main.boardID.none then return false end
   local guide=ms.d_guideUI
   if main.g_isNeedGuide or (guide and guide.g_isPlayingMoving) then return false end
   return true
  end
  local function loadTexture(job)
   if texturePaused then return 'skipped' end
   if lowMemory() then
    texturePaused=true;release();log('memory_pause');return 'skipped'
   end
   if not CCTextureCache or not CCTextureCache.sharedTextureCache then return 'skipped' end
   local cache=CCTextureCache:sharedTextureCache()
   if not cache or not cache.addImage or not cache.textureForKey then return 'skipped' end
   if state.retained_bytes+job.estimated_bytes>plan.retained_texture_bytes then return 'skipped' end
   local texture=cache:textureForKey(job.path)
   if not texture then texture=cache:addImage(job.path) end
   if not texture then error('texture unavailable') end
   -- Never retain a texture without a measurable allocation and release API.
   if not texture.getPixelsWide or not texture.getPixelsHigh or not texture.retain or not texture.release then
    return 'skipped'
   end
   local width,height=texture:getPixelsWide(),texture:getPixelsHigh()
   if type(width)~='number' or type(height)~='number' or width<=0 or height<=0 then return 'skipped' end
   local bytes=math.max(job.estimated_bytes,math.ceil(width*height*4*4/3))
   if state.retained_bytes+bytes>plan.retained_texture_bytes then return 'skipped' end
   if not pins[texture] then
    texture:retain();pins[texture]={texture=texture,bytes=bytes}
    state.retained_bytes=state.retained_bytes+bytes
   end
   return 'loaded'
  end
  local function run(job)
   local started=clock()
   local good,result=pcall(function()
    if job.kind=='texture' then return loadTexture(job) end
    local module=ms[job.module]
    local getter=type(module)=='table' and module[job.getter]
    if type(getter)~='function' then return 'skipped' end
    -- Lazy loaders assign globals before parsing completes. Restore those
    -- references on failure so an optional prewarm cannot leave a partial cache.
    local before={}
    for _,key in ipairs(job.cache_fields) do before[key]=module[key] end
    local ready=pcall(getter)
    if not ready then
     for _,key in ipairs(job.cache_fields) do module[key]=before[key] end
     error('configuration unavailable')
    end
    return 'loaded'
   end)
   local elapsed=clock()-started
   if good then state[result]=state[result]+1
   else state.failed=state.failed+1;log('job_failed',' job='..(job.path or job.getter)) end
   if elapsed>plan.slow_job_seconds then cooldown=plan.cooldown_seconds end
   return elapsed
  end
  local function nextJob(coreOnly)
   local job=plan.core[state.core]
   if job then state.core=state.core+1;return job end
   if not coreOnly then
    job=plan.warm[state.warm]
    if job then state.warm=state.warm+1;return job end
   end
  end
  function state.current()
   return package.loaded.ms==ms and ms.d_mainUI==main and ms.d_loginUI==login and ms.d_u==u
    and ms.d_data==data and main.show==wrappedShow and login.show==wrappedLogin
    and (not originalClear or u.removeAllCache==wrappedClear)
  end
  function state.restore()
   stop();release()
   if main.show==wrappedShow then main.show=originalShow end
   if login.show==wrappedLogin then login.show=originalLogin end
   if originalClear and u.removeAllCache==wrappedClear then u.removeAllCache=originalClear end
   if rawget(_G,'_localResourcePreload')==state then _G._localResourcePreload=nil end
   state.phase='restored'
  end
  local function tick(dt)
   if not state.current() then state.restore();return end
   dt=math.max(0,tonumber(dt) or 0)
   age=age+dt
   if age>plan.max_warm_seconds then state.phase='expired';stop();log('expired');return end
   -- Long frames/background resumes do not trigger a catch-up burst.
   if dt>0.25 then cooldown=plan.cooldown_seconds;return end
   if cooldown>0 then cooldown=math.max(0,cooldown-dt);return end
   if lowMemory() and not texturePaused then texturePaused=true;release();log('memory_pause') end
   if atMain() and not entered then entered=true;age=0;delay=plan.warm_delay_seconds;state.phase='warm' end
   if entered then
    if not idle() then return end
    if delay>0 then delay=math.max(0,delay-dt);return end
   elseif not login.senceID or login.g_currentSence~=login.senceID.login then
    return -- no speculative work in opening movies or battles
   end
   local job=nextJob(not entered)
   if job then run(job) -- exactly one indivisible native task per scheduler callback
   elseif entered then state.phase='done';stop();log('done') end
  end
  local function start()
   if not timer and state.phase~='done' then
    local good,id=pcall(scheduler.scheduleScriptFunc,scheduler,function(dt)
     local good=pcall(tick,dt)
     if not good then state.phase='disabled';stop();release();log('disabled') end
    end,plan.warm_interval_seconds,false)
    if good then timer=id else state.phase='disabled';release();log('scheduler_unavailable') end
   end
  end
  wrappedShow=function(...)
   -- Keep show synchronous: later login packets may immediately use g_mainUI.
   -- Finish a bounded core slice while the native loading scene still owns UI.
   if not entered then
    local started=clock()
    for _=1,plan.startup_max_jobs do
     if clock()-started>=plan.startup_slice_seconds then break end
     local job=nextJob(true);if not job then break end
     run(job)
    end
    log('core_slice',' elapsed_ms='..math.floor((clock()-started)*1000))
   end
   local result=pack(originalShow(...))
   if atMain() and (not entered or state.phase=='expired') then
    entered=true;age=0;delay=plan.warm_delay_seconds;state.phase='warm'
   end
   start()
   return unpack(result,1,result.n)
  end
  wrappedLogin=function(...)
   reset()
   local result=pack(originalLogin(...))
   start()
   return unpack(result,1,result.n)
  end
  wrappedClear=function(...)
   -- Honor native pressure cleanup. Do not immediately reload what it freed.
   texturePaused=true;release();log('cache_clear')
   return originalClear(...)
  end
  main.show=wrappedShow;login.show=wrappedLogin
  if originalClear then u.removeAllCache=wrappedClear end
  _G._localResourcePreload=state
  start();log('installed')
 end
 local good=pcall(install)
 if not good then
  local state=rawget(_G,'_localResourcePreload')
  if state then pcall(state.restore) end
  print('[resource_preload] stage=install_unavailable')
 end
end
