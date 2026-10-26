"""Disposable native map/shop/rank callbacks; all network sends intercepted."""
from pathlib import Path
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from network_redirect import activity, activity_babel as babel, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode
with tempfile.TemporaryDirectory() as tmp:
    b=Backend(Path(tmp),18770,lambda *a,**k:None);role=b.profile();role.update(level=90,gold_coin=100000)
    now=1792987200;activity.prepare(role,now,b.activity_rules);fixtures={}
    for op in (1,3,8):
        packet=babel.settle(role,dict(id=op,data='{}'),now,b.activity_rules,b.journey_rules,login_fields)[0]
        fixtures[str(op)]=login_fields(decode(packet)[2]['data'])
    fixtures['3']['data']['last_top']=fixtures['3']['data']['all_top']
    fixtures['3']['data']['last_my_top']=fixtures['3']['data']['my_top']
    b.close()
source='local FIXTURE='+summon.lua(fixtures)+'\n'
source+='''
local ms=assert(package.loaded.ms)
local ui=assert(ms.d_tongtiantaUI)
local saved,checks,sent={},{},{}
local function clone(v,seen)
 if type(v)~='table' then return v end
 seen=seen or {};if seen[v] then return seen[v] end
 local t={};seen[v]=t;for k,x in pairs(v) do t[k]=clone(x,seen) end;return t
end
for _,name in ipairs({'d_tongtiantaUI','d_mainUI','d_data','d_u','d_info'}) do
 local t=ms[name]; local old={};for k,v in pairs(t) do old[k]=v end
 saved[#saved+1]={t=t,old=old}
 if name=='d_tongtiantaUI' or name=='d_mainUI' or name=='d_data' then
  for k,v in pairs(t) do if type(v)=='table' then t[k]=clone(v) end end
 end
end
local already=ui._localBabelRestore
local reported={};local oldReport=ms.MS_report_error
ms.MS_report_error=function(e) reported[#reported+1]=tostring(e) end
ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
ms.d_info.show=function() end
local parent=CCLayer:create();parent:retain()
ms.d_mainUI.g_mainUI.main_layer=parent
ms.d_mainUI.g_playerInfo.level=90
ui.g_summerUI.main_layer=nil;ui.g_summerUI.shop_layer=nil
'''
source+=(ROOT/'network_redirect/babel_client.lua').read_text()+'\n'
source+='''
local function check(name,fn)
 reported={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,ok=ok and #reported==0,error=(err or '')..table.concat(reported,'\\n')}
end
check('original map and resource widgets',function() ui.onGetResult(FIXTURE['1']) end)
check('six-slot shop',function() ui.onGetResult(FIXTURE['8']) end)
check('current and last offline rankings',function() ui.onGetResult(FIXTURE['3']) end)
check('overflow energy callback',function() ui.onGetResult({id=10,data={energy=415}}) end)
check('life callback',function() ui.onGetResult({id=11,data={life=100}}) end)
if not already and ui._localBabelRestore then ui._localBabelRestore() end
parent:removeAllChildrenWithCleanup(true);parent:release()
for i=#saved,1,-1 do local v=saved[i];for k in pairs(v.t) do v.t[k]=nil end;for k,x in pairs(v.old) do v.t[k]=x end end
ms.MS_report_error=oldReport
local passed=0;for _,v in ipairs(checks) do if v.ok then passed=passed+1 end end
return ms.d_json.encode({passed=passed,total=#checks,checks=checks,native_cocos=true,detached_layer=true,state_restored=true,sends_captured=#sent})
'''
out=ROOT/'.runtime/babel-native-fixture.lua';out.write_text(source);print(out)
