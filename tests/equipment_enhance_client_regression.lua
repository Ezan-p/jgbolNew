-- Isolated control-flow fixture from equipmentUpgradeUI:691-787. Cocos nodes
-- are stubs; the delayed callback and unconditional terminal gray are retained.
local source=...
local checks={}
local function check(name,ok) assert(ok,name);checks[#checks+1]=name end
local queue={}
local function button()
 return {gray=false,visible=true,setVisible=function(self,value) self.visible=value end}
end
local nativeGray=function(b,enabled) b.gray=true;b.enabled=enabled;return 'native' end
local ms={d_u={grayMenuItem=nativeGray,delay=function(_,_,fn) queue[#queue+1]=fn end},
 d_mainUI={g_playerInfo={level=99,silver_coin=100000,vip_level=3}}}
local ui={d_ms=ms,g_self={},g_equipment_upgrade={},g_skill_anim_on=false}
ms.d_equipmentUpgradeUI=ui
package.loaded.ms=ms
ui.checkEquipmentCanUpgrade=function()
 local p=ms.d_mainUI.g_playerInfo
 if ui.g_equipment_upgrade.item_table.level>=p.level*2 then return 2 end
 if p.silver_coin<50 then return 1 end
 return 0
end
ui.checkCanBatchUpgrade=function() return ms.d_mainUI.g_playerInfo.vip_level>=3 end
ui.createEnhanceLayer=function()
 ui.g_enhanceButtons={button(),button(),button(),button()}
 ui.g_enhanceButtons[4]:setVisible(false)
 if ui.checkEquipmentCanUpgrade(false)==2 then
  nativeGray(ui.g_enhanceButtons[2]);nativeGray(ui.g_enhanceButtons[3])
 end
 if not ui.checkCanBatchUpgrade(false) then nativeGray(ui.g_enhanceButtons[3]) end
end
local native=assert(loadstring([[
return function(ret)
 g_skill_anim_on=false
 if not ret.upgrade_list or not ret.upgrade_list[1] then return end
 if g_self.g_req_is_inbatch==true then g_skill_anim_on=true end
 local index=0
 showEquitInfo=function()
  index=index+1
  if not ret.upgrade_list[index] then
   g_skill_anim_on=false
   g_enhanceButtons[3]:setVisible(true)
   g_enhanceButtons[4]:setVisible(false)
   if #ret.upgrade_list>1 then
    d_ms.d_u.grayMenuItem(g_enhanceButtons[2])
    d_ms.d_u.grayMenuItem(g_enhanceButtons[3])
   end
   return
  end
  if g_skill_anim_on==false then index=#ret.upgrade_list end
  g_self.new_level=ret.upgrade_list[index].new_level
  g_self.old_level=ret.upgrade_list[index].old_level
  if index==#ret.upgrade_list then g_skill_anim_on=false end
  createEnhanceLayer()
  if g_skill_anim_on~=false then
   g_enhanceButtons[3]:setVisible(false)
   g_enhanceButtons[4]:setVisible(true)
  end
  d_ms.d_u.delay(g_self.main_layer,0.6,showEquitInfo)
 end
 showEquitInfo()
end
]]))()
setfenv(native,ui)
ui.changeEquipmentInfo=native
local function start(count,options)
 options=options or {}
 queue={}
 local old=options.old or 1
 ms.d_mainUI.g_playerInfo.silver_coin=options.silver or 100000
 ms.d_mainUI.g_playerInfo.vip_level=options.vip or 3
 ui.g_self={g_req_is_inbatch=options.batch~=false,main_layer={}}
 ui.g_equipment_upgrade={item_table={level=old+count}}
 local ret={upgrade_list={}}
 for n=1,count do ret.upgrade_list[n]={old_level=old+n-1,new_level=old+n} end
 ui.changeEquipmentInfo(ret)
end
local function drain()
 local n=0
 while #queue>0 do
  local fn=table.remove(queue,1);fn();n=n+1
  assert(n<30,'animation failed to stop')
 end
end
start(10);drain()
check('baseline reproduces gray below cap',ui.g_enhanceButtons[2].gray and ui.g_enhanceButtons[3].gray)
assert(loadstring(source))()
local adapted=getfenv(native)
assert(loadstring(source))()
check('repeat injection is idempotent',getfenv(native)==adapted)
check('shared utility remains untouched',ms.d_u.grayMenuItem==nativeGray and ui.d_ms==ms)
start(10)
check('batch retains animation and skip control',ui.g_skill_anim_on and not ui.g_enhanceButtons[3].visible and ui.g_enhanceButtons[4].visible)
drain()
check('completed batch can strengthen again',not ui.g_enhanceButtons[2].gray and not ui.g_enhanceButtons[3].gray)
check('animation settles at exact final level',ui.g_self.new_level==11 and ui.g_skill_anim_on==false)
check('normal buttons restored after animation',ui.g_enhanceButtons[3].visible and not ui.g_enhanceButtons[4].visible)
start(10,{old=11});drain()
check('second batch remains available',ui.g_self.new_level==21 and not ui.g_enhanceButtons[3].gray)
start(10);ui.g_skill_anim_on=false;drain()
check('skip animation does not gray buttons',ui.g_self.new_level==11 and not ui.g_enhanceButtons[2].gray and not ui.g_enhanceButtons[3].gray)
start(1,{batch=false});drain()
check('single enhancement preserved',ui.g_self.new_level==2 and not ui.g_enhanceButtons[2].gray)
start(2,{silver=0});drain()
check('insufficient silver retains native gray',ui.g_enhanceButtons[2].gray and ui.g_enhanceButtons[3].gray)
start(2,{old=196});drain()
check('level cap retains native gray',ui.g_enhanceButtons[2].gray and ui.g_enhanceButtons[3].gray)
start(2,{vip=2});drain()
check('VIP gate remains on batch only',not ui.g_enhanceButtons[2].gray and ui.g_enhanceButtons[3].gray)
local other=button()
check('unrelated buttons delegate unchanged',adapted.d_ms.d_u.grayMenuItem(other,false)=='native' and other.gray and other.enabled==false)
start(10)
ui._localEnhanceButtonsRestore()
drain()
check('restore also disables pending callback correction',ui.g_enhanceButtons[2].gray and ui.g_enhanceButtons[3].gray)
check('native environment restored',getfenv(native)==ui and ui._localEnhanceButtonsRestore==nil)
assert(loadstring(source))()
start(10);drain()
check('reinstall works',not ui.g_enhanceButtons[2].gray and not ui.g_enhanceButtons[3].gray)
return checks
