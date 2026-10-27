"""Isolated Lua 5.1 tests for complete replay transport and draw results.

Requires lupa.lua51; native Cocos verification is performed separately.
"""
import json
from pathlib import Path
from lupa.lua51 import LuaRuntime

ROOT=Path(__file__).resolve().parents[2]
source=(ROOT/'network_redirect/battle_replay_client.lua').read_text()
harness=(ROOT/'tests/battle_replay_client_regression.lua').read_text()
checks=LuaRuntime().execute(harness,source).splitlines()
print(json.dumps(dict(passed=True,checks=checks,native_cocos=False),ensure_ascii=False,indent=2))
