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
end
