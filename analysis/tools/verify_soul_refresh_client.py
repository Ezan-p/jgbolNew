"""Replay temporary-backend ascensions through the original Cocos soul list.

Outgoing sends are intercepted and client tables are restored in finally.
The player's persistent account is never read or written by the fixture backend.
"""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis/tools')]
from android_emulator.config import load_config, device_environment
from network_redirect import formation, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode, encode
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR


def fixture():
    def replay(packets):
        code = []
        for index, packet in enumerate(packets):
            mid, _, data = decode(packet)
            code.append('soulTest.next=' + str(decode(packets[index + 1])[0] if index + 1 < len(packets) else 0))
            if mid in (1034, 1035, 1046) or (mid == 1032 and data['unit_type'] == 4):
                code.append('soulTest.apply(%d,%s)' % (mid, summon.lua(data)))
            elif mid == 2998 and data['id'] == 50:
                code.append('ms.d_event_mgr.msg_common_event_2998(nil,%s,nil)' % summon.lua(data))
        return ';'.join(code)

    with tempfile.TemporaryDirectory() as directory:
        backend = Backend(Path(directory), 18790, lambda *a, **k: None)
        try:
            role = backend.profile()
            role.update(level=99, gold_coin=10000, silver_coin=1000000)
            target = role['corteges'][0]
            target.update(evolve_level=0, culture_point=100)
            tid = target['type']
            initial_count = formation.EVOLVE_COST[1] + formation.EVOLVE_COST[2]
            role['souls'] = {str(tid): initial_count}
            backend.save(role)
            initial = replay(backend.inventory(role) + summon.soul_snapshots(role))
            stages = []
            for serial in (100001, 100002):
                packets = backend.respond(encode(1084, dict(serial_num=serial, flag=0, cortege_id=target['id'])),
                                          dict(authenticated=True))
                events = [login_fields(decode(p)[2]['data']) for p in packets
                          if decode(p)[0] == 2998 and decode(p)[2]['id'] == 55]
                if events:
                    raise AssertionError(events)
                stages.append(replay(packets))
            return initial, stages, tid, initial_count, formation.EVOLVE_COST[2]
        finally:
            backend.close()


SETUP = r'''
local ms=package.loaded.ms
assert(not soulTest,'soul fixture already active')
local saved={}
for _,t in ipairs({ms.d_data,ms.d_packageUI,ms.d_lineupUI,ms.d_mainUI,
 ms.d_feishengUI,ms.d_u,ms.d_event_mgr,ms.d_createCell}) do
 local copy={};for k,v in pairs(t) do copy[k]=v end;saved[t]=copy
end
local registry=ms.d_event_mgr.g_msg_fun
local registered=registry and registry[1046]
local oldReport=ms.MS_report_error
soulTest={errors={},rows={},requests={},labels={}}
ms.MS_report_error=function(e) soulTest.errors[#soulTest.errors+1]=tostring(e) end
ms.d_u.main_server_send_msg=function(mid,data) soulTest.requests[#soulTest.requests+1]={mid=mid} end
ms.d_event_mgr.getNextPackageType=function() return soulTest.next or 0 end
local function up(fn,key)
 for i=1,100 do local name,value=debug.getupvalue(fn,i);if name==key then return value end;if not name then break end end
end
soulTest.state=function() return up(ms.d_allLineupUI.showAllSoul,'dataTable') end
soulTest.info=function(tid)
 for _,row in ipairs(soulTest.state().currentShowTable or {}) do if row.type==tid then return row end end
end
soulTest.restore=function()
 if ms.d_data._localSoulRefreshRestore and ms.d_data._localSoulRefreshRestore~=saved[ms.d_data]._localSoulRefreshRestore then
  ms.d_data._localSoulRefreshRestore()
 end
 local currentMain=ms.d_mainUI.g_mainUI
 for t,copy in pairs(saved) do for k in pairs(t) do t[k]=nil end;for k,v in pairs(copy) do t[k]=v end end
 if registry then registry[1046]=registered end
 ms.d_mainUI.g_mainUI=currentMain;ms.MS_report_error=oldReport
 ms.d_packageUI.g_isInPackage=false
 ms.d_packageUI.g_isPackageSorted=false;ms.d_packageUI.sortItems();ms.d_lineupUI.sortcharacterInfo()
 ms.d_loginUI.g_currentSence=ms.d_loginUI.senceID.adventure;ms.d_mainUI.show()
 soulTest=nil
end
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(ms.d_mainUI.g_playerInfo)
ms.d_mainUI.g_playerInfo.level=99
ms.d_lineupUI.g_characterInfo={};ms.d_packageUI.g_packageItemsInfo={}
ms.d_data.g_soulsInfoTable={};ms.d_data.g_soulsTypeTable={}
ms.d_packageUI.g_isInPackage=false
local createCell=ms.d_createCell.createCommonCharCells
ms.d_createCell.createCommonCharCells=function(parent,info,...)
 if info.isSoul then soulTest.rows[info.type]={count=info.count,need=info.feiShengCount} end
 return createCell(parent,info,...)
end
local create=ms.d_u.createByStyle
ms.d_u.createByStyle=function(style,...)
 local node=create(style,...)
 if soulTest.capture and style.type=='label' then soulTest.labels[#soulTest.labels+1]=tostring(style.string) end
 return node
end
soulTest.apply=function(mid,packet)
 if mid==1034 then ms.d_lineupUI.getDateFormServer(packet)
 elseif mid==1035 then ms.d_packageUI.getDateFormServer(packet)
 elseif mid==1032 then ms.d_lineupUI.updateCharacterInfo(packet)
 elseif mid==1046 then ms.d_event_mgr.g_msg_fun[1046](nil,packet,nil) end
end
return 'isolated'
'''


