-- Execute against the original Cocos client with all sends captured and state restored.
local m=assert(package.loaded.ms)
local r,v=m.d_rechargeUI,m.d_vipUI
local saved,checks,sent,errors={},{},{},{}
local function preserve(t)
 if not t then return end
 local old={};for k,val in pairs(t) do old[k]=val end;saved[#saved+1]={t=t,old=old}
end
for _,t in ipairs({r,v,m.d_mainUI,m.d_data,m.d_u,m.d_recharge,m.d_monthCardUI,m.d_packageUI,m.d_actNoticeUI,m.d_c,m.d_chargePresentUI,m.d_commonLayerUI}) do preserve(t) end
local report=m.MS_report_error
m.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
local layer=CCLayer:create();layer:retain()
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]=name..':'..tostring(ok and #errors==0)..':'..(err or '')..table.concat(errors,' ')
end
local function cardButton(tag)
 local function find(node)
  if node:getTag()==tag then return tolua.cast(node,'CCMenuItem') end
  local children=node:getChildren()
  if children then for i=0,children:count()-1 do
   local hit=find(tolua.cast(children:objectAtIndex(i),'CCNode'));if hit then return hit end
  end end
 end
 return assert(find(assert(CCDirector:sharedDirector():getRunningScene():getChildByTag(19851))))
end
local ok,err=xpcall(function()
 if m.d_actNoticeUI._localWelfareRestore then m.d_actNoticeUI._localWelfareRestore() end
 if v._localVipRestore then v._localVipRestore() end
 r.g_self=m.d_c.table_copy(r.g_self);r.g_self.main_layer=nil;r.g_self.parent_layer=nil
 v.g_self=m.d_c.table_copy(v.g_self);v.g_self.main_layer=nil
 m.d_mainUI.g_playerInfo=m.d_c.table_copy(m.d_mainUI.g_playerInfo)
 m.d_mainUI.g_mainUI={main_layer=layer}
 m.d_data.g_new_config=m.d_c.table_copy(m.d_data.g_new_config)
 m.d_data.g_new_config.local_recharge=m.d_c.table_copy(FIXTURE)
 m.d_data.g_new_config.local_vip=nil
 m.d_packageUI.g_itemAttrTable=m.d_c.table_copy(m.d_packageUI.g_itemAttrTable)
 m.d_monthCardUI.g_monthCardUI={}
 m.d_actNoticeUI.g_self=m.d_c.table_copy(m.d_actNoticeUI.g_self);m.d_actNoticeUI.g_self.data=nil
 m.d_u.g_is_waiting_1106=false
 m.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
 local nativeFirst=r.pressFirstCharge
 local nativeMonthShow=m.d_monthCardUI.show
 local nativeMonthClaim=m.d_monthCardUI.pressGetGold
 local springUpdates=0
 m.d_chargePresentUI.updateActivityStatus=function(data) assert(data.spring_info);springUpdates=springUpdates+1 end
 -- INSTALL_PATCH
 if RECHARGE_PREVIEW then
  CCDirector:sharedDirector():getRunningScene():addChild(layer,9999)
  r.show(layer);r.pressPurchase(r.g_self.button_tag+3)
  r._localCardChange('large_count',-1);r._localCardChange('small_count',10)
  return
 end
 check('card_description_runtime_override',function()
  assert(m.d_packageUI.g_itemAttrTable[1156].introduction=='等同于充值5元')
  assert(m.d_packageUI.g_itemAttrTable[1152].introduction=='等同于充值50元')
 end)
 check('original_layout_and_all_six_buttons',function()
  r.show(layer);assert(r.g_self.main_layer and r.g_self.menu)
  for i=1,6 do
   local b=tolua.cast(r.g_self.menu:getChildByTag(r.g_self.button_tag+i),'CCMenuItem')
   assert(b);b:activate()
   local s=assert(r._localCardSelection)
   assert(s.product.id==100+i and s.large_count*50+s.small_count*5==s.product.rmb)
   r._localCardCancel()
  end
 end)
 check('choose_small_cards_and_idempotent_retry',function()
  r.pressPurchase(r.g_self.button_tag+2)
  r._localCardChange('large_count',-1);r._localCardChange('small_count',10)
  r._localCardConfirm()
  local req=sent[#sent];assert(req.mid==1111 and req.data.event_id==251)
  local data=assert(loadstring('return '..req.data.data))()
  assert(data.item_id==102 and data.large_count==0 and data.small_count==10)
  r._localCardConfirm()
  assert(sent[#sent].data.data==req.data.data)
  r._localCardCancel();assert(r._localCardSelection==nil)
  r.pressPurchase(r.g_self.button_tag+3)
  assert(r._localCardSelection.product.id==102 and r._localCardSelection.order_id==data.order_id)
  r._localCardConfirm();assert(sent[#sent].data.data==req.data.data)
  local s=m.d_c.table_copy(FIXTURE);s.last_order_id=data.order_id;s.small_count=s.small_count-10
  m.d_data.callback_update_config({local_recharge=s})
  assert(r._localCardSelection==nil)
 end)
 check('failed_order_receipt_unlocks_selection',function()
  r.pressPurchase(r.g_self.button_tag+2);r._localCardConfirm()
  local id=r._localCardSelection.order_id
  local failed=m.d_c.table_copy(FIXTURE);failed.failed_order_id=id
  m.d_data.callback_update_config({local_recharge=failed})
  assert(r._localCardSelection and r._localCardSelection.order_id==nil)
  r._localCardChange('large_count',-1);assert(r._localCardSelection.large_count==0)
  r._localCardCancel()
 end)
 check('styled_buttons_mixed_payment_and_pending_lock',function()
  m.d_data.g_new_config.local_recharge=m.d_c.table_copy(FIXTURE)
  r.pressPurchase(r.g_self.button_tag+3)
  cardButton(19872):activate();assert(not cardButton(19863):isEnabled())
  cardButton(19884):activate();assert(cardButton(19863):isEnabled())
  cardButton(19863):activate()
  local req=sent[#sent];local data=assert(loadstring('return '..req.data.data))()
  assert(data.item_id==103 and data.large_count==1 and data.small_count==10)
  for _,tag in ipairs({19871,19872,19873,19874,19881,19882,19883,19884,19862}) do
   assert(not cardButton(tag):isEnabled())
  end
  cardButton(19863):activate();assert(sent[#sent].data.data==req.data.data)
  local done=m.d_c.table_copy(FIXTURE);done.last_order_id=data.order_id
  m.d_data.callback_update_config({local_recharge=done});assert(r._localCardSelection==nil)
 end)
 check('styled_buttons_clamp_inventory_auto_close_and_refresh',function()
  local state=m.d_data.g_new_config.local_recharge
  state.large_count=2;state.small_count=3
  r.pressPurchase(r.g_self.button_tag+3)
  cardButton(19884):activate();assert(r._localCardSelection.small_count==3)
  assert(not cardButton(19884):isEnabled() and cardButton(19863):isEnabled())
  cardButton(19881):activate();assert(r._localCardSelection.small_count==0)
  assert(not cardButton(19882):isEnabled() and cardButton(19863):isEnabled())
  cardButton(19871):activate();assert(r._localCardSelection.large_count==0)
  cardButton(19873):activate();cardButton(19874):activate();assert(r._localCardSelection.large_count==2)
  cardButton(19872):activate();cardButton(19862):activate();assert(r._localCardSelection.large_count==2)
  local empty=m.d_c.table_copy(FIXTURE);empty.large_count=0;empty.small_count=1
  m.d_data.callback_update_config({local_recharge=empty})
  assert(not cardButton(19863):isEnabled());local n=#sent
  cardButton(19860):activate();assert(r._localCardSelection==nil and #sent==n)
  m.d_data.g_new_config.local_recharge=m.d_c.table_copy(FIXTURE)
 end)
 check('overpayment_requires_confirmation_cancel_and_retry',function()
  local state=m.d_c.table_copy(FIXTURE);state.large_count=1;state.small_count=0
  m.d_data.g_new_config.local_recharge=state
  m.d_monthCardUI.canBuyFund()
  local s=assert(r._localCardSelection)
  assert(s.product.id==202 and s.large_count==1 and s.small_count==0)
  local n=#sent
  cardButton(19863):activate()
  assert(s.overpay_confirm and not s.order_id and #sent==n)
  cardButton(19864):activate()
  assert(not s.overpay_confirm and not s.order_id and #sent==n)
  cardButton(19863):activate();cardButton(19860):activate()
  assert(r._localCardSelection==nil and #sent==n)
  m.d_monthCardUI.canBuyFund();cardButton(19863):activate();cardButton(19865):activate()
  assert(#sent==n+1)
  local req=sent[#sent];local data=assert(loadstring('return '..req.data.data))()
  assert(data.item_id==202 and data.large_count==1 and data.small_count==0)
  cardButton(19863):activate();assert(sent[#sent].data.data==req.data.data)
  local done=m.d_c.table_copy(FIXTURE);done.last_order_id=data.order_id
  m.d_data.callback_update_config({local_recharge=done});assert(r._localCardSelection==nil)
 end)
 check('overpayment_confirmation_inventory_refresh_and_selection_change',function()
  m.d_data.g_new_config.local_recharge=m.d_c.table_copy(FIXTURE)
  r.pressPurchase(r.g_self.button_tag+2);cardButton(19883):activate()
  local n=#sent;cardButton(19863):activate();assert(#sent==n)
  local empty=m.d_c.table_copy(FIXTURE);empty.large_count=0
  m.d_data.callback_update_config({local_recharge=empty})
  assert(not cardButton(19865):isEnabled() and #sent==n)
  cardButton(19864):activate();assert(not cardButton(19863):isEnabled())
  m.d_data.callback_update_config({local_recharge=m.d_c.table_copy(FIXTURE)})
  cardButton(19863):activate();cardButton(19864):activate()
  cardButton(19882):activate();assert(not r._localCardSelection.overpay_confirm)
  cardButton(19883):activate();cardButton(19863):activate()
  assert(r._localCardSelection.overpay_confirm and #sent==n)
  cardButton(19865):activate();assert(#sent==n+1)
  local data=assert(loadstring('return '..sent[#sent].data.data))()
  assert(data.item_id==102 and data.large_count==1 and data.small_count==1)
  local done=m.d_c.table_copy(FIXTURE);done.last_order_id=data.order_id
  m.d_data.callback_update_config({local_recharge=done})
 end)
 check('insufficient_cards_and_cancel_do_not_send',function()
  m.d_data.g_new_config.local_recharge.large_count=0
  m.d_data.g_new_config.local_recharge.small_count=1
  r.pressPurchase(r.g_self.button_tag+1)
  local n=#sent;r._localCardConfirm();assert(#sent==n)
  r._localCardCancel();assert(r._localCardSelection==nil)
  m.d_data.g_new_config.local_recharge=m.d_c.table_copy(FIXTURE)
 end)
 check('month_fund_and_every_channel_entrance',function()
  r.pressMonthCard();assert(r._localCardSelection.product.id==201);r._localCardCancel()
  for _,key in ipairs({'recharge_order_request','recharge_For_IOS','pressBuyYYB','buy_item_yyb'}) do
   m.d_recharge[key](7);assert(r._localCardSelection.product.id==201);r._localCardCancel()
  end
  m.d_monthCardUI.pressBuyMcard();assert(r._localCardSelection.product.id==201);r._localCardCancel()
  m.d_monthCardUI.canBuyFund();assert(r._localCardSelection.product.id==202);r._localCardCancel()
  local n=#sent;m.d_u.main_server_send_msg(1112,{event_id=3,data='{item_id=8}'})
  assert(#sent==n and r._localCardSelection.product.id==202);r._localCardCancel()
  assert(r.pressFirstCharge==nativeFirst)
 end)
 check('month_footer_and_extra_quota_handlers_removed',function()
  assert(m.d_monthCardUI.show==nativeMonthShow)
  assert(m.d_monthCardUI.pressGetGold==nativeMonthClaim)
  assert(FIXTURE.month.rewards_remaining==nil)
 end)
 check('bag_card_uses_unique_persistent_order',function()
  local request={item_id=12345,item_type=1156,item_count=2,des_type=1,des_id=0}
  m.d_u.main_server_send_msg(1051,request)
  local first=sent[#sent];assert(first.mid==1111 and first.data.event_id==253)
  local data=assert(loadstring('return '..first.data.data))();assert(data.item_id==12345 and data.item_count==2)
  m.d_u.main_server_send_msg(1051,request);assert(sent[#sent].data.data==first.data.data)
  local updated=m.d_c.table_copy(FIXTURE);updated.last_order_id=data.order_id
  m.d_data.callback_update_config({local_recharge=updated})
  m.d_u.main_server_send_msg(1051,request);assert(sent[#sent].data.data~=first.data.data)
 end)
 check('single_charge_panel_refresh_has_one_layer',function()
  r._localSingleOpen(1)
  local scene=CCDirector:sharedDirector():getRunningScene()
  local old=scene:getChildByTag(19851);assert(old)
  local function find(node,tag)
   if node:getTag()==tag then return node end
   local children=node:getChildren()
   if children then for i=0,children:count()-1 do
    local hit=find(tolua.cast(children:objectAtIndex(i),'CCNode'),tag)
    if hit then return hit end
   end end
  end
  local claim=assert(find(old,19901));tolua.cast(claim,'CCMenuItem'):activate()
  local request=sent[#sent];assert(request.mid==1111 and request.data.event_id==252)
  assert(assert(loadstring('return '..request.data.data))().index==1)
  m.d_data.callback_update_config({local_recharge=m.d_c.table_copy(FIXTURE)})
  local current=scene:getChildByTag(19851);assert(current and current~=old)
  assert(r.g_self.main_layer and r._localCardSelection==nil)
  r._localCardCancel();assert(scene:getChildByTag(19851)==nil)
 end)
 check('passive_sync_does_not_open_closed_welfare_or_send_queries',function()
  local notice=m.d_actNoticeUI
  notice.g_self.data=m.d_c.table_copy(FUND_FLOW.initial);notice.g_self.main_layer=nil
  local show=notice.show;notice.show=function() error('passive sync opened welfare') end
  local n=#sent
  local state={all_activity=m.d_c.table_copy(FUND_FLOW.initial.all_activity),spring_info={start_time=0,end_time=0}}
  local receipt=m.d_c.table_copy(FIXTURE);receipt.last_order_id='passive-checkout'
  m.d_data.callback_update_config({local_recharge=receipt,local_welfare=state})
  assert(#sent==n and notice.g_self.main_layer==nil and springUpdates>0)
  assert(r.g_self.main_layer and r.g_self.main_layer:getParent())
  notice.show=show
 end)
 check('native_fund_button_selects_cards_with_channel_disabled_and_refreshes_claim',function()
  r.pressClose()
  local notice=m.d_actNoticeUI
  m.d_c.g_can_recharge=false
  m.d_mainUI.g_playerInfo.buy_growup=0;m.d_mainUI.g_playerInfo.level=60
  notice.g_self.data=m.d_c.table_copy(FUND_FLOW.initial)
  notice.g_self.config={had_prize_flag={}}
  notice.g_self.meiri=notice.g_self.data.all_activity[74]
  notice.show(layer);notice.g_self.last_press_btn_tag=2;notice.showContent(notice.g_self.main_layer,2)
  local originalLayer=notice.g_self.main_layer
  assert(notice.g_get_fund_btn);notice.g_get_fund_btn:activate()
  local checkout=assert(r._localCardSelection)
  assert(checkout.product.id==202 and checkout.large_count==0 and checkout.small_count==9)
  assert(notice.g_self.main_layer==originalLayer)
  r._localCardConfirm();local order=checkout.order_id
  for _,packet in ipairs(FUND_FLOW.purchase) do
   local data=assert(loadstring('return '..packet.data))()
   if data.local_recharge then data.local_recharge.last_order_id=order end
   m.d_data.callback_update_config(data)
  end
  assert(r._localCardSelection==nil and m.d_mainUI.g_playerInfo.buy_growup==1)
  assert(notice.g_self.main_layer==originalLayer)
  assert(notice.g_self.data.all_activity[22].role_info[10].can_take)
  notice.g_get_fund_btn:activate()
  local req=sent[#sent];assert(req.mid==1127 and req.data.act_type==22 and req.data.flag==2)
  local prize=m.d_commonLayerUI.showPrizeResLayer
  m.d_commonLayerUI.showPrizeResLayer=function() end
  for _,packet in ipairs(FUND_FLOW.claimed) do m.d_event_mgr.msg_common_event_2998(nil,packet,nil) end
  m.d_commonLayerUI.showPrizeResLayer=prize
  assert(notice.g_self.data.all_activity[22].role_info[10].take_prize)
  local n=#sent;notice.pressBuyFund();assert(#sent==n and r._localCardSelection==nil)
  notice.closeNoticeUI()
 end)
 check('activity_entrances_repeat_with_disabled_channel_and_keep_source',function()
  local scene=CCDirector:sharedDirector():getRunningScene()
  local source=CCLayer:create();scene:addChild(source,100)
  local notice=m.d_actNoticeUI
  local prior,refresh=notice.g_self.main_layer,notice._localRefreshContent
  notice.g_self.main_layer=source;notice._localRefreshContent=function() end
  m.d_c.g_can_recharge=false
  local entries={notice.gotoCharge,notice.pressRecharge,m.d_xianlingShopUI.recharge,
                 m.d_shopUI.recharge,m.d_twoYearsCelebrateUI.recharge,v.pressRecharge,m.d_firstChargeUI.pressRecharge}
  for _,entry in ipairs(entries) do
   for i=1,3 do
    entry();local current=assert(r.g_self.main_layer)
    assert(current:getParent()==scene and source:getParent()==scene)
    entry();assert(r.g_self.main_layer==current)
    r.pressClose();assert(r.g_self.main_layer==nil and source:getParent()==scene)
   end
  end
  assert(m.d_c.g_can_recharge==false)
  notice.g_self.main_layer=prior;notice._localRefreshContent=refresh
  source:removeFromParentAndCleanup(true)
 end)
 check('payment_receipt_and_legacy_callback_keep_recharge_window',function()
  m.d_data.g_new_config.local_recharge=m.d_c.table_copy(FIXTURE)
  local notice=m.d_actNoticeUI
  notice.g_self.data=m.d_c.table_copy(FUND_FLOW.initial);notice.g_self.config={had_prize_flag={}}
  notice.show(layer);local source=notice.g_self.main_layer
  local tab=notice.g_self.last_press_btn_tag
  notice.gotoCharge();local current=assert(r.g_self.main_layer)
  for i=1,2 do
   r.pressPurchase(r.g_self.button_tag+2);cardButton(19863):activate()
   local order=r._localCardSelection.order_id
   for _,packet in ipairs(FUND_FLOW.ordinary[i]) do
    local data=assert(loadstring('return '..packet.data))()
    if data.local_recharge then
     data.local_recharge.last_order_id=order
    end
    m.d_data.callback_update_config(data)
   end
   assert(r._localCardSelection==nil and r.g_self.main_layer==current and r._localIsOpen())
   assert(m.d_data.g_new_config.local_recharge.large_count==2-i)
   assert(notice.g_self.main_layer==source and source:getParent() and notice.g_self.last_press_btn_tag==tab)
   r.onReceiveRechargeResult();assert(r.g_self.main_layer==current and r._localIsOpen())
  end
  r.pressClose();r.onReceiveRechargeResult();assert(r.g_self.main_layer==nil)
  assert(notice.g_self.main_layer==source and source:getParent())
  notice.closeNoticeUI()
 end)
 check('stale_parent_cleanup_does_not_destroy_or_block_recharge',function()
  local scene=CCDirector:sharedDirector():getRunningScene()
  local source=CCLayer:create();source:retain();scene:addChild(source,100)
  r.show(source);local current=assert(r.g_self.main_layer)
  source:removeAllChildrenWithCleanup(true);source:removeFromParentAndCleanup(true)
  assert(r.g_self.main_layer==current and r._localIsOpen())
  r.pressClose();r.show(source);assert(r._localIsOpen())
  -- Emulate a parent-driven cleanup that leaves the old Lua handle behind.
  current=r.g_self.main_layer;current:retain();current:removeFromParentAndCleanup(true)
  r.show(source);assert(r.g_self.main_layer~=current and r._localIsOpen())
  current:release();r.pressClose();source:release()
 end)
 check('anniversary_native_recharge_button_preserves_activity',function()
  local notice=m.d_actNoticeUI
  notice.g_self.data=m.d_c.table_copy(FUND_FLOW.initial)
  notice.g_self.config={had_prize_flag={}}
  notice.show(layer)
  local source=notice.g_self.main_layer
  local content=CCLayer:create();source:addChild(content)
  -- Legacy week_year_charge (34) is hidden in the shipping catalog. Keep its
  -- anonymous native button compatible without re-enabling the activity.
  local info={end_time=m.d_time.getTime()+86400,max_gold_count=500,min_money=6,max_order=1,
              had_took30=false,role_charge={charge_gold=0,order=0,had_took=false},prize_list={{},{}}}
  notice.createAnniversaryRecharge(info,content)
  local function find(node)
   if node:getTag()==19890 then return tolua.cast(node,'CCMenuItem') end
   local children=node:getChildren()
   if children then for i=0,children:count()-1 do
    local hit=find(tolua.cast(children:objectAtIndex(i),'CCNode'));if hit then return hit end
   end end
  end
  local btn=assert(find(content))
  for i=1,3 do
   btn:activate();assert(r._localIsOpen() and notice.g_self.main_layer==source and source:getParent())
   r.pressClose();assert(source:getParent())
  end
  notice.closeNoticeUI()
 end)
 check('rendered_welfare_recharge_buttons_repeat_on_original_tabs',function()
  local notice=m.d_actNoticeUI
  m.d_data.g_new_config.local_vip=nil
  m.d_mainUI.g_playerInfo.first_charge=0;m.d_mainUI.g_playerInfo.first_charge_gift=0
  m.d_mainUI.g_playerInfo.take_charge_gift_time=0
  notice.g_self.data=m.d_c.table_copy(FUND_FLOW.initial);notice.g_self.config={had_prize_flag={}}
  notice.show(layer)
  local source=notice.g_self.main_layer
  local createMenu=m.d_u.createMenu
  m.d_u.createMenu=function(styles,...)
   for _,style in ipairs(styles) do
    if style.call_back==notice.gotoCharge or style.call_back==notice.pressRecharge then style.tag=19891 end
   end
   return createMenu(styles,...)
  end
  local function find(node)
   if node:getTag()==19891 then return tolua.cast(node,'CCMenuItem') end
   local children=node:getChildren()
   if children then for i=0,children:count()-1 do
    local hit=find(tolua.cast(children:objectAtIndex(i),'CCNode'));if hit then return hit end
   end end
  end
  local tested={}
  for index,kind in ipairs(notice.g_self.data.order_list) do
   notice.g_self.last_press_btn_tag=index;notice.showContent(source,index)
   if find(source) then
    for i=1,3 do
     assert(find(source)):activate()
     assert(r._localIsOpen() and notice.g_self.main_layer==source and source:getParent())
     r.pressClose()
     assert(notice.g_self.main_layer==source and notice.g_self.last_press_btn_tag==index)
    end
    tested[kind]=true
   end
  end
  m.d_u.createMenu=createMenu
  assert(tested[20] and tested[60],'first-charge and anniversary-gift buttons must be exercised: '..table.tostring(tested))
  notice.closeNoticeUI()
 end)
 check('native_month_dialog_stacking_and_receipt_focus',function()
  local month=m.d_monthCardUI
  r.show();local recharge=r.g_self.main_layer
  month.show();local current=month.g_monthCardUI.main_layer
  assert(current:getParent()==recharge:getParent() and current:getZOrder()>=recharge:getZOrder())
  -- Re-enter recharge over an existing month dialog. A receipt must not
  -- rebuild that background dialog on top of the current recharge page.
  r.show()
  for _,packet in ipairs(FUND_FLOW.ordinary[1]) do
   m.d_data.callback_update_config(assert(loadstring('return '..packet.data))())
  end
  assert(r.g_self.main_layer==recharge and month.g_monthCardUI.main_layer==current)
  r.pressClose();assert(month.g_monthCardUI.main_layer:getParent())
  month.g_monthCardUI.main_layer:removeFromParentAndCleanup(true);month.g_monthCardUI.main_layer=nil
 end)
 check('restore_callbacks_and_original_item_text',function()
  if r.g_self.main_layer then r.pressClose() end
  m.d_actNoticeUI._localWelfareRestore();v._localVipRestore()
  assert(r._localCardOpen==nil and r._localSingleOpen==nil)
  assert(m.d_packageUI.g_itemAttrTable[1156].introduction~='等同于充值5元')
 end)
end,debug.traceback)
local function restore()
if r._localCardCancel then pcall(r._localCardCancel) end
if r.g_self and r.g_self.main_layer then pcall(r.pressClose) end
if m.d_actNoticeUI.g_self.main_layer then pcall(m.d_actNoticeUI.closeNoticeUI) end
if m.d_actNoticeUI._localWelfareRestore then pcall(m.d_actNoticeUI._localWelfareRestore) end
if v._localVipRestore then pcall(v._localVipRestore) end
for i=#saved,1,-1 do
 local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end
 for k,val in pairs(row.old) do row.t[k]=val end
end
m.MS_report_error=report
layer:removeFromParentAndCleanup(true);layer:removeAllChildrenWithCleanup(true);layer:release()
end
if RECHARGE_PREVIEW and ok then
 _G.rechargeStylePreview={restore=restore,button=cardButton}
 return 'preview ready'
end
restore()
if not ok then return 'fixture:false:'..tostring(err) end
return table.concat(checks,'\n')
