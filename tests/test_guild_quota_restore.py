import unittest
from network_redirect import guild,guild_hunt,guild_instances
class RestoredWanderTests(unittest.TestCase):
 def test_restored_quota_is_floor_not_extra_task_reward(self):
  r=guild.load_rules();a=dict(tasks=[],paid_tasks=0,wander=0,restored_wander_limit=6)
  self.assertEqual(guild_hunt.wander_capacity(a,r),6)
  a.update(tasks=[1,2,3],paid_tasks=3,wander=6)
  self.assertEqual(guild_hunt.wander_capacity(a,r)-a['wander'],0)
 def test_restore_expires_on_daily_rollover(self):
  s=dict(day=100,instances=dict(day=99,restored_wander_limit=6))
  a=guild_instances.state(s)
  self.assertEqual(a['restored_wander_limit'],0)
 def test_normal_task_entitlements_unchanged(self):
  r=guild.load_rules();a=dict(tasks=[1,2],paid_tasks=1)
  self.assertEqual(guild_hunt.wander_capacity(a,r),r['wander_daily']+3)
