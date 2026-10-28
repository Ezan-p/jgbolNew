-- Run with Lua 5.1/LuaJIT; exercise the actual patched menu callback.
local sent,notices,button={}, {}, nil
local ui={g_data={boss={specter_info={fight_boss_times=0,max_fight_count=5}}}}
local ms={d_abyssUI=ui,d_u={},d_info={show=function(t) notices[#notices+1]=t end},
 d_lineupUI={getCharacterCSVConfig=function(k) assert(k=='specter_boss') end,saveLastFightLevel=function() end}}
package.loaded.ms=ms
ui.sendRequest=function(op,data) sent[#sent+1]=op end
ms.d_u.createMenu=function(config) button=config[1].call_back end
local menu=ms.d_u.createMenu
ui.showBossLayer=function()
 ms.d_u.createMenu({{npic='v2/abyssUI/challenge1.png',call_back=function() error('broken native gate') end}})
end
local native=ui.showBossLayer
dofile('network_redirect/abyss_client.lua')
ui.showBossLayer();assert(ms.d_u.createMenu==menu)
for used=0,5 do
 ui.g_data.boss.specter_info.fight_boss_times=used
 button();assert(sent[#sent]==6) -- Even cached 0/5 must reach server rollover.
end
assert(#sent==6)
ui.g_data.boss.specter_info.complete=true
button();assert(#sent==6 and #notices==1)
ui.g_data={};button();assert(sent[#sent]==16)
ui._localBossRestore();assert(ui.showBossLayer==native)
ui.showBossLayer=function() error('render failure') end
dofile('network_redirect/abyss_client.lua')
assert(not pcall(ui.showBossLayer));assert(ms.d_u.createMenu==menu)
print('abyss client regression OK')
local removed=0
local parent={getChildByTag=function(_,tag) assert(tag==77);return 'old' end,
 removeChild=function(_,child,cleanup) assert(child=='old' and cleanup);removed=removed+1 end}
ui.tagDef={random_layer=77};ui.g_abyssUI={hook_layer=parent};ui.g_data={random={event_type=4}}
ui.showRandomEvent=function(p) assert(p==nil or p==parent);return 'rendered' end
ms.d_yaoshendianUI={getBitFromInt=function(v) return v end}
dofile('network_redirect/abyss_client.lua')
assert(ui.showRandomEvent()=='rendered' and removed==1)
ui.g_data.random.op_type=2;ui.showRandomEvent();assert(removed==1)
ui.g_data.random={event_type=1};ui.showRandomEvent(parent);assert(removed==1)
assert(ms.d_yaoshendianUI.getBitFromInt(-1)==4294967295)
assert(ms.d_yaoshendianUI.getBitFromInt(-2147483648)==2147483648)
assert(ms.d_yaoshendianUI.getBitFromInt(255)==255)
local wrapper=ui.showRandomEvent;dofile('network_redirect/abyss_client.lua');assert(ui.showRandomEvent==wrapper)
ui._localAbyssEventsRestore();ms.d_yaoshendianUI._localAbyssDrugBitsRestore()
print('abyss event redraw and signed recipe flags OK')
