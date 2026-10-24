"""Render original daily/checkin callbacks with actual isolated backend replies."""
import sys
import tempfile
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from network_redirect.backend import Backend
from network_redirect import daily, summon
from network_redirect.protocol import encode, decode
ROOT=Path(__file__).resolve().parents[2]

with tempfile.TemporaryDirectory() as tmp:
 b=Backend(Path(tmp),18790,lambda *a,**k:None)
 lines=["""local ms=assert(package.loaded.ms)
local ui=ms.d_checkinUI
local saved={player=ms.d_mainUI.g_playerInfo,config=ms.d_data.g_new_config,send=ms.d_u.main_server_send_msg,report=ms.MS_report_error,info=ms.d_info.show,self=ui.g_self,day=ui.g_day,hint=ui.g_daily_hint,prizeLayer=ms.d_commonLayerUI.showPrizeResLayer}
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
ms.d_data.g_new_config=ms.d_c.table_copy(saved.config)
ui.g_self=ms.d_c.table_copy(saved.self);ui.g_self.table_checkin_bonus=nil;ui.g_self.has_get_prize_time=nil
ui.g_day={};ms.d_u.main_server_send_msg=function(...) end
local errors='';daily_fixture_results={};daily_fixture_restored=false
ms.MS_report_error=function(e) errors=errors..'\\n'..tostring(e) end
ms.d_commonLayerUI.showPrizeResLayer=function(parent,prizes,callback)
 saved.prizeLayer(parent,prizes,callback)
 if callback then callback() end
end
local cases={}
local function step(name,fn) cases[#cases+1]={name=name,run=fn} end
local function apply(d)
 local payload=assert(loadstring('return '..d.data))()
 if d.id==198 then ui.onGetResult(payload)
 elseif d.id==54 then ui.callbackUpdateRet(payload) end
end
"""]
 for k,v in daily.client_config(b.daily_rules).items():lines.append('ms.d_data.g_new_config['+str(k)+']='+summon.lua(v))
 serial=10000
 def request(name,mid,**kw):
  global serial
  serial+=1; replies=b.respond(encode(mid,dict(serial_num=serial,**kw)),dict(authenticated=True))
  lines.append("step("+summon.lua(name)+",function()")
  for packet in replies:
   m,_,d=decode(packet)
   if m==2998:lines.append('apply('+summon.lua(d)+')')
  lines.append('end)')
 request('daily_empty',1347,id=1,data='{}')
 request('checkin_query',1206,checkin_type=1)
 request('checkin_claim',1206,checkin_type=3)
 request('checkin_duplicate',1206,checkin_type=3)
 role=b.profile()
 for k in range(1,10):daily.record(role,k,1000,int(time.time()),b.daily_rules)
 role['daily']['checkin_count']=30;b.save(role)
 lines.append("step('close_sign',function() ms.d_u.remove(ui.g_self.main_layer) end)")
 request('daily_full',1347,id=1,data='{}')
 # The real chest button holds a private preview closure, recovered through its upvalue.
 lines.append("step('daily_box_preview',function() local preview;for i=1,30 do local n,v=debug.getupvalue(ui.showDaily,i);if not n then break end;if type(v)=='function' and n=='showGift' then preview=v end end;assert(preview,'preview function missing');preview(ui.g_self.daily_main_layer,ui.g_day.data.point_prize[1],1) end)")
 request('daily_box_claim',1347,id=2,data='{prize_id=1}')
 lines.append("step('daily_claim_status',function() assert(ui.g_day.data.point_prize[1].status==3,'claimed status missing') end)")
 request('checkin_bonus_query',1206,checkin_type=1)
 request('checkin_bonus_claim',1206,checkin_type=2,day_index=3)
 request('checkin_bonus_duplicate',1206,checkin_type=2,day_index=3)
 lines.append("""local function restore()
 pcall(ms.d_u.remove,ui.g_self.daily_main_layer)
 ms.d_commonLayerUI.showPrizeResLayer=saved.prizeLayer
 ms.d_u.main_server_send_msg=saved.send;ms.MS_report_error=saved.report;ms.d_info.show=saved.info
 ms.d_mainUI.g_playerInfo=saved.player;ms.d_data.g_new_config=saved.config
 ui.g_self=saved.self;ui.g_day=saved.day;ui.g_daily_hint=saved.hint
 ms.d_mainUI.show();daily_fixture_restored=true
end
local scheduler=CCDirector:sharedDirector():getScheduler();local index=0;local handle
handle=scheduler:scheduleScriptFunc(function()
 if index>0 then daily_fixture_results[index]={name=cases[index].name,errors=errors} end
 index=index+1
 if index>#cases then scheduler:unscheduleScriptEntry(handle);restore();return end
 errors='';local ok,err=xpcall(cases[index].run,debug.traceback);if not ok then errors=errors..'\\n'..tostring(err) end
end,2,false)
return 'scheduled '..#cases..' original daily UI checks; no live save writes'
""")
 (ROOT/'.runtime/daily-fixture.lua').write_text('\n'.join(lines)); b.close()
