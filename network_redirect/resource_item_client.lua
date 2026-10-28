-- Recovery items and seasonal foods reuse the native quantity picker.
do
 local ms=package.loaded.ms
 local bag=ms and ms.d_packageUI
 if not bag or not ms.d_data or not ms.d_data.createBatchUse then return 'pending' end
 if not bag._localResourceItemRestore then
  local original=bag.requestUseItem
  local foods={[1130]=true,[1131]=true,[1132]=true,[1133]=true,
               [1213]=true,[1214]=true,[1215]=true,[1216]=true}
  bag.requestUseItem=function(item,...)
   if not item or (item.type_id~=1020 and item.type_id~=1022 and item.type_id~=1023 and not foods[item.type_id])
     or (item.count or 0)<=1 then return original(item,...) end
   local maximum=foods[item.type_id] and math.min(100,item.count) or item.count
   ms.d_data.createBatchUse(ms.d_mainUI.g_mainUI.main_layer,{min=1,max=maximum},function(count)
    if type(count)~='number' or count~=math.floor(count) or count<1 or count>maximum then return end
    bag.g_lastRequestUsedItem=bag.g_lastRequestUsedItem or {}
    bag.g_lastRequestUsedItem.item=item
    bag.g_lastRequestUsedItem.count=count
    ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_use_item,{
     item_type=item.type_id,item_id=item.id or bag.getPropIDByTypeId(item.type_id),
     des_type=ms.d_common_def.object_type.role,des_id=0,item_count=count})
   end)
  end
  bag._localResourceItemRestore=function()
   bag.requestUseItem=original;bag._localResourceItemRestore=nil
  end
 end
end
