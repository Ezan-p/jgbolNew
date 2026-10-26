local seen, calls=false,0
local pet={pet_is_open=false,canJoin=function() return false end}
local original=function(arg) seen=pet.pet_is_open;calls=calls+1;return arg end
local profile={showPlayerInfoLayer=original}
package.loaded.ms={d_petUI=pet,d_runeUI=profile}
dofile('network_redirect/pet_client.lua')
local wrapper=profile.showPlayerInfoLayer
dofile('network_redirect/pet_client.lua');assert(wrapper==profile.showPlayerInfoLayer)
pet.pet_is_open=false
assert(profile.showPlayerInfoLayer(42)==42 and seen and calls==1)
assert(not pet.canJoin(),'original level gate must remain unchanged')
pet._localPetRestore()
assert(profile.showPlayerInfoLayer==original and pet.pet_is_open==false)
print('pet entry regression passed')
