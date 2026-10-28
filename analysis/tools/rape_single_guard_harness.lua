-- Detached native Cocos nodes; all requests are captured and live UI restored.
local ms=assert(package.loaded.ms)
local ui=assert(ms.d_crossDoomUI)
local saved={}
for _,t in ipairs({ui,ms.d_u,ms.d_mainUI}) do
 local old={};for k,v in pairs(t) do old[k]=v end
 saved[#saved+1]={t=t,old=old}
end
local errors,checks={},{}
local report=ms.MS_report_error
ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
local parent=CCScene:create();parent:retain()
local function check(name,fn)
 local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,passed=ok,error=err or ''}
end
local ok,err=xpcall(function()
 if ui._localRapeRestore then ui._localRapeRestore() end
 local nativeHead=ui.createCardHead
 local shown,sent,delays
 ui.showLittleWin=function(tag) shown=tag end
 ui.send_fight_req=function(id,column,typ) sent={id=id,column=column,type=typ} end
 ms.d_mainUI.g_playerInfo={energy=10}
 ms.d_u.main_server_send_msg=function() error('unexpected network request') end
 ms.d_u.delay=function(layer,time,fn) delays[#delays+1]=time;fn() end
 local function reset()
  parent:removeAllChildrenWithCleanup(true)
  ui.g_self={cardPage_layer=parent,cardPage_enmey_map={},card_h=0.1,h3=0.2,h5=0.5}
  shown=nil;sent=nil;delays={}
 end
 local function heads(n,won)
  local rows={}
  for i=1,n do rows[i]={id=950000+i,type=2,v={show_type=1001,cortege_layer=0,has_win=won,rand=7-i}} end
  return rows
 end
 check('original single guard omission reproduced',function()
  reset();nativeHead(1,heads(1,false),nil,true)
  assert(next(ui.g_self.cardPage_enmey_map)==nil and parent:getChildrenCount()==0)
 end)
 -- INSTALL_PATCH
 local wrapped=ui.createCardHead
 -- INSTALL_PATCH
 check('idempotent installation',function() assert(ui.createCardHead==wrapped) end)
 for column=1,3 do
  for n=1,6 do
   for _,fast in ipairs({false,true}) do
    check('native heads '..column..'/'..n..' fast='..tostring(fast),function()
     reset();local rows=heads(n,false);local callbacks=0
     ui.createCardHead(column,rows,function() callbacks=callbacks+1 end,fast)
     assert(parent:getChildrenCount()==2*n and callbacks==1)
     for i=1,n do
      local tag=column*100+i;local entry=assert(ui.g_self.cardPage_enmey_map[tag])
      assert(entry==rows[i] and entry.head_sprite:isVisible())
      assert(entry.menu:getParent()==parent and entry.head_sprite:getParent()==parent)
      assert(entry.x>0 and entry.x<ms.d_u.getW() and entry.y>0 and entry.y<ms.d_u.getH())
      tolua.cast(entry.menu:getChildByTag(tag),'CCMenuItem'):activate()
      assert(shown==tag,'native head click must open the opponent')
      ui.doFightNpc(tag)
      assert(sent.id==entry.id and sent.column==column and sent.type==entry.type)
     end
     if n==1 then
      assert(math.abs(delays[1]-(fast and 0.001 or 0.1))<0.000001)
      assert(math.abs(delays[2]-(fast and 0.003 or 0.3))<0.000001)
     end
    end)
   end
  end
 end
 check('defeated single guard remains visible and dimmed',function()
  reset();ui.createCardHead(2,heads(1,true),nil,true)
  local entry=assert(ui.g_self.cardPage_enmey_map[201])
  local color=entry.head_sprite:getColor()
  assert(color.r==32 and color.g==64 and color.b==64)
 end)
 check('single guard redraw binds replacement identity',function()
  reset();local rows=heads(1,false);rows[1].id=960000
  ui.createCardHead(3,rows,nil,true);ui.doFightNpc(301)
  assert(sent.id==960000 and sent.column==3)
 end)
 check('restore original head renderer',function()
  ui._localRapeRestore();assert(ui.createCardHead==nativeHead)
 end)
end,debug.traceback)
parent:removeAllChildrenWithCleanup(true);parent:release()
for i=#saved,1,-1 do
 local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end
 for k,v in pairs(row.old) do row.t[k]=v end
end
ms.MS_report_error=report
assert(ok,err);assert(#errors==0,table.concat(errors,'\n'))
return table.tostring(checks)
