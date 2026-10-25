-- Run in the game's Lua VM with adapter_source supplied by the harness.
local cases=0
local function check(v) assert(v);cases=cases+1 end
local chars={{reborn_layer=0},{reborn_layer=0,fate_rebullding_state=2}}
local ui={}
local original=function()
 table.sort(chars,function(a,b)
  if a.reborn_layer~=b.reborn_layer then return a.reborn_layer>b.reborn_layer end
  return a.fate_rebullding_state>b.fate_rebullding_state
 end)
 return chars
end
ui.getAscCorts=original
local ms={d_ascensionUI=ui,d_lineupUI={g_characterInfo=chars}}
local env=setmetatable({package={loaded={ms=ms}}},{__index=_G})
local function install() local f=assert(loadstring(adapter_source));setfenv(f,env);f() end
install()
check(ui.getAscCorts()==chars)
check(chars[1].fate_rebullding_state==2 and chars[2].fate_rebullding_state==0)
local wrapped=ui.getAscCorts;install();check(ui.getAscCorts==wrapped)
chars={{reborn_layer=1},{reborn_layer=0}}
ms.d_lineupUI.g_characterInfo=chars
check(ui.getAscCorts()[1].reborn_layer==1)
check(chars[1].fate_rebullding_state==0 and chars[2].fate_rebullding_state==0)
ui._localRebornRestore();check(ui.getAscCorts==original and ui._localRebornRestore==nil)
return 'passed '..cases..' client regression checks'
