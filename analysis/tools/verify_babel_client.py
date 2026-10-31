"""Lua 5.1 client compatibility checks (requires lupa.lua51 on PYTHONPATH)."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from lupa.lua51 import LuaRuntime
from network_redirect import summon
vm=LuaRuntime(unpack_returned_tuples=True)
vm.execute('''
local ui={g_self={}}
local gethz=function(key) return 'original:'..key end
ui.showRank=function() return gethz('tongtianta18'),gethz('tongtianta19'),gethz('other') end
ui.onGetResult=function(msg)
 if msg.id==3 then
  assert(ui.g_self.rankData[1].my_top_data.order==7)
  if msg.data.last_my_top.order then
   assert(ui.g_self.rankData[2].my_top_data.order==2)
  else
   assert(ui.g_self.rankData[2].my_top_data==nil)
  end
 end
 return 'native-result'
end
package.loaded.ms={d_tongtiantaUI=ui,d_tongtiantaSecretUI={onGetResult=function() return 'secret-result' end},d_info={show=function(text) message=text end}}
originalResult=ui.onGetResult
originalSecret=package.loaded.ms.d_tongtiantaSecretUI.onGetResult
''')
source=(ROOT/'network_redirect/babel_client.lua').read_text()
vm.execute(source)
assert vm.execute("return package.loaded.ms.d_tongtiantaUI.showRank()") == (
    '离线NPC榜：同层按到达时间排名','周四结算，周一重置；奖励由系统邮件领取','original:other')
vm.execute('''
local ui=package.loaded.ms.d_tongtiantaUI
assert(ui.onGetResult({id=3,data={my_top={order=7},last_my_top={order=2}}})=='native-result')
ui.onGetResult({id=3,data={my_top={order=7},last_my_top={}}})
ui.onGetResult({id=2,data={completed_now=true}})
assert(string.find(message,'70'))
local secret=package.loaded.ms.d_tongtiantaSecretUI
assert(secret.onGetResult({id=13,data={completed_now=true}})=='secret-result')
assert(string.find(message,'1张入场券'))
wrappedSecret=secret.onGetResult
wrappedResult=ui.onGetResult
''')
vm.execute(source)
vm.execute('''
local ui=package.loaded.ms.d_tongtiantaUI
assert(ui.onGetResult==wrappedResult)
ui._localBabelRestore()
assert(ui.onGetResult==originalResult)
assert(ui.showRank()=='original:tongtianta18')
assert(ui._localBabelRestore==nil)
local secret=package.loaded.ms.d_tongtiantaSecretUI
assert(secret.onGetResult==wrappedSecret)
secret._localBabelSecretRestore()
assert(secret.onGetResult==originalSecret)
''')
# Load, do not execute, the entire production injection to catch composition errors.
vm.globals().full_source=summon.client_source(summon.load_rules())
vm.execute('assert(loadstring(full_source))')
report=dict(passed=True,lua_version='5.1',native_cocos=False,
            checks=['personal current/last rank and absent last-week data before original rendering','offline/mail text with fallback',
                    'ordinary and secret completion notifications','idempotent install','restore original callbacks/upvalues',
                    'full production injection compiles'])
(ROOT/'analysis/evidence/babel/client_patch_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))
