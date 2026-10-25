local ms=package.loaded.ms;local t=ms.d_trainingUI
if training_level_restore then training_level_restore() end
local original=ms.d_u.main_server_send_msg
training_level_probe={sends={}}
local probe=training_level_probe
ms.d_u.main_server_send_msg=function(mid,d)if mid==1081 or mid==1082 then probe.sends[#probe.sends+1]={mid=mid,data=d} else return original(mid,d) end end
local active=true
training_level_restore=function()if not active then return end;active=false;ms.d_u.main_server_send_msg=original;ms.d_mainUI.g_mainUI.main_layer:removeChildByTag(ms.d_data.getTagFromDef('training'),true);probe.restored=true end
local restore=training_level_restore;local scheduler=CCDirector:sharedDirector():getScheduler();local sid;sid=scheduler:scheduleScriptFunc(function()restore();scheduler:unscheduleScriptEntry(sid)end,60,false)
local c=ms.d_c.table_copy(ms.d_lineupUI.g_characterInfo[1]);c.level=TEST_LEVEL;c.culture_point=30;c.train_change_value=0;c.train_increase_field=0;c.train_decrease_field=0
t.show(c);probe.level=c.level;probe.potential=c.culture_point
return 'level '..c.level..' ready'
