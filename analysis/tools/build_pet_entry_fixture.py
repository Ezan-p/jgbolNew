"""Build a native profile-entry probe; run the generated Lua on the game thread."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
adapter=(ROOT/'network_redirect/pet_client.lua').read_text()
regression=(ROOT/'tests/pet_client_regression.lua').read_text().replace("dofile('network_redirect/pet_client.lua')",'do\n'+adapter+'\nend')
(ROOT/'.runtime/pet-entry-probe.lua').write_text('''local ms=package.loaded.ms
local ok,err=pcall(function()
'''+regression+'''
end)
package.loaded.ms=ms
assert(ok,err)
'''+adapter+'''
local u=ms.d_u;local create=u.createMenu
local send=u.main_server_send_msg;local captured;local outgoing
local player=ms.d_mainUI.g_playerInfo
local oldLevel=player.level
u.createMenu=function(styles,...)
 for _,s in pairs(styles) do if type(s)=='table' and s.npic=='v2/playerInfoUI/btn31.png' then captured=s.call_back end end
 return create(styles,...)
end
u.main_server_send_msg=function(id,data) outgoing={id=id,data=data} end
local scene=ms.d_mainUI.g_mainUI.main_layer
local resultOk,result=pcall(function()
 ms.d_petUI.pet_is_open=false
 ms.d_runeUI.showPlayerInfoLayer(scene,90,9981)
 assert(captured,'original pet button missing')
 player.level=49;outgoing=nil;captured();assert(not outgoing,'level49 must be blocked')
 player.level=50;captured();assert(outgoing and outgoing.id==1330 and outgoing.data.id==4,'entry must send pet query')
 return 'original profile button: present; level49 blocked; level50 sends 1330/op4'
end)
u.createMenu=create;u.main_server_send_msg=send;player.level=oldLevel
pcall(ms.d_petUI.pressClose)
if scene then scene:removeChildByTag(9981,true) end
assert(resultOk,result)
return result
''')
