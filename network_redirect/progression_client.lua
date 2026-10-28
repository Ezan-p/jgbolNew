-- Keep the original reward UI and wire requests; refresh its same-day cached data.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_levelUpBuffUI
 local main=ms and ms.d_mainUI
 if not (ui and main and main.levelUpBox) then return 'pending' end
 if not ui._localProgressionRestore then
  local old=ui.showLevelUpBuff
  ui.showLevelUpBuff=function(...)
   ui.g_self.data=nil
   return old(...)
  end
  ui._localProgressionRestore=function()
   ui.showLevelUpBuff=old
   ui._localProgressionRestore=nil
  end
 end
 -- Original playerLevelUp opens a box for each reached level but shares one
 -- prize_list. Select the server's matching list while creating each native box.
 if not main._localProgressionRewardsRestore then
  local oldBox=main.levelUpBox
  main.levelUpBox=function(parent,level,...)
   local info=main.g_playerInfo and main.g_playerInfo.levelUpInfo
   local lists=info and info.gift_lists_by_level
   local gifts=lists and (lists[level] or lists[tostring(level)])
   if not gifts then return oldBox(parent,level,...) end
   local previous=main.levelup_prize
   local oldInfo=ms.d_data.getCertainInfo
   -- The original bytecode has only TWO coordinate entries, despite reserving
   -- table capacity for three. Render a three-column reward row when necessary.
   main.levelup_prize={prize_list=#gifts>2 and {} or gifts}
   -- Native labels only include quantities for gold; show item counts as well.
   ms.d_data.getCertainInfo=function(kind,tid,...)
    local value=oldInfo(kind,tid,...)
    for _,gift in ipairs(gifts) do
     if kind==5 and gift.object_type==kind and gift.attach_type==tid and value then
      local copy={};for k,v in pairs(value) do copy[k]=v end
      copy.name=value.name..' ×'..tostring(gift.attach_count)
      return copy
     end
    end
    return value
   end
   local args={...}
   local ok,result=pcall(function()
    local result=oldBox(parent,level,unpack(args))
    if #gifts>2 then
     local layer=main.g_levelUpLayer
     local size=CCDirector:sharedDirector():getVisibleSize()
     for i,gift in ipairs(gifts) do
      local icon=ms.d_data.getCertainSmallSprite(gift.object_type,gift.attach_type)
      ms.d_u.setStyle(icon,{scale=0.07})
      local x,y=size.width*(0.3+(i-1)*0.2),size.height*0.49
      icon:setPosition(x,y);layer:addChild(icon,5)
      local item=oldInfo(gift.object_type,gift.attach_type)
      local name=gift.object_type==11 and (tostring(gift.attach_count)..item.name)
       or (item.name..' ×'..tostring(gift.attach_count))
      local label=ms.d_u.createByStyle({type='label',font='arial',fontsize=20,string=name})
      label:setPosition(x,y-icon:getContentSize().height*icon:getScale()*0.7)
      layer:addChild(label,5)
     end
    end
    return result
   end)
   ms.d_data.getCertainInfo=oldInfo
   main.levelup_prize=previous
   if not ok then error(result) end
   return result
  end
  main._localProgressionRewardsRestore=function()
   main.levelUpBox=oldBox
   main._localProgressionRewardsRestore=nil
  end
 end
end
