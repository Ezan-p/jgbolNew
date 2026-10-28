"""Replay isolated growth replies through original Cocos previews and training UI.

All backend writes use a temporary database. Client sends are intercepted, saved
module/data references are restored in finally, and assertions read CCLabels.
"""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis/tools')]
from android_emulator.config import device_environment, load_config
from network_redirect import formation, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode, encode
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR


def packet_source(packets):
    lines = []
    for index, packet in enumerate(packets):
        mid, _, data = decode(packet)
        lines.append('stateRefreshTest.next=' + str(decode(packets[index + 1])[0]
                     if index + 1 < len(packets) else 0))
        if mid in (1032, 1034, 1035) or (mid == 2998 and data['id'] == 4):
            lines.append('stateRefreshTest.apply(%d,%s)' % (mid, summon.lua(data)))
    return ';'.join(lines)


def fixture():
    with tempfile.TemporaryDirectory() as directory:
        backend = Backend(Path(directory), 18790, lambda *a, **k: None)
        try:
            role = backend.profile()
            role.update(level=99, vip_level=3, silver_coin=1000000000, gold_coin=10000)
            role['corteges'][0].update(level=20, culture_point=100)
            hero = role['corteges'][0]['id']
            summon.add_item(role, 1001, 1000)
            # Preserve selected gear even when its snapshot arrives in a later chunk.
            for _ in range(130):
                role['attachments'].append(dict(id=formation.new_id(role), attach_type=5,
                                                type_id=1001, level=1, count=1))
            gear = []
            for main in (1, 2, 3):
                type_id = next(t for t, row in formation.ITEMS.items()
                               if int(row['main_type']) == main and int(row['quality']) == 5)
                identity = formation.new_id(role)
                role['attachments'].append(dict(id=identity, attach_type=5, type_id=type_id,
                                                level=20, count=1, equip_order=1, equip_pos=main))
                gear.append(identity)
            backend.save(role)
            role = backend.profile()
            initial = packet_source(backend.inventory(role))
            serial = 10000

            def request(mid, **data):
                nonlocal serial
                serial += 1
                packets = backend.respond(encode(mid, dict(serial_num=serial, **data)), {'authenticated': True})
                errors = [login_fields(d['data']) for m, _, d in map(decode, packets)
                          if m == 2998 and d['id'] == 55]
                assert not errors, errors
                return packet_source(packets)

            equipment_cases = []
            for main, identity in enumerate(gear, 1):
                stages = []
                for _ in range(2):
                    with patch.object(summon, 'weighted_choice', return_value=1):
                        source = request(1052, equip_id=identity, equip_order=1, inbatch=False)
                    current = next(i for i in backend.profile()['attachments'] if i['id'] == identity)
                    stages.append(dict(source=source, level=current['level'], effect=current['effect_value']))
                    if len(stages) == 1:
                        snapshot = packet_source(backend.inventory(backend.profile()))
                equipment_cases.append(dict(main=main, identity=identity, stages=stages, snapshot=snapshot))
            training_cases = []
            for _ in range(2):
                with patch('network_redirect.formation.secrets.choice', return_value='gongji'):
                    preview = request(1081, cortege_id=hero, train_type=1, intensive=False)
                confirm = request(1082, cortege_id=hero, confirm=True)
                current = next(c for c in backend.profile()['corteges'] if c['id'] == hero)
                training_cases.append(dict(preview=preview, confirm=confirm,
                                           potential=current['culture_point'], attack=current['gongji']))
            player = {key: role[key] for key in ('level', 'vip_level', 'silver_coin', 'gold_coin', 'cortege_count')}
            return dict(initial=initial, hero=hero, player=player, inventory_count=len(role['attachments']),
                        equipment=equipment_cases, training=training_cases)
        finally:
            backend.close()


