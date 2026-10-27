-- Exercise original callbacks and scratch widgets on a detached Cocos layer.
local ms=assert(package.loaded.ms);local ui=assert(ms.d_loginGameUI)
local saved={};local checks={};local errors={};local sent={}
local function preserve(t)
 local old={};for k,v in pairs(t) do old[k]=v end;saved[#saved+1]={t=t,old=old}
end
for _,name in ipairs({'d_loginGameUI','d_activityUI','d_mainUI','d_u','d_data','d_commonLayerUI','d_packageUI','d_event_mgr'}) do preserve(ms[name]) end
if ui._localVisitRestore then ui._localVisitRestore() end
-- INSTALL_PATCH
local report=ms.MS_report_error;ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
local root=CCLayer:create();root:retain()
ms.d_activityUI.g_self={main_layer=root};ms.d_activityUI.g_isCurrentSenceRun=true
ms.d_activityUI.activityStatus={}
local player={};for k,val in pairs(ms.d_mainUI.g_playerInfo) do player[k]=val end
ms.d_mainUI.g_playerInfo=player
ui.g_prize={{},0,0};ui.g_visitList={}
ms.d_packageUI.g_isInPackage=false
ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,ok=ok and #errors==0,error=(err or '')..table.concat(errors,'\n')}
end
check('native query and three choices',function()
 ui.getResFromServer(FIXTURE.query);assert(#ui.g_visitList==3);assert(ui.g_selectGameLayer)
end)
local gameFu,gameLu=ui.gameFu,ui.gameLu
ui.gameFu=function() end;ui.gameLu=function() end
check('native eight card callback',function()
 ui.getResFromServer(FIXTURE.fu);assert(#ui.g_prize[1]==8)
 local p=ui.g_prize[1][ui.g_getPrize];assert(p.get_flag and p.object_type==5)
 local sprite=ms.d_data.getCertainSmallSprite(p.object_type,p.attach_type);assert(sprite)
end)
check('native dice callback',function()
 ui.getResFromServer(FIXTURE.lu);assert(ui.g_prize[2].total_money==160000)
 for _,point in ipairs(ui.g_prize[2].form_type) do assert(point==6) end
end)
ui.gameFu=gameFu;ui.gameLu=gameLu
local nativeBig=ms.d_data.getCertainBigSprite
local nativeSmall=ms.d_data.getSmallSkillSprite;local atlasCalls={}
local nativePanel=ms.d_commonLayerUI.showPrizeResLayer;local panels={}
ms.d_commonLayerUI.showPrizeResLayer=function(parent,list,...)
 panels[#panels+1]=list
 return nativePanel(parent,list,...)
end
ms.d_data.getSmallSkillSprite=function(tid,...)
 atlasCalls[#atlasCalls+1]=tid;return nativeSmall(tid,...)
end
if not VISIT_PREVIEW then
for i,row in ipairs(FIXTURE.scratch) do
 check('native scratch and claim spell '..row.draw.visit_list[3].prize_info.attach_type,function()
  root:removeAllChildrenWithCleanup(true)
  ui.getResFromServer(FIXTURE.query)
  atlasCalls={}
  local tid=row.draw.visit_list[3].prize_info.attach_type
  local missing=type(nativeBig(6,tid))~='userdata'
  ui.getResFromServer(row.draw)
  if missing then
   assert(#atlasCalls==2 and atlasCalls[1]==tid and atlasCalls[2]==tid,'wrong spell atlas icon')
  end
  local info=row.draw.visit_list[3].prize_info
  assert(ui.g_prize[3].object_type==6 and ui.g_prize[3].type==info.attach_type)
  assert(ui.g_shouPrizeMenuItem,'missing spell icon menu')
  assert(ms.d_data.getCertainBigSprite==nativeBig,'renderer was not restored')
  assert(ui.g_wipeLayer and ui.g_itemMask)
  local prefix={first_send=true,attach_count=128,attach_list={}}
  for j=1,128 do
   local item={};for k,v in pairs(FIXTURE.inventory_prefix.attach_list[j]) do item[k]=v end
   prefix.attach_list[j]=item
  end
  ms.d_event_mgr.getNextPackageType=function() return 1035 end
  ms.d_packageUI.getDateFormServer(prefix)
  ms.d_event_mgr.getNextPackageType=function() return 2998 end
  ms.d_packageUI.getDateFormServer(row.inventory)
  local book=ms.d_packageUI.g_packageItemsInfo[129]
  assert(book and book.attach_type==6 and book.type_id==tid and book.protogenic==0,'book missing from inventory')
  assert(ms.d_packageUI.g_reorgItemsInfo[6][1].id==book.id,'book missing from spell category')
  local count=#panels
  assert(count==i-1,'draw displayed a reward panel')
  ui.getResFromServer(row.claim)
  assert(ui.g_visitList[3].has_visit)
  assert(#panels==count+1,'missing reward panel')
  assert(panels[#panels][1].object_type==6 and panels[#panels][1].attach_type==tid
   and panels[#panels][1].attach_count==1,'wrong reward panel book/count')
  ui.getResFromServer(row.claim)
  assert(#panels==count+1,'duplicate claim opened another panel')
 end)
end
end
local function restore()
 root:removeAllChildrenWithCleanup(true)
 if root:getParent() then root:removeFromParentAndCleanup(true) end
 root:release()
 for i=#saved,1,-1 do local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end;for k,v in pairs(row.old) do row.t[k]=v end end
 ms.MS_report_error=report
end
if VISIT_PREVIEW then
 root:removeAllChildrenWithCleanup(true)
 ui.getResFromServer(FIXTURE.query)
 for _,row in ipairs(FIXTURE.scratch) do
  if row.draw.visit_list[3].prize_info.attach_type==216 then
   ui.getResFromServer(row.draw);ui.getResFromServer(row.claim);break
  end
 end
 CCDirector:sharedDirector():getRunningScene():addChild(root,9999)
 visitPreview={restore=restore,root=root}
 return 'preview ready'
end
restore()
local out={};for _,v in ipairs(checks) do out[#out+1]=v.name..':'..tostring(v.ok)..':'..v.error end
return table.concat(out,'\n')
