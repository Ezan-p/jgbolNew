local ms=assert(package.loaded.ms);local ui=assert(ms.d_cardUI)
local saved,checks,sent,errors={},{},{},{}
local function preserve(t)
 local old={};for k,v in pairs(t) do old[k]=v end;saved[#saved+1]={t=t,old=old}
end
for _,t in ipairs({ui,ms.d_u,ms.d_info,ms.d_data,ms.d_time,ms.d_hz,ms.d_packageUI,ms.d_prizeUI,ms.d_quitUI,ms.d_activityUI}) do preserve(t) end
local liveSelf=ui.g_self;local liveCountdown=ui.count_down_func
local scheduler=CCDirector:sharedDirector():getScheduler();local liveTimer=liveSelf.CountDownHandler
if liveTimer and liveTimer~=0 then scheduler:unscheduleScriptEntry(liveTimer) end
local report=ms.MS_report_error;ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
if ui._localTangwangRestore then ui._localTangwangRestore() end
ui.g_self=ms.d_c.table_copy(ui.g_self);ui.g_self.CountDownHandler=nil;ui.g_cardUI={}
local kind=ms.d_common_def.item_main_type.invisible_card
ms.d_packageUI.g_reorgItemsInfo={[5]={[kind]=ms.d_c.table_copy(FIXTURE.cards)}}
local now=FIXTURE.now;local prize,confirm
ms.d_time.getTime=function() return now end
ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
ms.d_info.show=function() end
local nativePrize=ms.d_prizeUI.setPrize
ms.d_prizeUI.setPrize=function(p) prize=p.prize_list;return nativePrize(p) end;ms.d_prizeUI.show=function() end
ms.d_quitUI.createYesNoByStyle=function(parent,style,yes) confirm=yes end
-- INSTALL_PATCH
local parent=CCScene:create();parent:retain()
local menus={};local menu=ms.d_u.createMenu
ms.d_u.createMenu=function(styles,...) menus[#menus+1]=styles;return menu(styles,...) end
local function cleanup()
 if ui.g_self.CountDownHandler then scheduler:unscheduleScriptEntry(ui.g_self.CountDownHandler);ui.g_self.CountDownHandler=nil end
 if ui._localTangwangRestore then ui._localTangwangRestore() end
 parent:removeFromParentAndCleanup(true);parent:removeAllChildrenWithCleanup(true);parent:release()
 for i=#saved,1,-1 do local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end;for k,v in pairs(row.old) do row.t[k]=v end end
 ms.MS_report_error=report
 if liveTimer and liveTimer~=0 then liveSelf.CountDownHandler=scheduler:scheduleScriptFunc(liveCountdown,1,false) end
end
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,ok=ok and #errors==0,error=(err or '')..table.concat(errors,'\n')}
end
local function update(v) ui.updateActivityStatus(ms.d_c.table_copy(v)) end
local function choose(levels)
 ui.resetCards()
 for i,lv in ipairs(levels) do
  local sprite=ui.getCardSprite(lv,1);ui.g_cardUI.main_layer:addChild(sprite)
  ui.g_cardUI.UsedCards[i]={level=lv,sprite=sprite}
 end
end
check('native entry query and scene',function()
 update(FIXTURE.status);assert(ui.canJoin());ui.show(parent)
 assert(ui.g_cardUI.main_layer and sent[#sent].mid==1205)
end)
check('automatic combination controls removed',function()
 local exchange=false
 for _,styles in ipairs(menus) do for _,row in ipairs(styles) do
  assert(not (row.npic and row.npic:find('v2/CardUI/scheme',1,true)))
  if row.npic=='v2/CardUI/exchange1.png' then assert(row.x==0.5);exchange=true end
 end end
 assert(exchange)
end)
check('native weekly countdown',function()
 ui.count_down_func()
 assert(tolua.cast(ui.g_cardUI.main_layer:getChildByTag(ui.g_self.timeLabelTag),'CCLabelTTF'):getString()=='1天12小时0分0秒')
end)
check('heartbeat card status does not rebuild activity menu',function()
 local v=ms.d_c.table_copy(FIXTURE.status);v.local_tangwang_only=true
 local layer=ui.g_cardUI.main_layer;ms.d_activityUI.getQiwenStatus(v)
 assert(ui.g_cardUI.main_layer==layer and layer:getParent()==parent)
end)
check('eight native letter sprites',function()
 for i,v in ipairs({'国','庆','快','乐','有','礼','欢','度'}) do assert(ms.d_data.g_letters[i]==v);assert(ui.getCardSprite(i,1)) end
end)
check('locked cards excluded without changing package',function()
 ui.resetCards();local counts=ui.g_cardUI.countList or ui.g_self.countList;assert(counts[1].count==4)
 assert(#ms.d_packageUI.g_reorgItemsInfo[5][kind]==29)
end)
if TANGWANG_PREVIEW then
 CCDirector:sharedDirector():getRunningScene():addChild(parent,9999)
 tangwangPreview={intro=function() ui.showTips() end,restore=cleanup}
 return 'preview ready'
end
for index,levels in ipairs({{1,2,3,4},{1,2,5,6},{7,8,1,2}}) do
 check('native manual combination '..index,function()
  choose(levels);assert(ui.checkCompose());ui.exchangePressed()
  local req=sent[#sent];assert(req.mid==1213 and req.data.count==4 and #req.data.card_list==4)
  local unique={};for _,c in ipairs(req.data.card_list) do assert(not unique[c.id]);unique[c.id]=true end
 end)
end
check('unmatched asks confirmation and uses four distinct ids',function()
 choose({1,1,1,1});assert(not ui.checkCompose());local n=#sent
 ui.exchangePressed();assert(#sent==n and type(confirm)=='function');confirm()
 assert(sent[#sent].mid==1213);local ids={};for _,c in ipairs(sent[#sent].data.card_list) do assert(not ids[c.id]);ids[c.id]=true end
end)
check('incomplete selection sends no request',function()
 choose({1,2,3});local n=#sent;ui.exchangePressed();ui.sendExchangeRequest();assert(#sent==n)
end)
check('native reward callback',function()
 ui.onGetExchangeResponse(ms.d_c.table_copy(FIXTURE.reward));assert(prize and #prize==1)
 assert(prize[1].attach_type==6005 and prize[1].attach_count==3, (function() local v={} for k,x in pairs(prize[1]) do v[#v+1]=tostring(k)..'='..tostring(x) end return table.concat(v,',') end)())
end)
check('native introduction special reward copy and no automatic actions',function()
 local n=#sent;ui.showTips();local layer=ui.g_cardUI.main_layer:getChildByTag(91094);assert(layer)
 local labels={};local function walk(node)
  if tolua.type(node)=='CCLabelTTF' then labels[#labels+1]=node:getString() end
  local children=node:getChildren();if children then for i=0,children:count()-1 do walk(tolua.cast(children:objectAtIndex(i),'CCNode')) end end
 end
 walk(layer);local text=table.concat(labels,'\n')
 for _,name in ipairs({'国庆快乐','国庆有礼','欢度国庆'}) do assert(text:find(name..'：可兑换特殊奖励',1,true)) end
 assert(text:find('放入四枚金牌',1,true))
 assert(not text:find('五法界魂箱',1,true) and not text:find('破障丹',1,true) and not text:find('元宝',1,true))
 assert(not text:find('自动组合',1,true));assert(#sent==n)
 ui.g_cardUI.main_layer:removeChildByTag(91094,true)
end)
check('weekly boundary blocks both direct and pending confirm',function()
 choose({1,2,3,4});now=FIXTURE.status.tangwang_info.next_weekly_refresh;local n=#sent
 ui.exchangePressed();ui.sendExchangeRequest();ui.count_down_func();assert(#sent==n+1 and sent[#sent].mid==1205)
 assert(ui.canJoin() and ui.g_cardUI.main_layer)
 ms.d_packageUI.g_reorgItemsInfo[5][kind]=ms.d_c.table_copy(FIXTURE.new_cards)
 update(FIXTURE.next_week);assert(#ui.g_cardUI.UsedCards==0)
 local n=#sent;confirm();assert(#sent==n)
 assert(tolua.cast(ui.g_cardUI.main_layer:getChildByTag(ui.g_self.timeLabelTag),'CCLabelTTF'):getString()=='7天0小时0分0秒')
end)
check('disabled entry',function()
 local v=ms.d_c.table_copy(FIXTURE.next_week);v.tangwang_info.local_enabled=false;update(v);assert(not ui.canJoin())
end)
cleanup()
local out={};for _,v in ipairs(checks) do out[#out+1]=v.name..':'..tostring(v.ok)..':'..v.error end
return table.concat(out,'\n')
