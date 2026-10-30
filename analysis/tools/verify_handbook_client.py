"""Validate handbook filtering and native Rulai details without account writes.

Run with the spell handbook open. Installs the current adapter in the live
client; captures outgoing sends during checks and restores formation context.
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis/tools')]
from network_redirect import summon
from network_redirect.backend import login_fields
from android_emulator.config import load_config
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR

HARNESS = r'''
local ms=package.loaded.ms
local ui,h,position=ms.d_packageUI,ms.d_handbookUI,ms.d_charPositionUI
assert(h.g_self.last_tag==6 and h.g_self.board_layer,'open the spell handbook first')
local catalog,context=ui.g_itemSkillTable,position.g_charPosUI
local send,create=ms.d_u.main_server_send_msg,ms.d_u.createByStyle
local report={passed=false,checks={},network_sends=0}
local labels={}
ms.d_u.main_server_send_msg=function() report.network_sends=report.network_sends+1 end
ms.d_u.createByStyle=function(style,...)
 if style.type=='label' then labels[#labels+1]=tostring(style.string) end
 return create(style,...)
end
local function check(name,fn) fn();report.checks[#report.checks+1]=name end
local function close()
 if h.g_charintro_layer and h.g_charintro_layer.mainLayer then h.menuCancel() end
end
local ok,err=xpcall(function()
 close()
 if ui._localSkillRestore then ui._localSkillRestore() end
 position.g_charPosUI=nil
 local before,reason=pcall(h.showHandbookDetail,21)
 report.original_error=tostring(reason)
 assert(not before and tostring(reason):find('g_charPosUI'),'expected original missing owner failure')
 assert(loadstring(__SOURCE__))()
 check('native_grid_filters_internal_and_blank_tiles',function()
  h.g_self.last_tag=0;h.createListBoard(6)
  local count=0
  for _,id in pairs(h.g_self.handbook_map) do assert(id>11);count=count+1 end
  local expected=0;for id in pairs(catalog) do if id>11 then expected=expected+1 end end
  assert(count==expected);report.visible_spells=count
  assert(ui.g_itemSkillTable==catalog and catalog[2] and catalog[11])
 end)
 check('Rulai_opens_without_formation_and_can_close_reopen',function()
  for _=1,2 do
   labels={};h.showHandbookDetail(21)
   assert(h.g_charintro_layer.mainLayer and position.g_charPosUI==nil)
   local joined=table.concat(labels,'|')
   assert(joined:find('3.0%%') and joined:find('8.0%%'),joined)
   close();assert(h.g_charintro_layer.mainLayer==nil)
  end
 end)
 check('Rulai_ignores_stale_owner_bonus_and_restores_context',function()
  local selected={magic=80000}
  local state={current_characterInfo=selected}
  position.g_charPosUI=state;labels={};h.showHandbookDetail(21)
  assert(position.g_charPosUI==state and state.current_characterInfo==selected and selected.magic==80000)
  assert(table.concat(labels,'|'):find('3.0%%'))
  close()
 end)
 check('every_visible_spell_opens_and_closes',function()
  position.g_charPosUI=nil
  for _,id in pairs(h.g_self.handbook_map) do
   h.showHandbookDetail(id);assert(h.g_charintro_layer.mainLayer,'missing detail '..id);close()
  end
 end)
 position.g_charPosUI=context
 h.showHandbookDetail(21)
 assert(position.g_charPosUI==context and report.network_sends==0)
 report.passed=true
end,debug.traceback)
position.g_charPosUI=context
ms.d_u.main_server_send_msg=send;ms.d_u.createByStyle=create
if not ok then report.error=tostring(err) end
return table.tostring(report)
'''


def main():
    import frida
    config = load_config(ROOT / 'game.json')
    pid = next(p for p, n in processes(config).items() if n == config['package'])
    session = frida.get_device(config['serial'], timeout=10).attach(pid)
    evaluator = LUA_EVALUATOR.replace('pending={code,resolve};',
        "const task={code,resolve};pending=task;setTimeout(()=>{if(pending===task){pending=null;resolve({status:-1,result:'No Lua frame'});}},15000);")
    script = session.create_script(evaluator)
    try:
        script.load()
        code = HARNESS.replace('__SOURCE__', summon.lua((ROOT / 'network_redirect/skill_client.lua').read_text()))
        result = script.exports_sync.evaluate(code)
        if result.get('status') != 0:
            raise RuntimeError(result)
        report = login_fields(result['result'])
    finally:
        script.unload()
        session.detach()
    dest = ROOT / 'analysis/evidence/handbook'
    dest.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    (dest / 'client_validation.json').write_text(rendered)
    print(rendered)
    if not report.get('passed'):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
