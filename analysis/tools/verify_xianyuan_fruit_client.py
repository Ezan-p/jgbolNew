"""Verify native 3.87 choice/preview/request/callback against a disposable backend."""
import json
from pathlib import Path
import sys
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT/'analysis/tools')]
from network_redirect import summon, xianyuan_fruit
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode
from android_emulator.config import load_config
from observability.collector import processes


def fixture():
    with tempfile.TemporaryDirectory() as tmp:
        b = Backend(Path(tmp), 18770, lambda *a, **k: None)
        try:
            cases = []
            for kind, target in ((10,5004), (10,5001), (5,5001), (5,5002), (5,5003), (5,5004), (5,5005)):
                for count in (1,15):
                    role = b.profile()
                    summon.add_item(role,1246,20)
                    b.save(role)
                    ident = next(i['id'] for i in role['attachments'] if i['type_id']==1246)
                    req = dict(serial_num=len(cases)+1,item_type=1246,item_id=ident,item_count=count,
                               des_type=kind,des_id=target)
                    replies = b.respond(encode(1051,req), {'authenticated':True})
                    event = [login_fields(d['data']) for m,_,d in map(decode,replies) if m==2998 and d['id']==21][0]
                    cases.append(dict(kind=kind,target=target,count=count,gain=event['attach_list'][1]['attach_count']))
            req.update(serial_num=len(cases)+1,item_count=3,des_type=10,des_id=5004)
            replies = b.respond(encode(1051,req), {'authenticated':True})
            result = [login_fields(d['data']) for m,_,d in map(decode,replies) if m==2998 and d['id']==21][0]
            config = login_fields(decode(b.bootstrap()[0])[2]['data'])
            return dict(catalog=config[xianyuan_fruit.CONFIG_SECTION],cases=cases,result=result)
        finally:
            b.close()


def main():
    import frida
    source = 'local FIXTURE='+summon.lua(fixture())+'\n'+(ROOT/'analysis/tools/xianyuan_fruit_client_harness.lua').read_text()
    config = load_config(ROOT/'game.json')
    pid = next(p for p,n in processes(config).items() if n==config['package'])
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
 try{const code=SOURCE;let status=load(L,Memory.allocUtf8String(code),unescape(encodeURIComponent(code)).length,Memory.allocUtf8String('@fruit-regression'));
 if(!status)status=call(L,0,1,0);const p=str(L,-1,ptr(0));send({status:status,result:p.isNull()?'':p.readUtf8String()});
 }catch(e){send({error:String(e)});}finally{set(L,old);}
}});
'''.replace('SOURCE',json.dumps(source))
    completed = threading.Event()
    messages = []
    def receive(message,data):
        messages.append(message)
        completed.set()
    script = session.create_script(js)
    script.on('message', receive)
    try:
        script.load()
        completed.wait(30)
    finally:
        script.unload()
        session.detach()
    report = {}
    for message in messages:
        payload = message.get('payload', {})
        if payload.get('status')==0:
            report = login_fields(payload['result'])
    checks = list(report.get('checks', {}).values())
    report['checks'] = checks
    report['passed'] = len(checks)==22 and all(c['passed'] for c in checks) and report.get('restored',False)
    if not report['passed']:
        report['raw'] = messages
    out = ROOT/'analysis/evidence/xianyuan_fruit/client_validation.json'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(f'{sum(c["passed"] for c in checks)}/{len(checks)} original Cocos checks passed; restored={report.get("restored",False)}')
    for c in checks:
        if not c['passed']:
            print(c['name'],c['error'])
    if not report['passed']:
        raise SystemExit(1)


if __name__=='__main__':
    main()
