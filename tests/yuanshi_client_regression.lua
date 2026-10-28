-- Isolated Lua 5.1 checks for permanent entry, server deadlines and stale actions.
local now=1000
local sent,styles,callbacks={},{},{}
local layer={children={}}
function layer:removeChildByTag(tag) self.children[tag]=nil end
function layer:addChild(node,z,tag) if tag then self.children[tag]=node end end
local ms={d_time={},d_data={g_new_config={[24]={}}},d_activityUI={},d_u={},d_msg_def={gscl_msg_id={msg_yuanshi_activity=1334}}}
package.loaded.ms=ms
local ui={g_self={main_layer=layer,timeTag=12348,detailTag=1349},my=0.32,h=0.09}
ms.d_twoYearsCelebrateUI=ui
ms.d_time.getTime=function() return now end
ms.d_u.createByStyles=function(style) styles[#styles+1]=style;return style end
ms.d_u.delay=function(parent,seconds,fn) callbacks[#callbacks+1]=fn end
ms.d_u.main_server_send_msg=function(mid,data) assert(mid==1334);sent[#sent+1]=data end
ms.d_data.callback_update_config=function() end
ms.d_activityUI.getQiwenStatus=function() end
ms.d_activityUI.g_currentActivity=46
ui.canJoin=function() return false end
ui.tickTime=function() error('native expiry timer called') end
ui.createMainFrame=function()
 ms.d_u.createByStyles({pic='v2/moonCakeUI/time.png',x=0.13,y=0.824})
 ui.tickTime()
end
ui.showNews=function() end
ui.onGetResult=function(d) ui.g_self[d.flag]=d end
ui.closeShop=function() ui.g_self.shoplayer=nil end
for name,flag in pairs({pray=2,getChar=2,buy=4,openGiftPackEnsure=1,createShop=3,openGiftPack=1,showGiftDetail=1}) do
 ui[name]=function() sent[#sent+1]={flag=flag} end
end
local originalTick,originalFrame,originalPray=ui.tickTime,ui.createMainFrame,ui.pray
local function snapshot(start)
 return {flag=0,begin_time=start,end_time=start+14*86400,refresh_time=start+14*86400,
 permanent=true,cur_progress=0,free_times=1,gift_list={},claimed=false}
end
-- INSTALL_PATCH
ui.onGetResult(snapshot(now))
assert(ui.canJoin(),'inclusive cycle start must be open')
local create=ms.d_u.createByStyles
ui.createMainFrame()
assert(styles[1].string=='距下次刷新' and not styles[1].pic,'old expiry caption survived')
assert(layer.children[12348].string=='14天00:00:00')
assert(math.abs(layer.children[12348].y-0.752)<0.00001,'native timer layout changed')
assert(ms.d_u.createByStyles==create)
now=now+1;callbacks[#callbacks]()
assert(layer.children[12348].string=='13天23:59:59')
ui.pray();assert(sent[#sent].flag==2)
now=1000+14*86400
callbacks[#callbacks]()
assert(ui.canJoin(),'entry closed at refresh boundary')
assert(layer.children[12348].string=='0天00:00:00')
local n=#sent;assert(sent[n].flag==0)
for _,name in ipairs({'pray','getChar','buy','openGiftPackEnsure','createShop','openGiftPack','showGiftDetail'}) do ui[name]() end
assert(#sent==n,'expired actions escaped refresh query')
now=now+3;ui.pray();assert(#sent==n+1 and sent[#sent].flag==0)
ui.g_self.shoplayer={};ui.g_self[3]={};ui.g_self[4]={};layer.children[1349]={}
ms.d_data.callback_update_config({local_yuanshi=snapshot(1000+14*86400)})
assert(not ui.g_self.shoplayer and not ui.g_self[3] and not ui.g_self[4] and not layer.children[1349])
callbacks[#callbacks]()
assert(layer.children[12348].string=='13天23:59:57')
ui.pray();assert(sent[#sent].flag==2)
-- Common-config updates can precede the activity snapshot; stale UI still queries.
now=1000+28*86400
ms.d_activityUI.getQiwenStatus({yuanshi_info=snapshot(now)})
n=#sent;ui.pray();assert(#sent==n+1 and sent[#sent].flag==0)
ms.d_data.g_new_config[24].yuanshi_info={begin_time=0,end_time=0,permanent=false}
assert(not ui.canJoin())
ui._localYuanshiRestore()
assert(ui.tickTime==originalTick and ui.createMainFrame==originalFrame and ui.pray==originalPray)
assert(not ui._localYuanshiRestore and not ui._localYuanshiVersion)
return 'permanent entry, fortnight timer, rollover query, stale actions, dialog/cache reset and restoration passed'
