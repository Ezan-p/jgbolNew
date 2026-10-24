local m=assert(package.loaded.ms)
assert(m.d_vipUI._localVipRestore)
m.d_shopUI.recharge()
return table.tostring({original_layout=m.d_rechargeUI.g_self.menu~=nil,vip=m.d_mainUI.g_playerInfo.vip_level,header_digits=#m.d_mainUI.g_mainUI.playerInfoTab.vip_number})
