-- Detached Lua 5.1 contract fixture. Native upvalue identity and delayed button
-- callbacks are modeled; this does not claim an Android rendering test.
local patch=...
local MAX_JP=4
local ui={g_self={cort_id=1},character={id=1,fate_rebullding_jp_slots=1}}
local prices={100,300,700,1000}
ui.getCharInfoById=function(id) assert(id==1);return ui.character end
ui.showJPLockLayer=function(items)
 local locks={}
 local count=0
 local shown=MAX_JP
 local function toggle(pos)
  assert(pos<=shown and items[pos],'slot not shown')
  if count==MAX_JP-1 and not locks[pos] then return false end
  if locks[pos] then locks[pos]=nil;count=count-1 else locks[pos]=true;count=count+1 end
  return true
 end
 local function confirm()
  local positions={};for p in pairs(locks) do positions[#positions+1]=p end
  table.sort(positions)
  return positions,prices[count] or 0
 end
 return shown,toggle,confirm
end
package.loaded.ms={d_jpmkUI=ui}
local original=ui.showJPLockLayer
assert(loadstring(patch))()
local installed=ui.showJPLockLayer
assert(loadstring(patch))()
assert(ui.showJPLockLayer==installed,'patch not idempotent')
local shown,toggle,confirm=ui.showJPLockLayer({1,2,3,4,5})
assert(shown==5,'fifth slot not shown')
for _,p in ipairs({1,2,3,5}) do assert(toggle(p)) end
assert(not toggle(4),'five locks accepted')
local locks,cost=confirm()
assert(#locks==4 and locks[4]==5 and cost==1000,'delayed four-lock confirmation failed')
assert(toggle(5) and toggle(4))
locks,cost=confirm();assert(locks[4]==4 and cost==1000)
ui.character.fate_rebullding_jp_slots=0
shown,toggle,confirm=ui.showJPLockLayer({1,2,3,4})
assert(shown==4,'ordinary companion gained fifth slot')
for p=1,3 do assert(toggle(p)) end
assert(not toggle(4))
locks,cost=confirm();assert(#locks==3 and cost==700)
ui._localEssenceHotupdateRestore()
assert(ui.showJPLockLayer==original and MAX_JP==4)
return {'fifth slot display and selection','four locks cost 1000','fifth slot can be protected',
 'reject five locks','ordinary three locks cost 700','switch companion resets limit',
 'idempotent install','restore original upvalue and callback'}
