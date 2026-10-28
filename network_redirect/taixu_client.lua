-- Native Taixu maps, formations and arena layouts; offline schedule controls.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_arenaUI
 local map=ms and ms.d_undergoMapUI
 if not (ui and map and ms.d_undergoOrdealUI) then return 'pending' end
 if ui and map and not ui._localTaixuRestore then
  local oldResult,oldReturn=ui.onGetResult,ui.onFightReturn
  local oldHz=ms.d_hz.gethz
  local oldMapShow=map.show
  local oldMapFight=map.canFightNextChallenge
  local oldEnter=ms.d_undergoOrdealUI.pressEnterUndergoLayer
  local oldRootEnter=ms.d_undergoOrdealUI.enter
  local oldShopSend=ms.d_undergoOrdealUI.sendMsg
  local oldShopResult=ms.d_undergoOrdealUI.onGetResult
  local shopToken=nil
  ms.d_undergoOrdealUI.onGetResult=function(op,data,...)
   if op==3 then shopToken=data and data[1] and data[1].shop_token end
   return oldShopResult(op,data,...)
  end
  ms.d_undergoOrdealUI.sendMsg=function(op,data,...)
   if op==5 then
    local request={};for k,v in pairs(data or {}) do request[k]=v end
    request.shop_token=shopToken;data=request
   end
   return oldShopSend(op,data,...)
  end
  local oldArenaEnter=ui.enter
  local prizeView=false
  local wrappers={}
  local state={}
  local entryTag=9875
  local entryVisualTag=9879
  local entryVisual=nil
  local function isExit(event)
   return event=='exit' or type(event)=='table' and event.name=='exit'
  end
  local function removeLayer(layer)
   if not layer or not layer.getParent or not layer:getParent() then return end
   pcall(ms.d_u.remove,layer)
  end
  local function clearArenaLayers()
   local seen={}
   for _,key in ipairs({'qualify_layer','blood_layer','rank_parent'}) do
    local layer=ui.g_arenaUI[key]
    if layer and layer~=ui.g_arenaUI.main_layer and not seen[layer] then
     seen[layer]=true;removeLayer(layer)
    end
    ui.g_arenaUI[key]=nil
   end
  end
  local function hideEntryVisual()
   if entryVisual and entryVisual.getParent and entryVisual:getParent() then
    entryVisual:setVisible(false)
   end
  end
  local function restoreEntryVisual()
   if entryVisual and entryVisual.getParent and entryVisual:getParent() then
    entryVisual:setVisible(true)
   end
  end
  local function watchRankClose(parent)
   if not parent or parent:getChildByTag(9880) then return end
   -- This client sends {name='exit'}, not a string. Use a child observer so
   -- native rank lifecycle handlers keep their own cleanup callbacks.
   local watcher=CCLayer:create()
   watcher:registerScriptHandler(function(event)
    if not isExit(event) then return end
    for _,key in ipairs({'qualify_layer','blood_layer','rank_parent'}) do
     if ui.g_arenaUI[key]==parent then ui.g_arenaUI[key]=nil end
    end
    restoreEntryVisual()
   end)
   parent:addChild(watcher,0,9880)
  end
  local function button(parent,text,x,y,fn,size)
   local label=CCLabelTTF:create(text,'arial',size or 24)
   label:setColor(ccc3(255,220,140))
   local item=CCMenuItemLabel:create(label);item:registerScriptTapHandler(fn)
   local menu=CCMenu:createWithItem(item);ms.d_u.setProperties(parent,menu,{x=x,y=y})
   parent:addChild(menu,40);return menu
  end
  local function optionButton(parent,text,x,y,fn,enabled,width)
   local w,h=width or 168,46
   local function face(pressed)
    local border=CCLayerColor:create(enabled and ccc4(206,157,78,255) or ccc4(105,100,90,255),w,h)
    local fill=CCLayerColor:create(enabled and (pressed and ccc4(116,65,34,255) or ccc4(66,39,27,255)) or ccc4(49,47,43,255),w-4,h-4)
    fill:setPosition(ccp(2,2));border:addChild(fill)
    local label=CCLabelTTF:create(text,'arial',22)
    label:setColor(enabled and ccc3(255,230,172) or ccc3(153,149,139))
    label:setPosition(ccp(w/2,h/2));border:addChild(label,1)
    return border
   end
   local item=CCMenuItemSprite:create(face(false),face(true))
   item:setEnabled(enabled);item:registerScriptTapHandler(fn)
   local menu=CCMenu:createWithItem(item);ms.d_u.setProperties(parent,menu,{x=x,y=y})
   menu:setScale(math.min(1,CCDirector:sharedDirector():getWinSize().width/960))
   parent:addChild(menu,40);return menu
  end
  local rulesEntryTag,rulesPanelTag=9881,9882
  local rulePages={
   {title='玩法流程',lines={
    '50级开放，按等级分四组；每组为自己与19名对手。',
    '流程：冲榜 → 练习 → 血战一、二、三 → 结算本届。',
    '冲榜有10次免费挑战；练习有5次，不改变积分和血量。',
    '每段血战有9行动力，每战消耗3点；全届共24场免费战。',
    '每阶段完成一战即可手动推进，不要求获胜；血量为0也可推进。',
    '提前推进不保留剩余次数，不能回到上一阶段补打。',
    '正式赛胜利加100分、对手扣20血；前两段进攻失败不扣血。',
    '第三段进攻失败扣20血；按血量优先、积分其次排名。',
    '免费次数用完可付20元宝补一战，全届最多补5次。',
   }},
   {title='活动时间',lines={
    '每周开放一届，按北京时间周一00:00统一刷新。',
    '本周内随时可玩，各阶段由玩家手动推进。',
    '周刷新时，无论上届是否结算，全部重新开始冲榜。',
    '未完成的阶段、积分、血量、次数和战报均不跨周保留。',
    '新周重置免费挑战、行动力和付费补战额度，重新确定分组。',
    '同周结算后不能再开第二届，需等下周一00:00刷新。',
    '同周退出、重登或跨日保留进度，零点不额外补次数。',
    '请在周刷新前结算；未结算的上周排名奖励不补发。',
    '已经获得的元宝、圣母蟠桃和仙晶保留，不随周刷新清空。',
   }},
   {title='奖励说明',lines={
    '冲榜、练习和三段血战：每次击败对手都获得100仙晶。',
    '重复击败同一对手照常发奖；失败、平局及战报回放不发奖。',
    '最终排名奖励：元宝 / 圣母蟠桃 / 仙晶',
    '第1名           500元宝       10个圣母蟠桃       10000仙晶',
    '第2—3名       400元宝         8个圣母蟠桃         8000仙晶',
    '第4—10名     250元宝         5个圣母蟠桃         5000仙晶',
    '第11—20名   150元宝         3个圣母蟠桃         3000仙晶',
    '点击“结算本届”自动发放三项奖励，每届只发一次。',
    '最终奖励不再记录声望；关闭奖励弹窗不影响已经到账的奖励。',
   }},
  }
  local function showArenaRules(parent,page)
   parent:removeChildByTag(rulesPanelTag,true)
   local layer=CCLayer:create();parent:addChild(layer,2000,rulesPanelTag)
   ms.d_u.createSwallowTouchLayer(layer)
   local size=CCDirector:sharedDirector():getWinSize()
   local scale=math.min(size.width/960,size.height/540)
   local shade=CCLayerColor:create(ccc4(0,0,0,205),size.width,size.height)
   layer:addChild(shade,-2)
   local border=CCLayerColor:create(ccc4(173,127,65,255),size.width*0.90,size.height*0.88)
   border:setPosition(ccp(size.width*0.05,size.height*0.06));layer:addChild(border,-1)
   local panel=CCLayerColor:create(ccc4(42,29,24,255),size.width*0.90-4,size.height*0.88-4)
   panel:setPosition(ccp(2,2));border:addChild(panel)
   local function label(text,x,y,font,color,center)
    local n=CCLabelTTF:create(text,'arial',font*scale)
    n:setColor(color);n:setAnchorPoint(ccp(center and 0.5 or 0,0.5))
    n:setScale(math.min(1,size.width*0.80/math.max(1,n:getContentSize().width)))
    n:setPosition(ccp(size.width*x,size.height*y));layer:addChild(n,10)
   end
   label('血战 · 离线规则',0.5,0.88,28,ccc3(255,221,153),true)
   for index,section in ipairs(rulePages) do
    local selected=index
    optionButton(layer,(index==page and '◆ ' or '')..section.title,0.28+(index-1)*0.22,0.77,function()
     showArenaRules(parent,selected)
    end,true,172):setTag(9883+index)
   end
   for index,text in ipairs(rulePages[page].lines) do
    label(text,0.10,0.675-(index-1)*0.060,22,ccc3(241,227,201),false)
   end
   label('以上为当前离线玩法；可随时关闭说明，继续游戏。',0.5,0.11,18,ccc3(185,164,132),true)
   layer:addChild(ms.d_u.createMenu({x=0,y=0,{npic='v2/introUI/close1.png',spic='v2/introUI/close2.png',x=0.90,y=0.88,
    call_back=function() ms.d_u.remove(layer) end}}),60,9887)
  end
  local function addRulesEntry()
   local parent=ms.d_undergoOrdealUI.getMainLayer()
   if not parent then return end
   parent:removeChildByTag(rulesEntryTag,true)
   -- Keep the entrance beside the native help menu, below shop/arena overlays.
   local layer=CCLayer:create();parent:addChild(layer,1,rulesEntryTag)
   optionButton(layer,'血战规则',0.17,0.95,function() showArenaRules(parent,1) end,true,132)
  end
  ui._localRefreshRulesEntry=addRulesEntry
  -- The native carousel hard-codes seven slots. Keep the four original high
  -- group IDs (4..7), but build only their entrance cards and native art.
  wrappers.show=ui.show
  ui.show=function(parent,returnFromFight,isRecord)
   parent=parent or ui.g_arenaUI.parent_layer
   clearArenaLayers()
   parent:removeChildByTag(entryTag,true)
   entryVisual=nil
   local layer=CCLayer:create();parent:addChild(layer,1000,entryTag)
   local visual=CCLayer:create();layer:addChild(visual,0,entryVisualTag);entryVisual=visual
   ui.g_arenaUI.parent_layer=parent;ui.g_arenaUI.main_layer=layer
   layer:registerScriptHandler(function(event)
    if isExit(event) and ui.g_arenaUI.main_layer==layer then
     entryVisual=nil
     ui.g_arenaUI.main_layer=nil
     ui.g_arenaUI.qualify_layer=nil;ui.g_arenaUI.blood_layer=nil;ui.g_arenaUI.rank_parent=nil
    end
   end)
   ms.d_u.createSwallowTouchLayer(layer)
   visual:addChild(ms.d_u.createByStyle({pic='v2/summonUI/advance_bkg.jpg',x=0.5,y=0.5,scaleX=1,scaleY=1}))
   visual:addChild(ms.d_u.createByStyle({pic='v2/arenaUI/title8.png',x=0.5,y=0.92}))
   local size=CCDirector:sharedDirector():getWinSize()
   local entry=ui.g_data.enter
   local portraits={[4]=5036,[5]=5048,[6]=5027,[7]=5046}
   for group=4,7 do
    local info=entry.group_type_level[group]
    if info then
     local x=0.185+(group-4)*0.21
     local own=group==entry.role_group
     local body=ms.d_data.getBodySprite(portraits[group],true)
     local bounds=body:getContentSize()
     body:setAnchorPoint(ccp(0.5,0.5))
     body:setScale(math.min(size.width*0.18/math.max(1,bounds.width),size.height*0.43/math.max(1,bounds.height)))
     body:setPosition(ccp(size.width*x,size.height*0.55));visual:addChild(body)
     local label=CCLabelTTF:create(tostring(info.min_level)..'—'..tostring(info.max_level)..'级','arial',24)
     label:setColor(own and ccc3(255,220,140) or ccc3(235,225,207))
     label:setPosition(ccp(size.width*x,size.height*0.29));visual:addChild(label)
     local selected=group
     optionButton(visual,own and '进入本组' or '查看分组',x,0.19,function()
      ui.sendRequest(2,{enter_group=selected})
     end,true,154):setTag(9900+group)
    end
   end
   visual:addChild(ms.d_u.createMenu({x=0,y=0,{npic='v2/introUI/close1.png',spic='v2/introUI/close2.png',x=0.95,y=0.93,
    call_back=function() ms.d_u.remove(layer) end}}),10)
   if returnFromFight~=nil and ui.g_data.rank then
    hideEntryVisual()
    local snapshot={};for key,value in pairs(ui.g_data.rank) do snapshot[key]=value end
    snapshot.id=2;oldResult(snapshot)
    if isRecord then ui.showBloodHis(ui.g_arenaUI.blood_layer or ui.g_arenaUI.rank_parent) end
   end
  end
  local function controls(parent)
   if not parent or not state.title then return end
   parent:removeChildByTag(9876,true)
   local layer=CCLayer:create();parent:addChild(layer,80,9876)
   local text=state.title
   if state.settled then
    text=text..' · 第'..tostring((state.settlement or {}).order or '-')..'名'
   else text=text..' · 本阶段已战'..tostring(state.stage_fights or 0)..'场' end
   button(layer,text,0.5,0.955,function()
    ms.d_info.show('血战：每周一北京时间00:00重置，未完成赛程也清空。冲榜→练习→血战三阶段→结算；每次胜利100仙晶。最终按血量、分数排名，发放元宝、圣母蟠桃与仙晶。请在周刷新前结算。')
   end,19)
   if state.own and not state.settled then
    local labels={'进入练习赛','进入血战一','进入血战二','进入血战三','结算本届'}
    optionButton(layer,labels[state.stage] or '推进赛程',0.80,0.89,ui._localAdvance,state.can_advance==true):setTag(9878)
   end
  end
  ui._localAdvance=function()
   if state.own and not state.settled and state.can_advance then ui.sendRequest(7,{stage=state.stage}) end
  end
  ui._localStage=function() return state end
  for _,name in ipairs({'showQualifyFight','showExerFight','showBloodFight','showCommonRank','showDoubleRank'}) do
   local native=ui[name];wrappers[name]=native
   ui[name]=function(...)
    local result
    if name=='showExerFight' then
     -- The original practice view polls when formal_race.start_time has passed.
     -- Preserve every original node/position, but render its timer slot once as
     -- an offline instruction, without installing the one-second poll callback.
     local oldRest,oldDelay=ms.d_time.getRestTime,ms.d_u.delay
     local schedule=ui.g_data.enter.schedule_list.match_time_list
     local formalStart=schedule[3].start_time
     ms.d_time.getRestTime=function(time,...)
      if time==formalStart then return '可直接推进' end
      return oldRest(time,...)
     end
     ms.d_u.delay=function(parent,seconds,callback,...)
      if seconds==1 then return end
      return oldDelay(parent,seconds,callback,...)
     end
     local ok,value=pcall(native,...)
     ms.d_time.getRestTime=oldRest;ms.d_u.delay=oldDelay
     if not ok then error(value) end
     result=value
    else result=native(...) end
    local parent=ui.g_arenaUI[name=='showQualifyFight' and 'qualify_layer' or name=='showBloodFight' and 'blood_layer' or 'rank_parent']
    controls(parent)
    watchRankClose(parent)
    return result
   end
  end
  wrappers.showPrize=ui.showPrize
  ui.showPrize=function(...)
   prizeView=true
   local ok,value=pcall(wrappers.showPrize,...)
   prizeView=false
   if not ok then error(value) end
   return value
  end
  ui.onGetResult=function(data)
   if data.local_arena then state=data.local_arena end
   if data.local_entry then ui.g_data.enter=data.local_entry end
   if data.id==1 then
    ui.g_data.enter=data
    return ui.show()
   end
   if data.id==2 and state.settled then
    -- The native rank close button only removes its own layer. Rebuild a
    -- clean entrance host underneath; its visual layer is hidden while the
    -- settled rank is open and restored after the rank layer exits.
    ui.show()
   end
   if data.id==2 then hideEntryVisual() end
   -- Exercise responses have no original update branch. Keep every native view
   -- on the same authoritative snapshot, including records and score changes.
   if data.id==5 and ui.g_data.rank then
    ui.g_data.rank.rank_data=data.rank_data or ui.g_data.rank.rank_data
    ui.g_data.rank.event_info=data.event_info or ui.g_data.rank.event_info
    ui.g_data.reward_score=data.reward_score or 0
   end
   local result=oldResult(data)
   if data.local_prizes and #data.local_prizes>0 then
    ms.d_commonLayerUI.showPrizeResLayer(ui.g_arenaUI.main_layer,data.local_prizes)
   end
   return result
  end
  ui.onFightReturn=function(isRecord)
   -- Native return calls our four-group show with delay=0. Restore the current
   -- authoritative board synchronously, without entry/group network queries.
   return oldReturn(isRecord)
  end
  ms.d_hz.gethz=function(key,...)
   if key=='kfight6' and prizeView then return '结算本届后显示获得奖励' end
   if key=='undergo_info22' then return '玩家等级达到50级开放' end
   if key=='undergo_info16' then return '每日0点恢复神仙次数，当前大关小关进度重置' end
   return oldHz(key,...)
  end
  ms.d_undergoOrdealUI.pressEnterUndergoLayer=function()
   if ms.d_mainUI.g_playerInfo.level<50 then ms.d_info.show('玩家等级达到50级开放');return end
   ms.d_undergoOrdealUI.sendMsg(1,{})
  end
  ms.d_undergoOrdealUI.enter=function(...)
   -- activityUI.getRequireLevel: the outer menu/shop unlocks at 12.
   -- pressEnterUndergoLayer separately enforces the original 50-level gate.
   if ms.d_mainUI.g_playerInfo.level<12 then ms.d_info.show('玩家等级达到12级开放');return end
   local result=oldRootEnter(...)
   addRulesEntry()
   return result
  end
  ui.enter=function(...)
   if ms.d_mainUI.g_playerInfo.level<50 then ms.d_info.show('玩家等级达到50级开放');return end
   return oldArenaEnter(...)
  end
  map.canFightNextChallenge=function(mid,sid)
   if mid>9 then return false end
   return oldMapFight(mid,sid)
  end
  map.show=function(...)
   local result=oldMapShow(...)
   local parent=map.g_mapUI.main_layer
   if parent then
    parent:removeChildByTag(9877,true)
    local layer=CCLayer:create();parent:addChild(layer,80,9877)
    local progress=map.g_mapUI.mapList
    local complete=progress and progress.challenge.big_id>9
    button(layer,complete and '历劫九九关已通关 · 每日可领奖' or '刷新历劫进度',0.78,0.95,function()
     ms.d_undergoOrdealUI.sendMsg(1,{})
    end,20)
   end
   return result
  end
  ui._localTaixuRestore=function()
   -- The native module can retain a destroyed scene after leaving Taixu.
   pcall(function()
    local root=ms.d_undergoOrdealUI.getMainLayer()
    if root then root:removeChildByTag(rulesEntryTag,true);root:removeChildByTag(rulesPanelTag,true) end
   end)
   ui.onGetResult=oldResult;ui.onFightReturn=oldReturn
   ms.d_hz.gethz=oldHz;map.show=oldMapShow;map.canFightNextChallenge=oldMapFight
   ms.d_undergoOrdealUI.pressEnterUndergoLayer=oldEnter
   ms.d_undergoOrdealUI.enter=oldRootEnter;ui.enter=oldArenaEnter
   ms.d_undergoOrdealUI.sendMsg=oldShopSend;ms.d_undergoOrdealUI.onGetResult=oldShopResult
   for name,native in pairs(wrappers) do ui[name]=native end
   ui._localRefreshRulesEntry=nil
   ui._localAdvance=nil;ui._localStage=nil;ui._localTaixuRestore=nil
  end
 end
end
