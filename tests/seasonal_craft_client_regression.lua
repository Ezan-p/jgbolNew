-- Production adapters with the native recipe/picker contract; no live account.
local moonSource,riceSource=...
local function node()
 return {addChild=function() end,removeChildByTag=function() end}
end
local now=1000
local picker,sends,notices=nil,{},{}
local function noop() end
local function makeUI(name,common)
 local ui={g_self={end_time=0,Recipe={},timeTag=1,mx=0,my=0,w=1,h=1,newTag=2}}
 ui[name=='moon' and 'g_moonCakeUI' or 'g_ricePuddingUI']={main_layer=node()}
 for _,key in ipairs({'updateActivityStatus','canJoin','tickTime','create','cook','showNews','onGetResult'}) do ui[key]=noop end
 for index=1,4 do ui.g_self.Recipe[index]={source={
  {object_type=5,attach_type=common,attach_count=15},
  {object_type=5,attach_type=common+index,attach_count=15}}} end
 return ui
end
local moon,rice=makeUI('moon',1134),makeUI('rice',1208)
local bag={g_propsTable={},getAllProps=noop}
local ms={d_moonCakeUI=moon,d_ricePuddingUI=rice,d_packageUI=bag,
 d_hz={gethz=function(key) return key end},
 d_info={show=function(text) notices[#notices+1]=text end},
 d_time={getTime=function() return now end},
 d_u={createByStyles=node,clearLayer=function() return nil end,
  main_server_send_msg=function(mid,request) sends[#sends+1]={mid=mid,request=request} end},
 d_data={createBatchUse=function(layer,options,callback) picker={layer=layer,options=options,callback=callback} end},
 d_msg_def={gscl_msg_id={msg_common_event=2998}},d_commonLayerUI={recvUsedItem=noop}}
package.loaded.ms=ms
-- Keep the request table observable; wire serialization is covered in Python.
table.tostring=function(value) return value end
assert(loadstring(moonSource))();assert(loadstring(riceSource))()
local checks=0
local function check(test) test();checks=checks+1 end
local function stock(common,count)
 bag.g_propsTable={}
 for tid=common,common+4 do bag.g_propsTable[#bag.g_propsTable+1]={id=tid+10000,type_id=tid,count=count} end
end
local function quota(ui,left)
 ui.onGetResult({local_craft_remaining=left,local_craft_reset_time=2000})
end
for _,spec in ipairs({{ui=moon,name='moon',common=1134},{ui=rice,name='rice',common=1208}}) do
 local ui,name,common=spec.ui,spec.name,spec.common
 check(function()
  stock(common,1500);quota(ui,100)
  for index=1,4 do
   picker=nil;ui.cook(index);assert(picker and picker.options.min==1 and picker.options.max==100)
   local before=#sends;picker.callback(23);assert(#sends==before+1)
   local message=sends[#sends];assert(message.mid==2998 and message.request.id==249)
   local data=message.request.data;assert(data.activity==name and data.count==23)
   if name=='moon' then assert(data.src_type==common+index)
   else
    assert(data.compose_type==index and data.material_count==2)
    assert(data.material_list[1].id==common+10000 and data.material_list[2].id==common+index+10000)
   end
   picker.callback(23);assert(#sends==before+1,'duplicate confirmation')
  end
 end)
 check(function()
  stock(common,1500);quota(ui,7);ui.cook(1);assert(picker.options.max==7)
  local before=#sends
  for _,n in ipairs({0,-1,8,1.5,'2'}) do picker.callback(n) end
  assert(#sends==before)
  quota(ui,0);picker=nil;ui.cook(1);assert(picker==nil)
  now=2000;ui.cook(1);assert(picker.options.max==100);now=1000
 end)
 check(function()
  quota(ui,100);stock(common,149);ui.cook(1);assert(picker.options.max==9)
  local before=#sends;bag.g_propsTable[1].count=15;picker.callback(9);assert(#sends==before)
  bag.g_propsTable[1].count=14;picker=nil;ui.cook(1);assert(not picker)
 end)
 check(function()
  for _,key in ipairs({'is_lock','owner_id','equip_pos','equip_order'}) do
   stock(common,1500);bag.g_propsTable[1][key]=1;picker=nil;ui.cook(1);assert(not picker,key)
   bag.g_propsTable[1][key]=0;ui.cook(1);assert(picker.options.max==100)
  end
 end)
 check(function()
  stock(common,1500);ui.cook(1);local before=#sends
  local field=name=='moon' and 'g_moonCakeUI' or 'g_ricePuddingUI'
  local frame=ui[field];ui[field]={main_layer=node()};picker.callback(2);assert(#sends==before)
  ui[field]=frame;ui.cook(1);local layer=frame.main_layer;frame.main_layer=nil;picker.callback(2)
  assert(#sends==before);frame.main_layer=layer
 end)
 check(function()
  stock(common,1500);ui.cook(1);local callback=picker.callback;local before=#sends
  ui.updateActivityStatus({local_permanent=true,local_enabled=false});callback(2);assert(#sends==before)
  picker=nil;ui.cook(1);assert(not picker)
  ui.updateActivityStatus({local_permanent=true,local_enabled=true,local_craft_remaining=5,local_craft_reset_time=2000})
  ui.cook(1);assert(picker.options.max==5)
 end)
end
check(function()
 stock(1134,15);quota(moon,100)
 bag.g_propsTable[#bag.g_propsTable+1]={id=1,type_id=1134,count=30}
 bag.g_propsTable[#bag.g_propsTable+1]={id=2,type_id=1135,count=30}
 moon.cook(1);assert(picker.options.max==3,'moon combines eligible stacks')
 stock(1208,15);quota(rice,100)
 bag.g_propsTable[#bag.g_propsTable+1]={id=1,type_id=1208,count=30}
 bag.g_propsTable[#bag.g_propsTable+1]={id=2,type_id=1209,count=30}
 rice.cook(1);assert(picker.options.max==2,'rice uses selected stack capacity')
 picker.callback(2);local data=sends[#sends].request.data
 assert(data.material_list[1].id==1 and data.material_list[2].id==2)
end)
check(function()
 quota(moon,3);quota(rice,7)
 stock(1134,1500);moon.cook(1);assert(picker.options.max==3)
 stock(1208,1500);rice.cook(1);assert(picker.options.max==7)
end)
check(function()
 rice._localRiceRestore();moon._localMoonRestore()
 assert(moon.cook==noop and rice.cook==noop and moon.onGetResult==noop and rice.onGetResult==noop)
end)
return checks
