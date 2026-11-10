"""Selection restrictions in the injected Lua 5.1 equipment adapter."""
import unittest
from pathlib import Path
from network_redirect import summon

try:
    from lupa.lua51 import LuaRuntime
except ImportError:
    LuaRuntime = None


@unittest.skipIf(LuaRuntime is None, 'requires lupa.lua51')
class EquipmentRecycleClientTests(unittest.TestCase):
    def setUp(self):
        self.lua = LuaRuntime()
        self.source = (Path(summon.__file__).parent / 'equipment_client.lua').read_text()
        self.lua.execute('''
         items={}
         ui={getEquipsForRecycle=function() return items end}
         native=ui.getEquipsForRecycle
         package.loaded.ms={d_cortegeRecycleUI=ui}
         function item(id,fields)
          local row={id=id,count=1,level=1,csvInfo={quality=4,mainType=1}}
          for key,value in pairs(fields or {}) do row[key]=value end
          items[#items+1]=row;return row
         end
        ''')
        self.lua.execute(self.source)

    def test_protected_equipment_excluded_without_hiding_valid_growth(self):
        self.lua.execute('''
         item(1)
         item(2,{level=80,advance_level=10,star_count=7,cur_spirit_count=2,
           drill_count=2,stone1_level=10,csvInfo={quality=5,mainType=3}})
         item(3,{count=3,is_lock=0,reborn_bit=0,star_level=0})
         for n,key in ipairs({'equip_order','owner_id','is_lock','innate_owner_id',
           'protogenic','star_level','reborn_bit'}) do item(10+n,{[key]=1}) end
         for n,key in ipairs({'advance_level','star_count','cur_spirit_count','drill_count'}) do
          item(30+n,{count=2,[key]=1})
         end
         item(40,{count=2,level=2});item(41,{count=0})
         item(42,{csvInfo={quality=3}});item(43,{csvInfo={quality=6}})
         local rows=ui.getEquipsForRecycle()
         assert(#rows==3 and rows[1].id==1 and rows[2].id==2 and rows[3].id==3)
         assert(rows[2]==items[2] and items[2].stone1_level==10)
         assert(#items==18, 'must not remove inventory entries')
         items[1].is_lock=1
         assert(#ui.getEquipsForRecycle()==2, 'reopening must use current restrictions')
        ''')

    def test_idempotent_install_restore_and_late_module_load(self):
        self.lua.execute('wrapped=ui.getEquipsForRecycle')
        self.lua.execute(self.source)
        self.lua.execute('''
         assert(ui.getEquipsForRecycle==wrapped)
         ui._localEquipRecycleRestore()
         assert(ui.getEquipsForRecycle==native and not ui._localEquipRecycleRestore)
         package.loaded.ms={}
        ''')
        self.lua.execute(self.source)
        self.lua.execute('package.loaded.ms.d_cortegeRecycleUI=ui')
        self.lua.execute(self.source)
        self.lua.execute('assert(ui.getEquipsForRecycle~=native)')

    def test_login_patch_contains_adapter_and_compiles(self):
        source = summon.client_source(summon.load_rules())
        self.assertIn('_localEquipRecycleRestore', source)
        self.lua.globals().source = source
        self.lua.execute('assert(loadstring(source))')
