-- Lua 5.1 adapter regression; also used alongside the original Cocos UI probes.
local player={level=15,pray_spirit_times=0,spirit_retain=80}
local costs,starts,hint={},0,''
local originalConfig={{spirit_coins=200},{spirit_coins=500},{spirit_coins=1000}}
local ui={g_qiFuConsumeConfig=originalConfig}
local original=function()
 starts=starts+1
 local config=ui.g_qiFuConsumeConfig
 local row=config[player.pray_spirit_times or 1] or config[#config]
 costs[#costs+1]=row.spirit_coins
 return 'original-selector'
end
ui.startQiFu=original
package.loaded.ms={d_qiFuUI=ui,d_mainUI={g_playerInfo=player},
 d_info={show=function(text) hint=text end}}
local file=assert(io.open('network_redirect/pray_client.lua'));local source=file:read('*a');file:close()
source=source:gsub('__PRAY_COSTS__','{200,500,1000}')
assert(loadstring(source))()
local wrapped=ui.startQiFu
assert(loadstring(source))()
assert(ui.startQiFu==wrapped,'idempotent install')
for _,count in ipairs({0,1,2,3,100}) do
 player.pray_spirit_times=count
 assert(ui.startQiFu()=='original-selector')
 assert(player.pray_spirit_times==count and player.spirit_retain==80,'no local debit')
end
assert(table.concat(costs,',')=='200,500,1000,1000,1000')
player.level=14;ui.startQiFu()
assert(starts==5 and hint=='神石祈福15级开放')
player.level=15;player.pray_spirit_times=0;ui.startQiFu()
assert(costs[6]==200,'next-day cost resets')
ui._localPrayRestore()
assert(ui.startQiFu==original and ui.g_qiFuConsumeConfig==originalConfig and not ui._localPrayRestore)
print('pray client regression: cost tiers, fallback, level gate, no local debit, restore passed')
