-- Run with the generated adapter source passed as vararg in a Lua 5.1/LuaJIT VM.
-- All UI/network dependencies are fakes; this never sends a game request.
local source = ...
local reports = {}
local function check(condition, name)
    assert(condition, name)
    reports[#reports+1] = name
end
local sent, hints, originalCalls = {}, {}, {}
local s = {g_banshu=true, g_allowSummon={false,false,false}, g_summonerCount={0,0,0},
           g_goldSpriteTable={}, g_isInSummonPage=true}
local ms = {d_data={getItemCountByType=function() return 42 end},d_mainUI={g_playerInfo={gold_coin=1000}},
    d_u={main_server_send_msg=function(id,data) sent[#sent+1]={id=id,data=data} end},
    d_info={show=function(text) hints[#hints+1]=text end},
    d_msg_def={gscl_msg_id={msg_cortege_ramdom_get=1042}},
    d_common_def={cortege_pick_type={pay=3}}}
local prices = {17,123,456}
local parent={children={}}
function parent:getChildByTag(tag) return self.children[tag] end
function parent:addChild(label,z,tag) self.children[tag]=label end
function parent:removeChildByTag(tag) self.children[tag]=nil end
local function label()
    return {setString=function(self,text) self.text=text end, setPosition=function() end,
        getPositionX=function() return 100 end, getPositionY=function() return 100 end,
        getContentSize=function() return {height=40} end, getParent=function() return parent end}
end
for i=1,3 do s.g_goldSpriteTable[i]={gold=label(),sprite=label()} end
s.startSummon=function(grade) originalCalls[#originalCalls+1]=grade end
s.updateSummonLabels=function() end
s.sortNews=function(a,b) return a.time>b.time end
s.g_summonNews={}
s.updateSummonNews=function(data)
    for i,row in ipairs(data.lottery_list) do s.g_summonNews[i]=row end
    table.sort(s.g_summonNews,s.sortNews)
end
local oldItemCount=ms.d_data.getItemCountByType
local oldNews,oldSort=s.updateSummonNews,s.sortNews
local oldStart,oldLabels=s.startSummon,s.updateSummonLabels
local env=setmetatable({package={loaded={['ui.summonUI']=s,ms=ms}},
    CCLabelTTF={create=function() return label() end},tolua={cast=function(node) return node end}},{__index=_G})
local run=assert(loadstring(source));setfenv(run,env)
check(run()=='ready' and s.g_banshu==false,'entry enabled')
for i,price in ipairs(prices) do
    check(s.g_goldSpriteTable[i].gold.text==tostring(price),'configured price label '..i)
    ms.d_mainUI.g_playerInfo.gold_coin=price
    s.startSummon(i)
    check(sent[#sent].id==1042 and sent[#sent].data.pick_grade==i
        and sent[#sent].data.pick_type==3 and sent[#sent].data.ten_pick==0,'exact balance paid request '..i)
    local before=#sent
    ms.d_mainUI.g_playerInfo.gold_coin=price-1
    s.startSummon(i)
    check(#sent==before and hints[#hints]:find(tostring(price),1,true),'insufficient balance no request '..i)
end
local before=#sent
ms.d_mainUI.g_playerInfo.gold_coin=1000
ms.d_u.g_is_waiting_1106=true;s.startSummon(3);ms.d_u.g_is_waiting_1106=false
check(#sent==before,'pending request suppresses duplicate click')
s.g_allowSummon[1]=true;s.startSummon(1)
check(originalCalls[#originalCalls]==1 and #sent==before,'free path preserved')
s.g_summonerCount[2]=1;s.startSummon(2)
check(originalCalls[#originalCalls]==2 and #sent==before,'token path preserved')
s.g_summonerCount[3]=10;s.startSummon(103)
check(originalCalls[#originalCalls]==103 and #sent==before,'ten token path preserved')
for grade=2,3 do
    for _,tokens in ipairs({0,1,7,9}) do
        s.g_summonerCount[grade]=tokens
        s.g_allowSummon[grade]=true
        ms.d_mainUI.g_playerInfo.gold_coin=prices[grade]*(10-tokens)
        s.updateSummonLabels()
        check(parent.children[707200+grade]==nil,'no ten hint '..grade..' tokens '..tokens)
        s.startSummon(100+grade)
        check(sent[#sent].data.pick_grade==grade and sent[#sent].data.pick_type==3
            and sent[#sent].data.ten_pick==10,'ten gold request '..grade..' tokens '..tokens)
        local count=#sent
        ms.d_mainUI.g_playerInfo.gold_coin=prices[grade]*(10-tokens)-1
        s.startSummon(100+grade)
        check(#sent==count and hints[#hints]:find(tostring(prices[grade]*(10-tokens)),1,true),'ten insufficient '..grade..' tokens '..tokens)
    end
    s.g_summonerCount[grade]=10;s.updateSummonLabels()
    check(parent.children[707200+grade]==nil,'no ten token hint '..grade)
end
before=#sent
s.g_summonerCount[3]=0;s.g_allowSummon[3]=false
ms.d_mainUI.g_isNeedGuide=true;s.startSummon(3);ms.d_mainUI.g_isNeedGuide=false
check(originalCalls[#originalCalls]==3 and #sent==before,'guide path preserved')
ms.d_packageUI={g_packageItemsInfo={
    {attach_type=5,type_id=1006,count=3},{attach_type=5,type_id=1006,count=4},
    {attach_type=5,type_id=1007,count=9},{attach_type=4,type_id=1006,count=99}}}
check(ms.d_data.getItemCountByType(5,1006)==7,'sum advanced token stacks')
check(ms.d_data.getItemCountByType(5,1007)==9,'keep super token stacks separate')
check(ms.d_data.getItemCountByType(4,1006)==42,'other item types retain original counter')
s.getSummonerCount=function() s.g_summonerCount[2]=ms.d_data.getItemCountByType(5,1006) end
s.g_summonerCount[2]=0
ms.d_mainUI.g_playerInfo.gold_coin=369
local previous=#sent
s.startSummon(102)
check(#sent==previous+1 and s.g_summonerCount[2]==7,'refresh stale token cache before ten payment')
s.getSummonerCount=nil
ms.d_packageUI.g_packageItemsInfo={}
check(ms.d_data.getItemCountByType(5,1006)==0,'empty inventory clears token count')
local rows={}
for i=1,6 do rows[i]={type_id=i,time=100} end
s.updateSummonNews({first_send=true,lottery_list=rows})
check(#s.g_summonNews==6 and s.g_summonNews[1].type_id==1 and s.g_summonNews[6].type_id==6,'same second news order preserved')
s.updateSummonNews({first_send=true,lottery_list={{type_id=7,time=101}}})
check(#s.g_summonNews==1 and s.g_summonNews[1].type_id==7,'short snapshot clears stale rows')
s.updateSummonNews({first_send=true,lottery_list={}})
check(#s.g_summonNews==0,'empty snapshot clears news')
local wrapper=s.startSummon
check(run()=='ready' and s.startSummon==wrapper,'installation idempotent')
s._localGoldRestore()
check(s.startSummon==oldStart and s.updateSummonLabels==oldLabels and s.g_banshu==true
    and ms.d_data.getItemCountByType==oldItemCount and s.updateSummonNews==oldNews and s.sortNews==oldSort
    and s._localGoldRestore==nil,'cleanup restores original functions')
check(next(parent.children)==nil,'cleanup removes ten labels')
before=#sent
wrapper(103)
check(originalCalls[#originalCalls]==103 and #sent==before,'retained menu callback restores original behavior')
return table.concat(reports,'\n')
