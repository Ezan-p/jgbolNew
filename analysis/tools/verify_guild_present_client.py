"""Exercise the native gift dialog with disposable data and captured sends."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis/tools')]
from network_redirect import guild, guild_feast, summon
from network_redirect.backend import login_fields
from verify_guild_client import LUA_EVALUATOR


def fixture():
    rules = guild.load_rules()
    now = 1792728000
    role = dict(role_id=1, role_name='赠礼验证', union_rank=1)
    state = dict(day=now//86400)
    union = dict(members={str(i):dict(rank=5) for i in range(1,7)})
    data = guild_feast.data(role,state,union,now,rules)
    return r'''
local ms=assert(package.loaded.ms)
local ui=ms.d_guildPartyUI
local saved={state=ui.g_guildPartyUI,config=ui.g_self,send=ms.d_u.main_server_send_msg,
 menu=ms.d_u.createMenu,report=ms.MS_report_error,player=ms.d_mainUI.g_playerInfo}
local parent=CCLayer:create();parent:retain()
local buttons,sent,errors={},{},{}
local function restore()
 ms.d_u.main_server_send_msg=saved.send;ms.d_u.createMenu=saved.menu
 ms.MS_report_error=saved.report;ms.d_mainUI.g_playerInfo=saved.player
 parent:removeAllChildrenWithCleanup(true);parent:release()
 ui.g_guildPartyUI=saved.state;ui.g_self=saved.config
end
local ok,result=xpcall(function()
 ui.g_guildPartyUI=ms.d_c.table_copy(saved.state)
 ui.g_self=ms.d_c.table_copy(saved.config)
 ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
 ms.d_mainUI.g_playerInfo.vip_level=1;ms.d_mainUI.g_playerInfo.last_feast_grab_count=0
 ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
 ms.d_u.main_server_send_msg=function(mid,d) sent[#sent+1]={mid=mid,data=d} end
 ms.d_u.createMenu=function(options,...)
  for _,v in pairs(options) do
   if type(v)=='table' and type(v.call_back)=='function' then
    buttons[debug.getinfo(v.call_back,'S').linedefined]=v.call_back
   end
  end
  return saved.menu(options,...)
 end
 ui.show(parent,__DATA__)
 ui.showPresentLayer()
 assert(#errors==0,table.concat(errors,'\n'))
 -- Native confirm/select/cancel closures from guildPartyUI L301/287/255.
 local confirm=assert(buttons[301],'confirm missing: dialog did not finish')
 local choose=assert(buttons[287],'gift selection missing')
 local cancel=assert(buttons[255],'cancel missing')
 confirm()
 choose(2);confirm()
 assert(#sent==2,'unexpected network sends')
 for i,tid in ipairs({1120,1121}) do
  local packet=sent[i];assert(packet.mid==1301 and packet.data.id==67)
  local d=assert(loadstring('return '..packet.data.data))()
  assert(d.gift_type==tid and d.count==2,'native gift request mismatch')
 end
 cancel()
 ui.showPresentLayer();assert(#errors==0,table.concat(errors,'\n'))
 assert(buttons[255])()
 return {passed=true,checks={'native dialog renders','both gift selections',
  'native item IDs and quantity','cancel and reopen'},network_sends_captured=true,
  live_account_resources_changed=false}
end,debug.traceback)
restore()
assert(ok,result)
return table.tostring(result)
'''.replace('__DATA__', summon.lua(data))


def main():
    import frida
    from android_emulator.config import load_config
    from observability.collector import processes
    config = load_config(ROOT / 'game.json')
    pid = next(p for p,n in processes(config).items() if n==config['package'])
    session = frida.get_device(config['serial'],timeout=5).attach(pid)
    script = session.create_script(LUA_EVALUATOR)
    script.load()
    try:
        answer = script.exports_sync.evaluate(fixture())
        assert answer.get('status')==0, answer
        report = login_fields(answer['result'])
        report.update(native_cocos=True,restored=True)
        output = ROOT / 'analysis/evidence/guild/present_client_validation.json'
        output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps(report,ensure_ascii=False,indent=2))
    finally:
        script.unload()
        session.detach()


if __name__=='__main__':
    main()
