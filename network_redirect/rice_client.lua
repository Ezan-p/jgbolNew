-- Native Dragon Boat recipes, permanent entry and independent personal progress.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_ricePuddingUI
 if not ui or not ms.d_hz or not ms.d_u or not ms.d_commonLayerUI or not ms.d_data or not ms.d_data.createBatchUse or not ms.d_packageUI then return 'pending' end
 if not ui._localRiceRestore then
  local old={}
  for _,key in ipairs({'updateActivityStatus','canJoin','tickTime','create','cook','showNews','onGetResult'}) do old[key]=ui[key] end
  local hz=ms.d_hz.gethz
  local usedItem=ms.d_commonLayerUI.recvUsedItem
  local enabled=__RICE_ENABLED__
__SEASONAL_CRAFT_HELPER__
  local originalEnd=ui.g_self.end_time
  local progress={rice_count=0,left_process=__RICE_BONUS_EVERY__}
  local labels={
   rice1='每累计制作__RICE_BONUS_EVERY__个粽子，额外领取蟠桃×__RICE_BONUS_COUNT__',
   rice2='旅途、天命胜利及蟠桃会挑战均可随机获得材料',
   rice3='制作了',rice4='获得'
  }
  ms.d_hz.gethz=function(key,...) return labels[key] or hz(key,...) end
  ms.d_commonLayerUI.recvUsedItem=function(data,...)
   -- The shipped callback has a mooncake branch but no zongzi result branch.
   if data and data.type_id and data.type_id>=1213 and data.type_id<=1217 and data.result==1 then
    ms.d_packageUI.updateItemCellInfo(data.type_id)
    if data.attach_list and #data.attach_list>0 then
     ms.d_commonLayerUI.showPrizeResLayer(CCDirector:sharedDirector():getRunningScene(),data.attach_list)
    end
    return
   end
   return usedItem(data,...)
  end
  ui.updateActivityStatus=function(data,...)
   updateCraft(data)
   if data and data.local_permanent then enabled=data.local_enabled end
   if data and data.rice_count then progress=data end
   local result=old.updateActivityStatus(data,...)
   originalEnd=ui.g_self.end_time;ui.g_self.end_time=enabled and math.huge or 0
   ui.tickTime();ui.showNews()
   return result
  end
  ui.onGetResult=function(data,...)
   updateCraft(data)
   if data and data.local_rice_progress then progress=data.local_rice_progress end
   return old.onGetResult(data,...)
  end
  ui.canJoin=function() return enabled end
  ui.cook=function(index)
   return craftBatch(index,'rice',ui.g_ricePuddingUI)
  end
  ui.tickTime=function()
   local layer=ui.g_ricePuddingUI and ui.g_ricePuddingUI.main_layer
   if not layer then return end
   layer:removeChildByTag(ui.g_self.timeTag,true)
   layer:addChild(ms.d_u.createByStyles({type='label',font='arial',fontsize=28,
    x=ui.g_self.mx,y=ui.g_self.my+ui.g_self.h*0.46,
    string=enabled and '常驻开放' or '暂未开放',color={255,255,255}}),1,ui.g_self.timeTag)
  end
  ui.create=function(...)
   local create=ms.d_u.createByStyles
   ms.d_u.createByStyles=function(styles,...)
    local node=create(styles,...)
    if styles.pic=='v2/ricePuddingUI/time.png' then node:setVisible(false) end
    return node
   end
   local ok,result=pcall(old.create,...)
   ms.d_u.createByStyles=create
   if not ok then error(result) end
   return result
  end
  ui.showNews=function()
   local frame=ui.g_ricePuddingUI
   if not frame or not frame.main_layer then return end
   local s=ui.g_self
   local layer=ms.d_u.clearLayer(frame.main_layer,10,s.newTag)
   if not layer then return end
   local x=s.mx-s.w*0.33
   local function label(text,y,size,tag)
    layer:addChild(ms.d_u.createByStyles({type='label',font='arial',fontsize=size,x=x,
     y=s.my+s.h*y,string=text,color={120,30,0}}),1,tag)
   end
   label('个人粽子累计制作',0.30,24,91141)
   label(tostring(progress.rice_count)..' 个',0.20,30,91142)
   label('再做'..tostring(progress.left_process)..'个领蟠桃',0.10,22,91143)
   local recent=s.luck_list and s.luck_list[1]
   if recent then
    local item=ms.d_packageUI.g_itemAttrTable[recent.type_id]
    label('最近制作',-0.08,22,91144)
    label(item and item.name or '粽子',-0.19,24,91145)
   end
  end
  ui._localRiceRestore=function()
   for key,value in pairs(old) do ui[key]=value end
   ui.g_self.end_time=originalEnd
   ms.d_commonLayerUI.recvUsedItem=usedItem
   ms.d_hz.gethz=hz;ui._localRiceRestore=nil
  end
 end
end
