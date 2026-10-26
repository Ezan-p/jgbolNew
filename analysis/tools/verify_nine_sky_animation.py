"""Timed native walk, automatic temporary-layer restoration, no account writes."""
import json
import sys
import threading
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from android_emulator.config import load_config
from observability.collector import processes
from build_nine_sky_client_fixture import main as build


def main():
    import frida
    build()
    fixture=(ROOT/'.runtime/nine-sky-native-fixture.lua').read_text().split('local ms=assert(package.loaded.ms)',1)[0]
    source=fixture+(ROOT/'analysis/tools/nine_sky_animation_harness.lua').read_text().replace('-- INSTALL_PATCH',(ROOT/'network_redirect/nine_sky_client.lua').read_text())
    config=load_config(ROOT/'game.json');device=frida.get_device(config['serial'],timeout=10)
    pid=next(p for p,n in processes(config).items() if n==config['package']);session=device.attach(pid)
    js=r'''
const m=Process.getModuleByName('libxiyoujilua.so');
const f=(n,r,a)=>new NativeFunction(m.getExportByName(n),r,a);
const top=f('lua_gettop','int',['pointer']),set=f('lua_settop','void',['pointer','int']);
const load=f('luaL_loadbuffer','int',['pointer','pointer','uint','pointer']);
const call=f('lua_pcall','int',['pointer','int','int','int']);
const str=f('lua_tolstring','pointer',['pointer','int','pointer']);
let busy=false,started=false,done=false,last=0;
Interceptor.attach(m.getExportByName('lua_pcall'),{onEnter(args){
 if(busy||done||Date.now()-last<500)return;busy=true;last=Date.now();const L=args[0],old=top(L);
 try{
 if(!started){
  const gate='local ms=package.loaded.ms; return ms and ms.d_towerUI and ms.d_mainUI and ms.d_mainUI.g_playerInfo and ms.d_mainUI.g_playerInfo.role_id and "READY" or "WAIT"';
  let check=load(L,Memory.allocUtf8String(gate),gate.length,Memory.allocUtf8String('@nine-gate'));
  if(!check)check=call(L,0,1,0);const q=str(L,-1,ptr(0));const ready=!check&&!q.isNull()&&q.readUtf8String()==='READY';set(L,old);if(!ready)return;
 }
 const code=started?'return nine_sky_animation_result or "WAIT"':SOURCE;started=true;
 let status=load(L,Memory.allocUtf8String(code),unescape(encodeURIComponent(code)).length,Memory.allocUtf8String('@nine-sky-animation'));
 if(!status)status=call(L,0,1,0);const p=str(L,-1,ptr(0));const result=p.isNull()?'':p.readUtf8String();
 if(status||result.startsWith('PASS:')||result.startsWith('FAIL:')){done=true;send({status,result});}
 }catch(e){done=true;send({error:String(e)});}finally{set(L,old);busy=false;}
}});
'''.replace('SOURCE',json.dumps(source))
    completed=threading.Event();messages=[]
    def receive(message,data):messages.append(message);completed.set()
    script=session.create_script(js);script.on('message',receive)
    try:script.load();completed.wait(58)
    finally:script.unload();session.detach()
    passed=any(m.get('payload',{}).get('result','').startswith('PASS:') for m in messages)
    report=dict(passed=passed,native_timed_animation=True,ten_rolls=True,account_resources_changed=False,raw=messages)
    (ROOT/'analysis/evidence/nine_sky/animation_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))
    if not passed:raise SystemExit(1)

if __name__=='__main__':main()
