local ms=assert(package.loaded.ms);local fight=ms.d_fightUI;local mgr=ms.d_event_mgr;local fixtures=__FIXTURES__
assert(not battlePipelineRestore and not guildPetRestore and not guild_fixture_restore,'another fixture is active')
local hadPatch=ms._localBattleReplayRestore~=nil
if hadPatch then ms._localBattleReplayRestore() end
local saved={send=ms.d_u.main_server_send_msg,dispatch=mgr.g_msg_fun,report=ms.MS_report_error,
 menu=ms.d_u.createMenu,style=ms.d_u.createByStyle,patched=hadPatch,speed=fight.g_fightUI.fight_speed,skill=ms.d_skill_mgr.showSkill,rune=ms.d_runeUI.printRune,player=ms.d_mainUI.g_playerInfo,infos=mgr.g_fight_info,ids=mgr.g_fight_id_list}
local passiveCalls,runeCalls,runeCompleted={},{},0
ms.d_skill_mgr.showSkill=function(info,...)
 if info.attackInfo and ms.d_skill_mgr.isPassiveSkill(info.attackInfo.skill_type) then passiveCalls[#passiveCalls+1]=info.attackInfo.skill_type end
 return saved.skill(info,...)
end
ms.d_runeUI.printRune=function(parent,id,order,callback)
 runeCalls[#runeCalls+1]={id=id,order=order}
 return saved.rune(parent,id,order,function(...) runeCompleted=runeCompleted+1;return callback(...) end)
end
local errors={};local returnButton;local drawLabel;local resultSprite;local initialTotals
ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
ms.d_u.main_server_send_msg=function(mid,data,...)
 if mid==2999 then return saved.send(mid,data,...) end
end
local dispatch={};for mid,fn in pairs(saved.dispatch) do dispatch[mid]=mid==2999 and fn or function() end end
mgr.g_msg_fun=dispatch
ms.d_u.createMenu=function(options,...)
 for _,row in pairs(options) do
  if type(row)=='table' and row.npic=='v2/fightUI/return1.png' then returnButton=row.call_back end
 end
 return saved.menu(options,...)
end
ms.d_u.createByStyle=function(options,...)
 local node=saved.style(options,...)
 if options.string=='平局' then drawLabel=node end
 if options.pic and string.find(options.pic,'v2/fightUI/succ',1,true) then resultSprite=options.pic end
 return node
end
local installBattlePatch
function battlePipelineRestore()
 if ms._localBattleReplayRestore then ms._localBattleReplayRestore() end
 ms.d_u.createMenu=saved.menu;ms.d_u.createByStyle=saved.style
 ms.d_skill_mgr.showSkill=saved.skill;ms.d_runeUI.printRune=saved.rune;ms.d_mainUI.g_playerInfo=saved.player
 mgr.g_fight_info=saved.infos;mgr.g_fight_id_list=saved.ids
 ms.MS_report_error=saved.report;mgr.g_msg_fun=saved.dispatch;ms.d_u.main_server_send_msg=saved.send
 if saved.patched then installBattlePatch() end
 fight.g_fightUI.fight_speed=saved.speed
 mgr.setSpecialFightType(0);ms.d_mainUI.show();battlePipelineRestore=nil
 return 'restored'
end
installBattlePatch=function()
-- __BATTLE_PATCH__
end
installBattlePatch()
local function deliver(rows)
 local last
 for _,row in ipairs(rows) do
  if row.mid==2998 and row.data.id==121 then mgr.msg_common_event_2998(nil,row.data,nil)
  else last=table.loadstring(row.data.data) end
 end
 return last
end
local function cachedEvents(fid)
 local events=mgr.get_fight_events(fid);local n=0
 for _,v in pairs(events or {}) do if type(v)=='table' then n=n+1 end end
 return n
end
function battlePipelineTransport()
 deliver(fixtures.large_events)
 assert(cachedEvents(fixtures.large_event_fid)==fixtures.large_event_count,'effect chunks lost')
 local payload=assert(deliver(fixtures.large_response))
 assert(#payload.fight_result_list==fixtures.history_count,'history entries lost')
 local replay=payload.fight_result_list[#payload.fight_result_list]
 assert(#replay.fight_result_msg.fight_result==fixtures.actual_actions)
 assert(#replay.fight_events==fixtures.actual_events)
 replay.fight_result_msg.final_result=1
 local reference=fixtures.large_response[#fixtures.large_response].data.data
 local original=table.loadstring(reference)
 assert(original.fight_result_list[#original.fight_result_list].fight_result_msg.final_result==fixtures.actual_result,'cache was mutated')
 local oldInfos,oldIds=mgr.g_fight_info,mgr.g_fight_id_list
 local fid=fixtures.long9.line_up_msg.fight_id
 mgr.g_fight_info={[fid]={line_up_msg=fixtures.long9.line_up_msg}};mgr.g_fight_id_list={fid}
 for _,row in ipairs(fixtures.long_result_packets) do
  if row.mid==2998 then mgr.msg_common_event_2998(nil,row.data,0)
  else mgr.special_fight_result_1140(nil,row.data,0) end
 end
 local complete=mgr.g_fight_info[fid].fight_result_msg
 assert(complete.fight_round==540 and #complete.fight_result==540 and complete.guide_stage==0,'native receiver did not restore long result')
 mgr.g_fight_info=oldInfos;mgr.g_fight_id_list=oldIds
 return table.tostring({events=cachedEvents(fixtures.large_event_fid),records=#payload.fight_result_list,native_result_actions=complete.fight_round,errors=errors})
end
function battlePipelineStart(name)
 returnButton=nil;drawLabel=nil;resultSprite=nil;passiveCalls={};runeCalls={};runeCompleted=0
 local replay=table.loadstring(table.tostring(fixtures[name]))
 local kind=replay.fight_result_msg.fight_type
 mgr.setSpecialFightType(kind)
 ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
 ms.d_mainUI.g_playerInfo.cur_genius_type=502
 if name=='long9' then
  mgr.g_fight_info={[replay.line_up_msg.fight_id]={line_up_msg=replay.line_up_msg}};mgr.g_fight_id_list={replay.line_up_msg.fight_id}
  for _,row in ipairs(fixtures.long_result_packets) do
   if row.mid==2998 then mgr.msg_common_event_2998(nil,row.data,0)
   else mgr.special_fight_result_1140(nil,row.data,0) end
  end
  replay.fight_result_msg=mgr.g_fight_info[replay.line_up_msg.fight_id].fight_result_msg
  assert(#replay.fight_result_msg.fight_result==540,'native receiver lost long actions')
 end
 -- Deliberately evict this replay's native event cache; the embedded copy
 -- must restore effects even after viewing a long history list.
 for i=1,25 do mgr.callback_fight_extra_logic({fight_id=70000+i}) end
 fight.actFight(replay,kind)
 fight.g_fightUI.fight_speed=name=='long9' and 40 or 6
 package.loaded.main_server.change_speed(name=='long9' and 20 or 3)
 initialTotals={o=fight.g_fightUI.g_hp.o_all,e=fight.g_fightUI.g_hp.e_all}
 assert(cachedEvents(replay.line_up_msg.fight_id)==#replay.fight_events,'embedded events were not restored')
 return 'started'
end
function battlePipelinePoll()
 local state=fight.g_fightUI;local hp,hpMax={},{}
 for key,value in pairs(state.tableChar or {}) do if type(value)=='table' then hp[key]=value.hp;hpMax[key]=value.hp_max end end
 local drawSize=drawLabel and drawLabel:getContentSize()
 return table.tostring({ended=state.is_fight_end or false,button_ready=returnButton~=nil,
  result=state.last_final_result or -1,star=fight.getLastFightStar(),step=state.iAttackStep or -1,
  step_without_effects=state.iAttackStepNoBuff or -1,render_steps=#(state.lastAttackInfos or {}),
  draw=drawLabel~=nil and drawLabel:isRunning(),draw_width=drawSize and drawSize.width*drawLabel:getScaleX(),draw_height=drawSize and drawSize.height*drawLabel:getScaleY(),
  result_sprite=resultSprite or '',passives=passiveCalls,runes=runeCalls,rune_completed=runeCompleted,hp=hp,hp_max=hpMax,errors=errors})
end
function battlePipelineCheck(name)
 local state=fight.g_fightUI;local expected=fixtures[name].fight_result_msg
 assert(state.is_fight_end,'result screen missing')
 assert(state.last_final_result==expected.final_result,'result changed during playback')
 assert(#errors==0,table.concat(errors,'\n'))
 if expected.final_result==0 then
  assert(drawLabel and drawLabel:isRunning(),'draw title missing')
  assert(not resultSprite,'draw battle rendered a victory sprite')
  assert(fight.getLastFightStar()==0,'draw battle awarded a star')
  assert(drawLabel:getScaleX()<=1 and drawLabel:getContentSize().width*drawLabel:getScaleX()<300,'draw text was magnified or overflowed')
 else assert(not drawLabel,'resolved battle rendered an draw title') end
 assert(state.iAttackStep>#state.lastAttackInfos,'playback ended before the last action')
 for key,hp in pairs(fixtures.expected_hp[name]) do
  local unit=state.tableChar[key]
  assert(unit and unit.hp==hp,'client/server HP mismatch: '..key..' actual='..tostring(unit and unit.hp)..' expected='..hp)
 end
 for key,hp in pairs(fixtures.expected_max_hp[name]) do
  assert(state.tableChar[key].hp_max==hp,'client/server max HP mismatch: '..key)
 end
 assert(state.g_hp.o_all==initialTotals.o and state.g_hp.e_all==initialTotals.e,'team HP maximum changed')
 if name=='passives' then assert(#passiveCalls>=5,'native passive animations missing') end
 if name=='talent' then assert(#runeCalls==1 and runeCalls[1].id==502 and runeCalls[1].order==0 and runeCompleted==1,'rune animation did not finish') end
 local result=table.loadstring(battlePipelinePoll());result.hp_matches_server=true
 return table.tostring(result)
end
return 'ready'
