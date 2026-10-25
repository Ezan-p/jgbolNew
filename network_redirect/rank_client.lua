-- Keep the original rank layout, cards, inspection and replay renderer.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_rankUI
 if not ui or not ms.d_fightrecordUI then return 'pending' end
 if not ui._localRankRestore then
  local oldConfig=ms.d_data.callback_update_config
  local oldCheck=ui.checkHadGetHighestRewards
  local oldLeft=ui.addLeftFrameUI
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
   if data and data.local_rank then state=data.local_rank end
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
   ms.d_data.callback_update_config=oldConfig;ui.checkHadGetHighestRewards=oldCheck
   ui.addLeftFrameUI=oldLeft;ms.d_fightrecordUI.menuClose=oldClose;ms.d_fightrecordUI.create=oldCreate
   ms.d_fightUI.showFightEnd=oldFightEnd;ms.d_fightrecordUI.show=oldRecordShow
   if patchedHome and ms.d_fightUI.menuHome_private==patchedHome then ms.d_fightUI.menuHome_private=nativeHome end
   ms.d_fightrecordUI.play_fightRecord=oldPlay;ui.getDateFormServer=oldRankData
   ui._localRankRestore=nil;ui._localRankOpenRecords=nil
  end
 end
end
