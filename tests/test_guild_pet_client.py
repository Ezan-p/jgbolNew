"""Run spirit-land task UI regressions with the Lua 5.1 adapter."""
import unittest
from pathlib import Path

try:
    from lupa.lua51 import LuaRuntime
except ImportError:
    LuaRuntime = None


@unittest.skipIf(LuaRuntime is None, 'requires lupa.lua51')
class GuildPetClientTests(unittest.TestCase):
    def test_task_completion_clicks_and_daily_refresh(self):
        LuaRuntime().execute(Path('tests/guild_pet_client_regression.lua').read_text())
