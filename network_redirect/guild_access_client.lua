-- Offline entry policy, applied after the original client's activity hotfixes.
do
 local ms=package.loaded.ms
 if not (ms and ms.d_xianmengUI and ms.d_pethuntUI and ms.d_petUI and ms.d_guildFightUI and ms.d_crossRealm) then return 'pending' end
 if not ms._localGuildAccessRestore then
  local undo={}
  local function replace(t,key,fn)
   local old=t[key];t[key]=fn
   undo[#undo+1]=function() t[key]=old end
   return old
  end
  local ui=ms.d_xianmengUI
  local function upvalue(fn,key)
   for i=1,100 do
    local name,value=debug.getupvalue(fn,i)
    if name==key then return value end
    if not name then break end
   end
  end
  local createGuild=assert(upvalue(ui.getServerResponse,'createGuildLayer'))
  local original=getfenv(createGuild)
  local function enterPets()
   local guild=upvalue(ui.getServerResponse,'selfGuildInfo')
   if not guild or guild.level<5 or ms.d_mainUI.g_playerInfo.level<50 then
    return ms.d_info.show('条件不足，需要仙盟5级以上，人物等级50以上')
   end
   return ms.d_pethuntUI.enterPethunt(function()
    local layer=ui.getXianMengMainLayer()
    layer:removeAllChildrenWithCleanup(true)
    ms.d_pethuntUI.showMainLayer(layer)
   end)
  end
  -- Replace the actual island button, not just petHomeUI.show: installed
  -- live 3.87 has a level-100 gate; bundled source has the intended level 50.
  local utilities=setmetatable({createMenu=function(options,...)
   for _,option in pairs(options) do
    if type(option)=='table' and option.npic=='v2/pethuntUI/entrance1.png' then
     option.call_back=enterPets
    end
   end
   return ms.d_u.createMenu(options,...)
  end},{__index=ms.d_u})
  local proxy=setmetatable({d_u=utilities,d_petUI=setmetatable({pet_is_open=true},{__index=ms.d_petUI})},{__index=ms})
  setfenv(createGuild,setmetatable({d_ms=proxy},{__index=original,__newindex=original}))
  undo[#undo+1]=function() setfenv(createGuild,original) end
  if not __GUILD_WARS_ENABLED__ then
   local function closed() return ms.d_info.show('离线模式，暂未开放') end
   replace(ms.d_guildFightUI,'requestTimeTable',closed)
   replace(ms.d_guildFightUI,'show',closed)
   replace(ms.d_crossRealm,'sendCommonRequest',closed)
   replace(ms.d_crossRealm,'show',closed)
   local nativeShow=ui.show
   replace(ui,'show',function(kind,...)
    if kind==ui.showTypeDef.guildFight or kind==ui.showTypeDef.crossRealm then return closed() end
    return nativeShow(kind,...)
   end)
   local nativeTip=ui.getActivityTipNum
   replace(ui,'getActivityTipNum',function(kind,...)
    if kind==3 or kind==4 then return 0 end
    return nativeTip(kind,...)
   end)
  end
  ms._localGuildAccessRestore=function()
   for i=#undo,1,-1 do undo[i]() end
   ms._localGuildAccessRestore=nil
  end
 end
end
