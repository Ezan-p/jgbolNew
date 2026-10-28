"""Generate isolated 3.87 native UI callbacks for Taixu; captures all sends."""
import copy
import sys
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import activity, activity_undergo as u, activity_arena as arena, summon
from network_redirect.backend import Backend
NOW=1792814400
with tempfile.TemporaryDirectory() as tmp:
    b=Backend(Path(tmp),18770,lambda *a,**k:None)
    role=b.profile();role['level']=60;activity.prepare(role,NOW,b.activity_rules)
    s=u.state(role,NOW,b.activity_rules);maps={'initial':u.detail(s)}
    s.update(gate=201,challenge=105,passed=list(range(101,110)),started=NOW,top_big_id=1)
    maps['progress']=u.detail(s)
    s.update(gate=1001,challenge=1001,challenge_passed=sorted(u.GATES),top_big_id=10)
    maps['complete']=u.detail(s)
    prizes=dict(day_prize=u.day_prize(s),attach_list=[dict(object_type=5,attach_type=1366,attach_count=360,attach_level=1)])
    shop=u.shop(s,b.activity_rules)
    shop_catalog=[dict(activity.prize_spec(p['reward']), crystals=p['cost'], buy_times=p['limit'],
                       shop_token='catalog-fixture') for p in b.activity_rules['undergo_shop']]
    ar=arena.state(role,NOW,b.activity_rules);fixtures={'entry':arena.entry(role,ar,NOW)}
    for stage in range(1,7):
        ar.update(stage=stage,settled=stage==6,stage_fights=1)
        fixtures[str(stage)]=arena.board(role,ar)
        fixtures['entry_'+str(stage)]=arena.entry(role,ar,NOW)
    fixtures['update']=arena.board(role,ar,5)
    fixtures['update']['event_info']['reward_score']=100
    fixtures['rank']=arena.board(role,ar,3)
    ar['settled']=False
    fixtures['settlement']=arena.board(role,ar)
    fixtures['settlement']['local_prizes']=arena.settle_prizes(role,ar)
    fixtures['settlement'].update(arena.board(role,ar))
    b.close()
