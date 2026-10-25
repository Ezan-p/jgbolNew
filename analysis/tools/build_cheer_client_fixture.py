"""Replay isolated backend Bagua packets into original 3.87 UI; no live save writes."""
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from network_redirect import cheer, formation as f, summon, reborn
from network_redirect.backend import Backend
from network_redirect.protocol import encode, decode
ROOT = Path(__file__).resolve().parents[2]
with tempfile.TemporaryDirectory() as tmp:
    b = Backend(Path(tmp), 18790, lambda *a, **k: None)
    role = b.profile(); role.update(level=99, reborn_layer=4, gold_coin=100000)
    for t in (1015,1016,1017,1206): summon.add_item(role,t,100000)
    for t in (5002,5003): role['corteges'].append(summon.companion(role,t))
    item = dict(id=f.new_id(role),type_id=22,attach_type=6,count=1,level=1,equip_order=0,equip_pos=0)
    role['attachments'].append(item)
    f.prepare(role,b.formation_rules);b.save(role);role=b.profile()
    ids=[c['id'] for c in role['corteges']]
    lines=[r'''local ms=assert(package.loaded.ms)
local ui=ms.d_cheerSquadUI
local saved={player=ms.d_mainUI.g_playerInfo,corts=ms.d_lineupUI.g_characterInfo,items=ms.d_packageUI.g_packageItemsInfo,send=ms.d_u.main_server_send_msg,report=ms.MS_report_error,self=ui.g_self,view=ui.g_cheerSquadUI,realm=ms.d_roleRebornUI.g_reborn_condition}
ms.d_u.main_server_send_msg=function() end
local errors='';cheer_fixture_results={};cheer_fixture_restored=false
ms.MS_report_error=function(e) errors=errors..'\n'..tostring(e) end
ui.g_self=ms.d_c.table_copy(saved.self);ui.g_cheerSquadUI={}
local cases={}
local function step(name,fn) cases[#cases+1]={name=name,run=fn} end
local function apply(mid,d)
 if mid==1032 then ms.d_event_mgr.msg_modify_attr_1032(nil,d,nil)
 elseif mid==1034 then ms.d_lineupUI.getDateFormServer(d)
 elseif mid==1035 then ms.d_packageUI.getDateFormServer(d)
 elseif mid==2998 and d.id==95 then ui.onGetCheerResults(assert(loadstring('return '..d.data))()) end
end
''']
    lines.append('ms.d_mainUI.g_playerInfo='+summon.lua(dict(role, role_id=role['role_id'])))
    lines.append('ui.initCost('+summon.lua(cheer.client_config(b.cheer_rules))+')')
    rc=reborn.client_config(b.reborn_rules);rc[4]['rights']['open_cheer_skill']=True
    lines.append('ms.d_roleRebornUI.initData('+summon.lua(rc)+')')
    for packet in b.inventory(role):
        m,_,d=decode(packet); lines.append('apply('+str(m)+','+summon.lua(d)+')')
    lines.append("step('open_ui',function() ui.show(ms.d_mainUI.g_mainUI.main_layer,1) end)")
    serial=100000
    def request(name,flag,order=1,identity=0,pos=9):
        global serial
        serial+=1
        packets=b.respond(encode(1087,dict(serial_num=serial,flag=flag,order=order,id=identity,client_flag=pos)),{'authenticated':True})
        body=[]
        for packet in packets:
            m,_,d=decode(packet)
            assert not (m==2998 and d['id']==55),(name,d)
            if m in (1032,1034,1035,2998): body.append('apply('+str(m)+','+summon.lua(d)+')')
        lines.append('step('+summon.lua(name)+',function() '+';'.join(body)+' end)')
    request('open_third_positive',8,3)
    lines.append("step('return_first',function() ui.gotoPosition(1) end)")
    request('supporter',1,identity=ids[1]);request('target',2,identity=ids[0])
    for n in range(2,11):request('upgrade_'+str(n),3)
    request('wash_preview',4);request('wash_cancel',5)
    request('wash_preview_again',4);request('wash_confirm',6)
    request('skill_open_2',9,pos=2);request('skill_open_3',9,pos=3)
    request('skill_equip',11,identity=item['id'],pos=2)
    lines.append("step('skill_upgrade_panel',function() ui.g_self.last_advance_tag=2;ui.showSkillAdvance(2) end)")
    request('skill_upgrade',10)
    request('skill_wash',13,pos=2);request('skill_wash_confirm',15)
    request('skill_unload',11,pos=2)
    request('innate_query',12,identity=ids[1])
    request('open_reverse',8,9);request('reverse_supporter',1,9,ids[2]);request('reverse_target',2,9,ids[0])
    for n in range(2,11):request('reverse_upgrade_'+str(n),3,9)
    request('reverse_skill_open',9,9,pos=2)
    request('reverse_skill_equip',11,9,identity=item['id'],pos=2)
    request('reverse_wash',4,9);request('reverse_wash_confirm',6,9)
    request('reverse_skill_wash',13,9,pos=2);request('reverse_skill_wash_cancel',14,9)
    request('reverse_skill_unload',11,9,pos=2)
    lines.append(r'''local function restore()
 pcall(ui.forceClose)
 ms.d_mainUI.g_playerInfo=saved.player;ms.d_lineupUI.g_characterInfo=saved.corts;ms.d_packageUI.g_packageItemsInfo=saved.items
 ui.g_self=saved.self;ui.g_cheerSquadUI=saved.view;ms.d_roleRebornUI.g_reborn_condition=saved.realm
 ms.d_packageUI.g_isPackageSorted=false;ms.d_packageUI.sortItems();ms.d_lineupUI.sortcharacterInfo()
 ms.d_u.main_server_send_msg=saved.send;ms.MS_report_error=saved.report
 ms.d_mainUI.show();cheer_fixture_restored=true
end
local scheduler=CCDirector:sharedDirector():getScheduler();local index=0;local handle
handle=scheduler:scheduleScriptFunc(function()
 if index>0 then cheer_fixture_results[index]={name=cases[index].name,errors=errors} end
 index=index+1
 if index>#cases then scheduler:unscheduleScriptEntry(handle);local ok,e=pcall(restore);if not ok then cheer_restore_error=tostring(e) end;return end
 errors='';local ok,e=xpcall(cases[index].run,debug.traceback);if not ok then errors=errors..'\n'..tostring(e) end
end,1,false)
return 'scheduled '..#cases..' isolated original Bagua UI checks'
''')
    (ROOT/'.runtime/cheer-fixture.lua').write_text('\n'.join(lines));b.close()
