"""Execute the fishing adapter in Lua 5.1 without a live game account."""
from pathlib import Path
import unittest

try:
    from lupa.lua51 import LuaRuntime
except ImportError:
    LuaRuntime = None


@unittest.skipIf(LuaRuntime is None, 'requires lupa.lua51')
class FishClientTests(unittest.TestCase):
    def test_preview_disabled_across_rebuilds_and_callbacks(self):
        lua = LuaRuntime()
        lua.execute('''
         nativePreviews=0;removed=0;staticCalls=0;children=0
         local function node()
          return {getContentSize=function() return {width=100,height=100} end,
           setPosition=function() end,setScaleX=function() end,setScaleY=function() end}
         end
         layer={unregisterScriptTouchHandler=function() removed=removed+1 end,
          setTouchEnabled=function(self,value) self.touch=value end,
          addChild=function() children=children+1 end}
         ui={g_FishRushUI={main_layer=layer},
          createStaticElements=function()
           staticCalls=staticCalls+1;layer.touch=true;return 'native-static'
          end,
          showPriceListInfo=function() nativePreviews=nativePreviews+1 end}
         originalPreview=ui.showPriceListInfo;originalStatic=ui.createStaticElements
         package.loaded.ms={d_fishRushUI=ui,d_u={},d_time={},d_hz={gethz=function() end}}
         CCDirector={sharedDirector=function()
          return {getVisibleSize=function() return {width=1280,height=720} end}
         end}
         CCLayerColor={create=node};CCSprite={create=node}
         ccc4=function() end;ccp=function() end
        ''')
        source = Path('network_redirect/fish_client.lua').read_text()
        lua.execute(source)
        lua.execute('''
         ui.showPriceListInfo();assert(nativePreviews==0 and children==0)
         for i=1,2 do
          assert(ui.createStaticElements()=='native-static')
          assert(layer.touch==false and removed==i and staticCalls==i)
          local before=children
          ui.showPriceListInfo();assert(nativePreviews==0 and children==before)
         end
         wrapped=ui.createStaticElements
        ''')
        lua.execute(source)
        lua.execute('''
         assert(ui.createStaticElements==wrapped)
         ui._localFishRestore()
         assert(ui.createStaticElements==originalStatic and ui.showPriceListInfo==originalPreview)
        ''')
