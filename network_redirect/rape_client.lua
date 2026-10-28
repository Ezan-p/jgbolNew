-- Native Continue used query flag 1, which only reloaded the cleared board.
-- Flag 4 requests a server-validated next board; ordinary queries stay read-only.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_crossDoomUI
 if not ui then return 'pending' end
 if not ui._localRapeRestore then
  local oldContinue=ui.pressGoOnCard
  local oldInfo=ui.callbackRapeInfo
  local oldHead=ui.createCardHead
  -- Native createCardHead only has layouts for 2..6 guards (lines 1751..1775).
  -- Keep its tag, menu and enemy-map contracts for a single centered guard.
  ui.createCardHead=function(card_num,head_list,call_back,is_fast_show)
   if #head_list~=1 then return oldHead(card_num,head_list,call_back,is_fast_show) end
   local state=ui.g_self
   local layer=state.cardPage_layer
   local speed=is_fast_show and 0.01 or 1
   local x,y=(card_num*2-1)/6-0.005,state.h3+state.h5/2
   local tag=card_num*100+1
   ms.d_u.delay(layer,0.1*speed,function()
    local entry=head_list[1]
    local v=entry.v
    local head=ms.d_data.getHeadSprite(v.show_type,v.cortege_layer and v.cortege_layer>0)
    layer:addChild(ms.d_u.setStyle(head,{x=x,y=y,scaleH=state.card_h,tag=tag}),22)
    local frame=ms.d_u.createByStyle({pic='v2/crossDoom/head_frame.png'})
    entry.menu=ms.d_u.createMenu({x=0,y=0,{nsprite=frame,ssprite=frame,
     x=x,y=y,scaleH=state.card_h,tag=tag,opacity=1,call_back=ui.pressFightNpc}})
    entry.head_sprite=head
    entry.x=x*ms.d_u.getW();entry.y=y*ms.d_u.getH()
    state.cardPage_enmey_map[tag]=entry
    layer:addChild(entry.menu,23)
    if v.has_win then ms.d_u.setStyles(head,{color={32,64,64}}) end
   end)
   if call_back then ms.d_u.delay(layer,0.3*speed,call_back) end
  end
  ui.pressGoOnCard=function(...)
   local state=ui.g_self
   if not state or not state.card_data then return oldContinue(...) end
   ms.d_music_mgr.playClickEffect()
   ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_update_rape_info,{flag=4})
  end
  ui.callbackRapeInfo=function(data)
   -- Native callbacks only clear this flag for query responses (update_type=1).
   -- A refreshed board must also clear the prior sweep's completed UI state.
   if data and data.rape_list and ui.g_self then ui.g_self.is_all_pass=false end
   return oldInfo(data)
  end
  ui._localRapeRestore=function()
   ui.pressGoOnCard=oldContinue;ui.callbackRapeInfo=oldInfo
   ui.createCardHead=oldHead
   ui._localRapeRestore=nil
  end
 end
end
