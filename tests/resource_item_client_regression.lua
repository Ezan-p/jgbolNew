local source=...
local picker,sent,uses=nil,{},0
local bag={requestUseItem=function() uses=uses+1;return 'native' end,
 getPropIDByTypeId=function(id) return 9000+id end}
local ms={d_packageUI=bag,d_mainUI={g_mainUI={main_layer={}}},
 d_data={createBatchUse=function(parent,range,callback) picker={range=range,callback=callback} end},
 d_common_def={object_type={role=1}},d_msg_def={gscl_msg_id={msg_use_item=1051}},
 d_u={main_server_send_msg=function(mid,data) assert(mid==1051);sent[#sent+1]=data end}}
package.loaded.ms=ms
assert(loadstring(source))();assert(loadstring(source))()
for _,tid in ipairs({1020,1022,1023}) do
 for _,count in ipairs({0,1}) do
  assert(bag.requestUseItem({type_id=tid,count=count})=='native')
 end
 for _,count in ipairs({2,300,1000}) do
  bag.requestUseItem({type_id=tid,id=77,count=count})
  assert(picker.range.min==1 and picker.range.max==count)
  local before=#sent
  picker.callback(0);picker.callback(-1);picker.callback(1.5);picker.callback(count+1)
  assert(#sent==before)
  picker.callback(count)
  local request=sent[#sent]
  assert(request.item_id==77 and request.item_type==tid and request.item_count==count)
  assert(request.des_id==0 and request.des_type==1)
  assert(bag.g_lastRequestUsedItem.count==count)
 end
 bag.requestUseItem({type_id=tid,count=2});picker.callback(2)
 assert(sent[#sent].item_id==9000+tid)
end
assert(bag.requestUseItem({type_id=1029,count=20})=='native')
assert(uses==7)
for _,tid in ipairs({1130,1131,1132,1133,1213,1214,1215,1216}) do
 for _,count in ipairs({0,1}) do
  assert(bag.requestUseItem({type_id=tid,count=count})=='native')
 end
 for _,stock in ipairs({2,99,100,301}) do
  local maximum=math.min(100,stock)
  local before=#sent
  bag.requestUseItem({type_id=tid,id=78,count=stock})
  assert(#sent==before and picker.range.min==1 and picker.range.max==maximum)
  picker.callback(0);picker.callback(1.5);picker.callback(maximum+1)
  assert(#sent==before)
  picker.callback(maximum)
  local request=sent[#sent]
  assert(request.item_type==tid and request.item_id==78 and request.item_count==maximum)
  assert(request.des_type==1 and request.des_id==0)
  assert(bag.g_lastRequestUsedItem.count==maximum)
 end
end
-- Five-star rice dumplings are a separate gift, outside the four food pools.
assert(bag.requestUseItem({type_id=1217,count=20})=='native')
bag._localResourceItemRestore()
assert(bag.requestUseItem({type_id=1020,count=20})=='native')
assert(loadstring(source))()
bag.requestUseItem({type_id=1023,count=20});assert(picker.range.max==20)
return 'resource item client regression passed'
