"""Isolated original-client coupon checks; never send a live redemption."""
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import summon
from network_redirect.backend import Backend
from network_redirect.protocol import encode, decode

with tempfile.TemporaryDirectory() as tmp:
    b = Backend(Path(tmp), 18770, lambda *a, **kw: None)
    packets = b.respond(encode(1104, dict(serial_num=1, sn='JGBOL387', flag=0)), {'authenticated': True})
    event = next(d for m, _, d in map(decode, packets) if m == 2998 and d['id'] == 18)
    b.close()

code = r'''
local ms=assert(package.loaded.ms);local ui=ms.d_systemSetUI
assert(not (ui.g_self.ex_gift_layer and ui.g_self.ex_gift_layer.main_layer),'close existing coupon window first')
local saved={layer=ui.g_self.ex_gift_layer,close=ui.g_self.ex_gift_layer_close_callback,parent=ms.d_mainUI.g_mainUI.main_layer,
 send=ms.d_u.main_server_send_msg,info=ms.d_info.show,reward=ms.d_messageUI.createGetItemsLayer}
local checks={};local sent={};local tip;local reward
local function check(ok,name) assert(ok,name);checks[#checks+1]=name end
local function up(name)
 for i=1,30 do local n,v=debug.getupvalue(ui.createExchangeGiftBagLayer,i);if n==name then return v end end
 error('missing original upvalue '..name)
end
local cancel=up('menuCancelEGL');local submit=up('menuExchangeEGL')
local parent=up('CCLayerColor'):create(up('ccc4')(0,0,0,0));parent:retain()
ms.d_mainUI.g_mainUI.main_layer=parent
ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
ms.d_info.show=function(text) tip=text end
ms.d_messageUI.createGetItemsLayer=function(parent,data,z) reward=data end
ui.g_self.ex_gift_layer_close_callback=nil
local ok,err=xpcall(function()
 ui.exchangeGiftBag()
 check(ui.g_self.ex_gift_layer.main_layer~=nil,'original_input_window')
 local box=assert(ui.g_self.ex_gift_layer.gift_code_box)
 box:setString('');submit();check(#sent==0,'empty_input_no_request')
 box:setString('JGBOL387');submit()
 check(#sent==1 and sent[1].mid==1104 and sent[1].data.sn=='JGBOL387' and sent[1].data.flag==0,'original_1104_request')
 for _,result in ipairs({2,4,5,6,7,8,9,12,13,14,15}) do
  box:setString('JGBOL387');tip=nil
  ms.d_event_mgr.msg_common_event_2998(nil,{id=18,data='{result='..result..',client_flag=0}'},nil)
  check(type(tip)=='string' and #tip>0 and box:getString()=='','error_'..result..'_tip_and_clear')
 end
 ms.d_event_mgr.msg_common_event_2998(nil,__SUCCESS__,nil)
 check(reward and reward.attach_count==3 and #reward.attach_list==3,'server_payload_to_original_reward_layer')
 check(reward.attach_list[1].attach_count==300,'reward_amount')
 check(not ui.g_self.ex_gift_layer.main_layer,'success_closes_input')
 check(tip and tip:find('本地启程礼包',1,true),'original_success_name')
 ui.exchangeGiftBag();cancel()
 check(not ui.g_self.ex_gift_layer.main_layer and #sent==1,'reopen_cancel_no_request')
end,debug.traceback)
if ui.g_self.ex_gift_layer and ui.g_self.ex_gift_layer.main_layer then pcall(cancel) end
ui.g_self.ex_gift_layer=saved.layer;ui.g_self.ex_gift_layer_close_callback=saved.close
ms.d_mainUI.g_mainUI.main_layer=saved.parent;parent:release()
ms.d_u.main_server_send_msg=saved.send;ms.d_info.show=saved.info;ms.d_messageUI.createGetItemsLayer=saved.reward
assert(ok,err)
return ms.d_json.encode({passed=#checks,checks=checks,restored=true,live_redemptions=0,reward_renderer_stubbed=true,isolated_parent=true})
'''.replace('__SUCCESS__', summon.lua(event))
path = ROOT / '.runtime/gift-code-fixture.lua'
path.parent.mkdir(exist_ok=True)
path.write_text(code, encoding='utf-8')
print(path)
