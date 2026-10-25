"""Exercise original equipment UI with temporary binary backend responses."""
import sys
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect.backend import Backend
from network_redirect import formation as f,summon
from network_redirect.protocol import encode,decode

with tempfile.TemporaryDirectory() as tmp:
 b=Backend(Path(tmp),18790,lambda *a,**k:None);role=b.profile()
 role.update(level=99,reborn_layer=4,silver_coin=1000000000,gold_coin=100000)
 for t in (1093,1333,1369,1310,1313,1314,1334,1335):summon.add_item(role,t,100000)
 def add(t,**kw):
  i=dict(id=f.new_id(role),attach_type=5,type_id=t,count=1,level=1);i.update(kw);role['attachments'].append(i);return i['id']
 gear=add(2001,level=50,advance_level=10,equip_order=0)
 stone=add(1090,level=9);mat=add(1091,level=10);add(1090,level=10);add(1090,level=11)
 b.save(role);role=b.profile()
 lines=["""local ms=assert(package.loaded.ms)
local saved={player=ms.d_mainUI.g_playerInfo,corts=ms.d_lineupUI.g_characterInfo,items=ms.d_packageUI.g_packageItemsInfo,send=ms.d_u.main_server_send_msg,report=ms.MS_report_error,info=ms.d_info.show,open=ms.d_stoneUI.g_self.isOpen,limit=ms.d_stoneUI.g_self.Lvlimit,realm=ms.d_roleRebornUI.g_reborn_condition}
ms.d_u.main_server_send_msg=function(...) return end
local errors='';equipment_fixture_results={};equipment_fixture_restored=false
ms.MS_report_error=function(e) errors=errors..'\\n'..tostring(e) end
ms.d_info.show=function(...) return end
local cases={};local function step(name,fn) cases[#cases+1]={name=name,run=fn} end
local function apply(mid,d)
 if mid==1032 then ms.d_event_mgr.msg_modify_attr_1032(nil,d,nil)
 elseif mid==1034 then ms.d_lineupUI.getDateFormServer(d)
 elseif mid==1035 then ms.d_packageUI.getDateFormServer(d)
 elseif mid==2998 then
  local p=assert(loadstring('return '..d.data))()
  if d.id==83 then
   if p.flag==3 then ms.d_stoneUpgradeUI.onGetUpgradeResult(p)
   elseif p.flag==5 then ms.d_stoneCastUI.onGetResult(p)
   else ms.d_stoneUI.onGetResponse(p) end
  elseif d.id==172 then ms.d_ascensionUI.onGetResult(p)
  end
 end
end
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
ms.d_roleRebornUI.g_reborn_condition=ms.d_c.table_copy(saved.realm);for _,r in pairs(ms.d_roleRebornUI.g_reborn_condition) do r.rights.open_stone_sys=true end
ms.d_stoneUI.g_self.isOpen=true;ms.d_stoneUI.g_self.Lvlimit=10
""",(ROOT/'network_redirect/equipment_client.lua').read_text()]
 for key in ('level','reborn_layer','silver_coin','gold_coin'):lines.append('ms.d_mainUI.g_playerInfo.'+key+'='+str(role[key]))
 for p in b.inventory(role):
  mid,_,d=decode(p);lines.append('apply('+str(mid)+','+summon.lua(d)+')')
 lines.append("local function item(id) for _,i in ipairs(ms.d_packageUI.g_packageItemsInfo) do if i.id==id then return i end end error('missing '..id) end")
 lines.append('local gear='+str(gear)+';local stone='+str(stone))
 serial=100000
 def request(name,mid,check='',**kw):
  global serial
  serial+=1;packets=b.respond(encode(mid,dict(serial_num=serial,**kw)),dict(authenticated=True));body=[]
  for p in packets:
   m,_,d=decode(p);assert not(m==2998 and d['id']==55),(name,d)
   if m in (1032,1034,1035,2998):body.append('apply('+str(m)+','+summon.lua(d)+')')
  lines.append('step('+summon.lua(name)+',function() '+';'.join(body)+';'+check+' end)')
 def stoneop(name,op,target,ids=(),pos=0,check=''):
  request(name,1054,check=check,flag=op,des_id=target,equip_order=0,stone_pos=pos,src_count=len(ids),src_list=[dict(id=x) for x in ids])
 lines.append("step('stone_page',function() ms.d_mainUI.show();ms.d_stoneUI.showStoneLayer(ms.d_mainUI.g_mainUI.main_layer,1000,item(gear)) end)")
 stoneop('drill_callback',1,gear,check="assert(item(gear).drill_count==1)")
 stoneop('mosaic_callback',2,gear,[stone],1,check="assert(item(stone).owner_id==gear);assert(item(gear).stone1_level==9)")
 lines.append("step('upgrade_page',function() ms.d_stoneUpgradeUI.show(ms.d_stoneUI.g_stoneUI.main_layer,200,item(stone)) end)")
 stoneop('upgrade_callback',3,stone,[mat],1,check="assert(item(stone).level==10);assert(item(gear).stone1_level==10)")
 lines.append("step('stone_asc_page',function() ms.d_stoneUpgradeUI.call_back_close();ms.d_stoneCastUI.pressCast(ms.d_stoneUI.g_stoneUI.main_layer,item(stone),1000) end)")
 stoneop('stone_asc_callback',5,stone,pos=1,check="assert(item(stone).level==11)")
 stoneop('stone_refine_callback',5,stone,pos=1,check="assert(item(stone).level==12)")
 lines.append("step('return_stone_page',function() ms.d_mainUI.show();ms.d_stoneUI.showStoneLayer(ms.d_mainUI.g_mainUI.main_layer,1000,item(gear)) end)")
 stoneop('unload_callback',4,gear,[stone],1,check="assert(item(stone).owner_id==0);assert(item(gear).stone1_level==0)")
 lines.append("step('equipment_asc_page',function() ms.d_mainUI.show();ms.d_equipAscUI.show(ms.d_mainUI.g_mainUI.main_layer,1000,item(gear)) end)")
 request('equipment_asc_callback',1328,reborn_type=3,id=5,data=summon.lua(dict(equip_id=gear,equip_order=0)))
 lines.append("step('equipment_cast_page',function() ms.d_equipAscUI.pressClose();ms.d_equipCastUI.show(ms.d_mainUI.g_mainUI.main_layer,1000,item(gear)) end)")
 for lv in (2,3,4):request('equipment_cast_'+str(lv),1328,reborn_type=3,id=6,data=summon.lua(dict(equip_id=gear,equip_order=0)))
 lines.append("""local function restore()
 ms.d_u.main_server_send_msg=saved.send;ms.MS_report_error=saved.report;ms.d_info.show=saved.info
 ms.d_mainUI.g_playerInfo=saved.player;ms.d_lineupUI.g_characterInfo=saved.corts;ms.d_packageUI.g_packageItemsInfo=saved.items
 ms.d_roleRebornUI.g_reborn_condition=saved.realm
 ms.d_stoneUI.g_self.isOpen=saved.open;ms.d_stoneUI.g_self.Lvlimit=saved.limit
 ms.d_packageUI.g_isPackageSorted=false;ms.d_packageUI.sortItems();ms.d_lineupUI.sortcharacterInfo()
 ms.d_mainUI.show();equipment_fixture_restored=true
end
local scheduler=CCDirector:sharedDirector():getScheduler();local index=0;local handle
handle=scheduler:scheduleScriptFunc(function()
 if index>0 then equipment_fixture_results[index]={name=cases[index].name,errors=errors} end
 index=index+1
 if index>#cases then scheduler:unscheduleScriptEntry(handle);restore();return end
 errors='';local ok,err=xpcall(cases[index].run,debug.traceback);if not ok then errors=errors..'\\n'..tostring(err) end
end,2,false)
return 'scheduled '..#cases..' isolated original equipment client checks'
""")
 (ROOT/'.runtime/equipment-fixture.lua').write_text('\n'.join(lines));b.close()
