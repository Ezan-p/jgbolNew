-- Original Cocos widgets, isolated local upvalues; capture sends, restore all state.
local ms=assert(package.loaded.ms);local ui=assert(ms.d_soulHuntUI)
local saved,checks,errors,sent={},{},{},{}
local function preserve(t)
 local old={};for k,v in pairs(t) do old[k]=v end;saved[#saved+1]={t=t,old=old}
end
local function up(fn,key)
 for i=1,30 do local k,v=debug.getupvalue(fn,i);if k==key then return v end;if not k then break end end
 error('missing upvalue '..key)
end
local state=up(ui.onGetResponse,'g_self');local view=up(ui.onGetResponse,'g_soulHuntUI')
for _,t in ipairs({ui,state,view,ms.d_activityUI,ms.d_u,ms.d_info,ms.d_commonLayerUI,ms.d_data,ms.d_file,ms.d_time,ms.d_mainUI}) do preserve(t) end
for k in pairs(state) do state[k]=nil end;state.Below=-20;state.Speed=500
for k in pairs(view) do view[k]=nil end
local report=ms.MS_report_error;ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
local root=CCLayer:create();root:retain()
ms.d_activityUI.g_self={main_layer=root};ms.d_activityUI.show=function() end
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(ms.d_mainUI.g_playerInfo);ms.d_mainUI.g_playerInfo.level=60
ms.d_time.getTime=function() return FIXTURE.now end
ms.d_file.set=function() end;ms.d_file.get=function() return true end
ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
ms.d_info.show=function() end
local deferred={}
ms.d_u.delay=function(node,seconds,callback) deferred[#deferred+1]=callback end
ms.d_commonLayerUI.showPrizeResLayer=function(parent,list,callback)
 assert(type(list)=='table' and #list>0,'missing prizes');if callback then callback() end
end
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,ok=ok and #errors==0,error=(err or '')..table.concat(errors,'\n')}
end
local function response(data) ui.onGetResponse(ms.d_c.table_copy(data)) end
local function last(flag) local v=sent[#sent];assert(v and v.mid==1226 and v.data.flag==flag,'bad native request');return v.data end
check('activity status and native entry',function()
 ui.updateActivityStatus(FIXTURE.status);assert(ui.canEnter());ui.enterActivity();last(1)
end)
check('entry renders original map',function()
 response(FIXTURE.entry);assert(view.main_layer);assert(state.role_hunt_data.left_energy==400)
 assert(state.BallPrice[1].need_energy==20 and state.BallPrice[3].need_energy==60)
 assert(state.SoulValue[5].soul_value==200)
end)
check('all three native balls and aim',function()
 for i=1,3 do state.ball=i;state.degree=90;ui.showBall();ui.showCannon();ui.pressShoot();local r=last(2);assert(r.count==i and r.index==90) end
 assert(ui.getDegree(state.cannon_x,state.cannon_y+200)==90)
end)
check('native trajectory construction and captured souls',function()
 state.ball=1;state.degree=90;response(FIXTURE.shot)
 assert(state.role_hunt_data.left_energy==380)
 for _,segment in ipairs(FIXTURE.shot.move_result.move_path) do
  for _,soul in pairs(segment.soul_list) do local index=assert(ui.getSoulIndex(soul));ui.soulAbsorb(index) end
 end
 assert(state.role_hunt_data.left_soul_count==100066)
end)
check('energy exchange dialog and callback',function()
 ui.pressBuyEnergy();ui.sendBuyEnergyRequest(10);assert(last(3).count==10);response(FIXTURE.exchange)
 assert(state.role_hunt_data.left_energy==390)
end)
check('map refresh callback',function() ui.sendSoulFlushRequest();last(4);response(FIXTURE.refresh);assert(state.role_hunt_data.left_flush_times==2) end)
check('original six item shop',function() ui.pressShop();last(5);response(FIXTURE.shop);assert(#state.store_data.item_list==6) end)
for i=1,6 do check('purchase dialog '..i,function() ui.pressBuyItem(i) end) end
check('purchase callback and remaining stock',function()
 ui.sendBuyItemRequest(1,2);local r=last(6);assert(r.index==1 and r.count==2);response(FIXTURE.buy)
 assert(state.store_data.item_list[1].buy_times==1)
end)
check('store refresh callback',function() ui.sendStoreFlushRequest();last(7);response(FIXTURE.store_refresh) end)
for _,flag in ipairs({8,9,10,12,13}) do check('rank response '..flag,function() response(FIXTURE['rank'..flag]) end) end
for _,page in ipairs({4,5}) do check('original reward preview '..page,function() ui.showRankDetail(page) end) end
check('weekly winner and reward callback',function() response(FIXTURE.winner);ui.sendTakeRewardRequest();last(11);response(FIXTURE.prize);assert(state.rank_data.my_data.had_got_prize) end)
check('original tutorial',function() ui.showSoulHuntGuide() end)
root:removeAllChildrenWithCleanup(true);root:release()
for i=#saved,1,-1 do local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end;for k,v in pairs(row.old) do row.t[k]=v end end
ms.MS_report_error=report
hunt_fixture_results=checks
local out={};for _,v in ipairs(checks) do out[#out+1]=v.name..':'..tostring(v.ok)..':'..v.error end
return table.concat(out,'\n')
