-- Compatibility fixes only; preserve the original monument and record layouts.
do
 local ms=package.loaded.ms
 local m=ms and ms.d_monumentUI
 local r=ms and ms.d_fightrecordUI
 if not m or not r then return 'pending' end
 if not m._localMonumentRestore then
  local receive=m.onGetMonumentData
  local save=r.save_fight_record
  m.onGetMonumentData=function(data)
   -- Recompute switches after configuration/reconnection; original caches once.
   m.g_self.Config=nil
   return receive(data)
  end
  r.save_fight_record=function(records,fightType)
   if fightType==118 then
    -- Original pairs(records) cannot also carry the fight_type scalar it reads.
    -- Clear stale previous-day records, then repair the per-record replay type.
    r.g_fight_record={}
    save(records,fightType)
    for _,record in pairs(r.g_fight_record) do
     record.fightInfo.fight_result_msg.fight_type=fightType
    end
   else return save(records,fightType) end
  end
  m._localMonumentRestore=function()
   m.onGetMonumentData=receive;r.save_fight_record=save
   m._localMonumentRestore=nil
  end
 end
end

-- The public fortune window is shared by the monument and guild feast.
do
 local ms=package.loaded.ms
 local party=ms and ms.d_guildPartyUI
 if not party then return 'pending' end
 if not party._localWealthRestore then
  local native=party.showRankLayer
  party.showRankLayer=function(data)
   if not data.wealth_weekly then return native(data) end
   local create=ms.d_u.createByStyles
   local headings={'名次','姓名','财富分','捐赠资金','普通礼盒','高级礼盒'}
   ms.d_u.createByStyles=function(style,...)
    local index=style.pic and string.match(style.pic,'^v2/guildPartyUI/r([1-6])%.png$')
    if index then
     local copy={};for k,v in pairs(style) do copy[k]=v end
     copy.pic=nil;copy.type='label';copy.fontsize=22
     copy.string=headings[tonumber(index)];copy.color={255,170,100}
     return create(copy,...)
    end
    if style.type=='label' and type(style.string)=='string' and
       string.find(style.string,ms.d_hz.gethz('party_rank1'),1,true)==1 then
     local copy={};for k,v in pairs(style) do copy[k]=v end
     copy.fontsize=20
     local rank=data.order>0 and tostring(data.order) or '待首次结算'
     copy.string='上次结算名次：'..rank..'  本周累计：'..tostring(data.current_score or 0)..'分\n每周一00:00（北京时间）结算，离线自动补结算\nVIP×1000＋捐赠资金÷10＋普通礼盒×10＋高级礼盒×50'
     return create(copy,...)
    end
    return create(style,...)
   end
   local ok,result=pcall(native,data)
   ms.d_u.createByStyles=create
   if not ok then error(result) end
   return result
  end
  party._localWealthRestore=function()
   party.showRankLayer=native;party._localWealthRestore=nil
  end
 end
end
