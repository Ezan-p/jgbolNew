-- Lua 5.1 contract regression: native zero-truthiness and positional sweep UI.
local source=...
local checks={}
local function check(name,fn) fn();checks[#checks+1]=name end
local ui={}
local player={level=60,vip_level=0,energy=20,gold_coin=100}
local sent,dialog,notice,needGold,addEnergy,prizes,menu
local function label()
 return {setString=function(self,s) self.text=s end,
         setVisible=function(self,v) self.visible=v end}
end
local function oldMenu(style)
 menu=style
 return style
end
local function oldPage()
 ui.g_self.cost_gold_label=label()
 ui.g_self.main_btns={label(),label(),label(),label()}
 package.loaded.ms.d_u.createMenu({
  {npic='v2/crossDoom/fight_all1.png',call_back=function() error('old sweep callback') end},
  {npic='other',call_back=function() return 'other' end}})
 return 'native-page'
end
local function oldHint()
 -- Native refresh hides the option below level 25 or after clearing a board.
 ui.g_self.main_btns[2]:setVisible(player.level>=25 and not ui.g_self.is_all_pass)
 return 'native-hint'
end
local function oldSweep(data)
 prizes={}
 for _,r in ipairs(data) do
  local entry=ui.g_self.cardPage_enmey_map[r.form_index*100+r.index]
  if entry and r.fight_result>=1 and r.fight_result<=3 then
   entry.v.has_win=true
   if r.skill_type and r.skill_count then
    -- Native accepts zero and prize UI shows the resulting extra book icon.
    prizes[#prizes+1]={type=r.skill_type,count=r.skill_count}
   end
  end
 end
 return 'native-sweep'
end
ui.createCardPage=oldPage;ui.setFreeFreshTink=oldHint;ui.showRapeSweepRet=oldSweep
ui.pressGoOnCard=function() end;ui.callbackRapeInfo=function() end
ui.createCardHead=function() end
ui.createAddKillPointHint=function() addEnergy=true end
local ms={d_crossDoomUI=ui,d_mainUI={g_playerInfo=player},
 d_music_mgr={playClickEffect=function() end},
 d_info={show=function(v) notice=v end},
 d_summonUI={needGold=function() needGold=true end},
 d_quitUI={createYesNoByStyle=function(parent,style,callback) dialog={style=style,confirm=callback} end},
 d_msg_def={gscl_msg_id={msg_rape_sweep_request=1072}},
 d_u={createMenu=oldMenu,main_server_send_msg=function(id,data) sent={id=id,data=data} end}}
package.loaded.ms=ms
local function install() assert(loadstring(source))() end
local function reset(rate,n)
 sent=nil;dialog=nil;notice=nil;needGold=false;addEnergy=false;prizes={}
 player.level=60;player.vip_level=0;player.energy=20;player.gold_coin=100
 local rows,map={},{}
 for i=1,n or 3 do
  local v={has_win=false,index=i,rand=7-i}
  rows[900+i]=v
  -- Deliberately use reversed on-screen order, like native ascending rand.
  map[100+(n or 3)+1-i]={id=900+i,type=2,v=v}
 end
 ui.g_self={card_data={sweep_gold_per_fight=rate,rape_list={{form_list={[2]=rows}}}},
  cardPage_enmey_map=map,main_layer={},cardPage_layer={},is_all_pass=false}
 ui.createCardPage()
end
install()
check('idempotent installation',function()
 local wrapped=ui.showRapeSweepRet;install();assert(ui.showRapeSweepRet==wrapped)
end)
check('zero reward reproduced in native callback',function()
 reset(1)
 oldSweep({{form_index=1,index=1,fight_result=1,skill_type=101,skill_count=0}})
 assert(#prizes==1 and prizes[1].count==0)
end)
check('paid label and confirmation follow server quote even with stale VIP display',function()
 reset(1);player.vip_level=5;player.energy=2
 assert(ui.setFreeFreshTink()=='native-hint' and ui.g_self.cost_gold_label.text=='2元宝')
 menu[1].call_back()
 assert(dialog.style.txt_styles[2].string=='消耗精力： 2')
 assert(dialog.style.txt_styles[3].string=='消耗元宝： 2')
 assert(not sent and player.gold_coin==100)
 dialog.confirm();assert(sent.id==1072 and player.gold_coin==100)
 assert(menu[2].call_back()=='other' and ms.d_u.createMenu==oldMenu)
end)
check('VIP free quote and low-level VIP eligibility',function()
 reset(0);player.vip_level=5;player.level=8;player.gold_coin=0
 ui.setFreeFreshTink();assert(ui.g_self.cost_gold_label.text=='免费' and ui.g_self.main_btns[2].visible)
 menu[1].call_back();assert(dialog.style.txt_styles[3].string=='消耗元宝： 0')
 dialog.confirm();assert(sent.id==1072)
end)
check('legacy quote fallback uses VIP boundary',function()
 for _,vip in ipairs({0,4,5,10}) do
  reset(nil);player.vip_level=vip;ui.setFreeFreshTink()
  assert(ui.g_self.cost_gold_label.text==(vip<5 and '3元宝' or '免费'))
 end
end)
check('zero energy, insufficient gold, locked and busy do not send',function()
 reset(1);player.energy=0;menu[1].call_back();assert(addEnergy and not sent and not dialog)
 reset(1);player.gold_coin=2;menu[1].call_back();assert(needGold and not sent and not dialog)
 reset(1);player.level=24;ui.setFreeFreshTink();assert(ui.g_self.main_btns[2].visible)
 menu[1].call_back();assert(not sent and not dialog and notice)
 reset(1);ui.g_self.cross_doom_btn_busy=true;menu[1].call_back();assert(not sent and not dialog)
end)
check('only actual awards appear, IDs override wrong position',function()
 reset(1)
 local data={
  {form_index=1,index=1,object_type=2,object_id=901,fight_result=1,skill_type=101,skill_count=0},
  {form_index=1,index=2,object_type=2,object_id=902,fight_result=4,skill_type=101,skill_count=0},
 }
 assert(ui.showRapeSweepRet(data)=='native-sweep')
 local rows=ui.g_self.card_data.rape_list[1].form_list[2]
 assert(rows[901].has_win and not rows[902].has_win and not rows[903].has_win)
 assert(#prizes==0 and data[1].index==1 and data[1].skill_count==0)
 ui.setFreeFreshTink();assert(ui.g_self.cost_gold_label.text=='2元宝')
 menu[1].call_back();assert(dialog.style.txt_styles[3].string=='消耗元宝： 2')
 ui.showRapeSweepRet({
  {form_index=1,index=2,object_type=2,object_id=902,fight_result=1},
  {form_index=1,index=3,object_type=2,object_id=903,fight_result=1,skill_type=101,skill_count=2}})
 assert(#prizes==1 and prizes[1].type==101 and prizes[1].count==2)
 assert(rows[901].has_win and rows[902].has_win and rows[903].has_win)
 ui.g_self.is_all_pass=true;ui.setFreeFreshTink()
 assert(ui.g_self.cost_gold_label.text=='0元宝' and ui.g_self.main_btns[2].visible)
end)
check('option remains visible across levels and VIP tiers with accurate cost labels',function()
 for _,level in ipairs({8,24,25,60}) do
  for _,vip in ipairs({0,4,5,10}) do
   reset(vip<5 and 1 or 0);player.level=level;player.vip_level=vip
   ui.createCardPage()
   assert(ui.g_self.main_btns[2].visible)
   ui.setFreeFreshTink()
   assert(ui.g_self.main_btns[2].visible)
   assert(ui.g_self.cost_gold_label.text==(vip<5 and '3元宝' or '免费'))
   menu[1].call_back()
   if level<25 and vip<5 then
    assert(not dialog and notice=='一键渡劫需25级或VIP5')
   else
    assert(dialog.style.txt_styles[3].string=='消耗元宝： '..(vip<5 and 3 or 0))
   end
   player.energy=0;ui.setFreeFreshTink()
   assert(ui.g_self.main_btns[2].visible)
   assert(ui.g_self.cost_gold_label.text==(vip<5 and '0元宝' or '免费'))
  end
 end
end)
check('replacement IDs, mixed groups and equal sort keys resolve exact target',function()
 reset(1)
 local rows=ui.g_self.card_data.rape_list[1].form_list[2]
 rows[999]=rows[901];rows[901]=nil
 local map=ui.g_self.cardPage_enmey_map
 map[103].id=999
 ui.g_self.card_data.rape_list[1].form_list[1]={[999]={has_win=false}}
 map[101]={id=999,type=1,v=ui.g_self.card_data.rape_list[1].form_list[1][999]}
 ui.showRapeSweepRet({{form_index=1,index=1,object_type=2,object_id=999,fight_result=1}})
 assert(rows[999].has_win and not map[101].v.has_win)
end)
check('missing avatar still synchronizes server victory',function()
 reset(1);ui.g_self.cardPage_enmey_map[103]=nil
 ui.showRapeSweepRet({{form_index=1,index=1,object_type=2,object_id=901,fight_result=1}})
 local rows=ui.g_self.card_data.rape_list[1].form_list[2]
 assert(rows[901].has_win and not rows[903].has_win)
end)
check('page build failure restores shared menu factory',function()
 ui._localRapeRestore();ui.createCardPage=function() error('build failure') end;install()
 assert(not pcall(ui.createCardPage));assert(ms.d_u.createMenu==oldMenu)
 ui._localRapeRestore();ui.createCardPage=oldPage;install()
end)
check('uninstall restores all replaced methods',function()
 ui._localRapeRestore()
 assert(ui.createCardPage==oldPage and ui.setFreeFreshTink==oldHint and ui.showRapeSweepRet==oldSweep)
end)
return checks
