-- Isolated Lua 5.1 regression of the original funUI/tableView contracts.
local checks={}
local function check(name,fn) fn();checks[#checks+1]=name end
local function node()
 local n={children={},color={r=255,g=255,b=255}}
 function n:addChild(c) self.children[#self.children+1]=c end
 function n:getChildren()
  return {count=function() return #self.children end,objectAtIndex=function(_,i) return self.children[i+1] end}
 end
 function n:setColor(c) self.color=c end
 function n:setPosition(p) self.position=p end
 return n
end
function ccc3(r,g,b) return {r=r,g=g,b=b} end
function ccp(x,y) return {x=x,y=y} end
tolua={cast=function(n) return n end}
CCLabelTTF={create=function(_,text) local n=node();n.text=text;return n end}
local infos,sends,selected={},0,0
local thresholds={[3]=6,[5]=12,[12]=12,[23]=15,[25]=15,[36]=20,[47]=27}
local act={activityID={tongtianta=13}}
function act.getRequireLevel(id) return thresholds[id] or 0 end
function act.verifyLevel() return true end
function act.show(id) if act.verifyLevel(id) then sends=sends+1 end end
local fun={g_funUI={},funConfig={}}
for _,id in ipairs({3,5,12,13,23,25,36,47,49}) do fun.funConfig[id]={hasCCBI=true} end
local fail=false
function fun.createFunCell(parent,row)
 parent:addChild(node())
 if fail then error('native draw failed') end
 if row.hint and row.hint>0 then local n=node();n.badge=true;parent:addChild(n) end
 if fun.funConfig[row.id].hasCCBI then parent.children[1].animation=true end
end
function fun.create()
 local view={delegate={touchCellAtIndex=function(i) selected=selected+1;fun.g_funUI.last_selected=i end,
    unrelated=function() return 42 end}}
 function view:setDelegate(d) self.delegate=d end
 fun.g_funUI.funTableView=view
 fun.g_funUI.fun_list={{id=23,index=1,hint=1},{id=49,index=2}}
 return 'native-result'
end
local ms={d_activityUI=act,d_funUI=fun,d_mainUI={g_playerInfo={level=1}},
 d_info={show=function(s) infos[#infos+1]=s end}}
package.loaded.ms=ms
local originalCell,originalCreate,originalRequire,originalVerify=fun.createFunCell,fun.create,act.getRequireLevel,act.verifyLevel
-- INSTALL_PATCH
local function draw(id) local p=node();fun.createFunCell(p,{id=id,index=1,hint=1},{width=160,height=80});return p end
check('locked row remains visible, gray, labeled; badge and animation suppressed',function()
 local p=draw(23);assert(#p.children==2 and p.children[1].color.r==100 and p.children[2].text=='15级开放')
 assert(not p.children[1].animation and fun.funConfig[23].hasCCBI)
end)
check('selected-row redraw remains gray',function()
 fun.g_funUI.last_selected=1;assert(draw(23).children[1].color.r==100)
end)
check('threshold minus one blocks and exact threshold allows without stale cache',function()
 for _,id in ipairs({3,5,12,13,23,36,47}) do
  local n=act.getRequireLevel(id);ms.d_mainUI.g_playerInfo.level=n-1
  local before=sends;act.show(id);assert(sends==before and infos[#infos]=='角色达到'..n..'级开放')
  ms.d_mainUI.g_playerInfo.level=n;act.show(id);assert(sends==before+1)
  local p=draw(id);assert(p.children[1].color.r==255 and p.children[1].animation)
 end
end)
check('native regional and dynamic server levels remain live',function()
 thresholds[25]=1;assert(act.getRequireLevel(25)==1)
 thresholds[47]=38;ms.d_mainUI.g_playerInfo.level=37
 assert(not act.verifyLevel(47));assert(infos[#infos]=='角色达到38级开放')
end)
check('no-level activity retains native colors, badge and animation',function()
 ms.d_mainUI.g_playerInfo.level=1
 local p=draw(49);assert(#p.children==2 and p.children[2].badge and p.children[1].animation)
end)
check('native renderer error restores shared config',function()
 fail=true;local ok=pcall(draw,23);fail=false
 assert(not ok and fun.funConfig[23].hasCCBI)
end)
check('row tap preserves selection and alerts without sending gameplay request',function()
 assert(fun.create()=='native-result');local d=fun.g_funUI.funTableView.delegate
 local before=sends;d.touchCellAtIndex(1)
 assert(selected==1 and sends==before and infos[#infos]=='角色达到15级开放' and d.unrelated()==42)
 local count=#infos;d.touchCellAtIndex(2);assert(#infos==count and selected==2)
end)
check('level change unlocks selected activity immediately',function()
 ms.d_mainUI.g_playerInfo.level=15
 local count=#infos;fun.g_funUI.funTableView.delegate.touchCellAtIndex(1)
 assert(#infos==count and draw(23).children[1].color.r==255)
end)
check('repeated install is idempotent',function()
 local cell=fun.createFunCell
 -- INSTALL_AGAIN
 assert(fun.createFunCell==cell)
end)
check('restore removes functions and existing delegate interception',function()
 ms._localActivityLevelRestore()
 assert(fun.createFunCell==originalCell and fun.create==originalCreate)
 assert(act.getRequireLevel==originalRequire and act.verifyLevel==originalVerify)
 ms.d_mainUI.g_playerInfo.level=1;local count=#infos
 fun.g_funUI.funTableView.delegate.touchCellAtIndex(1);assert(#infos==count)
end)
return checks
