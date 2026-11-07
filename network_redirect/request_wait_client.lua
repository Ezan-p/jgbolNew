-- One in-flight business intent. UI delay never delays the actual request.
do
 local ms=package.loaded.ms
 local u=ms and ms.d_u
 local event=ms and ms.d_event_mgr
 local alert=ms and ms.d_alert
 local transport=rawget(_G,'main_server')
 if not (u and event and event.g_msg_fun and alert and transport and CCDirector
  and ms.d_data and type(ms.d_data.callback_update_config)=='function'
  and type(transport.send_msg)=='function' and type(u.main_server_send_msg)=='function'
  and type(alert.start_wait)=='function' and type(alert.stop_wait)=='function'
  and type(event.msg_process_done_1106)=='function') then return 'pending' end
 if not ms._localRequestWait then
  local scheduler=CCDirector:sharedDirector():getScheduler()
  local pending,finishing,invoking,timer
  local send=transport.send_msg
  local start,stop=alert.start_wait,alert.stop_wait
  local nativeSend=u.main_server_send_msg
  local nativeTimeout=u.packageTimeOut
  local done=event.msg_process_done_1106
  local control={[1001]=true,[1016]=true,[1105]=true,[2999]=true}
  local api={}
  ms._localRequestWait=api
  local function log(stage)
   local item=pending or finishing
   pcall(print,'[request_wait] stage='..stage..' serial_num='..tostring(item and item.serial or 0))
  end
  local function notice(text)
   if ms.d_info and ms.d_info.show then pcall(ms.d_info.show,text) end
  end
  local function copy(value)
   if type(value)~='table' then return value end
   local out={};for k,v in pairs(value) do out[k]=copy(v) end;return out
  end
  local function same(a,b)
   if type(a)~=type(b) then return false end
   if type(a)~='table' then return a==b end
   for k,v in pairs(a) do if k~='serial_num' and not same(v,b[k]) then return false end end
   for k in pairs(b) do if k~='serial_num' and a[k]==nil then return false end end
   return true
  end
  local function hide()
   pcall(stop,true)
   u.g_sys_busy=false
  end
  local function cancelTimer()
   if timer then scheduler:unscheduleScriptEntry(timer);timer=nil end
  end
  local function clear()
   pending=nil;cancelTimer();hide()
   u.g_is_waiting_1106=false;u.g_last_send_msg_id=0;u.g_last_req={}
  end
  local function uncertain(message)
   if pending then pending.stage='uncertain' end
   cancelTimer();hide();u.g_is_waiting_1106=false
   log('uncertain');notice(message)
  end
  local function recover()
   if not pending or pending.stage~='waiting' then return end
   pending.stage='recovering';pending.recovery=0
   hide();u.g_is_waiting_1106=true
   notice('响应较慢，正在确认原请求结果，请勿重复操作')
   log('recovering')
   local ok=pcall(send,1105,{serial_num=pending.serial,req_serial_num=u.g_server_ret_serial_num or 0})
   if not ok then uncertain('连接中断，结果尚未确认；重连后查看结果，或点击原操作重试') end
  end
  local function callbackFailed(mid)
   local item=finishing or pending
   if item then item.failed=true end
   hide();log('callback_error_'..tostring(mid))
  end
  local function tick(dt)
   if not pending then cancelTimer();return end
   local item=pending
   if item.stage=='waiting' then
    item.elapsed=item.elapsed+dt
    if item.elapsed>=0.2 and not item.shown and not item.failed then
     item.shown=true
     local ok=pcall(start,nil,math.max(0.1,10-item.elapsed),recover)
     if not ok then callbackFailed('spinner') end
    end
    if item.elapsed>=10 then recover() end
   elseif item.stage=='recovering' then
    item.recovery=item.recovery+dt
    if item.recovery>=10 then
     uncertain('连接超时，结果尚未确认；请重连查看，点击原操作只会重试同一请求')
    end
   end
  end
  local function arm()
   cancelTimer()
   timer=scheduler:scheduleScriptFunc(function(dt)
    local ok=pcall(tick,dt or 0.05)
    if not ok then uncertain('等待状态异常，请重新登录后查看结果') end
   end,0.05,false)
  end
  function api.retry()
   if not pending or pending.stage~='uncertain' then return false end
   if pending.failed then log('retry_blocked_callback_error');return false end
   pending.stage='waiting';pending.elapsed=0;pending.shown=false
   u.g_sys_busy=true;u.g_is_waiting_1106=true;arm();log('retry_same_id')
   local ok=pcall(send,pending.mid,copy(pending.data))
   if not ok then uncertain('连接尚未恢复，请重连后查看原请求结果') end
   return ok
  end
  function api.state() return pending and pending.stage or 'idle' end
  alert.start_wait=function(...)
   if invoking or pending then return end
   return start(...)
  end
  u.main_server_send_msg=function(mid,data,wait,...)
   if not control[mid] and pending and (wait==nil or wait>0) then
    if pending.stage=='uncertain' and mid==pending.mid and same(data,pending.data) then return api.retry() end
    if pending.stage=='uncertain' then notice('上一操作结果尚未确认，请重连后查看') end
    return false
   end
   local previousInvoking=invoking
   invoking=invoking or (not control[mid] and (wait==nil or wait>0))
   local result={pcall(nativeSend,mid,data,wait,...)}
   invoking=previousInvoking
   if not result[1] then
    if pending then uncertain('发送异常，结果尚未确认，请重连后查看') else hide();u.g_is_waiting_1106=false end
    return false
   end
   return unpack(result,2)
  end
  transport.send_msg=function(mid,data,...)
   local serial=type(data)=='table' and data.serial_num
   if not control[mid] and type(serial)=='number' and serial>0 then
    if pending then return false end
    pending={mid=mid,serial=serial,data=copy(data),stage='waiting',elapsed=0}
    u.g_sys_busy=true;u.g_is_waiting_1106=true;u.g_last_req={}
    arm();log('waiting')
    local result={pcall(send,mid,data,...)}
    if not result[1] then uncertain('发送中断，结果尚未确认，请重连后查看');return false end
    return unpack(result,2)
   end
   return send(mid,data,...)
  end
  u.packageTimeOut=function(...)
   if pending then return recover() end
   if nativeTimeout then return nativeTimeout(...) end
  end
  local function receive(head,data,...)
   local serial=data.req_serial_num
   if not pending then
    hide();u.g_is_waiting_1106=false;u.g_last_req={}
    if serial==0 then
     -- A reconnect replay may have queued notifications without a tracked
     -- business intent. Drain them without consuming a new client sequence.
     if event.handleSavedPackages then
      local ok=pcall(event.handleSavedPackages)
      if not ok then event.g_net_package_list={};callbackFailed('replay_dispatch') end
     end
    elseif serial==u.g_client_req_serial_num then
     local ok=pcall(done,head,data,...)
     if not ok then callbackFailed(1106) end
     u.g_client_req_serial_num=math.max(u.g_client_req_serial_num or 0,serial+1)
    end
    if not pending then hide();u.g_is_waiting_1106=false end
    return
   end
   if serial==0 then
    uncertain('尚未收到原请求确认，请点击原操作重试；不会创建新的请求标识')
    return
   end
   if serial~=pending.serial then log('stale_ack');return end
   local item=pending
   pending=nil;cancelTimer();hide();u.g_last_req={}
   -- Native callback increments the client sequence and drains queued responses.
   local previous=u.g_client_req_serial_num or serial
   finishing=item
   local ok,result=pcall(done,head,data,...)
   if not ok then
    item.failed=true;event.g_net_package_list={};u.g_last_req={};callbackFailed(1106)
   end
   finishing=nil
   u.g_client_req_serial_num=math.max(u.g_client_req_serial_num or 0,previous,serial+1)
   if not pending then hide();u.g_is_waiting_1106=false;u.g_last_send_msg_id=0 end
   return result
  end
  event.msg_process_done_1106=receive
  event.g_msg_fun[1106]=receive
  -- Catch the dispatch callback itself, including native handlers drained by 1106.
  for mid,fn in pairs(event.g_msg_fun) do
   if mid~=1106 and type(fn)=='function' then
    local id,original=mid,fn
    event.g_msg_fun[id]=function(head,data,...)
     if id==1002 and pending then
      if data.result==0 then
       clear();notice('已重新登录，请核对上次操作结果；不会自动重做上次操作')
      else
       uncertain('登录未成功，请重新登录后核对上次操作结果')
      end
     elseif id==1017 and data.reconnect==false and pending then
      clear();notice('已进入新会话，请核对上次操作结果；不会自动重做上次操作')
     elseif id==2996 then
      if data.ret~=0 then
       uncertain('重连失败，请重新登录查看结果；上次操作不会自动重做');return
      elseif pending then
       pending.stage='recovering';pending.recovery=0;arm()
       notice('连接已恢复，正在同步原请求结果')
      end
     end
     local ok,result=pcall(original,head,data,...)
     if not ok then callbackFailed(id);return end
     if id==1017 and pending and pending.stage~='uncertain' then u.g_is_waiting_1106=true end
     return result
    end
   end
  end
  local config=ms.d_data.callback_update_config
  ms.d_data.callback_update_config=function(value,...)
   local reset=value and value.local_request_reset
   if reset then
    local serial=pending and pending.serial or 0
    clear();event.g_net_package_list={}
    u.g_server_ret_serial_num=reset.server_serial or u.g_server_ret_serial_num
    u.g_server_lose_serial_num=0
    u.g_client_req_serial_num=math.max(u.g_client_req_serial_num or 0,serial+1,reset.next_request_serial or 1)
    notice('响应缓存已更新，正在同步最新状态；请重新打开活动查看结果')
    return
   end
   return config(value,...)
  end
  log('installed')
 end
end
