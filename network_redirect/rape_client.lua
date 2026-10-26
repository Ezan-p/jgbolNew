-- Native Continue used query flag 1, which only reloaded the cleared board.
-- Flag 4 requests a server-validated next board; ordinary queries stay read-only.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_crossDoomUI
 if not ui then return 'pending' end
 if not ui._localRapeRestore then
  local oldContinue=ui.pressGoOnCard
  local oldInfo=ui.callbackRapeInfo
  ui.pressGoOnCard=function(...)
   local state=ui.g_self
   if not state or not state.card_data then return oldContinue(...) end
   ms.d_music_mgr.playClickEffect()
   ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_update_rape_info,{flag=4})
  end
  ui.callbackRapeInfo=function(data)
   -- Native callbacks only clear this flag for query responses (update_type=1).
   -- A refreshed board must also clear the prior sweep's completed UI state.
   if data and data.rape_list and ui.g_self then ui.g_self.is_all_pass=false end
   return oldInfo(data)
  end
  ui._localRapeRestore=function()
   ui.pressGoOnCard=oldContinue;ui.callbackRapeInfo=oldInfo
   ui._localRapeRestore=nil
  end
 end
end
