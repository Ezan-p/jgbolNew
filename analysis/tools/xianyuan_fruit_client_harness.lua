-- Exercise original Cocos widgets in a detached layer; capture every send.
local ms=assert(package.loaded.ms);local ui=assert(ms.d_kickUI)
local saved,checks,sent,errors,buttons={},{},{},{},{}
local root=CCNode:create();root:retain()
local function preserve(t)
 local old={};for k,v in pairs(t) do old[k]=v end
 saved[#saved+1]={t=t,old=old}
end
for _,t in ipairs({ui,ms.d_data,ms.d_u,ms.d_packageUI,ms.d_lineupUI,ms.d_guildPartyUI,
                  ms.d_commonLayerUI,ms.d_info}) do preserve(t) end
local report=ms.MS_report_error
local amount,onAmount,limit,lastLabel=20,nil,nil,nil
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,passed=ok and #errors==0,error=(err or '')..table.concat(errors,'\n')}
end
local ok,err=xpcall(function()
 ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
 ui.g_self={};ui.g_fruitUI={}
 ms.d_lineupUI.g_characterInfo={{type=5004,type_id=5004,id=80001,level=1,evolve_level=0,reborn_layer=0}}
 ms.d_packageUI.g_reorgItemsInfo={[5]={[11]={}}}
 ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
 ms.d_data.getItemCountByType=function(kind,tid) assert(kind==5 and tid==1246);return amount end
 ms.d_data.getPropsID=function(tid) assert(tid==1246);return 9001246 end
 ms.d_packageUI.updateItemCellInfo=function() end
 ms.d_packageUI.refreshPackage=function() end
 local menu=ms.d_u.createMenu
 ms.d_u.createMenu=function(styles,...)
  for _,s in ipairs(styles) do if s.npic and s.call_back then buttons[s.npic]=s.call_back end end
  return menu(styles,...)
 end
 local style=ms.d_u.createByStyle
 ms.d_u.createByStyle=function(s,...)
  if s.type=='label' then lastLabel=s.string end
  return style(s,...)
 end
 local calc=ms.d_guildPartyUI.getCalc
 ms.d_guildPartyUI.getCalc=function(fn,max,...)
  onAmount=fn;limit=max;return calc(fn,max,...)
 end
 local function open()
  root:removeAllChildrenWithCleanup(true);ui.g_fruitUI={};buttons={}
  ui.showFruitUseLayer(root,30)
  assert(ui.g_fruitUI.main_layer and onAmount)
 end
 local function select(kind,tid)
  for i,r in ipairs(ui.g_fruitUI.data_list) do
   if (kind==5 and r.isItem and r.item.type_id==tid) or
      (kind==10 and not r.isItem and (r.char.type or r.char.type_id)==tid) then
     ui.g_fruitUI.lastTouchIndex=i;return
   end
  end
  error('target absent '..kind..'/'..tid)
 end
 check('original server catalog loader and ownership filter',function()
  ui.onGetCortList(FIXTURE.catalog)
  assert(#ui.g_self.cortege_list==51)
  assert(#ui.getFruitCorts()==48)
  for _,r in ipairs(ui.getFruitCorts()) do
   if not r.isItem then
    local tid=r.char.type or r.char.type_id
    assert(tid~=5027 and tid~=5046 and tid~=5053)
   end
  end
 end)
 check('special gods become selectable only when currently owned',function()
  for _,t in ipairs({5027,5046,5053}) do table.insert(ms.d_lineupUI.g_characterInfo,{type=t,type_id=t,id=t,evolve_level=0}) end
  assert(#ui.getFruitCorts()==51)
  ms.d_lineupUI.g_characterInfo={{type=5004,type_id=5004,id=80001,level=1,evolve_level=0,reborn_layer=0}}
 end)
 check('native selector and batch cap',function() open();assert(limit==15 and #ui.g_fruitUI.data_list==48) end)
 check('original backpack use opens fruit chooser',function()
  root:removeAllChildrenWithCleanup(true);ui.g_fruitUI={}
  ms.d_packageUI.g_packageUI={parent=root}
  ms.d_packageUI.requestUseItem({type_id=1246,count=20,id=9001246})
  assert(ui.g_fruitUI.main_layer and #ui.g_fruitUI.data_list==48)
 end)
 check('no selection sends no request',function()
  local n=#sent;buttons['v2/kickUI/btn11.png']();assert(#sent==n)
 end)
 for _,row in ipairs(FIXTURE.cases) do
  check('native preview and 1051 request '..row.kind..'/'..row.target..'/'..row.count,function()
   open();select(row.kind,row.target);onAmount(row.count,0)
   assert(tonumber(lastLabel)==row.gain,'preview gain '..tostring(lastLabel))
   buttons['v2/kickUI/btn11.png']()
   local req=assert(sent[#sent]);assert(req.mid==1051)
   assert(req.data.item_type==1246 and req.data.item_id==9001246 and req.data.item_count==row.count)
   assert(req.data.des_type==row.kind and req.data.des_id==row.target)
  end)
 end
 check('insufficient inventory sends no request',function()
  open();select(10,5004);onAmount(15,0);amount=1
  local n=#sent;buttons['v2/kickUI/btn11.png']();assert(#sent==n);amount=20
 end)
 check('small inventory limits native selector',function() amount=3;open();assert(limit==3);amount=20 end)
 check('original use result closes chooser and displays actual backend prize',function()
  open();local captured
  ms.d_u.delay=function(node,time,fn) fn() end
  ms.d_commonLayerUI.showQianKunResLayer=function(parent,list,flag) captured=list end
  ms.d_commonLayerUI.recvUsedItem(FIXTURE.result)
  assert(not ui.g_fruitUI.main_layer and captured and captured[1].attach_count==30)
  assert(captured[1].object_type==10 and captured[1].attach_type==5004)
 end)
end,debug.traceback)
if not ok then checks[#checks+1]={name='fixture setup',passed=false,error=err} end
root:removeAllChildrenWithCleanup(true);root:release()
for i=#saved,1,-1 do
 local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end
 for k,v in pairs(row.old) do row.t[k]=v end
end
ms.MS_report_error=report
return table.tostring({checks=checks,restored=true,network_sends_captured=true,
 live_account_resources_changed=false,native_cocos=true,detached_layer=true})
