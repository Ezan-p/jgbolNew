-- Native keypad/reset/confirm contracts from abyssUI L3702-3787.
-- Exercise button callbacks, displayed text and outgoing values together.
local source=...
local sent,notices,buttons={}, {}, {}
local ms={d_u={},d_abyssUI={g_self={}},d_info={}}
local ui=ms.d_abyssUI
package.loaded.ms=ms
ui.sendRequest=function(op,data) sent[#sent+1]={op=op,data=data} end
ms.d_info.show=function(message) notices[#notices+1]=message end
ms.d_u.createMenu=function(config)
 for _,row in ipairs(config) do buttons[row.tag or row.npic]=row.call_back end
 return config
end
-- Required by the existing boss adapter; unused in this fixture.
ui.showBossLayer=function() end
local frame
local function setNumString(node,text)
 node.text=text;ui.g_self.curNumStr=text
end
ui.showNumberGuess=function()
 local data=ui.g_data.random
 if data.is_win or data.left_times==0 then return 'finished' end
 local floor,ceil=data.min_num or 10,data.max_num or 40
 local numCount=#tostring(floor) -- Reproduce the shipped defect.
 frame={};ui.g_self.input_time=0
 setNumString(frame,numCount==3 and '000' or '00')
 local function pressReenter()
  ui.g_self.input_time=0
  setNumString(frame,numCount==3 and '000' or '00')
 end
 local function pressNum(num)
  if ui.g_self.input_time>=numCount then ms.d_info.show('full');return end
  local str=ui.g_self.curNumStr..tostring(num)
  local numStr=string.sub(str,2,#str)
  setNumString(frame,numStr)
  ui.g_self.input_time=ui.g_self.input_time+1
  local value=tonumber(numStr)
  if ui.g_self.input_time==numCount and (value<=floor or value>=ceil) then
   pressReenter();ms.d_info.show('range')
  end
 end
 for num=0,9 do
  ms.d_u.createMenu({{tag=num,npic='v2/abyssUI/randomEvent/num_btn1.png',call_back=pressNum}})
 end
 local function confirm()
  local num=tonumber(ui.g_self.curNumStr)
  if num>ceil or num<floor then ms.d_info.show('range');pressReenter();return end
  ui.sendRequest(4,{op_type=1,num=num})
 end
 ms.d_u.createMenu({
  {npic='v2/abyssUI/randomEvent/reenter1.png',call_back=pressReenter},
  {npic='v2/abyssUI/randomEvent/ensure1.png',call_back=confirm}})
 if data.render_error then error('render failure') end
 return 'rendered'
end
local native,create=ui.showNumberGuess,ms.d_u.createMenu
local function install() assert(loadstring(source))() end
install()
local wrapper=ui.showNumberGuess
install();assert(ui.showNumberGuess==wrapper,'repeated installation')
local function show(minimum,maximum,extra)
 buttons={};ui.g_data={random=extra or {min_num=minimum,max_num=maximum,left_times=4}}
 assert(ui.showNumberGuess()=='rendered')
 assert(ms.d_u.createMenu==create,'menu helper must be restored')
end
local function press(text)
 for digit in text:gmatch('.') do local n=tonumber(digit);buttons[n](n) end
end
local function reset() buttons['v2/abyssUI/randomEvent/reenter1.png']() end
local function confirm(expected)
 local before=#sent
 buttons['v2/abyssUI/randomEvent/ensure1.png']()
 assert(#sent==before+1 and sent[#sent].op==4)
 assert(sent[#sent].data.num==expected and sent[#sent].data.op_type==1)
end
-- Fresh event and redraws after either bound changes.
for _,range in ipairs({{0,100},{9,100},{9,80},{10,100},{50,100}}) do
 show(range[1],range[2]);press('72')
 assert(frame.text=='72' and ui.g_self.input_time==2,'two digits must remain visible')
 confirm(72)
 local count=#notices;press('3');assert(frame.text=='72' and #notices==count+1)
 reset();assert(frame.text=='00' and ui.g_self.input_time==0)
 press('75');confirm(75)
end
show(0,100);press('7');confirm(7) -- Native confirm still accepts single digits.
reset();press('07');confirm(7)
reset();press('00');assert(frame.text=='00' and ui.g_self.input_time==0)
show(9,80);press('80');assert(ui.g_self.input_time==0)
press('09');assert(ui.g_self.input_time==0)
press('79');confirm(79)
show(0,10);press('09');confirm(9)
show(99,1000);assert(frame.text=='000');press('123');confirm(123)
reset();assert(frame.text=='000');press('999');confirm(999)
show(0,100);assert(frame.text=='00','width must reset after three-digit event')
local before=#sent
ui.g_data.random={is_win=true};assert(ui.showNumberGuess()=='finished')
ui.g_data.random={left_times=0};assert(ui.showNumberGuess()=='finished')
assert(#sent==before and ms.d_u.createMenu==create)
ui.g_data.random={min_num=0,max_num=100,render_error=true}
assert(not pcall(ui.showNumberGuess));assert(ms.d_u.createMenu==create)
ui._localAbyssNumberRestore();assert(ui.showNumberGuess==native)
install();assert(ui.showNumberGuess~=native)
print('abyss number regression OK: multi-digit input, redraws, reset, range validation, requests, restore')
