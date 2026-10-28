local source=...
local picker,sent,shown,refreshes,uses=nil,{},nil,0,0
local bag={g_lastRequestUsedItem={},requestUseItem=function() uses=uses+1;return 'native' end,
 getPropIDByTypeId=function(id) assert(id==1021);return 77 end}
local ms={d_packageUI=bag,d_mainUI={g_mainUI={main_layer={}}},
 d_data={createBatchUse=function(parent,range,callback) picker={range=range,callback=callback} end},
 d_common_def={object_type={role=1}},d_msg_def={gscl_msg_id={msg_use_item=1051}},
 d_u={main_server_send_msg=function(mid,data) assert(mid==1051);sent[#sent+1]=data end},
 d_hz={gethz=function(key) return 'native '..key end}}
ms.d_commonLayerUI={recvUsedItem=function(data)
 shown=ms.d_hz.gethz(data.type_id==1021 and 'congrasFengShen' or 'other')
 refreshes=refreshes+1
 if data.explode then error('native failure') end
 return 'refreshed'
end}
package.loaded.ms=ms
local oldHz=ms.d_hz.gethz
assert(loadstring(source))();assert(loadstring(source))()
assert(bag.requestUseItem({type_id=1020,count=12})=='native')
assert(bag.requestUseItem({type_id=1021,count=1})=='native')
assert(bag.requestUseItem({type_id=1021,count=0})=='native')
assert(uses==3)
for _,count in ipairs({2,99,100,150}) do
 bag.requestUseItem({type_id=1021,id=77,count=count})
 assert(picker.range.min==1 and picker.range.max==math.min(count,100))
 local before=#sent
 picker.callback(0);picker.callback(1.5);picker.callback(picker.range.max+1)
 assert(#sent==before)
 picker.callback(picker.range.max)
 local request=sent[#sent]
 assert(request.item_id==77 and request.item_type==1021 and request.item_count==math.min(count,100))
 assert(request.des_id==0 and request.des_type==1)
 assert(bag.g_lastRequestUsedItem.count==request.item_count)
end
bag.requestUseItem({type_id=1021,count=2});picker.callback(2)
assert(sent[#sent].item_id==77)
assert(ms.d_commonLayerUI.recvUsedItem({type_id=1021,result=1,count=100,effect_value=300})=='refreshed')
assert(shown=='使用100枚封神令牌，增加300次封神榜挑战机会' and refreshes==1)
assert(ms.d_hz.gethz==oldHz)
ms.d_commonLayerUI.recvUsedItem({type_id=1021,result=0,count=2})
assert(shown=='封神令牌使用失败')
ms.d_commonLayerUI.recvUsedItem({type_id=1020,result=1})
assert(shown=='native other')
assert(not pcall(ms.d_commonLayerUI.recvUsedItem,{type_id=1021,result=1,explode=true}))
assert(ms.d_hz.gethz==oldHz)
bag._localRankTokenRestore()
assert(bag.requestUseItem({type_id=1021,count=10})=='native')
assert(loadstring(source))()
bag.requestUseItem({type_id=1021,count=2})
assert(picker.range.max==2)
return 'rank token client regression passed'
