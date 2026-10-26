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
  local wrappers={}
  local state={}
  local autoGroup=nil
  local function button(parent,text,x,y,fn,size)
   local label=CCLabelTTF:create(text,'arial',size or 24)
   label:setColor(ccc3(255,220,140))
   local item=CCMenuItemLabel:create(label);item:registerScriptTapHandler(fn)
   local menu=CCMenu:createWithItem(item);ms.d_u.setProperties(parent,menu,{x=x,y=y})
   parent:addChild(menu,40);return menu
  end
  local function controls(parent)
   if not parent or not state.title then return end
   parent:removeChildByTag(9876,true)
   local layer=CCLayer:create();parent:addChild(layer,80,9876)
   local text='本地NPC · '..state.title
   if state.settled then
    text=text..' · 第'..tostring((state.settlement or {}).order or '-')..'名 · 声望+'..tostring((state.settlement or {}).reputation or 0)..' · 奖励已入包'
   else text=text..' · 本阶段已战'..tostring(state.stage_fights or 0)..'场' end
   button(layer,text,0.5,0.955,function()
    ms.d_info.show('离线血战：每日最多开启一届，未完成的赛程保留。冲榜→练习→血战三阶段；每阶段至少战斗一次，可主动推进。前两阶段战败不扣血，第三阶段扣血。按血量、分数排名，最后结算奖励。对手均为本地NPC。')
   end,19)
   if state.own and not state.settled then
    local labels={'进入练习赛','进入血战一','进入血战二','进入血战三','结算本届'}
    button(layer,labels[state.stage] or '推进赛程',0.82,0.9,ui._localAdvance,23)
   end
  end
  ui._localAdvance=function()
   if state.own and not state.settled then ui.sendRequest(7,{stage=state.stage}) end
  end
  ui._localStage=function() return state end
  for _,name in ipairs({'showQualifyFight','showExerFight','showBloodFight','showCommonRank','showDoubleRank'}) do
   local native=ui[name];wrappers[name]=native
   ui[name]=function(...)
    local result=native(...)
    local parent=ui.g_arenaUI[name=='showQualifyFight' and 'qualify_layer' or name=='showBloodFight' and 'blood_layer' or 'rank_parent']
    controls(parent)
    return result
   end
  end
  ui.onGetResult=function(data)
   if data.local_arena then state=data.local_arena end
   -- Exercise responses have no original update branch. Keep every native view
   -- on the same authoritative snapshot, including records and score changes.
   if data.id==5 and ui.g_data.rank then
    ui.g_data.rank.rank_data=data.rank_data or ui.g_data.rank.rank_data
    ui.g_data.rank.event_info=data.event_info or ui.g_data.rank.event_info
    ui.g_data.reward_score=data.reward_score or 0
   end
   local result=oldResult(data)
   if data.id==1 and autoGroup then
    local group=autoGroup;autoGroup=nil;ui.sendRequest(2,{enter_group=group})
   end
   return result
  end
  ui.onFightReturn=function()
   ms.d_event_mgr.setSpecialFightType(0)
   autoGroup=ui.g_data.enter and ui.g_data.enter.role_group
   ui.enter(ms.d_undergoOrdealUI.getMainLayer())
  end
  ms.d_hz.gethz=function(key,...)
   if key=='undergo_info22' then return '玩家等级达到12级开放' end
   if key=='undergo_info16' then return '每日0点恢复神仙次数，当前大关小关进度重置' end
   return oldHz(key,...)
  end
  ms.d_undergoOrdealUI.pressEnterUndergoLayer=function()
   if ms.d_mainUI.g_playerInfo.level<12 then ms.d_info.show('玩家等级达到12级开放');return end
   ms.d_undergoOrdealUI.sendMsg(1,{})
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
   for name,native in pairs(wrappers) do ui[name]=native end
   ui._localAdvance=nil;ui._localStage=nil;ui._localTaixuRestore=nil
  end
 end
end
