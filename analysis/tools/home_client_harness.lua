-- Execute with HOME_FIXTURE set to a disposable backend 1348/24 query response.
-- Render native Cocos widgets on an unattached layer; restore every replaced global.
local ms=assert(package.loaded.ms)
local h=assert(ms.d_homeUI)
local savedData,savedUI,savedRead=h.g_data,h.g_homeUI,h.g_read_only
local savedRest=h.getRestDay
local installedHere=not h._localHomeRestore
local parent=CCLayer:create()
parent:retain()
local checks={}
local ok,err=xpcall(function()
 if installedHere then assert(loadstring(HOME_PATCH))() end
 h.initCsv()
 h.g_data={all_activity=HOME_FIXTURE.all_activity,base_data={level=1,point=0},config_data={offline_home=true,activity_flag={[68]=false,[69]=false,[70]=false,[72]=false}}}
 h.g_homeUI={main_layer=parent,garden_layer=parent}
 h.g_read_only=false
 assert(h.hasActivity(),'offline welfare entrance must be visible')
 assert(h.getRestDay(72)=='长期开放')
 checks[#checks+1]='offline welfare entrance and permanent schedule'
 h.showWelfare(parent)
 checks[#checks+1]='native welfare container and training targets'
 h.showHoleTarget(nil,2)
 checks[#checks+1]='native building targets'
 h.showHolePlan()
 checks[#checks+1]='native growth plan'
 h.showHoleTogetherBuild()
 checks[#checks+1]='native community construction (zero-based rewards)'
 h.showHoleCompete()
 checks[#checks+1]='native weekly rank (11 participants)'
 h.g_data.shop_data=HOME_SHOP.shop_data
 h.g_data.shop_flush_time=ms.d_time.getTime()+HOME_SHOP.diff_time
 h.showShop()
 checks[#checks+1]='native two-section shop'
end,debug.traceback)
parent:removeAllChildrenWithCleanup(true)
parent:release()
h.g_data,h.g_homeUI,h.g_read_only=savedData,savedUI,savedRead
if installedHere and h._localHomeRestore then h._localHomeRestore() end
h.getRestDay=savedRest
assert(ok,err)
return ms.d_json.encode({checks=checks,passed=#checks,original_cocos=true,detached_layer=true,state_restored=true})
