local ms=assert(package.loaded.ms)
ms.d_xianlingShopUI.closeShop()
ms.d_shopUI.recharge()
return table.tostring({menu=CCDirector:sharedDirector():getRunningScene():getChildByTag(709001)~=nil})
