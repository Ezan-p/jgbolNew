-- Keep the native encounter popup, three portraits, battle and reward widgets.
-- The native solo actions always use bossList[1]; promote the selected portrait.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_shilianUI
 if not ui or not ui.processStatus or not ms.d_u then return 'pending' end
 if not ui._localTrialRestore then
  local original,send=ui.processStatus,ms.d_u.main_server_send_msg
  local expiresAt
  local function up(fn,key,value,write)
   if not fn then return end
   for i=1,100 do
    local name,current=debug.getupvalue(fn,i)
    if not name then break end
    if name==key then
     if write then debug.setupvalue(fn,i,value) end
     return current
    end
   end
  end
  local show=up(original,'show')
  local getBoss=up(original,'getBoosInfo')
  local left=up(show,'createLeftPanel')
  local select=up(left,'selectBoss')
  if not show or not getBoss or not left or not select then return 'pending' end
  local function bosses() return up(getBoss,'bossList') or {} end
  local function state() return up(show,'dataTable') end
  local function finish()
   local s=state()
   if not s or not s.main_layer then return end
   s.lastSelectBoss=nil
   for _,tag in ipairs({1001,1005}) do
    local node=s.main_layer:getChildByTag(tag)
    if node then node:removeAllChildrenWithCleanup(true) end
   end
   for _,key in ipairs({'rightLayer','challengeInfoLayer','select'}) do
    if s[key] then s[key]:setVisible(false) end
   end
  end
  local function clearBosses()
   up(getBoss,'bossList',{},true)
   if state() and state().main_layer then left() end
   finish()
  end
  local function refreshHint()
   local s=state()
   local position=up(left,'setLeftRelativePos')
   if not s or not s.main_layer or not s.leftBkg or not position or not CCLabelTTF then return end
   local old=s.main_layer:getChildByTag(9175)
   if old then old:removeFromParentAndCleanup(true) end
   local label=CCLabelTTF:create('每日刷新清空','arial',18)
   label:setColor(ccc3(255,215,140))
   -- Anchor to the original left frame, just above its title strip.
   position(label,0.5,1.04)
   s.main_layer:addChild(label,20,9175)
  end
  local function selectOwn(index)
   local list,s=bosses(),state()
   refreshHint()
   index=tonumber(index)
   if not index or not list[index] then return end
   if index~=1 then
    list[1],list[index]=list[index],list[1]
    s.lastSelectBoss=nil
    -- Rebuild native portraits so the highlighted first portrait is the target.
    left()
    return
   end
   up(getBoss,'damageList',list[1].friend_damage_list or {},true)
   up(getBoss,'fightCount',list[1].train_times or 0,true)
   -- The native counter and cooldown share this layer; rebuild both on selection.
   if s.challengeInfoLayer and CCLabelTTF then
    s.challengeInfoLayer:removeAllChildrenWithCleanup(true)
    local count=CCLabelTTF:create('本首领挑战次数'..tostring(list[1].train_times or 0)..'/'..tostring(up(getBoss,'maxFightCount') or 10),'arial',26)
    ms.d_u.setStyles(count,{x=0.53,y=0.18})
    s.challengeInfoLayer:addChild(count,2,9177)
    local countdown=up(show,'createCountDownLabel')
    if countdown then countdown() end
   end
   select(1)
  end
  up(left,'selectBoss',selectOwn,true)
  ui.processStatus=function(data)
   if data.flag==2 and data.train_data then expiresAt=data.train_data.expires_at end
   if data.flag==2 and data.train_data and data.train_data.no_boss then
    clearBosses()
    ms.d_info.show('尚未遭遇试炼首领，请前往旅途闯关；最多留存3位。每日零点清空首领和未领奖励。')
    return
   end
   if data.flag==2 and state() then state().lastSelectBoss=nil end
   if (data.flag==8 or data.flag==9) and data.train_data and data.train_data.boss_id then
    local list=bosses()
    for i,b in ipairs(list) do
     if b.boss_id==data.train_data.boss_id then
      if data.flag==8 then
       b.friend_damage_list=data.train_data.friend_damage_list or {}
       b.train_times=data.train_data.train_times or b.train_times or 0
      end
      list[1],list[i]=list[i],list[1]
      if state() then state().lastSelectBoss=nil end
      break
     end
    end
   end
   local result=original(data)
   if data.flag==9 and data.result==1 and #bosses()==0 then finish() end
   return result
  end
  ms.d_u.main_server_send_msg=function(mid,data,...)
   if mid==1064 and data and (data.flag==3 or data.flag==4 or data.flag==7) then
    ms.d_info.show('好友助战暂未开放，请独自挑战试炼首领。')
    return
   end
   local isAction=data and ((mid==1064 and data.flag==9) or (mid==1026 and data.fight_type==11))
   if isAction and expiresAt and ms.d_time and ms.d_time.getTime()>=expiresAt then
    clearBosses()
    ms.d_info.show('诸神试炼已于零点刷新，旧首领和未领奖励已清空，请重新在旅途中遭遇。')
    return send(1064,{flag=2,id=0})
   end
   local b=bosses()[1]
   if b and data and ((mid==1064 and data.flag==9) or (mid==1026 and data.fight_type==11)) then
    local q={};for k,v in pairs(data) do q[k]=v end
    if mid==1064 then q.id=b.boss_id or 0
    else q.des_id=b.type_id;q.des_value=b.boss_id or 0 end
    return send(mid,q,...)
   end
   return send(mid,data,...)
  end
  ui._localTrialRestore=function()
   local s=state()
   local hint=s and s.main_layer and s.main_layer:getChildByTag(9175)
   if hint then hint:removeFromParentAndCleanup(true) end
   up(left,'selectBoss',select,true)
   ui.processStatus=original;ms.d_u.main_server_send_msg=send;ui._localTrialRestore=nil
  end
 end
end
