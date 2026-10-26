-- Run with a Lua runtime from the repository root; no Cocos or account mutation.
local ui={g_self={is_all_pass=true,card_data={free_count=3}}}
local sent, fallback, label=nil,0,''
local oldContinue=function() fallback=fallback+1 end
local oldInfo=function(data)
 if data.update_type~=5 then
  ui.g_self.card_data=data
  -- The native callback renders free_count directly, not limit-used_count.
  label='免费刷新次数：'..data.free_count
 end
 return 'native-callback'
end
ui.pressGoOnCard=oldContinue;ui.callbackRapeInfo=oldInfo
package.loaded.ms={d_crossDoomUI=ui,d_music_mgr={playClickEffect=function() end},
 d_msg_def={gscl_msg_id={msg_update_rape_info=1029}},
 d_u={main_server_send_msg=function(id,data) sent={id=id,flag=data.flag} end}}
dofile('network_redirect/rape_client.lua')
local wrapped=ui.pressGoOnCard
dofile('network_redirect/rape_client.lua')
assert(ui.pressGoOnCard==wrapped,'installation must be idempotent')
ui.pressGoOnCard()
assert(sent.id==1029 and sent.flag==4,'Continue must explicitly refresh')
assert(ui.g_self.card_data.free_count==3,'no optimistic local debit')
assert(ui.callbackRapeInfo({update_type=2,free_count=2,rape_list={}})=='native-callback')
assert(label=='免费刷新次数：2' and not ui.g_self.is_all_pass,'new board and counter must update')
ui.g_self.is_all_pass=true
ui.callbackRapeInfo({update_type=3,free_count=0,rape_list={}})
assert(label=='免费刷新次数：0' and not ui.g_self.is_all_pass)
ui.g_self.is_all_pass=true
ui.callbackRapeInfo({update_type=5})
assert(ui.g_self.is_all_pass,'single-target updates must not reset board state')
ui.g_self.card_data=nil;ui.pressGoOnCard();assert(fallback==1)
ui._localRapeRestore()
assert(ui.pressGoOnCard==oldContinue and ui.callbackRapeInfo==oldInfo and not ui._localRapeRestore)
print('rape client regression: continue, counts, state reset, install and restore passed')
