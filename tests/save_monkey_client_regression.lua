local checks,sent,notices={},{},{}
local now=100
local function check(name,fn) fn();checks[#checks+1]=name end
local function noop() end
local ui={g_self={data={}},g_newbieLoginConfig={}}
for _,name in ipairs({'sendMsgEnterGame','sendMsgUseItm','sendMsgUseEyeItm','sendMsgQueryActivityPoint',
 'sendMsgQueryPieceShop','sendMsgBuyItem','sendMsgTakeScoreItem','sendMsgTakePointItem','getRewardLoginConfig'}) do ui[name]=noop end
ui.canJoin=function() return false end
ui.checkCanUseBomb=function() return true end
ui.getItemCount=function() return 999 end
ui.setData=function(d) for k,v in pairs(d) do ui.g_self.data[k]=v end end
ui.onGetResult=function(d) if d.id==1 or d.id==2 then ui.setData(d) end;return 'native' end
local originalResult=ui.onGetResult
local originalSend=function(mid,req) sent[#sent+1]={mid=mid,req=req} end
local oldTimes={{start_time=1,end_time=2}}
local ms={d_saveMonkeyUI=ui,d_activityUI={getQiwenStatus=noop},d_data={g_new_config={[308]={[66]=oldTimes}}},
 d_common_def={client_config_type={activity_time=308},activity_type={save_monkey_activity=66}},
 d_time={getTime=function() return now end},d_info={show=function(v) notices[#notices+1]=v end},
 d_u={main_server_send_msg=originalSend},d_packageUI={g_packageItemsInfo={
 {attach_type=5,type_id=1350,count=3,is_lock=false},{attach_type=5,type_id=1350,count=4,is_lock=0},
 {attach_type=5,type_id=1350,count=90,is_lock=true},{attach_type=5,type_id=1350,count=99,owner_id=2}}}}
package.loaded.ms=ms
local function serialize(v)
 if type(v)=='table' then local parts={};for k,x in pairs(v) do parts[#parts+1]='['..serialize(k)..']='..serialize(x) end;return '{'..table.concat(parts,',')..'}' end
 if type(v)=='string' then return string.format('%q',v) end
 return tostring(v)
end
table.tostring=serialize;table.loadstring=function(s) return assert(loadstring('return '..s))() end
-- INSTALL_PATCH
local installed=ui.onGetResult
-- INSTALL_AGAIN
check('idempotent installation and original-entry visibility',function() assert(installed==ui.onGetResult and ui.canJoin()) end)
check('native operation ids and transposed coordinates retained',function()
 ui.sendMsgEnterGame();assert(sent[#sent].mid==1346 and sent[#sent].req.id==1)
 assert(ui.onGetResult(FIXTURE)=='native')
 ui.sendMsgUseItm(2,5,1350)
 local r=sent[#sent].req;local d=table.loadstring(r.data)
 assert(r.id==2 and d.pos_info.x==2 and d.pos_info.y==5 and d.local_token==FIXTURE.local_token)
 assert(ui.g_self.data.grid_conf==FIXTURE.grid_conf)
end)
check('all remaining native send callbacks carry server token',function()
 for _,v in ipairs({{'sendMsgUseEyeItm',2},{'sendMsgBuyItem',5},{'sendMsgTakeScoreItem',3},{'sendMsgTakePointItem',7}}) do
  ui[v[1]](1,2);local r=sent[#sent].req;assert(r.id==v[2] and table.loadstring(r.data).local_token==FIXTURE.local_token)
 end
 ui.sendMsgQueryPieceShop();assert(sent[#sent].req.id==4)
 ui.sendMsgQueryActivityPoint();assert(sent[#sent].req.id==6)
end)
check('1263 assist preview and inline exchange closure',function()
 assert(#ui.g_newbieLoginConfig==4 and #ui.g_newbieLoginConfig[1].rewardCount==3)
 assert(ms.d_data.g_exchange_table[1].consume[1]==300)
 ui.getRewardLoginConfig()
 ms.d_u.main_server_send_msg(1346,{id=9,data=table.tostring({index=1,count=2})})
 assert(table.loadstring(sent[#sent].req.data).local_token==FIXTURE.local_token)
end)
check('locked/owned stacks excluded and native granite check strengthened',function()
 assert(ui.getItemCount(1350)==7)
 assert(not ui.checkCanUseBomb({{{stone_type=3}}},1,1,1350))
 assert(ui.checkCanUseBomb({{{stone_type=1}}},1,1,1350))
end)
check('shop/claim replies synchronize main counters',function()
 ui.onGetResult({id=5,piece=3,local_token='new',local_reset_time=FIXTURE.local_reset_time})
 assert(ui.g_self.data.piece==3)
 ui.sendMsgBuyItem(2,1);assert(table.loadstring(sent[#sent].req.data).local_token=='new')
end)
check('expiry queries before mutation and leaves inline exchange unsent',function()
 now=FIXTURE.local_reset_time;ui.sendMsgUseEyeItm();assert(sent[#sent].req.id==1)
 local count=#sent;ms.d_u.main_server_send_msg(1346,{id=9,data=table.tostring({index=1,count=1})});assert(#sent==count)
 assert(#notices==2)
end)
check('other traffic unaffected and server disable honored',function()
 ms.d_u.main_server_send_msg(1205,{flag=0});assert(sent[#sent].mid==1205)
 ms.d_activityUI.getQiwenStatus({local_save_monkey={local_enabled=false,start_time=1,end_time=2}})
 assert(not ui.canJoin())
end)
check('restores sends, callbacks, config and original table',function()
 ui._localSaveMonkeyRestore();assert(ui.onGetResult==originalResult)
 assert(ms.d_u.main_server_send_msg==originalSend and ms.d_data.g_new_config[308][66]==oldTimes)
 assert(not ui._localSaveMonkeyRestore)
end)
return checks
