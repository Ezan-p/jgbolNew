-- Real stage-10 server event -> native level-2 box -> native confirm -> task guide.
local ms=assert(package.loaded.ms)
local main,guide=ms.d_mainUI,ms.d_guideUI
local saved,checks,errors={},{},{}
local function preserve(t)
 local old={};for k,v in pairs(t) do old[k]=v end
 saved[#saved+1]={t=t,old=old}
end
for _,t in ipairs({main,guide,ms.d_u}) do preserve(t) end
local oldReport=ms.MS_report_error
ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
local layer=CCLayer:create();layer:retain()
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]=name..':'..tostring(ok and #errors==0)..':'..(err or '')..table.concat(errors,' ')
end
local ok,err=xpcall(function()
 main.g_playerInfo=ms.d_c.table_copy(main.g_playerInfo)
 main.g_playerInfo.level=2
 main.g_playerInfo.guide_progress=2046
 main.g_isNeedGuide=true;main.g_isNeedHint=true
 guide.g_currentGuide=guide.guideState.guideLevelUp
 local confirm,task=false,false
 local menu=ms.d_u.createMenu
 ms.d_u.createMenu=function(styles,...)
  for _,s in ipairs(styles) do
   if s.npic=='v2/multi-selectUI/ensure1.png' then confirm=s.call_back end
  end
  return menu(styles,...)
 end
 ms.d_u.main_server_send_msg=function() error('unexpected live request') end
 guide.guideViewQuestFunc=function() task=true end
 check('tutorial_upgrade_event',function()
  ms.d_event_mgr.msg_common_event_2998(nil,UPGRADE,nil)
  assert(main.g_playerInfo.isLevelUp)
  assert(main.g_playerInfo.levelUpInfo.old_level==1 and main.g_playerInfo.levelUpInfo.new_level==2)
 end)
 check('tutorial_upgrade_box_and_arrow',function()
  main.playerLevelUp(layer)
  assert(main.g_levelUpLayer and main.g_ensureLevelBtn and type(confirm)=='function')
  assert(guide.g_currentGuide==guide.guideState.guideViewQuest)
 end)
 check('tutorial_upgrade_confirm_continues_task',function()
  confirm()
  assert(task)
 end)
end,debug.traceback)
layer:removeAllChildrenWithCleanup(true);layer:release()
ms.MS_report_error=oldReport
for i=#saved,1,-1 do
 local s=saved[i];for k in pairs(s.t) do s.t[k]=nil end
 for k,v in pairs(s.old) do s.t[k]=v end
end
if not ok then checks[#checks+1]='upgrade_harness:false:'..err end
return table.concat(checks,'\n')
