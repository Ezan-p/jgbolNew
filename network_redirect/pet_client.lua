-- Restore the original profile-page pet entry independently of welfare queries.
do
 local ms=package.loaded.ms
 local pet=ms and ms.d_petUI
 local profile=ms and ms.d_runeUI
 if not pet or not profile or not profile.showPlayerInfoLayer then return 'pending' end
 if not pet._localPetRestore then
  local show=profile.showPlayerInfoLayer
  local wasOpen=pet.pet_is_open
  pet.pet_is_open=true
  profile.showPlayerInfoLayer=function(...)
   -- actNoticeUI may reset the flag when receiving a partial activity response.
   pet.pet_is_open=true
   return show(...)
  end
  pet._localPetRestore=function()
   profile.showPlayerInfoLayer=show;pet.pet_is_open=wasOpen
   pet._localPetRestore=nil
  end
 end
 -- Native showFusionLayer closes over getResultExpection, which reads the live
 -- selected pet and invokes the original mathProcess. Keep that formula intact.
 if not pet._localPetFusionRestore then
  if not pet.showFusionLayer or not debug or not debug.getupvalue or not debug.setupvalue then return 'pending' end
  local function up(fn,key)
   for i=1,100 do
    local name,value=debug.getupvalue(fn,i)
    if not name then break end
    if name==key then return value,i end
   end
  end
  local original,index=up(pet.showFusionLayer,'getResultExpection')
  if type(original)~='function' or type(up(original,'g_petUI'))~='table' then return 'pending' end
  local showFusion=pet.showFusionLayer
  local function preview(...)
   local probabilities=original(...)
   local state=up(original,'g_petUI')
   local star=state and state.curPet and state.curPet.star_level or 0
   local minimum=star>6 and 4 or star>0 and 3 or 1
   local result={}
   for quality,chance in pairs(probabilities) do
    result[quality]=result[quality] or 0
    local target=math.max(quality,minimum)
    result[target]=(result[target] or 0)+chance
   end
   return result
  end
  debug.setupvalue(showFusion,index,preview)
  local restore=pet._localPetRestore
  pet._localPetFusionRestore=function()
   debug.setupvalue(showFusion,index,original)
   pet._localPetFusionRestore=nil
  end
  pet._localPetRestore=function()
   if pet._localPetFusionRestore then pet._localPetFusionRestore() end
   restore()
  end
 end
end
