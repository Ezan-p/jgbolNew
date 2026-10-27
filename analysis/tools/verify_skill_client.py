"""Original Cocos spell list, growth callbacks and chunked inventory replay.

Temporary backend only; outgoing client requests are intercepted; live state restored.
"""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis/tools')]
from network_redirect import formation as f, summon, activity_visit, equipment_crafting
from network_redirect.backend import Backend
from network_redirect.protocol import encode,decode
from android_emulator.config import load_config,device_environment
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR


def fixture():
    with tempfile.TemporaryDirectory() as tmp:
        b=Backend(Path(tmp),18790,lambda *a,**k:None)
        role=b.profile();role.update(level=99,gold_coin=10000)
        equipment_crafting.grant(role,[(6,t,1,1) for ts in activity_visit.SKILLS.values() for t in ts])
        # Force target and materials into later 128-entry inventory packets.
        equipment_crafting.grant(role,[(6,212,1,140)])
        equipment_crafting.grant(role,[(6,206,1,1)])
        b.save(role);role=b.profile();target=role['attachments'][-1]['id']
        mats=[i['id'] for i in role['attachments'] if i['attach_type']==6 and i['type_id']==212][:3]
        def packets(ps):
            out=[]
            for pos,p in enumerate(ps):
                m,_,d=decode(p)
                out.append("skillTest.next="+str(decode(ps[pos+1])[0] if pos+1<len(ps) else 0))
                if m in (1034,1035):out.append('apply(%d,%s)'%(m,summon.lua(d)))
                elif m==2998 and d['id']==2:out.append('ms.d_event_mgr.msg_common_event_2998(nil,%s,nil)'%summon.lua(d))
            return ';'.join(out)
        initial=packets(b.inventory(role))
        stages=[]
        for n,roll in enumerate((99,0,0)):
            with patch('network_redirect.formation.secrets.randbelow',return_value=roll):
                replies=b.respond(encode(1071,dict(serial_num=100+n,data=summon.lua(dict(des_skill_id=target,src_skill_list=[mats[n]])))),dict(authenticated=True))
            stages.append(packets(replies))
        b.close()
        return initial,stages,target


