-- Preserve complete battle/event payloads across the native 32 KB packet boundary.
do
 local ms=package.loaded.ms
 if not (ms and ms.d_event_mgr and ms.d_event_mgr.callback_fight_extra_logic
  and ms.d_fightUI and ms.d_fightUI.actFight and ms.d_fightUI.showFightEnd and table.loadstring) then return 'pending' end
 if not ms._localBattleReplayRestore then
  local event,fight=ms.d_event_mgr,ms.d_fightUI
  local undo,fragments,cache,cacheOrder={},{},{},{}
  local battleEvents,battleResults,battleOrder={},{},{}
  local nativeLoad=table.loadstring
  local function replace(t,key,fn)
   local old=t[key];t[key]=fn;undo[#undo+1]=function() t[key]=old end
  end
  local function fail(message)
   if ms.d_alert and ms.d_alert.stop_wait then ms.d_alert.stop_wait() end
   if ms.d_info and ms.d_info.show then ms.d_info.show(message) end
   error(message,2)
  end
  local function copy(value,seen)
   if type(value)~='table' then return value end
   seen=seen or {};if seen[value] then return seen[value] end
   local out={};seen[value]=out
   for key,item in pairs(value) do out[key]=copy(item,seen) end
   return out
  end
  local function hydrate(value,depth,resolved)
   if type(value)~='table' then return value end
   depth=depth or 0
   if depth>64 then return fail('战报数据层级异常，请重新打开战报') end
   local key=value._local_replay_id
   if key~=nil then
    if type(key)~='string' or not cache[key] then return fail('战报尚未加载完整，请重新打开战报') end
    if resolved then resolved.count=resolved.count+1 end
    -- Native arena/history pages mutate replay results and counts in place.
    -- A fresh copy keeps those pages from modifying the preloaded source.
    return hydrate(copy(cache[key]),depth+1,resolved)
   end
   if type(value._local_replay_parts)=='table' then
    local merged={}
    for _,part in ipairs(value._local_replay_parts) do
     part=hydrate(part,depth+1,resolved)
     for field,item in pairs(part) do
      if merged[field]~=nil then return fail('战报分组字段重复，请重新打开战报') end
      merged[field]=item
     end
    end
    return merged
   end
   for key,item in pairs(value) do
    if type(item)=='table' then value[key]=hydrate(item,depth+1,resolved) end
   end
   return value
  end
  local function trimCache()
   -- Only trim after a response has resolved every reference. A response can
   -- legitimately preload more records than the retained history cache size.
   while #cacheOrder>64 do local key=table.remove(cacheOrder,1);cache[key]=nil end
  end
  replace(table,'loadstring',function(source,...)
   local value=nativeLoad(source,...)
   if type(source)=='string' and string.find(source,'_local_replay_id',1,true) then
    local resolved={count=0};value=hydrate(value,nil,resolved)
    -- Chunk payload strings may themselves contain the marker. They are not
    -- consumers yet and must not evict preloads needed by a later response.
    if resolved.count>0 then trimCache() end
   end
   return value
  end)

  local nativeEvents=event.callback_fight_extra_logic
  local function retainBattle(id)
   for i=#battleOrder,1,-1 do if battleOrder[i]==id then table.remove(battleOrder,i);break end end
   battleOrder[#battleOrder+1]=id
   while #battleOrder>20 do
    local old=table.remove(battleOrder,1);battleEvents[old]=nil;battleResults[old]=nil
   end
  end
  local function receiveEvents(data,...)
   if type(data)=='table' and data.fight_id then
    retainBattle(data.fight_id)
    if type(data.offline_battle_result)=='table' then
     local result=data.offline_battle_result
     if result.fight_id~=data.fight_id or type(result.fight_result)~='table'
      or result.fight_round~=#result.fight_result then
      return fail('战报动作数据异常，请重新打开战报')
     end
     battleResults[data.fight_id]=copy(result)
     return
    end
    battleEvents[data.fight_id]=copy(data)
    data=copy(data);data.opening_passives=nil
   end
   return nativeEvents(data,...)
  end
  replace(event,'callback_fight_extra_logic',function(data,...)
   local chunk=type(data)=='table' and data.offline_battle_chunk
   if not chunk then return receiveEvents(data,...) end
   if type(chunk)~='table' or (chunk.kind~='events' and chunk.kind~='replay')
    or type(chunk.key)~='string' or #chunk.key>128 or type(chunk.payload)~='string'
    or #chunk.payload>32768 or type(chunk.total)~='number' or chunk.total%1~=0
    or chunk.total<1 or chunk.total>256 or type(chunk.index)~='number'
    or chunk.index%1~=0 or chunk.index<1 or chunk.index>chunk.total then
    return fail('战报分包格式异常，请重新打开战报')
   end
   local key=chunk.kind..':'..chunk.key
   local group=fragments[key]
   if not group then
    group={total=chunk.total,parts={},count=0,fight_id=data.fight_id,bytes=0};fragments[key]=group
   end
   if group.total~=chunk.total or group.fight_id~=data.fight_id then
    fragments[key]=nil;return fail('战报分包不一致，请重新打开战报')
   end
   local previous=group.parts[chunk.index]
   if previous and previous~=chunk.payload then
    fragments[key]=nil;return fail('战报分包重复冲突，请重新打开战报')
   end
   if not previous then
    group.parts[chunk.index]=chunk.payload;group.count=group.count+1;group.bytes=group.bytes+#chunk.payload
   end
   if group.bytes>4*1024*1024 then fragments[key]=nil;return fail('战报数据过大，请重新打开战报') end
   if group.count<group.total then return end
   fragments[key]=nil
   local ok,value=pcall(nativeLoad,table.concat(group.parts))
   if not ok or type(value)~='table' then return fail('战报数据无法解析，请重新打开战报') end
   if chunk.kind=='events' then
    if value.fight_id~=data.fight_id then return fail('战报事件编号不一致，请重新打开战报') end
    return receiveEvents(value,...)
   end
   if not cache[chunk.key] then cacheOrder[#cacheOrder+1]=chunk.key end
   cache[chunk.key]=value
  end)

  local function completeResult(result)
   if type(result)~='table' or result.guide_stage~=255 then return result end
   local full=battleResults[result.fight_id]
   if not full or full.fight_type~=result.fight_type or full.final_result~=result.final_result then
    return fail('战报动作尚未加载完整，请重新打开战报')
   end
   return copy(full)
  end
  -- Registered dispatch tables keep function references, not the named fields.
  -- Replace both so every live receiver sees the full result before native UI.
  for _,entry in ipairs({{1027,'fight_result_1027'},{1140,'special_fight_result_1140'}}) do
   local id,name=entry[1],entry[2]
   local original=event[name]
   if original then
    local wrapped=function(head,data,...)
     return original(head,completeResult(data),...)
    end
    replace(event,name,wrapped)
    if event.g_msg_fun and event.g_msg_fun[id] then replace(event.g_msg_fun,id,wrapped) end
   end
  end

  local nativeFight=fight.actFight
  replace(fight,'actFight',function(replay,...)
   local ok,value=pcall(function() return hydrate(copy(replay)) end)
   if not ok then return end -- fail() has already released the wait mask and explained the error.
   replay=value
   if type(replay)=='table' then
    replay.fight_result_msg=completeResult(replay.fight_result_msg)
    local fid=replay.line_up_msg and replay.line_up_msg.fight_id
    local effects=type(replay.fight_events)=='table' and copy(replay.fight_events)
     or fid and copy(battleEvents[fid])
    if not effects and fid and event.get_fight_events then effects=copy(event.get_fight_events(fid)) end
    if type(effects)=='table' then
     -- Native characters read passive actions into lastBuffList and play them
     -- on actual entry, including reserves. Their values already exist in the
     -- authoritative lineup; zero-damage display rows never grant them twice.
     local opening=effects.opening_passives;effects.opening_passives=nil
     local result=replay.fight_result_msg
     if type(opening)=='table' and #opening>0 and result and type(result.fight_result)=='table' then
      local actions={}
      for _,row in ipairs(opening) do actions[#actions+1]=copy(row) end
      for _,row in ipairs(result.fight_result) do actions[#actions+1]=row end
      result.fight_result=actions
      -- showFightEvents uses the displayed action index, whereas native entry
      -- timing uses iAttackStepNoBuff. Shift only the copied visual events.
      for _,effect in pairs(effects) do
       if type(effect)=='table' and type(effect.cur_action)=='number' then effect.cur_action=effect.cur_action+#opening end
      end
     end
     replay.fight_events=effects
     -- Native cache misses are truthy empty tables; explicitly restore these
     -- copied events before playback instead of relying on its fallback.
     nativeEvents(effects)
    end
    if replay.line_up_msg and replay.line_up_msg.lineup then replay.line_up_msg.lineup_count=#replay.line_up_msg.lineup end
    if replay.fight_result_msg and replay.fight_result_msg.fight_result then replay.fight_result_msg.fight_round=#replay.fight_result_msg.fight_result end
   end
   return nativeFight(replay,...)
  end)

  local nativeEnd=fight.showFightEnd
  replace(fight,'showFightEnd',function(...)
   if fight.g_fightUI.last_final_result~=0 then return nativeEnd(...) end
   -- getLastFightRet clamps 0 to 1 (the native "险胜" sprite). Keep the
   -- authoritative result at zero: getLastFightStar and return/reward paths
   -- must still see no victory. Change only the native result presentation.
   local create,sound=ms.d_u.createByStyle,ms.d_u.playSoundEffect
   ms.d_u.createByStyle=function(options,...)
    if options.pic=='v2/fightUI/succ1.png' then
     options=copy(options);options.pic=nil;options.type='label'
     -- Native sprite scale=2 means twice screen width; it makes text blurry
     -- and enormous. Render at font resolution, retaining only its position.
     options.scale=nil;options.scaleH=nil;options.scaleX=nil;options.scaleY=nil
     options.size=nil;options.font_rect=nil
     options.string='平局';options.fontsize=320;options.color={230,230,230}
    end
    return create(options,...)
   end
   ms.d_u.playSoundEffect=function(name,...)
    if name~='fight_succ' then return sound(name,...) end
   end
   local ok,result=pcall(nativeEnd,...)
   ms.d_u.createByStyle=create;ms.d_u.playSoundEffect=sound
   if not ok then error(result) end
   return result
  end)
  ms._localBattleReplayRestore=function()
   for index=#undo,1,-1 do undo[index]() end
   ms._localBattleReplayRestore=nil
  end
 end
end
