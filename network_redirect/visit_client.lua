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
  local original,receive,showPrize=ui.gameShou,ui.getResFromServer,ui.showShouPrize
  local claimed=false
  ui.gameShou=function(...)
   claimed=false
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
  ui.getResFromServer=function(value,...)
   if value and value.visit_index==3 and value.op_type==2 then
    -- A replay must not run the native mask-removal animation twice.
    if value.result~=1 or claimed then return end
   end
   return receive(value,...)
  end
  ui.showShouPrize=function(value)
   if value.result~=1 or claimed then return end
   local row=value.visit_list and value.visit_list[3]
   if not row or not row.has_visit then return end
   local parent=ui.g_mainLayer
   if not parent or not parent:getChildByTag(1) then return end
   showPrize(value)
   -- Inventory snapshots arrive before this success callback. The reward
   -- count is one book; a spell instance's count=0 is upgrade compensation.
   ms.d_commonLayerUI.showPrizeResLayer(parent,value.local_prizes or {row.prize_info},nil,{no_fall=true})
   claimed=true
  end
  ui._localVisitRestore=function()
   ui.gameShou=original;ui.getResFromServer=receive;ui.showShouPrize=showPrize
   ui._localVisitRestore=nil
  end
 end
end
