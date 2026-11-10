"""Run the injected Lua adapter against the native settlement/count contract."""
import unittest
from pathlib import Path
try:
    from lupa.lua51 import LuaRuntime
except ImportError:
    LuaRuntime=None


@unittest.skipIf(LuaRuntime is None,'requires lupa.lua51')
class GuildSecretClientTests(unittest.TestCase):
    def setUp(self):
        self.lua=LuaRuntime()
        self.lua.execute('''
         labels={};nodes={}
         function node(text)
          return {text=text,setTag=function(self,t) self.tag=t end,
           registerScriptHandler=function(self,f) self.handler=f end,
           setString=function(self,t) self.text=t end,setVisible=function() end}
         end
         parent={addChild=function(self,n) nodes[#nodes+1]=n end,
          getChildByTag=function(self,t) for _,n in ipairs(nodes) do if n.tag==t then return n end end end}
         secret={g_self={main_layer=parent,prize_bkg={},prize_btns={}}}
         ms={d_secretAreaUI=secret,d_petHomeUI={GetPetMenu=function() end,
          createShiLianLayer=function() end,GetResultInsidePetInfo=function() end},
          d_escortUI={},d_time={},d_u={getRealScale=function() return 1,1 end,
          createByStyles=function(o) labels[#labels+1]=o.string;return node(o.string) end,
          createMenu=function() end},d_hz={gethz=function(k)
           if k=='secretArea_prize_tink1' then return '第%d层，获得%d次' end
           if k=='secretArea_free_times' then return '今日可免费探宝次数：%d' end
          end}}
         package.loaded.ms=ms
         secret.showFightEnd=function()
          ending={secret.g_self.fight_count,secret.g_self.free_times}
          if failEnd then error('native failure') end
         end
         secret.setFreeTimes=function(f,n)
          if f~=nil then secret.g_self.free_times=f end
          if n~=nil then secret.g_self.fight_count=n end
         end
         secret.showPrizePage=function(p)
          local s=secret.g_self
          p:addChild(ms.d_u.createByStyles({type='label',string=string.format(ms.d_hz.gethz('secretArea_prize_tink1'),s.fight_count,s.prize_data.max_free_times)}))
          if s.free_times>0 then p:addChild(ms.d_u.createByStyles({type='label',string=string.format(ms.d_hz.gethz('secretArea_free_times'),s.free_times)})) end
         end
         secret.callback_fam_search_gold=function(d)
          if d.flag==1 then secret.g_self.prize_data=d end
          secret.setFreeTimes(d.free_times,d.fight_count)
          secret.showPrizePage(parent)
         end
         secret.showTeamPage=function() end
         originalEnd=secret.showFightEnd
        ''')
        self.source=Path('network_redirect/guild_activity_client.lua').read_text()
        self.lua.execute(self.source)

    def test_settlement_uses_clears_and_remaining_not_attempts(self):
        self.lua.execute('''
         for _,case in ipairs({{1,1,5},{2,1,3},{3,2,8},{3,3,15},{1,0,0}}) do
          secret.g_self.fight_count=case[1];secret.g_self.free_times=3
          secret.g_self.fight_data={cleared_layer=case[2],search_free_times=case[3]}
          secret.showFightEnd()
          assert(ending[1]==case[2] and ending[2]==case[3])
          assert(secret.g_self.fight_count==case[1] and secret.g_self.free_times==3)
         end
         failEnd=true;assert(not pcall(secret.showFightEnd))
         assert(secret.g_self.fight_count==1 and secret.g_self.free_times==3)
        ''')

    def test_reopen_counts_zero_and_partial_cache_refresh(self):
        self.lua.execute('''
         secret.callback_fam_search_gold({result=1,flag=1,cleared_layer=1,max_layer=3,
          fight_count=2,free_times=3,max_free_times=5,earned_search_times=5})
         assert(labels[1]=='今日已通关1/3层，累计获得5次探宝机会。')
         assert(labels[2]=='今日可免费探宝次数：3')
         assert(secret.g_self.fight_count==2)
         labels={}
         secret.callback_fam_search_gold({result=1,flag=5,cleared_layer=2,max_layer=3,
          fight_count=3,free_times=8,max_free_times=10,earned_search_times=10})
         assert(labels[1]=='今日已通关2/3层，累计获得10次探宝机会。')
         assert(labels[2]=='今日可免费探宝次数：8')
         secret.setFreeTimes(7);assert(nodes[#nodes].text=='今日可免费探宝次数：7')
         labels={}
         secret.callback_fam_search_gold({result=1,flag=1,cleared_layer=0,max_layer=3,
          fight_count=0,free_times=0,max_free_times=0,earned_search_times=0})
         assert(labels[1]=='今日已通关0/3层，累计获得0次探宝机会。')
         assert(labels[2]=='今日可免费探宝次数：0')
        ''')

    def test_restore_and_idempotence(self):
        self.lua.execute('wrappedEnd=secret.showFightEnd')
        self.lua.execute(self.source)
        self.lua.execute('''assert(secret.showFightEnd==wrappedEnd)
         ms._localGuildActivitiesRestore();assert(secret.showFightEnd==originalEnd)''')
