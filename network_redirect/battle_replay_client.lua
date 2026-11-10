-- Preserve complete battle/event payloads across the native 32 KB packet boundary.
do
 local ms=package.loaded.ms
 if not (ms and ms.d_event_mgr and ms.d_event_mgr.callback_fight_extra_logic
  and ms.d_fightUI and ms.d_fightUI.actFight and ms.d_fightUI.showFightEnd and table.loadstring) then return 'pending' end
 if not ms._localBattleReplayRestore then
  local event,fight=ms.d_event_mgr,ms.d_fightUI
  local undo,fragments,cache,cacheOrder={},{},{},{}
  local battleEvents,battleResults,battleOrder={},{},{}
  local essenceByAction={}
  local endingVisualWait=0
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
    data=copy(data);data.opening_passives=nil;data.essence_visuals=nil
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

  -- Pure visual notices use original name plates/CCBI assets. Do not call
  -- native strong-assault/passive handlers: those also mutate damage or HP.
  local ext=ms.d_skillExt
  if ext and ext.showSkillExt and ext.showOnceCCbiEffect and ext.showNameOnly then
   local nativeExt=ext.showSkillExt
   local art={
    [2]={'pojia001.ccbi',2.5},[4]={'fashufanghu.ccbi',2},
    [6]={'gedang001.ccbi',3},[8]={'fashufanghu001.ccbi',3},
    [9]={'fashuchuantou001.ccbi',3},[12]={'zhanyi001.ccbi',3},
    [13]={'zhiliao001.ccbi',2.5},[18]={'zhufu001.ccbi',4}
   }
   local function clearIcons(v,family)
    for _,row in ipairs(v.skill_result_list or {}) do
     local char=ext.getTarget(v,row)
     if char and char.removeCcbiBuff then
      char:removeCcbiBuff(101000+family*10+1)
      char:removeCcbiBuff(102000+family*10+1)
     end
    end
   end
   replace(ext,'showSkillExt',function(value,...)
    if not value.offline_essence_visual then
     -- Native showZhufu expects a passive attackInfo, but runtime blessing
     -- increments arrive as HP events. Keep field=9999 and consume it once.
     if value.logic_type%1000==181 and not value.attackInfo then
      ext.set_fight_delay_time(1.6,1)
      if fight.g_fightUI.iAttackStep and fight.g_fightUI.iAttackStep>#(fight.g_fightUI.lastAttackInfos or {}) then
       endingVisualWait=math.max(endingVisualWait,1.6)
      end
      -- The entrant's strength name can occupy the first 0.7 seconds.
      return ext.showOnceCCbiEffect(value,'zhufu001.ccbi',0.8,false,4)
     end
     return nativeExt(value,...)
    end
    local v=copy(value)
    local code=v.logic_type%1000
    local family=math.floor(code/10)
    -- Authoritative HP deltas are separate events. Strip all attribute fields
    -- even if a future producer accidentally puts a value in a visual notice.
    for _,row in ipairs(v.skill_result_list or {}) do
     for key in pairs(row) do if key~='des_order' then row[key]=nil end end
     row.field=0;row.field_plus=0
    end
    if code==13 or code==163 then return clearIcons(v,family) end
    if code==171 then clearIcons(v,16) end
    if code==11 or code==161 then
     clearIcons(v,family)
     for _,row in ipairs(v.skill_result_list) do
      local char=ext.getTarget(v,row)
      if char and char.hp>0 then char:addCcbiBuff(v.logic_type) end
     end
    end
    -- Native 012 is disabled and 141 has no dispatcher; both have the same
    -- original family name plate. 142 is the original lucky-dodge name code.
    if code~=142 then v.logic_type=math.floor(v.logic_type/10)*10+1 end
    local resource=art[family]
    if resource and v.visual_detail~='assault_bonus' then
     return ext.showOnceCCbiEffect(v,resource[1],0,false,resource[2])
    end
    return ext.showNameOnly(v,0)
   end)
   if fight.showFightEvents then
    local nativeFightEvents=fight.showFightEvents
    replace(fight,'showFightEvents',function(...)
     local count=nativeFightEvents(...) or 0
     local notices=essenceByAction[fight.g_fightUI.iAttackStep] or {}
     -- Preserve application/removal order; stagger names from the same caster.
     -- The last-action+1 hook also runs before the result screen.
     local offsets={};local orderedDelay=0
     for _,notice in ipairs(notices) do
      local v=copy(notice);local key=v.who_use..':'..v.src_order
      local delay=math.max(orderedDelay,offsets[key] or 0)
      orderedDelay=delay+0.05
      offsets[key]=delay+0.7
      ms.d_u.delay(fight.g_fightUI.layerFrontground,delay,function() ext.showSkillExt(v) end)
      ext.set_fight_delay_time(delay+0.8,0)
      if fight.g_fightUI.iAttackStep>#(fight.g_fightUI.lastAttackInfos or {}) then
       endingVisualWait=math.max(endingVisualWait,delay+0.8)
      end
     end
     return count+#notices
    end)
   end
  end

  -- Upkeep HP events need their own timeline slots (poison/revival ordering
  -- and reserve entry depend on them). Native skill-1 playback ignores
  -- self_use and animates these zero-damage slots as attacks on the enemy.
  -- Events and their delays have already run before showSingleAttackEffect.
  if fight.showSingleAttackEffect and fight.showFightDetailStepByStep then
   local nativeAttack=fight.showSingleAttackEffect
   replace(fight,'showSingleAttackEffect',function(action,...)
    local upkeep=action.self_use==true and action.skill_type==1
     and action.src_order==action.des_order and type(action.damage_list)=='table'
     and #action.damage_list>0
    if upkeep then
     for _,damage in pairs(action.damage_list) do
      if damage~=0 then upkeep=false;break end
     end
    end
    if upkeep then
     -- Keep the native non-passive action counter aligned with lineup entry.
     local state=fight.g_fightUI
     state.iAttackStepNoBuff=state.iAttackStepNoBuff+1
     return fight.showFightDetailStepByStep()
    end
    return nativeAttack(action,...)
   end)
  end

  local nativeFight=fight.actFight
  replace(fight,'actFight',function(replay,...)
   local ok,value=pcall(function() return hydrate(copy(replay)) end)
   if not ok then return end -- fail() has already released the wait mask and explained the error.
   replay=value
   essenceByAction={}
   endingVisualWait=0
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
     local visuals=effects.essence_visuals;effects.essence_visuals=nil
     local offset=type(opening)=='table' and #opening or 0
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
     if type(visuals)=='table' then
      if not (ext and ext.showNameOnly and fight.showFightEvents) then
       return fail('精魄特效尚未加载，请重新打开战报')
      end
      for _,notice in ipairs(visuals) do
       local step=math.max(1,(notice.cur_action or 0)+(notice.after_action and 1 or 0))+offset
       essenceByAction[step]=essenceByAction[step] or {}
       essenceByAction[step][#essenceByAction[step]+1]=copy(notice)
      end
     end
     -- Runtime blessing is caused by the death/deployment at cur_action.
     -- Native events run BEFORE that action, so display/apply the increment
     -- at the next step, after the reserve has actually entered the scene.
     for _,effect in pairs(effects) do
      if type(effect)=='table' and type(effect.logic_type)=='number'
       and effect.logic_type%1000==181 and not effect.attackInfo then
       for _,row in ipairs(effect.skill_result_list or {}) do
        if row.field==9999 then effect.cur_action=effect.cur_action+1;break end
       end
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
   if endingVisualWait>0 then
    local delay,args=endingVisualWait,{...};endingVisualWait=0
    return ms.d_u.delay(fight.g_fightUI.layerFrontground,delay,function() fight.showFightEnd(unpack(args)) end)
   end
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
