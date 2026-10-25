"""Disposable backend -> original UI callbacks; restore live UI state at end."""
import sys
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from network_redirect import pets, activity, activity_home, summon
from network_redirect.backend import Backend
from network_redirect.protocol import encode,decode
lines=['''local ms=assert(package.loaded.ms)
assert(not pet_fixture_restore,'pet fixture already running')
local ui=ms.d_petUI
local saved={player=ms.d_mainUI.g_playerInfo,items=ms.d_packageUI.g_packageItemsInfo,send=ms.d_u.main_server_send_msg,report=ms.MS_report_error,open=ui.pet_is_open}
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player);ms.d_mainUI.g_playerInfo.level=60
ms.d_u.main_server_send_msg=function() end
ui.pet_is_open=true
pet_fixture_finished=false;pet_fixture_results={};local errors='';local cases={}
ms.MS_report_error=function(e) errors=errors..'\\n'..tostring(e) end
local function step(name,fn) cases[#cases+1]={name=name,run=fn} end
local function apply(mid,d)
 if mid==1035 then ms.d_packageUI.getDateFormServer(d)
 elseif mid==2998 and d.id==174 then ms.d_event_mgr.msg_common_event_2998(nil,d,nil) end
end
function pet_fixture_restore()
 pcall(ui.pressClose)
 ms.d_mainUI.g_playerInfo=saved.player;ms.d_packageUI.g_packageItemsInfo=saved.items
 ms.d_packageUI.g_isPackageSorted=false;ms.d_packageUI.sortItems()
 ms.d_u.main_server_send_msg=saved.send;ms.MS_report_error=saved.report;ui.pet_is_open=saved.open
 pet_fixture_restore=nil;ms.d_mainUI.show()
end
''']
for op,name in [(4,'enter'),(3,'select'),(1,'eat'),(2,'fusion'),(6,'star'),(5,'train')]:
 with tempfile.TemporaryDirectory() as tmp:
  b=Backend(Path(tmp),18771,lambda *a,**k:None);r=b.profile();r['level']=60
  activity.prepare(r,1792814400,b.activity_rules);h=activity_home.state(r,1792814400,b.activity_rules)
  target=pets.add(h,201,3);target['order']=1
  foods=[pets.add(h,102,1) for _ in range(6)]
  if op==5:target['star_level']=1
  for tid in (1345,1347):summon.add_item(r,tid,100)
  h['independent_pet_initialized']=True;b.save(r)
  lines.append('step('+summon.lua(name)+',function() pcall(ui.pressClose);ms.d_mainUI.show();ui.show({parent=ms.d_mainUI.g_mainUI.main_layer,zorder=100,tag=9876})')
  def req(serial,op,**data):
   packets=b.respond(encode(1330,dict(serial_num=serial,flag=1,id=op,data=summon.lua(data))),dict(authenticated=True))
   for p in packets:
    m,_,d=decode(p)
    assert not(m==2998 and d['id']==55),(name,d)
    if m==1035 or m==2998 and d['id']==174:lines.append('apply('+str(m)+','+summon.lua(d)+')')
  req(100001,4)
  if op!=4:
   lines.append('ui.pressMenu('+str({1:1,2:3,3:1,5:4,6:4}[op])+')')
   data=dict(des_id=target['id'])
   if op in (1,2,6):data['src_list']=[p['id'] for p in foods[:{1:1,2:3,6:5}[op]]]
   if op==5:data['pos']=1
   req(100002,op,**data)
  lines.append('end)');b.close()
lines.append('''step('guide_and_handbook',function()
 ui.pressMenu(2);ui.getAllPetHandbook();ui.getPetIntroLayer(201)
end)
local scheduler=CCDirector:sharedDirector():getScheduler();local index=0;local handle
handle=scheduler:scheduleScriptFunc(function()
 if index>0 then pet_fixture_results[index]={name=cases[index].name,errors=errors} end
 index=index+1
 if index>#cases then scheduler:unscheduleScriptEntry(handle);pet_fixture_restore();pet_fixture_finished=true;return end
 errors='';local ok,err=xpcall(cases[index].run,debug.traceback)
 if not ok then errors=errors..'\\n'..tostring(err) end
end,3,false)
return 'pet original UI fixture started'
''')
(ROOT/'.runtime/pet-fixture.lua').write_text('\n'.join(lines))
