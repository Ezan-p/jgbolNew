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
  local oldHome=ms.d_fightUI.menuHome_private
  local recordMeta={}
  local state={pending_score=0,previous_best=0}
  local fromRank=false
  ms.d_data.callback_update_config=function(data)
   oldConfig(data)
   if data and data.local_rank then state=data.local_rank end
   if data and data.local_rank_records then recordMeta=data.local_rank_records end
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
     ui.requestRankData()
    else return oldClose(...) end
   end
  end
  ms.d_fightUI.menuHome_private=function(...)
   local rankReplay=fromRank and ms.d_event_mgr.getLastFightType()==118
   local result=oldHome(...)
   if rankReplay then
    fromRank=false
    ms.d_activityUI.show()
    ui.requestRankData()
   end
   return result
  end
  ui._localRankRestore=function()
   ms.d_data.callback_update_config=oldConfig;ui.checkHadGetHighestRewards=oldCheck
   ui.addLeftFrameUI=oldLeft;ms.d_fightrecordUI.menuClose=oldClose;ms.d_fightrecordUI.create=oldCreate
   ms.d_fightUI.menuHome_private=oldHome
   ui._localRankRestore=nil;ui._localRankOpenRecords=nil
  end
 end
end
