local ms=assert(package.loaded.ms)
assert(ms.d_vipUI._localVipRestore,'local recharge adapter not installed')
ms.d_xianlingShopUI.create(CCDirector:sharedDirector():getRunningScene())
return table.tostring({adapter=true,requested=true})
