local m=assert(package.loaded.ms)
local r=m.d_rechargeUI;local v=m.d_vipUI
if r.g_self.main_layer then r.pressClose() end
if v.g_self.main_layer then v.pressClose() end
if v._localVipRestore then v._localVipRestore() end
local saved={player=m.d_mainUI.g_playerInfo,config=m.d_data.g_new_config,send=m.d_u.main_server_send_msg,waiting=m.d_u.g_is_waiting_1106}
m.d_mainUI.g_playerInfo=m.d_c.table_copy(saved.player)
m.d_data.g_new_config=m.d_c.table_copy(saved.config)
local captured
m.d_u.main_server_send_msg=function(mid,data) captured={mid=mid,data=data} end
m.d_u.g_is_waiting_1106=false
local results={}
local function check(name,fn) local ok,e=xpcall(fn,debug.traceback);results[#results+1]={name=name,ok=ok,error=not ok and tostring(e) or nil} end
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

check("original_market_layout",function() m.d_shopUI.recharge();assert(r.g_self.main_layer and r.g_self.menu);assert(r.g_self.hasCharged) end)
check('purchase_button_1',function()
 local button=tolua.cast(r.g_self.menu:getChildByTag(r.g_self.button_tag+1),'CCMenuItem')
 assert(button);button:activate();assert(captured.mid==1111 and captured.data.event_id==250)
 local d=assert(loadstring('return '..captured.data.data))();assert(d.item_id==101)
end)
check('purchase_button_2',function()
 local button=tolua.cast(r.g_self.menu:getChildByTag(r.g_self.button_tag+2),'CCMenuItem')
 assert(button);button:activate();assert(captured.mid==1111 and captured.data.event_id==250)
 local d=assert(loadstring('return '..captured.data.data))();assert(d.item_id==102)
end)
check('purchase_button_3',function()
 local button=tolua.cast(r.g_self.menu:getChildByTag(r.g_self.button_tag+3),'CCMenuItem')
 assert(button);button:activate();assert(captured.mid==1111 and captured.data.event_id==250)
 local d=assert(loadstring('return '..captured.data.data))();assert(d.item_id==103)
end)
check('purchase_button_4',function()
 local button=tolua.cast(r.g_self.menu:getChildByTag(r.g_self.button_tag+4),'CCMenuItem')
 assert(button);button:activate();assert(captured.mid==1111 and captured.data.event_id==250)
 local d=assert(loadstring('return '..captured.data.data))();assert(d.item_id==104)
end)
check('purchase_button_5',function()
 local button=tolua.cast(r.g_self.menu:getChildByTag(r.g_self.button_tag+5),'CCMenuItem')
 assert(button);button:activate();assert(captured.mid==1111 and captured.data.event_id==250)
 local d=assert(loadstring('return '..captured.data.data))();assert(d.item_id==105)
end)
check('purchase_button_6',function()
 local button=tolua.cast(r.g_self.menu:getChildByTag(r.g_self.button_tag+6),'CCMenuItem')
 assert(button);button:activate();assert(captured.mid==1111 and captured.data.event_id==250)
 local d=assert(loadstring('return '..captured.data.data))();assert(d.item_id==106)
end)
check('credit_1_vip_1',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=100,["vip_level"]=1,["vip_gift"]=0,["next_charge_gold"]=500,["day_take_gold_limit"]=0,["enhance_inbatch_limit"]=0,["strength_item_limit"]=5,["energy_item_limit"]=5,["top_fight_limit"]=6,["rape_flush_limit"]=4,["convert_fight_limit"]=2,["tollgate_flush_limit"]=1}})
 assert(m.d_mainUI.g_playerInfo.vip_level==1)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==1 or digits[1]~=old) and #digits==#"1")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_2_vip_2',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=600,["vip_level"]=2,["vip_gift"]=0,["next_charge_gold"]=1000,["day_take_gold_limit"]=0,["enhance_inbatch_limit"]=0,["strength_item_limit"]=8,["energy_item_limit"]=8,["top_fight_limit"]=7,["rape_flush_limit"]=5,["convert_fight_limit"]=2,["tollgate_flush_limit"]=2}})
 assert(m.d_mainUI.g_playerInfo.vip_level==2)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==2 or digits[1]~=old) and #digits==#"2")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_3_vip_3',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=1600,["vip_level"]=3,["vip_gift"]=0,["next_charge_gold"]=2000,["day_take_gold_limit"]=0,["enhance_inbatch_limit"]=1,["strength_item_limit"]=10,["energy_item_limit"]=10,["top_fight_limit"]=8,["rape_flush_limit"]=6,["convert_fight_limit"]=3,["tollgate_flush_limit"]=3}})
 assert(m.d_mainUI.g_playerInfo.vip_level==3)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==3 or digits[1]~=old) and #digits==#"3")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_4_vip_4',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=3600,["vip_level"]=4,["vip_gift"]=0,["next_charge_gold"]=5000,["day_take_gold_limit"]=20,["enhance_inbatch_limit"]=1,["strength_item_limit"]=12,["energy_item_limit"]=12,["top_fight_limit"]=10,["rape_flush_limit"]=7,["convert_fight_limit"]=3,["tollgate_flush_limit"]=3}})
 assert(m.d_mainUI.g_playerInfo.vip_level==4)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==4 or digits[1]~=old) and #digits==#"4")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_5_vip_5',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=8600,["vip_level"]=5,["vip_gift"]=0,["next_charge_gold"]=10000,["day_take_gold_limit"]=30,["enhance_inbatch_limit"]=1,["strength_item_limit"]=14,["energy_item_limit"]=14,["top_fight_limit"]=12,["rape_flush_limit"]=8,["convert_fight_limit"]=4,["tollgate_flush_limit"]=4}})
 assert(m.d_mainUI.g_playerInfo.vip_level==5)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==5 or digits[1]~=old) and #digits==#"5")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_6_vip_6',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=18600,["vip_level"]=6,["vip_gift"]=0,["next_charge_gold"]=20000,["day_take_gold_limit"]=40,["enhance_inbatch_limit"]=1,["strength_item_limit"]=16,["energy_item_limit"]=16,["top_fight_limit"]=12,["rape_flush_limit"]=9,["convert_fight_limit"]=5,["tollgate_flush_limit"]=5}})
 assert(m.d_mainUI.g_playerInfo.vip_level==6)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==6 or digits[1]~=old) and #digits==#"6")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_7_vip_7',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=28600,["vip_level"]=7,["vip_gift"]=0,["next_charge_gold"]=50000,["day_take_gold_limit"]=50,["enhance_inbatch_limit"]=1,["strength_item_limit"]=18,["energy_item_limit"]=18,["top_fight_limit"]=12,["rape_flush_limit"]=10,["convert_fight_limit"]=6,["tollgate_flush_limit"]=6}})
 assert(m.d_mainUI.g_playerInfo.vip_level==7)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==7 or digits[1]~=old) and #digits==#"7")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_8_vip_7',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=38600,["vip_level"]=7,["vip_gift"]=0,["next_charge_gold"]=50000,["day_take_gold_limit"]=50,["enhance_inbatch_limit"]=1,["strength_item_limit"]=18,["energy_item_limit"]=18,["top_fight_limit"]=12,["rape_flush_limit"]=10,["convert_fight_limit"]=6,["tollgate_flush_limit"]=6}})
 assert(m.d_mainUI.g_playerInfo.vip_level==7)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==7 or digits[1]~=old) and #digits==#"7")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_9_vip_7',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=48600,["vip_level"]=7,["vip_gift"]=0,["next_charge_gold"]=50000,["day_take_gold_limit"]=50,["enhance_inbatch_limit"]=1,["strength_item_limit"]=18,["energy_item_limit"]=18,["top_fight_limit"]=12,["rape_flush_limit"]=10,["convert_fight_limit"]=6,["tollgate_flush_limit"]=6}})
 assert(m.d_mainUI.g_playerInfo.vip_level==7)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==7 or digits[1]~=old) and #digits==#"7")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_10_vip_8',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=58600,["vip_level"]=8,["vip_gift"]=0,["next_charge_gold"]=100000,["day_take_gold_limit"]=60,["enhance_inbatch_limit"]=1,["strength_item_limit"]=18,["energy_item_limit"]=18,["top_fight_limit"]=12,["rape_flush_limit"]=11,["convert_fight_limit"]=7,["tollgate_flush_limit"]=6}})
 assert(m.d_mainUI.g_playerInfo.vip_level==8)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==8 or digits[1]~=old) and #digits==#"8")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_11_vip_8',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=68600,["vip_level"]=8,["vip_gift"]=0,["next_charge_gold"]=100000,["day_take_gold_limit"]=60,["enhance_inbatch_limit"]=1,["strength_item_limit"]=18,["energy_item_limit"]=18,["top_fight_limit"]=12,["rape_flush_limit"]=11,["convert_fight_limit"]=7,["tollgate_flush_limit"]=6}})
 assert(m.d_mainUI.g_playerInfo.vip_level==8)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==8 or digits[1]~=old) and #digits==#"8")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_12_vip_8',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=78600,["vip_level"]=8,["vip_gift"]=0,["next_charge_gold"]=100000,["day_take_gold_limit"]=60,["enhance_inbatch_limit"]=1,["strength_item_limit"]=18,["energy_item_limit"]=18,["top_fight_limit"]=12,["rape_flush_limit"]=11,["convert_fight_limit"]=7,["tollgate_flush_limit"]=6}})
 assert(m.d_mainUI.g_playerInfo.vip_level==8)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==8 or digits[1]~=old) and #digits==#"8")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_13_vip_8',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=88600,["vip_level"]=8,["vip_gift"]=0,["next_charge_gold"]=100000,["day_take_gold_limit"]=60,["enhance_inbatch_limit"]=1,["strength_item_limit"]=18,["energy_item_limit"]=18,["top_fight_limit"]=12,["rape_flush_limit"]=11,["convert_fight_limit"]=7,["tollgate_flush_limit"]=6}})
 assert(m.d_mainUI.g_playerInfo.vip_level==8)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==8 or digits[1]~=old) and #digits==#"8")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_14_vip_8',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=98600,["vip_level"]=8,["vip_gift"]=0,["next_charge_gold"]=100000,["day_take_gold_limit"]=60,["enhance_inbatch_limit"]=1,["strength_item_limit"]=18,["energy_item_limit"]=18,["top_fight_limit"]=12,["rape_flush_limit"]=11,["convert_fight_limit"]=7,["tollgate_flush_limit"]=6}})
 assert(m.d_mainUI.g_playerInfo.vip_level==8)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==8 or digits[1]~=old) and #digits==#"8")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_15_vip_9',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=108600,["vip_level"]=9,["vip_gift"]=0,["next_charge_gold"]=200000,["day_take_gold_limit"]=80,["enhance_inbatch_limit"]=1,["strength_item_limit"]=22,["energy_item_limit"]=22,["top_fight_limit"]=12,["rape_flush_limit"]=12,["convert_fight_limit"]=8,["tollgate_flush_limit"]=6}})
 assert(m.d_mainUI.g_playerInfo.vip_level==9)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==9 or digits[1]~=old) and #digits==#"9")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_16_vip_9',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=118600,["vip_level"]=9,["vip_gift"]=0,["next_charge_gold"]=200000,["day_take_gold_limit"]=80,["enhance_inbatch_limit"]=1,["strength_item_limit"]=22,["energy_item_limit"]=22,["top_fight_limit"]=12,["rape_flush_limit"]=12,["convert_fight_limit"]=8,["tollgate_flush_limit"]=6}})
 assert(m.d_mainUI.g_playerInfo.vip_level==9)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==9 or digits[1]~=old) and #digits==#"9")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_17_vip_9',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=128600,["vip_level"]=9,["vip_gift"]=0,["next_charge_gold"]=200000,["day_take_gold_limit"]=80,["enhance_inbatch_limit"]=1,["strength_item_limit"]=22,["energy_item_limit"]=22,["top_fight_limit"]=12,["rape_flush_limit"]=12,["convert_fight_limit"]=8,["tollgate_flush_limit"]=6}})
 assert(m.d_mainUI.g_playerInfo.vip_level==9)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==9 or digits[1]~=old) and #digits==#"9")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_18_vip_9',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=138600,["vip_level"]=9,["vip_gift"]=0,["next_charge_gold"]=200000,["day_take_gold_limit"]=80,["enhance_inbatch_limit"]=1,["strength_item_limit"]=22,["energy_item_limit"]=22,["top_fight_limit"]=12,["rape_flush_limit"]=12,["convert_fight_limit"]=8,["tollgate_flush_limit"]=6}})
 assert(m.d_mainUI.g_playerInfo.vip_level==9)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==9 or digits[1]~=old) and #digits==#"9")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_19_vip_9',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=148600,["vip_level"]=9,["vip_gift"]=0,["next_charge_gold"]=200000,["day_take_gold_limit"]=80,["enhance_inbatch_limit"]=1,["strength_item_limit"]=22,["energy_item_limit"]=22,["top_fight_limit"]=12,["rape_flush_limit"]=12,["convert_fight_limit"]=8,["tollgate_flush_limit"]=6}})
 assert(m.d_mainUI.g_playerInfo.vip_level==9)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==9 or digits[1]~=old) and #digits==#"9")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_20_vip_9',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=158600,["vip_level"]=9,["vip_gift"]=0,["next_charge_gold"]=200000,["day_take_gold_limit"]=80,["enhance_inbatch_limit"]=1,["strength_item_limit"]=22,["energy_item_limit"]=22,["top_fight_limit"]=12,["rape_flush_limit"]=12,["convert_fight_limit"]=8,["tollgate_flush_limit"]=6}})
 assert(m.d_mainUI.g_playerInfo.vip_level==9)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==9 or digits[1]~=old) and #digits==#"9")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_21_vip_9',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=168600,["vip_level"]=9,["vip_gift"]=0,["next_charge_gold"]=200000,["day_take_gold_limit"]=80,["enhance_inbatch_limit"]=1,["strength_item_limit"]=22,["energy_item_limit"]=22,["top_fight_limit"]=12,["rape_flush_limit"]=12,["convert_fight_limit"]=8,["tollgate_flush_limit"]=6}})
 assert(m.d_mainUI.g_playerInfo.vip_level==9)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==9 or digits[1]~=old) and #digits==#"9")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_22_vip_9',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=178600,["vip_level"]=9,["vip_gift"]=0,["next_charge_gold"]=200000,["day_take_gold_limit"]=80,["enhance_inbatch_limit"]=1,["strength_item_limit"]=22,["energy_item_limit"]=22,["top_fight_limit"]=12,["rape_flush_limit"]=12,["convert_fight_limit"]=8,["tollgate_flush_limit"]=6}})
 assert(m.d_mainUI.g_playerInfo.vip_level==9)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==9 or digits[1]~=old) and #digits==#"9")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_23_vip_9',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=188600,["vip_level"]=9,["vip_gift"]=0,["next_charge_gold"]=200000,["day_take_gold_limit"]=80,["enhance_inbatch_limit"]=1,["strength_item_limit"]=22,["energy_item_limit"]=22,["top_fight_limit"]=12,["rape_flush_limit"]=12,["convert_fight_limit"]=8,["tollgate_flush_limit"]=6}})
 assert(m.d_mainUI.g_playerInfo.vip_level==9)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==9 or digits[1]~=old) and #digits==#"9")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_24_vip_9',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=198600,["vip_level"]=9,["vip_gift"]=0,["next_charge_gold"]=200000,["day_take_gold_limit"]=80,["enhance_inbatch_limit"]=1,["strength_item_limit"]=22,["energy_item_limit"]=22,["top_fight_limit"]=12,["rape_flush_limit"]=12,["convert_fight_limit"]=8,["tollgate_flush_limit"]=6}})
 assert(m.d_mainUI.g_playerInfo.vip_level==9)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==9 or digits[1]~=old) and #digits==#"9")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_25_vip_10',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=208600,["vip_level"]=10,["vip_gift"]=0,["next_charge_gold"]=200000,["day_take_gold_limit"]=100,["enhance_inbatch_limit"]=1,["strength_item_limit"]=26,["energy_item_limit"]=26,["top_fight_limit"]=12,["rape_flush_limit"]=12,["convert_fight_limit"]=9,["tollgate_flush_limit"]=6}})
 assert(m.d_mainUI.g_playerInfo.vip_level==10)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==10 or digits[1]~=old) and #digits==#"10")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('credit_26_vip_10',function()
 local old=m.d_mainUI.g_mainUI.playerInfoTab.vip_number[1]
 local oldLevel=m.d_mainUI.g_playerInfo.vip_level
 local childCount=m.d_mainUI.g_mainUI.player_layer:getChildrenCount()
 m.d_data.callback_update_config({["local_vip"]={["charge_gold"]=218600,["vip_level"]=10,["vip_gift"]=0,["next_charge_gold"]=200000,["day_take_gold_limit"]=100,["enhance_inbatch_limit"]=1,["strength_item_limit"]=26,["energy_item_limit"]=26,["top_fight_limit"]=12,["rape_flush_limit"]=12,["convert_fight_limit"]=9,["tollgate_flush_limit"]=6}})
 assert(m.d_mainUI.g_playerInfo.vip_level==10)
 local digits=m.d_mainUI.g_mainUI.playerInfoTab.vip_number
 assert((oldLevel==10 or digits[1]~=old) and #digits==#"10")
 assert(m.d_mainUI.g_mainUI.player_layer:getChildrenCount()==childCount)
 assert(r.g_self.main_layer)
end)
check('vip_navigation',function() r.pressVIP();assert(v.g_self.main_layer);v.pressRecharge();assert(r.g_self.main_layer) end)
r.pressClose()
m.d_mainUI.g_playerInfo=saved.player;m.d_data.g_new_config=saved.config
m.d_u.main_server_send_msg=saved.send;m.d_u.g_is_waiting_1106=saved.waiting
local main=m.d_mainUI.g_mainUI
main.playerInfoTab=m.d_playerInfoUI.reloadPlayerInfo(main.player_layer)
return table.tostring({results=results,restored=true})
