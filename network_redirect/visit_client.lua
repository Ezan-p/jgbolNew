-- Some original spell books have no skill/<id>.jpg. getBigSkillSprite then
-- returns a STRING ('skill/107.jpg'), which crashes the scratch menu. Use that
-- spell's inventory atlas icon, never another spell's picture. Scope the fix
-- to native gameShou and restore the shared renderer even if creation fails.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_loginGameUI
 local data=ms and ms.d_data
 if not ui or not ui.gameShou or not data then return 'pending' end
 if not ui._localVisitRestore then
  local original=ui.gameShou
  ui.gameShou=function(...)
   local renderer=data.getCertainBigSprite
   data.getCertainBigSprite=function(kind,tid,...)
    local sprite=renderer(kind,tid,...)
    if kind==ms.d_common_def.object_type.skill and type(sprite)~='userdata' then
     local icon=data.getSmallSkillSprite(tid)
     local reference=data.getBigSkillSprite(107)
     local size=reference:getContentSize()
     local iconSize=icon:getContentSize()
     local frame=CCSprite:create()
     frame:setContentSize(size)
     icon:setScale(math.min(size.width/iconSize.width,size.height/iconSize.height))
     icon:setPosition(CCPointMake(size.width/2,size.height/2))
     frame:addChild(icon)
     return frame
    end
    return sprite
   end
   local ok,result=pcall(original,...)
   data.getCertainBigSprite=renderer
   if not ok then error(result) end
   return result
  end
  ui._localVisitRestore=function()
   ui.gameShou=original;ui._localVisitRestore=nil
  end
 end
end
