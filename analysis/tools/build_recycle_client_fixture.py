"""Isolated backend responses through original 3.87 UI; no live save mutations."""
import sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from network_redirect import formation as f,summon
from network_redirect.backend import Backend,login_fields
from network_redirect.protocol import encode,decode
lines=[r'''local ms=assert(package.loaded.ms);local ui=ms.d_cortegeRecycleUI
local saved={player=ms.d_mainUI.g_playerInfo,corts=ms.d_lineupUI.g_characterInfo,items=ms.d_packageUI.g_packageItemsInfo,self=ui.g_self,view=ui.g_RecycleUI,send=ms.d_u.main_server_send_msg,report=ms.MS_report_error,current=ms.d_activityUI.g_currentActivity}
local parent=CCLayer:create();ms.d_mainUI.g_mainUI.main_layer:addChild(parent,999)
local errors='';local cases={};recycle_fixture_results={};recycle_fixture_finished=false
local sent={};ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
ms.MS_report_error=function(e) errors=errors..'\n'..tostring(e) end
ui.g_self=ms.d_c.table_copy(saved.self);ui.g_self.selected_list={};ui.g_RecycleUI={}
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player);ms.d_mainUI.g_playerInfo.level=60
local function step(name,fn) cases[#cases+1]={name=name,run=fn} end
local function apply(mid,d)
 if mid==1034 then ms.d_lineupUI.getDateFormServer(d)
 elseif mid==1035 then ms.d_packageUI.getDateFormServer(d)
 elseif mid==2998 and (d.id==64 or d.id==116) then ms.d_event_mgr.msg_common_event_2998(nil,d,nil) end
end
''']
with tempfile.TemporaryDirectory() as tmp:
 b=Backend(Path(tmp),18770,lambda *a,**kw:None);r=b.profile();r['level']=60
 for tid in (4064,4065,4066,4067,4022):r['corteges'].append(summon.companion(r,tid))
 ids=[c['id'] for c in r['corteges'][-5:]]
 gears=[]
 for main in (1,2,3):
  tid=next(t for t,c in f.ITEMS.items() if int(c['main_type'])==main and int(c['quality'])==4)
  i=dict(id=f.new_id(r),type_id=tid,attach_type=5,level=1,count=1);r['attachments'].append(i);gears.append(i['id'])
 f.prepare(r,b.formation_rules);b.save(r)
 for p in b.inventory(r):
  m,_,d=decode(p);lines.append('apply('+str(m)+','+summon.lua(d)+')')
 lines += [r'''step('entry',function() ui.show(parent);assert(ui.g_RecycleUI.main_layer) end)
step('cortege_tab',function() ui.showMainLayer(1);assert(ui.g_RecycleUI.cortege5BtnTable) end)
step('select_and_fate_preview',function()
 ui.createSkillMutilSelectLayer();assert(#ui.g_self.cortegeInfos==5)
 ui.g_RecycleUI.main_layer:removeChildByTag(ui.g_self.tags.Choose,true)
 ui.g_self.selected_list={true,true,true,true,true};ui.fillInHeadBtns()
 assert(ui.checkHasFate());assert(#ui.g_self.last_selected_id==5)
end)
step('original_1086_send',function()
 ui.sendCortegeRecycle();assert(sent[#sent].mid==1086);assert(sent[#sent].data.flag==0)
end)
''']
 def response(name,mid,req,pre=''):
  packets=b.respond(encode(mid,dict(serial_num=100000+len(lines),**req)),{'authenticated':True})
  lines.append('step('+summon.lua(name)+',function() '+pre)
  for p in packets:
   m,_,d=decode(p)
   assert not(m==2998 and d['id']==55),d
   if m in (1034,1035,2998):lines.append('apply('+str(m)+','+summon.lua(d)+')')
  lines.append('end)')
 response('consume_and_reward_animation',1086,dict(flag=0,**{'c%d'%(n+1):v for n,v in enumerate(ids)}))
 lines += [r'''step('reselect_after_consumption',function() assert(#ui.g_self.selected_list==0);ui.createSkillMutilSelectLayer();assert(#ui.g_self.cortegeInfos==0) end)
step('equipment_tab',function() ui.pressClose();ui.showMainLayer(2);assert(ui.g_RecycleUI.main_layer) end)
step('equipment_select_all_and_preview',function() ui.showEquipChooseLayer();ui.oneKeyChoose();ui.changeEquip();assert(next(ui.g_RecycleUI.chosenEquips)) end)
step('original_1074_confirmation_and_send',function()
 local original=ms.d_quitUI.createYesNoByStyle;local accept
 ms.d_quitUI.createYesNoByStyle=function(parent,style,yes,...) accept=yes;return original(parent,style,yes,...) end
 local ok,e=xpcall(ui.sendEquipRecycle,debug.traceback);ms.d_quitUI.createYesNoByStyle=original
 assert(ok,e);assert(accept);accept()
 assert(sent[#sent].mid==1074);assert(sent[#sent].data.count==3)
 assert(sent[#sent].data.flag==1 and sent[#sent].data.num==1)
end)
''']
 response('equipment_reward_animation',1074,dict(flag=1,num=1,des_type=1,count=3,id_list=[dict(id=i) for i in gears]))
 lines += [r'''step('equipment_empty_and_return',function() ui.showEquipChooseLayer();ui.pressClose();ui.pressClose() end)
step('reopen',function() ui.show(parent);ui.showMainLayer(1);ui.pressClose();ui.pressClose() end)
''']
 b.close()
lines.append(r'''local function restore()
 parent:removeFromParentAndCleanup(true)
 ms.d_mainUI.g_playerInfo=saved.player;ms.d_lineupUI.g_characterInfo=saved.corts;ms.d_packageUI.g_packageItemsInfo=saved.items
 ui.g_self=saved.self;ui.g_RecycleUI=saved.view;ms.d_activityUI.g_currentActivity=saved.current
 ms.d_packageUI.g_isPackageSorted=false;ms.d_packageUI.sortItems();ms.d_lineupUI.sortcharacterInfo()
 ms.d_u.main_server_send_msg=saved.send;ms.MS_report_error=saved.report
 recycle_fixture_finished=true
end
local scheduler=CCDirector:sharedDirector():getScheduler();local index=0;local handle
handle=scheduler:scheduleScriptFunc(function()
 if index>0 then recycle_fixture_results[index]={name=cases[index].name,errors=errors} end
 index=index+1
 if index>#cases then scheduler:unscheduleScriptEntry(handle);restore();return end
 errors='';local ok,e=xpcall(cases[index].run,debug.traceback);if not ok then errors=errors..'\n'..tostring(e) end
end,4,false)
return 'scheduled '..#cases..' recycle cases'
''')
(ROOT/'.runtime/recycle-fixture.lua').write_text('\n'.join(lines))
print('Built original-client recycle fixture')
