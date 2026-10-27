-- Keep the original reward UI and wire requests; refresh its same-day cached data.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_levelUpBuffUI
 if not ui then return 'pending' end
 if not ui._localProgressionRestore then
  local old=ui.showLevelUpBuff
  ui.showLevelUpBuff=function(...)
   ui.g_self.data=nil
   return old(...)
  end
  ui._localProgressionRestore=function()
   ui.showLevelUpBuff=old
   ui._localProgressionRestore=nil
  end
 end
end
