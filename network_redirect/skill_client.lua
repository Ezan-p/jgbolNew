-- Legacy spell count is retained as zero; upgrades no longer accumulate pity.
-- Preserve selected spell tables across full/chunked inventory snapshots.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_packageUI
 if ui and ui.getDateFormServer and not ui._localSkillRestore then
  local receive,show,refresh=ui.getDateFormServer,ui.showPackage,ui.refreshPackage
  local upgrade=ms.d_skillUpgradeUI
  local upgradeShow=upgrade and upgrade.show
  local upgradeResult=upgrade and upgrade.showServerRet
  local undo={}
  local active=true
  local function clearPity(item)
   if not item then return end
   if item.attach_type==6 then item.count=0
   elseif item.attach_type==5 and (item.type_id==1090 or item.type_id==1091 or item.type_id==1092) then
    item.prob_compen=0
   end
  end
  -- Native material pickers append the compensation suffix even at zero.
  -- Remove that suffix only within these two upgrade screens.
  local function plainRate(text)
   if type(text)~='string' or not ms.d_hz then return text end
   local name=ms.d_hz.gethz('skill_up_add_rate')
   local start=text:find('('..name..': +',1,true)
   if start then return (text:sub(1,start-1):gsub('%s+$','')) end
   return text
  end
  local function scope(fn,proxy)
   local env=getfenv(fn)
   setfenv(fn,setmetatable({d_ms=setmetatable(proxy,{__index=ms})},{__index=env,__newindex=env}))
   undo[#undo+1]=function() setfenv(fn,env) end
  end
  if upgrade and upgrade.createSkillMutilSelectLayer and ms.d_selectLayer then
   local selector=setmetatable({}, {__index=ms.d_selectLayer})
   selector.createSelectLayer=function(parent,items,options,...)
    for _,key in ipairs({'touchCellFunc','selectAllFunc','unSelectAllFunc','ensureFilterCallback'}) do
     local native=options[key]
     if native then
      options[key]=function(...)
       local selected=upgrade.g_self.params.skill_info
       if active then selected.count=0 end
       local result=native(...)
       if active then
        for i=1,100 do
         local name,label=debug.getupvalue(native,i)
         if not name then break end
         if name=='upgrade_rate_lable' and label then label:setString(plainRate(label:getString())) end
        end
       end
       return result
      end
     end
    end
    return ms.d_selectLayer.createSelectLayer(parent,items,options,...)
   end
   scope(upgrade.createSkillMutilSelectLayer,{d_selectLayer=selector})
  end
  local stone=ms.d_stoneUpgradeUI
  if stone then
   local createSelector=stone.createStoneMutilSelectLayer
   for _,key in ipairs({'show','createStoneMutilSelectLayer'}) do
    local native=stone[key]
    if native then
     stone[key]=function(...)
      for _,item in ipairs(ui.g_packageItemsInfo or {}) do clearPity(item) end
      if stone.g_stoneUpgradeUI then clearPity(stone.g_stoneUpgradeUI.stone) end
      if key=='show' then local _,_,item=...;clearPity(item) end
      return native(...)
     end
     undo[#undo+1]=function() stone[key]=native end
    end
   end
   -- Local callbacks inherit the native selector's scoped environment.
   if createSelector and ms.d_u then
    local utilities=setmetatable({}, {__index=ms.d_u})
    utilities.createByStyle=function(style,...)
     if active and style.type=='label' then style.string=plainRate(style.string) end
     return ms.d_u.createByStyle(style,...)
    end
    scope(createSelector,{d_u=utilities})
   end
  end
  for _,item in ipairs(ui.g_packageItemsInfo or {}) do clearPity(item) end
  local handbook=ms.d_handbookUI
  local handbookShow=handbook and handbook.showSkill
  local handbookDetail=handbook and handbook.showHandbookDetail
  if handbookShow then
   handbook.showSkill=function(...)
    -- IDs 2..11 are internal battle/test skills (11 is an unnamed tile on
    -- older servers). Keep the shared templates
    -- intact: the handbook builds its own grid and hit map from this reader.
    local catalog=ui.g_itemSkillTable
    local visible={}
    for id,skill in pairs(catalog or {}) do
     local number=tonumber(id)
     if not (number and number>=1 and number<=11) then visible[id]=skill end
    end
    ui.g_itemSkillTable=visible
    local ok,result=pcall(handbookShow,...)
    ui.g_itemSkillTable=catalog
    if not ok then error(result,0) end
    return result
   end
  end
  if handbookDetail then
   handbook.showHandbookDetail=function(id,...)
    if id~=21 or not handbook.g_self or handbook.g_self.last_tag~=6 then
     return handbookDetail(id,...)
    end
    -- Native createSkillLabel reads current_characterInfo.magic for Rulai.
    -- A catalog preview has no owner; use zero owner bonus even if a prior
    -- formation visit left a selected character cached in this module.
    local position=ms.d_charPositionUI
    local state=position.g_charPosUI
    local preview={}
    for key,value in pairs(state or {}) do preview[key]=value end
    preview.current_characterInfo={magic=0}
    position.g_charPosUI=preview
    local ok,result=pcall(handbookDetail,id,...)
    position.g_charPosUI=state
    if not ok then error(result,0) end
    return result
   end
  end
  local previous={}
  local hintTag=91106
  local function index()
   local result={}
   for _,item in ipairs(ui.g_packageItemsInfo or {}) do
    if item.attach_type==6 then result[item.id]=item end
   end
   return result
  end
  -- Formation/change-item lists can pass a copied spell record. The original
  -- result callback updates target_skill_level, but its labels and success-rate
  -- calculation still read params.skill_info. Rebind that reader before every
  -- draw/result; preserving only the inventory object's identity is insufficient.
  local function bindSkill(params)
   local selected=params and params.skill_info
   if not selected then return end
   selected.count=0
   for _,item in ipairs(ui.g_packageItemsInfo or {}) do
    if item.attach_type==6 and item.id==selected.id and item.type_id==selected.type_id then
     item.count=0
     if selected~=item then
      for key,value in pairs(item) do selected[key]=value end
      params.skill_info=item
     end
     return item
    end
   end
  end
  if upgradeShow then
   upgrade.show=function(params,...)
    bindSkill(params or (upgrade.g_self and upgrade.g_self.params))
    return upgradeShow(params,...)
   end
  end
  if upgradeResult then
   upgrade.showServerRet=function(data,...)
    bindSkill(upgrade.g_self and upgrade.g_self.params)
    return upgradeResult(data,...)
   end
  end
  -- getItemsByPackageTag removes innate skills from the shared category in place.
  -- Give that reader its own array so lineup/material readers retain the catalog.
  local function withCategory(fn,...)
   if not ui.g_isPackageSorted then ui.sortItems() end
   local categories=ui.g_reorgItemsInfo
   local skills=categories and categories[6]
   if skills then
    local copy={};for i,item in ipairs(skills) do copy[i]=item end
    categories[6]=copy
   end
   local ok,result=pcall(fn,...)
   if skills then categories[6]=skills end
   if not ok then error(result,0) end
   return result
  end
  local function emptyHint()
   local board=ui.g_packageUI and ui.g_packageUI.board_layer
   if not board or not ui.g_isInPackage then return end
   board:removeChildByTag(hintTag,true)
   if ui.g_lastSelectedItemButton~=ui.packageTagDef.skill then return end
   for _,item in ipairs(ui.g_packageItemsInfo or {}) do
    if item.attach_type==6 and (item.protogenic or 0)==0 then return end
   end
   local layer=CCLayer:create();board:addChild(layer,20,hintTag)
   local function label(text,y,size)
    layer:addChild(ms.d_u.createByStyles({type='label',font='arial',fontsize=size,
     x=0.60,y=y,string=text,color={254,235,185}}))
   end
   label('尚无可装备的法术',0.65,28)
   label('神仙自带法术可在「阵容」中查看和升级',0.53,21)
   label('获取途径：旅途掉落、乾坤袋、三星赐福',0.41,21)
   label('五星被动法术也可通过碎片合成获得',0.31,21)
  end
  ui.showPackage=function(tag)
   local result=withCategory(show,tag);emptyHint();return result
  end
  ui.refreshPackage=function(...)
   local result=withCategory(refresh,...);emptyHint();return result
  end
  ui.getDateFormServer=function(data)
   if data.first_send then previous=index() end
   local current=index()
   for n,item in ipairs(data.attach_list or {}) do
    clearPity(item)
    local old=current[item.id] or previous[item.id]
    if item.attach_type==6 and old and old.type_id==item.type_id then
     for key,value in pairs(item) do old[key]=value end
     data.attach_list[n]=old
    end
   end
   local result=receive(data)
   -- The original receiver marks intermediate 1035 chunks unsorted.
   if ui.g_isPackageSorted then
    previous={}
    if ui.g_isInPackage then ui.refreshPackage() end
   end
   return result
  end
  ui._localSkillRestore=function()
   active=false
   for i=#undo,1,-1 do undo[i]() end
   ui.getDateFormServer=receive;ui.showPackage=show;ui.refreshPackage=refresh
   if upgradeShow then upgrade.show=upgradeShow end
   if upgradeResult then upgrade.showServerRet=upgradeResult end
   if handbookShow then handbook.showSkill=handbookShow end
   if handbookDetail then handbook.showHandbookDetail=handbookDetail end
   local board=ui.g_packageUI and ui.g_packageUI.board_layer
   -- Scene teardown can free the Cocos node before its Lua exit callback runs.
   if ui.g_isInPackage and board then pcall(function() board:removeChildByTag(hintTag,true) end) end
   ui._localSkillRestore=nil
  end
 end
end
