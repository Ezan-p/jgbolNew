"""Play one real five-member secret-area battle to completion in native Cocos.

The backend uses a disposable database; live requests/pushes are isolated while
the original animation runs. No combat statistics or outcome are patched.
"""
import json
from pathlib import Path
import sys
import tempfile
import time
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from android_emulator.config import load_config
from observability.collector import processes
from network_redirect.backend import Backend, login_fields
from network_redirect import guild, summon
from network_redirect.protocol import encode, decode
from verify_guild_client import LUA_EVALUATOR


def fixture():
    with tempfile.TemporaryDirectory() as tmp, patch('network_redirect.backend.time.time', return_value=1792814400):
        backend = Backend(Path(tmp), 18790, lambda *a, **kw: None)
        try:
            role = backend.profile()
            role.update(level=20, gold_coin=100000, silver_coin=100000)
            backend.save(role)
            serial = 100

            def request(op, **data):
                nonlocal serial
                serial += 1
                rows = [decode(p) for p in backend.respond(encode(1301, dict(
                    serial_num=serial, id=op, data=summon.lua(data))), dict(authenticated=True))]
                assert not any(mid == 2998 and d['id'] == 55 for mid, _, d in rows), rows
                return rows

            request(1, union_name='动画验证仙盟')
            role = backend.profile()
            applicants = list(map(int, role['guild']['unions'][str(role['union_id'])]['applications']))
            request(5, role_list=applicants)
            request(26)
            role = backend.profile()
            request(28, role_list=list(map(int, role['guild']['instances']['team']['applications'])))
            role = backend.profile()
            members = list(map(int, role['guild']['instances']['team']['members']))
            rows = request(41, fight_list=members)
            data = next(login_fields(d['data']) for mid, _, d in rows if mid == 1301 and d['id'] == 41)
            replay = data['fight_result_list'][1]
            assert len(members) == 5 and len(replay['participants']) == 8
            config = guild.client_config(backend.guild_rules)
            events = [d for mid, _, d in rows if mid == 2998 and d['id'] == 121]
        finally:
            backend.close()
    source = r'''
local ms=assert(package.loaded.ms);local mgr=ms.d_event_mgr
assert(not guild_fixture_restore and not guildBattleRestore,'another guild fixture is active')
local saved={player=ms.d_mainUI.g_playerInfo,config=ms.d_data.g_new_config,
 guildConfig=ms.d_xianmengUI.guildConfig,send=ms.d_u.main_server_send_msg,
 report=ms.MS_report_error,dispatch=mgr.g_msg_fun,secret=ms.d_secretAreaUI.g_self,
 fights=mgr.g_fight_info,ids=mgr.g_fight_id_list,menu=ms.d_u.createMenu}
local errors='';local sent={};local resultButton
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
ms.d_data.g_new_config=ms.d_c.table_copy(saved.config)
for k,v in pairs(__ROLE__) do ms.d_mainUI.g_playerInfo[k]=v end
ms.d_data.g_new_config[8]=__CONFIG__;ms.d_xianmengUI.getGuildConfig(ms.d_data.g_new_config[8])
ms.d_u.main_server_send_msg=function(mid,d,...)
 if mid==2999 then return saved.send(mid,d,...) end
 sent[#sent+1]={mid=mid,id=d and d.id}
end
local dispatch={};for mid,fn in pairs(saved.dispatch) do dispatch[mid]=mid==2999 and fn or function() end end
mgr.g_msg_fun=dispatch;mgr.g_fight_info={};mgr.g_fight_id_list={}
ms.MS_report_error=function(e) errors=errors..'\n'..tostring(e) end
ms.d_secretAreaUI.g_self={fight_data=__DATA__}
ms.d_secretAreaUI.g_self.fight_data.play_index=0
ms.d_secretAreaUI.g_self.fight_count=1;ms.d_secretAreaUI.g_self.free_times=2
ms.d_u.createMenu=function(options,...)
 for _,row in pairs(options) do
  if type(row)=='table' and row.call_back==ms.d_secretAreaUI.playNextFight then resultButton=row.call_back end
 end
 return saved.menu(options,...)
end
function guildBattleRestore()
 mgr.setSpecialFightType(0)
 ms.d_mainUI.g_playerInfo=saved.player;ms.d_data.g_new_config=saved.config
 ms.d_xianmengUI.getGuildConfig(saved.guildConfig)
 ms.d_u.main_server_send_msg=saved.send;ms.MS_report_error=saved.report
 ms.d_u.createMenu=saved.menu
 mgr.g_msg_fun=saved.dispatch;mgr.g_fight_info=saved.fights;mgr.g_fight_id_list=saved.ids
 ms.d_secretAreaUI.g_self=saved.secret
 guildBattleRestore=nil;guildBattlePoll=nil;guildBattleReturn=nil
 ms.d_mainUI.show()
 return 'restored'
end
function guildBattlePoll()
 local f=ms.d_fightUI.g_fightUI
 return table.tostring({ended=f.is_fight_end or false,button_ready=resultButton~=nil,errors=errors,
  final_result=f.last_final_result or -1,fight_type=f.last_fight_type or -1,
  play_index=ms.d_secretAreaUI.g_self.fight_data and ms.d_secretAreaUI.g_self.fight_data.play_index or -1,
  sent=sent})
end
function guildBattleReturn()
 assert(ms.d_fightUI.g_fightUI.is_fight_end,'animation still running')
 assert(resultButton,'native secret-area result button missing')()
 return 'returned through original battle button'
end
for _,d in ipairs(__EVENTS__) do mgr.msg_common_event_2998(nil,d,nil) end
ms.d_secretAreaUI.playNextFight()
return 'started'
'''
    fields = {key: role[key] for key in ('level', 'role_id', 'union_id', 'union_rank', 'union_name')}
    for marker, value in (('__ROLE__', fields), ('__CONFIG__', config), ('__DATA__', data), ('__EVENTS__', events)):
        source = source.replace(marker, summon.lua(value))
    return source, dict(members=members, participants=8, enemy=replay['enemy_npc'],
                       rounds=replay['fight_result_msg']['fight_round'],
                       backend_result=replay['fight_result_msg']['final_result'])


