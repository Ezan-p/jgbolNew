-- Original 3.87 forge widgets, with the missing entry and protocol bridges.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_forgeUI
 if not ui or not ui.showForgeMainLayer then return 'pending' end
 if not ui._localExchangeRestore then
 -- Upgrade the older bridge before capturing native functions.
 if ui._localCraftingRestore then ui._localCraftingRestore() end
 local function up(fn,key)
  for i=1,40 do
   local name,value=debug.getupvalue(fn,i)
   if not name then break end
   if name==key then return value end
  end
 end
 local state=assert(up(ui.showForgeMainLayer,'g_forgeUI'))
 local config=assert(up(ui.showForgeMainLayer,'g_self'))
 local old={}
 for _,key in ipairs({'show','returnBack','updateForgeList','isNeedUpdateList',
   'updateActivityStatus','getForgeResult','showForgeMainLayer','getEquipsByQuality','canForge','countDown'}) do old[key]=ui[key] end
 local catalog,offsets={},{}
 local weekly,pendingNotice,refreshing
 local minimum=30
 local function alive()
  if not state.main_layer then return false end
  local ok,parent=pcall(function() return state.main_layer:getParent() end)
  return ok and parent
 end
 local function query()
  if (tonumber(ms.d_mainUI.g_playerInfo.level) or 0)<minimum then
   ms.d_info.show('角色达到'..minimum..'级开放装备兑换');return
  end
  ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_query_compose_list,{flag=0})
 end
 local function refreshWeek()
  if refreshing then return end
  refreshing=true
  ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_query_compose_list,{flag=1})
 end
 ui.canForge=function(notify)
  if weekly then
   if ms.d_time.getTime()>=weekly.weekly_reset_at then
    refreshWeek()
    if notify then ms.d_info.show('每周兑换额度正在刷新，请稍后再试') end
    return false
   end
   if weekly.weekly_remaining<=0 then
    if notify then ms.d_info.show(weekly.weekly_notice) end
    return false
   end
  end
  return old.canForge(notify)
 end
 ui.countDown=function()
  if not weekly then return old.countDown() end
  if not alive() then return end
  state.main_layer:removeChildByTag(config.tagDef.timeTag,true)
  local label=ms.d_u.createByStyle({type='label',font='arial',fontsize=22,
   string='每周一00:00刷新（北京时间）',x=0.75,y=0.76,color=config.Color.gray})
  state.main_layer:addChild(label,1,config.tagDef.timeTag)
  -- Schedule against the label: replacement or closing cancels the old timer.
  ms.d_u.delay(label,math.max(1,weekly.weekly_reset_at-ms.d_time.getTime()),refreshWeek)
 end
 local function page(kind)
  local all=catalog[kind]
  if not all then return end
  -- The native renderer has exactly three slots. Overlap the last group so
  -- every slot stays real, including a four-fragment or 61-equipment catalog.
  local first=math.max(1,math.min(offsets[kind] or 1,#all-2))
  offsets[kind]=first
  local list={left_times=all.left_times,max_times=all.max_times}
  for i=first,math.min(first+2,#all) do list[#list+1]=all[i] end
  config.forgeList[kind]=list
 end
 local function button(parent,text,x,y,callback)
  local function sprite()
   local s=CCSprite:create('v2/forgeUI/name_bkg.png')
   local size=s:getContentSize()
   local label=CCLabelTTF:create(text,'arial',24)
   label:setColor(ccc3(255,200,80));label:setPosition(ccp(size.width/2,size.height/2))
   s:addChild(label);return s
  end
  local menu=ms.d_u.createMenu({x=0,y=0,{nsprite=sprite(),ssprite=sprite(),x=x,y=y,call_back=callback}})
  parent:addChild(menu,30)
 end
 ui.returnBack=function()
  local layer=state.main_layer
  state.main_layer=nil;state.chosenEquips={};state.tmpRequest=nil
  state.currentForgeType=nil;state.lastTargetIndex=nil;state.buttons=nil
  pendingNotice=nil;refreshing=false
  if layer then
   pcall(function() layer:stopAllActions();layer:removeFromParentAndCleanup(true) end)
  end
 end
 ui.isNeedUpdateList=function() return true end -- Reopen always queries saved counts.
 ui.show=function(parent)
  if (tonumber(ms.d_mainUI.g_playerInfo.level) or 0)<minimum then query();return end
  if not ui.canJoin() or not catalog[2] then query();return end
  if alive() then ui.returnBack() end
  -- Clear stale native pointers even if another board already destroyed it.
  state.main_layer=nil;state.currentForgeType=nil;state.lastTargetIndex=nil
  state.chosenEquips={};state.tmpRequest=nil
  old.show(parent or ms.d_mainUI.g_mainUI.main_layer)
  if alive() then
   state.main_layer:registerScriptHandler(function(event)
    if event=='exit' then state.main_layer=nil;state.chosenEquips={};state.tmpRequest=nil end
   end)
  end
 end
 ui.updateActivityStatus=function(data)
  local snapshot=data.equip_compose
  if snapshot and weekly and snapshot.weekly_reset_at and snapshot.weekly_reset_at<weekly.weekly_reset_at then return end
  old.updateActivityStatus(data)
  if not data.equip_compose or not ui.canJoin() then return end
  minimum=tonumber(data.equip_compose.min_role_level) or minimum
  if snapshot.weekly_reset_at then weekly=snapshot;refreshing=false end
  catalog={}
  for _,kind in ipairs({2,3}) do
   local all=config.forgeList[kind]
   table.sort(all,function(a,b) return a.equip_type<b.equip_type end)
   if kind==3 then
    all.max_times=math.max(0,tonumber(all.max_times) or 0)
    all.left_times=math.max(0,math.min(all.max_times,tonumber(all.left_times) or 0))
   end
   catalog[kind]=all;page(kind)
  end
 end
 ui.updateForgeList=function(data)
  ui.updateActivityStatus(data)
  if data.show then ui.show()
  elseif alive() then ui.countDown();ui.showForgeMainLayer() end
 end
 ui.showForgeMainLayer=function()
  if not alive() then return end
  local kind=state.currentForgeType
  page(kind)
  local nativeStyle=ms.d_u.createByStyle
  local list=config.forgeList[kind]
  local nativeCount=ms.d_hz.gethz('piece_time')..': '..tostring(list.left_times)..'/'..tostring(list.max_times)
  ms.d_u.createByStyle=function(style,...)
   if weekly and style.string==nativeCount then
    local copy={};for k,v in pairs(style) do copy[k]=v end
    copy.string='本周剩余兑换: '..weekly.weekly_remaining..'/'..weekly.weekly_limit
    style=copy
   end
   return nativeStyle(style,...)
  end
  local ok,err=pcall(old.showForgeMainLayer)
  ms.d_u.createByStyle=nativeStyle
  if not ok then error(err,0) end
  local frame=state.main_layer:getChildByTag(config.tagDef.frameTag)
  local all=catalog[kind]
  if not frame or not all then return end
  if weekly and kind==2 then
   frame:addChild(ms.d_u.createByStyle({type='label',font='arial',fontsize=26,
    string='本周剩余兑换: '..weekly.weekly_remaining..'/'..weekly.weekly_limit,
    x=0.76,y=0.07,color=config.Color.gray}))
  end
  local function change(delta)
   offsets[kind]=math.max(1,math.min((offsets[kind] or 1)+delta,#all-2))
   state.lastTargetIndex=1;state.chosenEquips={};state.tmpRequest=nil
   ui.showForgeMainLayer()
  end
  button(frame,'上一组',0.09,0.9,function() change(-3) end)
  button(frame,'下一组',0.23,0.9,function() change(3) end)
  frame:addChild(ms.d_u.createByStyle({type='label',font='arial',fontsize=18,
   string=offsets[kind]..'—'..math.min(offsets[kind]+2,#all)..' / '..#all,
   x=0.16,y=0.85,color={255,200,80}}))
  if pendingNotice then local notice=pendingNotice;pendingNotice=nil;ms.d_info.show(notice) end
 end
 ui.getForgeResult=function(data)
  if data.compose_type==1 then return old.getForgeResult(data) end
  local snapshot=data.equip_compose
  if snapshot and weekly and snapshot.weekly_reset_at and snapshot.weekly_reset_at<weekly.weekly_reset_at then return end
  if snapshot and snapshot.weekly_reset_at then weekly=snapshot end
  pendingNotice=data.exchange_notice
  local kind=data.compose_type
  local all=catalog[kind]
  -- Keep the real prize count for the native animation/reward popup. That
  -- callback incorrectly subtracts count from left_times (40 shards -> -30).
  local remaining=all and all.left_times
  if kind==3 and all then
   local snapshot=data.equip_compose and data.equip_compose.exchange
   local maximum=snapshot and snapshot.count_limit or all.max_times
   local left=snapshot and maximum-snapshot.exchanged_count or (remaining or 0)-1
   all.left_times=math.max(0,math.min(maximum,left))
   all.max_times=maximum
   local list=config.forgeList[3]
   -- Native subtracts count synchronously, before starting its animation.
   list.left_times=all.left_times+(tonumber(data.count) or 0)
  end
  if alive() then
   local current=config.forgeList[state.currentForgeType]
   local target=current and current[state.lastTargetIndex or 1]
   if target and state.currentForgeType==kind and target.equip_type==data.equip_type then
    old.getForgeResult(data)
   else
    ms.d_commonLayerUI.showPrizeResLayer(state.main_layer,data.attach_list)
    if pendingNotice then ms.d_info.show(pendingNotice);pendingNotice=nil end
   end
  elseif pendingNotice then
   ms.d_info.show(pendingNotice);pendingNotice=nil
  end
  if data.equip_compose then
   ui.updateActivityStatus(data)
  elseif all then -- Older local server during a rolling restart.
   if kind==2 then for _,row in ipairs(all) do if row.equip_type==data.equip_type then row.isForged=true end end end
   page(kind)
  end
 end
 ui.getEquipsByQuality=function(quality)
  local result={}
  -- Preserve original enhancement selection/confirmation (>10); exclude the
  -- locked, worn, ascended or reborn materials rejected by local server policy.
  for _,item in ipairs(old.getEquipsByQuality(quality)) do
   local valid=(item.count or 0)>0
   for _,key in ipairs({'equip_order','owner_id','is_lock','innate_owner_id','protogenic',
     'advance_level','star_count','cur_spirit_count','reborn_bit','star_level'}) do
    local value=item[key]
    if value and value~=0 then valid=false end
   end
   if valid then result[#result+1]=item end
  end
  return result
 end
 -- forge=26 has no funConfig or btn26/pic26/hz26 assets in 3.87. Supply a
 -- labelled entry on the existing activity board instead of missing artwork.
 local fun=ms.d_funUI
 local oldCreate=fun.create
 fun.create=function(...)
  local result=oldCreate(...)
  local layer=fun.g_funUI.main_layer
  if layer then
   layer:removeChildByTag(92601,true)
   local entry=CCLayer:create();layer:addChild(entry,30,92601)
   button(entry,'装备兑换',0.76,0.91,query)
  end
  return result
 end
 ui._localExchangeRestore=function()
  for _,key in ipairs({'show','returnBack','updateForgeList','isNeedUpdateList',
    'updateActivityStatus','getForgeResult','showForgeMainLayer','getEquipsByQuality','canForge','countDown'}) do ui[key]=old[key] end
  fun.create=oldCreate
  if fun.g_funUI and fun.g_funUI.main_layer then fun.g_funUI.main_layer:removeChildByTag(92601,true) end
  ui._localExchangeRestore=nil
 end
 end
end
