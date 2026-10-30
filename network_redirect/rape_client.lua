-- Native Continue used query flag 1, which only reloaded the cleared board.
-- Flag 4 requests a server-validated next board; ordinary queries stay read-only.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_crossDoomUI
 if not ui then return 'pending' end
 if not ui._localRapeRestore then
  local oldContinue=ui.pressGoOnCard
  local oldInfo=ui.callbackRapeInfo
  local oldHead=ui.createCardHead
  local oldPage,oldHint=ui.createCardPage,ui.setFreeFreshTink
  local oldSweep=ui.showRapeSweepRet
  local oldBackPrize=ui.createBackSkillPrize
  ui.createBackSkillPrize=function(skill_type,name)
   local function valid(value)
    local id=tonumber(value)
    if id and id>0 and id==math.floor(id) then return id end
   end
   local id=valid(skill_type)
   if not id then
    -- Older event 77 responses omitted skill_type. Recover only from the
    -- matching revenge message, before native code creates its touch blocker.
    local result=ui.g_last_rape_fight_ret or {}
    local request=tonumber(result.request_id or ui.g_last_rape_fight_back_id)
    local messages=ms.d_messageUI and ms.d_messageUI.g_fightBackMssage
    for key,row in pairs(messages and messages.rape or {}) do
     if request and tonumber(key)==request then id=valid(row.skill_type);break end
    end
   end
   if not id then
    ms.d_info.show('反击奖励信息不完整，请在背包中查看。')
    return
   end
   return oldBackPrize(id,name)
  end
  local function sweepQuote()
   local state=ui.g_self
   local player=ms.d_mainUI.g_playerInfo
   local card=state.card_data or {}
   local count=0
   for _,board in pairs(card.rape_list or {}) do
    for _,rows in pairs(board.form_list or {}) do
     for _,target in pairs(rows) do
      if not target.has_win then count=count+1 end
     end
    end
   end
   count=math.min(count,math.max(0,tonumber(player.energy) or 0))
   local rate=tonumber(card.sweep_gold_per_fight)
   if rate==nil then rate=(tonumber(player.vip_level) or 0)>=5 and 0 or 1 end
   return count,count*rate,rate
  end
  local function refreshCost()
   local state=ui.g_self
   if not state or not state.card_data or not state.cost_gold_label then return end
   local _,cost,rate=sweepQuote()
   -- Keep the option discoverable below its usage level and after a clear.
   -- A zero quote caused by no energy/targets is not the VIP free privilege.
   state.cost_gold_label:setString(rate==0 and '免费' or tostring(cost)..'元宝')
   if state.main_btns and state.main_btns[2] then
    state.main_btns[2]:setVisible(true)
   end
  end
  local function pressSweep()
   local state=ui.g_self
   if not state or state.cross_doom_btn_busy then return end
   local player=ms.d_mainUI.g_playerInfo
   ms.d_music_mgr.playClickEffect()
   if (tonumber(player.level) or 0)<25 and (tonumber(player.vip_level) or 0)<5 then
    ms.d_info.show('一键渡劫需25级或VIP5');return
   end
   if (tonumber(player.energy) or 0)<=0 then ui.createAddKillPointHint();return end
   local count,cost=sweepQuote()
   refreshCost()
   if count==0 then ms.d_info.show('当前没有敌人可以进行战斗。');return end
   if (tonumber(player.gold_coin) or 0)<cost then
    ms.d_summonUI.needGold(state.cardPage_layer);return
   end
   ms.d_quitUI.createYesNoByStyle(state.main_layer,{string='',txt_styles={
    {type='label',x=0,y=0.11,fontsize=26,string='确定挑战剩余目标？',color={225,207,185}},
    {type='label',x=-0.17,y=-0.02,fontsize=22,string='消耗精力： '..count,
     color={225,237,225},h_align=kCCTextAlignmentLeft,anchor={0,0.5}},
    {type='label',x=-0.17,y=-0.13,fontsize=22,string='消耗元宝： '..cost,
     color={225,237,225},h_align=kCCTextAlignmentLeft,anchor={0,0.5}}
   }},function()
    ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_rape_sweep_request,{})
   end)
  end
  -- pressFightAll is a private closure made by createCardPage, so replace its
  -- menu binding while that page is being built. Always restore the UI helper.
  ui.createCardPage=function(...)
   local createMenu=ms.d_u.createMenu
   ms.d_u.createMenu=function(style,...)
    for _,item in ipairs(style) do
     if item.npic=='v2/crossDoom/fight_all1.png' then item.call_back=pressSweep end
    end
    return createMenu(style,...)
   end
   local ok,result=pcall(oldPage,...)
   ms.d_u.createMenu=createMenu
   if not ok then error(result,0) end
   refreshCost()
   return result
  end
  ui.setFreeFreshTink=function(...)
   local result=oldHint(...)
   refreshCost()
   return result
  end
  ui.showRapeSweepRet=function(data)
   local state=ui.g_self
   local normalized={}
   for k,v in pairs(data) do normalized[k]=v end
   for i,row in ipairs(data) do
    local result={};for k,v in pairs(row) do result[k]=v end
    -- Accept older servers too: zero is truthy in Lua and must be omitted.
    if (tonumber(result.skill_count) or 0)<=0 then
     result.skill_count=nil;result.skill_type=nil
    end
    if row.object_id and state then
     -- Never apply a positional fallback to a different guard if this target
     -- has no avatar (for example while the page is being rebuilt).
     result.index=0
     for tag,entry in pairs(state.cardPage_enmey_map or {}) do
      if math.floor(tag/100)==row.form_index and
       tonumber(entry.id)==tonumber(row.object_id) and
       tonumber(entry.type)==tonumber(row.object_type) then
       result.index=tag%100;break
      end
     end
    end
    normalized[i]=result
   end
   local result=oldSweep(normalized)
   -- Synchronize the data even if an avatar was absent during the animation.
   -- Wins only: failed and unattempted guards remain available to challenge.
   if state and state.card_data then
    for _,row in ipairs(normalized) do
     if row.object_id and row.fight_result>=1 and row.fight_result<=3 then
      local board=(state.card_data.rape_list or {})[row.form_index]
      local rows=board and board.form_list[row.object_type]
      local target=rows and (rows[row.object_id] or rows[tostring(row.object_id)])
      if target then target.has_win=true end
     end
    end
   end
   return result
  end
  -- Native createCardHead only has layouts for 2..6 guards (lines 1751..1775).
  -- Keep its tag, menu and enemy-map contracts for a single centered guard.
  ui.createCardHead=function(card_num,head_list,call_back,is_fast_show)
   if #head_list~=1 then return oldHead(card_num,head_list,call_back,is_fast_show) end
   local state=ui.g_self
   local layer=state.cardPage_layer
   local speed=is_fast_show and 0.01 or 1
   local x,y=(card_num*2-1)/6-0.005,state.h3+state.h5/2
   local tag=card_num*100+1
   ms.d_u.delay(layer,0.1*speed,function()
    local entry=head_list[1]
    local v=entry.v
    local head=ms.d_data.getHeadSprite(v.show_type,v.cortege_layer and v.cortege_layer>0)
    layer:addChild(ms.d_u.setStyle(head,{x=x,y=y,scaleH=state.card_h,tag=tag}),22)
    local frame=ms.d_u.createByStyle({pic='v2/crossDoom/head_frame.png'})
    entry.menu=ms.d_u.createMenu({x=0,y=0,{nsprite=frame,ssprite=frame,
     x=x,y=y,scaleH=state.card_h,tag=tag,opacity=1,call_back=ui.pressFightNpc}})
    entry.head_sprite=head
    entry.x=x*ms.d_u.getW();entry.y=y*ms.d_u.getH()
    state.cardPage_enmey_map[tag]=entry
    layer:addChild(entry.menu,23)
    if v.has_win then ms.d_u.setStyles(head,{color={32,64,64}}) end
   end)
   if call_back then ms.d_u.delay(layer,0.3*speed,call_back) end
  end
  ui.pressGoOnCard=function(...)
   local state=ui.g_self
   if not state or not state.card_data then return oldContinue(...) end
   ms.d_music_mgr.playClickEffect()
   ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_update_rape_info,{flag=4})
  end
  ui.callbackRapeInfo=function(data)
   -- Native callbacks only clear this flag for query responses (update_type=1).
   -- A refreshed board must also clear the prior sweep's completed UI state.
   if data and data.rape_list and ui.g_self then ui.g_self.is_all_pass=false end
   return oldInfo(data)
  end
  ui._localRapeRestore=function()
   ui.pressGoOnCard=oldContinue;ui.callbackRapeInfo=oldInfo
   ui.createCardHead=oldHead
   ui.createCardPage=oldPage;ui.setFreeFreshTink=oldHint
   ui.showRapeSweepRet=oldSweep
   ui.createBackSkillPrize=oldBackPrize
   ui._localRapeRestore=nil
  end
 end
end
