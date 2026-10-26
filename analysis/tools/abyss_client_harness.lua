-- Native widgets and callbacks with all sends captured, on an unattached layer.
local ms=assert(package.loaded.ms)
local ui=assert(ms.d_abyssUI)
local saved={};local checks={};local sent={};local errors={}
local function clone(t,seen)
 if type(t)~='table' then return t end
 seen=seen or {};if seen[t] then return seen[t] end
 local out={};seen[t]=out;for k,v in pairs(t) do out[k]=clone(v,seen) end;return out
end
local function preserve(t)
 local old={};for k,v in pairs(t) do old[k]=v end
 saved[#saved+1]={t=t,old=old}
end
for _,name in ipairs({'d_abyssUI','d_treasureMapUI','d_mainUI','d_data','d_u','d_info','d_yaoshendianUI','d_lineupUI'}) do
 if ms[name] then preserve(ms[name]) end
end
ui.g_self=clone(ui.g_self)
ms.d_treasureMapUI.g_self=clone(ms.d_treasureMapUI.g_self)
ms.d_mainUI.g_playerInfo=clone(ms.d_mainUI.g_playerInfo)
ms.d_data.g_new_config=clone(ms.d_data.g_new_config)
local oldReport=ms.MS_report_error
ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
ms.d_info.show=function() end
ms.d_mainUI.g_playerInfo.level=80;ms.d_mainUI.g_playerInfo.drug_level=36
local parent=CCLayer:create();parent:retain()
ui.g_data={hook=FIXTURE['1']}
ui.g_abyssUI={hook_layer=parent,hell_layer=parent,boss_layer=parent}
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,ok=ok and #errors==0,error=(err or '')..table.concat(errors,'\n')}
end
check('hook and income news',function() ui.showHookLayer(parent) end)
check('temporary bag',function() ui.onGetResult(FIXTURE['10']) end)
check('soul crystal shop',function() ui.onGetResult(FIXTURE['13']) end)
check('daily statistics',function() ui.onGetResult(FIXTURE['9']) end)
check('floor81 boss and pill slots',function() ui.onGetResult(FIXTURE['16']) end)
check('top20 NPC ranking',function() ui.onGetResult(FIXTURE['7']) end)
for kind=1,5 do
 check('random event '..kind,function() ui.onGetResult(FIXTURE['event'..kind]) end)
end
check('treasure map',function()
 local map=ms.d_treasureMapUI
 map.g_treasureMapUI={parent=parent,type_id=1431}
 map.onGetResult(FIXTURE.map)
end)
check('treasure draw callback',function() ms.d_treasureMapUI.onGetResult(FIXTURE.map_draw) end)
parent:removeAllChildrenWithCleanup(true);parent:release()
for i=#saved,1,-1 do
 local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end
 for k,v in pairs(row.old) do row.t[k]=v end
end
ms.MS_report_error=oldReport
local passed=0;for _,row in ipairs(checks) do if row.ok then passed=passed+1 end end
return ms.d_json.encode({checks=checks,passed=passed,total=#checks,sends_captured=#sent,
 original_cocos=true,detached_layer=true,state_restored=true})
