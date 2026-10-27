-- Lua 5.1 callback regression without a running Cocos client.
-- Native-like layer removal exposes stale-stage bugs in settlement navigation.
local function node(w,h)
 local n={children={},width=w or 960,height=h or 640,enabled=true}
 function n:addChild(child,z,tag) child.parent=self;child.tag=tag or child.tag;self.children[#self.children+1]=child end
 function n:removeChildByTag(tag) local c=self:getChildByTag(tag);if c then c:removeFromParentAndCleanup(true) end end
 function n:getChildByTag(tag) for _,c in ipairs(self.children) do if c.tag==tag then return c end end end
 function n:removeFromParentAndCleanup()
  if self.parent then for i,c in ipairs(self.parent.children) do if c==self then table.remove(self.parent.children,i);break end end end
  self.parent=nil
 end
 function n:getParent() return self.parent end
 function n:setTag(v) self.tag=v end
 function n:setColor(v) self.color=v end
 function n:setPosition(x,y) self.position=type(x)=='table' and x or {x=x,y=y} end
 function n:setScale(v) self.scale=v end
 function n:setAnchorPoint(v) self.anchor=v end
 function n:setEnabled(v) self.enabled=v end
 function n:getContentSize() return {width=self.width,height=self.height} end
 function n:registerScriptTapHandler(fn) self.callback=fn end
 function n:tap() if self.enabled then return self.callback() end end
 return n
end
function ccp(x,y) return {x=x,y=y} end
function ccc3(...) return {...} end
function ccc4(...) return {...} end
CCLayer={create=function() return node() end}
CCLayerColor={create=function(_,color,w,h) return node(w,h) end}
CCLabelTTF={create=function(_,text,font,size) local n=node(#text*size/3,size);n.text=text;return n end}
CCMenuItemLabel={create=function(_,label) local n=node();n:addChild(label);return n end}
CCMenuItemSprite={create=function(_,normal,selected) local n=node(normal.width,normal.height);n.normal=normal;n.selected=selected;return n end}
CCMenu={createWithItem=function(_,item) local n=node();n.item=item;n:addChild(item);return n end}
local scene=node()
CCDirector={sharedDirector=function() return {getWinSize=function() return {width=960,height=640} end} end}
local sent,popups,rendered={},0,{}
local root=node();scene:addChild(root)
local ms={d_mainUI={g_playerInfo={level=60}},d_info={show=function() end},d_time={getRestTime=function() end},d_hz={gethz=function(k) return k end},d_u={}}
ms.d_data={getBodySprite=function() return node(300,500) end}
ms.d_u.setProperties=function(parent,n,props) n.position=props end
ms.d_u.createByStyle=function() return node() end
ms.d_u.createSwallowTouchLayer=function() end
ms.d_u.remove=function(n) n:removeFromParentAndCleanup(true) end
ms.d_u.delay=function() error('Arena return must render synchronously') end
ms.d_u.createMenu=function(config)
 local n=node();for _,item in ipairs(config) do local b=node();b:registerScriptTapHandler(item.call_back);n:addChild(b) end;return n
end
ms.d_commonLayerUI={showPrizeResLayer=function(parent,list) assert(#list==2);popups=popups+1 end}
ms.d_undergoMapUI={show=function() end,canFightNextChallenge=function() end}
ms.d_undergoOrdealUI={enter=function() end,pressEnterUndergoLayer=function() end,getMainLayer=function() return root end}
ms.d_event_mgr={setSpecialFightType=function() end}
local ui={g_data={},g_arenaUI={parent_layer=root}}
ms.d_arenaUI=ui;package.loaded.ms=ms
ui.enter=function() end
ui.sendRequest=function(id,data) sent[#sent+1]={id=id,data=data} end
local function render(name,parent)
 parent=parent or ui.g_arenaUI.main_layer
 local n=node();parent:addChild(n)
 ui.g_arenaUI[name=='showQualifyFight' and 'qualify_layer' or name=='showBloodFight' and 'blood_layer' or 'rank_parent']=n
 local close=node();close:registerScriptTapHandler(function() ms.d_u.remove(n) end);n:addChild(close);n.close=close
 rendered[#rendered+1]=name
end
for _,name in ipairs({'showQualifyFight','showExerFight','showBloodFight','showCommonRank','showDoubleRank'}) do ui[name]=function(parent) render(name,parent) end end
ui.show=function() error('Seven-group carousel must not run') end
ui.onFightReturn=function(record) ms.d_event_mgr.setSpecialFightType(0);ui.show(ms.d_undergoOrdealUI.getMainLayer(),0,record) end
ui.onGetResult=function(data)
 if data.id==1 then error('Native entry requires seven groups') end
 if data.id==2 then
  ui.g_data.rank=data
  if not data.event_info.in_rank then
   ui[data.enter_group==7 and 'showDoubleRank' or 'showCommonRank']()
  else ui[data.rank_type==1 and 'showQualifyFight' or data.rank_type==2 and 'showExerFight' or 'showBloodFight']() end
 end
end
ui.showPrize=function() end
ui.showBloodHis=function(parent) assert(parent);rendered[#rendered+1]='history' end
local originalShow,originalReturn=ui.show,ui.onFightReturn
assert(loadfile('network_redirect/taixu_client.lua'))()
local patched=ui.show;assert(loadfile('network_redirect/taixu_client.lua'))();assert(patched==ui.show)
local groups={};for g=4,7 do groups[g]={min_level=50+(g-4)*10,max_level=g==7 and 99 or 59+(g-4)*10} end
ui.onGetResult({id=1,role_group=5,group_type_level=groups,schedule_list={match_time_list={{},{},{start_time=1}}}})
for g=4,7 do
 local menu=assert(ui.g_arenaUI.main_layer:getChildByTag(9900+g));menu.item:tap()
 assert(sent[#sent].id==2 and sent[#sent].data.enter_group==g)
end
for g=1,3 do assert(not ui.g_arenaUI.main_layer:getChildByTag(9900+g)) end
local function board(stage,ready,group)
 return {id=2,enter_group=group or 5,rank_type=math.min(stage,3),rank_data={},event_info={in_rank=stage<6},
  local_arena={title='阶段',stage=stage,stage_fights=ready and 1 or 0,can_advance=ready,own=true,settled=stage==6}}
end
for stage=1,5 do
 ui.onGetResult(board(stage,false))
 local p=ui.g_arenaUI[stage==1 and 'qualify_layer' or stage==2 and 'rank_parent' or 'blood_layer']
 local menu=p:getChildByTag(9876):getChildByTag(9878)
 local count=#sent;assert(not menu.item.enabled);menu.item:tap();assert(#sent==count)
 ui.onGetResult(board(stage,true))
 p=ui.g_arenaUI[stage==1 and 'qualify_layer' or stage==2 and 'rank_parent' or 'blood_layer']
 menu=p:getChildByTag(9876):getChildByTag(9878);assert(menu.item.enabled)
 menu.item:tap();assert(sent[#sent].id==7 and sent[#sent].data.stage==stage)
 count=#sent;local before=#rendered;ui.onFightReturn(false)
 assert(#sent==count and #rendered==before+1)
end
ui.onFightReturn(true);assert(rendered[#rendered]=='history')
for _,group in ipairs({5,7}) do
 ui.onGetResult(board(5,true,group));local previous=ui.g_arenaUI.main_layer
 local settlement=board(6,false,group);settlement.local_prizes={{object_type=11},{object_type=5}}
 ui.onGetResult(settlement)
 assert(not previous:getParent() and not ui.g_arenaUI.blood_layer)
 local rank=ui.g_arenaUI.rank_parent;rank.close:tap();assert(not rank:getParent())
 for g=4,7 do assert(ui.g_arenaUI.main_layer:getChildByTag(9900+g)) end
 local count=popups;ui.onGetResult(board(6,false,group));assert(popups==count)
end
ui._localTaixuRestore();assert(ui.show==originalShow and ui.onFightReturn==originalReturn)
print('taixu client regression passed: four groups, enabled/disabled stage buttons, five synchronous returns, record return, both settled rank closes, popup, restore')
