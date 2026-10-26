"""Run the isolated guild response/callback fixture in the original Cocos client.

All sends are intercepted, all backend writes use a temporary SQLite database,
and the original player/config/send references are restored even on timeout.
"""
import json
from pathlib import Path
import runpy
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from android_emulator.config import load_config
from observability.collector import processes
from network_redirect.backend import login_fields


def main():
    import frida
    runpy.run_path(str(ROOT/'analysis/tools/build_guild_client_fixture.py'))
    source=(ROOT/'.runtime/guild-fixture.lua').read_text()
    config=load_config(ROOT/'game.json')
    device=frida.get_device(config['serial'],timeout=10)
    pid=next(p for p,n in processes(config).items() if n==config['package'])
    session=device.attach(pid)
    js=r'''
const m=Process.getModuleByName('libxiyoujilua.so');
const f=(n,r,a)=>new NativeFunction(m.getExportByName(n),r,a);
const top=f('lua_gettop','int',['pointer']),set=f('lua_settop','void',['pointer','int']);
const load=f('luaL_loadbuffer','int',['pointer','pointer','uint','pointer']);
const call=f('lua_pcall','int',['pointer','int','int','int']);
const str=f('lua_tolstring','pointer',['pointer','int','pointer']);
let busy=false,pending=null;
Interceptor.attach(m.getExportByName('lua_pcall'),{onEnter(args){
 if(busy||pending===null)return;busy=true;
 const task=pending;pending=null;const L=args[0],old=top(L);
 try{const code=task.code;let status=load(L,Memory.allocUtf8String(code),unescape(encodeURIComponent(code)).length,Memory.allocUtf8String('@guild-regression'));
 if(!status)status=call(L,0,1,0);const p=str(L,-1,ptr(0));task.resolve({status:status,result:p.isNull()?'':p.readUtf8String()});
 }catch(e){task.resolve({error:String(e)});}finally{set(L,old);busy=false;}
}});
rpc.exports.evaluate=function(code){return new Promise(resolve=>{if(pending!==null)throw Error('evaluation already queued');pending={code,resolve};});};
'''
    script=session.create_script(js);raw=[];state={};started=False
    def evaluate(code):
        answer=script.exports_sync.evaluate(code);raw.append(answer)
        if answer.get('status')!=0:raise RuntimeError(answer)
        return answer['result']
    try:
        script.load()
        evaluate("assert(not guild_fixture_restore,'a guild fixture is already active');return 'ready'")
        evaluate(source);started=True
        stop=time.monotonic()+120
        while time.monotonic()<stop:
            time.sleep(.5)
            state=login_fields(evaluate("return table.tostring({results=guild_fixture_results or {},restored=guild_fixture_restored or false,expected=guild_fixture_case_count or 0})"))
            if state.get('restored'):break
    finally:
        if started and not state.get('restored'):
            try:evaluate("if guild_fixture_restore then guild_fixture_restore() end;return tostring(guild_fixture_restored)")
            except Exception as error:raw.append(dict(restore_error=str(error)))
        script.unload();session.detach()
    checks=list(state.get('results',{}).values())
    passed=bool(state.get('restored') and state.get('expected') and len(checks)==state['expected'] and all(c['ok'] for c in checks))
    report=dict(passed=passed,checks=checks,expected=state.get('expected',0),restored=state.get('restored',False),
                native_cocos=True,network_sends_captured=True,live_account_resources_changed=False,
                coverage='Original callbacks, timed store refresh, management responses and NPC team selection; not exhaustive human button/animation testing.')
    if not passed:report['last_runtime_messages']=raw[-3:]
    path=ROOT/'analysis/evidence/guild/current_client_validation.json'
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(f'{sum(bool(c["ok"]) for c in checks)}/{len(checks)} original Cocos checks passed; restored={report["restored"]}',flush=True)
    for c in checks:
        if not c['ok']:print(c['name'],c['error'],flush=True)
    if not passed:raise SystemExit(1)

if __name__=='__main__':main()