ISOLATE = r'''
local ms=assert(package.loaded.ms)
assert(not stateRefreshTest,'another state-refresh fixture is active')
local bag,lineup,pos,training=ms.d_packageUI,ms.d_lineupUI,ms.d_charPositionUI,ms.d_trainingUI
local saved={}
for _,module in ipairs({bag,lineup,pos,training,ms.d_mainUI,ms.d_event_mgr,ms.d_u,ms.d_info,ms.d_loginUI}) do
 local copy={};for k,v in pairs(module) do copy[k]=v end;saved[module]=copy
end
local report=ms.MS_report_error
local savedRestore=ms._localStateRefreshRestore
stateRefreshTest={errors={},sent={},next=0,labels={}}
local test=stateRefreshTest
ms.MS_report_error=function(message) table.insert(test.errors,tostring(message)) end
ms.d_u.main_server_send_msg=function(mid,data) table.insert(test.sent,{mid=mid,data=data}) end
ms.d_info.show=function() end
ms.d_event_mgr.getNextPackageType=function() return test.next end
test.restore=function()
 -- Tear down fixture nodes while outgoing requests are still intercepted.
 local currentMain=ms.d_mainUI.g_mainUI
 if currentMain and currentMain.main_layer then
  pcall(function() currentMain.main_layer:removeChildByTag(ms.d_mainUI.boardID.charPosition,true) end)
  pcall(function() currentMain.main_layer:removeChildByTag(ms.d_data.getTagFromDef('training'),true) end)
 end
 if ms._localStateRefreshRestore and ms._localStateRefreshRestore~=savedRestore then
  ms._localStateRefreshRestore()
 end
 for module,copy in pairs(saved) do
  for key in pairs(module) do module[key]=nil end
  for key,value in pairs(copy) do module[key]=value end
 end
 ms._localStateRefreshRestore=savedRestore
 ms.MS_report_error=report
 ms.d_mainUI.g_mainUI=currentMain
 bag.g_isInPackage=false;bag.g_isPackageSorted=false
 pos.g_isQuitBoard=true;pos.g_charPosUI={}
 bag.sortItems();lineup.sortcharacterInfo()
 ms.d_loginUI.g_currentSence=ms.d_loginUI.senceID.adventure
 ms.d_mainUI.show()
 stateRefreshTest=nil
end
-- Isolate the arrays before the identity-preserving adapter sees fixture IDs.
if ms._localStateRefreshRestore then ms._localStateRefreshRestore() end
bag.g_packageItemsInfo={};bag.g_isInPackage=false;bag.g_isPackageSorted=false
lineup.g_characterInfo={};pos.g_charPosUI={};pos.g_isQuitBoard=true
training.g_self=ms.d_c.table_copy(training.g_self)
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(ms.d_mainUI.g_playerInfo)
test.item=function(id)
 for _,item in ipairs(bag.g_packageItemsInfo) do if item.id==id then return item end end
 error('missing item '..id)
end
test.hero=function(id)
 for _,hero in ipairs(lineup.g_characterInfo) do if hero.id==id then return hero end end
 error('missing hero '..id)
end
test.apply=function(mid,data)
 if mid==1032 then ms.d_event_mgr.msg_modify_attr_1032(nil,data,nil)
 elseif mid==1034 then lineup.getDateFormServer(data)
 elseif mid==1035 then bag.getDateFormServer(data)
 elseif mid==2998 then ms.d_event_mgr.msg_common_event_2998(nil,data,nil) end
end
local create=ms.d_u.createByStyle
ms.d_u.createByStyle=function(style,...)
 local node=create(style,...)
 if test.captureLabels and style.type=='label' then table.insert(test.labels,node) end
 return node
end
test.label=function(value)
 local expected=tostring(value);local values={}
 local layer=pos.g_charPosUI.charInfoLayer
 assert(layer and layer:getChildByTag(pos.tagDef.usedItemIntro),'preview is no longer attached')
 for _,label in ipairs(test.labels) do
  local value=label:getString();values[#values+1]=value
  if value==expected then return true end
 end
 error('missing rendered CCLabel '..expected..': '..table.concat(values,','))
end
return 'isolated'
'''


