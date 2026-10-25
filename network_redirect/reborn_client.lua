-- The installed release_w ascension list also sorts by fate_rebullding_state.
-- The preserved 3.87 protocol has no such field: absent means not activated.
-- Normalize only missing client fields, before the original filter and sort.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_ascensionUI
 if not ui or type(ui.getAscCorts)~='function' then return 'pending' end
 if not ui._localRebornRestore then
  local original=ui.getAscCorts
  ui.getAscCorts=function(...)
   for _,c in pairs(ms.d_lineupUI.g_characterInfo or {}) do
    if c.fate_rebullding_state==nil then c.fate_rebullding_state=0 end
   end
   return original(...)
  end
  ui._localRebornRestore=function()
   ui.getAscCorts=original
   ui._localRebornRestore=nil
  end
 end
end
