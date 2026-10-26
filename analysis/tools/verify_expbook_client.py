"""Compare isolated original Lua previews to local settlement; capture outgoing IDs."""
import copy
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis/tools')]
from network_redirect import formation as f, summon
from network_redirect.backend import Backend, login_fields
from android_emulator.config import load_config
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR


def fixtures():
    cases = []
    with tempfile.TemporaryDirectory() as tmp:
        b = Backend(Path(tmp), 18770, lambda *a, **k: None)
        try:
            baseline = b.profile()
            specs = [(q, tid, 80, 1, 0) for q in range(1, 6) for tid in sorted(f.EXPERIENCE_BOOKS)]
            specs += [(5, 1041, 21, 51, f.EXPERIENCE[5, 51]-100), (5, 1041, 21, 52, 0.1),
                      (5, 1041, 79, 198, 0), (5, 1041, 80, 198, 0)]
            for q, tid, level, cl, xp in specs:
                role = copy.deepcopy(baseline); role['level'] = level
                c = role['corteges'][0]
                c.update(type=next(t for t,r in f.BASES.items() if int(r['quality']) == q),
                         level=cl, cur_exp=xp, culture_point=0)
                summon.add_item(role, tid, 1)
                event = f.feed(role, dict(first_send=True, flag=1, cortege_id=c['id'], roll_count=1,
                                         roll_list=[dict(type_id=tid, count=1)]), b.formation_rules)[0][1]
                cases.append(dict(quality=q, book=tid, player=level, level=cl, cur_exp=xp,
                                  raw=int(f.ITEMS[tid]['experience_plus']), expected_level=c['level'],
                                  expected_exp=c['cur_exp'], expected_gain=event['experience']))
        finally: b.close()
    return cases


def main():
    import frida
    source = r'''
local ms=assert(package.loaded.ms);local ui=assert(package.loaded['ui.expbookUI'], 'Open the game before running this fixture')
local saved={};for k,v in pairs(ui) do saved[k]=v end
local player=ms.d_mainUI.g_playerInfo;local exp=ms.d_data.g_characterExpTable
local send=ms.d_u.main_server_send_msg
local checks={};local sent={}
local ok,err=xpcall(function()
 ms.d_mainUI.g_playerInfo={}
 ms.d_data.g_characterExpTable=__EXPERIENCE__
 ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
 for _,row in ipairs(__CASES__) do
  ms.d_mainUI.g_playerInfo.level=row.player
  ui.g_self={selectedCortId=1,MAXLV=200,lvLimit={{lv=0,rate=1},{lv=2.5,rate=.2},{lv=3,rate=0}}}
  ui.getCortegeInfo=function() return {csvInfo={quality=row.quality},level=row.level,cur_exp=row.cur_exp} end
  local old,level,gain,current=ui.getExpResult(row.raw)
  assert(level==row.expected_level and math.abs(gain-row.expected_gain)<.001 and math.abs(current-row.expected_exp)<.001,
   'preview mismatch: '..row.quality..'/'..row.book..'/'..row.player)
  checks[#checks+1]='preview '..row.quality..'/'..row.book..'/'..row.player..'/'..row.level
 end
 ui.g_self={selectedCortId=123,last_select_page=1,expbook={
  {type=1041,isChosen=true},{type=1041,isChosen=true},{type=1043,isChosen=true},
  {type=1042,isChosen=true},{type=1080,isChosen=false}}}
 ui.sendEatExpbookRequest()
 assert(#sent==1 and sent[1].mid==1059 and sent[1].data.first_send and sent[1].data.flag==1)
 local req=sent[1].data;assert(req.cortege_id==123 and req.roll_count==3)
 local counts={};for _,r in ipairs(req.roll_list) do counts[r.type_id]=r.count end
 assert(counts[1041]==2 and counts[1043]==1 and counts[1042]==1 and counts[1080]==nil)
 checks[#checks+1]='original request groups by ID'
end,debug.traceback)
for k in pairs(ui) do ui[k]=nil end;for k,v in pairs(saved) do ui[k]=v end
ms.d_mainUI.g_playerInfo=player;ms.d_data.g_characterExpTable=exp;ms.d_u.main_server_send_msg=send
return table.tostring({passed=ok,error=err or '',checks=checks,restored=true,
 native_lua=true,network_sends_captured=true,live_account_resources_changed=false,
 coverage='Original preview function and request builder; no full UI/animation walkthrough'})
'''.replace('__CASES__', summon.lua(fixtures())).replace('__EXPERIENCE__', summon.lua({
        q: {n: xp for (quality,n),xp in f.EXPERIENCE.items() if quality==q} for q in range(1,6)}))
    config = load_config(ROOT/'game.json')
    pid = next(p for p,n in processes(config).items() if n == config['package'])
    session = frida.get_device(config['serial'], timeout=10).attach(pid)
    script = session.create_script(LUA_EVALUATOR)
    try:
        script.load(); result = script.exports_sync.evaluate(source)
        assert result.get('status') == 0, result
        report = login_fields(result['result'])
    finally:
        script.unload(); session.detach()
    (ROOT/'analysis/evidence/expbooks/client_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(f"{len(report['checks'])} original Lua checks; passed={report['passed']}")
    if not report['passed']: raise RuntimeError(report['error'])


if __name__ == '__main__': main()
