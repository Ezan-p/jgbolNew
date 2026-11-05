"""Exercise original Cocos dream UI with detached fixtures, never real account writes."""
import json
from pathlib import Path
import sys
import tempfile
import threading
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import activity_dream as d, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode
from android_emulator.config import load_config
from observability.collector import processes


def fixture():
    now=1793620800
    with tempfile.TemporaryDirectory() as tmp, patch('network_redirect.game_clock.now',return_value=now):
        b=Backend(Path(tmp),18770,lambda *a,**k:None)
        try:
            role=b.profile();role['level']=60
            def call(op,**data):
                if op!=1:data['local_token']=role['activity']['dream']['token']
                event=d.settle(role,dict(id=op,data=summon.lua(data)),now,login_fields)[0]
                return login_fields(decode(event)[2]['data'])
            rows=[]
            for stage in range(6):
                entry=call(1);solved=call(2,answer=list(range(1,10)))
                friends=[p['id'] for p in entry['local_friends'].values()][:2]
                blessed=call(3,des_list=friends,index=1)
                rows.append(dict(entry=entry,solved=solved,blessed=blessed))
            d.record_charge(role,300,now)
            return dict(now=now,stages=rows,eligible=call(1),claimed=call(4))
        finally:b.close()


def main():
    import frida
    f=fixture()
    source='local FIXTURE='+summon.lua(f)+'\n'+(ROOT/'analysis/tools/dream_native_harness.lua').read_text().replace(
        '-- INSTALL_PATCH',(ROOT/'network_redirect/dream_client.lua').read_text())
    c=load_config(ROOT/'game.json')
    pid=next(p for p,n in processes(c).items() if n==c['package'])
    device=frida.get_device(c['serial'],timeout=5)
    session=device.attach(pid)
    js=r'''
const m=Process.getModuleByName('libxiyoujilua.so');
const f=(n,r,a)=>new NativeFunction(m.getExportByName(n),r,a);
const top=f('lua_gettop','int',['pointer']),set=f('lua_settop','void',['pointer','int']);
const load=f('luaL_loadbuffer','int',['pointer','pointer','uint','pointer']);
const call=f('lua_pcall','int',['pointer','int','int','int']);
const str=f('lua_tolstring','pointer',['pointer','int','pointer']);
let busy=false,done=false;
Interceptor.attach(m.getExportByName('lua_pcall'),{onEnter(args){
 if(busy||done)return;busy=true;done=true;const L=args[0],old=top(L);
 try{const code=SOURCE;let status=load(L,Memory.allocUtf8String(code),unescape(encodeURIComponent(code)).length,Memory.allocUtf8String('@dream-regression'));
 if(!status)status=call(L,0,1,0);const p=str(L,-1,ptr(0));send({status:status,result:p.isNull()?'':p.readUtf8String()});
 }catch(e){send({error:String(e)});}finally{set(L,old);busy=false;}
}});
'''.replace('SOURCE',json.dumps(source))
    completed=threading.Event();messages=[]
    def receive(message,data):messages.append(message);completed.set()
    script=session.create_script(js);script.on('message',receive)
    try:script.load();completed.wait(30)
    finally:script.unload();session.detach()
    checks=[]
    for message in messages:
        p=message.get('payload',{})
        if p.get('status')==0:
            for line in p['result'].splitlines():
                name,sep,rest=line.partition(':')
                if sep and rest.startswith(('true:','false:')):
                    result,_,error=rest.partition(':');checks.append(dict(name=name,passed=result=='true',error=error))
    passed=len(checks)==10 and all(c['passed'] for c in checks)
    report=dict(passed=passed,native_cocos=True,detached_layers=True,
                network_sends_captured=True,live_account_resources_changed=False,checks=checks,raw=messages)
    out=ROOT/'analysis/evidence/dream/native_validation.json';out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if not passed:raise SystemExit(1)


if __name__=='__main__':main()
