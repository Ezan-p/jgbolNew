local ms=package.loaded.ms
local v,u=ms.d_actNoticeUI,ms.d_u
local create,menu,send,show=u.createByStyle,u.createMenu,u.main_server_send_msg,ms.d_info.show
local oldButton=v.g_get_fund_btn
local texts,button,callback,requests,notices={},nil,nil,{},{}
local scene=CCDirector:sharedDirector():getRunningScene()
local checks=0
local function check(value) assert(value,'check '..(checks+1));checks=checks+1 end
local function render(level,taken,visible)
 texts={};button=nil;callback=nil
 local layer=visible and CCLayerColor:create(ccc4(40,25,15,255)) or CCLayer:create()
 if visible then scene:addChild(layer,9999,19877) end
 local ps={};for i,n in ipairs({100,300,600,1000,1500}) do ps[i]={min_level=i*10,attach_list={{attach_count=n}}} end
 v.createUpgradeRole({end_time=0,permanent=true,role_info={level=level},prize_list=ps,had_taken_gift=taken},layer)
 return layer
end
local ok,err=xpcall(function()
 u.createByStyle=function(s,...)
  if s.string then texts[s.string]=true end
  return create(s,...)
 end
 u.createMenu=function(styles,items,...)
  for _,s in ipairs(styles) do if s.npic=='v2/actNoticeUI/get1.png' then callback=s.call_back end end
  local node=menu(styles,items,...);button=items and items[1];return node
 end
 u.main_server_send_msg=function(mid,request) requests[#requests+1]={mid=mid,data=request} end
 ms.d_info.show=function(message) notices[#notices+1]=message end
 render(9,false);check(not button:isEnabled());callback();check(#requests==0)
 render(10,false);check(button:isEnabled() and texts['活动剩余时间：永久'])
 callback();check(#notices==1 and #requests==0)
 callback();check(#requests==1 and requests[1].mid==ms.d_msg_def.gscl_msg_id.msg_common_activity and requests[1].data.act_type==7 and requests[1].data.flag==2 and requests[1].data.index==0)
 render(99,true);check(not button:isEnabled() and texts['已领取 · 永久不可重复'])
 render(99,false,true);check(button:isEnabled() and texts['当前可领取 1500 元宝'])
 callback();check(#requests==2)
end,debug.traceback)
u.createByStyle,u.createMenu,u.main_server_send_msg,ms.d_info.show=create,menu,send,show
v.g_get_fund_btn=oldButton
if not ok then error(err) end
return 'passed:'..checks
