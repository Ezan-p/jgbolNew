"""Native request/result contract; detached role, captured sends, no player writes."""
import json
from pathlib import Path
import sys
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT/'analysis/tools')]
from network_redirect import summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode
from android_emulator.config import load_config
from observability.collector import processes


def fixture():
    with tempfile.TemporaryDirectory() as tmp:
        b = Backend(Path(tmp), 18770, lambda *a, **k: None)
        try:
            role = b.profile()
            role.update(level=80, gold_coin=100000)
            b.save(role)
            b.respond(encode(1301, dict(serial_num=1, id=1, data=summon.lua(dict(union_name='道具验证仙盟')))), {'authenticated': True})
            rows = []
            for serial, (tid, count) in enumerate(((1020,1), (1029,1), (1029,15), (1022,1), (1023,1)), 2):
                role = b.profile()
                summon.add_item(role, tid, count)
                b.save(role)
                ident = next(i['id'] for i in role['attachments'] if i['type_id'] == tid)
                replies = b.respond(encode(1051, dict(serial_num=serial, item_type=tid, item_id=ident,
                    item_count=count, des_type=1, des_id=0)), {'authenticated': True})
                result = next(login_fields(d['data']) for m, _, d in map(decode, replies) if m == 2998 and d['id'] == 21)
                rows.append(dict(tid=tid, count=count, result=result))
            return rows
        finally:
            b.close()


def main():
    import frida
    source = 'local FIXTURE='+summon.lua(fixture())+'\n'+(ROOT/'analysis/tools/consumable_client_harness.lua').read_text()
    config = load_config(ROOT/'game.json')
    pid = next(p for p,n in processes(config).items() if n == config['package'])
    session = frida.get_device(config['serial'],timeout=10).attach(pid)
    js = r'''
const m=Process.getModuleByName('libxiyoujilua.so');
const f=(n,r,a)=>new NativeFunction(m.getExportByName(n),r,a);
const top=f('lua_gettop','int',['pointer']),set=f('lua_settop','void',['pointer','int']);
const load=f('luaL_loadbuffer','int',['pointer','pointer','uint','pointer']);
const call=f('lua_pcall','int',['pointer','int','int','int']);
const str=f('lua_tolstring','pointer',['pointer','int','pointer']);
let done=false;
Interceptor.attach(m.getExportByName('lua_pcall'),{onEnter(args){
 if(done)return;done=true;const L=args[0],old=top(L);
 try{const code=SOURCE;let status=load(L,Memory.allocUtf8String(code),unescape(encodeURIComponent(code)).length,Memory.allocUtf8String('@consumable-regression'));
 if(!status)status=call(L,0,1,0);const p=str(L,-1,ptr(0));send({status:status,result:p.isNull()?'':p.readUtf8String()});
 }catch(e){send({error:String(e)});}finally{set(L,old);}
}});
'''.replace('SOURCE', json.dumps(source))
    done = threading.Event()
    messages = []
    def receive(message, data):
        messages.append(message)
        done.set()
    script = session.create_script(js)
    script.on('message', receive)
    try:
        script.load()
        done.wait(30)
    finally:
        script.unload()
        session.detach()
    report = {}
    for message in messages:
        payload = message.get('payload', {})
        if payload.get('status') == 0:
            report = login_fields(payload['result'])
    checks = list(report.get('checks', {}).values())
    report.update(checks=checks, native_cocos=True, live_account_resources_changed=False)
    report['passed'] = len(checks) == 12 and all(c['passed'] for c in checks) and report.get('restored', False) and not report.get('error')
    if not report['passed']:
        report['raw'] = messages
    out = ROOT/'analysis/evidence/consumables/client_validation.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not report['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