def main():
    import frida
    initial, stages, tid, before, after = fixture()
    config = load_config(ROOT / 'game.json')
    pid = next(p for p, name in processes(config).items() if name == config['package'])
    session = frida.get_device(config['serial'], timeout=10).attach(pid)
    evaluator = LUA_EVALUATOR.replace('pending={code,resolve};',
        "const task={code,resolve};pending=task;setTimeout(()=>{if(pending===task){pending=null;resolve({status:-1,result:'No Lua frame'});}},15000);")
    script = session.create_script(evaluator)
    dest = ROOT / 'analysis/evidence/realtime_refresh'
    dest.mkdir(parents=True, exist_ok=True)
    report = dict(native_cocos=True, temporary_backend=True, live_account_resources_changed=False,
                  network_sends_captured=True, checks=[])

    def evaluate(code):
        value = script.exports_sync.evaluate(code)
        if value.get('status') != 0:
            raise RuntimeError(value)
        return value['result']

    def check(name, code):
        evaluate('local ms=package.loaded.ms;' + code +
                 ';assert(#soulTest.errors==0,table.concat(soulTest.errors,"\\n"));return "ok"')
        report['checks'].append(name)

    def capture(name):
        time.sleep(.4)
        result = subprocess.run([str(config['adb_path']), '-s', config['serial'], 'exec-out', 'screencap', '-p'],
                                env=device_environment(config), capture_output=True, check=True, timeout=15)
        (dest / name).write_bytes(result.stdout)

    try:
        script.load()
        evaluate('assert(not _soulTestTick);_soulTestTick=CCDirector:sharedDirector():getScheduler():scheduleScriptFunc(function() end,0.1,false);return "tick"')
        source = (ROOT / 'tests/soul_refresh_client_regression.lua').read_text().replace(
            '-- INSTALL_PATCH', (ROOT / 'network_redirect/soul_refresh_client.lua').read_text())
        report['unit_checks'] = evaluate('local saved=package.loaded.ms;local ok,result=pcall(function() ' + source +
            ' end);package.loaded.ms=saved;if not ok then error(result) end;return table.concat(result,"\\n")').splitlines()
        evaluate(SETUP)
        evaluate((ROOT / 'network_redirect/soul_refresh_client.lua').read_text() + '\nreturn "installed"')
        evaluate('local ms=package.loaded.ms;ms.d_loginUI.g_currentSence=ms.d_loginUI.senceID.adventure;ms.d_mainUI.show();return "scene"')
        time.sleep(.5)
        report['scene_setup_messages'] = json.loads(evaluate('local old=soulTest.errors;soulTest.errors={};return package.loaded.ms.d_json.encode(old)'))
        check('original soul list displays temporary backend inventory', initial +
              f';ms.d_lineupUI.show();ms.d_lineupUI.showDetailUI(2);assert(soulTest.info({tid}).count=={before});assert(soulTest.rows[{tid}].count=={before})')
        capture('souls_before.png')
        check('first ascension redraws original soul cells without reopening the list',
              f'ms.d_feishengUI.show({tid},soulTest.info({tid}));soulTest.rows={{}};soulTest.labels={{}};soulTest.capture=true;' + stages[0] +
              f';soulTest.capture=false;assert(soulTest.info({tid}).count=={after});assert(soulTest.rows[{tid}].count=={after});assert(soulTest.state().currentTableView.dataSource.tableViewNumberOfRows()==2)')
        time.sleep(1)
        # Native result touch handler only closes the result overlay.
        check('ascension result closes onto the refreshed soul list', 'ms.d_feishengUI.onTouch()')
        capture('souls_after_ascension.png')
        report['rendered_first_ascension'] = json.loads(evaluate('local rows={};for id,row in pairs(soulTest.rows) do rows[tostring(id)]=row end;return package.loaded.ms.d_json.encode({rows=rows,labels=soulTest.labels})'))
        check('spending the final soul stack clears native rows and the captured row count',
              f'ms.d_feishengUI.show({tid},soulTest.info({tid}));' + stages[1] +
              ';assert(#ms.d_data.g_soulsInfoTable==0);assert(#soulTest.state().currentShowTable==0);assert(soulTest.state().currentTableView.dataSource.tableViewNumberOfRows()==1)')
        time.sleep(1)
        check('empty soul list remains empty after closing the result', 'ms.d_feishengUI.onTouch();assert(#soulTest.state().currentShowTable==0)')
        capture('souls_empty.png')
        report['requests_intercepted'] = int(evaluate('return tostring(#soulTest.requests)'))
        report['passed'] = True
    except Exception as error:
        report.update(passed=False, error=str(error))
    finally:
        try:
            report['restored'] = evaluate('if soulTest then soulTest.restore() end;return "restored"') == 'restored'
            time.sleep(.5)
            evaluate('if _soulTestTick then CCDirector:sharedDirector():getScheduler():unscheduleScriptEntry(_soulTestTick);_soulTestTick=nil end;return "done"')
        except Exception as error:
            report.update(restored=False, restore_error=str(error))
        finally:
            script.unload()
            session.detach()
            (dest / 'soul_client_validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not report.get('passed') or not report.get('restored'):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
