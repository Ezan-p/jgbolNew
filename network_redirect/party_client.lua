-- Daily offline party: disable luck and paginate the native fight reward box.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_worldBossUI
 if not ui or not ui.showFightEnd or not ms.d_loginGameUI then return 'pending' end
 if not ui._localPartyRestore then
  local old={checkLuckRank=ui.checkLuckRank,getLuckPointReward=ui.getLuckPointReward,
   getLuckRankRes=ui.getLuckRankRes,showFightEnd=ui.showFightEnd,showAward=ui.showAward}
  local function unavailable() ms.d_info.show('离线模式，暂不开启') end
  ui.checkLuckRank=unavailable;ui.getLuckPointReward=unavailable;ui.getLuckRankRes=unavailable
  local function rewardBox(parent)
   if not parent then return end
   parent:removeChildByTag(95120,true)
   local data=ui.g_realTimeFightInfo or {}
   local prizes=data.fight_prize or {}
   local create=ms.d_loginGameUI.createPrizeBoxBkg
   local layer
   ms.d_loginGameUI.createPrizeBoxBkg=function(target,...)
    layer=target;layer:setTag(95120)
    return create(target,...)
   end
   data.fight_prize={}
   ui.g_currentRoundDamage=ui.g_currentRoundDamage or data.cur_damage or 0
   local ok,err=pcall(old.showFightEnd,parent)
   data.fight_prize=prizes
   ms.d_loginGameUI.createPrizeBoxBkg=create
   if not ok then error(err) end
   if not layer then return end
   local page=1;local pages=math.max(1,math.ceil(#prizes/6))
   local function label(text,x,y,size)
    return ms.d_u.createByStyle({type='label',font='arial',fontsize=size,
     string=text,x=x,y=y,color={255,246,221}})
   end
   local function draw()
    layer:removeChildByTag(95121,true)
    local grid=CCLayer:create();layer:addChild(grid,5,95121)
    local win=CCDirector:sharedDirector():getWinSize()
    for index=(page-1)*6+1,math.min(page*6,#prizes) do
     local row=prizes[index];local cell=(index-1)%6
     local x=0.37+(cell%3)*0.13;local y=0.47-math.floor(cell/3)*0.12
     local icon=ms.d_data.getSmallItemSprite(row.attach_type)
     if icon then
      local size=icon:getContentSize()
      icon:setScale(math.min(win.width*0.12/size.width,win.height*0.075/size.height))
      ms.d_u.setStyles(icon,{x=x,y=y});grid:addChild(icon)
     end
     local attr=ms.d_packageUI.g_itemAttrTable[row.attach_type]
     local text=label((attr and attr.name or '物品')..' ×'..tostring(row.attach_count),x,y-0.043,18)
     local width=text:getContentSize().width
     if width>win.width*0.12 then text:setScale(win.width*0.12/width) end
     grid:addChild(text)
    end
    if #prizes==0 then grid:addChild(label('本次未获得物品',0.5,0.43,24)) end
    if pages>1 then
     grid:addChild(label(page..' / '..pages,0.65,0.54,18))
     for _,step in ipairs({-1,1}) do
      local text=label(step<0 and '上一页' or '下一页',0,0,20)
      local item=CCMenuItemLabel:create(text)
      ms.d_u.setStyles(item,{x=step<0 and 0.35 or 0.65,y=0.25})
      item:registerScriptTapHandler(function() page=(page-1+step+pages)%pages+1;draw() end)
      local menu=CCMenu:createWithItem(item);menu:setPosition(CCPointMake(0,0));grid:addChild(menu)
     end
    end
   end
   draw()
  end
  ui.showFightEnd=function(parent) return rewardBox(parent) end
  -- Also use the same multi-item layout for rewards opened from the event page.
  ui.showAward=function()
   local parent=ui.g_mainLayer
   if ui.g_isInWorldBossStartPage then parent=ui.g_startLayer
   elseif ui.g_isInFightInfoPage then parent=ui.g_fightInfoLayer end
   return rewardBox(parent)
  end
  ui._localPartyRestore=function()
   for key,value in pairs(old) do ui[key]=value end
   ui._localPartyRestore=nil
  end
 end
end
