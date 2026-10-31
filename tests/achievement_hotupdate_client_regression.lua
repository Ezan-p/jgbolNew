local source,packets=...
local checks={}
local function check(name,fn) fn();checks[#checks+1]=name end
local received,configCalls={},0
local data={g_achieveTable={{id=563,max_repeatable_times=200}}}
data.getAchievementsCSVConfig=function() end
data.callback_update_config=function() configCalls=configCalls+1 end
local ui={g_self={Achieve={},AchieveShow={}},onGetAchieves=function(p) received[#received+1]=p end}
local ms={d_data=data,d_achieveUI=ui};package.loaded.ms=ms
assert(loadstring(source))()
local function apply(packet)
 if packet.mid==1066 then ui.onGetAchieves(packet.data)
 elseif packet.mid==2998 then data.callback_update_config(assert(loadstring('return '..packet.data.data))()) end
end
check('old client receives all 14 catalogue changes exactly once',function()
 local n=0;for _,r in pairs(data.g_achieveTable) do n=n+1 end
 assert(n==14);data.getAchievementsCSVConfig();assert(#data.g_achieveTable==14)
 assert(data.g_achieveTable[1].max_repeatable_times==400)
 assert(data.g_achieveTable[14].id==590 and data.g_achieveTable[14].max_repeatable_times==24)
 assert(data.g_achieveTable[14].full_progress==1 and data.g_achieveTable[14].repeatable)
 assert(ui.g_self.Achieve==nil and ui.g_self.AchieveShow==nil)
end)
check('self 258-entry snapshot reaches native callback atomically',function()
 for i,p in ipairs(packets.initial) do apply(p);if i<#packets.initial then assert(#received==0) end end
 assert(#received==1 and #received[1].achievements==258 and received[1].new==0)
end)
check('other role complete comparison is not overwritten by tail chunk',function()
 for _,p in ipairs(packets.other) do apply(p) end
 assert(#received==2 and received[2].role_id==200 and #received[2].achievements==258)
 assert(received[2].achievements[1].id==101 and received[2].achievements[258].id==590)
end)
check('small incremental update goes through unchanged',function()
 for _,p in ipairs(packets.delta) do apply(p) end
 assert(#received==3 and received[3].new==1 and #received[3].achievements==1)
 assert(received[3].achievements[1].id==590)
end)
check('duplicate first chunk does not prematurely deliver an incomplete snapshot',function()
 for i=1,#packets.initial-1 do apply(packets.initial[i]) end
 apply(packets.initial[#packets.initial-1]);assert(#received==3)
 apply(packets.initial[#packets.initial]);assert(#received==4)
end)
check('new snapshot discards interrupted old batch',function()
 for i=1,#packets.initial-1 do apply(packets.initial[i]) end
 for _,p in ipairs(packets.other) do apply(p) end
 assert(#received==5 and received[5].role_id==200 and #received[5].achievements==258)
end)
check('login config cancels pending batch and unrelated config is preserved',function()
 for i=1,#packets.initial-1 do apply(packets.initial[i]) end
 data.callback_update_config({config_end=true});assert(configCalls==1)
 for _,p in ipairs(packets.delta) do apply(p) end
 assert(#received==6 and #received[6].achievements==1)
 data.callback_update_config({local_fate_rebuild={}});assert(configCalls==2)
end)
check('repeat injection does not wrap twice',function()
 local original=ui.onGetAchieves
 assert(loadstring(source))();assert(original==ui.onGetAchieves)
end)
return checks
