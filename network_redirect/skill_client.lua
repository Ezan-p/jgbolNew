-- Original 3.87 spell instances use count for failure compensation, including 0.
-- Preserve selected spell tables across full/chunked inventory snapshots.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_packageUI
 if ui and ui.getDateFormServer and not ui._localSkillRestore then
  local receive,show,refresh=ui.getDateFormServer,ui.showPackage,ui.refreshPackage
  local upgrade=ms.d_skillUpgradeUI
  local upgradeShow=upgrade and upgrade.show
  local upgradeResult=upgrade and upgrade.showServerRet
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
   for _,item in ipairs(ui.g_packageItemsInfo or {}) do
    if item.attach_type==6 and item.id==selected.id and item.type_id==selected.type_id then
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
   ui.getDateFormServer=receive;ui.showPackage=show;ui.refreshPackage=refresh
   if upgradeShow then upgrade.show=upgradeShow end
   if upgradeResult then upgrade.showServerRet=upgradeResult end
   local board=ui.g_packageUI and ui.g_packageUI.board_layer
   -- Scene teardown can free the Cocos node before its Lua exit callback runs.
   if ui.g_isInPackage and board then pcall(function() board:removeChildByTag(hintTag,true) end) end
   ui._localSkillRestore=nil
  end
 end
end
