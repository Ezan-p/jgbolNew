-- Run the production checkout with isolated Cocos node contracts, without a save.
local source=...
local checks,sent,messages={},{},{}
local function node()
 local n={children={},enabled=true}
 function n:addChild(child,z,tag) child.parent=self;child.tag=tag or child.tag;self.children[#self.children+1]=child end
 function n:getParent() return self.parent end
 function n:removeFromParentAndCleanup()
  if self.parent then
   for i,child in ipairs(self.parent.children) do if child==self then table.remove(self.parent.children,i);break end end
  end
  self.parent=nil
 end
 function n:removeAllChildrenWithCleanup() for _,child in ipairs(self.children) do child.parent=nil end;self.children={} end
 function n:removeChildByTag(tag) for _,child in ipairs(self.children) do if child.tag==tag then child:removeFromParentAndCleanup();return end end end
 function n:getContentSize() return {width=400,height=50} end
 function n:setEnabled(value) self.enabled=value end
 function n:setTag(value) self.tag=value end
 function n:registerScriptTapHandler(fn) self.callback=fn end
 function n:activate() if self.enabled then self.callback(self.tag) end end
 for _,name in ipairs({'setColor','setPosition','setScale','setScaleX','setScaleY','setContentSize','setAnchorPoint'}) do n[name]=function() end end
 return n
end
CCNode={create=node};CCLayer={create=node};CCLayerColor={create=node};CCSprite={create=node}
CCLabelTTF={create=function(_,value) local n=node();n.text=value;return n end}
CCMenuItemSprite={create=node}
CCMenu={createWithItem=function(_,item) local n=node();n:addChild(item);return n end}
ccp=function(x,y) return {x=x,y=y} end
ccc3=function(...) return {...} end;ccc4=ccc3;CCSizeMake=ccp
local scene=node()
CCDirector={sharedDirector=function() return {
 getRunningScene=function() return scene end,
 getVisibleSize=function() return {width=960,height=640} end,
 getVisibleOrigin=function() return ccp(0,0) end} end}
table.tostring=function(data)
 local fields={};for k,v in pairs(data) do fields[#fields+1]=k..'='..(type(v)=='string' and string.format('%q',v) or tostring(v)) end
 table.sort(fields);return '{'..table.concat(fields,',')..'}'
end
local r,v={g_self={}},{}
local ms={d_rechargeUI=r,d_mainUI={g_playerInfo={},g_mainUI={}},
 d_actNoticeUI={getSprite=node},d_data={g_new_config={}},
 d_msg_def={gscl_msg_id={msg_order_request=1111}},
 d_info={show=function(value) messages[#messages+1]=value end},
 d_u={createSwallowTouchLayer=function() end,
 main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end}}
ms.d_data.callback_update_config=function(data) for k,value in pairs(data) do ms.d_data.g_new_config[k]=value end end
package.loaded.ms=ms;package.loaded['ui.vipUI']=v
assert(loadstring(source))()
local function find(tag,n)
 n=n or scene
 if n.tag==tag then return n end
 for _,child in ipairs(n.children) do local result=find(tag,child);if result then return result end end
end
local function click(tag) assert(find(tag),'missing button '..tag):activate() end
local function textContains(value,n)
 n=n or scene
 if n.text and string.find(n.text,value,1,true) then return true end
 for _,child in ipairs(n.children) do if textContains(value,child) then return true end end
 return false
end
local fund={id=202,rmb=45,name='成长基金'}
local gold={id=102,rmb=50,name='500元宝'}
local function stock(large,small,extra)
 local data={large_count=large,small_count=small,products={fund,gold}}
 for k,value in pairs(extra or {}) do data[k]=value end
 ms.d_data.callback_update_config({local_recharge=data})
end
local function check(name,fn) fn();checks[#checks+1]=name end
check('fund_auto_select_and_cancel_without_order',function()
 stock(1,0);r._localCardOpen(fund)
 assert(r._localCardSelection.large_count==1 and r._localCardSelection.small_count==0)
 click(19863);assert(#sent==0 and not r._localCardSelection.order_id)
 assert(textContains('超出 5 元不找零、不退还') and textContains('充值额度及奖励仍按商品金额计算'))
 click(19864);assert(#sent==0 and not r._localCardSelection.overpay_confirm)
 click(19863);click(19860);assert(#sent==0 and not r._localCardSelection)
end)
check('confirmed_overpayment_and_same_order_retry',function()
 r._localCardOpen(fund);click(19863);click(19865);assert(#sent==1)
 local data=assert(loadstring('return '..sent[1].data.data))()
 assert(data.item_id==202 and data.large_count==1 and data.small_count==0)
 click(19863);assert(#sent==2 and sent[1].data.data==sent[2].data.data)
 r._localCardCancel();r._localCardOpen(gold)
 assert(r._localCardSelection.product.id==202)
 click(19863);assert(sent[3].data.data==sent[1].data.data)
 stock(0,0,{last_order_id=data.order_id});assert(not r._localCardSelection)
end)
check('exact_payment_sends_without_extra_confirmation',function()
 stock(1,9);r._localCardOpen(fund)
 assert(r._localCardSelection.large_count==0 and r._localCardSelection.small_count==9)
 local n=#sent;click(19863);assert(#sent==n+1)
 stock(1,0,{last_order_id=r._localCardSelection.order_id})
end)
check('underpayment_cannot_send',function()
 stock(0,8);r._localCardOpen(fund)
 local n=#sent;assert(not find(19863).enabled)
 r._localCardConfirm();assert(#sent==n and not r._localCardSelection.order_id)
 r._localCardCancel()
end)
check('inventory_change_during_confirmation_is_rechecked',function()
 stock(1,0);r._localCardOpen(fund);click(19863)
 local n=#sent;stock(0,0);assert(not find(19865).enabled)
 click(19865);assert(#sent==n)
 -- Even a delayed callback must re-read the current stock.
 find(19865).callback();assert(#sent==n and not r._localCardSelection.overpay_confirm)
 r._localCardCancel()
end)
check('selection_change_requires_fresh_confirmation_and_failure_unlocks',function()
 stock(2,10);r._localCardOpen(gold);click(19883);click(19863)
 local n=#sent;local stale=find(19865).callback
 click(19864);click(19883);stale();assert(#sent==n)
 click(19863);assert(#sent==n);click(19865);assert(#sent==n+1)
 local data=assert(loadstring('return '..sent[#sent].data.data))()
 assert(data.large_count==1 and data.small_count==2)
 stock(2,10,{failed_order_id=data.order_id});assert(not r._localCardSelection.order_id)
 click(19863);assert(#sent==n+1 and r._localCardSelection.overpay_confirm)
 r._localCardCancel()
end)
check('closed_confirmation_cannot_submit_new_selection',function()
 stock(1,0);r._localCardOpen(fund);click(19863)
 local n=#sent;local stale=find(19865).callback
 click(19860);r._localCardOpen(gold);stale();assert(#sent==n)
 r._localCardCancel()
end)
return checks
