-- Original recharge layout [A], local settlement transport [B].
do
    local ms = package.loaded['ms']
    local v = package.loaded['ui.vipUI']
    if not ms or not v or not ms.d_rechargeUI or not ms.d_data or not ms.d_data.callback_update_config then return 'pending' end
    if not v._localVipRestore then
        local r = ms.d_rechargeUI
        local originalRecharge, originalFrame = v.pressRecharge, v.createMainFrame
        local originalConfig = ms.d_data.callback_update_config
        local originalShow, originalPurchase, originalRFrame = r.show, r.pressPurchase, r.createMainFrame
        local originalMonth, originalFirst = r.pressMonthCard, r.pressFirstCharge
        local products = __VIP_PRODUCTS__
        local originalCheckVIP = ms.d_mainUI.checkVIPAnim
        local orderSequence = 0
        local displayedLevel, displayedTab
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
        local function sync()
            local state = (ms.d_data.g_new_config or {}).local_vip
            local player = ms.d_mainUI and ms.d_mainUI.g_playerInfo
            if state and player then for k,value in pairs(state) do player[k] = value end end
        end
        v.createMainFrame = function(...)
            sync()
            return originalFrame(...)
        end
        r.createMainFrame = function(layer)
            -- Welfare settlement now preserves the original first-charge-double state.
            r.g_self.hasCharged = (ms.d_mainUI.g_playerInfo.first_charge or 0) ~= 0
            local player = ms.d_mainUI.g_playerInfo
            local threshold = player.next_charge_gold
            player.next_charge_gold = math.max(0, threshold - (player.charge_gold or 0))
            originalRFrame(layer)
            player.next_charge_gold = threshold
            local size = CCDirector:sharedDirector():getVisibleSize()
            local note = CCLabelTTF:create('本地模拟充值（不扣款）', 'Arial', 14)
            note:setPosition(size.width * 0.5, size.height * 0.965)
            layer:addChild(note, 30)
        end
        r.show = function(parent)
            sync()
            if r.g_self.main_layer then r.pressClose() end
            return originalShow(parent)
        end
        r.pressPurchase = function(tag)
            if ms.d_u.g_is_waiting_1106 then return end
            local index = tonumber(tag) and tonumber(tag) - r.g_self.button_tag
            local product
            for _,p in ipairs(products) do if p.ui_index == index then product = p end end
            if not product then return end
            orderSequence = orderSequence + 1
            local order = tostring(os.time())..'-'..tostring(math.random(100000,999999))..'-'..tostring(orderSequence)
            ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_order_request,
                {event_id=250,data=table.tostring({item_id=product.id,order_id=order})})
        end
        local function unavailable()
            ms.d_info.show('本地模拟充值：月卡与首充活动暂未开放，不发生扣款')
        end
        r.pressMonthCard, r.pressFirstCharge = unavailable, unavailable
        v.pressRecharge = function() v.pressClose(); r.show() end
        ms.d_data.callback_update_config = function(data)
            originalConfig(data)
            sync()
            if data and data.local_vip and not data.config_end then
                -- Original 1032/vip_level handler updates data and red dots only.
                -- Rebuild the original header, replacing its cached digit sprites.
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
            end
        end
        v._localVipRestore = function()
            v.pressRecharge, v.createMainFrame = originalRecharge, originalFrame
            ms.d_data.callback_update_config = originalConfig
            ms.d_mainUI.checkVIPAnim = originalCheckVIP
            r.show, r.pressPurchase, r.createMainFrame = originalShow, originalPurchase, originalRFrame
            r.pressMonthCard, r.pressFirstCharge = originalMonth, originalFirst
            v._localVipRestore = nil
        end
    end
end
