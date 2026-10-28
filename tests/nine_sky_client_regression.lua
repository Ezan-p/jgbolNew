-- Lua 5.1 regression for clock boundaries, stale offer guards and movement ownership.
local function copy(value)
 if type(value)~='table' then return value end
 local out={};for k,v in pairs(value) do out[k]=copy(v) end;return out
end
local function node()
 local n={children={}}
 function n:addChild(child,z,tag) child.parent=self;child.tag=tag;self.children[#self.children+1]=child end
 function n:getChildByTag(tag) for _,child in ipairs(self.children) do if child.tag==tag then return child end end end
 function n:removeChildByTag(tag) for i=#self.children,1,-1 do if self.children[i].tag==tag then self.children[i].parent=nil;table.remove(self.children,i) end end end
 function n:getParent() return self.parent end
 function n:getContentSize() return {width=300,height=30} end
 function n:setScale(v) self.scale=v end
 return n
end
CCLayerColor={create=function() return node() end}
CCDirector={sharedDirector=function() return {getVisibleSize=function() return {width=960,height=640} end} end}
function ccc4(...) return {...} end
local now=1000;local sent,notices,delays,styles={},{},{},{}
local root=node()
local ms={d_c={table_copy=copy},d_u={},d_time={},d_hz={},d_info={}}
ms.d_time.getTime=function() return now end
ms.d_time.getRestTime=function() return 'native countdown' end
ms.d_hz.gethz=function(key) return key end
ms.d_info.show=function(text) notices[#notices+1]=text end
ms.d_u.createByStyle=function(style) styles[#styles+1]=copy(style);local n=node();n.text=style.string;return n end
ms.d_u.getRealScale=function() return 0.8,0.8 end
ms.d_u.delay=function(layer,seconds,callback) delays[#delays+1]={layer=layer,callback=callback} end
ms.d_u.createMenu=function() return node() end
ms.d_u.createSwallowTouchLayer=function() end
local ui={g_self={Tags={Shop=1,Buy=2,Time=5},shop_data={},role_shop_data={}},g_towerUI={}}
ms.d_towerUI=ui;package.loaded.ms=ms
ui.updateActivityStatus=function(d) ui.g_self.begin_time=d.begin_time;ui.g_self.end_time=d.end_time end
ui.canJoin=function() return false end
ui.sendRequest=function(op,data) sent[#sent+1]={op=op,data=copy(data)} end
ui.getTowerFloor=function(steps) return steps>99999 and 10 or 1 end
ui.processCardList=function(cards) return copy(cards) end
ui.showDynamicInfo=function() end;ui.showTokenCount=function() end;ui.showTopPlayer=function() end
ui.showFloorTitle=function() end;ui.showGameLayer=function() end;ui.cancelSwallow=function() end
ui.getItemName=function(reward) return reward.object_type==1 and '100天星卡' or 'VIP乾坤袋' end
ui.create=function()
 ui.g_towerUI.bw=0.8;ui.g_towerUI.bh=0.3
 ms.d_u.createByStyle({pic='v2/towerUI/p_label1.png',x=0.2,y=0.2})
 assert(ms.d_time.getRestTime()==nil,'native timer must be suppressed during local render')
end
ui.showShopLayer=function(page)
 local layer=node();ui.g_towerUI.main_layer:addChild(layer,1,1);ui.g_towerUI.shopType=page
 ms.d_u.createByStyle({pic='v2/towerUI/s_bkg.png'})
 ms.d_u.createByStyle({type='label',string='upgrade_role_t2'})
 assert(ms.d_time.getRestTime()==nil)
end
ui.showComplexBuyLayer=function() ui.g_towerUI.main_layer:addChild(node(),2,2) end
ui.clearTinaInfo=function()
 ui.g_self.special_shop_data=nil;ui.g_self.special_role_shop_data=nil
 ui.g_self.shop_data[3]=nil;ui.g_self.shop_data[4]=nil
end
ui.onGetActResult=function(d)
 if d.flag==1 then
  assert(not d.tina_shop,'entry must not replay a palace encounter')
  ui.g_self.role_data=copy(d.role_sky_data or d.local_snapshot)
  ui.g_towerUI.main_layer=node();root:addChild(ui.g_towerUI.main_layer);ui.create()
 elseif d.flag==3 then
  ui.g_self.shop_data[d.shop_type]=d.shop_data;ui.g_self.role_shop_data[d.shop_type]={0,0}
  ui.showShopLayer(d.shop_type)
 elseif d.flag==5 then
  assert(ui.g_self.shop_data[3],'day refresh must preserve a paused palace catalog')
 end
end
local originals=copy(ui)
-- INSTALL_PATCH
local function snapshot(day,week)
 return {steps=0,stars=100,credits=30,free_times=5,end_time=week or 2000,cur_map=0,cur_point={x=0,y=0},
  local_permanent=true,local_enabled=true,next_daily_refresh=day or 1100,next_weekly_refresh=week or 2000,
  shop_day=1,shop_revision='r1'}
end
local function response(flag,s,extra)
 local d={flag=flag,local_snapshot=copy(s),local_cards={},local_top={}}
 for k,v in pairs(extra or {}) do d[k]=v end
 ui.onGetActResult(d);return d
end
local checks={}
local function check(name,fn) fn();checks[#checks+1]=name end
local s=snapshot()
check('permanent entry and week label',function()
 ui.updateActivityStatus(s);response(1,s)
 assert(ui.canJoin());assert(styles[1].string=='周重置倒计时')
 assert(ms.d_time.getRestTime()=='native countdown')
 assert(ui.g_towerUI.main_layer:getChildByTag(5).text=='0天 00:16:40')
end)
check('reentry suppresses legacy palace and clears cached encounter',function()
 for _,sold in ipairs({false,true}) do
  ui.g_self.tinaIndex=3;ui.g_self.special_shop_data={{}}
  ui.g_self.special_role_shop_data={sold and 1 or 0};ui.g_self.shop_data[3]={{}}
  local legacy={shop_index=3,role_buy_list={{sold and 1 or 0},{sold and 2 or 0,sold and 2 or 0}}}
  local d=response(1,s,{tina_shop=legacy})
  assert(d.tina_shop==legacy,'do not mutate replay packet')
  assert(not ui.g_self.tinaIndex and not ui.g_self.special_shop_data and not ui.g_self.shop_data[3])
 end
end)
check('always fetch full catalog and bind purchase version',function()
 ui.sendRequest(3,{buy_type=1,first_send=false});assert(sent[#sent].data.first_send)
 response(3,s,{shop_type=1,shop_data={{}}})
 ui.sendRequest(4,{buy_type=1,index=1,count=1})
 assert(sent[#sent].op==4 and sent[#sent].data.shop_day==1 and sent[#sent].data.shop_revision=='r1')
 assert(ui.g_towerUI.main_layer:getChildByTag(1):getChildByTag(11).text=='00:01:40')
end)
check('midnight blocks stale purchase and refreshes visible page',function()
 ui.showComplexBuyLayer(1);now=1100
 ui.sendRequest(4,{buy_type=1,index=1,count=1})
 assert(sent[#sent].op==3 and sent[#sent].data.buy_type==1)
 local count=#sent;ui._localNineSkyTick();assert(#sent==count,'refresh requests must be throttled')
 local new=copy(s);new.shop_day=2;new.next_daily_refresh=1200
 response(3,new,{shop_type=1,shop_data={{fresh=true}}});s=new
 assert(not ui.g_towerUI.main_layer:getChildByTag(2))
 assert(ui.g_self.shop_data[1][1].fresh and not ui.g_self.shop_data[2])
 ui.sendRequest(4,{buy_type=1,index=1,count=1});assert(sent[#sent].data.shop_day==2)
end)
check('revision update rejects other page cached version',function()
 response(3,s,{shop_type=2,shop_data={{}}})
 local new=copy(s);new.shop_revision='r2';now=1104
 response(3,new,{shop_type=1,shop_data={{fresh=true}}});s=new
 ui.sendRequest(4,{buy_type=2,index=1,count=1})
 assert(sent[#sent].op==3 and sent[#sent].data.buy_type==2)
end)
check('exact Monday remains open and blocks old-week movement',function()
 now=2000;assert(ui.canJoin())
 ui.sendRequest(2,{count=10,index=1});assert(sent[#sent].op==1)
 local new=snapshot(2100,3000);new.shop_day=3
 response(1,new);s=new
 assert(ui.g_self.role_data.steps==0 and ui.canJoin())
end)
check('moving batch owns coordinates and defers refresh until final callback',function()
 local after=copy(s);after.steps=40;after.stars=250;after.free_times=6
 local battle={floor=2,enemy_name='天将',won=true,rewards={{object_type=1,attach_count=1}}}
 response(2,after,{local_battles={battle,{floor=3,enemy_name='守军',won=false,rewards={}}}})
 ui.g_self.role_data.steps=10;ui.cancelSwallow()
 assert(ui.g_self.role_data.steps==10 and not ui.g_towerUI.main_layer:getChildByTag(91037))
 now=2101;local count=#sent;ui._localNineSkyTick();assert(#sent==count)
 ui.g_self.role_data.steps=40;ui.cancelSwallow()
 assert(ui.g_self.role_data.stars==250 and ui.g_self.role_data.free_times==6)
 local panel=ui.g_towerUI.main_layer:getChildByTag(91037);assert(panel)
 assert(panel:getChildByTag(11).text:find('胜利') and panel:getChildByTag(11).text:find('100天星卡'))
 assert(panel:getChildByTag(12).text:find('未获胜'))
 assert(sent[#sent].op==1)
end)
check('palace balances during paused movement survive final snapshot',function()
 now=2200;s=snapshot(2300,3000);s.shop_day=4;response(1,s)
 ui.g_self.shop_data[3]={{}};ui.g_self.shop_data[4]={{}}
 local after=copy(s);after.steps=50;after.stars=300
 response(2,after)
 ui.g_self.role_data.steps=20;ui.g_self.role_data.stars=180
 local bought=copy(after);bought.free_times=8;bought.shop_day=5;bought.next_daily_refresh=2400
 response(5,bought,{local_cards={[100]=1}})
 assert(ui.g_self.role_data.steps==20 and ui.g_self.role_data.free_times==8)
 assert(ui.g_self.shop_data[3] and ui.g_self.shop_data[4])
 ui.g_self.role_data.steps=50;ui.cancelSwallow()
 assert(ui.g_self.role_data.free_times==8 and ui.g_self.card_list[100]==1)
end)
check('request crossing Monday starts from reset coordinates',function()
 now=2999;s=snapshot(3000,3000);s.steps=600;s.cur_point={x=2,y=80};response(1,s)
 local before=snapshot(4000,9000);before.shop_day=6
 local after=copy(before);after.steps=3;after.stars=15
 response(2,after,{local_before_snapshot=before})
 assert(ui.g_self.role_data.steps==0 and ui.g_self.role_data.cur_point.y==0)
 ui.g_self.role_data.steps=3;ui.cancelSwallow();assert(ui.g_self.role_data.stars==15)
end)
check('ninth title clamp and complete restoration',function()
 ui.g_self.role_data.floor=10;ui.showFloorTitle();assert(ui.g_self.role_data.floor==9)
 ui.updateActivityStatus({begin_time=0,end_time=0});assert(not ui.canJoin())
 ui._localNineSkyRestore();assert(ui.onGetActResult==originals.onGetActResult)
 assert(ui.sendRequest==originals.sendRequest and not ui._localNineSkyTick)
end)
return checks
