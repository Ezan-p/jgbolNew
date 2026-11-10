"""Exercise the abyss keypad adapter and compile the production Lua 5.1 bundle."""
from pathlib import Path
import sys

from lupa.lua51 import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import summon


def main():
    fixture = (ROOT / 'tests/abyss_number_client_regression.lua').read_text()
    source = (ROOT / 'network_redirect/abyss_client.lua').read_text()
    try:
        LuaRuntime().execute(fixture, '')
    except Exception as exc:
        if 'two digits must remain visible' not in str(exc):
            raise
    else:
        raise AssertionError('Unpatched native keypad must reproduce the one-digit bug')
    print('Confirmed original one-digit failure')
    LuaRuntime().execute(fixture, source)
    for name in ('abyss_client_regression', 'abyss_success_client_regression'):
        LuaRuntime().execute((ROOT / f'tests/{name}.lua').read_text())
    LuaRuntime().execute('assert(loadstring(...))', summon.client_source(summon.load_rules()))
    print('Full client injection compiles in Lua 5.1')


if __name__ == '__main__':
    main()
