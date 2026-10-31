local source=...
local checks={}
local function check(name,ok) assert(ok,name);checks[#checks+1]=name end
local originalCalls,shown,info=0,0,nil
local ui={g_self={csv={[1]={[14]={}},[2]={[14]={}},[3]={[14]={}}}},g_stoneCastUI={}}
local original=function(...) originalCalls=originalCalls+1;return 'native' end
ui.pressCast=original
ui.initConfig=function() end
ui.showTilian=function() shown=shown+1;return 'refine' end
local ms={d_stoneCastUI=ui,d_mainUI={g_playerInfo={reborn_layer=4}},
 d_roleRebornUI={g_reborn_condition={[4]={rights={open_stone_sys=true}}}},
 d_common_def={object_type={item=5}},d_data={getCertainInfo=function(_,tid) return {sub_type=tid-1089} end},
 d_info={show=function(text) info=text end},d_hz={gethz=function(key) return key end}}
package.loaded.ms=ms
assert(loadstring(source))()
local patched=ui.pressCast
assert(loadstring(source))()
check('repeat injection is idempotent',patched==ui.pressCast)
for level=9,14 do
 local stone={level=level,type_id=1090,csvInfo={sub_type=1}}
 local before=originalCalls
 local ret=ui.pressCast('parent',stone,321)
 if level==13 then
  check('level 13 opens native refinement',ret=='refine' and originalCalls==before)
  check('target identity and parent preserved',ui.g_stoneCastUI.stone==stone and ui.g_stoneCastUI.parent_layer=='parent' and ui.g_stoneCastUI.zOrder==321 and stone.level==13)
 else check('native path preserved for level '..level,ret=='native' and originalCalls==before+1) end
end
for kind=1,3 do
 check('uncached item type '..kind,ui.pressCast('p',{level=13,type_id=1089+kind})=='refine' and ui.g_stoneCastUI.zOrder==100)
end
local count=shown
ms.d_mainUI.g_playerInfo.reborn_layer=3
ui.pressCast('p',{level=13,type_id=1090})
check('fourth realm required',shown==count and info=='asc30')
ms.d_mainUI.g_playerInfo.reborn_layer=4
ms.d_roleRebornUI.g_reborn_condition[4].rights.open_stone_sys=false
ui.pressCast('p',{level=13,type_id=1090})
check('stone system rights required',shown==count)
ms.d_roleRebornUI.g_reborn_condition[4]=nil
ui.pressCast('p',{level=13,type_id=1090})
check('missing rights rejected safely',shown==count)
ui.g_self.csv[1][14]=nil
check('missing recipe retains native guard',ui.pressCast('p',{level=13,type_id=1090})=='native')
ui._localStoneRefineRestore()
check('restore removes wrapper',ui.pressCast==original and ui._localStoneRefineRestore==nil)
assert(loadstring(source))()
check('reinstall supported',ui.pressCast~=original)
return checks
