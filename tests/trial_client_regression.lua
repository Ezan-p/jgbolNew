-- Lua 5.1 contract fixture for the native closure/index-one API.
local source=...
local checks,sent,notices={},{},{}
local now=100
local function check(name,fn) fn();checks[#checks+1]=name end
local function node()
 local n={children={},visible=true}
 function n:getChildByTag(tag) return self.children[tag] end
 function n:addChild(child,z,tag) child.parent=self;child.tag=tag;self.children[tag]=child end
 function n:removeAllChildrenWithCleanup() self.children={} end
 function n:removeFromParentAndCleanup() self.parent.children[self.tag]=nil end
 function n:setVisible(v) self.visible=v end
 function n:setColor(v) self.color=v end
 return n
end
local function newState()
 local main=node();main:addChild(node(),0,1001);main:addChild(node(),0,1005)
 return {main_layer=main,rightLayer=node(),challengeInfoLayer=node(),select=node(),leftBkg=node()}
end
local dataTable,bossList,damageList=newState(),{},{}
local fightCount,maxFightCount=0,10
local function createCountDownLabel() dataTable.isOnTime=true end
local function selectBoss(index)
 dataTable.lastSelectBoss=index
 if bossList[index] then
  dataTable.main_layer:getChildByTag(1001):addChild(node(),0,1)
 end
end
local function setLeftRelativePos(label,x,y) label.framePosition={x=x,y=y} end
local function createLeftPanel()
 local position=setLeftRelativePos -- Native closure exposes this positioning helper.
 selectBoss(1)
end
local function show() if dataTable.main_layer then createCountDownLabel();createLeftPanel() end end
local function getBoosInfo(data)
 bossList=data.train_data.boss_list
 damageList=data.train_data.friend_damage_list
 fightCount=data.train_data.train_times or 0
 maxFightCount=data.train_data.day_max_train_num or 10
end
local encounterType={}
local function native(data)
 if data.flag==2 then getBoosInfo(data);show()
 elseif data.flag==5 then encounterType[#encounterType+1]=data.train_data.type_id
 elseif data.flag==8 then bossList[1].hp=data.train_data.hp;bossList[1].is_dead=data.result==7
 elseif data.flag==9 then table.remove(bossList,1);createLeftPanel() end
end
local ui={processStatus=native}
local rawSend=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
package.loaded.ms={d_time={getTime=function() return now end},d_shilianUI=ui,d_u={main_server_send_msg=rawSend,setStyles=function(n,s) n.style=s end},
 d_info={show=function(s) notices[#notices+1]=s end}}
CCLabelTTF={create=function(_,text,font,size) local n=node();n.text=text;return n end}
ccc3=function(r,g,b) return {r,g,b} end
assert(loadstring(source))()
local function entry()
 ui.processStatus({flag=2,result=1,train_data={boss_list={
  {boss_id=11,type_id=5001,tier_name='低档',manual_grade=6,train_times=10,hp=100,friend_damage_list={11}},
  {boss_id=12,type_id=5022,tier_name='中档',manual_grade=6,train_times=0,hp=200,friend_damage_list={12}},
  {boss_id=13,type_id=5045,tier_name='高档',manual_grade=6,train_times=3,hp=300,friend_damage_list={13}}},friend_damage_list={11},expires_at=200}})
end
local function up(fn,key)
 for i=1,100 do local k,v=debug.getupvalue(fn,i);if k==key then return v end;if not k then break end end
end
check('three portraits keep independent counters and refresh hint above left frame',function()
 entry();local choose=up(createLeftPanel,'selectBoss')
 choose(2)
 assert(bossList[1].boss_id==12 and dataTable.lastSelectBoss==1 and damageList[1]==12)
 assert(fightCount==0 and dataTable.challengeInfoLayer:getChildByTag(9177).text=='本首领挑战次数0/10')
 assert(dataTable.main_layer:getChildByTag(9175).text=='每日刷新清空')
 local hint=dataTable.main_layer:getChildByTag(9175)
 assert(hint.framePosition.x==0.5 and hint.framePosition.y>1)
 assert(not dataTable.main_layer:getChildByTag(1001):getChildByTag(9175))
 choose(3)
 assert(bossList[1].boss_id==13 and damageList[1]==13)
 assert(fightCount==3 and dataTable.challengeInfoLayer:getChildByTag(9177).text=='本首领挑战次数3/10')
end)
check('challenge and claim carry immutable instance identity',function()
 local send=package.loaded.ms.d_u.main_server_send_msg
 local request={fight_type=11,des_type=8,des_id=5001,des_value=0}
 send(1026,request)
 assert(sent[#sent].data.des_id==5045 and sent[#sent].data.des_value==13)
 assert(request.des_value==0)
 send(1064,{flag=9,id=0});assert(sent[#sent].data.id==13)
end)
check('responses settle matching instance after selection changes',function()
 ui.processStatus({flag=8,result=7,train_data={boss_id=12,hp=0,train_times=1,friend_damage_list={99}}})
 assert(bossList[1].boss_id==12 and bossList[1].is_dead)
 show();assert(damageList[1]==99 and fightCount==1)
 ui.processStatus({flag=9,result=1,train_data={boss_id=12,prize={}}})
 assert(#bossList==2 and bossList[1].boss_id~=12 and dataTable.lastSelectBoss==1)
 assert(dataTable.main_layer:getChildByTag(9175))
end)
check('last claim clears widgets and cooldown selection',function()
 for i=1,2 do ui.processStatus({flag=9,result=1,train_data={boss_id=bossList[1].boss_id,prize={}}}) end
 assert(#bossList==0 and dataTable.lastSelectBoss==nil)
 assert(next(dataTable.main_layer:getChildByTag(1001).children)==nil)
end)
check('empty entry explains journey and clears stale state after reentry',function()
 dataTable=newState();entry()
 ui.processStatus({flag=2,result=2,train_data={no_boss=true,boss_list={}}})
 assert(#bossList==0 and dataTable.lastSelectBoss==nil)
 assert(string.find(notices[#notices],'旅途闯关',1,true))
end)
check('encounter push preserves original popup queue',function()
 ui.processStatus({flag=5,result=1,train_data={type_id=5001}})
 assert(encounterType[1]==5001)
end)
check('midnight action expires cached bosses and requests fresh query',function()
 entry();now=200
 package.loaded.ms.d_u.main_server_send_msg(1064,{flag=9,id=11})
 assert(#bossList==0 and dataTable.lastSelectBoss==nil)
 assert(sent[#sent].mid==1064 and sent[#sent].data.flag==2)
 assert(string.find(notices[#notices],'零点刷新',1,true))
 now=100;entry();now=201
 package.loaded.ms.d_u.main_server_send_msg(1026,{fight_type=11,des_type=8,des_id=5001})
 assert(sent[#sent].mid==1064 and sent[#sent].data.flag==2)
 now=100
end)
check('disabled help never sends and restore restores all hooks',function()
 local count=#sent
 for _,flag in ipairs({3,4,7}) do package.loaded.ms.d_u.main_server_send_msg(1064,{flag=flag}) end
 assert(#sent==count)
 ui._localTrialRestore()
 assert(ui.processStatus==native and package.loaded.ms.d_u.main_server_send_msg==rawSend)
 assert(up(createLeftPanel,'selectBoss')==selectBoss)
end)
return checks
