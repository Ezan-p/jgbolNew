-- Native resource instrumentation layered over the isolated battle harness.
local ext=ms.d_skillExt
local oldStyle,oldAnimation,oldNew=ms.d_u.createByStyle,ms.d_u.createAnimation,ms.d_u.createAnimation_new
local oldName=ext.showSkillExtName
local oldStart,oldCheck,oldRestore=battlePipelineStart,battlePipelineCheck,battlePipelineRestore
local visualStats
ms.d_u.createByStyle=function(options,...)
 local node=oldStyle(options,...)
 local pic=options.pic
 if visualStats and pic and string.match(pic,'^skill/ext/%d+n%.png$') then
  assert(node and node:getContentSize().width>0,'missing name sprite: '..pic)
  visualStats.names[pic]=(visualStats.names[pic] or 0)+1
  ms.d_u.delay(fight.g_fightUI.layerFrontground,0.05,function()
   if node:isRunning() then visualStats.visible_names[pic]=(visualStats.visible_names[pic] or 0)+1 end
  end)
 end
 return node
end
local function animation(original,resource,...)
 local node=original(resource,...)
 if visualStats then
  assert(node,'missing animation node: '..tostring(resource))
  visualStats.animations[resource]=(visualStats.animations[resource] or 0)+1
 end
 return node
end
ms.d_u.createAnimation=function(resource,...) return animation(oldAnimation,resource,...) end
ms.d_u.createAnimation_new=function(resource,...) return animation(oldNew,resource,...) end
ext.showSkillExtName=function(value,...)
 if visualStats then
  visualStats.codes[tostring(value.logic_type)]=(visualStats.codes[tostring(value.logic_type)] or 0)+1
  visualStats.name_steps[#visualStats.name_steps+1]={code=value.logic_type,step=fight.g_fightUI.iAttackStep}
 end
 return oldName(value,...)
end
function battlePipelineStart(name)
 visualStats={names={},visible_names={},animations={},codes={},name_steps={}}
 return oldStart(name)
end
function battlePipelineCheck(name)
 local result=table.loadstring(oldCheck(name))
 for _,pic in ipairs(fixtures.expected_names[name]) do
  assert(visualStats.names[pic],'native name not created: '..pic)
  assert(visualStats.visible_names[pic],'native name not attached to running scene: '..pic)
 end
 for _,resource in ipairs(fixtures.expected_art[name]) do
  assert(visualStats.animations[resource],'native animation not created: '..resource)
 end
 if string.find(name,'reserve',1,true) then
  for _,event in ipairs(fixtures[name].fight_events) do
   if event.logic_type%1000==181 then
    local found=false
    for _,shown in ipairs(visualStats.name_steps) do
     if shown.code==event.logic_type then
      assert(shown.step==event.cur_action+1,'blessing appeared before reserve deployment')
      found=true
     end
    end
    assert(found,'reserve blessing name missing')
   end
  end
 end
 result.visuals=visualStats
 return table.tostring(result)
end
function battlePipelineRestore()
 ms.d_u.createByStyle=oldStyle;ms.d_u.createAnimation=oldAnimation;ms.d_u.createAnimation_new=oldNew
 ext.showSkillExtName=oldName
 return oldRestore()
end
