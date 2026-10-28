-- Execute in original 3.87 VM. No network packets or persistent role mutations.
local ms=assert(package.loaded.ms)
local ui=assert(ms.d_cheerSquadUI)
local restores,checks={},{}
local function replace(t,k,v)
 local old=t[k]; restores[#restores+1]=function() t[k]=old end; t[k]=v
end
local function check(ok,name) assert(ok,name); checks[#checks+1]=name end
local ok,err=xpcall(function()
 local player={level=60}
 replace(ms.d_mainUI,'g_playerInfo',player)
 replace(ui,'g_Names',ms.d_c.table_copy(ui.g_Names))
 local state=ms.d_c.table_copy(ui.g_self)
 replace(ui,'g_self',state)
 replace(ui,'g_cheerSquadUI',{index=1,readOnly=false})
 replace(ui,'getPlayer',function() return player end)
 replace(ms.d_tianShuUI,'bit',ms.d_tianShuUI.bit)
 local confirmation,sent,tip,refreshed
 replace(ms.d_info,'show',function(s) tip=s end)
 replace(ms.d_quitUI,'createYesNoByStyle',function(_,_,fn) confirmation=fn end)
 replace(ms.d_u,'main_server_send_msg',function(mid,data) sent={mid=mid,data=data} end)
 replace(ui,'refreshCheerUI',function() refreshed=true end)
 replace(ms.d_data,'getItemCountByType',function() return 100 end)
 state.orientation=0; state.is_open_ni=2
 local names={'heaven','earth','shake','sunda','water','fire','hill','pool'}
 for _,n in ipairs(names) do player['cheer_'..n..'_level']=1 end
 check(ui.canShowChangeBtn()==true,'all positive slots at level one unlock reverse button')
 for _,n in ipairs(names) do
  player['cheer_'..n..'_level']=0
  check(ui.canShowChangeBtn()==false,'missing positive '..n..' hides reverse button')
  player['cheer_'..n..'_level']=1
 end
 state.is_open_ni=0
 check(ui.canShowChangeBtn()==false,'reverse switch zero hides button')
 state.is_open_ni=1
 check(ui.canShowChangeBtn()==true,'reverse switch one shows basic entry')
 state.is_open_ni=2
 ui.changeBaGuaUI()
 check(type(confirmation)=='function' and sent==nil,'first reverse entry asks before sending')
 check(state.orientation==0,'confirmation restores original orientation')
 confirmation()
 check(sent.mid==1087 and sent.data.flag==8 and sent.data.order==9 and sent.data.client_flag==9 and sent.data.id==0,'original confirmation sends flag8 order9')
 player.level=59; confirmation=nil; sent=nil
 ui.changeBaGuaUI()
 check(confirmation==nil and sent==nil and state.orientation==0 and tip~=nil,'level59 cannot enter current level60 config')
 player.level=60; player.cheer_unheaven_level=1
 ui.changeBaGuaUI()
 check(state.orientation==1 and refreshed and sent==nil,'already open reverse enters without payment')
 for i,n in ipairs(names) do
  check(ui.getPositionName(i)=='un'..n,'reverse direction '..i)
 end
 state.index=1
 ui.g_cheerSquadUI.index=1
 player.cheer_skill_open=131070; player.cheer_skill_ni_open=2
 local bits=ui.getSkillBit()
 check(bits[1]==1 and bits[2]==0,'reverse skill mask independent of positive mask: '..tostring(bits[1])..','..tostring(bits[2]))
 for index=1,8 do
  for slot=1,2 do
   player.cheer_skill_ni_open=2^(2*(index-1)+slot)
   local mask=ui.getSkillBit(index)
   check(mask[slot]==1 and mask[3-slot]==0,'original reverse mask '..index..'/'..slot)
  end
 end
 player.unheaven_skill_level=500
 check(ui.getSkillAdvanceLevel()==500,'original UI accepts reverse skill level500')
 ui.changeBaGuaUI()
 check(state.orientation==0,'switch back without payment')
end,debug.traceback)
for i=#restores,1,-1 do restores[i]() end
assert(ok,err)
return ms.d_json.encode({checks=checks,passed=#checks,original_functions=true,restored=true,network_sent=false})
