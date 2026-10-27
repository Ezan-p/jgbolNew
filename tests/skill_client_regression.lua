local ui={g_packageItemsInfo={},g_reorgItemsInfo={[6]={}},g_isPackageSorted=true,packageTagDef={skill=4}}
local upgrade={g_self={}}
upgrade.show=function(params)
 if params then upgrade.g_self.params=params end
 local item=upgrade.g_self.params.skill_info
 upgrade.rendered={level=item.level,effect=item.effect_value,count=item.count}
end
upgrade.showServerRet=function(data)
 upgrade.g_self.old_level=data.old_level;upgrade.g_self.new_level=data.new_level
 upgrade.g_self.target_skill_level=data.new_level
 upgrade.show()
end
local originalUpgradeShow,originalUpgradeResult=upgrade.show,upgrade.showServerRet
package.loaded.ms={d_packageUI=ui,d_skillUpgradeUI=upgrade}
ui.sortItems=function()
 ui.g_reorgItemsInfo={[6]={}}
 for _,v in ipairs(ui.g_packageItemsInfo) do if v.attach_type==6 then table.insert(ui.g_reorgItemsInfo[6],v) end end
 ui.g_isPackageSorted=true
end
ui.getDateFormServer=function(d)
 if d.first_send then ui.g_packageItemsInfo=d.attach_list
 else for _,v in ipairs(d.attach_list) do table.insert(ui.g_packageItemsInfo,v) end end
 if d.more then ui.g_isPackageSorted=false else ui.sortItems() end
end
local function filter()
 local ss=ui.g_reorgItemsInfo[6]
 for i=#ss,1,-1 do if ss[i].protogenic~=0 then table.remove(ss,i) end end
 return #ss
end
ui.showPackage=filter;ui.refreshPackage=filter
local original=ui.getDateFormServer
-- INSTALL_PATCH
local first={id=1,attach_type=6,type_id=22,level=1,count=0,protogenic=0,effect_value=100}
local innate={id=2,attach_type=6,type_id=209,level=1,count=0,protogenic=1}
ui.getDateFormServer({first_send=true,attach_list={first,innate}})
assert(ui.showPackage(4)==1 and #ui.g_reorgItemsInfo[6]==2)
assert(ui.refreshPackage()==1 and #ui.g_reorgItemsInfo[6]==2)
local detached={id=1,attach_type=6,type_id=22,level=1,count=0,protogenic=0,effect_value=100}
upgrade.show({skill_info=detached})
assert(upgrade.g_self.params.skill_info==first)
ui.getDateFormServer({first_send=true,more=true,attach_list={}})
ui.getDateFormServer({first_send=false,attach_list={{id=1,attach_type=6,type_id=22,level=2,count=5,protogenic=0,effect_value=120}}})
assert(ui.g_packageItemsInfo[1]==first and first.level==2 and first.count==5)
-- Also repair a window which was already open before the adapter was installed.
upgrade.g_self.params.skill_info=detached
upgrade.showServerRet({obj_id=1,old_level=1,new_level=2})
assert(upgrade.rendered.level==2 and upgrade.rendered.effect==120 and upgrade.rendered.count==5)
assert(upgrade.g_self.old_level==1 and upgrade.g_self.new_level==2)
assert(detached.level==2 and detached.effect_value==120)
ui.getDateFormServer({first_send=true,attach_list={{id=1,attach_type=6,type_id=22,level=3,count=0,protogenic=0,effect_value=140}}})
assert(ui.g_packageItemsInfo[1]==first and first.level==3 and first.count==0)
upgrade.showServerRet({obj_id=1,old_level=2,new_level=3})
assert(upgrade.rendered.level==3 and upgrade.rendered.effect==140 and upgrade.rendered.count==0)
ui.getDateFormServer({first_send=true,attach_list={{id=1,attach_type=6,type_id=22,level=3,count=1,protogenic=0,effect_value=140}}})
upgrade.showServerRet({obj_id=1,old_level=3,new_level=3})
assert(upgrade.rendered.level==3 and upgrade.rendered.count==1)
ui.getDateFormServer({first_send=true,attach_list={}})
assert(#ui.g_packageItemsInfo==0)
ui.getDateFormServer({first_send=false,attach_list={{id=1,attach_type=6,type_id=23,level=3,count=0,protogenic=0}}})
assert(ui.g_packageItemsInfo[1]~=first and ui.g_packageItemsInfo[1].type_id==23)
upgrade.show({skill_info=first})
assert(upgrade.g_self.params.skill_info==first,'different templates must not be rebound')
ui.g_isInPackage=true
ui.g_packageUI={board_layer={removeChildByTag=function() error('released Cocos node') end}}
ui._localSkillRestore();assert(ui.getDateFormServer==original)
assert(upgrade.show==originalUpgradeShow and upgrade.showServerRet==originalUpgradeResult)
return {'category does not delete innate entries','chunked snapshot keeps selected object','copied formation selection binds to live spell','already open result uses current level and power','consecutive growth refreshes level and compensation','failure refreshes compensation without another level','consumed books disappear','conversion does not retain wrong type cache','adapter restores original functions'}
