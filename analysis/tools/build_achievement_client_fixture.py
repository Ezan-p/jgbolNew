"""Replay wire packets through original achievement handlers, restoring all tables."""
import sys
import tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect.backend import Backend
from network_redirect import achievements as a, summon
from network_redirect.protocol import decode

with tempfile.TemporaryDirectory() as directory:
    b = Backend(Path(directory), 0, lambda *x, **kw: None)
    role = b.profile(); role['role_id'] = 1
    a.add(role, 101); a.add(role, 580); a.finalize(role)
    initial = [decode(p) for p in a.packets(role)]
    a.add(role, 459, 2); a.add(role, 590); a.finalize(role)
    update = [decode(p) for p in a.packets(role, new=1)]
    role['role_id'] = 200
    other = [decode(p) for p in a.packets(role)]
    b.close()

lines = ['''local ms=assert(package.loaded.ms)
local ui=ms.d_achieveUI
local saved={state=ui.g_self,player=ms.d_mainUI.g_playerInfo,check=ui.check,refresh=ui.refreshTaoPoint,show=ui.showAchievements,
 catalog=ms.d_data.g_achieveTable,adapter=ms._localAchievementRestore,send=ms.d_u.main_server_send_msg}
local result={};local function step(name,fn) local ok,e=pcall(fn);result[#result+1]={name=name,ok=ok,error=not ok and tostring(e) or ''};assert(ok,e) end
local ok,err=xpcall(function()
 ui.g_self=ms.d_c.table_copy(saved.state)
 ms.d_data.g_achieveTable=saved.catalog and ms.d_c.table_copy(saved.catalog) or nil
 ms.d_u.main_server_send_msg=function() error('unexpected network send') end
 __ACHIEVEMENT_PATCH__
 ui.g_self.Achieve=nil;ui.g_self.AchieveShow=nil;ui.g_self.isMe=false;ui.g_self.showList={}
 ui.g_self.otherCallBack=function() end
 ui.check=function() end;ui.refreshTaoPoint=function() end;ui.showAchievements=function() end
 ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player);ms.d_mainUI.g_playerInfo.role_id=1
 local function apply(mid,d)
  if mid==1032 then ms.d_event_mgr.msg_modify_attr_1032(nil,d,nil)
  elseif mid==1066 then ms.d_event_mgr.msg_modify_achievements_1066(nil,d,nil)
  elseif mid==2998 and d.id==80 then ms.d_data.callback_update_config(assert(loadstring('return '..d.data))()) end
 end
'''.replace('__ACHIEVEMENT_PATCH__', a.client_patch())]
for name, packets, assertion in (
    ('initial_258_no_popup', initial, "assert(ui.g_self.Achieve[101].accomplish_time==1);assert(ui.g_self.Achieve[580].accomplish_time==1);assert(ui.g_self.Achieve[563].csvInfo.max_repeatable_times==400);assert(#ui.g_self.showList==0)"),
    ('incremental_completion_and_tao', update, "assert(ui.g_self.Achieve[459].accomplish_time==2);assert(ui.g_self.Achieve[590].accomplish_time==1);assert(ms.d_mainUI.g_playerInfo.tao_point==%d);assert(#ui.g_self.showList==2)" % role['tao_point']),
    ('other_role_comparison', other, "assert(#ui.g_self.otherAchieveShow[ui.g_self.OtherCategory.all]==258);assert(ui.g_self.Achieve[459].accomplish_time==2)")):
    lines.append('step('+summon.lua(name)+',function()')
    for mid, _, data in packets: lines.append('apply('+str(mid)+','+summon.lua(data)+')')
    lines.append(assertion+' end)')
lines.append('''end,debug.traceback)
if not saved.adapter and ms._localAchievementRestore then ms._localAchievementRestore() end
ms.d_data.g_achieveTable=saved.catalog;ms.d_u.main_server_send_msg=saved.send
ui.g_self=saved.state;ui.check=saved.check;ui.refreshTaoPoint=saved.refresh;ui.showAchievements=saved.show
ms.d_mainUI.g_playerInfo=saved.player
achievement_fixture_result={ok=ok,error=not ok and tostring(err) or '',cases=result,restored=ui.g_self==saved.state and ms.d_mainUI.g_playerInfo==saved.player}
return ms.d_u.serialize(achievement_fixture_result)
'''.replace('return ms.d_u.serialize(achievement_fixture_result)', "local out={};for _,r in ipairs(result) do out[#out+1]=r.name..'='..tostring(r.ok)..':'..r.error end;return table.concat(out,'\\n')..'\\nrestored='..tostring(achievement_fixture_result.restored)..'\\nerror='..tostring(err)"))
path=ROOT/'.runtime/achievement-fixture.lua';path.parent.mkdir(exist_ok=True);path.write_text('\n'.join(lines))
print(path)
