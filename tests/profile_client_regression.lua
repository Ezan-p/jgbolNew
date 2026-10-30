local source=...
local calls={}
local ui={showChangeUserHead=function(parent,zorder,tag,use_gold)
 calls[#calls+1]={parent=parent,zorder=zorder,tag=tag,use_gold=use_gold}
 return 'native portrait picker'
end}
local ms={d_runeUI=ui,d_data={g_new_config={}}}
package.loaded.ms=ms
local original=ui.showChangeUserHead
assert(loadstring(source))();assert(loadstring(source))()
ui.showChangeUserHead('parent',10,1,true)
assert(calls[#calls].use_gold==true) -- No server state: preserve native behavior.
ms.d_data.g_new_config.local_profile={head_free_available=true}
assert(ui.showChangeUserHead('parent',10,1,true)=='native portrait picker')
assert(calls[#calls].parent=='parent' and calls[#calls].zorder==10 and calls[#calls].tag==1)
assert(calls[#calls].use_gold==false) -- No 200-gold prompt or balance gate.
ms.d_data.g_new_config.local_profile={head_free_available=false}
ui.showChangeUserHead('parent',10,1,true)
assert(calls[#calls].use_gold==true)
ui.showChangeUserHead('parent',10,1)
assert(calls[#calls].use_gold==nil) -- Preserve the initial naming flow.
ui._localProfileRestore();assert(ui.showChangeUserHead==original)
return 'Profile client: free/paid selector, native arguments, initial choice, restoration passed'
