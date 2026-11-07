"""Exercise the shipped C loader against real Lua 5.1 with a controlled clock."""
import ctypes
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,'/private/tmp/jgbol-wait-test-deps')
from lupa import lua51

def main():
 source=(ROOT/'offline_android/native/offline.c').read_text()
 body=source[source.index('static int activity_patch_current('):source.index('static void branch(')]
 pre=r'''
#include <string.h>
#include <dlfcn.h>
#include <stdarg.h>
typedef void lua_State; typedef unsigned int u32;
struct timespec32 { int sec; int nsec; };
static u32 now_ms, previous_ms; static int evaluating, lua_ready, lua_failed;
static char *patch_source; static u32 patch_size;
static int messages;
static void log_message(const char *format, ...) { (void)format; messages++; }
#define LOG(...) log_message(__VA_ARGS__)
#define ERR(...) log_message(__VA_ARGS__)
static int test_clock(int id, struct timespec32 *t) {
 (void)id;t->sec=now_ms/1000;t->nsec=(now_ms%1000)*1000000;return 0;
}
#define clock_gettime test_clock
static int (*lua_gettop_)(lua_State *);
static void (*lua_settop_)(lua_State *, int);
static void (*lua_getfield_)(lua_State *, int, const char *);
static int (*lua_type_)(lua_State *, int);
static int (*lua_pcall_original)(lua_State *, int, int, int);
static int (*luaL_loadbuffer_)(lua_State *, const char *, u32, const char *);
static const char *(*lua_tolstring_)(lua_State *, int, u32 *);
'''
 footer=r'''
void initialize(void *lib, char *code) {
 lua_gettop_=dlsym(lib,"lua_gettop");lua_settop_=dlsym(lib,"lua_settop");
 lua_getfield_=dlsym(lib,"lua_getfield");lua_type_=dlsym(lib,"lua_type");
 lua_pcall_original=dlsym(lib,"lua_pcall");lua_tolstring_=dlsym(lib,"lua_tolstring");
 luaL_loadbuffer_=dlsym(lib,"luaL_loadbuffer");
 patch_source=code;patch_size=strlen(code);
}
int invoke(lua_State *state, unsigned int ms) {now_ms=ms;return offline_pcall(state,0,1,0);}
int failed(void) {return lua_failed;}
int ready(void) {return lua_ready;}
int logs(void) {return messages;}
'''
 with tempfile.TemporaryDirectory() as tmp:
  c=Path(tmp)/'retry.c'; lib=Path(tmp)/'retry.dylib';c.write_text(pre+body+footer)
  subprocess.run(['/usr/bin/clang','-dynamiclib','-Wall','-Wextra','-Werror',str(c),'-o',str(lib)],check=True)
  lua=ctypes.CDLL(lua51.__file__); native=ctypes.CDLL(str(lib))
  lua.luaL_newstate.restype=ctypes.c_void_p
  for name,args,ret in [
   ('luaL_openlibs',[ctypes.c_void_p],None),('lua_close',[ctypes.c_void_p],None),
   ('luaL_loadstring',[ctypes.c_void_p,ctypes.c_char_p],ctypes.c_int),
   ('lua_pcall',[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int],ctypes.c_int),
   ('lua_gettop',[ctypes.c_void_p],ctypes.c_int),('lua_settop',[ctypes.c_void_p,ctypes.c_int],None),
   ('lua_tolstring',[ctypes.c_void_p,ctypes.c_int,ctypes.c_void_p],ctypes.c_char_p)]:
   f=getattr(lua,name);f.argtypes=args;f.restype=ret
  native.initialize.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
  native.invoke.argtypes=[ctypes.c_void_p,ctypes.c_uint]
  patch=b"attempts=(attempts or 0)+1;if not available then error('module not ready') end;return status or 'pending'"
  native.initialize(lua._handle,patch)
  state=lua.luaL_newstate();lua.luaL_openlibs(state);checks=[]
  def execute(code):
   assert lua.luaL_loadstring(state,code.encode())==0
   assert lua.lua_pcall(state,0,0,0)==0
  def call(ms):
   top=lua.lua_gettop(state)
   assert lua.luaL_loadstring(state,b"return 'original callback preserved'")==0
   assert native.invoke(state,ms)==0
   assert lua.lua_gettop(state)==top+1
   assert lua.lua_tolstring(state,-1,None)==b'original callback preserved'
   lua.lua_settop(state,top)
  try:
   call(250);assert native.failed()==1;execute('assert(attempts==1)');checks.append('initial error preserves original callback and stack')
   call(5249);execute('assert(attempts==1)');checks.append('five second error backoff')
   call(5250);execute('assert(attempts==2)');assert native.logs()==1;checks.append('persistent errors retry without log flooding')
   execute('available=true');call(10250);execute('assert(attempts==3)');assert native.failed()==0;checks.append('transient error recovers to pending')
   call(10499);execute('assert(attempts==3)');call(10500);execute('assert(attempts==4)');checks.append('normal pending interval restored')
   execute("status='ready'");call(10750);assert native.ready()==1;checks.append('recovered loader reaches ready')
   execute("package.loaded['ui.summonUI']={_localGoldRestore=function()end};package.loaded.ms={d_funUI={_localActivityEntryCurrent=function()return 'ready'end},d_twoYearsCelebrateUI={_localYuanshiCurrent=function()return 'ready'end}}")
   call(11000);execute('assert(attempts==5)');checks.append('ready modules skip redundant installation')
   execute('package.loaded.ms=nil;available=false');call(11250);assert native.failed()==1;execute('assert(attempts==6)')
   execute('available=true');call(16250);assert native.ready()==1;execute('assert(attempts==7)');checks.append('reload failure also recovers')
  finally:lua.lua_close(state)
 report=dict(passed=True,checks=checks,native_source_sha256=hashlib.sha256(source.encode()).hexdigest(),scope='Actual C loader compiled for host, real Lua 5.1, simulated monotonic clock; not Guangsu device validation')
 out=ROOT/'analysis/evidence/v110/guangsu-retry-20261106';out.mkdir(parents=True,exist_ok=True)
 (out/'native-retry-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
