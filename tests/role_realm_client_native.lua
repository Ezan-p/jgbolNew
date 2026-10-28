-- Original Cocos widgets, isolated parent/player/config, no outgoing requests.
local ms=package.loaded.ms
local ui=ms.d_roleRebornUI
local saved={};for k,v in pairs(ui) do saved[k]=v end
local player,main=ms.d_mainUI.g_playerInfo,ms.d_mainUI.g_mainUI
local send,count,notice=ms.d_u.main_server_send_msg,ms.d_data.getItemCountByType,ms.d_info.show
local checks,requests,notices={},{},{}
local stock=100000
local function clone(t) local r={};for k,v in pairs(t) do r[k]=v end;return r end
local function check(name,fn)
 local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,ok=ok,error=ok and '' or tostring(err)}
end
local function render(layer,level,n)
 if ui.g_role_reborn_layer then ui.closeRoleRebornUI() end
 ms.d_mainUI.g_playerInfo=clone(player)
 ms.d_mainUI.g_playerInfo.reborn_layer=layer
 ms.d_mainUI.g_playerInfo.level=level or 99
 ms.d_mainUI.g_playerInfo.maxlayer_reborn_count=n or 3
 ui.MenuPopRebornLayer()
end
local ok,err=xpcall(function()
 -- Constructor assigns fresh child tables; keep all live module tables intact.
 for k,v in pairs(ui) do if type(v)=='table' and k:sub(1,2)=='g_' then ui[k]=clone(v) end end
 ui.g_role_reborn_layer=nil
 ms.d_mainUI.g_mainUI=clone(main)
 ms.d_mainUI.g_mainUI.main_layer=CCLayer:create()
 ms.d_u.main_server_send_msg=function(mid,data) requests[#requests+1]={mid=mid,data=data} end
 ms.d_data.getItemCountByType=function() return stock end
 ms.d_info.show=function(s) notices[#notices+1]=s end
 ui.initData(REALM_CONFIG)
 assert(loadstring(ADAPTER_SOURCE))()
 for layer=0,4 do
  check('render_realm_'..layer,function()
   render(layer)
   for i=1,3 do
    assert(ui.g_info_label[i][3]:getString()=='开放区域:'..i..'-'..i,ui.g_info_label[i][3]:getString())
   end
   assert(ui.next_reborn_level==math.min(layer+1,4))
   assert(ui.g_reborn_condition_next==REALM_CONFIG[math.min(layer+1,4)])
   assert(ui.g_can_reborn==(layer<4))
  end)
 end
 for target=1,4 do
  check('level_boundary_'..target,function()
   render(target-1,REALM_CONFIG[target].condiction.need_role_level-1)
   assert(not ui.g_can_reborn)
   local before=#requests;ui.reborn_update_func();assert(#requests==before)
  end)
  check('material_boundary_'..target,function()
   stock=REALM_CONFIG[target].condiction.consume_list[1].attach_count-1
   render(target-1);assert(not ui.g_can_reborn)
   local before=#requests;ui.reborn_update_func();assert(#requests==before)
   stock=stock+1;ui.update_rightpanel_info(target-1);assert(ui.g_can_reborn)
   ui.reborn_update_func();assert(#requests==before+1)
   local req=requests[#requests].data
   assert(req.id==4 and req.reborn_type==1 and req.data=='')
   stock=100000
  end)
  if target>1 then
   check('companion_boundary_'..target,function()
    render(target-1,99,2);assert(not ui.g_can_reborn)
    local before=#requests;ui.reborn_update_func();assert(#requests==before)
   end)
  end
 end
 check('full_realm_no_request',function()
  render(4);local n=#requests;local m=#notices
  ui.reborn_update_func();ui.sendRebornRequest()
  assert(#requests==n and #notices==m+2 and not ui.g_can_reborn)
 end)
 check('idempotent_install_and_restore',function()
  local refresh=ui.update_rightpanel_info
  assert(loadstring(ADAPTER_SOURCE))();assert(refresh==ui.update_rightpanel_info)
  ui._localRealmRestore();assert(ui._localRealmRestore==nil)
 end)
end,debug.traceback)
if ui.g_role_reborn_layer then ui.closeRoleRebornUI() end
local keys={};for k in pairs(ui) do keys[#keys+1]=k end
for _,k in ipairs(keys) do ui[k]=nil end
for k,v in pairs(saved) do ui[k]=v end
ms.d_mainUI.g_playerInfo,ms.d_mainUI.g_mainUI=player,main
ms.d_u.main_server_send_msg,ms.d_data.getItemCountByType,ms.d_info.show=send,count,notice
if not ok then error(err) end
return ms.d_json.encode({checks=checks,restored=true,requests_captured=#requests})
