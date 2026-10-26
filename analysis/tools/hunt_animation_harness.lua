-- Run an actual timed native shot over a temporary visible layer, then restore.
local ms=assert(package.loaded.ms);local ui=assert(ms.d_soulHuntUI)
assert(not hunt_animation_restore,'restore previous animation first')
local saved,errors={},{}
local function keep(t) local old={};for k,v in pairs(t) do old[k]=v end;saved[#saved+1]={t=t,old=old} end
local function up(fn,key)
 for i=1,30 do local k,v=debug.getupvalue(fn,i);if k==key then return v end;if not k then break end end
 error(key)
end
local state=up(ui.onGetResponse,'g_self');local view=up(ui.onGetResponse,'g_soulHuntUI')
for _,t in ipairs({state,view,ms.d_activityUI,ms.d_u,ms.d_data,ms.d_file,ms.d_time,ms.d_mainUI}) do keep(t) end
for k in pairs(state) do state[k]=nil end;state.Below=-20;state.Speed=500
for k in pairs(view) do view[k]=nil end
local report=ms.MS_report_error;ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
local root=CCLayer:create();CCDirector:sharedDirector():getRunningScene():addChild(root,9999)
ms.d_activityUI.g_self={main_layer=root};ms.d_activityUI.show=function() end
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(ms.d_mainUI.g_playerInfo);ms.d_mainUI.g_playerInfo.level=60
ms.d_time.getTime=function() return FIXTURE.now end
ms.d_file.set=function() end;ms.d_file.get=function() return true end
ms.d_u.main_server_send_msg=function() error('unexpected live request') end
function hunt_animation_restore()
 root:removeFromParentAndCleanup(true)
 for i=#saved,1,-1 do local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end;for k,v in pairs(row.old) do row.t[k]=v end end
 ms.MS_report_error=report;hunt_animation_restore=nil
end
local ok,err=xpcall(function()
 ui.updateActivityStatus(FIXTURE.status);ui.onGetResponse(ms.d_c.table_copy(FIXTURE.entry))
 state.ball=1;state.degree=90;ui.showBall();ui.showCannon()
 ms.d_u.delay(root,2,function() ui.onGetResponse(ms.d_c.table_copy(FIXTURE.shot)) end)
 ms.d_u.delay(root,6,function()
  local pass,message=xpcall(function()
   assert(#errors==0,table.concat(errors,'\n'))
   local n=0;for _,p in pairs(state.role_hunt_data.point_list) do n=n+1;assert(p.x==300 and p.y==400) end
   assert(n==1,'captured sprites not removed');assert(state.role_hunt_data.left_energy==380)
   assert(state.role_hunt_data.left_soul_count==100066,'combo/balance mismatch')
  end,debug.traceback)
  hunt_animation_result={passed=pass,error=message or '',native_timed_animation=true}
  hunt_animation_restore()
 end)
end,debug.traceback)
if not ok then hunt_animation_restore();error(err) end
return 'native animation running; auto restore after six seconds'
