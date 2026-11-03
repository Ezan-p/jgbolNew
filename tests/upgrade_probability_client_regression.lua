-- Native picker contracts: skill callbacks capture a label; stone callbacks
-- inherit createStoneMutilSelectLayer's environment and create a fresh label.
local function label(text)
 return {text=text,setString=function(self,s) self.text=s end,getString=function(self) return self.text end}
end
local ui={g_packageItemsInfo={},getDateFormServer=function() end,showPackage=function() end,refreshPackage=function() end}
local skill={g_self={params={skill_info={attach_type=6,count=45}}}}
local stone={g_stoneUpgradeUI={}}
local ms={d_packageUI=ui,d_skillUpgradeUI=skill,d_stoneUpgradeUI=stone,
 d_hz={gethz=function(key) return key=='skill_up_add_rate' and '补偿概率' or '成功率：' end},
 d_u={createByStyle=function(style) return label(style.string) end},
 d_selectLayer={createSelectLayer=function(parent,items,options) skill.options=options end}}
package.loaded.ms=ms
local skillEnv=setmetatable({d_ms=ms,g_self=skill.g_self},{__index=_G})
skill.createSkillMutilSelectLayer=setfenv(function()
 local upgrade_rate_lable=label('')
 local function update(worth)
  local rate=math.min(100,math.floor(worth*100/2))+g_self.params.skill_info.count
  g_self.succ_rate=rate
  upgrade_rate_lable:setString('成功率：'..rate..'% (补偿概率: +'..g_self.params.skill_info.count..'%)')
 end
 d_ms.d_selectLayer.createSelectLayer(nil,{}, {touchCellFunc=update,selectAllFunc=update,
  unSelectAllFunc=update,ensureFilterCallback=update})
 return upgrade_rate_lable
end,skillEnv)
local stoneEnv=setmetatable({d_ms=ms,g_stoneUpgradeUI=stone.g_stoneUpgradeUI},{__index=_G})
stone.show=function(parent,zOrder,item) stone.g_stoneUpgradeUI.stone=item end
stone.createStoneMutilSelectLayer=setfenv(function()
 local targetStone=g_stoneUpgradeUI.stone
 return function(worth)
  local rate=math.min(1,worth/2+targetStone.prob_compen/100)
  return d_ms.d_u.createByStyle({type='label',string='成功率：'..math.floor(rate*100)..'%(补偿概率: +'..targetStone.prob_compen..'%)'})
 end
end,stoneEnv)
local originalSkill,originalStone=skill.createSkillMutilSelectLayer,stone.createStoneMutilSelectLayer
local originalShow=stone.show
-- INSTALL_PATCH
local rateLabel=skill.createSkillMutilSelectLayer()
for _,key in ipairs({'touchCellFunc','selectAllFunc','unSelectAllFunc','ensureFilterCallback'}) do
 skill.g_self.params.skill_info.count=45
 skill.options[key](0.8)
 assert(rateLabel.text=='成功率：40%',key..': '..rateLabel.text)
 assert(skill.g_self.succ_rate==40)
end
skill.options.unSelectAllFunc(0);assert(rateLabel.text=='成功率：0%')
skill.options.selectAllFunc(3);assert(rateLabel.text=='成功率：100%')
for tid=1090,1092 do
 local item={attach_type=5,type_id=tid,count=3,prob_compen=40}
 stone.show(nil,100,item)
 assert(item.prob_compen==0 and item.count==3)
 item.prob_compen=80
 local update=stone.createStoneMutilSelectLayer()
 assert(update(0.8).text=='成功率：40%')
 assert(update(3).text=='成功率：100%')
 assert(update(0).text=='成功率：0%')
end
local unrelated={attach_type=5,type_id=1001,count=7,prob_compen=29}
local spell={attach_type=6,id=1,count=9}
local gem={attach_type=5,type_id=1090,count=8,prob_compen=45}
ui.getDateFormServer({attach_list={spell,gem,unrelated}})
assert(spell.count==0 and gem.count==8 and gem.prob_compen==0 and unrelated.prob_compen==29)
assert(ms.d_u.createByStyle({string='成功率：40%(补偿概率: +0%)'}).text=='成功率：40%(补偿概率: +0%)')
ui._localSkillRestore()
assert(skill.createSkillMutilSelectLayer==originalSkill and getfenv(originalSkill)==skillEnv)
assert(stone.createStoneMutilSelectLayer==originalStone and getfenv(originalStone)==stoneEnv)
assert(stone.show==originalShow)
return {'all skill selection callbacks omit compensation','stone picker omits compensation for all three types',
 'zero and capped rates preserved','legacy packets cleared without changing quantities or other progress',
 'other UI labels untouched','native environments and entry points restored'}
