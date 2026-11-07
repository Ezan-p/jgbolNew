-- Observe actual transport sends and completion dispatch without changing waits.
do
 local ms=package.loaded.ms
 local transport=rawget(_G,'main_server')
 local event=ms and ms.d_event_mgr
 if ms and transport and event and type(transport.send_msg)=='function'
    and type(event.msg_process_done_1106)=='function' and not ms._localRequestTiming then
  local ok,socket=pcall(require,'socket')
  -- Lua 5.1 loaders may register the module without returning a table;
  -- require then returns true. Optional timing must not abort UI injection.
  local precise=ok and type(socket)=='table' and type(socket.gettime)=='function'
  local now=precise and socket.gettime or os.time
  local pending={}
  local function log(text) pcall(print,'[request_timing] '..text) end
  local send=transport.send_msg
  transport.send_msg=function(mid,data,...)
   local serial=type(data)=='table' and data.serial_num
   if type(serial)=='number' and serial>0 then
    -- The native client has one waiting request. Retries retain their origin.
    if not pending[serial] then
     pending={ [serial]={start=now(),mid=mid} }
    end
    log('stage=send message_id='..mid..' serial_num='..serial)
   end
   return send(mid,data,...)
  end
  local done=event.msg_process_done_1106
  local function receive(head,data,...)
   local serial=data.req_serial_num
   local item=pending[serial]
   local received=now()
   -- Native handling clears the spinner and can synchronously send the next request.
   pending[serial]=nil
   if item then
    log(string.format('stage=ack serial_num=%s message_id=%s elapsed_ms=%.3f clock=%s',
     serial,item.mid,(received-item.start)*1000,precise and 'socket_wall' or 'wall_seconds'))
   end
   local result=done(head,data,...)
   if item then
    log(string.format('stage=done serial_num=%s elapsed_ms=%.3f dispatch_ms=%.3f',
     serial,(now()-item.start)*1000,(now()-received)*1000))
   end
   return result
  end
  event.msg_process_done_1106=receive
  if event.g_msg_fun then event.g_msg_fun[1106]=receive end
  ms._localRequestTiming=true
  log('stage=installed clock='..(precise and 'socket_wall' or 'wall_seconds'))
 end
end
