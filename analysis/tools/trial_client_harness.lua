local ms=assert(package.loaded.ms)
if trialFixtureRestore then trialFixtureRestore() end
local oldUI,oldLoaded=ms.d_shilianUI,package.loaded['ui.shilianUI']
package.loaded['ui.shilianUI']=nil
local ui=require('ui.shilianUI');ms.d_shilianUI=ui
local saved,checks,sent,errors,notices={},{},{},{},{}
local function preserve(t)
 local old={};for k,v in pairs(t) do old[k]=v end;saved[#saved+1]={t=t,old=old}
end
for _,t in ipairs({ms.d_activityUI,ms.d_u,ms.d_time,ms.d_info,ms.d_event_mgr,ms.d_lineupUI}) do preserve(t) end
local report=ms.MS_report_error;ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
local root=CCLayer:create();root:retain()
-- Cocos registers menu touch delegates on enter; an entirely detached parent
-- can assert when the original reward/encounter widgets change touch priority.
root:setVisible(false)
CCDirector:sharedDirector():getRunningScene():addChild(root,10000)
function trialFixtureRestore()
 if ui._localTrialRestore then ui._localTrialRestore() end
 root:removeFromParentAndCleanup(true);root:release()
 for _,v in ipairs(saved) do
  for k in pairs(v.t) do v.t[k]=nil end
  for k,x in pairs(v.old) do v.t[k]=x end
 end
 ms.MS_report_error=report;ms.d_shilianUI=oldUI;package.loaded['ui.shilianUI']=oldLoaded
 trialFixtureRestore=nil
end
ms.d_activityUI.g_self={main_layer=root};ms.d_activityUI.g_isCurrentSenceRun=true
ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
ms.d_u.delay=function() end
ms.d_info.show=function(message) notices[#notices+1]=message end
local now=FIXTURE.now
ms.d_time.getTime=function() return now end
ms.d_lineupUI.saveLastFightLevel=function() end
ms.d_event_mgr.g_fight_info={};ms.d_event_mgr.g_fight_id_list={}
local function up(fn,key)
 for i=1,100 do local n,v=debug.getupvalue(fn,i);if not n then break end;if n==key then return v end end
 error('missing upvalue '..key)
end
local native=ui.processStatus
local show=up(native,'show');local state=up(show,'dataTable')
local getBoss=up(native,'getBoosInfo')
local left=up(show,'createLeftPanel')
local select=up(left,'selectBoss')
local below=up(select,'createBelowMenuStatus')
local challenge=up(below,'startChallenge');local claim=up(below,'requestTakePrize')
-- INSTALL_PATCH
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,ok=ok and #errors==0,error=(err or '')..table.concat(errors,'\n')}
end
local function response(d) ui.processStatus(ms.d_c.table_copy(d)) end
check('original activity entry request',function()
 ms.d_activityUI.requestShiLian()
 assert(sent[#sent].mid==1064 and sent[#sent].data.flag==2)
end)
check('native boss preview and challenge request',function()
 response(FIXTURE.entry);assert(state.main_layer)
 assert(up(getBoss,'bossList')[1].type_id==5022)
 assert(#up(getBoss,'bossList')[1].prize_list==2)
 challenge();local q=sent[#sent]
 assert(q.mid==1026 and q.data.des_type==8 and q.data.des_value==0 and q.data.des_id==5022 and q.data.fight_type==11)
end)
check('native full five star model pool',function()
 for _,tid in ipairs(FIXTURE.pool) do
  assert(ms.d_lineupUI.g_characterAttrTable[tid].quality==5)
  assert(type(ms.d_data.getBodySprite(tid))=='userdata','missing model '..tid)
  assert(type(ms.d_data.getHeadSprite(tid))=='userdata','missing portrait '..tid)
 end
end)
check('real backend replay native parser',function()
 local mgr=ms.d_event_mgr;local fid
 for _,row in ipairs(FIXTURE.wire) do
  if row[1]==1028 then fid=row[2].fight_id;mgr.fight_lineup_1028(nil,row[2],0)
  elseif row[1]==1027 then mgr.fight_result_1027(nil,row[2],0)
  elseif row[1]==2998 then mgr.msg_common_event_2998(nil,row[2],nil) end
 end
 assert(mgr.g_fight_info[fid].line_up_msg.lineup[1].des_type==5022)
end)
check('native cooldown damage and fight return',function()
 ui.fightEnd()
 assert(up(getBoss,'fightCount')==1)
 assert(up(getBoss,'bossList')[1].hp==FIXTURE.fight.train_data.hp)
 local n=#sent;challenge();assert(#sent==n)
 now=FIXTURE.now+61;show();challenge();assert(#sent>n and sent[#sent].mid==1026)
end)
check('native kill state and reward button',function()
 response(FIXTURE.kill);ui.fightEnd()
 assert(up(getBoss,'bossList')[1].is_dead)
 claim();assert(sent[#sent].mid==1064 and sent[#sent].data.flag==9)
end)
check('native pending reward reconnect',function()
 now=FIXTURE.now
 response(FIXTURE.dead);assert(up(getBoss,'bossList')[1].is_dead)
 claim();assert(sent[#sent].data.flag==9)
end)
check('native claim clears boss and stale challenge widgets',function()
 response(FIXTURE.claim);assert(#up(getBoss,'bossList')==0)
 assert(state.main_layer:getChildByTag(1001):getChildrenCount()==0)
 assert(state.main_layer:getChildByTag(1005):getChildrenCount()==0)
end)
check('cooldown menu refresh after claiming has no stale boss access',function()
 -- Call the same menu builder used when the native countdown expires.
 -- Do not manually invoke callbacks whose Cocos nodes were already cleaned up.
 below()
 assert(state.lastSelectBoss==nil)
 assert(state.main_layer:getChildByTag(1005):getChildrenCount()==0)
end)
check('completed daily entry has accurate message',function()
 response(FIXTURE.complete)
 assert(string.find(notices[#notices],'明日零点',1,true))
end)
check('reenter after native state replacement still cleans claimed boss',function()
 for i=1,100 do
  local name=debug.getupvalue(show,i)
  if not name then break end
  if name=='dataTable' then debug.setupvalue(show,i,{});break end
 end
 response(FIXTURE.dead);state=up(show,'dataTable')
 response(FIXTURE.claim)
 assert(state.lastSelectBoss==nil)
 assert(state.main_layer:getChildByTag(1001):getChildrenCount()==0)
 assert(state.main_layer:getChildByTag(1005):getChildrenCount()==0)
end)
check('friend help disabled without sending a request',function()
 local n=#sent
 for _,flag in ipairs({3,4,7}) do ms.d_u.main_server_send_msg(1064,{flag=flag,id=1}) end
 assert(#sent==n and string.find(notices[#notices],'暂未开放',1,true))
end)
check('native journey encounter popup',function()
 response({flag=5,result=1,train_data={type_id=5022}})
 assert(#up(native,'encounterType')==1)
 ui.showEncounterBoss(root,function() end)
 assert(#up(native,'encounterType')==0)
end)
trialFixtureRestore()
local out={};for _,v in ipairs(checks) do out[#out+1]=v.name..':'..tostring(v.ok)..':'..v.error end
return table.concat(out,'\n')
