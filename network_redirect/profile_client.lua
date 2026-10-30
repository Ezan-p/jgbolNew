-- Creation chooses the initial portrait; every role has one free replacement.
-- The server sends the remaining entitlement at login and after profile actions.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_runeUI
 if not ui or not ui.showChangeUserHead or not ms.d_data then return 'pending' end
 if not ui._localProfileRestore then
  local show=ui.showChangeUserHead
  ui.showChangeUserHead=function(parent,zorder,tag,use_gold)
   local state=(ms.d_data.g_new_config or {}).local_profile
   if state and state.head_free_available==true then use_gold=false end
   return show(parent,zorder,tag,use_gold)
  end
  ui._localProfileRestore=function()
   ui.showChangeUserHead=show;ui._localProfileRestore=nil
  end
 end
end
