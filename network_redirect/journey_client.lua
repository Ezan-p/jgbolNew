-- Native 3.87 renders a plain bun sprite for pass_map=1, but never binds
-- allStarsEat. Restore that entry while keeping server-side reward validation.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_subLevelUI
 local prize=ms and ms.d_prizeUI
 if not ui or not ui.createSubLevel or not prize or not prize.setPrize then return 'pending' end
 if not ui._localJourneyRestore then
  local create,setPrize=ui.createSubLevel,prize.setPrize
  local pending
  ui.createSubLevel=function(...)
   local result=create(...)
   local mid=ui.g_mapID
   local state=ui.g_mapStates and ui.g_mapStates[mid]
   local sprites=ui.g_eatBunsSpriteTable
   local bun=sprites and sprites.bunSprite
   if state and state.pass_map==1 and bun and bun:getParent() then
    local item=CCMenuItemImage:create('v2/subLevelUI/bun.png','v2/subLevelUI/bun.png')
    local pos=bun:getPositionLua()
    item:setPosition(pos.x,pos.y)
    local menu=CCMenu:createWithItem(item)
    menu:setPosition(0,0)
    bun:getParent():addChild(menu,6)
    sprites.claimMenu=menu
    item:registerScriptTapHandler(function()
     local current=ui.g_mapStates and ui.g_mapStates[mid]
     if ui.g_mapID~=mid or ui.g_eatBunsSpriteTable~=sprites
         or not current or current.pass_map~=1 then return end
     pending={mid=mid,sprites=sprites,menu=menu}
     ui.allStarsEat(0)
    end)
   end
   return result
  end
  prize.setPrize=function(data,...)
   local result=setPrize(data,...)
   if data.prize_type==3 and pending then
    local claim=pending;pending=nil
    local state=ui.g_mapStates and ui.g_mapStates[claim.mid]
    local map=ms.d_mapUI and ms.d_mapUI.g_mapUI
    if state and state.pass_map>1 and ui.g_mapID==claim.mid
        and ui.g_eatBunsSpriteTable==claim.sprites and map and map.jy_mode==1 then
     local ok,parent=pcall(function() return claim.menu:getParent() end)
     if ok and parent then
      claim.menu:removeFromParentAndCleanup(true)
      claim.sprites.claimMenu=nil
      ui.allStarGetBun()
      return result
     end
    end
    -- A response may arrive after the player closes or changes the chapter.
    ui.g_getFullStarPrize=false
   end
   return result
  end
  ui._localJourneyRestore=function()
   ui.createSubLevel=create;prize.setPrize=setPrize;ui._localJourneyRestore=nil
  end
 end
end
