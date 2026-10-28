-- Keep the original activity lists/operating switches and their native art.
-- activityUI already dims the legacy board; funUI's newer list needs the same
-- treatment in createFunCell (original L408-428). Keep locked rows touchable.
do
 local ms=package.loaded.ms
 local act=ms and ms.d_activityUI
 local fun=ms and ms.d_funUI
 if not act or not fun or not act.getRequireLevel or not act.verifyLevel
     or not fun.createFunCell or not fun.create then return 'pending' end
 if not ms._localActivityLevelRestore then
  local oldRequire,oldVerify=act.getRequireLevel,act.verifyLevel
  local oldCell,oldCreate=fun.createFunCell,fun.create
  local delegates=setmetatable({},{__mode='k'})
  -- Local opening levels requested by the user, not original client constants.
  local overrides={monday=15,fishrush=20,twoyears=20,rulaitable=20,
   tower=20,destiny=30,forge=30}
  local function level()
   return tonumber(ms.d_mainUI.g_playerInfo.level) or 0
  end
  act.getRequireLevel=function(id)
   for name,required in pairs(overrides) do
    if act.activityID[name] and id==act.activityID[name] then return required end
   end
   -- Native getRequireLevel omits this separate check in activityUI.show.
   if id==act.activityID.tongtianta then return 36 end
   return oldRequire(id) -- Includes Taiwan friends and server-supplied limits.
  end
  local function locked(id)
   local required=tonumber(act.getRequireLevel(id)) or 0
   return level()<required,required
  end
  local function notice(required)
   ms.d_info.show('角色达到'..required..'级开放')
  end
  act.verifyLevel=function(id,...)
   local blocked,required=locked(id)
   if blocked then notice(required);return false end
   return oldVerify(id,...)
  end
  fun.createFunCell=function(parent,row,size)
   local blocked,required=locked(row.id)
   if not blocked then return oldCell(parent,row,size) end
   -- Suppress only this locked cell's reward badge and festive animation.
   -- Do not mutate the server status or permanently change funConfig.
   local copy={};for k,v in pairs(row) do copy[k]=v end;copy.hint=0
   local config=fun.funConfig[row.id]
   local animation=config and config.hasCCBI
   if config then config.hasCCBI=false end
   local children=parent:getChildren()
   local first=children and children:count() or 0
   local ok,result=pcall(oldCell,parent,copy,size)
   if config then config.hasCCBI=animation end
   if not ok then error(result,0) end
   -- Original first added child is the CCSprite for btn<ID>1/2.png.
   children=parent:getChildren()
   if children and children:count()>first then
    tolua.cast(children:objectAtIndex(first),'CCSprite'):setColor(ccc3(100,100,100))
   end
   local label=CCLabelTTF:create(required..'级开放','arial',16)
   label:setColor(ccc3(255,100,101))
   label:setPosition(ccp(size.width*0.5,size.height*0.16))
   parent:addChild(label,3)
   return result
  end
  local function bindSelection()
   local state=fun.g_funUI
   local view=state and state.funTableView
   if not view or delegates[view] or not view.delegate
       or type(view.delegate.touchCellAtIndex)~='function' then return end
   local original=view.delegate
   local replacement={};for k,v in pairs(original) do replacement[k]=v end
   replacement.touchCellAtIndex=function(index,...)
    -- Preserve native selection/detail rendering (including its red level text).
    local result=original.touchCellAtIndex(index,...)
    local current=fun.g_funUI
    local row=current and current.fun_list and current.fun_list[index]
    if row then
     local blocked,required=locked(row.id)
     if blocked then notice(required) end
    end
    return result
   end
   delegates[view]={original=original,replacement=replacement}
   view:setDelegate(replacement)
  end
  fun.create=function(...)
   local result=oldCreate(...)
   bindSelection()
   return result
  end
  bindSelection()
  ms._localActivityLevelRestore=function()
   act.getRequireLevel=oldRequire;act.verifyLevel=oldVerify
   fun.createFunCell=oldCell;fun.create=oldCreate
   for view,saved in pairs(delegates) do
    if view.delegate==saved.replacement then view:setDelegate(saved.original) end
   end
   ms._localActivityLevelRestore=nil
  end
 end
end
