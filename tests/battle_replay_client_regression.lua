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
 ms._localBattleReplayRestore()
 assert(not ms._localBattleReplayRestore and table.loadstring==loadData)
 assert(fight.actFight==nativeFight and fight.showFightEnd==nativeEnd and ms.d_event_mgr.callback_fight_extra_logic==nativeEvents)
 assert(ms.d_event_mgr.g_msg_fun[1027]==nativeResult and ms.d_event_mgr.g_msg_fun[1140]==nativeResult)
end)
return table.concat(checks,'\n')
