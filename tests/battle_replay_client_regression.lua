local source=...
local checks={}
local function check(name,fn) fn();checks[#checks+1]=name end
local function encode(v)
 if type(v)=='number' or type(v)=='boolean' then return tostring(v) end
 if type(v)=='string' then return string.format('%q',v) end
 local out={};for k,item in pairs(v) do out[#out+1]='['..encode(k)..']='..encode(item) end
 return '{'..table.concat(out,',')..'}'
end
local loadData=function(s) return assert(loadstring('return '..s))() end
table.loadstring=loadData
local received,played,drawn,sounds,errors={},{},{},{},{}
local stopped=0;local eventCache={}
local nativeEvents=function(data) received[#received+1]=data;eventCache[data.fight_id]=data end
local nativeFight=function(data,kind)
 played[#played+1]={data=data,kind=kind,events=data and data.line_up_msg and eventCache[data.line_up_msg.fight_id]}
 return 'played'
end
local failCreate=false
local create=function(options) if failCreate then error('renderer failed') end;drawn[#drawn+1]=options;return options end
local sound=function(name) sounds[#sounds+1]=name end
local ms={d_event_mgr={callback_fight_extra_logic=nativeEvents},d_fightUI={actFight=nativeFight,g_fightUI={last_final_result=0}},
 d_u={createByStyle=create,playSoundEffect=sound},d_alert={stop_wait=function() stopped=stopped+1 end},
 d_info={show=function(message) errors[#errors+1]=message end}}
local fight=ms.d_fightUI
local attacks={}
fight.showFightDetailStepByStep=function()
 fight.g_fightUI.iAttackStep=fight.g_fightUI.iAttackStep+1
end
local nativeAttack=function(action,marker)
 attacks[#attacks+1]={action=action,marker=marker}
 fight.g_fightUI.iAttackStepNoBuff=fight.g_fightUI.iAttackStepNoBuff+1
 fight.showFightDetailStepByStep()
 return 'attack'
end
fight.showSingleAttackEffect=nativeAttack
local nativeResult=function(head,data) received[#received+1]={result=data};return data end
ms.d_event_mgr.fight_result_1027=nativeResult
ms.d_event_mgr.special_fight_result_1140=nativeResult
ms.d_event_mgr.g_msg_fun={[1027]=nativeResult,[1140]=nativeResult}
fight.getLastFightStar=function() local r=fight.g_fightUI.last_final_result;return r>0 and r<4 and r or 0 end
local nativeEnd=function()
 local result=math.max(1,math.min(6,fight.g_fightUI.last_final_result))
 ms.d_u.createByStyle({type='sprite',pic=result<4 and 'v2/fightUI/succ'..result..'.png' or 'v2/fightUI/fail'..(result-3)..'.png',scale=2,x=0.25,y=0.7})
 ms.d_u.playSoundEffect(result<4 and 'fight_succ' or 'fight_fail')
 return 'end'
end
fight.showFightEnd=nativeEnd;package.loaded.ms=ms
local visualCalls,scheduled={},{}
local character={hp=100,hp_max=100,buffs={}}
function character:addCcbiBuff(code) self.buffs[code]=true end
function character:removeCcbiBuff(code) self.buffs[code]=nil end
local function display(v,resource)
 visualCalls[#visualCalls+1]={code=v.logic_type,resource=resource,rows=v.skill_result_list}
 for _,row in ipairs(v.skill_result_list or {}) do
  if row.field==65 then character.hp=character.hp+row.field_plus end
  if row.field==9999 then character.hp=character.hp+(row.hp_add or 0);character.hp_max=character.hp_max+(row.hp_max_add or 0) end
 end
end
ms.d_skillExt={showSkillExt=function(v) display(v,'native') end,
 showNameOnly=function(v) display(v,'name') end,
 showOnceCCbiEffect=function(v,resource) display(v,resource) end,
 getTarget=function() return character end,
 set_fight_delay_time=function(before,after)
  fight.fight_step_begin_delay=math.max(fight.fight_step_begin_delay or 0,before)
 end}
local originalExt=ms.d_skillExt.showSkillExt
fight.showFightEvents=function() return 0 end
ms.d_u.delay=function(layer,delay,fn) scheduled[#scheduled+1]={delay=delay,fn=fn,sequence=#scheduled+1} end
local function flush()
 while #scheduled>0 do
  local batch=scheduled;scheduled={}
  table.sort(batch,function(a,b) return a.delay==b.delay and a.sequence<b.sequence or a.delay<b.delay end)
  for _,task in ipairs(batch) do task.fn() end
 end
end
assert(loadstring(source))()
local function chunks(kind,key,value,fid)
 local raw=encode(value);local at=math.floor(#raw/2)
 return {{fight_id=fid,offline_battle_chunk={kind=kind,key=key,index=1,total=2,payload=raw:sub(1,at)}},
  {fight_id=fid,offline_battle_chunk={kind=kind,key=key,index=2,total=2,payload=raw:sub(at+1)}}}
end
local function preload(key,value,fid)
 for _,part in ipairs(chunks('replay',key,value,fid or 77)) do ms.d_event_mgr.callback_fight_extra_logic(table.loadstring(encode(part))) end
end
check('idempotent_installation',function()
 local handler=ms.d_event_mgr.callback_fight_extra_logic;assert(loadstring(source))();assert(handler==ms.d_event_mgr.callback_fight_extra_logic)
end)
check('both_sides_healing_slots_do_not_play_zero_damage_attacks',function()
 for _,logic in ipairs({101101,102101}) do
  local state=fight.g_fightUI
  state.iAttackStep=1;state.iAttackStepNoBuff=0;attacks={};character.hp=100
  for _,side in ipairs({true,false}) do
   ms.d_skillExt.showSkillExt({logic_type=logic,skill_result_list={{field=65,field_plus=20}}})
   fight.showSingleAttackEffect({skill_type=1,self_use=true,is_src=side,
    src_order=1,des_order=1,damage_list={0,0}})
  end
  assert(character.hp==140 and #attacks==0)
  assert(state.iAttackStep==3 and state.iAttackStepNoBuff==2)
  for _,side in ipairs({true,false}) do
   local action={skill_type=1,self_use=false,is_src=side,src_order=1,des_order=1,damage_list={100,0}}
   assert(fight.showSingleAttackEffect(action,'forwarded')=='attack')
   assert(attacks[#attacks].action==action and attacks[#attacks].marker=='forwarded')
  end
  assert(#attacks==2 and state.iAttackStep==5 and state.iAttackStepNoBuff==4)
 end
 character.hp=100
end)
check('real_zero_damage_attacks_and_other_skills_still_play',function()
 for _,action in ipairs({
  {skill_type=1,self_use=false,src_order=1,des_order=1,damage_list={0}},
  {skill_type=1,self_use=true,src_order=1,des_order=1,damage_list={0,30}},
  {skill_type=6,self_use=true,src_order=1,des_order=1,damage_list={0}},
  {skill_type=22,self_use=true,src_order=1,des_order=1,damage_list={0}}
 }) do
  assert(fight.showSingleAttackEffect(action)=='attack')
 end
end)
check('all_event_chunks_merge_once_in_index_order',function()
 local data={fight_id=17,[1]={cur_action=1,speak='吸血'},[2]={cur_action=2,speak='复活'}}
 local parts=chunks('events','event-key',data,17)
 ms.d_event_mgr.callback_fight_extra_logic(parts[2]);ms.d_event_mgr.callback_fight_extra_logic(parts[2])
 assert(#received==0);ms.d_event_mgr.callback_fight_extra_logic(parts[1]);assert(#received==1)
 assert(received[1][1].speak=='吸血' and received[1][2].cur_action==2)
 ms.d_event_mgr.callback_fight_extra_logic({fight_id=18});assert(#received==2 and received[2].fight_id==18)
end)
local replay={line_up_msg={fight_id=77,lineup={{src_type=5001}}},fight_result_msg={final_result=3,fight_result={{cur_round=1}}},fight_events={fight_id=77,[1]={cur_action=1}}}
check('whole_response_and_nested_references_hydrate_before_native_handlers',function()
 preload('replay-key',replay)
 preload('response-key',{result=1,other='保留字段',fight_result_list={{_local_replay_id='replay-key'}}})
 local data=table.loadstring(encode({_local_replay_id='response-key'}))
 assert(data.other=='保留字段' and data.fight_result_list[1].line_up_msg.lineup[1].src_type==5001)
end)
check('grouped_preloads_merge_original_numeric_and_metadata_keys',function()
 preload('group-a',{[1]={cur_action=1},[2]={cur_action=2}})
 preload('group-b',{[3]={cur_action=3},fight_id=91,opening_passives={{skill_type=22}}})
 preload('group-root',{_local_replay_parts={{_local_replay_id='group-a'},{_local_replay_id='group-b'}}})
 local data=table.loadstring(encode({_local_replay_id='group-root'}))
 assert(#data==3 and data[3].cur_action==3 and data.fight_id==91 and data.opening_passives[1].skill_type==22)
end)
check('native_replay_mutation_cannot_contaminate_cached_source',function()
 local refs={{_local_replay_id='replay-key'},{_local_replay_id='replay-key'}}
 local data=table.loadstring(encode(refs));assert(data[1]~=data[2])
 data[1].fight_result_msg.final_result=6;data[1].line_up_msg.lineup[1].src_type=9999
 assert(data[2].fight_result_msg.final_result==3)
 assert(table.loadstring(encode({_local_replay_id='replay-key'})).line_up_msg.lineup[1].src_type==5001)
end)
check('missing_replay_releases_wait_and_never_starts_incomplete_battle',function()
 local count=#played;local before=stopped
 assert(not pcall(table.loadstring,encode({_local_replay_id='missing'})))
 fight.actFight({_local_replay_id='missing'},28)
 assert(#played==count and stopped==before+2 and #errors>=2)
end)
check('duplicate_chunk_conflicts_fail_without_poisoning_later_transfers',function()
 local parts=chunks('events','conflict',{fight_id=23,[1]={cur_action=1}},23)
 ms.d_event_mgr.callback_fight_extra_logic(parts[1])
 local altered=loadData(encode(parts[1]));altered.offline_battle_chunk.payload='bad'
 assert(not pcall(ms.d_event_mgr.callback_fight_extra_logic,altered))
 ms.d_event_mgr.callback_fight_extra_logic(parts[1]);ms.d_event_mgr.callback_fight_extra_logic(parts[2])
 assert(received[#received].fight_id==23)
end)
check('embedded_events_repopulate_native_cache_for_history_playback',function()
 eventCache[77]=nil;assert(fight.actFight({_local_replay_id='replay-key'},28)=='played')
 local row=played[#played];assert(row.events and row.events[1].cur_action==1)
 assert(row.data.line_up_msg.lineup_count==1 and row.data.fight_result_msg.fight_round==1)
end)
check('nine_slot_240_action_replay_is_not_truncated',function()
 local data={line_up_msg={fight_id=78,lineup={}},fight_result_msg={final_result=0,fight_result={}}}
 for i=1,9 do data.line_up_msg.lineup[i]={src_type=5000+i} end
 for i=1,240 do data.fight_result_msg.fight_result[i]={cur_round=i} end
 preload('nine',data,78);fight.actFight({_local_replay_id='nine'},30)
 local row=played[#played];assert(row.kind==30 and row.data.line_up_msg.lineup_count==9 and row.data.fight_result_msg.fight_round==240)
end)
check('draw_result_has_neutral_title_no_victory_audio_or_stars',function()
 fight.g_fightUI.last_final_result=0;local count=#sounds
 assert(fight.showFightEnd()=='end');local title=drawn[#drawn]
 assert(title.type=='label' and title.string=='平局' and title.pic==nil)
 assert(title.scale==nil and title.scaleH==nil and title.fontsize==320)
 assert(#sounds==count and fight.getLastFightStar()==0 and fight.g_fightUI.last_final_result==0)
 assert(ms.d_u.createByStyle==create and ms.d_u.playSoundEffect==sound)
end)
check('passive_display_rows_shift_copied_events_without_double_granting_or_mutation',function()
 local data=loadData(encode(replay))
 data.fight_events.opening_passives={{skill_type=22,self_use=true,is_src=true,src_order=1,des_order=1,damage_list={0}}}
 local raw=encode(data)
 fight.actFight(data,28)
 local shown=played[#played].data
 assert(#shown.fight_result_msg.fight_result==2 and shown.fight_result_msg.fight_result[1].skill_type==22)
 assert(shown.fight_result_msg.fight_result[1].damage_list[1]==0)
 assert(shown.fight_events[1].cur_action==2 and not shown.fight_events.opening_passives)
 assert(encode(data)==raw,'display preparation mutated source replay')
 fight.actFight(data,28)
 assert(#played[#played].data.fight_result_msg.fight_result==2)
 assert(played[#played].data.fight_events[1].cur_action==2)
end)
check('live_passives_are_kept_out_of_native_event_iteration',function()
 local data={fight_id=83,opening_passives={{skill_type=51}},[1]={cur_action=1}}
 ms.d_event_mgr.callback_fight_extra_logic(data)
 assert(not received[#received].opening_passives)
 fight.actFight({line_up_msg={fight_id=83},fight_result_msg={fight_result={{cur_round=1}}}},28)
 assert(#played[#played].data.fight_result_msg.fight_result==2)
 assert(played[#played].events[1].cur_action==2)
end)
check('visual_metadata_is_not_iterated_as_a_native_event_and_replay_does_not_duplicate_it',function()
 local data={fight_id=840,opening_passives={{skill_type=22}},essence_visuals={
  {cur_action=0,logic_type=102131,who_use=1,src_order=1,des_order=1,self_use=true,offline_essence_visual=true,
   skill_result_list={{field=71,field_plus=500,des_order=1}}},
  {cur_action=1,after_action=true,logic_type=102161,who_use=1,src_order=1,des_order=1,self_use=true,offline_essence_visual=true,
   skill_result_list={{field=65,field_plus=-90,des_order=1}}}}}
 local raw=encode(data)
 ms.d_event_mgr.callback_fight_extra_logic(data)
 assert(not received[#received].essence_visuals and not received[#received].opening_passives)
 for attempt=1,2 do
  fight.actFight({line_up_msg={fight_id=840},fight_result_msg={fight_result={{cur_round=1},{cur_round=1}}}},28)
  fight.g_fightUI.lastAttackInfos=played[#played].data.fight_result_msg.fight_result
  local start=#visualCalls
  fight.g_fightUI.iAttackStep=2;fight.showFightEvents();flush()
  assert(#visualCalls==start+1 and visualCalls[#visualCalls].resource=='zhiliao001.ccbi')
  fight.g_fightUI.iAttackStep=3;fight.showFightEvents();flush()
  assert(#visualCalls==start+2 and character.buffs[102161])
  assert(character.hp==100 and character.hp_max==100,'display changed authoritative HP')
 end
 assert(encode(data)==raw)
end)
check('all_38_name_and_effect_routes_are_display_only_including_lucky_and_intimidation_fallbacks',function()
 for _,tier in ipairs({101000,102000}) do
  for family=1,19 do
   local v={logic_type=tier+family*10+1,who_use=1,src_order=1,des_order=1,self_use=true,offline_essence_visual=true,
    skill_result_list={{field=9999,field_plus=50,hp_add=50,hp_max_add=50,des_order=1}}}
   ms.d_skillExt.showSkillExt(v)
   assert(visualCalls[#visualCalls].code==v.logic_type)
   assert(character.hp==100 and character.hp_max==100)
  end
 end
 ms.d_skillExt.showSkillExt({logic_type=102012,who_use=1,src_order=1,offline_essence_visual=true,skill_result_list={}})
 assert(visualCalls[#visualCalls].code==102011)
 ms.d_skillExt.showSkillExt({logic_type=102142,who_use=1,src_order=1,offline_essence_visual=true,skill_result_list={}})
 assert(visualCalls[#visualCalls].code==102142)
end)
check('cleanse_expiry_and_intimidation_consumption_remove_both_tier_icons',function()
 for _,code in ipairs({101013,102013,101163,102163,101171,102171}) do
  character.buffs={[101011]=true,[102011]=true,[101161]=true,[102161]=true}
  ms.d_skillExt.showSkillExt({logic_type=code,who_use=1,src_order=1,offline_essence_visual=true,
   skill_result_list={{des_order=1}}})
  local family=code%1000==13 and 1 or 16
  assert(not character.buffs[101000+family*10+1] and not character.buffs[102000+family*10+1])
 end
end)
check('runtime_blessing_uses_native_art_and_applies_increment_exactly_once',function()
 ms.d_skillExt.showSkillExt({logic_type=102181,who_use=1,src_order=1,des_order=2,self_use=true,
  skill_result_list={{field=9999,field_plus=10,hp_add=20,hp_max_add=20,des_order=2}}})
 assert(visualCalls[#visualCalls].resource=='zhufu001.ccbi')
 assert(character.hp==120 and character.hp_max==120)
 local source={fight_id=849,opening_passives={{skill_type=22}},[1]={cur_action=2,logic_type=102181,
  who_use=1,src_order=5,skill_result_list={{field=9999,hp_add=20,hp_max_add=20}}}}
 local replay={line_up_msg={fight_id=849},fight_result_msg={fight_result={{},{},{}}},fight_events=source}
 for i=1,2 do
  fight.actFight(replay,28)
  assert(played[#played].events[1].cur_action==4,'blessing must follow death and passive prefix')
  assert(source[1].cur_action==2,'replaying shifted original blessing')
 end
end)
check('terminal_visuals_finish_before_result_and_new_fights_clear_pending_notices',function()
 local notices={}
 for i=1,4 do notices[i]={cur_action=1,after_action=true,logic_type=101000+i*10+1,who_use=1,src_order=1,
  offline_essence_visual=true,skill_result_list={{des_order=1}}} end
 fight.actFight({line_up_msg={fight_id=850},fight_result_msg={fight_result={{cur_round=1}}},
  fight_events={fight_id=850,essence_visuals=notices}},28)
 fight.g_fightUI.lastAttackInfos={{}};fight.g_fightUI.iAttackStep=2
 local count=#drawn;fight.showFightEvents();fight.showFightEnd()
 assert(#drawn==count);flush();assert(#drawn>count)
 fight.actFight({line_up_msg={fight_id=851},fight_result_msg={fight_result={{cur_round=1}}},fight_events={fight_id=851}},28)
 local count=#visualCalls;fight.showFightEvents();flush();assert(#visualCalls==count)
end)
check('long_result_preload_is_restored_before_both_native_protocol_handlers',function()
 for _,id in ipairs({1027,1140}) do
  local data={fight_id=id,fight_type=28,final_result=0,fight_round=540,fight_result={}}
  for i=1,540 do data.fight_result[i]={cur_round=math.ceil(i/18)} end
  ms.d_event_mgr.callback_fight_extra_logic({fight_id=id,offline_battle_result=data})
  local notice={fight_id=id,fight_type=28,final_result=0,guide_stage=255,fight_round=0,fight_result={}}
  local complete=ms.d_event_mgr.g_msg_fun[id](nil,notice)
  assert(#complete.fight_result==540 and complete.fight_round==540 and #notice.fight_result==0)
  fight.actFight({line_up_msg={fight_id=id},fight_result_msg=notice},28)
  assert(#played[#played].data.fight_result_msg.fight_result==540)
 end
end)
check('missing_long_result_never_reaches_native_receiver',function()
 local count=#received
 assert(not pcall(ms.d_event_mgr.g_msg_fun[1027],nil,{fight_id=9087,guide_stage=255}))
 assert(#received==count)
end)
check('standalone_long_results_keep_only_recent_twenty_fights',function()
 for id=2001,2021 do
  ms.d_event_mgr.callback_fight_extra_logic({fight_id=id,offline_battle_result={fight_id=id,fight_type=28,final_result=0,fight_round=0,fight_result={}}})
 end
 assert(not pcall(ms.d_event_mgr.g_msg_fun[1027],nil,{fight_id=2001,fight_type=28,final_result=0,guide_stage=255}))
 assert(ms.d_event_mgr.g_msg_fun[1027](nil,{fight_id=2021,fight_type=28,final_result=0,guide_stage=255}).fight_id==2021)
end)
check('renderer_failure_cannot_leave_global_presentation_hooks_installed',function()
 fight.g_fightUI.last_final_result=0;failCreate=true
 assert(not pcall(fight.showFightEnd));failCreate=false
 assert(ms.d_u.createByStyle==create and ms.d_u.playSoundEffect==sound)
end)
check('all_six_real_win_loss_results_keep_native_titles_and_audio',function()
 for result=1,6 do
  fight.g_fightUI.last_final_result=result;fight.showFightEnd()
  assert(drawn[#drawn].type=='sprite')
  assert(sounds[#sounds]==(result<4 and 'fight_succ' or 'fight_fail'))
 end
end)
check('all_references_resolve_before_bounded_cache_is_trimmed',function()
 local refs={}
 for i=1,70 do preload('many-'..i,{value=i});refs[i]={_local_replay_id='many-'..i} end
 preload('many-response',refs)
 local value=table.loadstring(encode({_local_replay_id='many-response'}));for i=1,70 do assert(value[i].value==i) end
end)
check('unload_restores_original_functions',function()
 assert(fight.showSingleAttackEffect~=nativeAttack)
 ms._localBattleReplayRestore()
 assert(fight.showSingleAttackEffect==nativeAttack)
 assert(not ms._localBattleReplayRestore and table.loadstring==loadData)
 assert(fight.actFight==nativeFight and fight.showFightEnd==nativeEnd and ms.d_event_mgr.callback_fight_extra_logic==nativeEvents)
 assert(ms.d_event_mgr.g_msg_fun[1027]==nativeResult and ms.d_event_mgr.g_msg_fun[1140]==nativeResult)
 assert(ms.d_skillExt.showSkillExt==originalExt)
end)
return table.concat(checks,'\n')
