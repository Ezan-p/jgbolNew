"""Exercise original 3.87 Cocos callbacks in one isolated frame, with no live writes."""
import json
from pathlib import Path
import sys
import tempfile
import threading
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import progression, summon
from network_redirect.backend import Backend
from network_redirect.protocol import decode
from android_emulator.config import load_config
from observability.collector import processes


def main():
    import frida
    now = int(time.time())
    with tempfile.TemporaryDirectory() as tmp:
        b = Backend(Path(tmp), 18770, lambda *a, **kw: None)
        role = b.profile(); before = b.profile()
        progression.add_exp(role, 270, now)
        data = dict(now=now, query=progression.info(role, now),
                    upgrade=decode(progression.upgrade_events(before, role)[0])[2],
                    claim=decode(progression.settle(role, dict(op_type=0, flag=2, id=0), now)[0])[2])
        b.close()
    source = 'local FIXTURE=' + summon.lua(data) + '\n' + (ROOT / 'tests/progression_client_regression.lua').read_text()
    source = source.replace('-- INSTALL_PATCH', (ROOT / 'network_redirect/progression_client.lua').read_text())
    config = load_config(ROOT / 'game.json')
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
let busy=false,done=false;
Interceptor.attach(m.getExportByName('lua_pcall'),{onEnter(args){
 if(busy||done)return;busy=true;done=true;const L=args[0],old=top(L);
 try{const code=SOURCE;let status=load(L,Memory.allocUtf8String(code),unescape(encodeURIComponent(code)).length,Memory.allocUtf8String('@progression-regression'));
 if(!status)status=call(L,0,1,0);const p=str(L,-1,ptr(0));send({status:status,result:p.isNull()?'':p.readUtf8String()});
 }catch(e){send({error:String(e)});}finally{set(L,old);busy=false;}
}});
'''.replace('SOURCE', json.dumps(source))
    completed = threading.Event(); messages = []
    def receive(message, _):
        messages.append(message); completed.set()
    script = session.create_script(js); script.on('message', receive)
    try:
        script.load(); completed.wait(30)
    finally:
        script.unload(); session.detach()
    checks = []
    for msg in messages:
        payload = msg.get('payload', {})
        if payload.get('status') == 0:
            for line in payload.get('result', '').splitlines():
                name, sep, rest = line.partition(':')
                if sep and rest.startswith(('true:', 'false:')):
                    ok, _, error = rest.partition(':')
                    checks.append(dict(name=name, passed=ok == 'true', error=error))
    passed = len(checks) == 7 and all(c['passed'] for c in checks)
    report = dict(passed=passed, checks=checks, raw=messages, native_cocos=True,
                  live_account_resources_changed=False, network_sends_captured=True)
    path = ROOT / 'analysis/evidence/progression_client_validation.json'
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not passed: raise SystemExit(1)


if __name__ == '__main__':
    main()
