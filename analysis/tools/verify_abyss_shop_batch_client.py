"""Detached Lua 5.1 regression for the native Abyss shop quantity adapter."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from lupa.lua51 import LuaRuntime
from network_redirect import summon


def main():
    fixture = (ROOT / 'tests/abyss_shop_batch_client_regression.lua').read_text()
    patch = (ROOT / 'network_redirect/abyss_client.lua').read_text()
    try:
        LuaRuntime().execute(fixture, '')
    except Exception as exc:
        if 'all six slots must open a picker capped at 100' not in str(exc):
            raise
    else:
        raise AssertionError('Original native shop restriction must reproduce')
    print('Confirmed original slot restriction / 15-item batch limit')
    LuaRuntime().execute(fixture, patch)
    for name in ('abyss_client_regression', 'abyss_number_client_regression', 'abyss_success_client_regression'):
        source = (ROOT / f'tests/{name}.lua').read_text()
        LuaRuntime().execute(source, patch)
    LuaRuntime().execute('assert(loadstring(...))', summon.client_source(summon.load_rules()))
    print('Existing Abyss Lua regressions and complete client injection compile passed')


if __name__ == '__main__':
    main()
