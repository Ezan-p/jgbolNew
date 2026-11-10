local calls,refresh=0,0
local ui={g_data={friend_list={{id=712345678}},garden_data={plant_data={{cur_plus_times=0}}}}}
local old=function(op,data)
 calls=calls+1
 if op==26 and data.result==1 and data.upgrade_info then
  -- Native updateScale runs before the wrapper returns.
  assert(ui.g_data.base_data.upgrade_info==data.upgrade_info)
 end
 return 'native'
end
local oldHCJ=function() return 'native ordeal' end
ui.showHCJ=oldHCJ
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
ui.g_read_only=false
ui.g_data.base_data={level=1,upgrade_info={has_passed=true,boss_info={cortege_type=5004}}}
local nextStage={has_passed=false,fight_count=2,boss_info={cortege_type=5009},is_max_scale=false}
ui.onGetResult(26,{result=1,level=2,upgrade_info=nextStage})
assert(ui.g_data.base_data.upgrade_info==nextStage and ui.showHCJ()=='native ordeal')
ui.onGetResult(26,{result=0,upgrade_info={has_passed=true}})
assert(ui.g_data.base_data.upgrade_info==nextStage)
local finalStage={has_passed=false,fight_count=1,boss_info={cortege_type=0},is_max_scale=true}
ui.onGetResult(26,{result=1,level=3,upgrade_info=finalStage})
assert(ui.showHCJ()==nil)
ui._localHomeRestore();assert(ui.onGetResult==old and not ui._localHomeRestore)
assert(ui.showHCJ==oldHCJ)
assert(ui.showHolePlan()=='original home_welfare12' and not ui.hasActivity())
print('home client regression passed')
