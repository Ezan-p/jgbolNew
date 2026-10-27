"""Isolated Lua 5.1 adapter checks; no emulator, live network or account writes.

Requires lupa.lua51; original Lua contracts are separately audited from bytecode.
"""
import json
from pathlib import Path
from lupa.lua51 import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]
source = (ROOT/'network_redirect/equipment_client.lua').read_text()
harness = r'''
local source=...
local checks={};local function check(name,ok) assert(ok,name);checks[#checks+1]=name end
local original_calls,refreshes,shown=0,0,{}
local parent={}
local original=function(data) original_calls=original_calls+1;return data end
local ui={g_equipPieceUI={main_layer=parent},onGetComposeResult=original,
 showPieceInfo=function() refreshes=refreshes+1 end}
local dest={};for n=1,19 do dest[n]={object_type=5,attach_type=10200+n,attach_count=1,attach_level=1} end
dest[3].attach_type=10204
local row={src_material={attach_type=10001},des_material=dest}
local nativeLookup=function(id,all) return id,all end
local data={g_convertTable={[10001]={[2]=row}},getTransInfoByTypeid=nativeLookup}
package.loaded.ms={d_equipPieceUI=ui,d_commonLayerUI={
 showPrizeResLayer=function(p,prizes) shown[#shown+1]={parent=p,prizes=prizes} end},d_data=data}
assert(loadstring(source))()
check('preview duplicate corrected',dest[3].attach_type==10203 and dest[4].attach_type==10204)
local id,all=data.getTransInfoByTypeid(7001,true)
check('native lookup arguments preserved',id==7001 and all==true)
dest[3].attach_type=10204
data.getTransInfoByTypeid(10001,true)
check('reloaded preview repaired on access',dest[3].attach_type==10203)
local adapter=ui.onGetComposeResult
check('adapter installed',adapter~=original)
local prizes={{object_type=6,attach_type=51,attach_count=1,attach_level=1}}
ui.onGetComposeResult({object_type=6,count=1,equip_type=51,attach_list=prizes})
check('typed skill reward preserved',#shown==1 and shown[1].prizes==prizes and shown[1].prizes[1].object_type==6)
check('fragment page refreshed',refreshes==1 and shown[1].parent==parent)
check('skill bypasses hardcoded item renderer',original_calls==0)
local gear={object_type=5,count=1,equip_type=2001}
check('equipment retains native callback',ui.onGetComposeResult(gear)==gear and original_calls==1)
ui.g_equipPieceUI={}
ui.onGetComposeResult({object_type=6,attach_list=prizes})
check('closed page callback safe',#shown==1 and refreshes==1)
assert(loadstring(source))()
check('adapter injection idempotent',ui.onGetComposeResult==adapter)
ui._localFragmentRestore()
check('original callback restored',ui.onGetComposeResult==original and ui._localFragmentRestore==nil)
data._localFragmentPoolRestore()
check('original preview and lookup restored',dest[3].attach_type==10204 and data.getTransInfoByTypeid==nativeLookup)
return table.concat(checks,'\n')
'''
checks = LuaRuntime().execute(harness, source).splitlines()
report = dict(passed=True, checks=checks, runtime='Lua 5.1 / isolated adapter harness',
              original_contracts='audit.json and original bytecode listings',
              visible_ui_verified=False, reason='emulator-5562 unavailable during this run',
              live_account_resources_changed=False)
(ROOT/'analysis/evidence/item_rewards/client_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(f'PASS: {len(checks)} Lua adapter checks; full UI/animation not exercised.')