script=r'''
local ms=assert(package.loaded.ms);local ui=assert(ms.d_arenaUI);local map=assert(ms.d_undergoMapUI)
local installedBefore=ui._localTaixuRestore
local saved={}
local function preserve(t)
 local copy={};for k,v in pairs(t) do copy[k]=v end
 saved[#saved+1]={target=t,old=copy}
end
for _,name in ipairs({'d_arenaUI','d_undergoMapUI','d_undergoSubLevelUI','d_undergoLineupUI','d_undergoOrdealUI','d_loginUI','d_mainUI','d_commonLayerUI','d_newbieManualUI','d_info','d_hz'}) do preserve(ms[name]) end
-- Exercise the current source even if an older patch is already injected.
if installedBefore then installedBefore() end
for _,fn in ipairs({ms.d_undergoOrdealUI.getMainLayer,ms.d_undergoLineupUI.getCurrentPosCharList}) do
 for i=1,20 do local name,value=debug.getupvalue(fn,i);if not name then break end
  if name=='g_self' and type(value)=='table' then preserve(value) end
 end
end
local oldSend=ms.d_u.main_server_send_msg;local oldRun=ms.d_u.runScene;local oldReport=ms.MS_report_error
local errors='';local results={};local sent={};local scenes={}
local function clone(t)
 local out={};for k,v in pairs(t) do out[k]=type(v)=='table' and clone(v) or v end;return out
end
ms.d_mainUI.g_playerInfo=clone(ms.d_mainUI.g_playerInfo)
ms.d_mainUI.g_playerInfo.level=60;ms.d_mainUI.g_playerInfo.role_id=1
ms.d_u.main_server_send_msg=function(mid,d) sent[#sent+1]={mid=mid,data=d} end
ms.MS_report_error=function(e) errors=errors..'\n'..tostring(e) end
ms.d_u.runScene=function(scene) scene:retain();scenes[#scenes+1]=scene end
ms.d_info.show=function() end
local root=CCLayer:create();CCDirector:sharedDirector():getRunningScene():addChild(root,9999)
local function check(name,fn)
 errors='';local ok,err=xpcall(fn,debug.traceback)
 results[#results+1]={name=name,ok=ok and errors=='',error=(err or '')..errors}
end
ui.g_arenaUI={parent_layer=root};ui.g_data={};ui.g_self=clone(ui.g_self)
map.g_mapUI=clone(map.g_mapUI);map.g_mapUI.maps={};map.g_mapUI.main_layer=nil;map.g_mapUI.main_scene=nil
map.g_mapUI.lastFightMapID=0;map.g_mapUI.lastFightMapID_elite=0
'''
script+='\n'+(ROOT/'network_redirect/taixu_client.lua').read_text()+'\n'
script+='local fixtureTime='+str(NOW)+'\nlocal fixtures='+summon.lua(fixtures)+'\nlocal maps='+summon.lua(maps)+'\nlocal shop='+summon.lua(shop)+'\nlocal prizes='+summon.lua(prizes)+'\n'
script+='local shopCatalog='+summon.lua(shop_catalog)+'\n'
script+=r'''
local now=ms.d_time.getTime()
for name,data in pairs(fixtures) do
 if string.sub(name,1,5)=='entry' then
  for _,p in pairs(data.schedule_list.match_time_list) do p.start_time=p.start_time+now-fixtureTime;p.end_time=p.end_time+now-fixtureTime end
  for _,list in pairs(data.schedule_list.grade_time_list) do
   for _,p in ipairs(list) do p.start_time=p.start_time+now-fixtureTime;p.end_time=p.end_time+now-fixtureTime end
  end
 end
end
check('taixu_entry',function() ms.d_undergoOrdealUI.enter() end)
check('level50_entry_request',function()
 ms.d_mainUI.g_playerInfo.level=50;ms.d_undergoOrdealUI.pressEnterUndergoLayer()
 assert(sent[#sent].mid==1349 and sent[#sent].data.id==1)
 ms.d_mainUI.g_playerInfo.level=60
end)
check('level49_entry_blocked',function()
 local count=#sent;ms.d_mainUI.g_playerInfo.level=49
 ms.d_undergoOrdealUI.enter();ms.d_undergoOrdealUI.pressEnterUndergoLayer();ui.enter(root)
 assert(#sent==count);ms.d_mainUI.g_playerInfo.level=60
end)
check('arena_entry_four_groups',function()
 ui.onGetResult(clone(fixtures.entry))
 assert(fixtures.entry.group_type_level[1]==nil and fixtures.entry.group_type_level[3]==nil)
 local visual=assert(ui.g_arenaUI.main_layer:getChildByTag(9879))
 for group=4,7 do assert(visual:getChildByTag(9900+group)) end
 for group=1,3 do assert(not visual:getChildByTag(9900+group)) end
end)
for stage=1,6 do
 check('arena_exit_reenter_stage_'..stage,function()
  local native=ms.d_u.createMenu;local close
  ms.d_u.createMenu=function(config,...)
   for _,item in ipairs(config) do
    if item.npic=='v2/introUI/close1.png' then close=item.call_back end
   end
   return native(config,...)
  end
  local ok,err=pcall(function()
   for cycle=1,2 do
    ui.g_arenaUI.parent_layer=root
    ui.onGetResult(clone(fixtures['entry_'..stage]))
    local closeEntry=assert(close)
    ui.onGetResult(clone(fixtures[tostring(stage)]))
    -- Settlement rebuilds its own entrance, so capture that callback below
    -- by removing the host through the same native remove helper instead.
    local key=stage==1 and 'qualify_layer' or (stage==2 or stage==6) and 'rank_parent' or 'blood_layer'
    assert(ui.g_arenaUI[key]);assert(close);close()
    assert(ui.g_arenaUI[key]==nil,'Closed rank reference must be cleared')
    local host=assert(root:getChildByTag(9875))
    assert(host:getChildByTag(9879):isVisible(),'Entry must be visible after rank close')
    if stage==6 then ms.d_u.remove(host) else closeEntry() end
    assert(not root:getChildByTag(9875),'Touch-blocking host must be removed')
    assert(ui.g_arenaUI.main_layer==nil,'Closed entrance reference must be cleared')
   end
  end)
  ms.d_u.createMenu=native;assert(ok,err)
 end)
end
for stage=1,6 do
 check('arena_stage_'..stage,function()
  ui.onGetResult(clone(fixtures['entry_'..stage]))
  ui.onGetResult(clone(fixtures[tostring(stage)]))
  assert(ui._localStage().stage==stage)
  local count=#sent
  ui.showExerFight(ui.g_arenaUI.main_layer)
  assert(#sent==count,'Rendering must never poll the server')
  if stage<6 then ui._localAdvance();assert(sent[#sent].mid==1350 and sent[#sent].data.id==7) end
 end)
end
check('arena_fight_update',function() ui.onGetResult(clone(fixtures.update)) end)
check('arena_prize',function()
 local p=ui.g_data.rank.rank_prize_info[1][1].prize_list
 assert(p[1].object_type==11 and p[1].attach_count==500)
 assert(p[2].attach_type==1343 and p[2].attach_count==10)
 ui.showPrize(root);ui.showPrizeDetail(root,1)
end)
check('practice_expired_clock_does_not_poll',function()
 ui.onGetResult(clone(fixtures.entry_2))
 ui.g_data.enter.schedule_list.match_time_list[3].start_time=now-1
 local count=#sent;local oldRest=ms.d_time.getRestTime;local oldDelay=ms.d_u.delay
 ui.onGetResult(clone(fixtures['2']))
 assert(#sent==count,'Expired practice clock must not request another board')
 assert(ms.d_time.getRestTime==oldRest and ms.d_u.delay==oldDelay)
end)
check('arena_records',function() ui.showBloodHis(root) end)
check('arena_rank',function() ui.onGetResult(clone(fixtures.rank)) end)
for stage=1,5 do
 check('arena_return_stage_'..stage,function()
  ui.onGetResult(clone(fixtures['entry_'..stage]))
  ui.onGetResult(clone(fixtures[tostring(stage)]))
  local update=clone(fixtures[tostring(stage)]);update.id=5
  update.event_info.cur_fight_count=2;update.event_info.action_point=3
  update.local_arena.stage_fights=2;ui.onGetResult(update)
  local name=stage==1 and 'showQualifyFight' or stage==2 and 'showExerFight' or 'showBloodFight'
  local native=ui[name];local rendered=0
  ui[name]=function(...) rendered=rendered+1;return native(...) end
  local count=#sent;local oldDelay=ms.d_u.delay
  ms.d_undergoOrdealUI.enter() -- The real fightUI calls this before onFightReturn.
  local ok,err=pcall(ui.onFightReturn,false);ui[name]=native
  assert(ok,err);assert(ms.d_u.delay==oldDelay)
  assert(rendered==1,'Current arena must be rendered before return completes')
  assert(#sent==count,'Fight return must not query entry or group')
  assert(ui.g_data.rank.event_info.cur_fight_count==2 and ui.g_data.rank.event_info.action_point==3)
  assert(ui._localStage().stage_fights==2)
 end)
end
check('arena_record_return',function()
 local count=#sent;local native=ui.showBloodHis;local shown=0
 ui.showBloodHis=function(...) shown=shown+1;return native(...) end
 ms.d_undergoOrdealUI.enter()
 local ok,err=pcall(ui.onFightReturn,true);ui.showBloodHis=native
 assert(ok,err);assert(shown==1 and #sent==count)
end)
check('arena_settlement_popup',function()
 local native=ms.d_commonLayerUI.showPrizeResLayer;local shown=0
 ms.d_commonLayerUI.showPrizeResLayer=function(parent,list,...)
  shown=shown+1
  assert(parent==ui.g_arenaUI.main_layer and #list==3)
  assert(list[1].object_type==11 and list[1].attach_count>0)
  assert(list[2].attach_type==1343 and list[2].attach_count>0)
  assert(list[3].attach_type==1366 and list[3].attach_count>0)
  return native(parent,list,...)
 end
 local ok,err=pcall(function()
  ui.onGetResult(clone(fixtures.settlement));assert(shown==1)
  ui.onGetResult(clone(fixtures['6']));assert(shown==1,'Board refresh must not replay reward popup')
 end)
 ms.d_commonLayerUI.showPrizeResLayer=native;assert(ok,err)
end)
check('settlement_close_returns_to_entry',function()
 -- Fight-return fixtures capture detached scenes; lifecycle callbacks require
 -- this close check to run under the active scene's isolated root.
 ui.g_arenaUI.parent_layer=root
 ui.onGetResult(clone(fixtures.entry_5));ui.onGetResult(clone(fixtures['5']))
 local previous=ui.g_arenaUI.main_layer;previous:retain()
 local native=ms.d_u.createMenu;local close
 ms.d_u.createMenu=function(config,...)
  for _,item in ipairs(config) do
   if item.npic=='v2/introUI/close1.png' then close=item.call_back end
  end
  return native(config,...)
 end
 local ok,err=pcall(function()
  ui.onGetResult(clone(fixtures.settlement))
  assert(previous:getParent()==nil,'Previous blood stage must be removed')
  assert(ui.g_arenaUI.blood_layer==nil,'No blood-stage layer may remain below settlement')
  assert(not ui.g_arenaUI.main_layer:getChildByTag(9879):isVisible(),'Entry options must be hidden behind settlement rank')
  local rank=ui.g_arenaUI.rank_parent;rank:retain()
  assert(close);close()
  local removed=rank:getParent()==nil;rank:release();assert(removed)
  local visual=assert(ui.g_arenaUI.main_layer:getChildByTag(9879));assert(visual:isVisible())
  for group=4,7 do assert(visual:getChildByTag(9900+group)) end
 end)
 ms.d_u.createMenu=native;previous:release();assert(ok,err)
end)
check('map_init',function() map.initMapCsv() end)
check('map_entry',function() ms.d_undergoOrdealUI.onGetResult(1,clone(maps.initial)) end)
check('map_progress',function()
 ms.d_undergoOrdealUI.onGetResult(6,clone(maps.progress))
 assert(map.g_mapUI.mapList.challenge.top_big_id==1)
 assert(map.canFightNextChallenge(1,5))
 map.g_mapUI.jy_mode=2;map.show();ms.d_undergoSubLevelUI.show(1,5)
end)
check('map_nine_position_lineup',function()
 local positions={};local cid
 for _,c in pairs(ms.d_lineupUI.g_characterInfo) do cid=c.id;break end
 if cid then positions[cid]=9 end
 map.g_mapUI.cortege_list=positions
 ms.d_undergoLineupUI.createSearchLayer(map.g_mapUI.main_layer,105,2)
 ms.d_undergoLineupUI.sendMsgFight()
 assert(sent[#sent].mid==1349 and sent[#sent].data.id==4)
 local request=assert(loadstring('return '..sent[#sent].data.data))()
 assert(request.cortege_list[cid]==9 and request.mode==2 and request.map_id==105)
end)
check('map_complete',function()
 ms.d_undergoOrdealUI.onGetResult(6,clone(maps.complete));map.g_mapUI.jy_mode=2;map.show()
 assert(not map.canFightNextChallenge(10,1))
end)
for page=1,3 do
 check('shop_catalog_'..page,function()
  local rows={};for i=(page-1)*6+1,page*6 do rows[#rows+1]=clone(shopCatalog[i]) end
  ms.d_undergoOrdealUI.onGetResult(3,rows)
 end)
end
check('shop',function()
 assert(#shop==6)
 ms.d_undergoOrdealUI.onGetResult(3,clone(shop))
end)
check('shop_request_token',function()
 ms.d_undergoOrdealUI.sendMsg(5,{index=1,count=2})
 assert(sent[#sent].mid==1349 and sent[#sent].data.id==5)
 local request=assert(loadstring('return '..sent[#sent].data.data))()
 assert(request.index==1 and request.count==2 and request.shop_token==shop[1].shop_token)
end)
check('shop_purchase',function()
 local reward=clone(shop[1]);reward.buy_times=reward.buy_times-1
 ms.d_undergoOrdealUI.onGetResult(5,{index=1,attach_list={reward}})
end)
check('day_prize',function() ms.d_undergoOrdealUI.onGetResult(7,clone(prizes)) end)
if ui._localTaixuRestore then ui._localTaixuRestore() end
for _,scene in ipairs(scenes) do scene:cleanup();scene:release() end
root:removeFromParentAndCleanup(true)
for _,entry in ipairs(saved) do
 for k in pairs(entry.target) do if entry.old[k]==nil then entry.target[k]=nil end end
 for k,v in pairs(entry.old) do entry.target[k]=v end
end
ms.d_u.main_server_send_msg=oldSend;ms.d_u.runScene=oldRun;ms.MS_report_error=oldReport
return table.tostring(results)
'''
out=ROOT/'.runtime/taixu-fixture.lua';out.write_text(script)
print(out)
