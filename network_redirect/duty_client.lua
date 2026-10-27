-- Native gold=0 is truthy in Lua. Suppress that path and draw only the saved reward.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_endlessFightUI
 if not ui or not ui.initFightType or not ms.d_data then return 'pending' end
 if not ui._localDutyRewardRestore then
  local original=ui.initFightType
  ui.initFightType=function(lineups,...)
   local native={}
   for i,row in ipairs(lineups) do
    native[i]={}
    for k,v in pairs(row) do if k~='gold' then native[i][k]=v end end
   end
   local result=original(native,...)
   local layer=ui.g_fightTypeLayer
   if not layer then return result end
   local positions={{0.75,0.79},{0.25,0.79},{0.5,0.74}}
   for _,row in ipairs(lineups) do
    local reward=row.reward
    local pos=positions[row.stars]
    if reward and pos and (tonumber(reward.attach_count) or 0)>0 then
     local icon=ms.d_data.getCertainSmallSprite(reward.object_type,reward.attach_type,reward.attach_level)
     ms.d_u.setStyles(icon,{x=pos[1]-0.035,y=pos[2],scaleH=0.045})
     layer:addChild(icon,3)
     local label=ms.d_u.createByStyle({type='label',font='arial',fontsize=24,
      string='奖',x=pos[1]-0.075,y=pos[2]})
     layer:addChild(label,3)
     local count=ms.d_u.createByStyle({type='label',font='arial',fontsize=24,
      string='×'..reward.attach_count,x=pos[1]+0.025,y=pos[2]})
     layer:addChild(count,3)
    end
   end
   return result
  end
  ui._localDutyRewardRestore=function()
   ui.initFightType=original;ui._localDutyRewardRestore=nil
  end
 end
end
