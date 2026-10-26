"""Original Lua map callbacks with temporary data; restores references in one frame."""
import copy
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis/tools')]
from network_redirect import journey, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode
from android_emulator.config import load_config
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR


def fixture():
    now = 1792987200
    def packets(replies):
        return [dict(mid=mid, data=data) for mid, _, data in map(decode, replies) if mid in (1019, 1020)]
    with tempfile.TemporaryDirectory() as tmp, patch('network_redirect.backend.time.time', return_value=now):
        b = Backend(Path(tmp), 18770, lambda *a, **k: None)
        role = b.profile()
        initial = packets(journey.snapshots(role))
        before = copy.deepcopy(role)
        journey.attempt(role, 1, 101, journey.GATES[1][101], 3, now, b.journey_rules, b.formation_rules)
        won = packets(journey.updates(role, before))
        for kind in (1, 2):
            for gid in journey.GATES[kind]:
                role['journey']['gates'][f'{kind}:{gid}'] = dict(pass_star=3, day_count=2, flush_count=1)
        full = packets(journey.snapshots(role))
        journey.prepare(role, now + 86400, b.journey_rules)
        rollover = packets(journey.snapshots(role, reset=False))
        b.close()
    return dict(initial=initial, won=won, full=full, rollover=rollover)


def main():
    import frida
    data = fixture()
    source = r'''
local ms=assert(package.loaded.ms)
local saved={map=ms.d_mapUI.g_mapUI, states=ms.d_subLevelUI.g_mapStates,
 player=ms.d_mainUI.g_playerInfo, wait=ms.d_alert.stop_wait, send=ms.d_u.main_server_send_msg}
local sent=0;local report={checks={},native_cocos=true,live_account_resources_changed=false}
local function check(name,ok) assert(ok,name);table.insert(report.checks,name) end
local ok,err=xpcall(function()
 ms.d_mapUI.g_mapUI=ms.d_c.table_copy(saved.map)
 ms.d_subLevelUI.g_mapStates=ms.d_c.table_copy(saved.states or {})
 ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
 ms.d_mainUI.g_playerInfo.level=99
 ms.d_alert.stop_wait=function() end
 ms.d_u.main_server_send_msg=function() sent=sent+1 end
 local data=__DATA__
 local function apply(rows)
  for _,p in ipairs(rows) do
   if p.mid==1020 then ms.d_event_mgr.msg_update_tollgate_list_1020(nil,p.data,nil)
   else ms.d_event_mgr.msg_update_tollgate_data_1019(nil,p.data,nil) end
  end
 end
 apply(data.initial)
 local map=ms.d_mapUI.g_mapUI;map.mapID=1;map.jy_mode=1
 check('initial_gate',map.maps[1].tollgates[101].pass_star==0)
 apply(data.won)
 check('won_and_next_unlocked',map.maps[1].tollgates[101].pass_star==3 and map.maps[1].tollgates[102].pass_star==0)
 check('last_fight_not_overwritten',map.last_fight_npc==101)
 local exp,money=ms.d_mapUI.getLastFightExpAndMoney()
 check('normal_reward_display',tonumber(exp)==100 and tonumber(money)==150)
 apply(data.full)
 local normal,elite=map.maps[67].tollgates[6710],map.maps[67].tollgates_elite[6701]
 check('full_catalog_last_gates',normal.pass_star==3 and elite.pass_star==3)
 check('daily_counts_before_rollover',normal.day_count==2 and elite.day_count==2)
 map.mapID=1;map.jy_mode=2;map.last_fight_npc=101
 exp,money=ms.d_mapUI.getLastFightExpAndMoney()
 check('elite_reward_display',tonumber(exp)==300 and tonumber(money)==360)
 apply(data.rollover)
 check('rollover_preserves_open_panel_references',normal==map.maps[67].tollgates[6710] and elite==map.maps[67].tollgates_elite[6701])
 check('rollover_clears_both_counts',normal.day_count==0 and normal.flush_count==0 and elite.day_count==0 and elite.flush_count==0)
 check('rollover_retains_stars_and_last_fight',normal.pass_star==3 and elite.pass_star==3 and map.last_fight_npc==101)
 check('no_network_requests',sent==0)
end,debug.traceback)
ms.d_mapUI.g_mapUI=saved.map;ms.d_subLevelUI.g_mapStates=saved.states
ms.d_mainUI.g_playerInfo=saved.player;ms.d_alert.stop_wait=saved.wait;ms.d_u.main_server_send_msg=saved.send
report.restored=ms.d_mapUI.g_mapUI==saved.map and ms.d_mainUI.g_playerInfo==saved.player
report.passed=ok and report.restored;if not ok then report.error=tostring(err) end
return table.tostring(report)
'''.replace('__DATA__', summon.lua(data))
    config = load_config(ROOT / 'game.json')
    pid = next(p for p, n in processes(config).items() if n == config['package'])
    session = frida.get_device(config['serial'], timeout=10).attach(pid)
    script = session.create_script(LUA_EVALUATOR)
    try:
        script.load()
        result = script.exports_sync.evaluate(source)
        assert result.get('status') == 0, result
        report = login_fields(result['result'])
    finally:
        script.unload()
        session.detach()
    (ROOT / 'analysis/evidence/journey_client_validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not report['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
