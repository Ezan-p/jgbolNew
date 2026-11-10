"""Lua 5.1 regression for the actual injected map adapter."""
import unittest
from network_redirect import activity, activity_treasure, summon
try:
    from lupa.lua51 import LuaRuntime
except ImportError:
    LuaRuntime = None


@unittest.skipIf(LuaRuntime is None, 'requires lupa.lua51')
class TreasureClientTests(unittest.TestCase):
    def setUp(self):
        self.lua = LuaRuntime()
        self.lua.execute('''
         calls=0;notices={};owned=7
         ui={createBatchUse=function(parent,defs,callback)
          calls=calls+1;lastDefs=defs;lastCallback=callback;return 'picker'
         end}
         menus={createTableViewMenu=function(config) lastMenu=config;return 'menu' end}
         data={getItemCountByType=function(kind,tid) assert(kind==5);return owned end,g_new_config={}}
         ms={d_treasureMapUI=ui,d_data=data,d_tableView=menus,
          d_common_def={client_config_type={common_config=24}},
          d_mainUI={g_mainUI={main_layer={}},g_playerInfo={level=80}},
          d_info={show=function(text) notices[#notices+1]=text end}}
         package.loaded.ms=ms
         oldBatch=ui.createBatchUse;oldMenu=menus.createTableViewMenu
         function mapMenu(tid)
          local itemInfo={type_id=tid,count=7}
          local callback=function() assert(itemInfo.count>=10,'native threshold') end
          return {menuItems={{npic='use',tapHandler=function() singleCalled=true end},
            {nSprite={},sSprite={},tapHandler=callback,pos={x=2,y=3}}}}
         end
        ''')
        self.source = activity_treasure.client_source(activity.load_rules())
        self.lua.execute(self.source)

    def test_low_inventory_button_uses_native_picker_and_current_inventory(self):
        self.lua.execute('''
         local config=mapMenu(1431)
         assert(menus.createTableViewMenu(config)=='menu')
         local button=config.menuItems[2]
         assert(button.nSprite==nil and button.npic=='v2/packageUI/piliangshiyong1.png')
         assert(button.pos.x==2)
         config.menuItems[1].tapHandler();assert(singleCalled)
         owned=3;button.tapHandler()
         assert(calls==1 and lastDefs.itemType==1431 and lastDefs.max==3 and lastDefs.defaultCount==1)
         local costs=data.g_new_config[24].specter_info.open_multi_cost
         for i=1,5 do assert(costs[i]==(i-1)*20) end
        ''')

    def test_quantity_cap_zero_level_and_config_reload(self):
        self.lua.execute('''
         local defs={itemType=1440,max=15,defaultCount=15}
         owned=120;ui.createBatchUse({},defs)
         assert(lastDefs.max==99 and lastDefs.min==1 and defs.max==15)
         data.g_new_config={};owned=1;ui.createBatchUse({},defs)
         assert(lastDefs.max==1 and data.g_new_config[24].specter_info.open_multi_cost[5]==80)
         owned=0;ui.createBatchUse({},defs);assert(calls==2 and #notices==1)
         owned=3;ms.d_mainUI.g_playerInfo.level=69;ui.createBatchUse({},defs)
         assert(calls==2 and #notices==2)
        ''')

    def test_other_buttons_passthrough_and_idempotent_restore(self):
        self.lua.execute('''
         unrelated=mapMenu(1001);originalCallback=unrelated.menuItems[2].tapHandler
         menus.createTableViewMenu(unrelated)
         assert(unrelated.menuItems[2].tapHandler==originalCallback and unrelated.menuItems[2].nSprite)
         ui.createBatchUse({}, {itemType=1001,max=17},'callback')
         assert(lastDefs.max==17 and lastCallback=='callback')
         wrapped=ui.createBatchUse;wrappedMenu=menus.createTableViewMenu
        ''')
        self.lua.execute(self.source)
        self.lua.execute('''assert(wrapped==ui.createBatchUse and wrappedMenu==menus.createTableViewMenu)
         ui._localTreasureRestore();assert(ui.createBatchUse==oldBatch and menus.createTableViewMenu==oldMenu)''')

    def test_missing_dependencies_retry(self):
        lua = LuaRuntime(); lua.execute('package.loaded.ms={}')
        self.assertEqual(lua.execute(self.source), 'pending')

    def test_full_login_patch_compiles_with_adapter(self):
        source = summon.client_source(summon.load_rules())
        self.assertNotIn('__TREASURE_', source)
        self.lua.globals().source = source
        self.lua.execute('assert(loadstring(source))')
