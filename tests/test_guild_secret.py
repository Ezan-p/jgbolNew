import copy
import unittest
from network_redirect import formation, guild, guild_combat, guild_instances, guild_offline, guild_secret, npc_players


class GuildSecretBalanceTests(unittest.TestCase):
    def test_invalid_quota_and_flat_or_decreasing_difficulty_rejected(self):
        for changes in (dict(search_per_layer=4,search_daily=12),
                        dict(secret_power_per_level_squared=0),
                        dict(secret_floor_percent=[100,110,120]),
                        dict(secret_floor_percent=[100,220,200]),
                        dict(secret_floor_percent=[100,220]),
                        dict(secret_floor_percent=[100,220,True])):
            rules=guild.load_rules();rules.update(changes)
            with self.assertRaises(formation.Rejected):guild_offline.validate_rules(rules)

    def test_all_levels_and_layers_have_strict_growth(self):
        rules=guild.load_rules()
        previous=0
        for level in range(20,500):
            powers=[guild_secret.target_power(level,f,rules) for f in (1,2,3)]
            self.assertGreater(powers[0],previous)
            self.assertGreaterEqual(powers[1],2*powers[0])
            self.assertGreaterEqual(powers[2],2*powers[1])
            previous=powers[0]
        self.assertEqual([guild_secret.target_power(100,f,rules) for f in (1,2,3)],
                         [1200000,2640000,6000000])

    def test_actual_units_scale_and_shared_npcs_are_immutable(self):
        rules=guild.load_rules()
        for level in (20,40,60,99,100,200,300,499):
            state={'instances':{},'random_serial':0}
            key=guild_secret.choose({'level':level},state,rules,[])
            npc=npc_players.get(key);snapshot=copy.deepcopy(npc)
            previous=None
            for floor in (1,2,3):
                units=guild_combat.player_units(npc['role'])
                skills=[copy.deepcopy({k:v for k,v in u.items() if k not in ('hp','max_hp','gongji','fangyu','magic')}) for u in units]
                detail=guild_secret.scale(units,level,floor,rules)
                self.assertEqual(len(units),8)
                self.assertLess(abs(detail['attribute_power']-detail['target_power']),70)
                self.assertEqual(skills,[{k:v for k,v in u.items() if k not in ('hp','max_hp','gongji','fangyu','magic')} for u in units])
                for i,u in enumerate(units):
                    self.assertEqual(u['hp'],u['max_hp'])
                    if previous:
                        for stat in ('hp','gongji','fangyu','magic'):
                            self.assertGreaterEqual(u[stat],2*previous[i][stat])
                previous=units
            self.assertEqual(npc,snapshot)
            self.assertEqual(npc_players.get(key),snapshot)

    def test_template_persistence_legacy_progress_and_day_reset(self):
        rules=guild.load_rules()
        state={'day':100,'random_serial':0}
        a=guild_instances.state(state)
        a.update(layer=1,search=2,team_fights=1,team_opponents={'0':'old_template'})
        key=guild_secret.choose({'level':80},state,rules,[])
        serial=state['random_serial']
        self.assertEqual(guild_secret.choose({'level':90},state,rules,[]),key)
        self.assertEqual(state['random_serial'],serial)
        self.assertEqual((a['layer'],a['search'],a['team_fights']),(1,2,1))
        state['day']+=1;guild_instances.state(state)
        self.assertNotIn('team_enemy_npc',a)
        self.assertEqual((a['layer'],a['search'],a['team_fights']),(0,0,0))
