local ms=assert(package.loaded.ms)
local saved={};local out={};local errors={};local sent={};local menus={}
local function preserve(t)
 local old={};for k,v in pairs(t) do old[k]=v end;saved[#saved+1]={t=t,old=old}
end
local oldRestore=ms._localFateRestore
for _,name in ipairs({'d_mainUI','d_loginUI','d_lineupUI','d_packageUI','d_ascensionUI','d_fateRebuildUI','d_soulUI','d_soulSevenUI','d_u','d_info','d_data','d_roleRebornUI','d_prizeUI'}) do preserve(assert(ms[name],name)) end
if oldRestore then oldRestore() end
local report=ms.MS_report_error
local root=CCLayer:create();root:retain()
ms.d_mainUI.g_mainUI={main_layer=root};ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(ms.d_mainUI.g_playerInfo)
for _,k in ipairs({'level','reborn_layer','silver_coin','gold_coin'}) do ms.d_mainUI.g_playerInfo[k]=FIXTURE.role[k] end
ms.d_lineupUI.g_characterInfo={};ms.d_packageUI.g_packageItemsInfo={}
ms.d_fateRebuildUI.g_fateRebuildData=nil
ms.d_loginUI.g_currentSence=ms.d_loginUI.senceID.mainUI
ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
ms.d_info.show=function() end
ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
local nativeMenu=ms.d_u.createMenu
ms.d_u.createMenu=function(items,...)
 for _,item in ipairs(items) do if item.npic then menus[item.npic]=item.call_back end end
 return nativeMenu(items,...)
end
-- INSTALL_PATCH
local function check(name,fn)
 errors={};local ok,err=xpcall(fn,debug.traceback)
 out[#out+1]=(ok and #errors==0 and 'PASS ' or 'FAIL ')..name..':'..(err or '')..table.concat(errors,'\n')
end
local function apply(rows)
 for _,p in ipairs(rows) do
  if p.mid==1034 then ms.d_lineupUI.getDateFormServer(p.data)
  elseif p.mid==1035 then ms.d_packageUI.getDateFormServer(p.data)
  elseif p.mid==1032 and p.data.unit_type~=1 then ms.d_event_mgr.msg_modify_attr_1032(nil,p.data,nil)
  elseif p.mid==2998 and p.data.id==226 then ms.d_soulUI.callbackRapeSweepResultReturn(assert(loadstring('return '..p.data.data))())
  elseif p.mid==2998 and p.data.id==80 then ms.d_data.callback_update_config(assert(loadstring('return '..p.data.data))())
  end
 end
end
check('snapshot and material metadata',function()
 ms.d_data.callback_update_config({local_fate_rebuild=FIXTURE.state});apply(FIXTURE.inventory)
 assert(ms.d_lineupUI.g_characterInfo[1].fate_rebullding_state==0)
 assert(ms.d_data.getCertainInfo(5,1371).name=='天命石')
end)
check('soul box batch-use request',function()
 local native=ms.d_data.createBatchUse
 ms.d_data.createBatchUse=function(parent,range,fn) assert(range.max==99);fn(5) end
 local item;for _,i in ipairs(ms.d_packageUI.g_packageItemsInfo) do if i.type_id==1370 then item=i end end
 ms.d_packageUI.requestUseItem(assert(item));ms.d_data.createBatchUse=native
 assert(sent[#sent].mid==1051 and sent[#sent].data.item_count==5 and sent[#sent].data.item_type==1370)
end)
check('nine turn activation button',function()
 ms.d_ascensionUI.show(root)
 assert(menus['v2/fateRebuild/jh1.png'],'activation menu missing')
 menus['v2/fateRebuild/jh1.png']()
 assert(sent[#sent].mid==1357 and sent[#sent].data.id==3,'activation request missing')
end)
check('activation response refresh',function()
 apply(FIXTURE.activation);assert(ms.d_lineupUI.g_characterInfo[1].fate_rebullding_state==1)
end)
check('fate main window',function()
 ms.d_fateRebuildUI.g_record_cort_id=FIXTURE.cid;ms.d_fateRebuildUI.show(root)
 assert(ms.d_fateRebuildUI.g_fateRebuildData.id==FIXTURE.cid)
end)
for p=1,3 do check('soul window '..p,function() ms.d_soulUI.show(root,p) end) end
for p=1,7 do check('seven soul window '..p,function() ms.d_soulSevenUI.show(root,p) end) end
check('heaven node request and response',function()
 ms.d_soulUI.show(root,1);ms.d_soulUI.pressPointGD()
 assert(sent[#sent].mid==1357 and sent[#sent].data.id==0,'node request missing')
 apply(FIXTURE.node)
 assert(ms.d_lineupUI.g_characterInfo[1].spirit_heaven_stars==1)
end)
check('soul reset response and rewards',function()
 ms.d_soulUI.g_soulUI_flag_return=1
 local shown=false;ms.d_prizeUI.show=function() shown=true end
 apply(FIXTURE.reset)
 assert(ms.d_lineupUI.g_characterInfo[1].spirit_heaven_stars==0)
 assert(shown,'missing native refund display')
end)
for _,cap in ipairs({{8,'physic_zs_level',30},{10,'physic_yp_level',10}}) do
 check('seven soul configured cap '..cap[1],function()
  local state=FIXTURE.expected;state[FIXTURE.cid][cap[2]]=cap[3]
  ms.d_data.callback_update_config({local_fate_rebuild=state})
  ms.d_soulSevenUI.show(root,cap[1]-3)
 end)
end
check('chunked state merge and account clearing',function()
 ms.d_data.callback_update_config({local_fate_rebuild=FIXTURE.expected,local_fate_append=false})
 ms.d_data.callback_update_config({local_fate_rebuild={[987654]={fate_rebullding_state=1}},local_fate_append=true})
 assert(ms.d_lineupUI.g_characterInfo[1].fate_rebullding_state==1)
 ms.d_data.callback_update_config({local_fate_rebuild={},local_fate_append=false})
 assert(ms.d_lineupUI.g_characterInfo[1].fate_rebullding_state==0)
end)
check('roster refresh preserves fractional values',function()
 local state=FIXTURE.expected;state[FIXTURE.cid].fate_rebuilding_achive_rate=0.5
 ms.d_data.callback_update_config({local_fate_rebuild=state});apply(FIXTURE.inventory)
 assert(ms.d_lineupUI.g_characterInfo[1].fate_rebuilding_achive_rate==0.5)
end)
if ms._localFateRestore then ms._localFateRestore() end
root:removeAllChildrenWithCleanup(true);root:release()
for i=#saved,1,-1 do local row=saved[i];for k in pairs(row.t) do row.t[k]=nil end;for k,v in pairs(row.old) do row.t[k]=v end end
ms.MS_report_error=report;ms._localFateRestore=oldRestore
out[#out+1]='restored'
return table.concat(out,'\n')
