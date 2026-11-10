"""Lua adapter contracts for the weekend gate and trial reward presentation."""
import unittest
from pathlib import Path
try:
    from lupa.lua51 import LuaRuntime
except ImportError:
    LuaRuntime=None


@unittest.skipIf(LuaRuntime is None,'requires lupa.lua51')
class GuildTrialClientTests(unittest.TestCase):
    def setUp(self):
        self.lua=LuaRuntime()
        self.lua.execute('''
         weekend=false;labels={};sent=0;messages={}
         pet={g_self={g_InsidePetInfo={total_catch_times=3,left_catch_times=2}}}
         pet.g_self.total_catch_times={setString=function(self,s) self.text=s end}
         pet.g_self.g_rest_catch_times={setString=function(self,s) self.text=s end}
         ms={d_petHomeUI=pet,d_pethuntUI={g_self={},g_data={},g_pethuntUI={}},
          d_fightUI={g_fightUI={last_fight_type=27,last_final_result=4}},
          d_secretAreaUI={},d_escortUI={},
          d_event_mgr={getLastFightType=function() return 27 end},
          d_time={is_weekend=function() return weekend end},
          d_hz={gethz=function(k) return k end},
          d_info={show=function(s) messages[#messages+1]=s end},
          d_u={createByStyles=function(s) labels[#labels+1]=s.string end,createMenu=function() end},
          d_messageUI={createGetItemsLayer=function(parent,data) rewardItems=data.attach_list end}}
         package.loaded.ms=ms;pet.d_ms=ms
         setmetatable(pet,{__index=_G})
         pet.GetPetMenu=function()
          if not d_ms.d_time.is_weekend() then d_ms.d_info.show(d_ms.d_hz.gethz('pet_lucky_hint4'));return end
          sent=sent+1
         end
         pet.GetResultInsidePetInfo=function()
          timer=function() return d_ms.d_time.is_weekend(),d_ms.d_hz.gethz('pet_lucky_hint5') end
         end
         pet.createShiLianLayer=function()
          trialWeekend=d_ms.d_time.is_weekend()
          if renderSupportButton then
           d_ms.d_u.CreateButton('v2/petHomeUI/support1.png','v2/petHomeUI/support2.png',function()
            pet.sendMsgSupport();pet.g_self.g_data.can_support=1
           end)
          end
          for _,key in ipairs({'pet_reward_info1','pet_reward_info2','pet_reward_info3','pet_reward_info6'}) do
           d_ms.d_u.createByStyles({type='label',string=d_ms.d_hz.gethz(key)})
          end
         end
         for _,key in ipairs({'GetPetMenu','GetResultInsidePetInfo','createShiLianLayer'}) do setfenv(pet[key],pet) end
         pet.GetResultPrize=function() error('unexpected legacy prize') end
         supportRequests=0
         pet.sendMsgSupport=function() supportRequests=supportRequests+1 end
         pet.GetResultSupport=function() error('unexpected legacy support') end
         pet.updataShiLianLayer=function() pet.createShiLianLayer() end
         ms.d_fightUI.showFightEnd=function()
          assert(ms.d_event_mgr.getLastFightType()==28,'native trial autoplay was not suppressed')
          displayedResult=ms.d_fightUI.g_fightUI.last_final_result
         end
         ms.d_fightUI.menuHome_private=function() end
         originals={menu=pet.GetPetMenu,inside=pet.GetResultInsidePetInfo,trial=pet.createShiLianLayer}
        ''')
        for source in ('guild_activity_client.lua','guild_pet_client.lua'):
            self.lua.execute(Path('network_redirect',source).read_text())

    def test_adoption_gate_and_timer_follow_calendar_while_trial_stays_open(self):
        self.lua.execute('''
         pet.GetPetMenu();assert(sent==0 and messages[1]=='领养活动仅周六、周日开放')
         pet.GetResultInsidePetInfo();assert(pet.timer()==false)
         local _,hint=pet.timer();assert(hint=='领养活动仅周六、周日开放')
         weekend=true;pet.GetPetMenu();assert(pet.sent==1 and pet.timer()==true)
         weekend=false;pet.GetPetMenu();assert(pet.sent==1 and pet.timer()==false)
         pet.g_self.g_data={};pet.createShiLianLayer();assert(pet.trialWeekend==true)
         assert(ms.d_time.is_weekend()==false,'trial override leaked into shared clock')
        ''')

    def test_floor_adoption_preview_and_authoritative_claim_counters(self):
        self.lua.execute('''
         local trial={trial_reward_mode='silver_peach',train_prize={}}
         for floor=1,4 do trial.train_prize[floor]={add_catch_count=floor*3,prize_list={
          {object_type=12,attach_type=0,attach_count=floor*50000},
          {object_type=5,attach_type=1001,attach_count=floor*5}}} end
         pet.GetResultPrize({result=1,trial_state=trial,add_catch_count=9,
          total_catch_times=12,left_catch_times=11,prize_list={{attach_count=150000}}})
         assert(labels[1]=='一层累计领养+3' and labels[2]=='二层累计领养+6' and labels[3]=='三层累计领养+9')
         assert(labels[4]=='四层累计：银两×200000 蟠桃×20 领养+12')
         assert(pet.g_self.g_InsidePetInfo.total_catch_times==12 and pet.g_self.g_InsidePetInfo.left_catch_times==11)
         assert(pet.g_self.total_catch_times.text=='12' and pet.g_self.g_rest_catch_times.text=='11')
         assert(messages[1]=='获得领养次数×9，周末可使用' and rewardItems[1].attach_count==150000)
         assert(ms.d_hz.gethz('pet_reward_info1')=='pet_reward_info1','reward override leaked')
        ''')

    def test_defeat_panel_keeps_server_result_and_patches_restore(self):
        self.lua.execute('''
         ms.d_fightUI.showFightEnd();assert(displayedResult==4)
         assert(ms.d_event_mgr.getLastFightType()==27)
         ms._localGuildPetRestore();ms._localGuildActivitiesRestore()
         assert(pet.GetPetMenu==originals.menu and pet.GetResultInsidePetInfo==originals.inside)
         assert(pet.createShiLianLayer==originals.trial)
         pet.g_self.g_data={};pet.createShiLianLayer();assert(pet.trialWeekend==false)
        ''')

    def test_support_counts_percent_button_and_duplicate_click_guard(self):
        self.lua.execute('''
         local now=10
         ms.d_time.getTime=function() return now end
         local function node()
          return {setString=function(self,s) self.text=s end,setTag=function(self,t) self.tag=t end,
           setVisible=function(self,v) self.visible=v end,setEnabled=function(self,v) self.enabled=v end}
         end
         local parent={children={},getChildByTag=function(self,tag) return self.children[tag] end,
          addChild=function(self,n) self.children[n.tag]=n end}
         ms.d_u.createByStyles=function() return node() end
         ms.d_u.setProperties=function() end
         local state=pet.g_self
         state.g_Shilian_layer={};state.support1=node();state.support2=node()
         state.support2.getParent=function() return parent end
         state.g_suppor_info={node(),node(),node(),node()}
         state.g_data={support=0,support_limit=3,support_remaining=3,support_percent=5,
          support_bonus_percent=0,can_support=true,last_time=100}
         pet.upDateSupport()
         assert(state.support1.visible and state.support1.enabled and not state.support2.visible)
         local label=parent.children[910078]
         assert(label.text=='今日点赞 0/3（每次+5%）')
         for count=1,3 do
          pet.sendMsgSupport();assert(supportRequests==count)
          -- The native button sets numeric 1 while the reply is in flight.
          state.g_data.can_support=1;pet.upDateSupport()
          pet.sendMsgSupport();assert(supportRequests==count)
          assert(not state.support1.enabled and state.support2.visible)
          pet.GetResultSupport({result=1,support=count,support_limit=3,support_remaining=3-count,
           support_percent=5,support_bonus_percent=count*5,can_support=count<3})
          for _,n in ipairs(state.g_suppor_info) do assert(n.text=='+'..tostring(count*5)..'%') end
          assert(state.support1.enabled==(count<3))
          assert(parent.children[910078]==label)
         end
         assert(label.text=='今日点赞 3/3（每次+5%）')
         pet.sendMsgSupport();assert(supportRequests==3 and messages[#messages]=='今日试炼点赞次数已用完')
         state.g_data.support_remaining=1;state.g_data.can_support=0
         pet.upDateSupport();assert(state.support1.enabled)
         now=100;pet.upDateSupport();assert(not state.support1.enabled)
         pet.sendMsgSupport();assert(supportRequests==3 and messages[#messages]=='当前试炼不可点赞')
         state.g_Shilian_layer=nil
         pet.GetResultSupport({result=1,support=2,support_limit=3,support_remaining=1,
          support_percent=5,support_bonus_percent=10,can_support=true})
        ''')

    def test_paid_support_requires_confirmation_and_cancel_restores_button(self):
        self.lua.execute('''
         local now=10
         ms.d_time.getTime=function() return now end
         ms.d_mainUI={g_playerInfo={gold_coin=60}}
         local dialogs=0;local yes,no,prompt
         ms.d_quitUI={createYesNoByStyle=function(parent,options,confirm,cancel)
          dialogs=dialogs+1;yes=confirm;no=cancel;prompt=options.string
         end}
         local data={support=0,support_limit=3,support_remaining=3,support_percent=5,
          support_gold=20,support_bonus_percent=0,can_support=true,last_time=100}
         pet.g_self.g_data=data;pet.g_self.g_Shilian_layer={}
         local clicked
         local createButton=function(normal,selected,callback) clicked=callback end
         ms.d_u.CreateButton=createButton;renderSupportButton=true
         pet.createShiLianLayer();assert(ms.d_u.CreateButton==createButton)
         clicked()
         assert(dialogs==1 and supportRequests==0 and data.can_support==false)
         assert(prompt:find('消耗20元宝',1,true) and prompt:find('今日还可点赞3次',1,true))
         pet.sendMsgSupport();assert(dialogs==1 and supportRequests==0)
         no();assert(data.can_support==true and supportRequests==0)
         yes();assert(supportRequests==0,'cancelled confirmation must be inert')
         pet.sendMsgSupport();yes();yes()
         assert(supportRequests==1 and data.can_support==false)
         pet.GetResultSupport({result=1,support=1,support_limit=3,support_remaining=2,
          support_gold=20,gold_cost=20,support_percent=5,support_bonus_percent=5,can_support=true})
         assert(messages[#messages]=='点赞成功，消耗20元宝，当前加成+5%')
         assert(data.can_support and data.support_gold==20)
         ms.d_mainUI.g_playerInfo.gold_coin=19
         pet.sendMsgSupport();assert(dialogs==2 and supportRequests==1 and data.can_support)
         assert(messages[#messages]=='元宝不足，点赞需要20元宝')
         ms.d_mainUI.g_playerInfo.gold_coin=20
         pet.sendMsgSupport();ms.d_mainUI.g_playerInfo.gold_coin=0;yes()
         assert(supportRequests==1 and data.can_support,'balance must be rechecked on confirm')
         ms.d_mainUI.g_playerInfo.gold_coin=20
         pet.sendMsgSupport();now=100;yes();assert(supportRequests==1)
         now=10;pet.sendMsgSupport();pet.g_self.g_Shilian_layer=nil;yes()
         assert(supportRequests==1,'closed trial must not spend gold')
        ''')
