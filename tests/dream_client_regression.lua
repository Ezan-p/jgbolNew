-- Lua 5.1 adapter contract fixture, with the native shared upvalue topology.
-- Cocos nodes are stubs; this does not claim device rendering coverage.
local checks,sent,notices,styles={},{},{},{}
local now=1000
local function copy(t)
 if type(t)~='table' then return t end
 local out={};for k,v in pairs(t) do out[k]=copy(v) end;return out
end
local function node()
 return {removeChildByTag=function() end,addChild=function() end}
end
local ms={d_u={},d_time={},d_info={},d_data={},d_followUI={g_friendList={{id=999}}}}
package.loaded.ms=ms
ms.d_time.getTime=function() return now end
ms.d_info.show=function(v) notices[#notices+1]=v end
ms.d_u.createByStyles=function(s) styles[#styles+1]=s;return node() end
ms.d_data.getCertainInfo=function() return {name='造化神石'} end
ms.d_data.getDreamConfig=function() ms.d_data.g_dreamTable='baseline' end
local ui={};ms.d_dreamUI=ui
local g_self,g_dreamUI={}, {main_layer=node()}
local function gethz(key) return key end
local function sendRequest(op,data) sent[#sent+1]={op=op,data=copy(data or {})} end
ui.enter=function() return sendRequest(1) end
ui.puzzleSubmit=function() return sendRequest(2,{answer={1,2,3,4,5,6,7,8,9}}) end
ui.blessSubmit=function() return sendRequest(3,{des_list={100},index=1}) end
ui.take=function() return sendRequest(4) end
ui.updateActivityStatus=function(d) ui.activity=d end
ui.show=function() ms.d_data.getDreamConfig();ui.g_config=ms.d_data.g_dreamTable end
ui.showEntrance=function() return g_dreamUI.main_layer end
ui.showBless=function()
 g_dreamUI.friends=g_dreamUI.friends or ms.d_followUI.g_friendList
 ui.shownFriends=g_dreamUI.friends
end
ui.showFinalReward=function(eligible)
 ui.finalEligible=eligible;ui.finalText=gethz('dream20')
 ui.unrelatedText=gethz('dream3')
end
ui.onGetResponse=function(data)
 if data.flag==1 then g_self.dream_data=data.dream_data;g_self.plus_data=data.plus_data;ui.show()
 elseif data.flag==2 then g_self.dream_data.status=data.dream_data.status
 elseif data.flag==3 then g_dreamUI.friends=nil;g_dreamUI.BF=nil
 elseif data.flag==4 then g_self.dream_data.take_charge=data.dream_data.take_charge end
end
local originals={};for k,v in pairs(ui) do originals[k]=v end
local originalConfig=ms.d_data.getDreamConfig
-- INSTALL_PATCH
local function response(op,changes)
 local d={flag=op,result=1,dream_data={cur_dream=1,status=1,take_charge=false,can_take=false,
  local_token='token'..op,local_refresh_time=2000},
  plus_data={min_charge=30,charge_prize={{object_type=5,attach_type=1369,attach_count=3,attach_level=1}}},
  local_friends={{id=100,name='NPC甲',level=60},{id=101,name='NPC乙',level=55}},
  local_rewards={{dream_prizes={{attach_type=1022,attach_count=5,attach_level=1}}}},
  local_activity={begin_time=999,end_time=2000,min_level=18,can_join=true}}
 for k,v in pairs(changes or {}) do d.dream_data[k]=v end
 ui.onGetResponse(d);return d
end
local function check(name,fn) fn();checks[#checks+1]=name end
check('entry remains native and reward tables replace baseline before show',function()
 ui.enter();assert(sent[#sent].op==1 and next(sent[#sent].data)==nil)
 local d=response(1)
 assert(ui.g_config==d.local_rewards and ui.activity.min_level==18)
 assert(g_self.plus_data==d.plus_data)
end)
check('puzzle bless claim share protected request context',function()
 ui.puzzleSubmit();assert(sent[#sent].op==2 and sent[#sent].data.local_token=='token1')
 assert(#sent[#sent].data.answer==9)
 response(2,{status=2});ui.blessSubmit()
 assert(sent[#sent].op==3 and sent[#sent].data.local_token=='token2')
 response(3,{cur_dream=7,can_take=true});ui.take()
 assert(sent[#sent].op==4 and sent[#sent].data.local_token=='token3')
end)
check('full state updates native partial caches including final eligibility',function()
 assert(g_self.dream_data.cur_dream==7 and g_self.dream_data.can_take)
 ui.showFinalReward(false)
 assert(ui.finalEligible and ui.finalText=='造化神石×3' and ui.unrelatedText=='dream3')
end)
check('NPC list stays scoped to dream and refreshes after sending',function()
 ui.showBless();assert(ui.shownFriends[1].player.id==100 and not ui.shownFriends[1].isChosen)
 assert(ms.d_followUI.g_friendList[1].id==999)
 response(3);ui.showBless();assert(#ui.shownFriends==2)
end)
check('unqualified final page shows recharge and claimed page cannot reopen claim',function()
 response(1,{cur_dream=7});ui.showFinalReward(true);assert(not ui.finalEligible)
 response(4,{cur_dream=7,take_charge=true});ui.showFinalReward()
 assert(notices[#notices]=='本期仙梦居祝福已领取')
end)
check('expired popup never sends stale mutation',function()
 now=2000
 for _,fn in ipairs({ui.puzzleSubmit,ui.blessSubmit,ui.take}) do
  local n=#sent;fn();assert(#sent==n+1 and sent[#sent].op==1)
 end
 now=1000
end)
check('entry labels local NPC and remaining period',function()
 ui.showEntrance();assert(styles[#styles].string:find('离线NPC',1,true))
end)
check('repeated injection is idempotent',function()
 local before=ui.onGetResponse
 -- INSTALL_AGAIN
 assert(ui.onGetResponse==before)
end)
check('restore removes wrappers and shared token changes',function()
 ui._localDreamRestore()
 for k,v in pairs(originals) do assert(ui[k]==v,k) end
 assert(ms.d_data.getDreamConfig==originalConfig and ui._localDreamRestore==nil)
 ui.puzzleSubmit();assert(sent[#sent].data.local_token==nil)
 originals.showFinalReward(false);assert(ui.finalText=='dream20')
end)
return checks
