-- The shipped 1263 CSVs already have four-lock prices and current parameters.
-- Its native lock dialog still captures MAX_JP=4. Preserve native callbacks,
-- pricing and validation while including the unlocked fifth slot.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_jpmkUI
 if not ui or not ui.showJPLockLayer or not ui.getCharInfoById then return 'pending' end
 if not debug or not debug.getupvalue or not debug.setupvalue then return 'pending' end
 if not ui._localEssenceHotupdateRestore then
  local original=ui.showJPLockLayer
  local index,previous
  for i=1,64 do
   local name,value=debug.getupvalue(original,i)
   if not name then break end
   if name=='MAX_JP' then index,previous=i,value;break end
  end
  if not index then return 'pending' end
  ui.showJPLockLayer=function(...)
   local character=ui.getCharInfoById(ui.g_self.cort_id)
   local extra=character and character.fate_rebullding_jp_slots or 0
   debug.setupvalue(original,index,extra>=1 and 5 or 4)
   -- Keep the upvalue until the native dialog closes: nested button callbacks
   -- share it, including count, price and the serialized lock_list.
   return original(...)
  end
  ui._localEssenceHotupdateRestore=function()
   ui.showJPLockLayer=original
   debug.setupvalue(original,index,previous)
   ui._localEssenceHotupdateRestore=nil
  end
 end
end
