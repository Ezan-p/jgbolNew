"""Execute the escort module's scoped translations in Lua 5.1."""
import unittest
from pathlib import Path
try:
    from lupa.lua51 import LuaRuntime
except ImportError:
    LuaRuntime = None


@unittest.skipIf(LuaRuntime is None, 'requires lupa.lua51')
class EscortClientTests(unittest.TestCase):
    def test_no_guarantee_text_module_scope_and_restore(self):
        lua = LuaRuntime()
        lua.execute('''
         ms={d_petHomeUI={createShiLianLayer=function() end},
          d_secretAreaUI={},d_escortUI={},d_time={},
          d_hz={gethz=function(k,extra) return 'native:'..k..(extra or '') end}}
         escort=ms.d_escortUI;escort.d_ms=ms;originalMS=escort.d_ms
         -- The native module resolves d_ms through its Lua module environment.
         function chosenTip(key,remaining)
          return string.format(d_ms.d_hz.gethz(key),remaining)
         end
         setfenv(chosenTip, setmetatable(escort,{__index=_G}))
         package.loaded.ms=ms
        ''')
        source = Path('network_redirect/guild_activity_client.lua').read_text()
        lua.execute(source)
        lua.execute('''
         assert(chosenTip('book_tip28',4)=='还可刷新4次，品质随机')
         assert(chosenTip('book_tip282',0)=='刷新次数已用完，可运送当前经书')
         assert(chosenTip('book_tip284',0)=='仅随机刷新高四档，可降档、可重复，无保底')
         assert(chosenTip('book_tip281',0)=='已获得最高档经书')
         assert(chosenTip('book_tip283',0)=='已获得最高档经书')
         assert(escort.d_ms.d_hz.gethz('other','!')=='native:other!')
         assert(ms.d_hz.gethz('book_tip28')=='native:book_tip28')
         wrappedMS=escort.d_ms
        ''')
        lua.execute(source)
        lua.execute('''
         assert(escort.d_ms==wrappedMS)
         ms._localGuildActivitiesRestore()
         assert(escort.d_ms==originalMS)
         assert(chosenTip('book_tip28',4)=='native:book_tip28')
        ''')


if __name__ == '__main__':
    unittest.main()
