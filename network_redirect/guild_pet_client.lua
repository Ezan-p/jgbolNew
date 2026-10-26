-- Spirit-land settlement: publish counters before playback and use native exits.
do
 local ms=package.loaded.ms
 if not (ms and ms.d_pethuntUI and ms.d_fightUI) then return 'pending' end
 if not ms._localGuildPetRestore then
  local ui=ms.d_pethuntUI
  local native=ui.onGetResult
  ui.onGetResult=function(op,data,...)
   if data.result==1 and op==84 and data.task_state then
    ui.g_data.main=data.task_state
    -- Rebuild only the counter strip; the task/reward dialog remains intact.
    if ui.g_pethuntUI.main_layer then ui.addMainBottomLayer(ui.g_pethuntUI.main_layer) end
   end
   if data.result==1 and op==85 then
    local replay=data.fight_result_list and data.fight_result_list[1]
    if not replay then return ms.d_info.show('暂无挑战战报，请重新进入挑战') end
    ui.g_self.cur_task_index=data.task_index or ui.g_self.cur_task_index
    replay.line_up_msg.lineup_count=#replay.line_up_msg.lineup
    replay.fight_result_msg.fight_round=#replay.fight_result_msg.fight_result
    -- 28 has a native return path that rebuilds the task page and its reward.
    return ms.d_fightUI.actFight(replay,ms.d_common_def.fight_type.union_task_boss_fight)
   end
   if data.result==1 and op==87 then
    if ui.g_data.field_boss and data.left_times~=nil then ui.g_data.field_boss.left_times=data.left_times end
    if data.two_type==1 then ui.g_self.playing_hunt_ani=false end
   end
   return native(op,data,...)
  end
  ms._localGuildPetRestore=function()
   ui.onGetResult=native;ms._localGuildPetRestore=nil
  end
 end
end
