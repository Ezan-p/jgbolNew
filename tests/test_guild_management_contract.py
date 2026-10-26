"""Native management buttons send bulk lists, including full NPC role IDs."""
import unittest
from tests import test_guild as base


class GuildManagementContractTests(unittest.TestCase):
    setUp=base.GuildTests.setUp
    req=base.GuildTests.req
    role=base.GuildTests.role
    create=base.GuildTests.create
    ok=base.GuildTests.ok

    def applicants(self):
        self.create()
        return list(map(int,self.role()['guild']['unions']['2']['applications']))

    def test_native_bulk_accept_and_unmute(self):
        ids=self.applicants();self.assertEqual(len(ids),4)
        self.ok(5,role_list=ids)
        g=self.role()['guild']['unions']['2']
        self.assertEqual(len(g['members']),5)
        self.assertFalse(g['applications'])
        for ident in ids:self.ok(20,role_id=ident)
        self.assertEqual(len(self.role()['guild']['unions']['2']['forbidden']),4)
        self.ok(21,role_list=ids)
        self.assertFalse(self.role()['guild']['unions']['2']['forbidden'])

    def test_native_bulk_reject_and_invalid_selections_are_atomic(self):
        ids=self.applicants()
        for selection in (ids+[99999],ids+[ids[0]],[True],{2:ids[0]},[]):
            before=self.role()
            self.assertEqual(self.req(5,role_list=selection)[-1][1],55)
            self.assertEqual(self.role(),before)
        self.ok(6,role_list=ids[:2])
        self.assertEqual(set(self.role()['guild']['unions']['2']['applications']),set(map(str,ids[2:])))
        self.ok(24)
        self.assertFalse(self.role()['guild']['unions']['2']['applications'])

    def test_native_transfer_keeps_exactly_one_leader(self):
        ids=self.applicants();self.ok(5,role_list=ids)
        self.ok(11,role_id=ids[0],new_rank=1)
        role=self.role();g=role['guild']['unions']['2']
        self.assertEqual(role['union_rank'],5)
        self.assertEqual([m['id'] for m in g['members'].values() if m['rank']==1],[ids[0]])
        before=self.role()
        self.assertEqual(self.req(11,role_id=ids[1],new_rank=1)[-1][1],55)
        self.assertEqual(self.role(),before)
        self.ok(3);self.assertEqual(self.role()['union_id'],0)

    def test_accept_full_selection_keeps_waiting_members(self):
        ids=self.applicants()
        self.b.guild_rules['member_limit']=3
        self.ok(5,role_list=ids)
        g=self.role()['guild']['unions']['2']
        self.assertEqual(len(g['members']),3)
        self.assertEqual(set(g['applications']),set(map(str,ids[2:])))
        before=self.role()
        self.assertEqual(self.req(5,role_list=ids[2:])[-1][1],55)
        self.assertEqual(self.role(),before)


if __name__=='__main__':unittest.main()
