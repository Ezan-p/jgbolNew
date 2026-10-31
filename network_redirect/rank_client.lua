-- Keep the original rank layout, cards, inspection and replay renderer.
-- Reuse the native quantity picker and inventory-result refresh for tokens.
do
 local ms=package.loaded.ms
 local bag=ms and ms.d_packageUI
 local common=ms and ms.d_commonLayerUI
 if bag and common and ms.d_data and ms.d_data.createBatchUse and not bag._localRankTokenRestore then
  local oldUse,oldResult=bag.requestUseItem,common.recvUsedItem
  bag.requestUseItem=function(item,...)
   if not item or item.type_id~=1021 or (item.count or 0)<=1 then return oldUse(item,...) end
   local maximum=math.min(100,item.count)
   ms.d_data.createBatchUse(ms.d_mainUI.g_mainUI.main_layer,{min=1,max=maximum},function(count)
    if type(count)~='number' or count~=math.floor(count) or count<1 or count>maximum then return end
    bag.g_lastRequestUsedItem.item=item
    bag.g_lastRequestUsedItem.count=count
    ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_use_item,{
     item_type=1021,item_id=item.id or bag.getPropIDByTypeId(1021),
     des_type=ms.d_common_def.object_type.role,des_id=0,item_count=count})
   end)
  end
  common.recvUsedItem=function(data,...)
   if not data or data.type_id~=1021 then return oldResult(data,...) end
   local oldHz=ms.d_hz.gethz
   ms.d_hz.gethz=function(key,...)
    if key=='congrasFengShen' then
     if data.result~=1 then return '封神令牌使用失败' end
     return string.format('使用%d枚封神令牌，增加%d次封神榜挑战机会',data.count or 1,data.effect_value or 3*(data.count or 1))
    end
    return oldHz(key,...)
   end
   local ok,result=pcall(oldResult,data,...)
   ms.d_hz.gethz=oldHz
   if not ok then error(result) end
   return result
  end
  bag._localRankTokenRestore=function()
   bag.requestUseItem=oldUse;common.recvUsedItem=oldResult;bag._localRankTokenRestore=nil
  end
 end
