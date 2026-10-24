"""Replay real original purchase buttons + response state without spending user funds."""
import sys,json,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from network_redirect import summon,vip
from network_redirect.backend import Backend
from network_redirect.protocol import encode
root=Path(__file__).resolve().parents[2]
out=root/'analysis/evidence/recharge';out.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory() as t:
 b=Backend(Path(t),18790,lambda *a,**k:None)
 src="""local m=assert(package.loaded.ms)
local r=m.d_rechargeUI;local v=m.d_vipUI
if r.g_self.main_layer then r.pressClose() end
if v.g_self.main_layer then v.pressClose() end
if v._localVipRestore then v._localVipRestore() end
local saved={player=m.d_mainUI.g_playerInfo,config=m.d_data.g_new_config,send=m.d_u.main_server_send_msg,waiting=m.d_u.g_is_waiting_1106}
m.d_mainUI.g_playerInfo=m.d_c.table_copy(saved.player)
m.d_data.g_new_config=m.d_c.table_copy(saved.config)
local captured
m.d_u.main_server_send_msg=function(mid,data) captured={mid=mid,data=data} end
m.d_u.g_is_waiting_1106=false
local results={}
local function check(name,fn) local ok,e=xpcall(fn,debug.traceback);results[#results+1]={name=name,ok=ok,error=not ok and tostring(e) or nil} end
"""
 src+=(root/'network_redirect/vip_client.lua').read_text().replace('__VIP_PRODUCTS__',summon.lua(b.vip_rules['products']))
 src+='\ncheck("original_market_layout",function() m.d_shopUI.recharge();assert(r.g_self.main_layer and r.g_self.menu);assert(r.g_self.hasCharged) end)\n'
 for i in range(1,7):
  src+=f'''check('purchase_button_{i}',function()
 local button=tolua.cast(r.g_self.menu:getChildByTag(r.g_self.button_tag+{i}),'CCMenuItem')
 assert(button);button:activate();assert(captured.mid==1111 and captured.data.event_id==250)
 local d=assert(loadstring('return '..captured.data.data))();assert(d.item_id=={100+i})
end)
'''
 for serial,product in enumerate([101,102,103,104,105,106]+[106]*20,1):
  b.respond(encode(1111,dict(serial_num=serial,event_id=250,data=summon.lua(dict(item_id=product,order_id=f'fixture-{serial:04}')))),dict(authenticated=True))
  role=b.profile()
  src+=f'''check('credit_{serial}_vip_{role['vip_level']}',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({summon.lua(dict(local_vip=vip.client_state(role)))})
 assert(m.d_mainUI.g_playerInfo.vip_level=={role['vip_level']})
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel=={role['vip_level']} or digits[1]~=old) and #digits==#{summon.lua(str(role['vip_level']))})
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
'''
 src+='''check('vip_navigation',function() r.pressVIP();assert(v.g_self.main_layer);v.pressRecharge();assert(r.g_self.main_layer) end)
r.pressClose()
m.d_mainUI.g_playerInfo=saved.player;m.d_data.g_new_config=saved.config
m.d_u.main_server_send_msg=saved.send;m.d_u.g_is_waiting_1106=saved.waiting
local main=m.d_mainUI.g_mainUI
main.playerInfoTab=m.d_playerInfoUI.reloadPlayerInfo(main.player_layer)
return table.tostring({results=results,restored=true})
'''
 (out/'client_fixture.lua').write_text(src);b.close()
