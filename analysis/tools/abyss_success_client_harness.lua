-- Original Cocos rendering on a detached layer, with no server requests.
local ms=assert(package.loaded.ms)
local ui=assert(ms.d_abyssUI)
local saved={}
for _,module in ipairs({ui,ms.d_u,ms.d_data}) do
 local old={};for k,v in pairs(module) do old[k]=v end
 saved[#saved+1]={module,old}
end
local parent=CCLayer:create();parent:retain()
local checks={}
local function check(name,fn)
 local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,ok=ok,error=err}
 parent:removeAllChildrenWithCleanup(true)
end
if ui._localAbyssSuccessRestore then ui._localAbyssSuccessRestore() end
local success=ui.showChallengeSuccess
local env=getfenv(success)
local swallow=ms.d_u.createSwallowTouchLayer
local mask
ms.d_u.createSwallowTouchLayer=function(layer,...)
 mask=layer;return swallow(layer,...)
end
-- Run the actual delayed renderer now, so a Lua failure reaches the check.
ms.d_u.delay=function(_,_,fn) return fn() end
ms.d_u.main_server_send_msg=function() error('unexpected server request') end
check('unpatched native currency reward reproduces stuck overlay',function()
 ui.g_data={boss={prize_list=REWARDS['1']}}
 local ok,err=pcall(success,parent)
 assert(not ok and tostring(err):find("local 'itemInfo'"),tostring(err))
 local layer=tolua.cast(mask:getChildren():objectAtIndex(3),'CCLayer')
 assert(not layer:isTouchEnabled(),'expected the old close handler to be missing')
 assert(getfenv(success)==env)
end)
assert(loadstring(ABYSS_PATCH))()
for _,floor in ipairs({'1','40','81'}) do
 check('native floor '..floor..' rewards finish and enable close touch',function()
  ui.g_data={boss={prize_list=REWARDS[floor]}}
  ui.showChallengeSuccess(parent)
  assert(mask and mask:getParent()==parent)
  -- Native child order: swallow, background, success banner, reward layer.
  local layer=tolua.cast(mask:getChildren():objectAtIndex(3),'CCLayer')
  assert(layer and layer:isTouchEnabled(),'close touch was never enabled')
  assert(getfenv(success)==env)
 end)
end
parent:release()
for i=#saved,1,-1 do
 local row=saved[i]
 for k in pairs(row[1]) do row[1][k]=nil end
 for k,v in pairs(row[2]) do row[1][k]=v end
end
local passed=0;for _,row in ipairs(checks) do if row.ok then passed=passed+1 end end
return ms.d_json.encode({checks=checks,passed=passed,total=#checks,
 native_cocos=true,detached_layer=true,state_restored=true,live_save_modified=false})
