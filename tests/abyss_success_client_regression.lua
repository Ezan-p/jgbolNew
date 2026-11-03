-- Native abyssUI L2353-2411 lifecycle: delay, reward names, then close handler.
local delayed,labels,closed,touch
local ui={showBossLayer=function() end,sendRequest=function() error('unexpected request') end}
local ms={d_abyssUI=ui,d_u={},d_data={}}
package.loaded.ms=ms;d_ms=ms
ms.d_u.delay=function(_,seconds,fn) assert(seconds==.75);delayed=fn end
ms.d_data.getCertainSmallSprite=function() return {} end
ms.d_data.getItemName=function(id)
 assert(id~=0,'currency ID is not an item')
 return '道具'..id
end
local itemName,sprite=ms.d_data.getItemName,ms.d_data.getCertainSmallSprite
ui.showChallengeSuccess=function(parent)
 assert(parent=='boss layer','render failure')
 closed=false;touch=nil;labels={}
 d_ms.d_u.delay(parent,.75,function()
  for _,prize in ipairs(ui.g_data.boss.prize_list) do
   d_ms.d_data.getCertainSmallSprite(prize.object_type,prize.attach_type,1)
   labels[#labels+1]=d_ms.d_data.getItemName(prize.attach_type)..'X'..prize.attach_count
  end
  touch=function() closed=true end
 end)
end
local native=ui.showChallengeSuccess
local env=getfenv(native)
ui.g_data={boss={specter_info={boss_layer=2},prize_list={
 {object_type=5,attach_type=1441,attach_count=10},
 {object_type=12,attach_type=0,attach_count=120000}}}}
native('boss layer')
assert(not pcall(delayed) and touch==nil and not closed,'must reproduce the stuck mask')
dofile('network_redirect/abyss_client.lua')
local wrapper=ui.showChallengeSuccess
dofile('network_redirect/abyss_client.lua');assert(ui.showChallengeSuccess==wrapper)
ui.showChallengeSuccess('boss layer')
assert(getfenv(native)==env and touch==nil)
assert(ms.d_data.getItemName==itemName and ms.d_data.getCertainSmallSprite==sprite)
assert(not pcall(itemName,0),'other screens must retain native item validation')
delayed()
assert(labels[1]=='道具1441X10' and labels[2]=='银币X120000')
assert(touch and not closed);touch()
assert(closed and ui.g_data.boss.specter_info.boss_layer==2)
-- Currency type must reset before the following normal item, even on floor 81.
ui.g_data.boss.specter_info={boss_layer=81,complete=true}
ui.g_data.boss.prize_list={
 {object_type=11,attach_type=0,attach_count=5},
 {object_type=5,attach_type=1431,attach_count=1}}
ui.showChallengeSuccess('boss layer');delayed();touch()
assert(labels[1]=='元宝X5' and labels[2]=='道具1431X1' and closed)
ui.g_data.boss.prize_list={}
ui.showChallengeSuccess('boss layer');delayed();touch();assert(closed)
assert(not pcall(ui.showChallengeSuccess,'bad parent') and getfenv(native)==env)
ui._localAbyssSuccessRestore();assert(ui.showChallengeSuccess==native)
print('abyss success regression OK: stuck-mask reproduction, delayed currency rendering, close callback, next floor, final floor, environment restore')
