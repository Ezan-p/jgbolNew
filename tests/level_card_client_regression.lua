local source=...
local sent,uses,hints,refreshes,results,panels={},0,0,0,0,{}
local scene={}
CCDirector={sharedDirector=function() return {getRunningScene=function() return scene end} end}
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
ms.d_mainUI.playerLevelUp=function(parent)
 assert(parent==scene and refreshes>0)
 local player=ms.d_mainUI.g_playerInfo
 assert(player.isLevelUp and player.levelUpInfo)
 panels[#panels+1]=player.levelUpInfo
 player.isLevelUp=false
end
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
-- The wire sends event 2 before event 21; mirror the native event 2 handler.
local function upgrade(old,new)
 local info={old_level=old,new_level=new,gift_lists_by_level={
  [new]={{object_type=5,attach_type=1020,attach_count=3}}}}
 ms.d_mainUI.g_playerInfo.level=new
 ms.d_mainUI.g_playerInfo.levelUpInfo=info
 ms.d_mainUI.g_playerInfo.isLevelUp=true
 return info
end
local info=upgrade(19,20)
ms.d_commonLayerUI.recvUsedItem({type_id=1901,result=0})
assert(refreshes==0 and #panels==0)
ms.d_commonLayerUI.recvUsedItem({type_id=1901,result=1,count=1})
assert(refreshes==1 and results==0 and #panels==1 and panels[1]==info)
assert(not ms.d_mainUI.g_playerInfo.isLevelUp)
-- A repeated callback or later main-screen check must not reopen this panel.
ms.d_commonLayerUI.recvUsedItem({type_id=1901,result=1,count=1})
assert(#panels==1)
info=upgrade(20,21)
ms.d_commonLayerUI.recvUsedItem({type_id=1901,result=1,count=1})
assert(#panels==2 and panels[2]==info)
info=upgrade(98,99)
ms.d_commonLayerUI.recvUsedItem({type_id=1901,result=1,count=1})
assert(#panels==3 and panels[3]==info)
bag.requestUseItem({type_id=1901,count=1});assert(#sent==2 and hints==2)
assert(ms.d_commonLayerUI.recvUsedItem({type_id=1152,result=1})=='native result')
assert(results==1)
assert(#panels==3)
bag.g_itemAttrTable={[1152]=template}
bag.getPackageCSVConfig();assert(bag.g_itemAttrTable[1901].name=='等级卡')
bag._localLevelCardRestore();assert(bag.g_itemAttrTable[1901]==nil)
assert(ms.d_commonLayerUI.recvUsedItem({type_id=1901})=='native result')
assert(bag.requestUseItem({type_id=1901,count=1})=='native')
assert(loadstring(source))();assert(bag.g_itemAttrTable[1901].name=='等级卡')
return 'Level card client regression passed'
