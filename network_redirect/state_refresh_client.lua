-- Keep live growth windows attached to authoritative 1034/1035 instances.
-- The original receivers replace their arrays; callbacks often retain a row
-- from the previous array (training, inheritance, equipment and stone panels).
do
 local ms=package.loaded.ms
 local bag=ms and ms.d_packageUI
 local lineup=ms and ms.d_lineupUI
 if bag and lineup and not ms._localStateRefreshRestore then
  local restores={}
  local function wrap(t,name,make)
   if not t or type(t[name])~='function' then return end
   local original=t[name]
   t[name]=make(original)
   restores[#restores+1]=function() t[name]=original end
  end
  local function index(rows)
   local result={}
   for _,row in ipairs(rows or {}) do result[row.id]=row end
   return result
  end
  local function copyInto(old,row)
   -- Keep client-only CSV/animation fields; wire fields include explicit zeros.
   for key,value in pairs(row) do old[key]=value end
   return old
  end
  local function currentItem(item)
   if not item then return end
   for _,row in ipairs(bag.g_packageItemsInfo or {}) do
    if row.id==item.id and row.attach_type==item.attach_type and row.type_id==item.type_id then
     return row
    end
   end
  end
  local position=ms.d_charPositionUI
  local previewCharacter
  local function ownPosition()
   return position and position.g_charPosUI and not position.g_isQuitBoard
     and not position.g_charPosUI.isReadOnly
  end
  wrap(position,'showItemIntro',function(original)
   return function(item,character)
    if ownPosition() then item=currentItem(item) or item end
    previewCharacter=character
    return original(item,character)
   end
  end)
  local function refreshPreview()
   if not ownPosition() or not position.tagDef then return end
   local parent=position.g_charPosUI.charInfoLayer
   if not parent or not parent:getChildByTag(position.tagDef.usedItemIntro) then return end
   local item=currentItem(position.g_lastItemIntro)
   if item then position.showItemIntro(item,previewCharacter)
   else parent:removeChildByTag(position.tagDef.usedItemIntro,true) end
  end
  local previousItems={}
  wrap(bag,'getDateFormServer',function(original)
   return function(data)
    if data.first_send then previousItems=index(bag.g_packageItemsInfo) end
    local current=index(bag.g_packageItemsInfo)
    for n,row in ipairs(data.attach_list or {}) do
     local old=current[row.id] or previousItems[row.id]
     -- Spells are handled by skill_client, including its category protection.
     if row.attach_type~=6 and old and old.attach_type==row.attach_type and old.type_id==row.type_id then
      data.attach_list[n]=copyInto(old,row)
     end
    end
    local result=original(data)
    if bag.g_isPackageSorted then previousItems={};refreshPreview() end
    return result
   end
  end)
  local previousCharacters={}
  wrap(lineup,'getDateFormServer',function(original)
   return function(data)
    if data.first_send then previousCharacters=index(lineup.g_characterInfo) end
    local current=index(lineup.g_characterInfo)
    for n,row in ipairs(data.cortege_list or {}) do
     local old=current[row.id] or previousCharacters[row.id]
     if old and old.type==row.type then data.cortege_list[n]=copyInto(old,row) end
    end
    local result=original(data)
    local events=ms.d_event_mgr
    if not events or not events.getNextPackageType or events.getNextPackageType()~=1034 then
     previousCharacters={}
    end
    return result
   end
  end)
  for _,name in ipairs({'updateItemInfo','updateSkillInfo'}) do
   wrap(lineup,name,function(original)
    return function(data)
     local result=original(data)
     refreshPreview()
     return result
    end
   end)
  end
  -- The formation menu can pass a copied row created before the last sync.
  wrap(ms.d_equipmentUpgradeUI,'showEnhanceLayer',function(original)
   return function(parent,item,...)
    return original(parent,currentItem(item) or item,...)
   end
  end)
  ms._localStateRefreshRestore=function()
   for n=#restores,1,-1 do restores[n]() end
   ms._localStateRefreshRestore=nil
  end
 end
end
