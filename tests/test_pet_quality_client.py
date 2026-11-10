"""Lua 5.1 adapter parity with server probabilities, including native upvalues."""
from pathlib import Path
import unittest
from network_redirect import pets, summon
try:
    from lupa.lua51 import LuaRuntime
except ImportError:
    LuaRuntime = None


@unittest.skipIf(LuaRuntime is None, 'requires lupa.lua51')
class PetQualityClientTests(unittest.TestCase):
    def setUp(self):
        self.lua = LuaRuntime()
        self.source = Path('network_redirect/pet_client.lua').read_text()
        self.lua.globals().nativeProbabilities = lambda main, quality, value: self.lua.table_from(
            dict.fromkeys(range(1, 5), 0) | pets.fusion_probabilities(main, quality, value))
        self.lua.execute('''
         local g_petUI={curPet={star_level=0}}
         state=g_petUI
         local getResultExpection=function(main,quality,value)
          assert(g_petUI.curPet)
          raw=nativeProbabilities(main,quality,value)
          return raw
         end
         originalExpectation=getResultExpection
         pet={pet_is_open=false,canJoin=function() return false end,
          showFusionLayer=function(...) return getResultExpection(...) end}
         profile={showPlayerInfoLayer=function() return pet.pet_is_open end}
         originalProfile=profile.showPlayerInfoLayer
         package.loaded.ms={d_petUI=pet,d_runeUI=profile}
        ''')
        self.lua.execute(self.source)

    def test_preview_matches_server_all_valid_quality_star_combinations(self):
        for main in (1, 2):
            for quality in range(1, 5):
                for star in range(int(pets.CONTROL[main, quality]['max_star_level'])+1):
                    for value in (0, 3, 24, 210, 1200, 7200, 45000):
                        self.lua.globals().state.curPet.star_level = star
                        actual = self.lua.globals().pet.showFusionLayer(main, quality, value)
                        expected = pets.effective_fusion_probabilities(main, quality, value, star)
                        self.assertAlmostEqual(sum(actual.values()), 1)
                        for q in range(1, 5):
                            self.assertAlmostEqual(actual[q] or 0, expected.get(q, 0))
                        raw = self.lua.globals().raw
                        for q, chance in pets.fusion_probabilities(main, quality, value).items():
                            self.assertEqual(raw[q], chance)

    def test_idempotent_restore_and_entry_gate(self):
        self.lua.execute('savedRestore=pet._localPetRestore; savedProfile=profile.showPlayerInfoLayer')
        self.lua.execute(self.source)
        self.lua.execute('''
         assert(savedRestore==pet._localPetRestore and savedProfile==profile.showPlayerInfoLayer)
         assert(profile.showPlayerInfoLayer() and not pet.canJoin())
         state.curPet.star_level=1
         local result=pet.showFusionLayer(1,3,3);assert(result[2]==0)
         pet._localPetRestore()
         assert(profile.showPlayerInfoLayer==originalProfile and not pet.pet_is_open)
         assert(not pet._localPetFusionRestore and not pet._localPetRestore)
         assert(pet.showFusionLayer(1,3,3)[2]>0.5)
        ''')
        self.lua.execute(self.source)
        self.lua.execute('assert(pet.showFusionLayer(1,3,3)[2]==0)')

    def test_missing_fusion_dependencies_can_retry_after_entry_install(self):
        self.lua.execute('pet._localPetRestore(); savedFusion=pet.showFusionLayer; pet.showFusionLayer=nil')
        self.assertEqual(self.lua.execute(self.source), 'pending')
        self.lua.execute('pet.showFusionLayer=savedFusion')
        self.lua.execute(self.source)
        self.lua.execute('state.curPet.star_level=1; assert(pet.showFusionLayer(1,3,3)[2]==0)')

    def test_full_client_source_compiles_and_legacy_entry_regression(self):
        self.lua.globals().source = summon.client_source(summon.load_rules())
        self.lua.execute('assert(loadstring(source))')
        LuaRuntime().execute(Path('tests/pet_client_regression.lua').read_text())
