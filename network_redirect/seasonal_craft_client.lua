-- Embedded in each event adapter so their selection and quota stay independent.
  local craftRemaining,craftReset=__CRAFT_DAILY_LIMIT__,0
  local function updateCraft(data)
   if data and type(data.local_craft_remaining)=='number' then
    craftRemaining=data.local_craft_remaining
    craftReset=data.local_craft_reset_time or 0
   end
  end
  local function availableCrafts()
   if craftReset>0 and ms.d_time.getTime()>=craftReset then
    craftRemaining=__CRAFT_DAILY_LIMIT__;craftReset=0
   end
   return math.min(100,craftRemaining)
  end
  local function usable(item)
   for _,key in ipairs({'is_lock','owner_id','equip_pos','equip_order'}) do
    local value=item[key]
    if value and value~=0 then return false end
   end
   return (item.count or 0)>0
  end
  local function craftMaterials(recipe,name)
   ms.d_packageUI.getAllProps()
   local limit,materials=availableCrafts(),{}
   for _,part in ipairs(recipe.source) do
    local count,best=0,nil
    for _,item in pairs(ms.d_packageUI.g_propsTable or {}) do
     if item.type_id==part.attach_type and usable(item) then
      if name=='moon' then count=count+item.count
      elseif not best or item.count>best.count then best=item;count=item.count end
     end
    end
    limit=math.min(limit,math.floor(count/part.attach_count))
    if best then materials[#materials+1]={id=best.id} end
   end
   return limit,materials
  end
  local function craftBatch(index,name,frame)
   if not enabled then ms.d_info.show('活动暂未开放');return end
   local state=ui.g_self
   local recipe=state.Recipe and state.Recipe[index]
   if not recipe or not frame or not frame.main_layer then return end
   if availableCrafts()<1 then ms.d_info.show('今日合成次数已满');return end
   local maximum=craftMaterials(recipe,name)
   if maximum<1 then ms.d_info.show('合成材料不足');return end
   local layer=frame.main_layer
   local submitted=false
   ms.d_data.createBatchUse(layer,{min=1,max=maximum,defaultCount=1},function(count)
    if submitted or not enabled or ui.g_self~=state or frame.main_layer~=layer or
      (name=='moon' and ui.g_moonCakeUI~=frame) or
      (name=='rice' and ui.g_ricePuddingUI~=frame) or state.Recipe[index]~=recipe then return end
    if type(count)~='number' or count~=math.floor(count) or count<1 or count>maximum then return end
    local current,materials=craftMaterials(recipe,name)
    if count>current then ms.d_info.show('材料或剩余合成次数不足，请重新选择');return end
    submitted=true
    local request={activity=name,count=count}
    if name=='moon' then request.src_type=1134+index
    else request.compose_type=index;request.material_count=#materials;request.material_list=materials end
    ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_common_event,
     {id=249,data=table.tostring(request)})
   end)
  end
