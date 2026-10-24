"""Build an isolated original-client UI/response fixture; never edits live save."""
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from network_redirect.backend import Backend, login_fields
from network_redirect import formation as f, reborn as r, reborn_stars as stars, summon
from network_redirect.protocol import encode, decode

ROOT=Path(__file__).resolve().parents[2]
with tempfile.TemporaryDirectory() as tmp:
 b=Backend(Path(tmp),18790,lambda *a,**k:None);role=b.profile()
 role.update(level=99,reborn_layer=4,silver_coin=100000000,gold_coin=100000)
 role['corteges']=[summon.companion(role,5022)];c=role['corteges'][0];c.update(order=1,level=165)
 for t in [1329,1330,1333,1334,1335,1310,10000,10101,10117,10118,10300]:summon.add_item(role,t,10000)
 eq=dict(id=f.new_id(role),attach_type=5,type_id=2001,count=1,level=1,advance_level=10,equip_order=0,equip_pos=0)
 role['attachments'].append(eq);b.save(role);role=b.profile()
 innate=next(x for x in role['attachments'] if x.get('innate_owner_id')==c['id']);innate['level']=10;sid=innate['id']
 materials=[]
 for tid in (42,43):
  ident=f.new_id(role);materials.append(ident);role['attachments'].append(dict(id=ident,attach_type=6,type_id=tid,count=1,level=1))
 star_id=f.new_id(role);role['attachments'].append(dict(id=star_id,attach_type=5,type_id=10301,count=1,level=1))
 b.save(role);role=b.profile()
 # Decode inventory so every optional field is present exactly as on the wire.
 inventory=[(decode(p)[0],decode(p)[2]) for p in b.inventory(role)]
 header="""local ms=assert(package.loaded.ms)
local saved={player=ms.d_mainUI.g_playerInfo,corts=ms.d_lineupUI.g_characterInfo,items=ms.d_packageUI.g_packageItemsInfo,config=ms.d_roleRebornUI.g_reborn_condition,send=ms.d_u.main_server_send_msg,report=ms.MS_report_error,info=ms.d_info.show}
ms.d_u.main_server_send_msg=function(...) return end
local errors='';reborn_fixture_results={};reborn_fixture_restored=false
ms.MS_report_error=function(e) errors=errors..'\\n'..tostring(e) end
ms.d_info.show=function(message,...) if message==ms.d_hz.gethz('operation_failed') then errors=errors..'\\noperation_failed toast' end;return saved.info(message,...) end
local cases={}
local function step(name,fn) cases[#cases+1]={name=name,run=fn} end
local function apply(mid,d)
 if mid==1032 then ms.d_event_mgr.msg_modify_attr_1032(nil,d,nil)
 elseif mid==1034 then ms.d_lineupUI.getDateFormServer(d)
 elseif mid==1035 then ms.d_packageUI.getDateFormServer(d)
 elseif mid==2998 then
  local p=assert(loadstring('return '..d.data))()
  if d.id==172 then ms.d_ascensionUI.onGetResult(p)
  elseif d.id==183 then ms.d_wakeUI.onGetResult(p)
  elseif d.id==186 then ms.d_wakeUI.onEquipResult(p)
  elseif d.id==187 then ms.d_wakeUI.onUnloadResult(p)
  elseif d.id==188 then ms.d_wakeUI.onUpgradeResult(p)
  elseif d.id==189 then ms.d_wakeUI.onResolveResult(p)
  elseif d.id==191 then ms.d_wakeUI.reStoreAwakenSkillResult(p)
  elseif d.id==190 then ms.d_wakeUI.onDivineResult(p)
  end
 end
end
"""
 lines=[header,"ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)"]
 for key in ('level','reborn_layer','maxlayer_reborn_count','silver_coin','gold_coin'):lines.append('ms.d_mainUI.g_playerInfo.'+key+'='+str(role[key]))
 lines.append('ms.d_roleRebornUI.initData('+summon.lua(r.client_config(b.reborn_rules))+')')
 lines.append('ms.d_wakeUI.onGetConfig({is_open=true,flag=true})')
 for mid,d in inventory:lines.append('apply('+str(mid)+','+summon.lua(d)+')')
 lines+= ["local function cort() return ms.d_lineupUI.g_characterInfo[1] end", "local function equip() for _,i in ipairs(ms.d_packageUI.g_packageItemsInfo) do if i.id=="+str(eq['id'])+" then return i end end end"]
 lines.append("step('realm_page',function() ms.d_mainUI.show();ms.d_roleRebornUI.show() end)")
 lines.append("step('realm_details',function() ms.d_roleRebornUI.MenuPopRebornLayer() end)")
 lines.append("step('cortege_ascension',function() ms.d_roleRebornUI.menuClose();ms.d_roleRebornUI.MenuPopCharacterRebornLayer() end)")
 serial=100000
 def request(name,mid,**kw):
  global serial
  serial+=1;packets=b.respond(encode(mid,dict(serial_num=serial,**kw)),dict(authenticated=True))
  body=[]
  for packet in packets:
   m,_,d=decode(packet)
   assert not (m==2998 and d['id']==55), (name,d)
   if m in (1032,1034,1035,2998):body.append('apply('+str(m)+','+summon.lua(d)+')')
  lines.append("step("+summon.lua(name)+",function() "+';'.join(body)+" end)")
 request('first_vein_callback',1328,reborn_type=2,id=1,data=summon.lua(dict(cortege_id=c['id'],material_list={10000:300})))
 role=b.profile();role['corteges'][0]['reborn_vein_level']=9;b.save(role)
 lines.append("step('nine_veins',function() cort().reborn_vein_level=9;ms.d_ascensionUI.onCortChanged() end)")
 request('rebirth_callback',1328,reborn_type=2,id=2,data=summon.lua(dict(cortege_id=c['id'])))
 lines.append("step('attribute_types',function() ms.d_ascensionUI.showChangeLayer() end)")
 request('attribute_change_callback',1328,reborn_type=2,id=3,data=summon.lua(dict(cortege_id=c['id'],des_type=1)))
 lines.append("step('equipment_rebirth',function() ms.d_ascensionUI.pressClose();ms.d_equipAscUI.show(ms.d_mainUI.g_mainUI.main_layer,1000,equip()) end)")
 request('equipment_rebirth_callback',1328,reborn_type=3,id=5,data=summon.lua(dict(equip_id=eq['id'],equip_order=0)))
 lines.append("step('equipment_cast',function() ms.d_equipAscUI.pressClose();ms.d_equipCastUI.show(ms.d_mainUI.g_mainUI.main_layer,1000,equip()) end)")
 request('equipment_cast_callback',1328,reborn_type=3,id=6,data=summon.lua(dict(equip_id=eq['id'],equip_order=0)))
 lines.append("step('divination_enter',function() ms.d_equipCastUI.pressClose();ms.d_wakeUI.enterDivine(ms.d_mainUI.g_mainUI.main_layer) end)")
 request('divination_query',1337,event_type=1,data='{}')
 request('divination_single',1337,event_type=2,data='{}')
 request('divination_quick',1337,event_type=3,data='{}')
 request('divination_collect',1337,event_type=5,data='{}')
 lines.append("step('star_package',function() ms.d_wakeUI.showStarPackage() end)")
 lines.append("step('star_resolve',function() ms.d_wakeUI.showStarResolve() end)")
 wake_inventory=[(decode(p)[0],decode(p)[2]) for p in b.inventory(b.profile())]
 lines.append("step('awakening_page',function() ms.d_mainUI.show();ms.d_charPositionUI.show();ms.d_charPositionUI.tapHeadButton(1);local w=ms.d_wakeUI;w.g_self.des_char=cort();for _,i in ipairs(ms.d_packageUI.g_packageItemsInfo) do if i.id=="+str(sid)+" then w.g_self.des_skill=i end end;w.enter(ms.d_mainUI.g_mainUI.main_layer,w.g_self.des_skill) end)")
 request('awakening_callback',1332,des_id=sid,awaken_type=1,material_count=2,material_list=[dict(id=i) for i in materials])
 request('star_equip_callback',1338,des_cortege_id=c['id'],ext_star_id=star_id,element_id=1,replace=0)
 lines.append("step('star_upgrade_page',function() for _,i in ipairs(ms.d_packageUI.g_packageItemsInfo) do if i.id=="+str(star_id)+" then ms.d_wakeUI.showStarUpgrade(ms.d_wakeUI.g_wakeUI.main_layer,i) end end end)")
 request('star_upgrade_callback',1340,ext_star_id=star_id,cost_count=5)
 request('star_unload_callback',1339,des_cortege_id=c['id'],element_id=1)
 lines.append("step('awaken_restore_page',function() ms.d_wakeUI.showTalantRestore(ms.d_wakeUI.g_wakeUI.main_layer,ms.d_wakeUI.g_self.des_skill.awaken) end)")
 request('awaken_restore_callback',1342,des_id=sid)
 if '--wake-only' in sys.argv:
  lines.append('local filtered={};for i=20,#cases do filtered[#filtered+1]=cases[i] end;cases=filtered')
  for mid,d in wake_inventory:lines.append('apply('+str(mid)+','+summon.lua(d)+')')
 lines.append("""local function restore()
 ms.d_u.main_server_send_msg=saved.send;ms.MS_report_error=saved.report;ms.d_info.show=saved.info
 ms.d_mainUI.g_playerInfo=saved.player
 ms.d_lineupUI.g_characterInfo=saved.corts;ms.d_packageUI.g_packageItemsInfo=saved.items
 ms.d_roleRebornUI.g_reborn_condition=saved.config
 ms.d_packageUI.g_isPackageSorted=false;ms.d_packageUI.sortItems();ms.d_lineupUI.sortcharacterInfo()
 ms.d_mainUI.show();reborn_fixture_restored=true
end
local scheduler=CCDirector:sharedDirector():getScheduler();local index=0;local handle
handle=scheduler:scheduleScriptFunc(function()
 if index>0 then reborn_fixture_results[index]={name=cases[index].name,errors=errors} end
 index=index+1
 if index>#cases then scheduler:unscheduleScriptEntry(handle);restore();return end
 errors='';local ok,err=xpcall(cases[index].run,debug.traceback);if not ok then errors=errors..'\\n'..tostring(err) end
end,4,false)
return 'scheduled '..#cases..' original client checks; isolated fixture, no live save writes'
""")
 (ROOT/'.runtime/reborn-fixture.lua').write_text('\n'.join(lines))
 b.close()
