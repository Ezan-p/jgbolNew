"""Run real 3.87 UI callbacks with a disposable backend; never spend live items."""
import sys
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect.backend import Backend
from network_redirect import formation as f,summon,equipment_crafting as c
from network_redirect.protocol import encode,decode

with tempfile.TemporaryDirectory() as tmp:
 b=Backend(Path(tmp),18790,lambda *a,**k:None);role=b.profile()
 role.update(level=99,reborn_layer=4,silver_coin=1000000000,gold_coin=100000)
 def add(t,**kw):
  i=dict(id=f.new_id(role),attach_type=5,type_id=t,count=1,level=1);i.update(kw);role['attachments'].append(i);return i['id']
 fragment=add(6002,count=80);spirit=add(1313,count=100);add(1100,count=10);add(1369,count=100)
 trans=add(2001,level=30,drill_count=1,stone1_level=3);stone=add(1090,level=3,owner_id=trans,equip_pos=1)
 star=add(2002,level=20);star_mat=add(2002,level=5,advance_level=1)
 recycle=add(2004,level=5,advance_level=1)
 sale_tid=next(t for t,r in f.ITEMS.items() if int(r['main_type'])==1 and int(r['quality'])==3)
 sale=add(sale_tid,level=5)
 forge_tid=next(t for t,r in f.ITEMS.items() if int(r['main_type'])==1 and int(r['quality'])==4)
 forge_ids=[add(forge_tid) for _ in range(5)];exchange_ids=[add(forge_tid) for _ in range(5)];add(1008)
 b.save(role);role=b.profile()
 lines=["""local ms=assert(package.loaded.ms)
local saved={player=ms.d_mainUI.g_playerInfo,corts=ms.d_lineupUI.g_characterInfo,items=ms.d_packageUI.g_packageItemsInfo,send=ms.d_u.main_server_send_msg,report=ms.MS_report_error,info=ms.d_info.show}
ms.d_u.main_server_send_msg=function(...) return end
local errors='';crafting_fixture_results={};crafting_fixture_restored=false
ms.MS_report_error=function(e) errors=errors..'\\n'..tostring(e) end
ms.d_info.show=function(...) return end
local saleFixtureItems;local cases={};local function step(name,fn) cases[#cases+1]={name=name,run=fn} end
local function apply(mid,d)
 if mid==1032 then ms.d_event_mgr.msg_modify_attr_1032(nil,d,nil)
 elseif mid==1034 then ms.d_lineupUI.getDateFormServer(d)
 elseif mid==1035 then ms.d_packageUI.getDateFormServer(d)
 elseif mid==2998 then ms.d_event_mgr.msg_common_event_2998(nil,d,nil) end
end
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
if ms.d_batchSaleUI._localSaleRestore then ms.d_batchSaleUI._localSaleRestore() end
if ms.d_forgeUI._localCraftingRestore then ms.d_forgeUI._localCraftingRestore() end
""",(ROOT/'network_redirect/equipment_client.lua').read_text()]
 for key in ('level','reborn_layer','silver_coin','gold_coin'):lines.append('ms.d_mainUI.g_playerInfo.'+key+'='+str(role[key]))
 for p in b.inventory(role):
  mid,_,d=decode(p);lines.append('apply('+str(mid)+','+summon.lua(d)+')')
 lines.append("local function item(id) for _,i in ipairs(ms.d_packageUI.g_packageItemsInfo) do if i.id==id then return i end end end")
 lines.append("local function parent() return ms.d_mainUI.g_mainUI.main_layer end")
 serial=200000
 def step(name,code):lines.append('step('+summon.lua(name)+',function() '+code+' end)')
 def request(name,mid,check='',**kw):
  global serial
  serial+=1;packets=b.respond(encode(mid,dict(serial_num=serial,**kw)),dict(authenticated=True));body=[]
  for p in packets:
   m,_,d=decode(p);assert not(m==2998 and d['id']==55),(name,d)
   if m in (1032,1034,1035) or m==2998 and d['id'] in (6,7,16,98,116,124,201):body.append('apply('+str(m)+','+summon.lua(d)+')')
  step(name,';'.join(body)+';'+check)
 step('main_page','ms.d_mainUI.show()')
 request('forge_query_and_page',1055,flag=0,check="assert(ms.d_forgeUI.canJoin());assert(not ms.d_forgeUI.isNeedUpdateList())")
 request('appointed_compose_callback',1053,compose_type=2,equip_type=2001,equip_quality=5,material_quality=4,material_count=5,material_list=[dict(id=i) for i in forge_ids])
 step('exchange_page','ms.d_forgeUI.ForgeTypeBtnPressed(3);ms.d_forgeUI.targetChanged(1)')
 request('exchange_compose_callback',1053,compose_type=3,equip_type=6001,equip_quality=4,material_quality=4,material_count=5,material_list=[dict(id=i) for i in exchange_ids])
 step('fragment_page','ms.d_equipPieceUI.show(parent(),6002)')
 request('fragment_compose_callback',1053,compose_type=1,equip_type=2,equip_quality=5,material_quality=5,material_count=1,material_list=[dict(id=fragment)],check='assert(item(%d).count==40)'%fragment)
 step('smith_page','ms.d_mainUI.show();ms.d_mainUI.g_allBoardlayer={};parent():removeChildByTag(ms.d_mainUI.boardID.smith,true);ms.d_smithUI.show(assert(ms.d_data.getTransInfoByTypeid(1313)))')
 # Select a real original material recipe before its animated callback.
 step('smith_select','ms.d_smithUI.g_smithUI.transInfo=assert(ms.d_data.getTransInfoByTypeid(1313));ms.d_smithUI.categoryPressed(1,true);assert(ms.d_smithUI.g_smithUI.transInfo.src_material.attach_type==1313)')
 request('material_compose_callback',1074,flag=2,num=1,des_type=1,count=1,id_list=[dict(id=spirit)],check='assert(item(%d).count==90)'%spirit)
 step('recycle_page','ms.d_mainUI.show();ms.d_cortegeRecycleUI.show(parent());ms.d_cortegeRecycleUI.changeEquip()')
 request('recycle_callback',1074,flag=1,num=1,des_type=1,count=1,id_list=[dict(id=recycle)],check='assert(not item(%d))'%recycle)
 step('transform_page','ms.d_mainUI.show();ms.d_equipTransUI.show(parent())')
 request('transform_callback',1225,state=2,item_id=trans,check='assert(not item(%d));assert(item(%d).owner_id==0)'%(trans,stone))
 step('six_star_page','ms.d_mainUI.show();ms.d_skillUpgradeUI.create_wshengxing({skill_info=item(%d),from_btn=120,parent_layer=parent(),isNeedUpdate=true})'%star)
 request('six_star_callback',1079,equipid=star,equip_order=0,material_equipid=star_mat,check='assert(item(%d).star_level==1);assert(not item(%d))'%(star,star_mat))
 step('batch_sale_page','ms.d_mainUI.show();saleFixtureItems={item(%d)};ms.d_batchSaleUI.show(saleFixtureItems)'%sale)
 request('batch_sale_callback',1056,data=summon.lua(dict(equip_list=[sale])),check='assert(not item(%d));assert(#saleFixtureItems==0)'%sale)
 lines.append("""local function restore()
 ms.d_u.main_server_send_msg=saved.send;ms.MS_report_error=saved.report;ms.d_info.show=saved.info
 ms.d_mainUI.g_playerInfo=saved.player;ms.d_lineupUI.g_characterInfo=saved.corts;ms.d_packageUI.g_packageItemsInfo=saved.items
 ms.d_packageUI.g_isPackageSorted=false;ms.d_packageUI.sortItems();ms.d_lineupUI.sortcharacterInfo()
 ms.d_mainUI.show();crafting_fixture_restored=true
end
local scheduler=CCDirector:sharedDirector():getScheduler();local index=0;local handle
handle=scheduler:scheduleScriptFunc(function()
 if index>0 then crafting_fixture_results[index]={name=cases[index].name,errors=errors} end
 index=index+1
 if index>#cases then scheduler:unscheduleScriptEntry(handle);restore();return end
 errors='';local ok,err=xpcall(cases[index].run,debug.traceback);if not ok then errors=errors..'\\n'..tostring(err) end
end,3,false)
return 'scheduled '..#cases..' isolated original crafting client checks'
""")
 (ROOT/'.runtime/crafting-fixture.lua').write_text('\n'.join(lines));b.close()
