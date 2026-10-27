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
        local originalResult = r.onReceiveRechargeResult
        local originalVIP = r.pressVIP
        local originalSend = ms.d_u.main_server_send_msg
        local notice = ms.d_actNoticeUI
        local originalFund = notice and notice.pressBuyFund
        local entranceCallbacks = {}
        local originalCheckVIP = ms.d_mainUI.checkVIPAnim
        local paymentCallbacks, monthCallbacks, cardDescriptions = {}, {}, {}
        local orderSequence, panel, selection, singlePage = 0, nil, nil, nil
        local displayedLevel, displayedTab
        local PANEL_TAG = 19851
        local pendingCardUse, pendingCheckout
        local function attached(node)
            if not node then return false end
            local scene=CCDirector:sharedDirector():getRunningScene()
            local ok,result=pcall(function()
                while node do
                    if node==scene then return true end
                    node=node:getParent()
                end
                return false
            end)
            return ok and result
        end
        local function remove(node)
            -- An activity/scene may have already cleaned up its old children.
            if node then pcall(function() node:removeFromParentAndCleanup(true) end) end
        end
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
            remove(panel)
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
        -- Reuse the original conversion-window frame, parchment and quantity buttons.
        local function skin(parent,path,x,y,w,h,z)
            local node = CCSprite:create(path)
            local size = node:getContentSize()
            node:setScaleX(w/size.width);node:setScaleY(h/size.height)
            node:setPosition(ccp(x,y));parent:addChild(node,z or 1)
            return node
        end
        local function fittedText(parent,value,x,y,size,color,width,left)
            local label = text(parent,value,x,y,size,color)
            if left then label:setAnchorPoint(ccp(0,0.5)) end
            if width and label:getContentSize().width>width then label:setScale(width/label:getContentSize().width) end
            return label
        end
        local function skinButton(parent,path,pressed,title,x,y,w,h,fn,enabled,tag)
            local function face(asset,down)
                local node = CCNode:create();node:setContentSize(CCSizeMake(w,h))
                local bg=skin(node,asset,w/2,h/2,w,h)
                if not enabled then bg:setColor(ccc3(115,108,94))
                elseif down then bg:setColor(ccc3(195,164,110)) end
                if title then
                    text(node,title,w/2+1,h/2-1,22,ccc3(53,27,12))
                    fittedText(node,title,w/2,h/2+1,22,enabled and ccc3(255,226,164) or ccc3(167,155,133),w-22)
                end
                return node
            end
            local item=CCMenuItemSprite:create(face(path,false),face(pressed or path,true),face(path,false))
            item:setEnabled(enabled);item:setTag(tag);item:registerScriptTapHandler(fn)
            local menu=CCMenu:createWithItem(item);menu:setPosition(ccp(x,y));parent:addChild(menu,10)
            return item
        end
        renderPanel = function()
            if not panel or not selection then return end
            panel:removeAllChildrenWithCleanup(true)
            ms.d_u.createSwallowTouchLayer(panel)
            local director=CCDirector:sharedDirector()
            local size,origin=director:getVisibleSize(),director:getVisibleOrigin()
            local shade=CCLayerColor:create(ccc4(0,0,0,175),size.width,size.height)
            shade:setPosition(origin);panel:addChild(shade)
            local scale=math.min(size.width/960,size.height/640)
            local box=CCNode:create();box:setContentSize(CCSizeMake(780,560))
            box:setScale(scale);box:setPosition(ccp(origin.x+(size.width-780*scale)/2,origin.y+(size.height-560*scale)/2));panel:addChild(box,2)
            skin(box,'v2/kickUI/bkg4.png',390,280,780,560)
            text(box,'金 卡 充 值',391,522,31,ccc3(244,193,105))
            text(box,'金 卡 充 值',390,524,31,ccc3(46,24,12))
            skinButton(box,'v2/introUI/close1.png','v2/introUI/close2.png',nil,746,523,68,68,closePanel,true,19860)
            local s=selection
            local large,small=inventory()
            local paid=s.large_count*50+s.small_count*5
            local ready=paid==s.product.rmb and s.large_count<=large and s.small_count<=small
            fittedText(box,(s.product.name or '充值')..'  ·  需抵扣 '..s.product.rmb..' 元',390,472,23,ccc3(255,224,160),650)
            local rows={{key='large_count',name='大传世金卡',tid=1152,rmb=50,owned=large,y=396},
                        {key='small_count',name='小传世金卡',tid=1156,rmb=5,owned=small,y=286}}
            for index,row in ipairs(rows) do
                local key=row.key
                local icon=notice.getSprite({object_type=5,attach_type=row.tid,attach_count=0,attach_level=1})
                local iconSize=icon:getContentSize()
                icon:setScale(math.min(76/iconSize.width,76/iconSize.height));icon:setPosition(ccp(91,row.y));box:addChild(icon,5)
                fittedText(box,row.name,148,row.y+27,23,nil,210,true)
                text(box,'面值 '..row.rmb..' 元 / 张',222,row.y,19,ccc3(218,195,155))
                fittedText(box,'已拥有 '..row.owned..' 张',148,row.y-28,20,ccc3(244,190,52),210,true)
                skin(box,'v2/batchBuyUI/bkg.png',538,row.y+4,85,46)
                fittedText(box,tostring(s[key]),538,row.y+4,25,ccc3(51,30,14),70)
                local controls={{asset='minusT',delta=-10,x=403},{asset='minus',delta=-1,x=464},
                                {asset='add',delta=1,x=612},{asset='addT',delta=10,x=673}}
                for i,control in ipairs(controls) do
                    local delta=control.delta
                    local enabled=not s.order_id and (delta<0 and s[key]>0 or delta>0 and s[key]<row.owned)
                    skinButton(box,'v2/batchBuyUI/'..control.asset..'1.png','v2/batchBuyUI/'..control.asset..'2.png',
                        nil,control.x,row.y+4,54,46,function() change(key,delta) end,enabled,19860+index*10+i)
                end
                text(box,'抵扣 '..(s[key]*row.rmb)..' 元',538,row.y-34,18,ccc3(230,206,161))
                if index==1 then skin(box,'v2/godBlessUI/line.png',390,341,686,5) end
            end
            text(box,'已选 '..paid..' 元  /  应付 '..s.product.rmb..' 元',390,186,25,ccc3(255,221,150))
            local status='金额正好，可确认扣卡'
            if s.order_id then status='订单已提交，重试不会重复扣卡'
            elseif s.large_count>large or s.small_count>small then status='库存已变化，请重新选择金卡'
            elseif large*50+small*5<s.product.rmb then status='金卡不足，还缺 '..(s.product.rmb-large*50-small*5)..' 元面值'
            elseif paid<s.product.rmb then status='还差 '..(s.product.rmb-paid)..' 元，请增加金卡'
            elseif paid>s.product.rmb then status='多选 '..(paid-s.product.rmb)..' 元，请减少金卡' end
            fittedText(box,status,390,151,19,ready and ccc3(174,218,135) or ccc3(255,180,122),650)
            local action='v2/crossServerUI/btn_bkg.png'
            skinButton(box,action,nil,s.order_id and '关闭面板' or '取消',166,94,166,56,closePanel,true,19861)
            skinButton(box,action,nil,'自动搭配',390,94,180,56,autoSelect,not s.order_id,19862)
            skinButton(box,action,nil,s.order_id and '重试订单' or '确认扣卡',614,94,190,56,confirm,s.order_id~=nil or ready,19863)
            fittedText(box,'仅消耗所选金卡，充值额度计入 VIP、单充、累充及活动',390,43,17,ccc3(218,191,145),690)
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
        local function refreshRecharge()
            local layer=r.g_self.main_layer
            if not attached(layer) then return end
            layer:removeAllChildrenWithCleanup(true)
            ms.d_u.createSwallowTouchLayer(layer)
            r.g_self.isGiftTaken=(ms.d_mainUI.g_playerInfo.take_charge_gift_time or 0)~=0
            r.createMainFrame(layer)
        end
        r._localIsOpen=function() return attached(r.g_self.main_layer) end
        r.show = function()
            sync()
            -- Every entrance uses the current scene, never a cached activity parent.
            -- Native show() checks the real-payment flag and can refuse later opens.
            local scene=CCDirector:sharedDirector():getRunningScene()
            if attached(r.g_self.main_layer) and r.g_self.main_layer:getParent()==scene then
                r.g_self.main_layer:setVisible(true)
                scene:reorderChild(r.g_self.main_layer,100)
                return
            end
            remove(r.g_self.main_layer)
            r.g_self.main_layer=nil;r.g_self.menu=nil
            r.g_self.g_parent_layer=scene
            if not r.g_self.orders or #r.g_self.orders==0 then
                r.g_self.orders=ms.d_data.g_rechargeItemsPriceTable
            end
            r.create()
            -- Match native modal Z order so month-card/detail dialogs opened
            -- afterward can still appear above this window.
            scene:addChild(r.g_self.main_layer,100)
        end
        r.pressClose = function()
            closePanel()
            remove(r.g_self.main_layer)
            r.g_self.main_layer=nil;r.g_self.menu=nil
            -- Only explicit close refreshes the underlying activity. The original
            -- close also rebuilt a possibly stale turntable window unconditionally.
            if notice and notice._localRefreshContent then notice._localRefreshContent() end
            if month and month.g_monthCardUI and attached(month.g_monthCardUI.main_layer) then month.show() end
        end
        -- Old channel completion callbacks must not close/reopen or navigate.
        r.onReceiveRechargeResult=refreshRecharge
        r.pressVIP=function()
            r.pressClose()
            if v.g_self and attached(v.g_self.main_layer) then
                v.g_self.main_layer:setVisible(true)
            else v.show(CCDirector:sharedDirector():getRunningScene()) end
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
        v.pressRecharge = function() r.show() end
        local function bindEntrance(module,name)
            if not module or type(module[name])~='function' then return end
            entranceCallbacks[#entranceCallbacks+1]={module=module,name=name,fn=module[name]}
            module[name]=function() r.show() end
        end
        bindEntrance(notice,'gotoCharge')
        bindEntrance(notice,'pressRecharge')
        bindEntrance(ms.d_xianlingShopUI,'recharge')
        bindEntrance(ms.d_shopUI,'recharge')
        bindEntrance(ms.d_firstChargeUI,'pressRecharge')
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
                if v.g_self and attached(v.g_self.main_layer) then
                    v.g_self.main_layer:removeAllChildrenWithCleanup(true)
                    v.createMainFrame(v.g_self.main_layer)
                end
                refreshRecharge()
                if not r._localIsOpen() and month and month.g_monthCardUI and attached(month.g_monthCardUI.main_layer) then month.show() end
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
            r.onReceiveRechargeResult=originalResult
            r.pressVIP=originalVIP
            r._localIsOpen=nil
            for _,entry in ipairs(entranceCallbacks) do entry.module[entry.name]=entry.fn end
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
