-- Run after installing the isolated land-fixture.lua; always restores its state.

local ms=package.loaded.ms
local output={}
local ok,err=xpcall(function()
 for i=1,19 do output[#output+1]=land_fixture_next() end
 local land=ms.d_landUI
 local old=land.g_self
 land.g_self={prey_info={max_level_score=3000,grid_count=8},charmList={}}
 local expected={3000,2850,2700,2580,2520,2400,2250,2100}
 local scores={}
 local score_ok,score_err=xpcall(function()
  for i=1,8 do assert(land.calcFightScore(i)==expected[i],'score mismatch '..i) end
  for i=1,44 do land.g_self.charmList[i]={key=i%4+1,unlock=true,is_open=true} end
  local value=3000
  for _,factor in ipairs({20,25,15,30}) do value=value-math.floor((11+11^1.2)*0.5*factor) end
  assert(land.calcFightScore(1)==math.max(0,value),'charm score mismatch')
 end,debug.traceback)
 land.g_self=old
 output[#output+1]='original_score: '..(score_ok and 'OK' or tostring(score_err))
 for _,v in ipairs(land_fixture_results) do assert(v.ok and v.error=='',v.name..': '..v.error) end
 assert(score_ok,score_err)
end,debug.traceback)
local restored,restore_err=pcall(land_fixture_restore)
output[#output+1]='restored: '..tostring(restored)
if not restored then output[#output+1]=tostring(restore_err) end
if not ok then output[#output+1]=tostring(err) end
return table.concat(output,'\n')
