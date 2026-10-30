local source=...
local items,sent,animated={},0,0
local function node()
 local n={parent=true}
 function n:getParent() return self.parent end
 function n:getPositionLua() return {x=80,y=40} end
 function n:setPosition(x,y) self.x=x;self.y=y end
 function n:addChild(child) child.parent=self end
 function n:removeFromParentAndCleanup() self.parent=nil end
 function n:registerScriptTapHandler(fn) self.tap=fn end
 return n
end
CCMenuItemImage={create=function() local item=node();items[#items+1]=item;return item end}
CCMenu={createWithItem=function(_,item) local menu=node();menu.item=item;return menu end}
local ui={g_mapID=1,g_mapStates={[1]={pass_map=0}}}
local prize={}
local ms={d_subLevelUI=ui,d_prizeUI=prize,d_mapUI={g_mapUI={jy_mode=1}}}
package.loaded.ms=ms
ui.createSubLevel=function()
 local bun=node();bun.parent=node()
 ui.g_eatBunsSpriteTable={bunSprite=bun}
 return 'native level'
end
ui.allStarsEat=function(tag) assert(tag==0);sent=sent+1 end
ui.allStarGetBun=function() assert(ui.g_getFullStarPrize);animated=animated+1;ui.g_getFullStarPrize=false end
prize.setPrize=function(data)
 if data.prize_type==3 then ui.g_getFullStarPrize=true end
 return 'native prize'
end
local create,setPrize=ui.createSubLevel,prize.setPrize
assert(loadstring(source))();assert(loadstring(source))()
assert(ui.createSubLevel()=='native level' and #items==0)
ui.g_mapStates[1].pass_map=1
ui.createSubLevel();assert(#items==1 and items[1].x==80 and items[1].y==40)
items[1].tap();assert(sent==1 and animated==0) -- Wait for server confirmation.
items[1].tap();assert(sent==2) -- A rejected request must not permanently disable retry.
local menu=ui.g_eatBunsSpriteTable.claimMenu
ui.g_mapStates[1].pass_map=2
assert(prize.setPrize({prize_type=3})=='native prize')
assert(animated==1 and menu.parent==nil and ui.g_eatBunsSpriteTable.claimMenu==nil)
items[1].tap();assert(sent==2)
ui.createSubLevel();assert(#items==1) -- Claimed chapter uses native taken marker.
ui.g_mapStates[1].pass_map=1
ui.createSubLevel();items[2].tap()
ui.g_mapStates[1].pass_map=2;ui.g_mapID=2
prize.setPrize({prize_type=3});assert(animated==1 and not ui.g_getFullStarPrize)
ui.g_mapID=1;ui.g_mapStates[1].pass_map=1
ui.createSubLevel();items[3].tap()
ui.g_eatBunsSpriteTable.claimMenu.parent=nil
ui.g_mapStates[1].pass_map=2
prize.setPrize({prize_type=3});assert(animated==1 and not ui.g_getFullStarPrize)
ui.g_mapStates[1].pass_map=1
ui.createSubLevel();items[4].tap()
ui.createSubLevel();items[4].tap();assert(sent==5) -- Stale panel cannot send.
ui.g_mapStates[1].pass_map=2
prize.setPrize({prize_type=3});assert(animated==1 and not ui.g_getFullStarPrize)
assert(prize.setPrize({prize_type=1})=='native prize')
ui._localJourneyRestore();assert(ui.createSubLevel==create and prize.setPrize==setPrize)
return 'Journey client: claim button, server confirmation, retries, stale/closed panels, restoration passed'
