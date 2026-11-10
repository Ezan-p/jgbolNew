-- Display time is a server anchor plus suspend-aware elapsed time, never os.time.
do
 local ms=package.loaded.ms
 local t=ms and ms.d_time
 local event=ms and ms.d_event_mgr
 if not (t and event and event.g_msg_fun and type(t.setTime)=='function'
  and type(event.msg_keep_alive_2999)=='function'
  and type(event.event_client_info_20)=='function') then return 'pending' end
 if t._localGameClockCurrent and t._localGameClockCurrent()=='ready' then return 'ready' end
 if t._localGameClockRestore then t._localGameClockRestore() end
 local elapsed=rawget(_G,'_jgbolContinuousTime')
 if type(elapsed)~='function' then
  -- Desktop injection / older native shells may use the engine's LuaJIT FFI.
  local ok,ffi=pcall(require,'ffi')
  if ok and type(ffi)=='table' then
   local ready,clock=pcall(function()
    if not pcall(ffi.typeof,'jgbol_clock_timespec') then
     ffi.cdef('typedef struct { long sec; long nsec; } jgbol_clock_timespec;')
    end
    pcall(ffi.cdef,'int clock_gettime(int, void *);')
    local stamp=ffi.new('jgbol_clock_timespec[1]')
    return function()
     if ffi.C.clock_gettime(7,stamp)~=0 then return nil end
     return tonumber(stamp[0].sec)+tonumber(stamp[0].nsec)/1000000000
    end
   end)
   if ready then elapsed=clock end
  end
 end
 if type(elapsed)~='function' then return 'pending' end
 local function read()
  local ok,value,nanos=pcall(elapsed)
  if ok and type(value)=='number' and type(nanos)=='number' then value=value+nanos/1000000000 end
  if ok and type(value)=='number' and value==value and value>=0 and value<math.huge then return value end
 end
 local tick=read()
 if not tick then return 'pending' end
 local anchor=tonumber(t.g_self and t.g_self.server_time) or 0
 local last=anchor
 local waiting=false
 local resumeGeneration=0
 local oldSet,oldGet=t.setTime,t.getTime
 local oldHour,oldMin=t.getHour,t.getMin
 local oldShow,oldZone=t.getShowTime,t.getTimeZoneInterval
 local oldWeek,oldWeekend=t.getWeekIndex,t.is_weekend
 local oldBeat,oldLife=event.msg_keep_alive_2999,event.event_client_info_20
 local oldMapBeat,oldMapLife=event.g_msg_fun[2999],event.g_msg_fun[20]
 local function sync(value,...)
  if type(value)~='number' or value~=value or value<0 or value==math.huge then return end
  anchor=value;last=value;tick=read();waiting=false
  return oldSet(value,...)
 end
 local function get()
  local value=read()
  if not waiting and tick and value and value>=tick then
   last=math.max(last,math.floor(anchor+value-tick))
  end
  return last
 end
 local function heartbeat(head,data,...)
  if type(data)=='table' then sync(data.time) end
  return oldBeat(head,data,...)
 end
 local function lifecycle(head,data,...)
  if type(data)=='table' and (data.type==201 or data.type==202) then
   get();waiting=true
   resumeGeneration=resumeGeneration+1
  end
  local result=oldLife(head,data,...)
  if type(data)=='table' and data.type==202 and event.g_has_inside_game
   and ms.d_net and type(ms.d_net.sendHeartBeat)=='function' then
   local net=ms.d_net.g_self
   local delay=net and net.delay_time
   if net then net.delay_time=2147483646 end -- Request only; never a client time authority.
   pcall(ms.d_net.sendHeartBeat)
   if net then net.delay_time=delay end
   -- Consensus is asynchronous (bounded to five seconds). Fetch its result
   -- once promptly instead of waiting for the original long heartbeat period.
   if ms.d_u and type(ms.d_u.delay_node)=='function' then
    local generation=resumeGeneration
    pcall(ms.d_u.delay_node,6,function()
     if generation==resumeGeneration and package.loaded.ms==ms and event.g_has_inside_game
      and ms.d_net and type(ms.d_net.sendHeartBeat)=='function' then
      pcall(ms.d_net.sendHeartBeat)
     end
    end)
   end
  end
  return result
 end
 t.setTime=sync;t.getTime=get
 -- Calendar labels always use Beijing, independently of the device timezone.
 t.getHour=function() return math.floor((get()+28800)/3600)%24 end
 t.getMin=function() return math.floor((get()+28800)/60)%60 end
 local function showTime()
  -- Native UI calls os.date(local, getShowTime()). Convert the Beijing
  -- calendar fields into a local-formatting timestamp, without reading now.
  local fields=os.date('!*t',get()+28800)
  fields.isdst=nil
  return os.time(fields)
 end
 t.getShowTime=showTime
 t.getTimeZoneInterval=function() return get()-showTime() end
 t.getWeekIndex=function(value)
  return tostring((math.floor(((value or get())+28800)/86400)+3)%7+1)
 end
 t.is_weekend=function() local day=t.getWeekIndex();return day=='6' or day=='7' end
 event.msg_keep_alive_2999=heartbeat;event.g_msg_fun[2999]=heartbeat
 event.event_client_info_20=lifecycle;event.g_msg_fun[20]=lifecycle
 t._localGameClockCurrent=function()
  return package.loaded.ms==ms and ms.d_time==t and ms.d_event_mgr==event and t.getTime==get
   and t.setTime==sync and event.msg_keep_alive_2999==heartbeat
   and event.event_client_info_20==lifecycle and 'ready' or 'pending'
 end
 t._localGameClockRestore=function()
  resumeGeneration=resumeGeneration+1
  t.setTime=oldSet;t.getTime=oldGet
  t.getHour=oldHour;t.getMin=oldMin
  t.getShowTime=oldShow;t.getTimeZoneInterval=oldZone
  t.getWeekIndex=oldWeek;t.is_weekend=oldWeekend
  event.msg_keep_alive_2999=oldBeat;event.event_client_info_20=oldLife
  event.g_msg_fun[2999]=oldMapBeat;event.g_msg_fun[20]=oldMapLife
  t._localGameClockCurrent=nil;t._localGameClockRestore=nil
 end
 return 'ready'
end
