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
        local notice = ms.d_actNoticeUI
        local originalFund = notice and notice.pressBuyFund
        local originalCheckVIP = ms.d_mainUI.checkVIPAnim
        local paymentCallbacks, monthCallbacks, cardDescriptions = {}, {}, {}
        local orderSequence, panel, selection, singlePage = 0, nil, nil, nil
        local displayedLevel, displayedTab
        local PANEL_TAG = 19851
        local pendingCardUse, pendingCheckout
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
        r.pressClose = function(...)
            closePanel()
            local result=originalClose(...)
            if notice and notice._localRefreshContent then notice._localRefreshContent() end
            return result
        end
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
        if notice then
            -- The native handler checks the disabled real-payment channel
            -- before sending anything, and closes the parent after prebuy.
            notice.pressBuyFund=function()
                sync()
                if (ms.d_mainUI.g_playerInfo.buy_growup or 0)~=0 then
                    ms.d_info.show('成长基金已购买，可在达到等级后领取返还');return
                end
                openPanel(productById(202))
            end
        end
        if pay then
            for _,name in ipairs({'recharge_order_request','recharge_For_IOS','pressBuyYYB','buy_item_yyb'}) do
                paymentCallbacks[name]=pay[name]
                pay[name]=function(id) openPanel(nativeProduct(id)) end
            end
            paymentCallbacks.recharge_getBalance=pay.recharge_getBalance
            pay.recharge_getBalance=function() openPanel(nativeProduct(r.g_self.cur_purchase_tag)) end
        end
        if month then
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
            if notice then notice.pressBuyFund=originalFund end
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