def main():
    import frida
    source, report = fixture()
    (ROOT / '.runtime/guild-battle-fixture.lua').write_text(source)
    config = load_config(ROOT / 'game.json')
    device = frida.get_device(config['serial'], timeout=10)
    pid = next(p for p, n in processes(config).items() if n == config['package'])
    session = device.attach(pid)
    script = session.create_script(LUA_EVALUATOR)
    restored = False
    started = False
    report.update(passed=False, full_animation=True, stat_boosts=False, network_isolated=True)

    def evaluate(code):
        answer = script.exports_sync.evaluate(code)
        if answer.get('status') != 0:
            raise RuntimeError(answer)
        return answer['result']

    try:
        script.load()
        login_deadline = time.monotonic() + 45
        while evaluate("local ms=package.loaded.ms;return tostring(ms and ms.d_mainUI and ms.d_mainUI.g_playerInfo and ms.d_mainUI.g_playerInfo.role_id~=nil or false)") != 'true':
            if time.monotonic() >= login_deadline:
                raise RuntimeError('Enter the game before running the fixture')
            time.sleep(.5)
        evaluate(source);started = True
        deadline = time.monotonic() + 180
        while time.monotonic() < deadline:
            time.sleep(.5)
            state = login_fields(evaluate('return guildBattlePoll()'))
            (ROOT / '.runtime/guild-battle-progress.json').write_text(json.dumps(state, ensure_ascii=False, indent=2))
            if state['errors']:
                raise RuntimeError(state['errors'])
            if state['ended'] and state['button_ready']:
                assert state['fight_type'] == 15, state
                assert state['final_result'] == report['backend_result'], state
                report['animation'] = state
                evaluate('return guildBattleReturn()')
                time.sleep(1)
                returned = login_fields(evaluate('return guildBattlePoll()'))
                assert not returned['errors'], returned
                assert any(row.get('id') in (18, 44) for row in returned['sent'].values()), returned
                report.update(passed=True, return_requested_guild=True)
                break
        if not report['passed']:
            raise RuntimeError('Native battle did not finish within 180 seconds')
    except Exception as error:
        report['error'] = str(error)
    finally:
        if started:
            try:
                restored = evaluate('return guildBattleRestore()') == 'restored'
            except Exception as error:
                report['restore_error'] = str(error)
        try:script.unload()
        except Exception:pass
        try:session.detach()
        except Exception:pass
    report['restored'] = restored
    report['passed'] = bool(report['passed'] and restored)
    path = ROOT / 'analysis/evidence/guild/current_client_battle.json'
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False), flush=True)
    if not report['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
