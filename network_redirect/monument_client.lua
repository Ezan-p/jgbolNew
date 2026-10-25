-- Compatibility fixes only; preserve the original monument and record layouts.
do
 local ms=package.loaded.ms
 local m=ms and ms.d_monumentUI
 local r=ms and ms.d_fightrecordUI
 if not m or not r then return 'pending' end
 if not m._localMonumentRestore then
  local receive=m.onGetMonumentData
  local save=r.save_fight_record
  m.onGetMonumentData=function(data)
   -- Recompute switches after configuration/reconnection; original caches once.
   m.g_self.Config=nil
   return receive(data)
  end
  r.save_fight_record=function(records,fightType)
   if fightType==118 then
    -- Original pairs(records) cannot also carry the fight_type scalar it reads.
    -- Clear stale previous-day records, then repair the per-record replay type.
    r.g_fight_record={}
    save(records,fightType)
    for _,record in pairs(r.g_fight_record) do
     record.fightInfo.fight_result_msg.fight_type=fightType
    end
   else return save(records,fightType) end
  end
  m._localMonumentRestore=function()
   m.onGetMonumentData=receive;r.save_fight_record=save
   m._localMonumentRestore=nil
  end
 end
end
