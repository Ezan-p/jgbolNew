"""Opt-in live integration test: a separate Lua state, never the game's state.

Run from the project root with .runtime/venv/bin/python -m
observability.tests.live_lua_smoke while the game and frida-server are running.
"""
import json
from pathlib import Path
import time

from android_emulator.config import load_config
from android_emulator.manager import ready_device
from observability.collector import FridaCollector, processes
from observability.events import SessionWriter

SMOKE = r'''
rpc.exports.smoke = function () {
    const m = Process.getModuleByName('libxiyoujilua.so');
    const fn = (name, result, args) => new NativeFunction(m.getExportByName(name), result, args);
    const create = fn('luaL_newstate', 'pointer', []);
    const openlibs = fn('luaL_openlibs', 'void', ['pointer']);
    const load = fn('luaL_loadbuffer', 'int', ['pointer', 'pointer', 'uint', 'pointer']);
    const pcall = fn('lua_pcall', 'int', ['pointer', 'int', 'int', 'int']);
    const top = fn('lua_gettop', 'int', ['pointer']);
    const reset = fn('lua_settop', 'void', ['pointer', 'int']);
    const close = fn('lua_close', 'void', ['pointer']);
    const L = create();
    if (L.isNull()) throw new Error('Could not allocate independent Lua state');
    const results = {};
    try {
        openlibs(L);
        results.initialTop = top(L);
        const code = 'print("JGBOL_OBSERVER_SMOKE", 42, true, nil); error("expected observer smoke error")';
        results.load = load(L, Memory.allocUtf8String(code), code.length,
                           Memory.allocUtf8String('@observer-smoke.lua'));
        results.call = pcall(L, 0, 0, 0);
        results.errorTop = top(L);
        reset(L, 0);
        const invalid = 'local =';
        results.invalidLoad = load(L, Memory.allocUtf8String(invalid), invalid.length,
                                  Memory.allocUtf8String('@observer-invalid.lua'));
        results.invalidTop = top(L);
    } finally { close(L); }
    flush();
    return results;
};
'''


def main():
    config = load_config(Path(__file__).resolve().parents[2] / 'game.json')
    ready_device(config)
    pid = next(p for p, name in processes(config).items() if name == config['package'])
    writer = SessionWriter(config['runtime_dir'] / 'observations',
                           dict(mode='isolated_lua_smoke', package=config['package'], serial=config['serial']))
    collector = None
    try:
        collector = FridaCollector(config, writer)
        collector.source += SMOKE
        collector.attach(pid)
        result = collector.script.exports_sync.smoke()
        assert result == dict(initialTop=0, load=0, call=2, errorTop=1, invalidLoad=3, invalidTop=1), result
        expected = {'lua_print', 'lua_load', 'lua_pcall_error', 'lua_load_error'}
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            rows = [json.loads(line) for line in (writer.directory / 'events.jsonl').read_text().splitlines()]
            if expected <= {row['kind'] for row in rows}:
                break
            time.sleep(.05)
        else:
            raise AssertionError('Missing runtime hook events')
        printed = next(row['message'] for row in rows if row['kind'] == 'lua_print' and
                       row['message'].startswith('JGBOL_OBSERVER_SMOKE'))
        assert printed == 'JGBOL_OBSERVER_SMOKE\t42\ttrue\tnil', printed
        chunks = [row.get('chunk') for row in rows if row['kind'] == 'lua_load']
        assert '@observer-smoke.lua' in chunks and '@observer-invalid.lua' in chunks, chunks
        writer.emit(dict(kind='smoke_passed', message='独立 Lua state 实测通过', results=result))
        print('验证记录：' + str(writer.directory))
    finally:
        if collector:
            collector.close()
        writer.close()


if __name__ == '__main__':
    main()
