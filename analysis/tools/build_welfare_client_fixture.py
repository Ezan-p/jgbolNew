"""Exercise unmodified 3.87 welfare renderers using disposable server state."""
import sys,tempfile,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from network_redirect import welfare,summon
from network_redirect.backend import Backend,login_fields
from network_redirect.protocol import encode,decode
root=Path(__file__).resolve().parents[2]
with tempfile.TemporaryDirectory() as tmp:
 b=Backend(Path(tmp),1,lambda *a,**k:None);r=b.profile();r.update(level=60,vip_level=10,gold_coin=10000,buy_growup=1)
 now=int(time.time());welfare.record_charge(r,3000,now,b.welfare_rules)
 data=login_fields(decode(welfare.query(r,now,b.welfare_rules))[2]['data'])
 lines=['''local ms=assert(package.loaded.ms)
local v=ms.d_actNoticeUI
local hadAdapter=v._localWelfareRestore
local saved={player=ms.d_mainUI.g_playerInfo,send=ms.d_u.main_server_send_msg,config=v.g_self.config,meiri=v.g_self.meiri}
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
ms.d_u.main_server_send_msg=function(...) end
local results={}
local function check(name,fn)
 local ok,err=xpcall(fn,debug.traceback)
 results[#results+1]={name=name,ok=ok,error=not ok and tostring(err) or nil}
end
''']
 lines.append(Path('network_redirect/welfare_client.lua').read_text())
 lines.append('for k,val in pairs('+summon.lua({k:r[k] for k in ['level','vip_level','gold_coin','buy_growup','first_charge','first_charge_gift','take_charge_gift_time']})+') do ms.d_mainUI.g_playerInfo[k]=val end')
 lines.append('v.g_self.config={had_prize_flag={}};v.g_self.meiri='+summon.lua(data['all_activity'][74]))
 lines.append('v.g_self.data='+summon.lua(data))
 lines.append("check('open',function() v.show() end)")
 for i,a in enumerate(b.welfare_rules['order'],1):
  lines.append("check('page_%d',function() v.g_self.last_press_btn_tag=%d;v.showContent(v.g_self.main_layer,%d) end)"%(a,i,i))
 # Exercise success callbacks with real encoded server replies and disposable rewards.
 for a,i in [(16,0),(22,0),(23,0),(21,0),(21,10),(32,1),(33,1),(34,0),(35,1),(35,2),(36,1),(60,1),(71,1),(71,100)]:
  role=b.profile();role.update(r);summon.add_item(role,1001,1000);role['silver_coin']=10000000
  c=welfare.catalog(role,now,b.welfare_rules)
  lines.append('v.g_self.data='+summon.lua(dict(flag=1,order_list=b.welfare_rules['order'],all_activity=c)))
  pos=b.welfare_rules['order'].index(a)+1
  lines.append('v.g_self.last_press_btn_tag=%d;v.showContent(v.g_self.main_layer,%d)'%(pos,pos))
  events=welfare.settle(role,1127,dict(act_type=a,index=i,flag=2),now,b.welfare_rules,login_fields)
  for event in events:
   m,_,d=decode(event)
   lines.append("check('claim_%d_%d',function() v.callbackGetActNoticeData(%s);ms.d_messageUI.destroyLayer() end)"%(a,i,summon.lua(login_fields(d['data']))))
 for mid,req,a,fn in [(1201,dict(flag=6,id=0),20,'onReceiveGiftResult'),(1239,dict(buy_count=1),24,'onGetGrouponResult'),(1352,dict(id=3,data='{index=1}'),74,'showgetItem')]:
  import copy
  role=copy.deepcopy(r);role['silver_coin']=10000000
  c=welfare.catalog(role,now,b.welfare_rules)
  pos=b.welfare_rules['order'].index(a)+1
  lines.append('v.g_self.data='+summon.lua(dict(flag=1,order_list=b.welfare_rules['order'],all_activity=c)))
  lines.append('v.g_self.last_press_btn_tag=%d;v.showContent(v.g_self.main_layer,%d)'%(pos,pos))
  events=welfare.settle(role,mid,req,now,b.welfare_rules,login_fields)
  payload=login_fields(decode(events[0])[2]['data'])
  if mid==1352:payload=dict(attach_list=payload['data'],result=1)
  lines.append("check('callback_%d',function() v.%s(%s);ms.d_messageUI.destroyLayer() end)"%(mid,fn,summon.lua(payload)))
 lines.append("check('fund_request',function() local captured;ms.d_u.main_server_send_msg=function(mid,data) captured={mid=mid,data=data} end;v.pressBuyFund();assert(captured and captured.mid==1112 and captured.data.event_id==3);local d=assert(loadstring('return '..captured.data.data))();assert(d.item_id==8);ms.d_u.main_server_send_msg=function() end end)")
 lines.append('v.g_self.data='+summon.lua(data)+';v.show()')
 lines.append("check('daily_refresh_twice',function() local d=v.g_self.data.all_activity[74];v.setMeiridata(d);v.setMeiridata(d);local n=0;for _,id in ipairs(v.g_self.data.order_list) do if id==74 then n=n+1 end end;assert(n==1) end)")
 lines.append('''check('close',function() v.closeNoticeUI() end)
ms.d_mainUI.g_playerInfo=saved.player
ms.d_u.main_server_send_msg=saved.send
v.g_self.config=saved.config;v.g_self.meiri=saved.meiri
if not hadAdapter and v._localWelfareRestore then v._localWelfareRestore() end
return table.tostring({results=results,restored=true})''')
 (root/'analysis/evidence/welfare/client_fixture.lua').write_text('\n'.join(lines));b.close()