def main():
    import frida
    c=load_config(ROOT/'game.json');pid=next(p for p,n in processes(c).items() if n==c['package'])
    session=frida.get_device(c['serial'],timeout=10).attach(pid)
    evaluator=LUA_EVALUATOR.replace('pending={code,resolve};',"const task={code,resolve};pending=task;setTimeout(()=>{if(pending===task){pending=null;resolve({status:-1,result:'No Lua frame'});}},15000);")
    script=session.create_script(evaluator)
    dest=ROOT/'analysis/evidence/skills';dest.mkdir(parents=True,exist_ok=True)
    report=dict(native_cocos=True,live_account_resources_changed=False,network_sends_captured=True,checks=[])
    def evaluate(code):
        raw=script.exports_sync.evaluate(code)
        if raw.get('status')!=0:raise RuntimeError(raw)
        return raw['result']
    def check(name,code):
        evaluate('local ms=package.loaded.ms;local ui=ms.d_packageUI;'+code+';assert(#skillTest.errors==0,table.concat(skillTest.errors,"\\n"));return "ok"')
        report['checks'].append(name)
    def capture(name):
        time.sleep(.6)
        r=subprocess.run([str(c['adb_path']),'-s',c['serial'],'exec-out','screencap','-p'],env=device_environment(c),capture_output=True,check=True,timeout=15)
        (dest/name).write_bytes(r.stdout)
    initial,stages,target=fixture()
    try:
        script.load()
        evaluate('assert(not _skillTestTick);_skillTestTick=CCDirector:sharedDirector():getScheduler():scheduleScriptFunc(function() end,0.1,false);return "tick"')
        source=(ROOT/'tests/skill_client_regression.lua').read_text().replace('-- INSTALL_PATCH',(ROOT/'network_redirect/skill_client.lua').read_text())
        out=evaluate('local saved=package.loaded.ms;local ok,result=pcall(function() '+source+' end);package.loaded.ms=saved;if not ok then error(result) end;return table.concat(result,"\\n")')
        report['unit_checks']=out.splitlines()
        evaluate('assert(loadstring('+summon.lua(summon.client_source(summon.load_rules()))+'));return "compiled"')
        evaluate('''local ms=package.loaded.ms;local ui=ms.d_packageUI
assert(not skillTest)
local saved={};for _,t in ipairs({ui,ms.d_skillUpgradeUI,ms.d_u,ms.d_lineupUI,ms.d_mainUI,ms.d_event_mgr}) do
 local copy={};for k,v in pairs(t) do copy[k]=v end;saved[t]=copy
end
local oldReport=ms.MS_report_error
skillTest={errors={}}
ms.MS_report_error=function(e) table.insert(skillTest.errors,tostring(e)) end
ms.d_u.main_server_send_msg=function() end
ms.d_event_mgr.getNextPackageType=function() return skillTest.next or 0 end
skillTest.restore=function()
 if ui._localSkillRestore and ui._localSkillRestore~=saved[ui]._localSkillRestore then ui._localSkillRestore() end
 local currentMain=ms.d_mainUI.g_mainUI
 for t,copy in pairs(saved) do for k in pairs(t) do t[k]=nil end;for k,v in pairs(copy) do t[k]=v end end
 ms.d_mainUI.g_mainUI=currentMain
 ms.MS_report_error=oldReport
 ui.g_isInPackage=false;ui.g_packageItemsInfo=saved[ui].g_packageItemsInfo
 ui.g_isPackageSorted=false;ui.sortItems();ms.d_lineupUI.sortcharacterInfo();ms.d_loginUI.g_currentSence=ms.d_loginUI.senceID.adventure;ms.d_mainUI.show()
 skillTest=nil
end
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(ms.d_mainUI.g_playerInfo)
ms.d_skillUpgradeUI.g_self=ms.d_c.table_copy(ms.d_skillUpgradeUI.g_self)
if ui._localSkillRestore then ui._localSkillRestore() end
ui.g_packageItemsInfo={};ui.g_isInPackage=false
local create=ms.d_u.createByStyle
ms.d_u.createByStyle=function(style,...)
 local node=create(style,...)
 if skillTest.captureLabels and style.type=='label' then
  table.insert(skillTest.labels,{node=node,x=style.x,y=style.y,text=tostring(style.string)})
 end
 return node
end
skillTest.label=function(text)
 for _,entry in ipairs(skillTest.labels or {}) do if entry.node:getString()==text then return true end end
 local values={};for _,entry in ipairs(skillTest.labels or {}) do table.insert(values,entry.node:getString()) end
 error('missing rendered label '..text..': '..table.concat(values,','))
end
skillTest.apply=function(mid,d)
 if mid==1034 then ms.d_lineupUI.getDateFormServer(d) else ui.getDateFormServer(d) end
end
skillTest.item=function(id) for _,i in ipairs(ui.g_packageItemsInfo) do if i.id==id then return i end end end
return 'isolated'
''')
        evaluate((ROOT/'network_redirect/skill_client.lua').read_text()+"\nreturn 'installed'")
        evaluate('''local upgrade=package.loaded.ms.d_skillUpgradeUI;local result=upgrade.showServerRet
upgrade.showServerRet=function(data)
 skillTest.labels={};skillTest.captureLabels=true
 local ok,err=pcall(result,data);skillTest.captureLabels=false
 if not ok then error(err) end
end
return 'render capture installed' ''')
        evaluate('local ms=package.loaded.ms;ms.d_loginUI.g_currentSence=ms.d_loginUI.senceID.adventure;ms.d_mainUI.show();return "scene"')
        time.sleep(.6)
        check('empty list explains innate skills and acquisition', 'ui.sortItems();ui.show();ui.showPackage(4);assert(ui.g_packageUI.board_layer:getChildByTag(91106),"missing hint")')
        capture('empty.png')
        check('all 54 templates and chunked list render', 'local apply=skillTest.apply;'+initial+';ui.showPackage(4);assert(not ui.g_packageUI.board_layer:getChildByTag(91106),"hint still visible inbag="..tostring(ui.g_isInPackage).." items="..#ui.g_packageItemsInfo.." first="..tostring(ui.g_packageItemsInfo[2] and ui.g_packageItemsInfo[2].protogenic));local types={};for _,i in ipairs(ui.packageItemsInfo) do assert(i.protogenic==0,"innate leaked");types[i.type_id]=true end;local n=0;for _ in pairs(types) do n=n+1 end;assert(n==54,tostring(n));assert(#ui.g_reorgItemsInfo[6]==196,"total="..#ui.g_reorgItemsInfo[6])')
        capture('list.png')
        check('original upgrade window rebinds a copied formation selection',f'skillTest.selected=skillTest.item({target});skillTest.detached=ms.d_c.table_copy(skillTest.selected);ms.d_skillUpgradeUI.show({{from_btn=4,skill_info=skillTest.detached,parent_layer=ui.g_packageUI.board_layer,isNeedUpdate=false}});assert(ms.d_skillUpgradeUI.g_self.params.skill_info==skillTest.selected,"copied selection not rebound")')
        for n,code in enumerate(stages):
            expected=((1,1),(2,0),(3,0))[n]
            check(('failure compensation rendered immediately','success level and power rendered immediately','consecutive success renders level 3 and power 207')[n], 'local apply=skillTest.apply;'+code+f';assert(skillTest.item({target})==skillTest.selected,"identity");assert(skillTest.selected.level=={expected[0]},"level="..skillTest.selected.level);assert(skillTest.selected.count=={expected[1]},"count="..skillTest.selected.count);assert(ms.d_skillUpgradeUI.g_self.params.skill_info==skillTest.selected,"params identity");skillTest.label("{expected[0]}");skillTest.label("{145+31*(expected[0]-1)}")')
        capture('upgrade.png')
        report['passed']=True
    except Exception as e:
        report['error']=str(e);report['passed']=False
    finally:
        try:
            report['restored']=evaluate('if skillTest then skillTest.restore() end;return "restored"')=='restored'
            time.sleep(.6)
            evaluate('local ui=package.loaded.ms.d_packageUI;ui.show();ui.showPackage(4);if _skillTestTick then CCDirector:sharedDirector():getScheduler():unscheduleScriptEntry(_skillTestTick);_skillTestTick=nil end;return "bag"')
        finally:
            script.unload();session.detach()
            (dest/'client_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if not report.get('passed') or not report.get('restored'):raise SystemExit(1)

if __name__=='__main__':main()
