local calls,refresh=0,0
local ui={g_data={friend_list={{id=712345678}},garden_data={plant_data={{cur_plus_times=0}}}}}
local old=function() calls=calls+1; return 'native' end
ui.hasActivity=function() return false end
local gethz=function(key) return 'original '..key end
ui.showHolePlan=function() return gethz('home_welfare12') end
ui.onGetResult=old;ui.getRestDay=function() return 'original' end
ui.refreshWelfare=function(kind) assert(kind==69);refresh=refresh+1 end
package.loaded.ms={d_homeUI=ui}
dofile('network_redirect/home_client.lua')
local wrapped=ui.onGetResult
dofile('network_redirect/home_client.lua');assert(wrapped==ui.onGetResult)
assert(not ui.hasActivity())
ui.g_data.config_data={offline_home=true,activity_flag={[72]=false}}
assert(ui.hasActivity())
assert(ui.showHolePlan()=='豪华度达标即可领取，已领档位不会重复发放')
assert(ui.getRestDay(72)=='长期开放' and ui.getRestDay(71)=='original')
assert(ui.onGetResult(5,{result=1,friend_id=712345678,plants_plus_time={2}})=='native')
assert(ui.g_data.friend_list[1].has_invited and ui.g_data.garden_data.plant_data[1].cur_plus_times==2)
ui.g_read_only=true
ui.onGetResult(5,{result=1,friend_id=712345678,plants_plus_time={5}})
assert(ui.g_data.garden_data.plant_data[1].cur_plus_times==2)
ui.onGetResult(24,{result=1,flag=2,act_type=69,all_activity={[69]={total_gold=0}}})
assert(ui.g_data.all_activity[69].total_gold==0 and refresh==1)
ui._localHomeRestore();assert(ui.onGetResult==old and not ui._localHomeRestore)
assert(ui.showHolePlan()=='original home_welfare12' and not ui.hasActivity())
print('home client regression passed')
