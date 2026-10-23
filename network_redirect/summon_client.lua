-- Installed only by the explicitly enabled offline service, on the Lua thread.
local prices = __SUMMON_GOLD_PRICES__
local s = package.loaded['ui.summonUI']
local ms = package.loaded['ms']
if not ms or type(s) ~= 'table' or type(s.startSummon) ~= 'function'
        or type(s.updateSummonLabels) ~= 'function' or type(s.updateSummonNews) ~= 'function'
        or not ms.d_data or type(ms.d_data.getItemCountByType) ~= 'function' then
    return 'pending'
end
if s._localGoldRestore then return 'ready' end
local originalStart, originalLabels, originalBanshu = s.startSummon, s.updateSummonLabels, s.g_banshu
local originalNews, originalSort = s.updateSummonNews, s.sortNews
local originalItemCount = ms.d_data.getItemCountByType
ms.d_data.getItemCountByType = function(kind, typeId)
    local items = ms.d_packageUI and ms.d_packageUI.g_packageItemsInfo
    if kind == 5 and (typeId == 1006 or typeId == 1007) and type(items) == 'table' then
        local total = 0
        for _, item in pairs(items) do
            if item.attach_type == 5 and item.type_id == typeId then total = total + item.count end
        end
        return total
    end
    return originalItemCount(kind, typeId)
end
local tenLabelTag = 707200
s.updateSummonNews = function(data)
    if data.first_send then
        s.g_summonNews = {}
        local order = {}
        for i, row in ipairs(data.lottery_list) do order[row] = i end
        s.sortNews = function(a, b)
            if a.time ~= b.time then return a.time > b.time end
            return (order[a] or 0) < (order[b] or 0)
        end
    end
    originalNews(data)
    s.sortNews = originalSort
end
s.g_banshu = false
s.updateSummonLabels = function(...)
    originalLabels(...)
    for grade, price in ipairs(prices) do
        local entry = s.g_goldSpriteTable and s.g_goldSpriteTable[grade]
        if entry and entry.gold then entry.gold:setString(tostring(price)) end
        if grade > 1 and entry and entry.gold then
            -- Remove the previous offline adapter's optional ten-pick labels.
            entry.gold:getParent():removeChildByTag(tenLabelTag + grade, true)
        end
    end
end
s.startSummon = function(tag)
    -- Menus can retain the old callback after offline cleanup.
    if not s._localGoldRestore then return originalStart(tag) end
    local ten = tag == 102 or tag == 103
    local grade = ten and tag - 100 or tag
    -- Ten-pick consumes available tokens first and buys only the missing draws.
    if not prices[grade] or ms.d_mainUI.g_isNeedGuide == true then
        return originalStart(tag)
    end
    if type(s.getSummonerCount) == 'function' then s.getSummonerCount() end
    local tokens = s.g_summonerCount[grade] or 0
    if (ten and tokens >= 10) or (not ten and (tokens > 0 or s.g_allowSummon[grade] ~= false)) then
        return originalStart(tag)
    end
    if ms.d_u.g_is_waiting_1106 then return end
    local price = prices[grade] * (ten and (10 - math.min(10, math.max(0, tokens))) or 1)
    if (ms.d_mainUI.g_playerInfo.gold_coin or 0) < price then
        ms.d_info.show(string.format(ten and '元宝不足，召唤十次还需 %d 元宝' or '元宝不足，本次召唤需要 %d 元宝', price))
        return
    end
    -- Actual debit, daily limit and reward selection remain server-authoritative.
    s.g_pay_pick = not ten
    ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_cortege_ramdom_get,
        {pick_grade=grade, pick_type=ms.d_common_def.cortege_pick_type.pay, ten_pick=ten and 10 or 0})
end
s._localGoldRestore = function()
    s.startSummon, s.updateSummonLabels, s.g_banshu = originalStart, originalLabels, originalBanshu
    s.updateSummonNews, s.sortNews = originalNews, originalSort
    ms.d_data.getItemCountByType = originalItemCount
    s._localGoldRestore = nil
    if s.g_isInSummonPage and s.g_goldSpriteTable then
        for grade = 2, 3 do
            local entry = s.g_goldSpriteTable[grade]
            if entry and entry.gold then entry.gold:getParent():removeChildByTag(tenLabelTag + grade, true) end
        end
        s.updateSummonLabels()
    end
end
if s.g_isInSummonPage and s.g_goldSpriteTable then
    if type(s.updateSummonerLabel) == 'function' then s.updateSummonerLabel() end
    s.updateSummonLabels()
end
return 'ready'
