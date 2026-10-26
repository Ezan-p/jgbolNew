"""Current offline entry policy, including requests sent by stale clients."""
import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from network_redirect import guild, guild_combat, guild_match, journey, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode, encode

NOW = 1792728000


class GuildAccessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.addCleanup(self.b.close)
        clock = patch('network_redirect.backend.time.time', return_value=NOW)
        clock.start(); self.addCleanup(clock.stop)
        self.serial = 24000
        role = self.b.profile()
        role.update(level=50, gold_coin=10000)
        self.b.save(role)
        self.send(1301, id=1, data=summon.lua(dict(union_name='入口验证盟')))

    def send(self, mid, **data):
        self.serial += 1
        self.packet = encode(mid, dict(serial_num=self.serial, **data))
        self.replies = self.b.respond(self.packet, {'authenticated': True})
        return [(m, d) for m, _, d in map(decode, self.replies)]

    def rejected(self, mid, **data):
        before = self.b.profile()
        rows = self.send(mid, **data)
        errors = [login_fields(d['data']) for m, d in rows if m==2998 and d['id']==55]
        self.assertEqual(errors, [{'op_string': guild.WAR_CLOSED}])
        self.assertFalse(any(m in (1301, 1027, 1028) for m, _ in rows))
        self.assertEqual(self.b.profile(), before)
        self.assertEqual(self.b.respond(self.packet, {'authenticated': True}), self.replies)
        self.assertEqual(self.b.profile(), before)

    def test_wars_reject_every_query_mutation_and_binary_battle(self):
        self.assertFalse(self.b.guild_rules['wars_enabled'])
        for op in sorted(guild.WAR_OPS):
            self.rejected(1301, id=op, data=summon.lua(dict(query_type=34, index=1, count=1, bet_type=1, union_id=2)))
        for q in sorted(guild.WAR_QUERIES):
            self.rejected(1301, id=18, data=summon.lua(dict(query_type=q)))
        for q in (20,21,22,23,24,25,26,27,28,29,30,31,32,33,34):
            self.rejected(1301, id=58, data=summon.lua(dict(query_type=q,des_id=90001)))
        for ft in guild.WAR_FIGHTS:
            self.rejected(1026, fight_type=ft, des_type=1, des_id=90001, des_value=0, fight_id=0)

    def test_nonmember_cannot_enter_public_war_routes(self):
        self.send(1301, id=13, data='{}')
        for op, q in ((18,9), (58,20), (18,100)):
            self.rejected(1301, id=op, data=summon.lua(dict(query_type=q)))

    def test_icons_remain_visible_but_hints_and_rollover_are_disabled(self):
        r = self.b.guild_rules
        config = guild.client_config(r)['const_config']
        self.assertEqual((config['open_union_match'], config['open_world_match']), (1,1))
        role = self.b.profile(); s, g = guild.prepare(role, NOW, r)
        hints = guild.member(role, g, r)
        for key in ('can_match_fight','has_action_point','is_match_time','is_bet_time','has_bet','cross_fight_flag','can_rece_award'):
            self.assertFalse(hints[key], key)
        s['match'] = dict(day=s['day']-1, fights=1, bets={'1':2}, claimed=False)
        before = copy.deepcopy(role)
        guild_match.rollover(role, NOW, r)
        self.assertEqual(role, before)

    def test_tree_replay_uses_original_guardian_and_requested_fallback(self):
        for missing, expected, name in ((False,9001,'仙盟守护树'), (True,4015,'乌巢禅师')):
            with self.subTest(missing=missing):
                npcs = dict(journey.NPCS)
                if missing: npcs.pop(9001)
                role = self.b.profile()
                role['guild']['unions']['2']['tree'].update(state=3,hp=10000)
                self.b.save(role)
                with patch.object(journey, 'NPCS', npcs):
                    rows = self.send(1026, fight_type=13, des_type=1, des_id=0, des_value=0, fight_id=0)
                lineup = next(d for m,d in rows if m==1028)
                self.assertEqual(lineup['des_name'], name)
                self.assertEqual([v['des_type'] for v in lineup['lineup'] if v['des_type']], [expected])
                self.assertTrue(next(d for m,d in rows if m==1027)['fight_result'])
                # Reset the temporary cooldown for the next independent case.
                role=self.b.profile();role['guild']['unions']['2']['tree']['cooltime']=0;self.b.save(role)

    def test_trial_boss_is_a_five_star_god(self):
        role=self.b.profile();s,g=guild.prepare(role,NOW,self.b.guild_rules)
        _,_,replay=guild_combat.simulate(role,s,self.b.guild_rules,self.b.journey_rules,27,'灵兽试炼')
        tid=replay['line_up_msg']['lineup'][0]['des_type']
        self.assertTrue(5000<=tid<6000)
        self.assertEqual(int(summon.BASES[tid]['quality']),5)
