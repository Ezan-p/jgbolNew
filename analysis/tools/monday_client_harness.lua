local ms=assert(package.loaded.ms);local ui=assert(ms.d_mondayUI)
local saved={};local checks={};local errors={};local sent={}
local function preserve(t)
 local old={};for k,v in pairs(t) do old[k]=v end;saved[#saved+1]={t=t,old=old}
end
for _,name in ipairs({'d_mondayUI','d_activityUI','d_u','d_info','d_commonLayerUI','d_time'}) do preserve(ms[name]) end
local report=ms.MS_report_error;ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
local root=CCLayer:create();root:retain()
ui.g_self={Max=4,tags={Count=1,Time=2,Status=3}};ui.g_mondayUI={}
ms.d_activityUI.g_self={main_layer=root};ms.d_activityUI.g_isCurrentSenceRun=true
ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
ms.d_u.delay=function() end
ms.d_time.getRestTime=function() return '12:00:00' end
ms.d_time.isCrossDay=function(t) return t==0 end
ms.d_info.show=function() end
ms.d_commonLayerUI.showPrizeResLayer=function(parent,list,callback)
 assert(#list==1 and list[1].attach_count>0);if callback then callback() end
end
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,passed=ok and #errors==0,error=(err or '')..table.concat(errors,'\n')}
end
check('entry32 original 1219 request',function()
 assert(ms.d_activityUI.activityID.monday==32);ms.d_activityUI.requestMondayStatus()
 local q=sent[#sent];assert(q.mid==1219 and q.data.flag==1 and q.data.op_type==0 and q.data.level==0)
end)
check('closed day four preview slots',function()
 ui.onGetActivityStatus(FIXTURE.closed)
 assert(ui.g_mondayUI.week_day==7 and #ui.g_mondayUI.item_list==4 and ui.g_mondayUI.changeBtns)
 assert(not ui.g_mondayUI.GetBtn:isEnabled())
end)
check('original refresh request and callback',function()
 ui.requestChangeItem(1);local q=sent[#sent];assert(q.mid==1243 and q.data.index==1)
 ui.onGetExchangeResult(FIXTURE.refresh)
 assert(ui.g_mondayUI.random_time[1]==FIXTURE.refresh.attach_data.random_time)
 assert(not ui.g_mondayUI.changeBtns[2]:isEnabled())
end)
check('completed task can claim jade',function()
 ui.onGetActivityStatus(FIXTURE.task);assert(ui.g_mondayUI.GetBtn:isEnabled())
 ui.requestGetPrize();local q=sent[#sent];assert(q.mid==1219 and q.data.flag==2)
 ui.onGetActivityStatus(FIXTURE.claim)
 assert(ui.g_mondayUI.own==10 and not ui.g_mondayUI.GetBtn:isEnabled())
end)
check('monday four purchase slots',function()
 ui.onGetActivityStatus(FIXTURE.open)
 assert(ui.g_mondayUI.week_day==1 and ui.g_mondayUI.BuyBtns and not ui.g_mondayUI.changeBtns)
 assert(ui.g_mondayUI.GetBtn:isEnabled())
end)
check('opening gift and balance',function()
 ui.onGetActivityStatus(FIXTURE.opening_claim);assert(ui.g_mondayUI.own==30)
 assert(not ui.g_mondayUI.GetBtn:isEnabled())
end)
check('original exchange request and reward callback',function()
 ui.requestBuyItem(1);local q=sent[#sent];assert(q.mid==1219 and q.data.flag==3 and q.data.level==1)
 ui.onGetActivityStatus(FIXTURE.buy);assert(ui.g_mondayUI.own==20)
 assert(ui.g_mondayUI.BuyBtns[2]:isEnabled() and not ui.g_mondayUI.BuyBtns[8]:isEnabled())
end)
check('closure switches back to preview and resets balance',function()
 ui.onGetActivityStatus(FIXTURE.next)
 assert(ui.g_mondayUI.week_day==2 and ui.g_mondayUI.own==0 and ui.g_mondayUI.changeBtns)
end)
root:removeAllChildrenWithCleanup(true);root:release()
for i=#saved,1,-1 do local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end;for k,v in pairs(row.old) do row.t[k]=v end end
ms.MS_report_error=report
return table.tostring(checks)
