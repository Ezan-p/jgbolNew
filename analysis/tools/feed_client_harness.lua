-- All packets captured; original Cocos widgets live on a detached layer.
local ms=assert(package.loaded.ms);local ui=assert(ms.d_eatBunUI)
local saved,checks,errors,sent,delays={},{},{},{},{}
local function preserve(t)
 local old={};for k,v in pairs(t) do old[k]=v end;saved[#saved+1]={t=t,old=old}
end
for _,name in ipairs({'d_eatBunUI','d_activityUI','d_u','d_info','d_time','d_mainUI'}) do preserve(ms[name]) end
if ui._localFeedRestore then ui._localFeedRestore() end
ui.g_self={press_count=0,time_left=10,last_server_time=0,in_time_act=0,enable_act=0,feed_list={}}
ms.d_mainUI.g_playerInfo={}
ms.d_activityUI.activityStatus={}
-- INSTALL_PATCH
local report=ms.MS_report_error;ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
local root=CCLayer:create();root:retain()
local clock,server=100,FIXTURE.now
ms.d_time.getTime=function() return clock end
ms.d_time.getShowTime=function() return server end
ms.d_u.delay=function(node,seconds,callback) delays[#delays+1]={seconds=seconds,callback=callback} end
ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
ms.d_activityUI.returnBack=function() root:removeAllChildrenWithCleanup(true) end
ms.d_info.show=function() end
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,ok=ok and #errors==0,error=(err or '')..table.concat(errors,'\n')}
end
local function scoreSends()
 local n=0;for _,v in ipairs(sent) do if v.mid==1040 and v.data.feed_count>0 then n=n+1 end end;return n
end
check('entry queries only',function()
 ui.show(root)
 for _,v in ipairs(delays) do if v.seconds==0 then v.callback() end end
 assert(#sent==1 and sent[1].mid==1040 and sent[1].data.feed_count==0)
 ui.callbackFeedRet(FIXTURE.entry)
 assert(ui.g_self.in_time_act==1 and ui.g_self.enable_act==1)
 assert(ui.g_self.feed_list[1]==1 and not ui.g_self.got1:isVisible())
end)
check('start waits for first barrel click',function()
 ui.pressBegin();assert(ui.g_self._feedPhase=='ready')
 assert(ui.g_self.press_count==0 and ui.g_self.time_left==10 and scoreSends()==0)
 clock=150;ui.count_down();ui.sendResult()
 assert(ui.g_self.time_left==10 and scoreSends()==0)
end)
local stale
check('first click starts original ten seconds',function()
 ui.pressEatBun()
 assert(ui.g_self.press_count==1 and ui.g_self.time_begin_sec==150 and ui.g_self.time_left==10)
 stale=delays[#delays].callback
end)
check('continuous clicks update native count and reward tier',function()
 for i=2,30 do clock=150+i/4;ui.pressEatBun() end
 assert(ui.g_self.press_count==30 and scoreSends()==0)
 assert(string.find(ui.g_self._feedTierLabel:getString(),'40体力'))
 ui.sendResult();assert(scoreSends()==0)
end)
check('deadline rejects late click and waits original two seconds',function()
 clock=160;ui.pressEatBun()
 assert(ui.g_self.press_count==30 and ui.g_self.time_left==0 and ui.g_self._feedPhase=='finished')
 assert(delays[#delays].seconds==2 and scoreSends()==0)
 delays[#delays].callback()
 assert(scoreSends()==1 and sent[#sent].data.feed_count==30)
 ui.sendResult();ui.pressEatBun();assert(scoreSends()==1 and ui.g_self.press_count==30)
end)
check('original settlement callback shows actual reward',function()
 ui.callbackFeedRet(FIXTURE.result)
 assert(ui.g_self._feedPhase=='idle' and ui.g_self.self_feed_strength==40)
 assert(ui.g_self.beginPage_layer:isVisible())
 ui.checkCanFeedNow(FIXTURE.result.feed_time,server)
 assert(ui.g_self.got1:isVisible() and ui.g_self.enable_act==0)
 ui.pressBegin();assert(ui.g_self._feedPhase=='idle')
end)
check('second period starts a fresh run without stale callbacks',function()
 server=FIXTURE.now+21600;ui.callbackFeedRet(FIXTURE.dinner)
 assert(ui.g_self.in_time_act==2 and ui.g_self.enable_act==2)
 ui.pressBegin();assert(ui.g_self.press_count==0 and ui.g_self.time_left==10)
 stale();assert(scoreSends()==1 and ui.g_self._feedPhase=='ready')
 clock=200;ui.pressEatBun()
 for i=2,10 do clock=200+i/4;ui.pressEatBun() end
 clock=210;ui.count_down();delays[#delays].callback()
 assert(scoreSends()==2 and sent[#sent].data.feed_count==10)
 ui.callbackFeedRet(FIXTURE.dinner_result)
 assert(ui.g_self.self_feed_count==30 and ui.g_self.self_feed_strength==40)
end)
check('next day clears claimed indicators',function()
 server=FIXTURE.now+86400;ui.callbackFeedRet(FIXTURE.next_day)
 assert(not ui.g_self.got1:isVisible() and not ui.g_self.got2:isVisible())
 ui.pressBegin();assert(ui.g_self._feedPhase=='ready')
end)
check('close cancels delayed score submission',function()
 clock=300;for i=1,201 do ui.pressEatBun() end
 assert(ui.g_self.press_count==200 and string.find(ui.g_self._feedTierLabel:getString(),'计分上限'))
 clock=310;ui.count_down()
 local finish=delays[#delays].callback
 ui.pressClose();finish();assert(scoreSends()==2)
 ui.show(root);ui.callbackFeedRet(FIXTURE.next_day);finish()
 assert(ui.g_self._feedPhase=='idle' and scoreSends()==2)
end)
check('closed hours cannot start',function()
 server=FIXTURE.now+86400+10800
 ui.checkCanFeedNow(FIXTURE.next_day.feed_time,server);ui.pressBegin()
 assert(ui.g_self.in_time_act==0 and ui.g_self._feedPhase=='idle' and scoreSends()==2)
end)
check('patch restore',function() ui._localFeedRestore();assert(ui._localFeedRestore==nil) end)
root:removeAllChildrenWithCleanup(true);root:release()
for i=#saved,1,-1 do local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end;for k,v in pairs(row.old) do row.t[k]=v end end
ms.MS_report_error=report
local out={};for _,v in ipairs(checks) do out[#out+1]=v.name..':'..tostring(v.ok)..':'..v.error end
return table.concat(out,'\n')
