local FIXTURE={["products"]={{["id"]=101,["native_id"]=1,["ui_index"]=1,["kind"]="gold",["name"]="100元宝",["rmb"]=10,["gold"]=100,["bonus"]=0},{["id"]=102,["native_id"]=2,["ui_index"]=2,["kind"]="gold",["name"]="500元宝",["rmb"]=50,["gold"]=500,["bonus"]=50},{["id"]=103,["native_id"]=3,["ui_index"]=3,["kind"]="gold",["name"]="1000元宝",["rmb"]=100,["gold"]=1000,["bonus"]=110},{["id"]=104,["native_id"]=4,["ui_index"]=4,["kind"]="gold",["name"]="2000元宝",["rmb"]=200,["gold"]=2000,["bonus"]=240},{["id"]=105,["native_id"]=5,["ui_index"]=5,["kind"]="gold",["name"]="5000元宝",["rmb"]=500,["gold"]=5000,["bonus"]=650},{["id"]=106,["native_id"]=6,["ui_index"]=6,["kind"]="gold",["name"]="10000元宝",["rmb"]=1000,["gold"]=10000,["bonus"]=1500},{["id"]=201,["native_id"]=7,["kind"]="month",["name"]="30天月卡",["rmb"]=50,["gold"]=500,["bonus"]=0},{["id"]=202,["native_id"]=8,["kind"]="fund",["name"]="成长基金",["rmb"]=45,["gold"]=0,["bonus"]=0}},["large_count"]=100,["small_count"]=100,["large_rmb"]=50,["small_rmb"]=5,["last_order_id"]="",["month"]={["rmb"]=50,["daily_gold"]=100,["expires_at"]=0,["last_claim_at"]=0,["rewards_remaining"]=30},["single"]={["start_time"]=0,["end_time"]=2140000000,["max_rmb"]=50,["rows"]={{["index"]=1,["rmb"]=50,["status"]=2,["prize_list"]={{["object_type"]=11,["attach_type"]=0,["attach_count"]=50,["attach_level"]=1}}}}}}
-- Execute against the original Cocos client with all sends captured and state restored.
local m=assert(package.loaded.ms)
local r,v=m.d_rechargeUI,m.d_vipUI
local saved,checks,sent,errors={},{},{},{}
local function preserve(t)
 if not t then return end
 local old={};for k,val in pairs(t) do old[k]=val end;saved[#saved+1]={t=t,old=old}
end
for _,t in ipairs({r,v,m.d_mainUI,m.d_data,m.d_u,m.d_recharge,m.d_monthCardUI,m.d_packageUI,m.d_actNoticeUI}) do preserve(t) end
local report=m.MS_report_error
m.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
local layer=CCLayer:create();layer:retain()
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]=name..':'..tostring(ok and #errors==0)..':'..(err or '')..table.concat(errors,' ')
end
local ok,err=xpcall(function()
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
 -- Native recharge entrances and VIP layouts, settled with inventory gold cards.
do
    local ms = package.loaded['ms']
    local v = package.loaded['ui.vipUI']
    if not ms or not v or not ms.d_rechargeUI or not ms.d_data or not ms.d_data.callback_update_config then return 'pending' end
    if not v._localVipRestore then
        local r, pay, month = ms.d_rechargeUI, ms.d_recharge, ms.d_monthCardUI
        local originalRecharge, originalFrame = v.pressRecharge, v.createMainFrame
        local originalConfig = ms.d_data.callback_update_config
        local originalShow, originalPurchase, originalRFrame = r.show, r.pressPurchase, r.createMainFrame
        local originalMonth, originalFirst, originalClose = r.pressMonthCard, r.pressFirstCharge, r.pressClose
        local originalSend = ms.d_u.main_server_send_msg
        local originalCheckVIP = ms.d_mainUI.checkVIPAnim
        local paymentCallbacks, monthCallbacks, cardDescriptions = {}, {}, {}
        local orderSequence, panel, selection, singlePage = 0, nil, nil, nil
        local displayedLevel, displayedTab
        local PANEL_TAG = 19851
        local pendingCardUse, pendingCheckout
        local lastRefreshOrder
        local function state() return (ms.d_data.g_new_config or {}).local_recharge or {} end
        local function products() return state().products or {} end
        local function productById(id)
            for _,p in ipairs(products()) do if p.id == id then return p end end
        end
        local function nativeProduct(id)
            if id==nil then return end
            local numeric = tonumber(id)
            for _,p in ipairs(products()) do
                if numeric and (p.native_id == numeric or p.ui_index == numeric) then return p end
            end
            -- iOS uses the original string product identifier instead of its index.
            for index,row in pairs(ms.d_data.g_rechargeItemsPriceTable or {}) do
                if row.product_id == id then return nativeProduct(tonumber(index)) end
            end
        end
        local function refreshHeader()
            local main, player = ms.d_mainUI.g_mainUI, ms.d_mainUI.g_playerInfo
            if main and player and main.playerInfoTab and main.player_layer and main.player_layer:getParent()
                and (displayedLevel ~= player.vip_level or displayedTab ~= main.playerInfoTab) then
                main.playerInfoTab = ms.d_playerInfoUI.reloadPlayerInfo(main.player_layer)
                displayedLevel, displayedTab = player.vip_level, main.playerInfoTab
            end
        end
        ms.d_mainUI.checkVIPAnim = function(...)
            originalCheckVIP(...)
            refreshHeader()
        end
        local function cardText()
            local items=ms.d_packageUI and ms.d_packageUI.g_itemAttrTable
            if not items then return end
            for tid,rmb in pairs({[1152]=50,[1156]=5}) do
                local row=items[tid]
                if row then
                    if not cardDescriptions[tid] then
                        cardDescriptions[tid]={row=row,name=row.name,description=row.description,introduction=row.introduction}
                    end
                    row.name=tid==1152 and '大传世金卡' or '小传世金卡'
                    row.description='面值'..rmb..'元，可在充值界面抵扣或在背包使用，计入VIP及充值活动。'
                    row.introduction='等同于充值'..rmb..'元'
                end
            end
        end
        local function sync()
            cardText()
            local info = (ms.d_data.g_new_config or {}).local_vip
            local player = ms.d_mainUI and ms.d_mainUI.g_playerInfo
            if info and player then for k,value in pairs(info) do player[k] = value end end
        end
        local function closePanel()
            if panel and panel:getParent() then panel:removeFromParentAndCleanup(true) end
            panel, selection, singlePage = nil, nil, nil
            r._localCardSelection = nil
        end
        local function inventory()
            return tonumber(state().large_count) or 0, tonumber(state().small_count) or 0
        end
        local function text(parent,value,x,y,size,color)
            local label = CCLabelTTF:create(value,'Arial',size or 22)
            label:setColor(color or ccc3(245,226,185))
            label:setPosition(ccp(x,y));parent:addChild(label,5)
            return label
        end
        local function button(parent,title,x,y,fn,enabled,width)
            local w,h = width or 140,44
            local function face(pressed)
                local edge = CCLayerColor:create(enabled and ccc4(190,146,74,255) or ccc4(94,89,81,255),w,h)
                local fill = CCLayerColor:create(pressed and ccc4(107,65,29,255) or ccc4(58,39,27,255),w-4,h-4)
                fill:setPosition(ccp(2,2));edge:addChild(fill)
                text(edge,title,w/2,h/2,20,enabled and ccc3(255,230,171) or ccc3(135,130,120))
                return edge
            end
            local item = CCMenuItemSprite:create(face(false),face(true))
            item:setEnabled(enabled);item:registerScriptTapHandler(fn)
            local menu = CCMenu:createWithItem(item);menu:setPosition(ccp(x,y));parent:addChild(menu,10)
            return item
        end
        local renderPanel
        local function change(kind,amount)
            if not selection or selection.order_id then return end
            local large,small = inventory()
            local limit = kind == 'large_count' and large or small
            selection[kind] = math.max(0,math.min(limit,selection[kind]+amount))
            renderPanel()
        end
        local function autoSelect()
            if not selection or selection.order_id then return end
            local large,small = inventory()
            local due = selection.product.rmb
            local n = math.min(large,math.floor(due/50))
            selection.large_count,selection.small_count = n,math.min(small,(due-50*n)/5)
            renderPanel()
        end
        local function confirm()
            if not selection then return end
            local s = selection
            if not s.order_id then
                local large,small = inventory()
                if 50*s.large_count+5*s.small_count ~= s.product.rmb then ms.d_info.show('所选金卡总额须等于本次充值金额');return end
                if s.large_count>large or s.small_count>small then ms.d_info.show('可用金卡不足，请调整数量');return end
                orderSequence = orderSequence+1
                s.order_id = tostring(os.time())..'-'..tostring(math.random(100000,999999))..'-'..tostring(orderSequence)
                pendingCheckout=s
            end
            -- Retain both the order and counts after a timeout: retrying is idempotent.
            originalSend(ms.d_msg_def.gscl_msg_id.msg_order_request,
                {event_id=251,data=table.tostring({item_id=s.product.id,order_id=s.order_id,
                    large_count=s.large_count,small_count=s.small_count})})
            if selection then renderPanel() end
        end
        renderPanel = function()
            if not panel or not selection then return end
            panel:removeAllChildrenWithCleanup(true)
            ms.d_u.createSwallowTouchLayer(panel)
            local size = CCDirector:sharedDirector():getVisibleSize()
            panel:addChild(CCLayerColor:create(ccc4(0,0,0,185),size.width,size.height))
            local scale = math.min(size.width/960,size.height/640)
            local box = CCLayerColor:create(ccc4(40,28,21,255),740,480)
            box:setScale(scale);box:setPosition(ccp((size.width-740*scale)/2,(size.height-480*scale)/2));panel:addChild(box,2)
            local s = selection
            local large,small = inventory()
            local paid = s.large_count*50+s.small_count*5
            local ready = paid == s.product.rmb and s.large_count<=large and s.small_count<=small
            text(box,'传世金卡充值',370,447,28,ccc3(255,218,128))
            text(box,(s.product.name or '充值')..'  ·  '..s.product.rmb..'元',370,408,23)
            text(box,'大卡 50元/张 · 小卡 5元/张 · 仅扣除所选道具',370,374,19)
            local rows={{key='large_count',name='大传世金卡',owned=large,y=314},{key='small_count',name='小传世金卡',owned=small,y=244}}
            for _,row in ipairs(rows) do
                local key = row.key
                text(box,row.name..'  可用 '..row.owned,164,row.y,20)
                button(box,'−10',318,row.y,function() change(key,-10) end,not s.order_id and s[key]>0,58)
                button(box,'−',387,row.y,function() change(key,-1) end,not s.order_id and s[key]>0,52)
                text(box,tostring(s[key])..'张',468,row.y,24)
                button(box,'+',548,row.y,function() change(key,1) end,not s.order_id and s[key]<row.owned,52)
                button(box,'+10',617,row.y,function() change(key,10) end,not s.order_id and s[key]<row.owned,58)
            end
            text(box,'已选 '..paid..'元 / 需 '..s.product.rmb..'元',370,188,24,ready and ccc3(158,224,147) or ccc3(255,164,125))
            text(box,s.order_id and '订单已提交；关闭面板不会撤回，可重新打开重试'  or '本次抵扣金额计入VIP、单充、累充及充值活动',370,149,18)
            button(box,s.order_id and '关闭面板' or '取消',154,85,closePanel,true,130)
            button(box,'自动搭配',370,85,autoSelect,not s.order_id,156)
            button(box,s.order_id and '重试同一订单' or '确认扣卡',586,85,confirm,s.order_id~=nil or ready,180)
        end
        local function openPanel(product)
            sync()
            if not product and not pendingCheckout then ms.d_info.show('充值商品尚未同步，请重新登录后重试');return end
            closePanel()
            local scene = CCDirector:sharedDirector():getRunningScene()
            scene:removeChildByTag(PANEL_TAG,true)
            panel = CCLayer:create();scene:addChild(panel,10000,PANEL_TAG)
            selection = pendingCheckout or {product=product,large_count=0,small_count=0}
            r._localCardSelection=selection
            if pendingCheckout then renderPanel() else autoSelect() end
        end
        local showSingle
        showSingle = function(page)
            if selection and selection.order_id then ms.d_info.show('请先确认当前充值订单');return end
            closePanel()
            local scene = CCDirector:sharedDirector():getRunningScene()
            panel = CCLayer:create();scene:addChild(panel,10000,PANEL_TAG)
            ms.d_u.createSwallowTouchLayer(panel)
            local size=CCDirector:sharedDirector():getVisibleSize()
            panel:addChild(CCLayerColor:create(ccc4(0,0,0,185),size.width,size.height))
            local scale=math.min(size.width/960,size.height/640)
            local box=CCLayerColor:create(ccc4(40,28,21,255),740,480)
            box:setScale(scale);box:setPosition(ccp((size.width-740*scale)/2,(size.height-480*scale)/2));panel:addChild(box,2)
            local single=state().single or {}
            local rows=single.rows or {}
            local pages=math.max(1,math.ceil(#rows/4))
            singlePage=math.max(1,math.min(page or 1,pages))
            text(box,'单笔充值奖励',370,446,28,ccc3(255,218,128))
            text(box,'本期最高单笔 '..tostring(single.max_rmb or 0)..'元 · 多笔充值不合并',370,404,21)
            for offset=1,4 do
                local row=rows[(singlePage-1)*4+offset]
                if row then
                    local y=354-(offset-1)*62
                    text(box,'单笔达到 '..row.rmb..'元',175,y,22)
                    local rewardText={}
                    for _,prize in ipairs(row.prize_list or {}) do
                        local typ=prize.object_type
                        local name=typ==11 and '元宝' or typ==12 and '银币' or (ms.d_data.getItemName and ms.d_data.getItemName(prize.attach_type)) or '道具'
                        rewardText[#rewardText+1]=name..'×'..tostring(prize.attach_count or 0)
                    end
                    text(box,table.concat(rewardText,' '),382,y,16)
                    local index=row.index or ((singlePage-1)*4+offset)
                    button(box,row.status==3 and '已领取' or row.status==2 and '领取' or '未达成',616,y,function()
                        originalSend(ms.d_msg_def.gscl_msg_id.msg_order_request,{event_id=252,data=table.tostring({index=index})})
                    end,row.status==2,128):setTag(19900+index)
                end
            end
            text(box,'单笔达标后各档可领一次；赠送元宝不计充值额度',370,103,18)
            button(box,'关闭',160,48,closePanel,true,120)
            button(box,'上一页',340,48,function() showSingle(singlePage-1) end,singlePage>1,120)
            text(box,tostring(singlePage)..' / '..pages,452,48,18)
            button(box,'下一页',575,48,function() showSingle(singlePage+1) end,singlePage<pages,120)
        end
        r._localSingleOpen=showSingle
        -- Exposed operations also let the native-client regression exercise taps.
        r._localCardOpen, r._localCardChange, r._localCardConfirm = openPanel, change, confirm
        r._localCardCancel, r._localCardAuto = closePanel, autoSelect
        v.createMainFrame = function(...) sync();return originalFrame(...) end
        r.createMainFrame = function(layer)
            r.g_self.hasCharged = (ms.d_mainUI.g_playerInfo.first_charge or 0) ~= 0
            local player = ms.d_mainUI.g_playerInfo
            local threshold = player.next_charge_gold
            player.next_charge_gold = math.max(0,(threshold or 0)-(player.charge_gold or 0))
            local ok,result = pcall(originalRFrame,layer)
            player.next_charge_gold = threshold
            if not ok then error(result) end
            local size = CCDirector:sharedDirector():getVisibleSize()
            text(layer,'传世金卡充值：大卡50元 · 小卡5元',size.width*0.5,size.height*0.965,16)
            if month and month.show then
                local item = CCMenuItemLabel:create(CCLabelTTF:create('月卡福利 / 续期','Arial',18))
                item:registerScriptTapHandler(function() month.show() end)
                local menu = CCMenu:createWithItem(item);menu:setPosition(ccp(size.width*0.38,size.height*0.055));layer:addChild(menu,35)
            end
            local singleItem=CCMenuItemLabel:create(CCLabelTTF:create('单笔充值奖励','Arial',18))
            singleItem:registerScriptTapHandler(function() showSingle(1) end)
            local singleMenu=CCMenu:createWithItem(singleItem);singleMenu:setPosition(ccp(size.width*0.66,size.height*0.055));layer:addChild(singleMenu,35)
        end
        r.show = function(parent)
            sync()
            if r.g_self.main_layer then r.pressClose() end
            return originalShow(parent)
        end
        r.pressClose = function(...) closePanel();return originalClose(...) end
        r.pressPurchase = function(tag)
            local index = tonumber(tag) and tonumber(tag)-r.g_self.button_tag
            local product
            for _,p in ipairs(products()) do if p.ui_index == index then product=p end end
            openPanel(product)
        end
        r.pressMonthCard = function() openPanel(productById(201)) end
        -- The native first-charge button opens its preview and claim UI.
        r.pressFirstCharge = originalFirst
        v.pressRecharge = function() v.pressClose();r.show() end
        if pay then
            for _,name in ipairs({'recharge_order_request','recharge_For_IOS','pressBuyYYB','buy_item_yyb'}) do
                paymentCallbacks[name]=pay[name]
                pay[name]=function(id) openPanel(nativeProduct(id)) end
            end
            paymentCallbacks.recharge_getBalance=pay.recharge_getBalance
            pay.recharge_getBalance=function() openPanel(nativeProduct(r.g_self.cur_purchase_tag)) end
        end
        if month then
            monthCallbacks.show,monthCallbacks.todayGoldHasTaken,monthCallbacks.pressGetGold=month.show,month.todayGoldHasTaken,month.pressGetGold
            month.todayGoldHasTaken=function()
                if (state().month or {}).rewards_remaining==0 then return true end
                return monthCallbacks.todayGoldHasTaken()
            end
            month.pressGetGold=function(...)
                if (state().month or {}).rewards_remaining==0 then
                    ms.d_info.show('本期月卡日奖已领完，可用金卡续期增加30份日奖');return
                end
                return monthCallbacks.pressGetGold(...)
            end
            month.show=function(...)
                sync()
                local result=monthCallbacks.show(...)
                local view=month.g_monthCardUI and month.g_monthCardUI.main_layer
                if view then
                    local size=CCDirector:sharedDirector():getVisibleSize()
                    local info=state().month or {}
                    local footer=CCLayerColor:create(ccc4(42,28,17,245),size.width*0.85,size.height*0.10)
                    footer:setPosition(ccp(size.width*0.075,size.height*0.065));view:addChild(footer,30)
                    text(footer,'剩余日奖 '..tostring(info.rewards_remaining or 0)..'份 · 每日'..tostring(info.daily_gold or 100)..'元宝',size.width*0.30,size.height*0.05,18)
                    button(footer,'金卡续期（50元 / 30天）',size.width*0.66,size.height*0.05,
                        function() openPanel(productById(201)) end,true,230)

                end
                return result
            end
            for name,id in pairs({pressBuyMcard=201,canBuyMcard=201,canBuyFund=202}) do
                monthCallbacks[name]=month[name]
                local productId=id
                month[name]=function() openPanel(productById(productId)) end
            end
        end
        -- Growth-fund UI emits prebuy directly, without passing common.recharge.
        ms.d_u.main_server_send_msg = function(mid,data,...)
            local ids=ms.d_msg_def.gscl_msg_id
            if mid==ids.msg_use_item and data and (data.item_type==1152 or data.item_type==1156) then
                local key=table.concat({data.item_id,data.item_type,data.item_count,data.des_type,data.des_id},':')
                if not pendingCardUse or pendingCardUse.key~=key then
                    orderSequence=orderSequence+1
                    pendingCardUse={key=key,order_id=tostring(os.time())..'-'..tostring(math.random(100000,999999))..'-'..tostring(orderSequence)}
                end
                return originalSend(ids.msg_order_request,{event_id=253,data=table.tostring({order_id=pendingCardUse.order_id,
                    item_id=data.item_id,item_type=data.item_type,item_count=data.item_count,des_type=data.des_type,des_id=data.des_id})})
            end
            if (mid==ids.msg_order_prebuy or mid==ids.msg_order_request) and data and data.event_id~=251 and data.event_id~=252 and data.event_id~=253 then
                local id=type(data.data)=='table' and data.data.item_id
                if type(data.data)=='string' then id=tonumber(string.match(data.data,'item_id%s*=%s*(%d+)')) end
                if id then openPanel(nativeProduct(id));return end
                -- Query/completion traffic from an old real-payment channel has no role in card settlement.
                return
            end
            return originalSend(mid,data,...)
        end
        ms.d_data.callback_update_config = function(data)
            originalConfig(data)
            sync()
            if data and data.local_single_charge_reward then
                ms.d_commonLayerUI.showPrizeResLayer(panel or r.g_self.main_layer or ms.d_mainUI.g_mainUI.main_layer,data.local_single_charge_reward)
            end
            if data and data.local_recharge then
                local order=data.local_recharge.last_order_id
                local failed=data.local_recharge.failed_order_id
                if pendingCardUse and (pendingCardUse.order_id==order or pendingCardUse.order_id==failed) then pendingCardUse=nil end
                if pendingCheckout and (pendingCheckout.order_id==order or pendingCheckout.order_id==failed) then
                    pendingCheckout=nil
                end
                if selection and selection.order_id==failed then selection.order_id=nil end
                if order and order~='' and order~=lastRefreshOrder then
                    lastRefreshOrder=order
                    local notice=ms.d_actNoticeUI
                    local view=notice and notice.g_self
                    if view and view.data then
                        if view.main_layer and view.main_layer:getParent() and view.last_press_btn_tag then
                            local activity=notice.getActInfo(view.last_press_btn_tag)
                            if activity and activity>0 then
                                originalSend(ms.d_msg_def.gscl_msg_id.msg_common_activity,{flag=1,act_type=activity,index=0})
                            end
                        else view.data=nil end
                    end
                end
                if selection and selection.order_id and data.local_recharge.last_order_id==selection.order_id then closePanel()
                elseif singlePage then showSingle(singlePage)
                elseif panel then renderPanel() end
            end
            if data and data.local_vip and not data.config_end then
                refreshHeader()
                if v.g_self and v.g_self.main_layer then
                    v.g_self.main_layer:removeAllChildrenWithCleanup(true)
                    v.createMainFrame(v.g_self.main_layer)
                end
                if r.g_self.main_layer then
                    r.g_self.main_layer:removeAllChildrenWithCleanup(true)
                    ms.d_u.createSwallowTouchLayer(r.g_self.main_layer)
                    r.createMainFrame(r.g_self.main_layer)
                end
                if month and month.g_monthCardUI and month.g_monthCardUI.main_layer and month.g_monthCardUI.main_layer:getParent() then month.show() end
            end
        end
        v._localVipRestore = function()
            closePanel()
            v.pressRecharge,v.createMainFrame = originalRecharge,originalFrame
            ms.d_data.callback_update_config = originalConfig
            ms.d_u.main_server_send_msg = originalSend
            ms.d_mainUI.checkVIPAnim = originalCheckVIP
            r.show,r.pressPurchase,r.createMainFrame = originalShow,originalPurchase,originalRFrame
            r.pressMonthCard,r.pressFirstCharge,r.pressClose = originalMonth,originalFirst,originalClose
            for name,fn in pairs(paymentCallbacks) do pay[name]=fn end
            for name,fn in pairs(monthCallbacks) do month[name]=fn end
            for _,saved in pairs(cardDescriptions) do
                saved.row.name,saved.row.description,saved.row.introduction=saved.name,saved.description,saved.introduction
            end
            r._localCardOpen,r._localCardChange,r._localCardConfirm,r._localCardCancel,r._localCardAuto,r._localSingleOpen=nil,nil,nil,nil,nil,nil
            v._localVipRestore=nil
        end
        cardText()
    end
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
 check('month_reward_quota_blocks_exhausted_claim',function()
  local info=m.d_data.g_new_config.local_recharge.month
  local remaining=info.rewards_remaining;info.rewards_remaining=0
  assert(m.d_monthCardUI.todayGoldHasTaken())
  local n=#sent;m.d_monthCardUI.pressGetGold();assert(#sent==n)
  info.rewards_remaining=remaining
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
 check('restore_callbacks_and_original_item_text',function()
  r.pressClose();v._localVipRestore()
  assert(r._localCardOpen==nil and r._localSingleOpen==nil)
  assert(m.d_packageUI.g_itemAttrTable[1156].introduction~='等同于充值5元')
 end)
end,debug.traceback)
if r._localCardCancel then pcall(r._localCardCancel) end
if r.g_self and r.g_self.main_layer then pcall(r.pressClose) end
if v._localVipRestore then pcall(v._localVipRestore) end
for i=#saved,1,-1 do
 local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end
 for k,val in pairs(row.old) do row.t[k]=val end
end
m.MS_report_error=report
layer:removeAllChildrenWithCleanup(true);layer:release()
if not ok then return 'fixture:false:'..tostring(err) end
return table.concat(checks,'\n')
