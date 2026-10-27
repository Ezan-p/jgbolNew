local ms=assert(package.loaded.ms)
local ui=assert(ms.d_levelUpBuffUI)
local saved,checks,sent,errors,buttons={},{},{},{},{}
local function preserve(t)
 local old={};for k,v in pairs(t) do old[k]=v end;saved[#saved+1]={t=t,old=old}
end
for _,t in ipairs({ui,ms.d_mainUI,ms.d_data,ms.d_u,ms.d_time,ms.d_commonLayerUI,ms.d_alert}) do preserve(t) end
local report=ms.MS_report_error
ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
local layer=CCLayer:create();layer:retain()
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]=name..':'..tostring(ok and #errors==0)..':'..(err or '')..table.concat(errors,' ')
end
local ok,err=xpcall(function()
 if ui._localProgressionRestore then ui._localProgressionRestore() end
 ui.g_self={buff_type=1}
 ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(ms.d_mainUI.g_playerInfo)
 ms.d_mainUI.g_playerInfo.level=4
 ms.d_mainUI.g_mainUI=ms.d_c.table_copy(ms.d_mainUI.g_mainUI)
 ms.d_mainUI.g_mainUI.main_layer=layer
 ms.d_data.g_new_config=ms.d_c.table_copy(ms.d_data.g_new_config)
 ms.d_data.g_new_config[24]=ms.d_data.g_new_config[24] or {}
 ms.d_data.g_new_config[24].buff_data=ms.d_c.table_copy(FIXTURE.query)
 ms.d_time.getTime=function() return FIXTURE.now end
 ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
 ms.d_u.delay=function() end
 ms.d_alert.stop_wait=function() end
 local menu=ms.d_u.createMenu
 ms.d_u.createMenu=function(styles,...)
  for _,style in ipairs(styles) do if style.npic and style.call_back then buttons[style.npic]=style.call_back end end
  return menu(styles,...)
 end
 -- INSTALL_PATCH
 check('native_entry_and_query',function()
  assert(ui.checkHasLevelBuff());assert(ui.checkHasLevelBuffFlag())
  ui.show(layer,1000,1)
  local req=sent[#sent];assert(req.mid==1131 and req.data.flag==1 and req.data.op_type==0 and req.data.id==0)
 end)
 check('native_daily_reward_panel',function()
  ui.callback_getBuffData(ms.d_c.table_copy(FIXTURE.query))
  assert(ui.g_self.data.can_take and ui.g_self.blackmask)
  assert(buttons['v2/actNoticeUI/get1.png'])
 end)
 check('native_claim_request',function()
  buttons['v2/actNoticeUI/get1.png']()
  local req=sent[#sent];assert(req.mid==1131 and req.data.flag==2 and req.data.op_type==0 and req.data.id==0)
 end)
 check('native_claim_response',function()
  ms.d_event_mgr.msg_common_event_2998(nil,FIXTURE.claim,nil)
  assert(ui.g_self.data.can_take==false and ui.g_self.data.left_times==6)
  assert(ms.d_data.g_new_config[24].buff_data.can_take==false)
 end)
 check('same_day_reopen_queries_server',function()
  local n=#sent;ui.showLevelUpBuff(layer)
  assert(#sent==n+1 and sent[#sent].data.flag==1)
 end)
 check('native_upgrade_event_and_popups',function()
  ms.d_event_mgr.msg_common_event_2998(nil,FIXTURE.upgrade,nil)
  assert(ms.d_mainUI.g_playerInfo.isLevelUp)
  assert(ms.d_mainUI.levelup_prize.prize_list[1].attach_type==1020)
  local box=ms.d_mainUI.levelUpBox;local levels={}
  ms.d_mainUI.levelUpBox=function(parent,level) levels[#levels+1]=level;return box(parent,level) end
  ms.d_mainUI.playerLevelUp(layer)
  assert(#levels==3 and levels[1]==4 and levels[3]==2)
  ms.d_mainUI.levelUpBox=box
 end)
 check('native_expired_entry',function()
  ms.d_data.g_new_config[24].buff_data.buff_type=0
  assert(not ui.checkHasLevelBuff() and not ui.checkHasLevelBuffFlag())
 end)
end,debug.traceback)
for i=#saved,1,-1 do
 local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end
 for k,v in pairs(row.old) do row.t[k]=v end
end
ms.MS_report_error=report
layer:removeAllChildrenWithCleanup(true);layer:release()
if not ok then return 'fixture:false:'..tostring(err) end
return table.concat(checks,'\n')
