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
  local oldArenaEnter=ui.enter
  local prizeView=false
  local wrappers={}
  local state={}
  local entryTag=9875
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
  -- The native carousel hard-codes seven slots. Keep the four original high
  -- group IDs (4..7), but build only their entrance cards and native art.
  wrappers.show=ui.show
  ui.show=function(parent,returnFromFight,isRecord)
   parent=parent or ui.g_arenaUI.parent_layer
   parent:removeChildByTag(entryTag,true)
   local layer=CCLayer:create();parent:addChild(layer,1000,entryTag)
   ui.g_arenaUI.parent_layer=parent;ui.g_arenaUI.main_layer=layer
   ui.g_arenaUI.qualify_layer=nil;ui.g_arenaUI.blood_layer=nil;ui.g_arenaUI.rank_parent=nil
   ms.d_u.createSwallowTouchLayer(layer)
   layer:addChild(ms.d_u.createByStyle({pic='v2/summonUI/advance_bkg.jpg',x=0.5,y=0.5,scaleX=1,scaleY=1}))
   layer:addChild(ms.d_u.createByStyle({pic='v2/arenaUI/title8.png',x=0.5,y=0.92}))
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
     body:setPosition(ccp(size.width*x,size.height*0.55));layer:addChild(body)
     local label=CCLabelTTF:create(tostring(info.min_level)..'—'..tostring(info.max_level)..'级','arial',24)
     label:setColor(own and ccc3(255,220,140) or ccc3(235,225,207))
     label:setPosition(ccp(size.width*x,size.height*0.29));layer:addChild(label)
     local selected=group
     optionButton(layer,own and '进入本组' or '查看分组',x,0.19,function()
      ui.sendRequest(2,{enter_group=selected})
     end,true,154):setTag(9900+group)
    end
   end
   layer:addChild(ms.d_u.createMenu({x=0,y=0,{npic='v2/introUI/close1.png',spic='v2/introUI/close2.png',x=0.95,y=0.93,
    call_back=function() ms.d_u.remove(layer) end}}),10)
   if returnFromFight~=nil and ui.g_data.rank then
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
    text=text..' · 第'..tostring((state.settlement or {}).order or '-')..'名 · 声望+'..tostring((state.settlement or {}).reputation or 0)
   else text=text..' · 本阶段已战'..tostring(state.stage_fights or 0)..'场' end
   button(layer,text,0.5,0.955,function()
    ms.d_info.show('血战：每日最多开启一届，未完成的赛程保留。冲榜→练习→血战三阶段；每阶段至少战斗一次，可主动推进。前两阶段战败不扣血，第三阶段扣血。按血量、分数排名，最后结算奖励。')
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
    -- The native rank close button only removes its own layer. Rebuild the
    -- entrance underneath, so it cannot reveal the previous blood stage.
    ui.show()
   end
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
   if ms.d_mainUI.g_playerInfo.level<50 then ms.d_info.show('玩家等级达到50级开放');return end
   return oldRootEnter(...)
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
   ui.onGetResult=oldResult;ui.onFightReturn=oldReturn
   ms.d_hz.gethz=oldHz;map.show=oldMapShow;map.canFightNextChallenge=oldMapFight
   ms.d_undergoOrdealUI.pressEnterUndergoLayer=oldEnter
   ms.d_undergoOrdealUI.enter=oldRootEnter;ui.enter=oldArenaEnter
   for name,native in pairs(wrappers) do ui[name]=native end
   ui._localAdvance=nil;ui._localStage=nil;ui._localTaixuRestore=nil
  end
 end
end
