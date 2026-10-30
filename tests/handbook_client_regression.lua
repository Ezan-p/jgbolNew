local source=...
local ui={g_itemSkillTable={}}
local handbook={g_self={last_tag=6}}
local position={}
package.loaded.ms={d_packageUI=ui,d_handbookUI=handbook,d_charPositionUI=position}
ui.getDateFormServer=function() end
ui.showPackage=function() end
ui.refreshPackage=function() end
for id=1,11 do ui.g_itemSkillTable[id]={name='internal'} end
for _,id in ipairs({21,22,202}) do ui.g_itemSkillTable[id]={name='spell'} end
ui.g_itemSkillTable['9']={name='string key'}
local catalog=ui.g_itemSkillTable
local failList,failDetail=false,false
handbook.showSkill=function(tag)
 assert(tag==6)
 if failList then error('list failure') end
 local ids={}
 for id in pairs(ui.g_itemSkillTable) do ids[#ids+1]=id end
 table.sort(ids)
 return table.concat(ids,',')
end
handbook.showHandbookDetail=function(id,marker)
 assert(marker=='forwarded')
 if failDetail then error('detail failure') end
 if id==21 then return 3+position.g_charPosUI.current_characterInfo.magic/10000 end
 return id
end
local originalList,originalDetail=handbook.showSkill,handbook.showHandbookDetail
assert(not pcall(originalDetail,21,'forwarded'),'native dependency must fail without formation state')
assert(loadstring(source))()
assert(handbook.showSkill(6)=='21,22,202')
assert(ui.g_itemSkillTable==catalog and catalog[2] and catalog[11] and catalog['9'])
assert(handbook.showHandbookDetail(21,'forwarded')==3)
assert(position.g_charPosUI==nil)
local selected={magic=80000,id=123}
local state={current_characterInfo=selected,other='preserved'}
position.g_charPosUI=state
assert(handbook.showHandbookDetail(21,'forwarded')==3)
assert(position.g_charPosUI==state and state.current_characterInfo==selected and selected.magic==80000)
handbook.g_self.last_tag=4
assert(handbook.showHandbookDetail(21,'forwarded')==11)
handbook.g_self.last_tag=6
assert(handbook.showHandbookDetail(22,'forwarded')==22)
failList=true;assert(not pcall(handbook.showSkill,6));assert(ui.g_itemSkillTable==catalog)
failDetail=true;assert(not pcall(handbook.showHandbookDetail,21,'forwarded'));assert(position.g_charPosUI==state)
local patched=handbook.showSkill
assert(loadstring(source))();assert(handbook.showSkill==patched)
ui._localSkillRestore()
assert(handbook.showSkill==originalList and handbook.showHandbookDetail==originalDetail)
return {'internal and blank tiles filtered without deleting templates','Rulai opens without formation state',
 'Rulai preview ignores stale owner bonus and restores selection','other details forwarded unchanged',
 'temporary state restored on errors','install is idempotent and restore removes hooks'}
