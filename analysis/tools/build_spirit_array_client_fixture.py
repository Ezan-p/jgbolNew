"""Temporary DB -> original 3.87 UI; restores live client tables, sends no requests."""
import sys
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect.backend import Backend
from network_redirect import summon, spirit_array as a
from network_redirect.protocol import encode, decode
lines=['''local ms=assert(package.loaded.ms);local ui=ms.d_lingUI
local saved={self=ui.g_self,ui=ui.g_lingUI,send=ms.d_u.main_server_send_msg,report=ms.MS_report_error,items=ms.d_packageUI.g_packageItemsInfo}
ui.g_self={};ui.g_lingUI={};ms.d_u.main_server_send_msg=function() end
local errors='';local cases={};array_fixture_results={};array_fixture_finished=false
ms.MS_report_error=function(e) errors=errors..'\\n'..tostring(e) end
local parent=ms.d_mainUI.g_mainUI.main_layer
local function step(name,fn) cases[#cases+1]={name=name,run=fn} end
local function apply(mid,d)
 if mid==1035 then ms.d_packageUI.getDateFormServer(d)
 elseif mid==2998 and d.id==165 then ms.d_event_mgr.msg_common_event_2998(nil,d,nil) end
end
local function close() if parent:getChildByTag(9875) then parent:removeChildByTag(9875,true) end end
local function open() close();ui.show(parent,1000,9875) end
''']
with tempfile.TemporaryDirectory() as tmp:
 b=Backend(Path(tmp),18770,lambda *a,**kw:None)
 r=b.profile();summon.add_item(r,1315,100000)
 for kind in (1090,1091,1092):
  for lv in (4,7,8,10,11):
   r['attachments'].append(dict(id=summon.next_id(r),attach_type=5,type_id=kind,level=lv,count=1))
 b.save(r)
 for packet in b.inventory(r):
  mid,_,d=decode(packet);lines.append('apply('+str(mid)+','+summon.lua(d)+')')
 serial=1000
 def request(name,op,pre='',post='',**data):
  global serial
  serial+=1;packets=b.respond(encode(1310,dict(serial_num=serial,id=op,data=summon.lua(data))),{'authenticated':True})
  lines.append('step('+summon.lua(name)+',function() '+pre)
  for packet in packets:
   mid,_,d=decode(packet)
   assert not(mid==2998 and d['id']==55),d
   if mid in (1035,2998):lines.append('apply('+str(mid)+','+summon.lua(d)+')')
  lines.append(post+' end)')
 request('enter_empty',5,post='open();assert(#ui.g_self.data==6)')
 lines.append("step('stone_select',function() ui.g_lingUI.index=1;ui.g_lingUI.pos=1;ui.pressChooseSingleStone() end)")
 stone=next(x['id'] for x in r['attachments'] if x['type_id']==1092 and x['level']==8)
 request('mosaic_refund',1,goss_id=1,pos=1,id_list=[stone],post='assert(ui.g_self.data[1].skill_list[1]==1)')
 request('activate_animation',2,goss_id=1)
 request('upgrade_callback',3,goss_id=1,pos=1,post='assert(ui.g_self.data[1].skill_list[1]==2)')
 lines.append("step('exchange_filter',function() ui.pressChooseMultipleStone();ui.createFilterLayer();ui.chooseAllFunc();ui.unChooseAllFunc() end)")
 stone=next(x['id'] for x in r['attachments'] if x['type_id']==1090 and x['level']==4)
 request('exchange_reward',6,id_list=[stone])
 r=b.profile()
 for stage in a.state(r):stage.update(activated=True,skill_list=[5]*len(stage['skill_list']))
 b.save(r)
 request('full_enter',5,post='open()')
 for stage in range(1,7):
  lines.append("step('stage_%d_all_positions',function() ui.changeToIndex(%d);for p=1,%d do ui.g_lingUI.pos=p;ui.showDetail() end end)"%(stage,stage,stage))
 lines.append("step('summary',function() ui.showSummary();assert(ui.getEffectSummary()) end)")
 b.close()
lines.append('''local function restore()
 close();ui.g_self=saved.self;ui.g_lingUI=saved.ui
 ms.d_u.main_server_send_msg=saved.send;ms.MS_report_error=saved.report
 ms.d_packageUI.g_packageItemsInfo=saved.items;ms.d_packageUI.g_isPackageSorted=false;ms.d_packageUI.sortItems()
 array_fixture_finished=true
end
local scheduler=CCDirector:sharedDirector():getScheduler();local index=0;local handle
handle=scheduler:scheduleScriptFunc(function()
 if index>0 then array_fixture_results[index]={name=cases[index].name,errors=errors} end
 index=index+1
 if index>#cases then scheduler:unscheduleScriptEntry(handle);restore();return end
 errors='';local ok,err=xpcall(cases[index].run,debug.traceback);if not ok then errors=errors..'\\n'..tostring(err) end
end,3,false)
return 'scheduled '..#cases..' spirit array client cases'
''')
(ROOT/'.runtime/spirit-array-fixture.lua').write_text('\n'.join(lines))
print('Built 15 client cases')
