-- Run in the original client's Lua VM with .runtime/inspect_ui.py.
-- Temporarily isolates clock/data for pure original functions; always restores.
local ms=assert(package.loaded.ms)
local shop,sales=ms.d_shopUI,ms.d_salesUI
local savedTime,savedData=ms.d_time.getTime,sales.g_self.data
local checks={}
local function check(ok,name)
    assert(ok,name)
    checks[#checks+1]=name
end
local ok,err=xpcall(function()
    check(#shop.g_self.Goods[1]==8,'eight discounted rows including buns')
    check(#shop.g_self.Goods[2]==15,'fifteen normal rows including forge tokens and buns')
    for page=1,2 do
        local previous=0
        for _,row in ipairs(shop.g_self.Goods[page]) do
            check(row.csvInfo.name~=nil and row.buyInfo.order>previous,'CSV info and order '..page..'/'..row.buyInfo.index)
            previous=row.buyInfo.order
        end
    end
    local now,start=0,100000
    ms.d_time.getTime=function() return now end
    sales.g_self.data={activity_data={sale_time=start,item1_sale_count=10,item1_sale_price=75,
        sale_item={{price=150,panic_discount={0.9,0.8,0.7,0.6,0.5,0.4}},{panic_price=180,per_buy_limit=3}}},role_data={}}
    for _,case in ipairs({{0,150},{1,135},{600,135},{601,120},{1200,120},{3001,60},{3600,60},{3601,150}}) do
        now=start+case[1]
        check(sales.getCurrentPrice()==case[2],'original price at elapsed '..case[1])
        local expected=(case[1]>0 and case[1]<=3600) and sales.statusDef.item1 or sales.statusDef.none
        check(sales.getStatus()==expected,'original phase at elapsed '..case[1])
    end
    now=start+1800
    sales.g_self.data.activity_data.item1_sale_count=0
    check(sales.getStatus()==sales.statusDef.item2,'sold out switches to second item')
    check(sales.getCurrentPrice()==75,'sold out shows final first item price')
end,debug.traceback)
ms.d_time.getTime=savedTime
sales.g_self.data=savedData
assert(ok,err)
return ms.d_json.encode({checks=checks,passed=#checks,original_functions=true,clock_and_data_restored=true})
