"""Regression tests for the ordered activity-entry client adapters."""
import unittest
from pathlib import Path

try:
    from lupa.lua51 import LuaRuntime
except ImportError:
    LuaRuntime = None

from network_redirect.summon import client_source, load_rules


FIXTURE = r'''
package={loaded={}}; ms={}; package.loaded.ms=ms
local ids={twoyears=46,dream=40,saveMonkey=48,tower=37,springCard=29,
 springActivityMoney=28,mooncake=45,rice=34,destiny=47}
local cfg={};for _,id in pairs(ids) do cfg[id]={} end
ms.d_funUI={funID=ids,funConfig=cfg,getFunList=function()
 local rows={{id=40},{id=48}}
 if ms.d_twoYearsCelebrateUI.canJoin() then rows[#rows+1]={id=46} end
 return rows end}
local ui={g_self={[0]={}},canJoin=function() return false end,showNews=function()end,
 onGetResult=function()end,pray=function()end,tickTime=function()end,
 createMainFrame=function()end,getChar=function()end,buy=function()end,
 openGiftPackEnsure=function()end,createShop=function()end,openGiftPack=function()end,
 showGiftDetail=function()end}
ms.d_twoYearsCelebrateUI=ui
ms.d_activityUI={getQiwenStatus=function()end}
ms.d_time={getTime=function()return 1000 end}
ms.d_data={g_new_config={[24]={yuanshi_info={begin_time=1000,end_time=2000,permanent=true}}},callback_update_config=function()end}
'''


@unittest.skipIf(LuaRuntime is None, 'requires lupa.lua51')
class ActivityEntryClientTests(unittest.TestCase):
    def test_activity_adapters_install_before_unrelated_pending_module(self):
        lua = LuaRuntime()
        lua.execute(FIXTURE)
        result = lua.execute(client_source(load_rules()))
        entries = lua.eval("(function() local x={};for _,row in ipairs(ms.d_funUI.getFunList()) do x[#x+1]=row.id end;return table.concat(x,',') end)()")
        self.assertEqual(result, 'pending')  # unrelated gameplay adapter is intentionally incomplete
        self.assertEqual(entries, '46')  # 仙梦居／十万猴急 hidden, 元始祈愿 retained
        self.assertEqual(lua.eval("ms.d_funUI._localActivityEntryCurrent()"), 'ready')
        self.assertEqual(lua.eval("ms.d_twoYearsCelebrateUI._localYuanshiCurrent()"), 'ready')


    def new_vm(self):
        lua = LuaRuntime()
        lua.execute(FIXTURE)
        return lua

    def install(self, lua):
        return lua.execute(client_source(load_rules()))

    def assert_entries(self, lua):
        lua.execute("""local rows=ms.d_funUI.getFunList()
          assert(#rows==1 and rows[1].id==46 and rows[1].index==1)
          assert(ms.d_twoYearsCelebrateUI.canJoin())""")

    def test_repeated_install_does_not_wrap_twice(self):
        lua = self.new_vm()
        self.install(lua)
        lua.execute('savedList=ms.d_funUI.getFunList;savedJoin=ms.d_twoYearsCelebrateUI.canJoin')
        for _ in range(3):
            self.install(lua)
            self.assert_entries(lua)
        lua.execute('assert(savedList==ms.d_funUI.getFunList and savedJoin==ms.d_twoYearsCelebrateUI.canJoin)')

    def test_new_activity_module_detected_while_summon_survives(self):
        lua = self.new_vm()
        self.install(lua)
        lua.execute("""package.loaded['ui.summonUI']={_localGoldRestore=function() end}
          oldCurrent=ms.d_funUI._localActivityEntryCurrent
          ms.d_funUI={funID=ms.d_funUI.funID,funConfig=ms.d_funUI.funConfig,
          getFunList=function() return {{id=40},{id=48},{id=46}} end}
          assert(oldCurrent()=='pending' and not ms.d_funUI._localActivityEntryCurrent)
          assert(type(package.loaded['ui.summonUI']._localGoldRestore)=='function')""")
        self.install(lua)
        self.assert_entries(lua)

    def test_same_table_list_redefinition_detected_and_repaired(self):
        lua = self.new_vm()
        self.install(lua)
        lua.execute("""ms.d_funUI.getFunList=function() return {{id=48},{id=40},{id=46}} end
          assert(ms.d_funUI._localActivityEntryCurrent()=='pending')""")
        self.install(lua)
        self.assert_entries(lua)

    def test_yuanshi_same_table_redefinition_detected_and_repaired(self):
        lua = self.new_vm()
        self.install(lua)
        lua.execute("""ms.d_twoYearsCelebrateUI.canJoin=function() return false end
          assert(ms.d_twoYearsCelebrateUI._localYuanshiCurrent()=='pending')""")
        self.install(lua)
        self.assert_entries(lua)

    def test_yuanshi_new_module_and_relogin(self):
        lua = self.new_vm()
        self.install(lua)
        lua.execute('oldCurrent=ms.d_twoYearsCelebrateUI._localYuanshiCurrent')
        lua.execute(FIXTURE)
        lua.execute("assert(oldCurrent()=='pending')")
        self.install(lua)
        self.assert_entries(lua)

    def test_missing_yuanshi_does_not_delay_hidden_entry_filter(self):
        lua = self.new_vm()
        lua.execute('savedYuanshi=ms.d_twoYearsCelebrateUI;ms.d_twoYearsCelebrateUI=nil;ms.d_funUI.getFunList=function() return {{id=40},{id=48}} end')
        self.assertEqual(self.install(lua), 'pending')
        lua.execute('assert(#ms.d_funUI.getFunList()==0);ms.d_twoYearsCelebrateUI=savedYuanshi')
        self.install(lua)
        self.assertEqual(lua.eval('ms.d_twoYearsCelebrateUI._localYuanshiCurrent()'), 'ready')

    def test_missing_entry_module_does_not_delay_yuanshi(self):
        lua = self.new_vm()
        lua.execute('savedEntry=ms.d_funUI;ms.d_funUI=nil')
        self.assertEqual(self.install(lua), 'pending')
        lua.execute('assert(ms.d_twoYearsCelebrateUI.canJoin());ms.d_funUI=savedEntry')
        self.install(lua)
        self.assert_entries(lua)

    def test_unrelated_animation_config_missing_does_not_delay_filter(self):
        lua = self.new_vm()
        lua.execute('ms.d_funUI.funConfig[37]=nil')
        self.install(lua)
        self.assert_entries(lua)

    def test_existing_yuanshi_cycle_and_stale_action_regression(self):
        import network_redirect
        source = Path(network_redirect.__file__).with_name('yuanshi_client.lua').read_text()
        harness = Path(__file__).with_name('yuanshi_client_regression.lua').read_text()
        self.assertIn('passed', LuaRuntime().execute(harness.replace('-- INSTALL_PATCH', source)))
