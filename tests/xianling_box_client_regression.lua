-- Run original widgets on a detached node; no live requests or inventory writes.
local ms=assert(package.loaded.ms)
local ui=assert(ms.d_xianlingShopUI)
local saved,sent,buttons={},{},{}
local root=CCNode:create();root:retain()
local function preserve(t)
 local old={};for k,v in pairs(t) do old[k]=v end
 saved[#saved+1]={t=t,old=old}
end
for _,t in ipairs({ui,ms.d_u,ms.d_data,ms.d_packageUI,ms.d_guildPartyUI}) do preserve(t) end
local amount,onAmount,limit,lastLabel=120,nil,nil,nil
local checks=0
local ok,err=xpcall(function()
 ui.g_self={cortege_list={5001,5004,5005}}
 ui.g_boxUI={}
 ms.d_packageUI.g_reorgItemsInfo={[5]={[11]={}}}
 ms.d_data.getItemCountByType=function(kind,tid) assert(kind==5 and tid==1249);return amount end
 ms.d_data.getPropsID=function(tid) assert(tid==1249);return 9001249 end
 ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
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
 ms.d_guildPartyUI.getCalc=function(fn,max,...) onAmount=fn;limit=max;return calc(fn,max,...) end
 local function open()
  root:removeAllChildrenWithCleanup(true);ui.g_boxUI={};buttons={}
  ms.d_packageUI.g_packageUI={parent=root}
  ms.d_packageUI.requestUseItem({type_id=1249,count=amount,id=9001249})
  assert(ui.g_boxUI.main_layer and #ui.g_boxUI.data_list==3)
 end
 for _,target in ipairs({5001,5004,5005}) do
  for _,n in ipairs({1,30,99}) do
   open();assert(limit==99)
   for i,row in ipairs(ui.g_boxUI.data_list) do
    if row.item.type_id==target then ui.g_boxUI.lastTouchIndex=i end
   end
   onAmount(n,0);assert(tonumber(lastLabel)==n,'preview must be 1:1')
   buttons['v2/kickUI/btn11.png']()
   local req=assert(sent[#sent]);assert(req.mid==1051)
   assert(req.data.item_type==1249 and req.data.item_id==9001249 and req.data.item_count==n)
   assert(req.data.des_type==5 and req.data.des_id==target)
   checks=checks+1
  end
 end
 amount=1;open();assert(limit==1);checks=checks+1
end,debug.traceback)
root:removeAllChildrenWithCleanup(true);root:release()
for i=#saved,1,-1 do
 local s=saved[i];for k in pairs(s.t) do s.t[k]=nil end
 for k,v in pairs(s.old) do s.t[k]=v end
end
return table.tostring({passed=ok,error=err or '',checks=checks,requests=sent,restored=true})
