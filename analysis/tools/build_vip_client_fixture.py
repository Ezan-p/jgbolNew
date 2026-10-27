"""Run original VIP UI callbacks with disposable backend rewards, restoring references."""
import sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from network_redirect import recharge,vip,summon
from network_redirect.backend import Backend,login_fields
from network_redirect.protocol import encode,decode
root=Path(__file__).resolve().parents[2]
with tempfile.TemporaryDirectory() as tmp:
 b=Backend(Path(tmp),18790,lambda *a,**k:None)
 r=b.profile();r.update(vip_level=10,charge_gold=200000);summon.add_item(r,1156,100);b.save(r)
 lines=["""local ms=assert(package.loaded.ms)
local v=ms.d_vipUI
local hadAdapter=v._localVipRestore
local saved={player=ms.d_mainUI.g_playerInfo,config=ms.d_data.g_new_config,send=ms.d_u.main_server_send_msg,waiting=ms.d_u.g_is_waiting_1106}
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
ms.d_data.g_new_config=ms.d_c.table_copy(saved.config)
ms.d_u.main_server_send_msg=function(...) end
local results={}
local function check(name,fn)
 local ok,err=xpcall(fn,debug.traceback)
 results[#results+1]={name=name,ok=ok,error=not ok and tostring(err) or nil}
end
"""]
 lines.append(Path('network_redirect/vip_client.lua').read_text())
 lines.append('ms.d_data.g_new_config.local_recharge='+summon.lua(recharge.client_state(b.profile(),int(__import__('time').time()),recharge.load_rules(),b.welfare_rules)))
 lines.append('ms.d_data.g_new_config[1]='+summon.lua(vip.client_config(b.vip_rules)))
 lines.append('ms.d_data.g_new_config.local_vip='+summon.lua(vip.client_state(r)))
 lines.append("check('open',function() v.show() end)")
 for level in range(1,11):
  lines.append("check('page_%d',function() v.g_self.main_layer:removeAllChildrenWithCleanup(true);v.createMainFrame(v.g_self.main_layer,%d) end)"%(level,level))
  lines.append("check('preview_%d',function() v.pressVipGiftDetail(%d);ms.d_messageUI.destroyLayer() end)"%(level,level))
  packets=b.respond(encode(1201,dict(serial_num=100+level,flag=7,id=level)),dict(authenticated=True))
  for p in packets:
   mid,_,d=decode(p)
   if mid==2998 and d['id']==59:lines.append("check('gift_%d',function() ms.d_mainUI.g_playerInfo.vip_gift=%d;v.callback_take_vip_gift(%s);ms.d_messageUI.destroyLayer() end)"%(level,b.profile()['vip_gift'],summon.lua(login_fields(d['data']))))
 for level in range(1,11):
  r=b.profile();item=next(x for x in r['attachments'] if x['type_id']==1100+level)
  packets=b.respond(encode(1051,dict(serial_num=150+level,item_type=item['type_id'],item_id=item['id'],item_count=1,des_type=1,des_id=0)),dict(authenticated=True))
  for p in packets:
   mid,_,d=decode(p)
   if mid==2998 and d['id']==21:lines.append("check('open_gift_%d',function() ms.d_commonLayerUI.recvUsedItem(%s);ms.d_messageUI.destroyLayer() end)"%(level,summon.lua(login_fields(d['data']))))
 packets=b.respond(encode(1201,dict(serial_num=200,flag=5,id=0)),dict(authenticated=True))
 for p in packets:
  mid,_,d=decode(p)
  if mid==2998 and d['id']==58:lines.append("check('daily',function() v.callback_take_vip_gold(%s) end)"%summon.lua(login_fields(d['data'])))
 lines.append("""check('recharge_menu',function() v.pressRecharge();assert(ms.d_rechargeUI.g_self.main_layer);ms.d_rechargeUI.pressClose() end)
check('recharge_send',function()
 local captured
 ms.d_u.main_server_send_msg=function(mid,data) captured={mid=mid,data=data} end
 ms.d_u.g_is_waiting_1106=false
 v.show();v.pressRecharge()
 local r=ms.d_rechargeUI
 local button=tolua.cast(r.g_self.menu:getChildByTag(r.g_self.button_tag+1),'CCMenuItem')
 button:activate()
 assert(r._localCardSelection and r._localCardSelection.product.id==101)
 assert(r._localCardSelection.small_count==2)
 r._localCardCancel()
end)
check('close',function() ms.d_rechargeUI.pressClose() end)
if not hadAdapter and v._localVipRestore then v._localVipRestore() end
ms.d_mainUI.g_playerInfo=saved.player
ms.d_data.g_new_config=saved.config
ms.d_u.main_server_send_msg=saved.send
ms.d_u.g_is_waiting_1106=saved.waiting
return table.tostring({results=results,restored=true})
""")
 (root/'analysis/evidence/vip/client_fixture.lua').write_text('\n'.join(lines))
 b.close()
