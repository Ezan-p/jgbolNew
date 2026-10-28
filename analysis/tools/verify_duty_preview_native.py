"""Exercise duty preview with native Cocos, captured sends and detached fixtures."""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT/'analysis/tools')]
from network_redirect import activity, activity_duty as duty, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode
from android_emulator.config import load_config
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR

with tempfile.TemporaryDirectory() as tmp:
    b = Backend(Path(tmp), 18770, lambda *a, **k: None)
    role = b.profile(); role['level'] = 60
    now = 1792814400
    activity.prepare(role, now, b.activity_rules)
    b.save(role)
    duty.start(role, b.activity_rules)
    role['activity']['duty'].update(initial_bonus=[10,0,20,0], bonus=[5,25,10,35])
    packet = duty.inspection(role, dict(des_type=1,des_id=0,flag=51), [], b.formation_rules)[0]
    fixture = login_fields(decode(packet)[2]['data'])
    b.close()

source = r'''
local ms=assert(package.loaded.ms)
local modules={}
for _,name in ipairs({'d_endlessFightUI','d_charPositionUI','d_checkLineupUI','d_activityUI',
 'd_followUI','d_cheerSquadUI','d_lineupUI','d_achieveUI'}) do
 local target=ms[name];local saved={}
 for k,v in pairs(target) do saved[k]=v end
 modules[#modules+1]={target=target,saved=saved}
end
local send=ms.d_u.main_server_send_msg
local menu=ms.d_u.createMenu
local reporter=ms.MS_report_error
local root=CCLayer:create()
CCDirector:sharedDirector():getRunningScene():addChild(root,9999)
local duty=ms.d_endlessFightUI;local position=ms.d_charPositionUI
local errors='';local sends={};local checks={}
ms.MS_report_error=function(e) errors=errors..tostring(e) end
ms.d_u.main_server_send_msg=function(mid,data) sends[#sends+1]={mid=mid,data=data} end
local function check(name,fn)
 errors='';local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]=name..':'..tostring(ok and errors=='')..':'..(err or '')..errors
end
local ok,err=xpcall(function()
 ms.d_activityUI.g_self=nil -- Tianming is not the generic activity scene
 if duty._localDutyPreviewRestore then duty._localDutyPreviewRestore() end
 assert(loadstring(PATCH))()
 check('main_entry',function()
  duty.showCharPos()
  assert(#sends==1 and sends[1].mid==1039 and sends[1].data.flag==51)
 end)
 check('native_preview',function()
  ms.d_checkLineupUI.show(FIXTURE)
  assert(position.g_charPosUI.isReadOnly)
  assert(position.g_charPosUI.playerInfo.duty_preview)
 end)
 check('native_values',function()
  for _,expected in pairs(FIXTURE.cortege_list) do
   local c=position.g_charPosUI.usedCharacters[expected.order].character
   for _,stat in ipairs({'hp','magic','gongji','fangyu','combat_power'}) do
    assert(c[stat]==expected[stat],stat..' mismatch')
   end
  end
 end)
 check('mutation_callbacks',function()
  local count=#sends
  for _,name in ipairs({'requestChangeChar','requestChangeOrder','requestChangeItem',
                       'showChgCharLayer','createChgPos','compareCharPosition','reloadData'}) do
   position[name]()
  end
  assert(#sends==count and position.g_charPosUI.isReadOnly)
 end)
 check('native_detail',function()
  position.tapHeadButton(1,true)
  assert(position.g_charPosUI.isReadOnly)
 end)
 check('normal_formation_reset',function()
  position.loadData()
  assert(not position.g_charPosUI.isReadOnly)
  assert(not (position.g_charPosUI.playerInfo or {}).duty_preview)
 end)
end,debug.traceback)
pcall(function() root:removeFromParentAndCleanup(true) end)
ms.d_u.main_server_send_msg=send;ms.d_u.createMenu=menu;ms.MS_report_error=reporter
for _,entry in ipairs(modules) do
 for k in pairs(entry.target) do if entry.saved[k]==nil then entry.target[k]=nil end end
 for k,v in pairs(entry.saved) do entry.target[k]=v end
end
if not ok then error(err) end
return table.concat(checks,'\n')
'''.replace('PATCH', summon.lua((ROOT/'network_redirect/duty_client.lua').read_text())).replace('FIXTURE', 'fixture')
if '--local-snapshot' in sys.argv:
    # Read a detached full-loadout fixture; never write the live account DB.
    import sqlite3
    with sqlite3.connect('file:'+str(ROOT/'.runtime/offline/game.sqlite3')+'?mode=ro', uri=True) as con:
        roles = [json.loads(row[0]) for row in con.execute('SELECT data FROM roles')]
    role = max(roles, key=lambda row: len(row.get('corteges', [])))
    packet = duty.inspection(role, dict(des_type=1,des_id=0,flag=51), [])[0]
    fixture = login_fields(decode(packet)[2]['data'])

source = 'local fixture='+summon.lua(fixture)+'\n'+source

def main():
    import frida
    config = load_config(ROOT/'game.json')
    pid = next(pid for pid,name in processes(config).items() if name==config['package'])
    session = frida.get_device(config['serial'], timeout=10).attach(pid)
    evaluator = LUA_EVALUATOR.replace('pending={code,resolve};',
        "const task={code,resolve};pending=task;setTimeout(()=>{if(pending===task){"
        "pending=null;resolve({status:-1,result:'No Lua frame'});}},15000);")
    script = session.create_script(evaluator)
    try:
        script.load()
        result = script.exports_sync.evaluate(source)
    finally:
        script.unload();session.detach()
    lines = result.get('result','').splitlines()
    checks = [line for line in lines if ':true:' in line or ':false:' in line]
    passed = result.get('status')==0 and len(checks)==6 and all(':true:' in line for line in checks)
    report = dict(passed=passed, native_cocos=True, captured_network=True,
                  full_account_snapshot='--local-snapshot' in sys.argv,
                  live_account_resources_changed=False, result=result)
    (ROOT/'analysis/evidence/duty/preview_native_validation.json').write_text(
        json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if not passed: raise SystemExit(1)

if __name__=='__main__': main()
