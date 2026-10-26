"""Creation, real NPC admission, leader permissions and old-save migration."""
import copy
import unittest
from unittest.mock import patch

from network_redirect import guild, guild_npcs, npc_players
from network_redirect.protocol import encode, decode
from tests import test_guild as harness


class GuildNpcMemberTests(unittest.TestCase):
    setUp = harness.GuildTests.setUp
    req = harness.GuildTests.req
    ok = harness.GuildTests.ok
    role = harness.GuildTests.role
    create = harness.GuildTests.create

    def current(self):
        role = self.role()
        return role['guild']['unions'][str(role['union_id'])]

    def approve_all(self):
        ids = [int(k) for k in self.current()['applications']]
        for ident in ids:
            self.ok(5, role_id=ident)
        return ids

    def test_world_uses_unique_players_profiles(self):
        self.ok(18, query_type=4, page=1)
        rows = [m for g in self.role()['guild']['unions'].values() for m in g['members'].values()]
        self.assertEqual(len(rows), 13)
        self.assertEqual(len({m['id'] for m in rows}), 13)
        for m in rows:
            entry = npc_players.catalog()[npc_players.resolve(m['id'])]
            self.assertEqual((m['name'], m['head_type'], m['level'], m['combat_power']),
                             tuple(entry['profile'][key] for key in ('role_name', 'head_type', 'level', 'role_combat_power')))
            self.assertLessEqual(abs(m['level'] - 30), 2)

    def test_created_leader_receives_four_real_applications_and_can_fill_team(self):
        out = self.create()
        pending = self.current()['applications']
        self.assertEqual(len(pending), 4)
        notices = [data for mid, op, data in out if mid == 2998 and op == 82 and data.get('event_id') == 7]
        self.assertEqual({n['role_id'] for n in notices}, set(map(int, pending)))
        ids = self.approve_all()
        self.assertEqual(len(self.current()['members']), 5)
        self.assertFalse(self.current()['applications'])
        before = self.role()
        self.assertEqual(self.req(5, role_id=ids[0])[-1][1], 55)
        self.assertEqual(before, self.role())
        self.ok(26)
        self.ok(28, role_list=ids)
        self.assertEqual(len(self.role()['guild']['instances']['team']['members']), 5)
        # Canonical player IDs also support native player-profile inspection.
        self.serial += 1
        packets = self.b.respond(encode(1039, dict(serial_num=self.serial, des_type=1,
                                 des_id=ids[0], flag=6, fight_id=0)), {'authenticated': True})
        self.assertTrue(any(mid == 2998 and data['id'] == 11 for mid, _, data in map(decode, packets)))

    def test_leader_appointment_limits_mutes_transfer_and_leave(self):
        self.create()
        ids = self.approve_all()
        self.ok(11, role_id=ids[0], new_rank=7)
        before = self.role()
        self.assertEqual(self.req(11, role_id=ids[1], new_rank=7)[-1][1], 55)
        self.assertEqual(before, self.role())
        self.ok(11, role_id=ids[0], new_rank=5)
        self.ok(20, role_id=ids[0])
        self.assertEqual(self.current()['forbidden'][0]['id'], ids[0])
        self.ok(21, role_id=ids[0])
        self.assertFalse(self.current()['forbidden'])
        self.ok(20, role_id=ids[0]); self.ok(20, role_id=ids[1]); self.ok(22)
        self.assertFalse(self.current()['forbidden'])
        self.ok(20, role_id=ids[0])
        with patch('network_redirect.backend.time.time', return_value=harness.NOW + self.b.guild_rules['mute_seconds'] + 1):
            self.ok(18, query_type=3)
        self.assertFalse(self.current()['forbidden'])
        self.ok(12, role_id=ids[0])
        self.assertEqual(self.role()['union_rank'], 5)
        self.assertEqual([m['id'] for m in self.current()['members'].values() if m['rank'] == 1], [ids[0]])
        before = self.role()
        self.assertEqual(self.req(25, role_id=ids[1])[-1][1], 55)
        self.assertEqual(before, self.role())
        self.ok(3)
        self.assertEqual(self.role()['union_id'], 0)

    def test_leader_can_remove_members_disband_and_recreate(self):
        self.create()
        ids = self.approve_all()
        before = self.role()
        self.assertEqual(self.req(13)[-1][1], 55)
        self.assertEqual(before, self.role())
        for ident in ids:
            self.ok(25, role_id=ident)
        self.ok(13)
        self.create()
        self.assertEqual(len(self.current()['applications']), 4)

    def test_recruitment_persists_rejection_until_next_day_and_avoids_duplicates(self):
        self.create()
        initial = set(self.current()['applications'])
        for ident in initial:
            self.ok(6, role_id=int(ident))
        self.ok(18, query_type=5)
        self.assertFalse(self.current()['applications'])
        with patch('network_redirect.backend.time.time', return_value=harness.NOW + 86400):
            self.ok(18, query_type=5)
            pending = copy.deepcopy(self.current()['applications'])
            self.assertEqual(len(pending), 4)
            self.ok(18, query_type=5)
            self.assertEqual(pending, self.current()['applications'])
        world = self.role()['guild']
        all_ids = [m['id'] for g in world['unions'].values()
                   for section in ('members', 'applications') for m in g[section].values()]
        self.assertEqual(len(all_ids), len(set(all_ids)))

    def test_legacy_migration_preserves_player_progress_and_social_links(self):
        self.ok(4, union_id=1)
        role = self.role(); s = role['guild']; g = s['unions']['1']
        original_player = copy.deepcopy(g['members'][str(int(role['role_id']))])
        old_key = next(k for k, m in g['members'].items() if m.get('npc'))
        old = g['members'].pop(old_key)
        old.update(id=10001, name='本地盟主', rank=1, totalcontrib=777, contrib=123)
        g['members']['10001'] = old
        g['forbidden'] = [dict(old, expires=harness.NOW + 3600)]
        s['instances'] = dict(team=dict(captain=10001, members=['10001', str(int(role['role_id']))], applications={}), appoint=10001)
        s['escort'] = dict(requests=[10001], issued={'10001': 2}, active=dict(book=dict(protector_id=10001)))
        s.pop('npc_players_version')
        guild_npcs.migrate(role, s, harness.NOW)
        leader = next(m for m in g['members'].values() if m['rank'] == 1)
        self.assertIsNotNone(npc_players.resolve(leader['id']))
        self.assertEqual((leader['totalcontrib'], leader['contrib']), (777, 123))
        self.assertEqual(g['members'][str(int(role['role_id']))], original_player)
        self.assertEqual(s['instances']['team']['captain'], leader['id'])
        self.assertIn(str(leader['id']), s['instances']['team']['members'])
        self.assertEqual(s['instances']['appoint'], leader['id'])
        self.assertEqual(g['forbidden'][0]['id'], leader['id'])
        self.assertEqual(s['escort']['requests'], [leader['id']])
        self.assertEqual(s['escort']['issued'], {str(leader['id']): 2})
        self.assertEqual(s['escort']['active']['book']['protector_id'], leader['id'])
        saved = copy.deepcopy(role)
        guild_npcs.migrate(role, s, harness.NOW)
        self.assertEqual(role, saved)

    def test_delayed_legacy_acceptance_clears_other_guild_applications(self):
        self.b.guild_rules['npc_auto_accept']=False
        self.ok(18,query_type=4,page=1)
        role=self.role();rid=str(int(role['role_id']))
        application=dict(guild.offline.npc(int(rid),role['role_name'],harness.NOW),
                         npc=False,requested_at=harness.NOW-4)
        for key in ('1','80001'):
            role['guild']['unions'][key]['applications'][rid]=copy.deepcopy(application)
        self.b.save(role)
        self.ok(18,query_type=1)
        role=self.role()
        self.assertEqual(role['union_id'],1)
        self.assertTrue(all(rid not in g['applications'] for g in role['guild']['unions'].values()))
        self.assertEqual(role['guild']['join_count'],1)
        self.ok(3)
        with patch('network_redirect.backend.time.time',return_value=harness.NOW+10):
            self.ok(18,query_type=4,page=1)
        self.assertEqual(self.role()['union_id'],0)
        self.assertEqual(self.role()['guild']['join_count'],1)


if __name__ == '__main__':
    unittest.main()
