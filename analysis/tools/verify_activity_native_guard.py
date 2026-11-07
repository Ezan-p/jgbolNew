"""Run the actual C readiness guard against Lua 5.1 states on the host."""
import ctypes
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), '/private/tmp/jgbol-wait-test-deps']
from lupa import lua51
from tests.test_activity_entry_client import FIXTURE
from network_redirect.summon import client_source, load_rules


def main():
    source = (ROOT / 'offline_android/native/offline.c').read_text()
    guard = source[source.index('static int activity_patch_current('):source.index('static int offline_pcall(')]
    declarations = '''#include <string.h>
#include <dlfcn.h>
typedef void lua_State; typedef unsigned int u32;
static int (*lua_gettop_)(lua_State *);
static void (*lua_settop_)(lua_State *, int);
static void (*lua_getfield_)(lua_State *, int, const char *);
static int (*lua_type_)(lua_State *, int);
static int (*lua_pcall_original)(lua_State *, int, int, int);
static const char *(*lua_tolstring_)(lua_State *, int, u32 *);
'''
    footer = '''
void initialize(void *lib) {
 lua_gettop_=dlsym(lib,"lua_gettop");lua_settop_=dlsym(lib,"lua_settop");
 lua_getfield_=dlsym(lib,"lua_getfield");lua_type_=dlsym(lib,"lua_type");
 lua_pcall_original=dlsym(lib,"lua_pcall");lua_tolstring_=dlsym(lib,"lua_tolstring");
}
int check(lua_State *state) {
 int before=lua_gettop_(state), result=client_patches_current(state);
 return lua_gettop_(state)==before ? result : -1;
}
'''
    with tempfile.TemporaryDirectory() as temp:
        c = Path(temp) / 'guard.c'; dylib = Path(temp) / 'guard.dylib'
        c.write_text(declarations + guard + footer)
        subprocess.run(['/usr/bin/clang', '-dynamiclib', '-Wall', '-Wextra', '-Werror',
                        str(c), '-o', str(dylib)], check=True)
        lua = ctypes.CDLL(lua51.__file__)
        native = ctypes.CDLL(str(dylib))
        native.initialize.argtypes = [ctypes.c_void_p]; native.initialize(lua._handle)
        native.check.argtypes = [ctypes.c_void_p]; native.check.restype = ctypes.c_int
        lua.luaL_newstate.restype = ctypes.c_void_p
        lua.luaL_openlibs.argtypes = [ctypes.c_void_p]
        lua.luaL_loadstring.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        lua.lua_pcall.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        lua.lua_tolstring.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
        lua.lua_tolstring.restype = ctypes.c_char_p
        lua.lua_close.argtypes = [ctypes.c_void_p]
        state = lua.luaL_newstate(); lua.luaL_openlibs(state)
        def execute(text):
            code = lua.luaL_loadstring(state, text.encode())
            if not code: code = lua.lua_pcall(state, 0, 0, 0)
            assert code == 0, lua.lua_tolstring(state, -1, None)
        checks = []
        def check(name, expected):
            value = native.check(state)
            assert value == expected, (name, value, expected)
            checks.append(dict(name=name, ready=bool(value), stack_preserved=True))
        bundle = client_source(load_rules())
        def reset():
            execute(FIXTURE)
            execute("package.loaded['ui.summonUI']={_localGoldRestore=function() end}")
            execute(bundle)
        try:
            check('prelogin', 0)
            reset(); check('all_critical_adapters_installed', 1)
            execute('ms.d_funUI.getFunList=function() return {{id=40},{id=48},{id=46}} end')
            check('in_place_entry_reload_despite_summon_marker', 0)
            execute(bundle); check('entry_reinstalled', 1)
            execute('ms.d_twoYearsCelebrateUI.canJoin=function() return false end')
            check('in_place_yuanshi_reload_despite_summon_marker', 0)
            execute(bundle); check('yuanshi_reinstalled', 1)
            execute('ms.d_funUI={}')
            check('replaced_activity_module', 0)
            reset(); execute('ms.d_data={}')
            check('replaced_config_module', 0)
            reset(); execute("ms.d_funUI._localActivityEntryCurrent=function() error('probe failure') end")
            check('guard_exception_balanced_and_not_ready', 0)
            reset(); execute("package.loaded['ui.summonUI']={}")
            check('summon_reload', 0)
            reset(); execute('package.loaded.ms=nil')
            check('logout', 0)
            reset(); check('relogin', 1)
        finally:
            lua.lua_close(state)
    report = dict(passed=True, checks=checks, native_source_sha256=hashlib.sha256(source.encode()).hexdigest(),
                  scope='Exact C guard compiled for host with real Lua 5.1; Android ARM binary is rebuilt separately')
    out = ROOT / 'analysis/evidence/v110/activity-entry-fix-20261106/native-guard-validation.json'
    out.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