def main():
    import frida
    data = fixture()
    config = load_config(ROOT / 'game.json')
    pid = next(p for p, name in processes(config).items() if name == config['package'])
    session = frida.get_device(config['serial'], timeout=10).attach(pid)
    evaluator = LUA_EVALUATOR.replace('pending={code,resolve};',
        "const task={code,resolve};pending=task;setTimeout(()=>{if(pending===task){pending=null;resolve({status:-1,result:'No Lua frame'});}},15000);")
    script = session.create_script(evaluator)
    destination = ROOT / 'analysis/evidence/realtime_refresh'
    destination.mkdir(parents=True, exist_ok=True)
    report = dict(native_cocos=True, live_account_resources_changed=False,
                  network_sends_captured=True, checks=[],
                  coverage='Original attached Cocos preview labels and training confirmation labels; replayed binary backend responses, not manual touch consumption.',
                  screenshot_notes='The fixture selection sidebar partially occludes equipment screenshots; assertions verify preview attachment and actual CCLabel text. The training screenshot is unobstructed.')

    def evaluate(source):
        result = script.exports_sync.evaluate(source)
        if result.get('status') != 0:
            raise RuntimeError(result)
        return result['result']

    def check(name, source):
        evaluate('local ms=package.loaded.ms;local test=stateRefreshTest;' + source +
                 ';assert(#test.errors==0,table.concat(test.errors,"\\n"));return "ok"')
        report['checks'].append(name)

    def capture(name):
        time.sleep(.7)
        result = subprocess.run([str(config['adb_path']), '-s', config['serial'], 'exec-out', 'screencap', '-p'],
                                env=device_environment(config), capture_output=True, check=True, timeout=15)
        (destination / name).write_bytes(result.stdout)

    try:
        script.load()
        evaluate('assert(not _stateRefreshTick);_stateRefreshTick=CCDirector:sharedDirector():getScheduler():scheduleScriptFunc(function() end,0.1,false);return "tick"')
        evaluate(ISOLATE)
        evaluate((ROOT / 'network_redirect/state_refresh_client.lua').read_text() + '\nreturn "installed"')
        evaluate('''local ms=package.loaded.ms;local pos=ms.d_charPositionUI;local original=pos.showItemIntro
pos.showItemIntro=function(...)
 local test=stateRefreshTest;test.labels={};test.captureLabels=true
 local ok,result=pcall(original,...);test.captureLabels=false
 if not ok then error(result,0) end;return result
end
return 'render capture installed' ''')
        player = ';'.join('ms.d_mainUI.g_playerInfo.%s=%s' % (key, value) for key, value in data['player'].items())
        evaluate('local ms=package.loaded.ms;ms.d_loginUI.g_currentSence=ms.d_loginUI.senceID.adventure;ms.d_mainUI.show();return "scene"')
        time.sleep(.7)
        check('isolated roster and chunked equipment snapshot installed', player + ';' + data['initial'] +
              ';assert(#ms.d_packageUI.g_packageItemsInfo==%d);test.item(%d)' %
              (data['inventory_count'], data['equipment'][0]['identity']))
        check('original formation equipment preview opens',
              'ms.d_charPositionUI.show();ms.d_charPositionUI.tapHeadButton(1)')
        time.sleep(.6)
        evaluate('local p=package.loaded.ms.d_charPositionUI.g_charPosUI;if p.chgCharCloseMenuItem then p.chgCharCloseMenuItem:activate() end;return "closed selection sidebar"')
        time.sleep(.6)
        for case in data['equipment']:
            main, identity = case['main'], case['identity']
            check('slot %d resolves a copied preview selection' % main,
                  'test.selected=test.item(%d);test.detached=ms.d_c.table_copy(test.selected);'
                  'ms.d_charPositionUI.showItemIntro(test.detached,test.hero(%d));'
                  'assert(ms.d_charPositionUI.g_lastItemIntro==test.selected)' % (identity, data['hero']))
            for index, stage in enumerate(case['stages']):
                check('slot %d enhancement %d renders current level and effect' % (main, index + 1),
                      stage['source'] + ';assert(test.item(%d)==test.selected);'
                      'assert(ms.d_charPositionUI.g_lastItemIntro==test.selected,"preview selection lost");'
                      'assert(test.selected.level==%d);test.label(%d);test.label(%d)' %
                      (identity, stage['level'], stage['level'], stage['effect']))
                if index == 0:
                    check('slot %d preserves selection through a full chunked snapshot' % main,
                          case['snapshot'] + ';assert(test.item(%d)==test.selected)' % identity)
            capture('equipment_preview_slot_%d.png' % main)
        check('original training window opens with authoritative potential',
              'ms.d_trainingUI.show(test.hero(%d));assert(tonumber(ms.d_trainingUI.g_leftPotentialNumLabel:getString())==100)' % data['hero'])
        for index, stage in enumerate(data['training']):
            check('training %d preview uses retained character' % (index + 1), stage['preview'])
            check('training %d confirmation renders current potential and attack' % (index + 1),
                  stage['confirm'] + ';assert(tonumber(ms.d_trainingUI.g_leftPotentialNumLabel:getString())==%d);'
                  'assert(tonumber(ms.d_trainingUI.g_statsLabel[2]:getString())==%d)' %
                  (stage['potential'], stage['attack']))
        capture('training_potential.png')
        report['captured_send_count'] = int(evaluate('return tostring(#stateRefreshTest.sent)'))
        report['passed'] = True
    except Exception as error:
        report.update(passed=False, error=str(error))
    finally:
        try:
            report['restored'] = evaluate('if stateRefreshTest then stateRefreshTest.restore() end;return "restored"') == 'restored'
            evaluate('if _stateRefreshTick then CCDirector:sharedDirector():getScheduler():unscheduleScriptEntry(_stateRefreshTick);_stateRefreshTick=nil end;return "stopped"')
        except Exception as error:
            report.update(restored=False, restore_error=str(error))
        finally:
            script.unload()
            session.detach()
            (destination / 'state_client_validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not report.get('passed') or not report.get('restored'):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
