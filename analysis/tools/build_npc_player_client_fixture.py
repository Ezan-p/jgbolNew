"""Generate an isolated, self-restoring native Lua NPC inspection smoke test."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import npc_players as npc, summon
from network_redirect.protocol import decode

lines=['''local ms=assert(package.loaded.ms)
assert(ms.d_mainUI.g_playerInfo and ms.d_mainUI.g_mainUI.main_layer,'main scene required')
for k,v in pairs(_G) do assert(type(k)~='string' or not k:match('fixture_restore$'),'another fixture is active') end
local saved={send=ms.d_u.main_server_send_msg,report=ms.MS_report_error,player=ms.d_mainUI.g_playerInfo,
 list=ms.d_followUI.g_otherPlayerList,index=ms.d_followUI.g_searchIndex,inboard=ms.d_followUI.g_isInThisBoard,
 other=ms.d_followUI.g_isInOtherPlayerPage,display=ms.d_checkLineupUI.displayLineupInfo}
local results={};local errors=''
ms.d_u.main_server_send_msg=function() end
ms.MS_report_error=function(e) errors=errors..'\\n'..tostring(e) end
local function step(name,fn)
 errors='';local ok,err=xpcall(fn,debug.traceback)
 results[#results+1]=name..': '..(ok and errors=='' and 'OK' or tostring(err)..errors)
end
ms.d_followUI.g_isInThisBoard=false;ms.d_followUI.g_isInOtherPlayerPage=false
ms.d_followUI.g_otherPlayerList={};ms.d_followUI.g_searchIndex=1
''']
search=decode(npc.search(dict(search_type=1,search_index=1,search_string='99'),99))[2]
lines.append('step("native_search",function() ms.d_event_mgr.msg_search_player_result_1092(nil,'+summon.lua(search)+',nil);assert(#ms.d_followUI.g_otherPlayerList==20) end)')
for key in ('npc_v1_l01_t5_attack','npc_v1_l99_t1_attack','npc_v2_l99_t1_attack'):
    n=npc.get(key);data=npc.inspection_data(n)
    lines.append('step('+summon.lua(key)+',function() ms.d_checkLineupUI.show('+summon.lua(data)+');assert(#ms.d_checkLineupUI.displayLineupInfo.usedCharacters=='+str(len(data['cortege_list']))+');for i=1,'+str(len(data['cortege_list']))+' do ms.d_charPositionUI.tapHeadButton(i,true) end;assert(ms.d_mainUI.g_playerInfo==saved.player) end)')
lines.append('''ms.d_followUI.g_otherPlayerList=saved.list;ms.d_followUI.g_searchIndex=saved.index
ms.d_followUI.g_isInThisBoard=saved.inboard;ms.d_followUI.g_isInOtherPlayerPage=saved.other
ms.d_checkLineupUI.displayLineupInfo=saved.display
local restored,restore_error=pcall(ms.d_mainUI.show)
ms.d_u.main_server_send_msg=saved.send;ms.MS_report_error=saved.report
assert(restored,restore_error)
return table.concat(results,'\\n')
''')
path=ROOT/'.runtime/npc-player-fixture.lua';path.write_text('\n'.join(lines))
print(path)
