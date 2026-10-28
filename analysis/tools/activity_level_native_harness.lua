-- Original Cocos functions on detached layers; never send gameplay packets.
local ms=assert(package.loaded.ms)
local act,fun=ms.d_activityUI,ms.d_funUI
local saved={player=ms.d_mainUI.g_playerInfo,state=fun.g_funUI,self=fun.g_self,
 list=fun.getFunList,info=ms.d_info.show,send=ms.d_u.main_server_send_msg}
local checks,roots,notices={}, {}, {}
local sent=0
local function install()
 -- INSTALL_PATCH
end
if ms._localActivityLevelRestore then ms._localActivityLevelRestore() end
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
fun.g_self=ms.d_c.table_copy(saved.self)
fun.g_funUI={}
ms.d_info.show=function(s) notices[#notices+1]=s end
ms.d_u.main_server_send_msg=function() sent=sent+1 end
local function check(name,fn)
 local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]=name..':'..tostring(ok)..':'..tostring(err or '')
end
local function root()
 local p=CCLayer:create();p:retain();roots[#roots+1]=p;return p
end
local function draw(id,index)
 local p=root();fun.createFunCell(p,{id=id,index=index or 1,hint=1},CCSizeMake(200,100))
 local c=p:getChildren()
 return p,tolua.cast(c:objectAtIndex(0),'CCSprite')
end
install()
check('original locked Cocos sprite gray and exact label',function()
 ms.d_mainUI.g_playerInfo.level=14
 local p,icon=draw(act.activityID.qifu)
 local color=icon:getColor();assert(color.r==100 and color.g==100 and color.b==100)
 local children=p:getChildren();assert(children:count()==2)
 assert(tolua.cast(children:objectAtIndex(1),'CCLabelTTF'):getString()=='15级开放')
end)
check('original selected sprite stays gray',function()
 fun.g_funUI.last_selected=1
 local _,icon=draw(act.activityID.qifu);assert(icon:getColor().r==100)
end)
check('original click route blocks all fixed activity thresholds',function()
 local fixed={xiulian=5,fengshenbang=6,dujie=8,tianmingzhizhan=12,undergo=12,
  pantaohui=13,qifu=15,cortegeRecycle=15,cortCall=16,soulHunt=20,answer=20,
  tongtianta=36,land=38,home=50,abyss=70,monday=15,fishrush=20,
  twoyears=20,rulaitable=20,tower=20,destiny=30,forge=30}
 for name,n in pairs(fixed) do
  local id=act.activityID[name];assert(act.getRequireLevel(id)==n,name)
  ms.d_mainUI.g_playerInfo.level=n-1;act.show(id)
  assert(notices[#notices]=='角色达到'..n..'级开放',name)
  assert(sent==0,name)
  ms.d_mainUI.g_playerInfo.level=n;assert(act.verifyLevel(id),name)
 end
end)
check('original unlocked cell restores color and native hint',function()
 ms.d_mainUI.g_playerInfo.level=15
 local p,icon=draw(act.activityID.qifu)
 assert(icon:getColor().r==255 and p:getChildren():count()==2)
end)
check('original table view selection alerts and retains detail panel',function()
 ms.d_mainUI.g_playerInfo.level=14
 fun.getFunList=function() return {{id=act.activityID.qifu,index=1,hint=1},
  {id=act.activityID.cortegeRecycle,index=2,hint=1}} end
 fun.g_funUI={main_layer=root()}
 fun.create()
 local view=assert(fun.g_funUI.funTableView)
 view.delegate.touchCellAtIndex(2)
 assert(fun.g_funUI.last_selected==2 and notices[#notices]=='角色达到15级开放')
 assert(sent==0)
 fun.pressMenu();assert(notices[#notices]=='角色达到15级开放' and sent==0)
end)
check('original renderer and list filter restored',function()
 ms._localActivityLevelRestore()
 assert(not ms._localActivityLevelRestore)
 fun.getFunList=saved.list
end)
-- Release detached native objects before restoring the live window references.
for _,p in ipairs(roots) do p:removeAllChildrenWithCleanup(true);p:release() end
fun.g_funUI=saved.state;fun.g_self=saved.self;fun.getFunList=saved.list
ms.d_mainUI.g_playerInfo=saved.player;ms.d_info.show=saved.info
ms.d_u.main_server_send_msg=saved.send
install() -- Leave the requested behavior installed for the live client as well.
return table.concat(checks,'\n')
