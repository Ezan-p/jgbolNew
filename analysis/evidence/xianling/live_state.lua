local ms=assert(package.loaded.ms)
local x=ms.d_xianlingShopUI.g_self
return table.tostring({config=x.config,shop_data=x.shop_data,month_charge=x.month_charge,canbuy_count=x.canbuy_count,take_list=x.take_list,adapter=ms.d_vipUI._localVipRestore~=nil})
