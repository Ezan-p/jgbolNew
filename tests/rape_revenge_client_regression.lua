-- Isolated model of native crossDoomUI L2290-2388: touch blocker precedes
-- skill lookup, and the confirmation button is created only after lookup.
local source=...
local ui,checks={},{}
local overlay,close,shown,notice,nativeCalls
local function check(name,fn) fn();checks[#checks+1]=name end
local function nativePrize(id,name)
 nativeCalls=nativeCalls+1
 overlay=true
 assert(id==101 or id==102,'skill lookup failed')
 shown={id=id,name=name}
 close=function() overlay=false end
 return 'native-prize'
end
local function nativeShow()
 local result=ui.g_last_rape_fight_ret
 if not result or result.result~=0 then return end
 for key,row in pairs(package.loaded.ms.d_messageUI.g_fightBackMssage.rape) do
  if key==result.request_id then ui.createBackSkillPrize(result.skill_type,row.name);break end
 end
end
ui.createBackSkillPrize=nativePrize
local ms={d_crossDoomUI=ui,d_messageUI={g_fightBackMssage={rape={}}},
 d_info={show=function(s) notice=s end}}
package.loaded.ms=ms
local function reset(result,messages)
 overlay=false;close=nil;shown=nil;notice=nil;nativeCalls=0
 ui.g_last_rape_fight_ret=result
 ui.g_last_rape_fight_back_id=701
 ms.d_messageUI.g_fightBackMssage.rape=messages or {[701]={skill_type=101,name='反击对手'}}
end
check('reproduce missing skill leaving an uncloseable blocker',function()
 reset({result=0,request_id=701})
 assert(not pcall(nativeShow))
 assert(overlay and not close)
end)
assert(loadstring(source))()
check('new response displays awarded skill and closes',function()
 reset({result=0,request_id=701,skill_type=102})
 nativeShow();assert(overlay and shown.id==102 and shown.name=='反击对手')
 assert(close);close();assert(not overlay)
end)
check('legacy response recovers exact message skill and closes',function()
 reset({result=0,request_id=701})
 nativeShow();assert(overlay and shown.id==101)
 close();assert(not overlay)
 assert(ui.g_last_rape_fight_ret.skill_type==nil,'do not mutate the response')
end)
check('string keys and numeric strings recover without choosing another message',function()
 reset({result=0,request_id=701},{['701']={skill_type='101'},[702]={skill_type=102}})
 assert(ui.createBackSkillPrize(nil,'对手')=='native-prize')
 assert(shown.id==101);close();assert(not overlay)
end)
check('missing or malformed message does not create a blocker',function()
 for _,messages in ipairs({{}, {[702]={skill_type=102}}, {[701]={}}, {[701]={skill_type=0}}}) do
  reset({result=0,request_id=701},messages)
  ui.createBackSkillPrize(nil,'对手')
  assert(nativeCalls==0 and not overlay and notice)
 end
 reset({result=0,request_id=701},{})
 for _,id in ipairs({0,-1,1.5,'bad'}) do ui.createBackSkillPrize(id,'对手') end
 assert(nativeCalls==0 and not overlay)
end)
check('loss and expired message never show victory dialog',function()
 reset({result=1,request_id=701,skill_type=101});nativeShow()
 assert(nativeCalls==0 and not overlay)
 reset({result=0,request_id=701,skill_type=101},{})
 nativeShow();assert(nativeCalls==0 and not overlay)
end)
check('install is idempotent and restore returns native dialog',function()
 local wrapped=ui.createBackSkillPrize
 assert(loadstring(source))();assert(ui.createBackSkillPrize==wrapped)
 ui._localRapeRestore();assert(ui.createBackSkillPrize==nativePrize)
end)
return checks
