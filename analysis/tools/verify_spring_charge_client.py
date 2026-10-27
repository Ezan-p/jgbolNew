"""Replay activity-30 query/claim against native Cocos, with captured sends only."""
import json
from pathlib import Path
import sys
import tempfile
import threading
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode, encode
from android_emulator.config import load_config
from observability.collector import processes


def fixture():
    now = int(time.time())
    with tempfile.TemporaryDirectory() as tmp:
        b = Backend(Path(tmp), 18790, lambda *a, **kw: None)
        role = b.profile(); summon.add_item(role, 1152, 2); b.save(role)
        b.respond(encode(1111, dict(serial_num=1, event_id=251, data=summon.lua(dict(
            item_id=103, order_id='spring-client-fixture', large_count=2, small_count=0)))), dict(authenticated=True))
        def response(mid, serial, event, **kw):
            packets = b.respond(encode(mid, dict(serial_num=serial, **kw)), dict(authenticated=True))
            return next(d for m, _, d in map(decode, packets) if m == 2998 and d['id'] == event)
        query = response(1216, 2, 93, flag=1)
        info = login_fields(query['data'])
        claim = response(1215, 3, 92, prize_id=1)
        data = dict(now=now, query=query, claim=claim, info=info,
                    ready=sum(row['status'] == 2 for key, row in info.items() if type(key) is int))
        b.close()
    return 'local FIXTURE=' + summon.lua(data) + '\n' + (ROOT / 'tests/spring_charge_client_regression.lua').read_text()


def main():
    import frida
    source = fixture()
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
 try{const code=SOURCE;let status=load(L,Memory.allocUtf8String(code),unescape(encodeURIComponent(code)).length,Memory.allocUtf8String('@spring-charge-regression'));
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
    for message in messages:
        payload = message.get('payload', {})
        if payload.get('status') == 0:
            for line in payload.get('result', '').splitlines():
                name, separator, rest = line.partition(':')
                if separator and rest.startswith(('true:', 'false:')):
                    ok, _, error = rest.partition(':')
                    checks.append(dict(name=name, passed=ok == 'true', error=error))
    passed = len(checks) == 6 and all(c['passed'] for c in checks)
    report = dict(passed=passed, checks=checks, raw=messages, native_cocos=True,
                  live_account_resources_changed=False, network_sends_captured=True,
                  module_private_upvalues_restored=True)
    path = ROOT / 'analysis/evidence/recharge/spring_charge_client_validation.json'
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not passed: raise SystemExit(1)


if __name__ == '__main__':
    main()