end
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_rankUI
 if not ui or not ms.d_fightrecordUI then return 'pending' end
 if not ui._localRankRestore then
  local oldExchange,oldScores=ms.d_data.g_topScoreExchangeTable,ms.d_data.g_topScoreTable
  local oldHz=ms.d_hz.gethz
  local oldCross,oldCrossFrom=ui.requestCrossRank,ui.requestCrossRankFromRank
  local cross=ms.d_crossRankUI
  local oldCrossShow=cross and cross.show
  local oldCredits=ui.getCreditsRewards
  ms.d_data.g_topScoreExchangeTable=__RANK_EXCHANGES__
  ms.d_data.g_topScoreTable=__RANK_DAILY_SCORES__
  local text={
   fengshenbang_rank_credits_tip='（每日零点刷新一次）',
   fengshenbang_rank_credits_speed='日积分: %d',
   fengshenbang_rank_rewards_tip='每日零点自动入账\n按昨日最高排名结算',
   fengshenbang_rank_newx_rewards='下次结算时间',
   fengshenbang_rank_can_rewards='日积分自动入账',
   crossRankCannotJoin='离线模式，暂未开启'
  }
  ms.d_hz.gethz=function(key,...)
   if text[key] then return text[key] end
   return oldHz(key,...)
  end
  local function closed() return ms.d_info.show('离线模式，暂未开启') end
  ui.requestCrossRank=closed;ui.requestCrossRankFromRank=closed
  if cross then cross.show=closed end
  ui.getCreditsRewards=function() return ms.d_info.show('排名日积分每日零点自动入账') end
  local oldCell,oldLabel=ui.createChargeCell,ui.update_label_state
  local oldClaim,oldClaimResult=ui.chargeButtonCallBack,ui.recvCreditsChargeMsg
  local oldPromotion,oldTimeBit,oldPrizeBit=ui.is_promotion_prize,ui.get_promotion_time_bit,ui.get_promotion_prize_bit
  local oldCheckCredits=ui.checkCreditsToCharge
  -- Display positions are independent of persisted exchange/claim IDs.
  ui.is_promotion_prize=function(index)
   local row=ms.d_data.g_topScoreExchangeTable[index]
   return row and row.promoteOrder>0 or false
  end
  ui.get_promotion_time_bit=function(index)
   local row=ms.d_data.g_topScoreExchangeTable[index]
   return row and row.promoteOrder>0 and oldTimeBit(row.exchangeIndex) or 0
  end
  ui.get_promotion_prize_bit=function(index)
   local row=ms.d_data.g_topScoreExchangeTable[index]
   return row and row.promoteOrder>0 and oldPrizeBit(row.exchangeIndex) or 0
  end
  ui.checkCreditsToCharge=function(index)
   local row=ms.d_data.g_topScoreExchangeTable[index]
   if row and row.costItem>0 then return ms.d_data.getItemCountByType(5,row.costItem)<row.costCount end
   return oldCheckCredits(index)
  end
  -- Native rankUI hardcodes peaches for every row except index 3. Keep its
  -- layout, but supply the real gold icon/name while constructing gold rows.
  ui.createChargeCell=function(index,y,row)
   if row.object_type~=11 and row.sub_type~=1343 then return oldCell(index,y,row) end
   local gold=row.object_type==11
   local function rewardSprite()
    if gold then return CCSprite:create('v2/money_gold.png') end
    return ms.d_data.getSingleSpriteFromPng('items/all_daoju3.png',8,8,47)
   end
   local env=getfenv(oldCell)
   local spriteIndex,sprite
   for i=1,100 do
    local name,value=debug.getupvalue(oldCell,i)
    if not name then break end
    if name=='CCSprite' then spriteIndex=i;sprite=value;break end
   end
   assert(spriteIndex,'rank reward sprite factory missing')
   local proxy=setmetatable({create=function(_,path,...)
    if path=='v2/rankUI/peach.png' then return rewardSprite() end
    return sprite.create(sprite,path,...)
   end},{__index=sprite})
   local hz=setmetatable({gethz=function(key,...)
    if key=='peachHZ' or key=='peachHZZ' then return gold and '元宝' or '圣母蟠桃' end
    if key=='countHZ' then return '' end
    return ms.d_hz.gethz(key,...)
   end},{__index=ms.d_hz})
   local utilities=setmetatable({setProperties=function(parent,node,style,...)
    if (style.scaleH==0.6 and style.x==0.134) or (style.scaleH==0.81 and style.x==0.132) then
     local fitted={};for key,value in pairs(style) do fitted[key]=value end
     fitted.scaleH=gold and 0.42 or 0.81
     return ms.d_u.setProperties(parent,node,fitted,...)
    end
    return ms.d_u.setProperties(parent,node,style,...)
   end},{__index=ms.d_u})
   local data=setmetatable({getSingleSpriteFromPng=function(path,...)
    if path=='items/all_daoju3.png' then return rewardSprite() end
    return ms.d_data.getSingleSpriteFromPng(path,...)
   end},{__index=ms.d_data})
   local function intro()
    if gold then ms.d_info.show('元宝：可用于游戏内购买与养成') else env.showPeachIntro2() end
   end
   setfenv(oldCell,setmetatable({d_ms=setmetatable({d_hz=hz,d_u=utilities,d_data=data},{__index=ms}),
    showPeachIntro=intro,showPeachIntro2=intro},
    {__index=env,__newindex=env}))
   debug.setupvalue(oldCell,spriteIndex,proxy)
   -- Native construction uses score==0 to choose a promotion button.
   local actualScore=row.score
   if row.costItem>0 then row.score=row.costCount end
   local ok,result=pcall(oldCell,index,y,row)
   row.score=actualScore
   debug.setupvalue(oldCell,spriteIndex,sprite);setfenv(oldCell,env)
   if not ok then error(result,0) end
   return result
  end
  local function canClaim(index)
   return ui.get_promotion_time_bit(index)==1 and ui.get_promotion_prize_bit(index)~=1
  end
  ui.update_label_state=function(index)
   local row=ms.d_data.g_topScoreExchangeTable[index]
   local labels=ui.g_isInChangePage and ui.g_label_info and ui.g_label_info[index]
   if row and row.costItem>0 and labels then
    local enabled=not ui.checkCreditsToCharge(index)
    labels.btn:setVisible(enabled);labels.btn:setEnabled(enabled)
    labels.btn2:setVisible(not enabled);labels.btn2:setEnabled(false)
    labels.text:setString('需蟠桃: '..row.costCount)
    return
   end
   oldLabel(index)
   local row=ms.d_data.g_topScoreExchangeTable[index]
   local labels=ui.g_isInChangePage and ui.g_label_info and ui.g_label_info[index]
   if not row or row.promoteOrder<=0 or not labels then return end
   local enabled=canClaim(index)
   labels.btn:setVisible(enabled);labels.btn:setEnabled(enabled)
   labels.btn2:setVisible(not enabled);labels.btn2:setEnabled(false)
   labels.numlabel:setVisible(enabled);labels.countBkg:setVisible(enabled)
   labels.btn_tip:setVisible(false)
   local claimed=ui.get_promotion_prize_bit(index)==1
   if claimed and not labels.claimed_background then
    -- The native disabled texture contains the word "领取". Cover it with
    -- a text-free native button skin so the claimed state is unambiguous.
    local size=labels.btn2:getContentSize()
    local background=CCSprite:create('v2/crossServerUI/btn_bkg.png')
    local original=background:getContentSize()
    background:setScaleX(size.width/original.width);background:setScaleY(size.height/original.height)
    background:setMaskEff('v2/gray.shader');background:setPosition(ccp(size.width/2,size.height/2))
    labels.btn2:addChild(background,100)
    local label=CCLabelTTF:create('已领取','arial',30)
    label:setColor(ccc3(190,190,190));label:setPosition(ccp(size.width/2,size.height/2))
    labels.btn2:addChild(label,101)
    labels.claimed_background=background;labels.claimed_text=label
   end
   if labels.claimed_background then
    labels.claimed_background:setVisible(claimed);labels.claimed_text:setVisible(claimed)
   end
  end
  ui.chargeButtonCallBack=function(index,...)
   local row=ms.d_data.g_topScoreExchangeTable[index]
   if not row then return end
   if row.promoteOrder>0 then
    if not canClaim(index) then return end
   elseif ui.checkCreditsToCharge(index) then
    return ms.d_info.show(row.costItem>0 and '蟠桃不足' or '积分不足')
   end
   return ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_exchange_top_score,{exchange_type=row.exchangeIndex})
  end
  ui.recvCreditsChargeMsg=function(prizes)
   if not prizes or not next(prizes) then return end
   if ui.g_rankUI and ui.g_isInChangePage then ui.updateSelfScore() end
   ms.d_commonLayerUI.showPrizeResLayer(CCDirector:sharedDirector():getRunningScene(),prizes)
  end
  local oldConfig=ms.d_data.callback_update_config
  local oldCheck=ui.checkHadGetHighestRewards
  local oldLeft=ui.addLeftFrameUI
  local oldPage,oldFlash=ui.createRankPage,ui.flashRankUI
  local function hideDailyClaim()
   local labels=ui.g_rankUI and ui.g_rankUI.show_labels
   if labels and labels.top_day_rewards_button then labels.top_day_rewards_button:setVisible(false) end
  end
  ui.createRankPage=function(...)
   local result=oldPage(...);hideDailyClaim();return result
  end
  ui.flashRankUI=function(...)
   local result=oldFlash(...);hideDailyClaim();return result
  end
  local oldClose=ms.d_fightrecordUI.menuClose
  local oldCreate=ms.d_fightrecordUI.create
  local oldFightEnd=ms.d_fightUI.showFightEnd
  local oldRecordShow=ms.d_fightrecordUI.show
  local nativeHome,patchedHome
  local oldPlay=ms.d_fightrecordUI.play_fightRecord
  local oldRankData=ui.getDateFormServer
  local recordMeta={}
  local state={pending_score=0,previous_best=0}
  local fromRank=false
  local replayFromRank=false
  local awaitingBoard=false
  local function returnToRank()
   ms.d_activityUI.show()
   ui.showRankUI()
   awaitingBoard=true
   ui.requestRankData()
  end
  ui.getDateFormServer=function(data)
   oldRankData(data)
   if awaitingBoard then awaitingBoard=false;ui.showRankUI() end
  end
  ms.d_data.callback_update_config=function(data)
   oldConfig(data)
   if data and data.local_rank then
    state=data.local_rank
    if ui.g_rankInfo then
     if state.score then ui.g_rankInfo.self_score=state.score end
     if state.promote_time then ui.g_rankInfo.promote_time=state.promote_time end
     if state.promote_prize then ui.g_rankInfo.promote_prize=state.promote_prize end
    end
    local login,act=ms.d_loginUI,ms.d_activityUI
    if ui.g_rankUI and ui.g_rankInfo and ui.g_isInRankPage
       and login.g_currentSence==login.senceID.adventure
       and act.g_currentActivity==act.activityID.fengshenbang then
     ui.updateSelfScore();hideDailyClaim()
     local labels=ui.g_rankUI.show_labels
     if labels and labels.rank_credits_label then
      labels.rank_credits_label:setString('封神榜积分 : '..tostring(state.score or 0))
     end
     if labels and labels.rank_highest_label then
      labels.rank_highest_label:setString('昨日最高排名 : '..((state.previous_best or 0)>0 and tostring(state.previous_best) or '未结算'))
     end
    end
   end
   if data and data.local_rank_records then recordMeta=data.local_rank_records end
   if data and data.local_rank_show_records then
    fromRank=true
    ms.d_fightrecordUI.show(ui.g_rankUI.rank_layer)
   end
  end
  ui.checkHadGetHighestRewards=function() return (state.pending_score or 0)<=0 end
  ui.addLeftFrameUI=function(parent)
   oldLeft(parent)
   local labels=ui.g_rankUI and ui.g_rankUI.show_labels
   if labels and labels.top_day_rewards_button then labels.top_day_rewards_button:setVisible(false) end
   if labels and labels.rank_highest_label then
    labels.rank_highest_label:setString('昨日最高排名 : '..((state.previous_best or 0)>0 and tostring(state.previous_best) or '未结算'))
   end
   local label=CCLabelTTF:create('战报 / 防守', 'arial', 26)
   label:setColor(ccc3(255,210,120))
   local item=CCMenuItemLabel:create(label)
   ui._localRankOpenRecords=function()
    fromRank=true
    ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_query_fight_record,{fight_type=2})
   end
   item:registerScriptTapHandler(ui._localRankOpenRecords)
   local menu=CCMenu:createWithItem(item);ms.d_u.setProperties(parent,menu,{x=0.2171875,y=0.19});parent:addChild(menu)
   local hint=CCLabelTTF:create('每日一次防守 · 败给身后对手会降名次', 'arial', 17)
   ms.d_u.setProperties(parent,hint,{x=0.2171875,y=0.64});parent:addChild(hint)
  end
  ms.d_fightrecordUI.show=function(parent)
   if fromRank and ms.d_fightrecordUI.g_self.main_layer then oldClose() end
   return oldRecordShow(parent)
  end
  ms.d_fightrecordUI.create=function()
   if not fromRank then return oldCreate() end
   for i,v in pairs(recordMeta) do
    local row=ms.d_fightrecordUI.g_fight_record[i]
    if row then row.rolename=v.label;row.fightpower=v.power;row.vip=0;row.dao=0 end
   end
   local gethz=ms.d_hz.gethz
   ms.d_hz.gethz=function(key,...)
    if key=='fight_record_unavaible' then return '封神榜：挑战与每日防守记录' end
    if key=='fight_record_only_5records' then return '保存最近5场，回放不消耗次数' end
    return gethz(key,...)
   end
   local ok,err=pcall(oldCreate)
   ms.d_hz.gethz=gethz
   if not ok then error(err) end
  end
  -- The existing record screen uses type 118; return to the originating page.
  if type(oldClose)=='function' then
   ms.d_fightrecordUI.menuClose=function(...)
    if fromRank then
     fromRank=false
     oldClose(...)
     returnToRank()
    else return oldClose(...) end
   end
  end
  ms.d_fightrecordUI.play_fightRecord=function(...)
   if fromRank then replayFromRank=true;fromRank=false end
   return oldPlay(...)
  end
  -- Original showFightEnd recreates its home callback for every fight.
  ms.d_fightUI.showFightEnd=function(...)
   local result=oldFightEnd(...)
   if replayFromRank then
    nativeHome=ms.d_fightUI.menuHome_private
    local home=nativeHome
    patchedHome=function(...)
     replayFromRank=false
     local value=home(...)
     returnToRank()
     return value
    end
    ms.d_fightUI.menuHome_private=patchedHome
   end
   return result
  end
  ui._localRankRestore=function()
   if ms.d_packageUI and ms.d_packageUI._localRankTokenRestore then ms.d_packageUI._localRankTokenRestore() end
   ms.d_data.g_topScoreExchangeTable=oldExchange;ms.d_data.g_topScoreTable=oldScores
   ms.d_hz.gethz=oldHz
   ui.requestCrossRank=oldCross;ui.requestCrossRankFromRank=oldCrossFrom
   if cross then cross.show=oldCrossShow end
   ui.getCreditsRewards=oldCredits
   ui.createChargeCell=oldCell;ui.update_label_state=oldLabel
   ui.chargeButtonCallBack=oldClaim;ui.recvCreditsChargeMsg=oldClaimResult
   ui.is_promotion_prize=oldPromotion;ui.get_promotion_time_bit=oldTimeBit;ui.get_promotion_prize_bit=oldPrizeBit
   ui.checkCreditsToCharge=oldCheckCredits
   ms.d_data.callback_update_config=oldConfig;ui.checkHadGetHighestRewards=oldCheck
   ui.createRankPage=oldPage;ui.flashRankUI=oldFlash
   ui.addLeftFrameUI=oldLeft;ms.d_fightrecordUI.menuClose=oldClose;ms.d_fightrecordUI.create=oldCreate
   ms.d_fightUI.showFightEnd=oldFightEnd;ms.d_fightrecordUI.show=oldRecordShow
   if patchedHome and ms.d_fightUI.menuHome_private==patchedHome then ms.d_fightUI.menuHome_private=nativeHome end
   ms.d_fightrecordUI.play_fightRecord=oldPlay;ui.getDateFormServer=oldRankData
   ui._localRankRestore=nil;ui._localRankOpenRecords=nil
  end
 end
end
