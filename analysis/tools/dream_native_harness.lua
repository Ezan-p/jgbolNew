-- Detached Cocos layers and captured network sends; restore all live references.
local ms=assert(package.loaded.ms);local ui=assert(ms.d_dreamUI)
local checks,errors,sent,menus,saved={},{},{},{},{}
local function preserve(t)
 local old={};for k,v in pairs(t) do old[k]=v end;saved[#saved+1]={t=t,old=old}
end
local function up(fn,key,value,write)
 for i=1,100 do
  local name,current=debug.getupvalue(fn,i);if not name then break end
  if name==key then if write then debug.setupvalue(fn,i,value) end;return current end
 end
end
assert(not ui._localDreamRestore,'Run fixture before installing a separate live dream adapter')
local nativeResponse,nativeBless=ui.onGetResponse,ui.showBless
local liveSelf=up(nativeResponse,'g_self');local liveView=up(nativeBless,'g_dreamUI')
local responseSelf={};local view={skipAnim=true}
for _,t in ipairs({ui,ms.d_u,ms.d_info,ms.d_data,ms.d_time,ms.d_activityUI,ms.d_commonLayerUI}) do preserve(t) end
up(nativeResponse,'g_self',responseSelf,true);up(nativeBless,'g_dreamUI',view,true)
local parent=CCScene:create();parent:retain()
local oldActSelf=ms.d_activityUI.g_self
ms.d_activityUI.g_self=ms.d_c.table_copy(oldActSelf);ms.d_activityUI.g_self.main_layer=parent
ms.d_activityUI.show=function() end
local report=ms.MS_report_error;ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
ms.d_time.getTime=function() return FIXTURE.now end
ms.d_info.show=function() end
ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=ms.d_c.table_copy(data)} end
local menu=ms.d_u.createMenu
ms.d_u.createMenu=function(styles,...) menus[#menus+1]=styles;return menu(styles,...) end
local prize
ms.d_commonLayerUI.showPrizeResLayer=function(layer,rewards,callback) prize=rewards end
local function cleanup()
 if ui._localDreamRestore then ui._localDreamRestore() end
 parent:removeAllChildrenWithCleanup(true);parent:release()
 up(nativeResponse,'g_self',liveSelf,true);up(nativeBless,'g_dreamUI',liveView,true)
 for i=#saved,1,-1 do local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end;for k,v in pairs(row.old) do row.t[k]=v end end
 ms.MS_report_error=report
end
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,ok=ok and #errors==0,error=(err or '')..table.concat(errors,'\n')}
end
local ok,err=xpcall(function()
 -- INSTALL_PATCH
 assert(ui._localDreamRestore,'patch did not install')
 check('native 1325 entry and original main layer',function()
  ui.enter();assert(sent[#sent].mid==1325 and sent[#sent].data.id==1)
  ui.onGetResponse(FIXTURE.stages[1].entry)
  assert(view.main_layer and ui.canJoin() and ui.g_min_level==18)
  assert(ui.g_config[2].dream_prizes[1].attach_level==6)
 end)
 for stage=1,6 do
  check('native nine-tile swaps stage '..stage,function()
   ui.onGetResponse(FIXTURE.stages[stage].entry)
   ui.showPreview();ui.showGameStart();ui.showPuzzle()
   assert(#view.pics==9)
   local press=assert(up(ui.showPuzzle,'pressBlank'))
   for i=1,9 do
    if view.pics[i]~=i then
     local j;for k=i+1,9 do if view.pics[k]==i then j=k;break end end
     assert(j);press(i);press(j)
    end
   end
   local request=sent[#sent]
   assert(request.mid==1325 and request.data.id==2)
   local data=assert(loadstring('return '..request.data.data))()
   assert(data.local_token==FIXTURE.stages[stage].entry.dream_data.local_token)
   for i=1,9 do assert(data.answer[i]==i) end
   ui.onGetResponse(FIXTURE.stages[stage].solved)
   ui.showBless();ui.showFriendChooseLayer()
   assert(#view.friends==6)
   view.BF={view.friends[1].player,view.friends[2].player}
   ui.showBless(true)
   local send
   for _,styles in ipairs(menus) do for _,s in ipairs(styles) do
    if s.npic=='v2/dreamUI/btn21.png' then send=s.call_back end
   end end
   assert(send);send()
   data=assert(loadstring('return '..sent[#sent].data.data))()
   assert(sent[#sent].data.id==3 and #data.des_list==2)
   assert(data.local_token==FIXTURE.stages[stage].solved.dream_data.local_token)
   ui.onGetResponse(FIXTURE.stages[stage].blessed)
   assert(responseSelf.dream_data.cur_dream==stage+1)
  end)
 end
 check('native gift preview uses all six 1263 rows',function()
  ui.showGiftPreview();assert(ui.g_config[6].dream_prizes[1].attach_type==1152)
 end)
 check('native final page displays configured prize and eligibility',function()
  ui.onGetResponse(FIXTURE.eligible)
  local render=ms.d_u.createByStyles;local seen=false
  ms.d_u.createByStyles=function(style,...)
   if style.string=='造化神石×3' then seen=true end
   return render(style,...)
  end
  local success,failure=pcall(ui.fallAsleep)
  ms.d_u.createByStyles=render
  assert(success,failure);assert(seen,'configured final reward text missing')
 end)
 check('native claimed final page and state refresh',function()
  ui.onGetResponse(FIXTURE.claimed);assert(responseSelf.dream_data.take_charge)
  ui.showFinalReward();assert(prize and #prize==1 and prize[1].attach_type==1369)
 end)
end,debug.traceback)
if not ok then checks[#checks+1]={name='fixture execution',ok=false,error=err} end
cleanup()
local out={};for _,c in ipairs(checks) do out[#out+1]=c.name..':'..tostring(c.ok)..':'..c.error end
return table.concat(out,'\n')
