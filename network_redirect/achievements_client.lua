-- [B] Assemble byte-sized wire chunks before the native other-role handler
-- replaces its comparison table. Original 1263 still uses a uint8 count.
do
 local ms=package.loaded.ms
 local data=ms and ms.d_data
 local ui=ms and ms.d_achieveUI
 if not data or not ui or not ui.onGetAchieves or not data.getAchievementsCSVConfig
  or not data.callback_update_config then return 'pending' end
 if not ms._localAchievementRestore then
  local changes=__ACHIEVEMENT_ROWS__
  local oldConfig=data.getAchievementsCSVConfig
  local oldCallback=data.callback_update_config
  local oldReceive=ui.onGetAchieves
  local pending
  local function catalog()
   oldConfig()
   local byId={}
   for _,row in pairs(data.g_achieveTable) do byId[row.id]=row end
   for _,row in ipairs(changes) do
    local dest=byId[row.id]
    if not dest then dest={};data.g_achieveTable[#data.g_achieveTable+1]=dest end
    for k,v in pairs(row) do dest[k]=v end
   end
  end
  data.getAchievementsCSVConfig=catalog
  catalog()
  -- Rebuild cached presentation rows against the amended CSV. The bootstrap
  -- snapshot supplies current progress; no resource or persistent save is touched.
  ui.g_self.Achieve=nil;ui.g_self.AchieveShow=nil
  data.callback_update_config=function(config)
   if config and config.local_achievement_batch then
    local batch=config.local_achievement_batch
    pending={role_id=batch.role_id,new=batch.new,count=batch.count,rows={},seen={}}
    return
   end
   if config and config.config_end then pending=nil end
   return oldCallback(config)
  end
  ui.onGetAchieves=function(packet)
   if not packet then return oldReceive(packet) end
   if pending then
    if packet.role_id~=pending.role_id or packet.new~=pending.new then
     pending=nil
     return oldReceive(packet)
    end
    for _,row in ipairs(packet.achievements or {}) do
     if not pending.seen[row.id] then
      pending.seen[row.id]=true;pending.rows[#pending.rows+1]=row
     end
    end
    if #pending.rows<pending.count then return end
    local complete={}
    for k,v in pairs(packet) do complete[k]=v end
    complete.achievements=pending.rows;complete.achievement_count=#pending.rows
    pending=nil
    return oldReceive(complete)
   end
   return oldReceive(packet)
  end
  ms._localAchievementRestore=function()
   data.getAchievementsCSVConfig=oldConfig;data.callback_update_config=oldCallback
   ui.onGetAchieves=oldReceive;ms._localAchievementRestore=nil
  end
 end
end
