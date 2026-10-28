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

-- The main duty button used to call loadData/create on the editable formation.
-- Fetch a fresh server snapshot instead; flags below are local protocol context.
do
 local ms=package.loaded.ms
 local duty=ms and ms.d_endlessFightUI
 local position=ms and ms.d_charPositionUI
 if not duty or not duty.showCharPos or not position or not position.showOthersInfo then return 'pending' end
 if not duty._localDutyPreviewRestore then
  local oldShow=duty.showCharPos
  local oldInfo=position.showOthersInfo
  local originals={}
  local function isPreview()
   local layer=position.g_charPosUI
   return layer and layer.playerInfo and layer.playerInfo.duty_preview
  end
  duty.showCharPos=function()
   return ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_query_lineup_info,
    {des_type=1,des_id=0,flag=51,fight_id=0})
  end
  position.showOthersInfo=function(info,...)
   if not isPreview() then return oldInfo(info,...) end
   position.g_charPosUI.isReadOnly=true
   -- Native comparison buttons open the ordinary self cache, losing the duty
   -- snapshot. Omit them only while constructing this preview's info panel.
   local menu=ms.d_u.createMenu
   ms.d_u.createMenu=function(styles,...)
    local filtered={}
    for k,v in pairs(styles) do
     if type(k)~='number' then filtered[k]=v end
    end
    for _,v in ipairs(styles) do
     if v.npic~='v2/charPositionUI/mine1.png' and v.npic~='v2/charPositionUI/yours1.png' then
      filtered[#filtered+1]=v
     end
    end
    return menu(filtered,...)
   end
   local ok,result=pcall(oldInfo,info,...)
   ms.d_u.createMenu=menu
   if not ok then error(result) end
   return result
  end
  -- Protect delayed refreshes and direct callbacks as well as native controls.
  for _,name in ipairs({'reloadData','requestChangeChar','requestChangeOrder','requestChangeItem',
                        'showChgCharLayer','createChgPos','compareCharPosition'}) do
   local original=position[name]
   if original then
    originals[name]=original
    position[name]=function(...)
     if isPreview() then return end
     return original(...)
    end
   end
  end
  duty._localDutyPreviewRestore=function()
   duty.showCharPos=oldShow
   position.showOthersInfo=oldInfo
   for name,original in pairs(originals) do position[name]=original end
   duty._localDutyPreviewRestore=nil
  end
 end
end
