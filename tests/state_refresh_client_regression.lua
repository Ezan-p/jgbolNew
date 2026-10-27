local checks={}
local nextPacket=0
local bag={g_packageItemsInfo={},g_isPackageSorted=true}
local lineup={g_characterInfo={}}
bag.getDateFormServer=function(data)
 if data.first_send then bag.g_packageItemsInfo={} end
 for _,row in ipairs(data.attach_list) do table.insert(bag.g_packageItemsInfo,row) end
 bag.g_isPackageSorted=nextPacket~=1035
end
lineup.getDateFormServer=function(data)
 if data.first_send then lineup.g_characterInfo={} end
 for _,row in ipairs(data.cortege_list) do table.insert(lineup.g_characterInfo,row) end
end
local function delta(data)
 for _,row in ipairs(bag.g_packageItemsInfo) do
  if row.id==data.id then for key,value in pairs(data.fields) do row[key]=value end end
 end
end
lineup.updateItemInfo=delta;lineup.updateSkillInfo=delta
local preview,previewCount,open=nil,0,false
local parent={
 getChildByTag=function() return open and {} or nil end,
 removeChildByTag=function() open=false end,
}
local position={g_isQuitBoard=false,g_charPosUI={charInfoLayer=parent,isReadOnly=false},tagDef={usedItemIntro=29}}
position.showItemIntro=function(item)
 position.g_lastItemIntro=item;preview={level=item.level,effect=item.effect_value};previewCount=previewCount+1;open=true
end
local equipment={showEnhanceLayer=function(_,item) return item end}
local ms={d_packageUI=bag,d_lineupUI=lineup,d_charPositionUI=position,d_equipmentUpgradeUI=equipment,
 d_event_mgr={getNextPackageType=function() return nextPacket end}}
package.loaded.ms=ms
local receiveItems,receiveCharacters,show=bag.getDateFormServer,lineup.getDateFormServer,position.showItemIntro
-- INSTALL_PATCH
local function item(level,effect)
 return {id=11,type_id=2001,attach_type=5,level=level,effect_value=effect,count=1,equip_order=1,equip_pos=1}
end
local selected=item(1,100);selected.csvInfo={name='weapon'}
bag.getDateFormServer({first_send=true,attach_list={selected}})
local stale=item(1,100)
position.showItemIntro(stale)
assert(position.g_lastItemIntro==selected)
lineup.updateItemInfo({id=11,fields={level=2,effect_value=125}})
assert(preview.level==2 and preview.effect==125)
assert(equipment.showEnhanceLayer({},stale)==selected)
checks[#checks+1]='copied formation preview and upgrade entry resolve the current item'
nextPacket=1035
local before=previewCount
bag.getDateFormServer({first_send=true,attach_list={{id=12,type_id=1001,attach_type=5,count=9}}})
assert(previewCount==before and preview.level==2)
nextPacket=0
bag.getDateFormServer({first_send=false,attach_list={item(3,150)}})
assert(bag.g_packageItemsInfo[2]==selected and preview.level==3 and preview.effect==150)
assert(selected.csvInfo.name=='weapon')
bag.getDateFormServer({first_send=true,attach_list={item(4,175)}})
lineup.updateItemInfo({id=11,fields={level=5,effect_value=200}})
assert(selected.level==5 and selected.effect_value==200 and preview.effect==200)
checks[#checks+1]='equipment keeps its live reference across chunks, consecutive snapshots and deltas'
local hero={id=1,type=5001,level=3,culture_point=100,cur_exp=0,hp_plus=0}
lineup.getDateFormServer({first_send=true,cortege_list={hero}})
nextPacket=1034
lineup.getDateFormServer({first_send=true,cortege_list={{id=2,type=5002,level=1}}})
nextPacket=0
lineup.getDateFormServer({first_send=false,cortege_list={{id=1,type=5001,level=4,culture_point=95,cur_exp=0.2,hp_plus=5}}})
assert(lineup.g_characterInfo[2]==hero and hero.culture_point==95 and hero.cur_exp==0.2)
lineup.getDateFormServer({first_send=true,cortege_list={{id=1,type=5001,level=5,culture_point=0,cur_exp=4294967296.5,hp_plus=100}}})
assert(lineup.g_characterInfo[1]==hero and hero.culture_point==0 and hero.cur_exp==4294967296.5 and hero.hp_plus==100)
checks[#checks+1]='training, inheritance and experience references receive consecutive full precision snapshots'
bag.getDateFormServer({first_send=true,attach_list={}})
assert(#bag.g_packageItemsInfo==0 and not open)
bag.getDateFormServer({first_send=false,attach_list={item(1,100)}})
assert(bag.g_packageItemsInfo[1]~=selected)
bag.getDateFormServer({first_send=true,attach_list={{id=11,type_id=3001,attach_type=5,level=1}}})
assert(bag.g_packageItemsInfo[1]~=selected and selected.type_id==2001)
lineup.getDateFormServer({first_send=true,cortege_list={}})
lineup.getDateFormServer({first_send=false,cortege_list={{id=1,type=5001,level=1}}})
assert(lineup.g_characterInfo[1]~=hero)
checks[#checks+1]='removed instances and converted types are not resurrected from old indexes'
position.g_charPosUI.isReadOnly=true
position.showItemIntro(stale)
local calls=previewCount
lineup.updateItemInfo({id=11,fields={level=7,effect_value=250}})
assert(position.g_lastItemIntro==stale and previewCount==calls)
position.g_charPosUI.isReadOnly=false;position.g_isQuitBoard=true
parent.getChildByTag=function() error('released node') end
lineup.updateItemInfo({id=11,fields={level=8}})
assert(previewCount==calls)
checks[#checks+1]='other player previews and released scenes are left untouched'
ms._localStateRefreshRestore()
assert(bag.getDateFormServer==receiveItems and lineup.getDateFormServer==receiveCharacters and position.showItemIntro==show)
checks[#checks+1]='adapter cleanup restores every intercepted function'
return checks
