"""Build isolated original UI replay; live sends blocked and player tables restored."""
import sys
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect.backend import Backend
from network_redirect import formation as f, summon
from network_redirect.protocol import encode,decode

with tempfile.TemporaryDirectory() as tmp:
 b=Backend(Path(tmp),18790,lambda *a,**k:None);role=b.profile()
 role.update(level=99,gold_coin=10000)
 def add(t,level):
  i=dict(id=f.new_id(role),attach_type=6,type_id=t,count=0,level=level)
  role['attachments'].append(i);return i['id']
 target=add(22,10);materials=[add(22,1),add(25,1)];summon.add_item(role,1095,1)
 b.save(role);role=b.profile()
 lines=["""local ms=assert(package.loaded.ms)
local saved={player=ms.d_mainUI.g_playerInfo,corts=ms.d_lineupUI.g_characterInfo,items=ms.d_packageUI.g_packageItemsInfo,send=ms.d_u.main_server_send_msg,report=ms.MS_report_error,info=ms.d_info.show}
ms.d_u.main_server_send_msg=function(...) return end
local errors='';insight_fixture_results={};insight_fixture_restored=false
ms.MS_report_error=function(e) errors=errors..'\\n'..tostring(e) end
ms.d_info.show=function(...) return end
local cases={};local function step(name,fn) cases[#cases+1]={name=name,run=fn} end
local function apply(mid,d)
 if mid==1032 then ms.d_event_mgr.msg_modify_attr_1032(nil,d,nil)
 elseif mid==1034 then ms.d_lineupUI.getDateFormServer(d)
 elseif mid==1035 then ms.d_packageUI.getDateFormServer(d)
 elseif mid==2998 then ms.d_event_mgr.msg_common_event_2998(nil,d,nil) end
end
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
ms.d_mainUI.g_playerInfo.gold_coin=10000
local function item(id) for _,i in ipairs(ms.d_packageUI.g_packageItemsInfo) do if i.id==id then return i end end end
local function parent() return ms.d_mainUI.g_mainUI.main_layer end
"""]
 for p in b.inventory(role):
  mid,_,d=decode(p);lines.append('apply('+str(mid)+','+summon.lua(d)+')')
 def step(name,code):lines.append('step('+summon.lua(name)+',function() '+code+' end)')
 step('insight_original_window','ms.d_mainUI.show();ms.d_skillUpgradeUI.show({from_btn=100,skill_info=item(%d),parent_layer=parent(),isNeedUpdate=false})'%target)
 def request(name,mid,serial,check,**req):
  code=[]
  for p in b.respond(encode(mid,dict(serial_num=serial,**req)),dict(authenticated=True)):
   m,_,d=decode(p)
   assert not(m==2998 and d['id']==55),d
   if m in (1032,1034,1035) or m==2998 and d['id'] in (156,89):code.append('apply('+str(m)+','+summon.lua(d)+')')
  step(name,';'.join(code)+';'+check)
 request('insight_original_callback',1076,100001,'assert(item(%d).upgrade_level==1);assert(not item(%d));assert(not item(%d))'%(target,*materials),upgrade_type=6,des_id=target,material_count=2,material_list=[dict(id=i) for i in materials])
 step('conversion_original_window','ms.d_mainUI.show();ms.d_qiankunnizhuan.show(parent())')
 request('conversion_original_callback',1212,100002,'assert(not item(%d))'%target,skill_id=target,state=4)
 lines.append("""local function restore()
 ms.d_u.main_server_send_msg=saved.send;ms.MS_report_error=saved.report;ms.d_info.show=saved.info
 ms.d_mainUI.g_playerInfo=saved.player;ms.d_lineupUI.g_characterInfo=saved.corts;ms.d_packageUI.g_packageItemsInfo=saved.items
 ms.d_packageUI.g_isPackageSorted=false;ms.d_packageUI.sortItems();ms.d_lineupUI.sortcharacterInfo()
 ms.d_mainUI.show();insight_fixture_restored=true
end
local scheduler=CCDirector:sharedDirector():getScheduler();local index=0;local handle
handle=scheduler:scheduleScriptFunc(function()
 if index>0 then insight_fixture_results[index]={name=cases[index].name,errors=errors} end
 index=index+1
 if index>#cases then scheduler:unscheduleScriptEntry(handle);local ok,e=pcall(restore);insight_fixture_restore_error=not ok and tostring(e) or nil;return end
 errors='';local ok,err=xpcall(cases[index].run,debug.traceback);if not ok then errors=errors..'\\n'..tostring(err) end
end,2,false)
return 'scheduled '..#cases..' isolated original insight checks'
""")
 (ROOT/'.runtime/insight-fixture.lua').write_text('\n'.join(lines));b.close()
