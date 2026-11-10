local source=...
local sent,uses,hints,refreshes,results={},0,0,0,0
local template={name='传世金卡',description='充值',file='217',mainType=6,isStackable=1}
local bag={g_itemAttrTable={[1152]=template},getPackageCSVConfig=function() end,
 refreshPackage=function() refreshes=refreshes+1 end,
 requestUseItem=function() uses=uses+1;return 'native' end,
 getPropIDByTypeId=function() return 88 end}
local ms={d_packageUI=bag,d_mainUI={g_playerInfo={level=19}},
 d_commonLayerUI={recvUsedItem=function() results=results+1;return 'native result' end},
 d_common_def={object_type={role=1}},d_msg_def={gscl_msg_id={msg_use_item=1051}},
 d_info={show=function() hints=hints+1 end},
 d_u={main_server_send_msg=function(mid,data) assert(mid==1051);sent[#sent+1]=data end}}
package.loaded.ms=ms
assert(loadstring(source))();assert(loadstring(source))()
assert(bag.g_itemAttrTable[1901].name=='等级卡')
assert(bag.g_itemAttrTable[1901].description:find('99'))
assert(bag.g_itemAttrTable[1901].file=='217' and template.name=='传世金卡')
assert(bag.requestUseItem({type_id=1152,count=1})=='native' and uses==1)
bag.requestUseItem({type_id=1901,count=0});assert(#sent==0)
bag.requestUseItem({type_id=1901,count=100,id=77})
assert(#sent==1 and sent[1].item_count==1 and sent[1].item_id==77)
assert(sent[1].des_type==1 and sent[1].des_id==0 and sent[1].item_type==1901)
bag.requestUseItem({type_id=1901,count=2});assert(sent[2].item_id==88)
ms.d_mainUI.g_playerInfo.level=99
bag.requestUseItem({type_id=1901,count=2});assert(#sent==2 and hints==1)
ms.d_commonLayerUI.recvUsedItem({type_id=1901,result=1,count=1})
assert(refreshes==1 and results==0)
assert(ms.d_commonLayerUI.recvUsedItem({type_id=1152,result=1})=='native result')
assert(results==1)
bag.g_itemAttrTable={[1152]=template}
bag.getPackageCSVConfig();assert(bag.g_itemAttrTable[1901].name=='等级卡')
bag._localLevelCardRestore();assert(bag.g_itemAttrTable[1901]==nil)
assert(ms.d_commonLayerUI.recvUsedItem({type_id=1901})=='native result')
assert(bag.requestUseItem({type_id=1901,count=1})=='native')
assert(loadstring(source))();assert(bag.g_itemAttrTable[1901].name=='等级卡')
return 'Level card client regression passed'
