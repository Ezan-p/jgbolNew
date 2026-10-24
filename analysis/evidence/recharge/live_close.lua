local m=assert(package.loaded.ms)
m.d_rechargeUI.pressClose()
return table.tostring({vip=m.d_mainUI.g_playerInfo.vip_level,header_digits=#m.d_mainUI.g_mainUI.playerInfoTab.vip_number})
