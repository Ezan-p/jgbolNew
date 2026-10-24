local ms=assert(package.loaded.ms)
local v=ms.d_vipUI
local hadAdapter=v._localVipRestore
local saved={player=ms.d_mainUI.g_playerInfo,config=ms.d_data.g_new_config,send=ms.d_u.main_server_send_msg,waiting=ms.d_u.g_is_waiting_1106}
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
ms.d_data.g_new_config=ms.d_c.table_copy(saved.config)
ms.d_u.main_server_send_msg=function(...) end
local results={}
local function check(name,fn)
 local ok,err=xpcall(fn,debug.traceback)
 results[#results+1]={name=name,ok=ok,error=not ok and tostring(err) or nil}
end

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
        local products = {{["id"]=1,["gold"]=100},{["id"]=2,["gold"]=500},{["id"]=3,["gold"]=1000},{["id"]=4,["gold"]=5000},{["id"]=5,["gold"]=10000},{["id"]=6,["gold"]=50000},{["id"]=101,["gold"]=100,["bonus"]=0,["ui_index"]=1},{["id"]=102,["gold"]=500,["bonus"]=50,["ui_index"]=2},{["id"]=103,["gold"]=1000,["bonus"]=110,["ui_index"]=3},{["id"]=104,["gold"]=2000,["bonus"]=240,["ui_index"]=4},{["id"]=105,["gold"]=5000,["bonus"]=650,["ui_index"]=5},{["id"]=106,["gold"]=10000,["bonus"]=1500,["ui_index"]=6}}
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
            -- Local settlement has standard tier bonuses, no first-charge doubling.
            r.g_self.hasCharged = true
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

ms.d_data.g_new_config[1]={[0]={["charge_gold"]=0,["lingyu_count"]=0,["day_take_gold_limit"]=0,["day_pick_cortege_limit"]={[1]=0,[2]=0,[3]=0}},[1]={["charge_gold"]=100,["lingyu_count"]=10,["day_take_gold_limit"]=0,["day_pick_cortege_limit"]={[1]=0,[2]=0,[3]=0}},[2]={["charge_gold"]=500,["lingyu_count"]=20,["day_take_gold_limit"]=0,["day_pick_cortege_limit"]={[1]=0,[2]=0,[3]=0}},[3]={["charge_gold"]=1000,["lingyu_count"]=30,["day_take_gold_limit"]=0,["day_pick_cortege_limit"]={[1]=0,[2]=0,[3]=0}},[4]={["charge_gold"]=2000,["lingyu_count"]=40,["day_take_gold_limit"]=20,["day_pick_cortege_limit"]={[1]=0,[2]=0,[3]=0}},[5]={["charge_gold"]=5000,["lingyu_count"]=50,["day_take_gold_limit"]=30,["day_pick_cortege_limit"]={[1]=0,[2]=0,[3]=0}},[6]={["charge_gold"]=10000,["lingyu_count"]=60,["day_take_gold_limit"]=40,["day_pick_cortege_limit"]={[1]=0,[2]=0,[3]=0}},[7]={["charge_gold"]=20000,["lingyu_count"]=80,["day_take_gold_limit"]=50,["day_pick_cortege_limit"]={[1]=0,[2]=0,[3]=0}},[8]={["charge_gold"]=50000,["lingyu_count"]=100,["day_take_gold_limit"]=60,["day_pick_cortege_limit"]={[1]=0,[2]=0,[3]=0}},[9]={["charge_gold"]=100000,["lingyu_count"]=120,["day_take_gold_limit"]=80,["day_pick_cortege_limit"]={[1]=0,[2]=0,[3]=0}},[10]={["charge_gold"]=200000,["lingyu_count"]=150,["day_take_gold_limit"]=100,["day_pick_cortege_limit"]={[1]=0,[2]=0,[3]=0}}}
ms.d_data.g_new_config.local_vip={["charge_gold"]=200000,["vip_level"]=10,["vip_gift"]=0,["next_charge_gold"]=200000,["day_take_gold_limit"]=100,["enhance_inbatch_limit"]=1,["strength_item_limit"]=3,["energy_item_limit"]=3,["tollgate_flush_limit"]=0}
check('open',function() v.show() end)
check('page_1',function() v.g_self.main_layer:removeAllChildrenWithCleanup(true);v.createMainFrame(v.g_self.main_layer,1) end)
check('preview_1',function() v.pressVipGiftDetail(1);ms.d_messageUI.destroyLayer() end)
check('gift_1',function() ms.d_mainUI.g_playerInfo.vip_gift=2;v.callback_take_vip_gift({["type_id"]=1101,["count"]=1});ms.d_messageUI.destroyLayer() end)
check('page_2',function() v.g_self.main_layer:removeAllChildrenWithCleanup(true);v.createMainFrame(v.g_self.main_layer,2) end)
check('preview_2',function() v.pressVipGiftDetail(2);ms.d_messageUI.destroyLayer() end)
check('gift_2',function() ms.d_mainUI.g_playerInfo.vip_gift=6;v.callback_take_vip_gift({["type_id"]=1102,["count"]=1});ms.d_messageUI.destroyLayer() end)
check('page_3',function() v.g_self.main_layer:removeAllChildrenWithCleanup(true);v.createMainFrame(v.g_self.main_layer,3) end)
check('preview_3',function() v.pressVipGiftDetail(3);ms.d_messageUI.destroyLayer() end)
check('gift_3',function() ms.d_mainUI.g_playerInfo.vip_gift=14;v.callback_take_vip_gift({["type_id"]=1103,["count"]=1});ms.d_messageUI.destroyLayer() end)
check('page_4',function() v.g_self.main_layer:removeAllChildrenWithCleanup(true);v.createMainFrame(v.g_self.main_layer,4) end)
check('preview_4',function() v.pressVipGiftDetail(4);ms.d_messageUI.destroyLayer() end)
check('gift_4',function() ms.d_mainUI.g_playerInfo.vip_gift=30;v.callback_take_vip_gift({["type_id"]=1104,["count"]=1});ms.d_messageUI.destroyLayer() end)
check('page_5',function() v.g_self.main_layer:removeAllChildrenWithCleanup(true);v.createMainFrame(v.g_self.main_layer,5) end)
check('preview_5',function() v.pressVipGiftDetail(5);ms.d_messageUI.destroyLayer() end)
check('gift_5',function() ms.d_mainUI.g_playerInfo.vip_gift=62;v.callback_take_vip_gift({["type_id"]=1105,["count"]=1});ms.d_messageUI.destroyLayer() end)
check('page_6',function() v.g_self.main_layer:removeAllChildrenWithCleanup(true);v.createMainFrame(v.g_self.main_layer,6) end)
check('preview_6',function() v.pressVipGiftDetail(6);ms.d_messageUI.destroyLayer() end)
check('gift_6',function() ms.d_mainUI.g_playerInfo.vip_gift=126;v.callback_take_vip_gift({["type_id"]=1106,["count"]=1});ms.d_messageUI.destroyLayer() end)
check('page_7',function() v.g_self.main_layer:removeAllChildrenWithCleanup(true);v.createMainFrame(v.g_self.main_layer,7) end)
check('preview_7',function() v.pressVipGiftDetail(7);ms.d_messageUI.destroyLayer() end)
check('gift_7',function() ms.d_mainUI.g_playerInfo.vip_gift=254;v.callback_take_vip_gift({["type_id"]=1107,["count"]=1});ms.d_messageUI.destroyLayer() end)
check('page_8',function() v.g_self.main_layer:removeAllChildrenWithCleanup(true);v.createMainFrame(v.g_self.main_layer,8) end)
check('preview_8',function() v.pressVipGiftDetail(8);ms.d_messageUI.destroyLayer() end)
check('gift_8',function() ms.d_mainUI.g_playerInfo.vip_gift=510;v.callback_take_vip_gift({["type_id"]=1108,["count"]=1});ms.d_messageUI.destroyLayer() end)
check('page_9',function() v.g_self.main_layer:removeAllChildrenWithCleanup(true);v.createMainFrame(v.g_self.main_layer,9) end)
check('preview_9',function() v.pressVipGiftDetail(9);ms.d_messageUI.destroyLayer() end)
check('gift_9',function() ms.d_mainUI.g_playerInfo.vip_gift=1022;v.callback_take_vip_gift({["type_id"]=1109,["count"]=1});ms.d_messageUI.destroyLayer() end)
check('page_10',function() v.g_self.main_layer:removeAllChildrenWithCleanup(true);v.createMainFrame(v.g_self.main_layer,10) end)
check('preview_10',function() v.pressVipGiftDetail(10);ms.d_messageUI.destroyLayer() end)
check('gift_10',function() ms.d_mainUI.g_playerInfo.vip_gift=2046;v.callback_take_vip_gift({["type_id"]=1110,["count"]=1});ms.d_messageUI.destroyLayer() end)
check('open_gift_1',function() ms.d_commonLayerUI.recvUsedItem({["result"]=1,["type_id"]=1101,["count"]=1,["attach_list"]={[1]={["object_type"]=12,["attach_type"]=1,["attach_count"]=1000000,["attach_level"]=1},[2]={["object_type"]=5,["attach_type"]=1021,["attach_count"]=3,["attach_level"]=1}}});ms.d_messageUI.destroyLayer() end)
check('open_gift_2',function() ms.d_commonLayerUI.recvUsedItem({["result"]=1,["type_id"]=1102,["count"]=1,["attach_list"]={[1]={["object_type"]=12,["attach_type"]=1,["attach_count"]=1500000,["attach_level"]=1},[2]={["object_type"]=5,["attach_type"]=1021,["attach_count"]=3,["attach_level"]=1},[3]={["object_type"]=5,["attach_type"]=1002,["attach_count"]=3,["attach_level"]=1},[4]={["object_type"]=5,["attach_type"]=1006,["attach_count"]=1,["attach_level"]=1},[5]={["object_type"]=5,["attach_type"]=3016,["attach_count"]=1,["attach_level"]=1}}});ms.d_messageUI.destroyLayer() end)
check('open_gift_3',function() ms.d_commonLayerUI.recvUsedItem({["result"]=1,["type_id"]=1103,["count"]=1,["attach_list"]={[1]={["object_type"]=12,["attach_type"]=1,["attach_count"]=2000000,["attach_level"]=1},[2]={["object_type"]=5,["attach_type"]=1001,["attach_count"]=500,["attach_level"]=1},[3]={["object_type"]=5,["attach_type"]=2010,["attach_count"]=1,["attach_level"]=1},[4]={["object_type"]=5,["attach_type"]=1002,["attach_count"]=3,["attach_level"]=1},[5]={["object_type"]=5,["attach_type"]=1021,["attach_count"]=5,["attach_level"]=1},[6]={["object_type"]=5,["attach_type"]=1006,["attach_count"]=1,["attach_level"]=1}}});ms.d_messageUI.destroyLayer() end)
check('open_gift_4',function() ms.d_commonLayerUI.recvUsedItem({["result"]=1,["type_id"]=1104,["count"]=1,["attach_list"]={[1]={["object_type"]=12,["attach_type"]=1,["attach_count"]=3000000,["attach_level"]=1},[2]={["object_type"]=5,["attach_type"]=1001,["attach_count"]=800,["attach_level"]=1},[3]={["object_type"]=5,["attach_type"]=1002,["attach_count"]=3,["attach_level"]=1},[4]={["object_type"]=5,["attach_type"]=1021,["attach_count"]=5,["attach_level"]=1},[5]={["object_type"]=5,["attach_type"]=1006,["attach_count"]=3,["attach_level"]=1},[6]={["object_type"]=5,["attach_type"]=4008,["attach_count"]=1,["attach_level"]=1}}});ms.d_messageUI.destroyLayer() end)
check('open_gift_5',function() ms.d_commonLayerUI.recvUsedItem({["result"]=1,["type_id"]=1105,["count"]=1,["attach_list"]={[1]={["object_type"]=12,["attach_type"]=1,["attach_count"]=5000000,["attach_level"]=1},[2]={["object_type"]=5,["attach_type"]=1001,["attach_count"]=1000,["attach_level"]=1},[3]={["object_type"]=5,["attach_type"]=1002,["attach_count"]=3,["attach_level"]=1},[4]={["object_type"]=5,["attach_type"]=1021,["attach_count"]=5,["attach_level"]=1},[5]={["object_type"]=5,["attach_type"]=2015,["attach_count"]=1,["attach_level"]=1},[6]={["object_type"]=5,["attach_type"]=4012,["attach_count"]=1,["attach_level"]=1},[7]={["object_type"]=5,["attach_type"]=1006,["attach_count"]=3,["attach_level"]=1}}});ms.d_messageUI.destroyLayer() end)
check('open_gift_6',function() ms.d_commonLayerUI.recvUsedItem({["result"]=1,["type_id"]=1106,["count"]=1,["attach_list"]={[1]={["object_type"]=12,["attach_type"]=1,["attach_count"]=6000000,["attach_level"]=1},[2]={["object_type"]=5,["attach_type"]=1001,["attach_count"]=1600,["attach_level"]=1},[3]={["object_type"]=5,["attach_type"]=1006,["attach_count"]=5,["attach_level"]=1},[4]={["object_type"]=5,["attach_type"]=2003,["attach_count"]=1,["attach_level"]=1}}});ms.d_messageUI.destroyLayer() end)
check('open_gift_7',function() ms.d_commonLayerUI.recvUsedItem({["result"]=1,["type_id"]=1107,["count"]=1,["attach_list"]={[1]={["object_type"]=12,["attach_type"]=1,["attach_count"]=7000000,["attach_level"]=1},[2]={["object_type"]=5,["attach_type"]=1001,["attach_count"]=2500,["attach_level"]=1},[3]={["object_type"]=5,["attach_type"]=3007,["attach_count"]=1,["attach_level"]=1},[4]={["object_type"]=5,["attach_type"]=4001,["attach_count"]=1,["attach_level"]=1},[5]={["object_type"]=5,["attach_type"]=1007,["attach_count"]=3,["attach_level"]=1}}});ms.d_messageUI.destroyLayer() end)
check('open_gift_8',function() ms.d_commonLayerUI.recvUsedItem({["result"]=1,["type_id"]=1108,["count"]=1,["attach_list"]={[1]={["object_type"]=12,["attach_type"]=1,["attach_count"]=8000000,["attach_level"]=1},[2]={["object_type"]=5,["attach_type"]=2007,["attach_count"]=1,["attach_level"]=1},[3]={["object_type"]=5,["attach_type"]=4003,["attach_count"]=1,["attach_level"]=1},[4]={["object_type"]=6,["attach_type"]=43,["attach_count"]=1,["attach_level"]=1},[5]={["object_type"]=5,["attach_type"]=1007,["attach_count"]=3,["attach_level"]=1}}});ms.d_messageUI.destroyLayer() end)
check('open_gift_9',function() ms.d_commonLayerUI.recvUsedItem({["result"]=1,["type_id"]=1109,["count"]=1,["attach_list"]={[1]={["object_type"]=12,["attach_type"]=1,["attach_count"]=9000000,["attach_level"]=1},[2]={["object_type"]=5,["attach_type"]=3005,["attach_count"]=1,["attach_level"]=1},[3]={["object_type"]=5,["attach_type"]=4007,["attach_count"]=1,["attach_level"]=1},[4]={["object_type"]=6,["attach_type"]=23,["attach_count"]=1,["attach_level"]=1},[5]={["object_type"]=5,["attach_type"]=1007,["attach_count"]=5,["attach_level"]=1}}});ms.d_messageUI.destroyLayer() end)
check('open_gift_10',function() ms.d_commonLayerUI.recvUsedItem({["result"]=1,["type_id"]=1110,["count"]=1,["attach_list"]={[1]={["object_type"]=12,["attach_type"]=1,["attach_count"]=10000000,["attach_level"]=1},[2]={["object_type"]=5,["attach_type"]=2008,["attach_count"]=1,["attach_level"]=1},[3]={["object_type"]=5,["attach_type"]=3002,["attach_count"]=1,["attach_level"]=1},[4]={["object_type"]=5,["attach_type"]=4004,["attach_count"]=1,["attach_level"]=1},[5]={["object_type"]=6,["attach_type"]=42,["attach_count"]=1,["attach_level"]=1},[6]={["object_type"]=5,["attach_type"]=1007,["attach_count"]=5,["attach_level"]=1}}});ms.d_messageUI.destroyLayer() end)
check('daily',function() v.callback_take_vip_gold({["gold_count"]=100,["lingyu_count"]=150}) end)
check('recharge_menu',function() v.pressRecharge();assert(ms.d_rechargeUI.g_self.main_layer);ms.d_rechargeUI.pressClose() end)
check('recharge_send',function()
 local captured
 ms.d_u.main_server_send_msg=function(mid,data) captured={mid=mid,data=data} end
 ms.d_u.g_is_waiting_1106=false
 v.show();v.pressRecharge()
 local r=ms.d_rechargeUI
 local button=tolua.cast(r.g_self.menu:getChildByTag(r.g_self.button_tag+1),'CCMenuItem')
 button:activate()
 assert(captured and captured.mid==1111 and captured.data.event_id==250)
 local data=assert(loadstring('return '..captured.data.data))()
 assert(data.item_id==101 and type(data.order_id)=='string')
end)
check('close',function() ms.d_rechargeUI.pressClose() end)
if not hadAdapter and v._localVipRestore then v._localVipRestore() end
ms.d_mainUI.g_playerInfo=saved.player
ms.d_data.g_new_config=saved.config
ms.d_u.main_server_send_msg=saved.send
ms.d_u.g_is_waiting_1106=saved.waiting
return table.tostring({results=results,restored=true})
