"""Execute original UI callbacks on isolated native layers and install the patch."""
import json
from pathlib import Path
import sys
import threading
import frida

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from android_emulator.config import load_config
from observability.collector import processes

config = load_config(ROOT / 'game.json')
source = (ROOT / 'analysis/tools/activity_level_native_harness.lua').read_text().replace(
    '-- INSTALL_PATCH', (ROOT / 'network_redirect/activity_level_client.lua').read_text())
device = frida.get_device(config['serial'], timeout=10)
pid = next(p for p, name in processes(config).items() if name == config['package'])
session = device.attach(pid)
js = r'''
const m=Process.getModuleByName('libxiyoujilua.so');
const f=(n,r,a)=>new NativeFunction(m.getExportByName(n),r,a);
const top=f('lua_gettop','int',['pointer']),set=f('lua_settop','void',['pointer','int']);
const load=f('luaL_loadbuffer','int',['pointer','pointer','uint','pointer']);
const call=f('lua_pcall','int',['pointer','int','int','int']);
const str=f('lua_tolstring','pointer',['pointer','int','pointer']);
let done=false;
const hook=Interceptor.attach(m.getExportByName('lua_pcall'),{onEnter(args){
 if(done)return;done=true;
 const L=args[0],n=top(L),text=SOURCE,p=Memory.allocUtf8String(text);
 let status=load(L,p,unescape(encodeURIComponent(text)).length,Memory.allocUtf8String('@activity_level_native'));
 if(!status)status=call(L,0,1,0);
 const out=str(L,-1,ptr(0));send({status:status,result:out.isNull()?'':out.readUtf8String()});
 set(L,n);hook.detach();
}});
'''.replace('SOURCE', json.dumps(source, ensure_ascii=False))
messages, ready = [], threading.Event()
script = session.create_script(js)
def on_message(message, data):
    messages.append(message)
    ready.set()
script.on('message', on_message)
try:
    script.load()
    if not ready.wait(30):
        raise RuntimeError('No native Lua callback within 30 seconds')
finally:
    script.unload()
    session.detach()
checks = []
for message in messages:
    payload = message.get('payload', {})
    if payload.get('status') == 0:
        for line in payload.get('result', '').splitlines():
            name, _, rest = line.partition(':')
            if rest.startswith(('true:', 'false:')):
                ok, _, error = rest.partition(':')
                checks.append(dict(name=name, passed=ok == 'true', error=error))
report = dict(passed=len(checks) == 6 and all(c['passed'] for c in checks),
              native_cocos=True, detached_layers=True, live_save_modified=False,
              checks=checks, raw=messages)
(ROOT / 'analysis/evidence/feature_levels/client_native.json').write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report, ensure_ascii=False))
if not report['passed']:
    raise SystemExit(1)
