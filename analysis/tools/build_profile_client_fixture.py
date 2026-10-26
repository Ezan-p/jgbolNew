"""Disposable database packets through original profile UI; no live account writes."""
import sys
import tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect.backend import Backend
from network_redirect import summon
from network_redirect.protocol import encode, decode
lines = ['''local ms=assert(package.loaded.ms)
assert(ms.d_mainUI.g_playerInfo and ms.d_mainUI.g_mainUI.main_layer,'main scene required')
assert(not profile_fixture_restore,'fixture already running')
local saved={player=ms.d_mainUI.g_playerInfo,send=ms.d_u.main_server_send_msg,report=ms.MS_report_error,items=ms.d_packageUI.g_packageItemsInfo,
 honor=ms.d_honorUI.g_self,rune=ms.d_runeUI.g_self,need=ms.d_mainUI.g_need_change_head_type}
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
ms.d_honorUI.g_self=ms.d_c.table_copy(saved.honor)
ms.d_runeUI.g_self=ms.d_c.table_copy(saved.rune)
ms.d_u.main_server_send_msg=function() end
local errors='';local cases={};profile_fixture_results={};profile_fixture_finished=false
ms.MS_report_error=function(e) errors=errors..'\\n'..tostring(e) end
local parent=ms.d_mainUI.g_mainUI.main_layer
local function step(name,fn) cases[#cases+1]={name=name,run=fn} end
local function apply(mid,d)
 if mid==1077 then ms.d_event_mgr.msg_modify_title_1077(nil,d,nil)
 elseif mid==1032 and d.unit_type==1 then ms.d_event_mgr.msg_modify_attr_1032(nil,d,nil)
 elseif mid==1035 then ms.d_packageUI.getDateFormServer(d)
 elseif mid==2998 then ms.d_event_mgr.msg_common_event_2998(nil,d,nil) end
end
function profile_fixture_next()
 local case=table.remove(cases,1)
 if not case then profile_fixture_finished=true;return 'finished' end
 errors='';local ok,err=xpcall(case.run,debug.traceback)
 if not ok then errors=errors..'\\n'..tostring(err) end
 profile_fixture_results[#profile_fixture_results+1]={name=case.name,errors=errors}
 return case.name..': '..errors
end
local function clear_overlays()
 for _,tag in ipairs({ms.d_runeUI.g_change_rune_tag,9876,ms.d_honorUI.tagDef.main_layer}) do
  for i=1,10 do if parent:getChildByTag(tag) then parent:removeChildByTag(tag,true) else break end end
 end
 ms.d_runeUI.g_change_runner_layer=nil
end
function profile_fixture_restore()
 clear_overlays()
 pcall(ms.d_commonLayerUI.cancelName)
 ms.d_mainUI.g_playerInfo=saved.player;ms.d_packageUI.g_packageItemsInfo=saved.items
 ms.d_honorUI.g_self=saved.honor;ms.d_runeUI.g_self=saved.rune
 ms.d_mainUI.g_need_change_head_type=saved.need
 ms.d_u.main_server_send_msg=saved.send;ms.MS_report_error=saved.report
 profile_fixture_restore=nil;ms.d_mainUI.show()
end
''']
with tempfile.TemporaryDirectory() as tmp:
    b = Backend(Path(tmp), 18770, lambda *a, **k: None)
    r = b.profile(); r.update(level=60, gold_coin=1000)
    summon.add_item(r, 1005, 3); b.save(r)
    lines.append('for k,v in pairs('+summon.lua({k:r[k] for k in ('role_id','level','gold_coin','role_name','head_type','cur_genius_type')})+') do ms.d_mainUI.g_playerInfo[k]=v end')
    serial = 10000
    def request(name, mid, pre='', **data):
        global serial
        serial += 1
        packets = b.respond(encode(mid, dict(serial_num=serial, **data)), dict(authenticated=True))
        lines.append('step('+summon.lua(name)+',function() '+pre)
        for packet in packets:
            m, _, d = decode(packet)
            if m == 2998 and d['id'] == 55: raise AssertionError(d)
            if m in (1032,1035,1077,2998): lines.append('apply('+str(m)+','+summon.lua(d)+')')
        lines.append('end)')
    request('first_avatar', 1069, 'ms.d_runeUI.showChangeUserHead(parent,100,9876,false)', head_type=101, flag=0)
    request('profile', 1307, flag=1)
    request('title_wear', 1078, 'ms.d_honorUI.showChangeTitle(parent)', des_id=1, flag=3)
    request('profile_with_title', 1307, flag=2)
    request('talent', 1070, 'ms.d_runeUI.showChangeRuneFrame(parent,100)', type_id=502)
    request('paid_avatar', 1069, 'ms.d_runeUI.showChangeUserHead(parent,100,9876,true)', head_type=102, flag=1)
    request('rename', 1031, 'ms.d_commonLayerUI.showModityNameCard(nil,100)', new_name='齐天行者')
    request('profile_final', 1307, 'clear_overlays()', flag=2)
    b.close()
lines.append("return 'profile fixture ready: '..#cases..' steps'")
(ROOT/'.runtime/profile-fixture.lua').write_text('\n'.join(lines))
print('Built 8 original UI profile cases')
