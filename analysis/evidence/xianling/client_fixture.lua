local ms=assert(package.loaded.ms)
local x=ms.d_xianlingShopUI
local v=ms.d_vipUI
if v.g_self and v.g_self.main_layer then v.pressClose() end
if v._localVipRestore then v._localVipRestore() end
local saved={player=ms.d_mainUI.g_playerInfo,config=ms.d_data.g_new_config,send=ms.d_u.main_server_send_msg,
 item=ms.d_smithUI.getItemInfoByType,count=ms.d_data.getItemCountByType,shop=x.g_self,box=x.g_boxUI,waiting=ms.d_u.g_is_waiting_1106}
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
ms.d_mainUI.g_playerInfo.gold_coin=10000
ms.d_data.g_new_config=ms.d_c.table_copy(saved.config)
x.g_self=ms.d_c.table_copy(saved.shop);x.g_self.main_layer=nil
local scene=CCDirector:sharedDirector():getRunningScene()
local host=CCLayer:create();scene:addChild(host,9999)
local captured
ms.d_u.main_server_send_msg=function(mid,data) captured={mid=mid,data=data} end
ms.d_u.g_is_waiting_1106=false
ms.d_smithUI.getItemInfoByType=function(kind,tid) if kind==5 and tid==1140 then return {count=1000,type_id=1140} end return saved.item(kind,tid) end
ms.d_data.getItemCountByType=function(kind,tid) if kind==5 and tid==1249 then return 90 end return saved.count(kind,tid) end
local results={}
local function check(name,fn) local ok,err=xpcall(fn,debug.traceback);results[#results+1]={name=name,ok=ok,error=not ok and tostring(err) or nil} end

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

check('open_shop',function() x.create(host);assert(captured.mid==1336 and captured.data.flag==4) end)
check("catalog",function()
x.onGetResult({["flag"]=4,["index"]=0,["exchange_list"]={[1]={["object_type"]=5,["attach_type"]=1001,["attach_count"]=10,["attach_level"]=1,["price"]=5},[2]={["object_type"]=5,["attach_type"]=1002,["attach_count"]=1,["attach_level"]=1,["price"]=10},[3]={["object_type"]=5,["attach_type"]=1006,["attach_count"]=1,["attach_level"]=1,["price"]=30},[4]={["object_type"]=5,["attach_type"]=1007,["attach_count"]=1,["attach_level"]=1,["price"]=90},[5]={["object_type"]=5,["attach_type"]=1249,["attach_count"]=1,["attach_level"]=1,["price"]=10},[6]={["object_type"]=5,["attach_type"]=1024,["attach_count"]=1,["attach_level"]=1,["price"]=20},[7]={["object_type"]=5,["attach_type"]=1095,["attach_count"]=1,["attach_level"]=1,["price"]=100}},["shop_data"]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1249,["attach_count"]=1,["attach_level"]=1}},["need_gold"]=10},["month_charge"]=0,["canbuy_count"]=1,["charge_shop"]={[1]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=20,["attach_level"]=1}}},[2]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=100,["attach_level"]=1}}},[3]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=300,["attach_level"]=1}}},[4]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=600,["attach_level"]=1}}}},["take_list"]={[1]=1,[2]=1,[3]=1,[4]=1}})
x.updateStatus({["tip_type"]=10,["tip_info"]="{[\"had_gift\"]=false}"})
end)
check('page_two',function() x.g_self.cur_page=2;x.updateExchangeLayer() end)
check('batch_dialog',function() x.createBatchBuy(x.g_self.config[1]) end)
check("exchange",function()
x.onGetResult({["flag"]=4,["index"]=0,["exchange_list"]={[1]={["object_type"]=5,["attach_type"]=1001,["attach_count"]=10,["attach_level"]=1,["price"]=5},[2]={["object_type"]=5,["attach_type"]=1002,["attach_count"]=1,["attach_level"]=1,["price"]=10},[3]={["object_type"]=5,["attach_type"]=1006,["attach_count"]=1,["attach_level"]=1,["price"]=30},[4]={["object_type"]=5,["attach_type"]=1007,["attach_count"]=1,["attach_level"]=1,["price"]=90},[5]={["object_type"]=5,["attach_type"]=1249,["attach_count"]=1,["attach_level"]=1,["price"]=10},[6]={["object_type"]=5,["attach_type"]=1024,["attach_count"]=1,["attach_level"]=1,["price"]=20},[7]={["object_type"]=5,["attach_type"]=1095,["attach_count"]=1,["attach_level"]=1,["price"]=100}},["shop_data"]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1249,["attach_count"]=1,["attach_level"]=1}},["need_gold"]=10},["month_charge"]=0,["canbuy_count"]=1,["charge_shop"]={[1]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=20,["attach_level"]=1}}},[2]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=100,["attach_level"]=1}}},[3]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=300,["attach_level"]=1}}},[4]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=600,["attach_level"]=1}}}},["take_list"]={[1]=1,[2]=1,[3]=1,[4]=1}})
x.onGetResult({["flag"]=1,["index"]=1,["canbuy_count"]=1,["take_list"]={[1]=1,[2]=1,[3]=1,[4]=1},["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1001,["attach_count"]=20,["attach_level"]=1}}})
x.updateStatus({["tip_type"]=10,["tip_info"]="{[\"had_gift\"]=false}"})
end)
check("daily_buy",function()
x.onGetResult({["flag"]=4,["index"]=0,["exchange_list"]={[1]={["object_type"]=5,["attach_type"]=1001,["attach_count"]=10,["attach_level"]=1,["price"]=5},[2]={["object_type"]=5,["attach_type"]=1002,["attach_count"]=1,["attach_level"]=1,["price"]=10},[3]={["object_type"]=5,["attach_type"]=1006,["attach_count"]=1,["attach_level"]=1,["price"]=30},[4]={["object_type"]=5,["attach_type"]=1007,["attach_count"]=1,["attach_level"]=1,["price"]=90},[5]={["object_type"]=5,["attach_type"]=1249,["attach_count"]=1,["attach_level"]=1,["price"]=10},[6]={["object_type"]=5,["attach_type"]=1024,["attach_count"]=1,["attach_level"]=1,["price"]=20},[7]={["object_type"]=5,["attach_type"]=1095,["attach_count"]=1,["attach_level"]=1,["price"]=100}},["shop_data"]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1249,["attach_count"]=1,["attach_level"]=1}},["need_gold"]=10},["month_charge"]=0,["canbuy_count"]=0,["charge_shop"]={[1]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=20,["attach_level"]=1}}},[2]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=100,["attach_level"]=1}}},[3]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=300,["attach_level"]=1}}},[4]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=600,["attach_level"]=1}}}},["take_list"]={[1]=1,[2]=1,[3]=1,[4]=1}})
x.onGetResult({["flag"]=3,["index"]=1,["canbuy_count"]=0,["take_list"]={[1]=1,[2]=1,[3]=1,[4]=1},["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1249,["attach_count"]=1,["attach_level"]=1}}})
x.updateStatus({["tip_type"]=10,["tip_info"]="{[\"had_gift\"]=false}"})
end)
check("charge_tracking",function()
x.updateStatus({["tip_type"]=10,["tip_info"]="{[\"had_gift\"]=true}"})
end)
check("eligible_monthly",function()
x.onGetResult({["flag"]=4,["index"]=0,["exchange_list"]={[1]={["object_type"]=5,["attach_type"]=1001,["attach_count"]=10,["attach_level"]=1,["price"]=5},[2]={["object_type"]=5,["attach_type"]=1002,["attach_count"]=1,["attach_level"]=1,["price"]=10},[3]={["object_type"]=5,["attach_type"]=1006,["attach_count"]=1,["attach_level"]=1,["price"]=30},[4]={["object_type"]=5,["attach_type"]=1007,["attach_count"]=1,["attach_level"]=1,["price"]=90},[5]={["object_type"]=5,["attach_type"]=1249,["attach_count"]=1,["attach_level"]=1,["price"]=10},[6]={["object_type"]=5,["attach_type"]=1024,["attach_count"]=1,["attach_level"]=1,["price"]=20},[7]={["object_type"]=5,["attach_type"]=1095,["attach_count"]=1,["attach_level"]=1,["price"]=100}},["shop_data"]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1249,["attach_count"]=1,["attach_level"]=1}},["need_gold"]=10},["month_charge"]=5000,["canbuy_count"]=5,["charge_shop"]={[1]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=20,["attach_level"]=1}}},[2]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=100,["attach_level"]=1}}},[3]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=300,["attach_level"]=1}}},[4]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=600,["attach_level"]=1}}}},["take_list"]={[1]=2,[2]=2,[3]=2,[4]=2}})
x.updateStatus({["tip_type"]=10,["tip_info"]="{[\"had_gift\"]=true}"})
end)
check('preview_1',function() x.showGiftDetail(1);x.g_self.main_layer:removeChildByTag(x.g_self.giftDetailTag,true) end)
check("monthly_1",function()
x.onGetResult({["flag"]=4,["index"]=0,["exchange_list"]={[1]={["object_type"]=5,["attach_type"]=1001,["attach_count"]=10,["attach_level"]=1,["price"]=5},[2]={["object_type"]=5,["attach_type"]=1002,["attach_count"]=1,["attach_level"]=1,["price"]=10},[3]={["object_type"]=5,["attach_type"]=1006,["attach_count"]=1,["attach_level"]=1,["price"]=30},[4]={["object_type"]=5,["attach_type"]=1007,["attach_count"]=1,["attach_level"]=1,["price"]=90},[5]={["object_type"]=5,["attach_type"]=1249,["attach_count"]=1,["attach_level"]=1,["price"]=10},[6]={["object_type"]=5,["attach_type"]=1024,["attach_count"]=1,["attach_level"]=1,["price"]=20},[7]={["object_type"]=5,["attach_type"]=1095,["attach_count"]=1,["attach_level"]=1,["price"]=100}},["shop_data"]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1249,["attach_count"]=1,["attach_level"]=1}},["need_gold"]=10},["month_charge"]=5000,["canbuy_count"]=5,["charge_shop"]={[1]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=20,["attach_level"]=1}}},[2]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=100,["attach_level"]=1}}},[3]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=300,["attach_level"]=1}}},[4]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=600,["attach_level"]=1}}}},["take_list"]={[1]=3,[2]=2,[3]=2,[4]=2}})
x.onGetResult({["flag"]=2,["index"]=1,["canbuy_count"]=5,["take_list"]={[1]=3,[2]=2,[3]=2,[4]=2},["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=20,["attach_level"]=1}}})
x.updateStatus({["tip_type"]=10,["tip_info"]="{[\"had_gift\"]=true}"})
end)
check('preview_2',function() x.showGiftDetail(2);x.g_self.main_layer:removeChildByTag(x.g_self.giftDetailTag,true) end)
check("monthly_2",function()
x.onGetResult({["flag"]=4,["index"]=0,["exchange_list"]={[1]={["object_type"]=5,["attach_type"]=1001,["attach_count"]=10,["attach_level"]=1,["price"]=5},[2]={["object_type"]=5,["attach_type"]=1002,["attach_count"]=1,["attach_level"]=1,["price"]=10},[3]={["object_type"]=5,["attach_type"]=1006,["attach_count"]=1,["attach_level"]=1,["price"]=30},[4]={["object_type"]=5,["attach_type"]=1007,["attach_count"]=1,["attach_level"]=1,["price"]=90},[5]={["object_type"]=5,["attach_type"]=1249,["attach_count"]=1,["attach_level"]=1,["price"]=10},[6]={["object_type"]=5,["attach_type"]=1024,["attach_count"]=1,["attach_level"]=1,["price"]=20},[7]={["object_type"]=5,["attach_type"]=1095,["attach_count"]=1,["attach_level"]=1,["price"]=100}},["shop_data"]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1249,["attach_count"]=1,["attach_level"]=1}},["need_gold"]=10},["month_charge"]=5000,["canbuy_count"]=5,["charge_shop"]={[1]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=20,["attach_level"]=1}}},[2]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=100,["attach_level"]=1}}},[3]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=300,["attach_level"]=1}}},[4]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=600,["attach_level"]=1}}}},["take_list"]={[1]=3,[2]=3,[3]=2,[4]=2}})
x.onGetResult({["flag"]=2,["index"]=2,["canbuy_count"]=5,["take_list"]={[1]=3,[2]=3,[3]=2,[4]=2},["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=100,["attach_level"]=1}}})
x.updateStatus({["tip_type"]=10,["tip_info"]="{[\"had_gift\"]=true}"})
end)
check('preview_3',function() x.showGiftDetail(3);x.g_self.main_layer:removeChildByTag(x.g_self.giftDetailTag,true) end)
check("monthly_3",function()
x.onGetResult({["flag"]=4,["index"]=0,["exchange_list"]={[1]={["object_type"]=5,["attach_type"]=1001,["attach_count"]=10,["attach_level"]=1,["price"]=5},[2]={["object_type"]=5,["attach_type"]=1002,["attach_count"]=1,["attach_level"]=1,["price"]=10},[3]={["object_type"]=5,["attach_type"]=1006,["attach_count"]=1,["attach_level"]=1,["price"]=30},[4]={["object_type"]=5,["attach_type"]=1007,["attach_count"]=1,["attach_level"]=1,["price"]=90},[5]={["object_type"]=5,["attach_type"]=1249,["attach_count"]=1,["attach_level"]=1,["price"]=10},[6]={["object_type"]=5,["attach_type"]=1024,["attach_count"]=1,["attach_level"]=1,["price"]=20},[7]={["object_type"]=5,["attach_type"]=1095,["attach_count"]=1,["attach_level"]=1,["price"]=100}},["shop_data"]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1249,["attach_count"]=1,["attach_level"]=1}},["need_gold"]=10},["month_charge"]=5000,["canbuy_count"]=5,["charge_shop"]={[1]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=20,["attach_level"]=1}}},[2]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=100,["attach_level"]=1}}},[3]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=300,["attach_level"]=1}}},[4]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=600,["attach_level"]=1}}}},["take_list"]={[1]=3,[2]=3,[3]=3,[4]=2}})
x.onGetResult({["flag"]=2,["index"]=3,["canbuy_count"]=5,["take_list"]={[1]=3,[2]=3,[3]=3,[4]=2},["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=300,["attach_level"]=1}}})
x.updateStatus({["tip_type"]=10,["tip_info"]="{[\"had_gift\"]=true}"})
end)
check('preview_4',function() x.showGiftDetail(4);x.g_self.main_layer:removeChildByTag(x.g_self.giftDetailTag,true) end)
check("monthly_4",function()
x.onGetResult({["flag"]=4,["index"]=0,["exchange_list"]={[1]={["object_type"]=5,["attach_type"]=1001,["attach_count"]=10,["attach_level"]=1,["price"]=5},[2]={["object_type"]=5,["attach_type"]=1002,["attach_count"]=1,["attach_level"]=1,["price"]=10},[3]={["object_type"]=5,["attach_type"]=1006,["attach_count"]=1,["attach_level"]=1,["price"]=30},[4]={["object_type"]=5,["attach_type"]=1007,["attach_count"]=1,["attach_level"]=1,["price"]=90},[5]={["object_type"]=5,["attach_type"]=1249,["attach_count"]=1,["attach_level"]=1,["price"]=10},[6]={["object_type"]=5,["attach_type"]=1024,["attach_count"]=1,["attach_level"]=1,["price"]=20},[7]={["object_type"]=5,["attach_type"]=1095,["attach_count"]=1,["attach_level"]=1,["price"]=100}},["shop_data"]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1249,["attach_count"]=1,["attach_level"]=1}},["need_gold"]=10},["month_charge"]=5000,["canbuy_count"]=5,["charge_shop"]={[1]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=20,["attach_level"]=1}}},[2]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=100,["attach_level"]=1}}},[3]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=300,["attach_level"]=1}}},[4]={["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=600,["attach_level"]=1}}}},["take_list"]={[1]=3,[2]=3,[3]=3,[4]=3}})
x.onGetResult({["flag"]=2,["index"]=4,["canbuy_count"]=5,["take_list"]={[1]=3,[2]=3,[3]=3,[4]=3},["attach_list"]={[1]={["object_type"]=5,["attach_type"]=1140,["attach_count"]=600,["attach_level"]=1}}})
x.updateStatus({["tip_type"]=10,["tip_info"]="{[\"had_gift\"]=false}"})
end)
check('box_selector',function() x.showBoxUseLayer(host,30) end)
check("box_reward",function()
ms.d_commonLayerUI.recvUsedItem({["result"]=1,["type_id"]=1249,["count"]=30,["attach_list"]={[1]={["object_type"]=5,["attach_type"]=5001,["attach_count"]=1,["attach_level"]=1}}})
end)
check('close_shop',function() x.closeShop() end)
check('market_recharge',function()
 ms.d_shopUI.recharge()
 local r=ms.d_rechargeUI
 assert(r.g_self.main_layer)
 tolua.cast(r.g_self.menu:getChildByTag(r.g_self.button_tag+1),'CCMenuItem'):activate()
 r.pressClose()
 assert(captured.mid==1111 and captured.data.event_id==250)
 local d=assert(loadstring('return '..captured.data.data))();assert(d.item_id==101 and d.order_id)
end)
check('xianling_recharge',function()
 x.create(host);x.recharge()
 assert(ms.d_rechargeUI.g_self.main_layer);ms.d_rechargeUI.pressClose()
end)
host:removeFromParentAndCleanup(true)
x.g_self=saved.shop;x.g_boxUI=saved.box
ms.d_mainUI.g_playerInfo=saved.player;ms.d_data.g_new_config=saved.config
ms.d_u.main_server_send_msg=saved.send;ms.d_u.g_is_waiting_1106=saved.waiting
ms.d_smithUI.getItemInfoByType=saved.item;ms.d_data.getItemCountByType=saved.count
return table.tostring({results=results,restored=true})
