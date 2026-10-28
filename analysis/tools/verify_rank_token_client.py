"""Check token batching and the production injection with Lua 5.1 (lupa)."""
from pathlib import Path
import sys

from lupa.lua51 import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import summon, activity_rank as rank

vm = LuaRuntime()
print(vm.execute((ROOT / 'tests/rank_token_client_regression.lua').read_text(),
                 rank.client_source()))
vm.execute('assert(loadstring(...))', summon.client_source(summon.load_rules()))
print('Full client injection compiles in Lua 5.1')
